# -*- coding: utf-8 -*-
"""
/***************************************************************************
                                ARK Spatial
                    A QGIS plugin for Archaeological Recording.
        Part of the Archaeological Recording Kit by L-P : Archaeology
                        http://ark.lparchaeology.com
                              -------------------
        begin                : 2014-12-07
        git sha              : $Format:%H$
        copyright            : 2014, 2015 by L-P : Heritage LLP
        email                : ark@lparchaeology.com
        copyright            : 2014, 2015 by John Layt
        email                : john@layt.net
 ***************************************************************************/

/***************************************************************************
 *                                                                         *
 *   This program is free software; you can redistribute it and/or modify  *
 *   it under the terms of the GNU General Public License as published by  *
 *   the Free Software Foundation; either version 2 of the License, or     *
 *   (at your option) any later version.                                   *
 *                                                                         *
 ***************************************************************************/
"""

from PyQt4.QtCore import Qt, QFileInfo, QPointF, QProcess, QSettings, QDir, QTextStream, QFile, QIODevice, QCoreApplication, pyqtSignal
from PyQt4.QtGui import QPixmap

from qgis.core import QgsPoint

from gcp import *

class ProcessStatus():

    Unknown = 0
    Running = 1
    Success = 2
    Failure = 3

class Georeferencer(QObject):

    Start = 0
    Crop = 1
    Translate = 2
    Warp = 3
    Overview = 4
    Stop = 0

    status = pyqtSignal(int, int)
    error = pyqtSignal(int, str)

    # Internal variables
    _tmpDir = QDir()
    _gdalDir = QDir()
    _step = Georeferencer.Start
    _translate = QFileInfo()
    _warp = QFileInfo()
    _overview = QFileInfo()
    _command = ''
    _args = ''
    _process = QProcess()

    _gc = GroundControl()
    _rawFile = QFileInfo()
    _pointFile = QFileInfo()
    _cropFile = QFileInfo()
    _translateFile = QFileInfo()
    _geoFile = QFileInfo()

    def __init__(self, tmpDir):

        self._tmpDir = tmpDir
        self._cropFile.setFile(self._tmpDir, '.georef_crop.png')
        self._translateFile = QFileInfo(self._tmpDir, + '.georef_translate.tiff')

        self._gdalDir = QDir(self.gdalPath())
        self.log('GDAL Path: ' + self._gdalDir.absolutePath())
        self._translate.setFile(gdalDir, 'gdal_translate')
        self._warp.setFile(gdalDir, 'gdalwarp')
        self._overview.setFile(gdalDir, 'gdaladdo')
        if (not self._translate.exists() or not self._warp.exists() or not self._overview.exists()):
            self.showStatus('ERROR: GDAL commands not found, please ensure GDAL Tools plugin is installed and has correct path set!')
            return

        self._process.started.connect(self._processStarted)
        self._process.finished.connect(self._processFinished)
        self._process.error.connect(self._processError)
        self._process.readyReadStandardError.connect(self._processError)

    def run(self, gc, rawFile, pointFile, geoFile):
        self._gc = gc
        if (!self._gc.isValid()):
            self._signalError('Invalid ground control points.')
            return

        self._rawFile = rawFile
        if (not self._rawFile.exists()):
            self._signalError('Raw file not found.')
            return

        self._pointFile = pointFile
        self._geoFile = geoFile

        if (False):
            self.log('Raw File: \'' + self._rawFile.absoluteFilePath() + '\'')
            self.log('GCP File: \'' + self._pointFile.absoluteFilePath() + '\'')
            self.log('Geo File: \'' + self._geoFile.absoluteFilePath() + '\'')

        QCoreApplication.processEvents()
        self._runCropStep()

    def _runCropStep(self):
        self._step = Georeferencer.Crop
        self._args = []
        self._command = ''
        pixmap = QPixmap(self._rawFile.absoluteFilePath())
        if pixmap.isNull():
            self._signalError('Loading of raw image failed.')
            return
        pixmap = pixmap.copy(0, 0, pixmap.width(), int(self.pixmap.height() * 0.84))
        image = pixmap.toImage()
        if image.isNull():
            self._signalError('Cropping of raw image failed.')
            return
        if !image.save(self._cropFile.absoluteFilePath(), 'PNG', 100):
            self._signalError('Saving of cropped image failed.')
            return
        self._runTranslateStep()

    def _runTranslateStep(self):
        self._step = Georeferencer.Translate
        self._args = []
        self._args.extend(['-of', 'GTiff'])
        self._args.extend(['-a_srs', self._gc.crt])
        self._args.extend(['-gcp', str(self._gc.point1.raw().x()), str(self._gc.point1.raw().y()), str(self._gc.point1.map().x()), str(self._gc.point1.map().y())])
        self._args.extend(['-gcp', str(self._gc.point2.raw().x()), str(self._gc.point2.raw().y()), str(self._gc.point2.map().x()), str(self._gc.point2.map().y())])
        self._args.extend(['-gcp', str(self._gc.point3.raw().x()), str(self._gc.point3.raw().y()), str(self._gc.point3.map().x()), str(self._gc.point3.map().y())])
        self._args.extend(['-gcp', str(self._gc.point4.raw().x()), str(self._gc.point4.raw().y()), str(self._gc.point4.map().x()), str(self._gc.point4.map().y())])
        self._args.append(self._cropFile.absoluteFilePath())
        self._args.append(self._translateFile.absoluteFilePath())
        self._command = self._translate.absoluteFilePath() + ' ' + ' '.join(self._args)
        self._process.start(self._translate.absoluteFilePath(), self._args)

    def _runWarpStep(self):
        self._step = Georeferencer.Warp
        self._args = []
        self._args.extend(['-order', '1'])
        self._args.extend(['-r', 'cubic'])
        self._args.extend(['-t_srs', self._crt])
        self._args.extend(['-of', 'GTiff'])
        self._args.extend(['-co', 'COMPRESS=JPEG'])
        self._args.extend(['-co', 'JPEG_QUALITY=50'])
        self._args.extend(['-co', 'TILED=YES'])
        self._args.append('-dstalpha')
        self._args.append('-overwrite')
        self._args.append('\"' + self._translateFile.absoluteFilePath() + '\"')
        self._args.append('\"' + self._geoFile.absoluteFilePath() + '\"')
        self._command = self._warp.absoluteFilePath() + ' ' + ' '.join(self._args)
        self._process.start(self._command)

    def _runOverviewStep(self):
        self._step = Georeferencer.Overview
        self._args = []
        self._args.extend(['--config', 'COMPRESS_OVERVIEW JPEG'])
        self._args.extend(['--config', 'INTERLEAVE_OVERVIEW PIXEL'])
        self._args.extend(['-r', 'cubic'])
        self._args.append('\"' + self._geoFile.absoluteFilePath() + '\"')
        self._args.append('2 4 8 16')
        self._command = self._overview.absoluteFilePath() + ' ' + ' '.join(self._args)
        self._process.start(self._command)

    def _processStarted(self):
        self._signalStatus(ProcessStatus.Running)
        self.log(self._command)

    def _processFinished(self):
        if (self._process.exitCode() != 0):
            if (self._step == Georeferencer.Translate):
                self._signalError('Translation failed.')
            elif (self._step == Georeferencer.Warp):
                self._signalError('Warp failed.')
            elif (self._step == Georeferencer.Overview):
                self._signalError('Overview failed.')
            self._step = Georeferencer.Stop
            return

        self._signalStatus(ProcessStatus.Success)
        if (self._step == Georeferencer.Translate):
            self._runWarpStep()
        elif (self._step == Georeferencer.Warp):
            self._step = Georeferencer.Overview
            self._runOverviewStep()
        elif (self._step == Georeferencer.Overview):
            self.writeGcpFile(self._gc, self._pointFile.absoluteFilePath())
            self._step = Georeferencer.Stop

    def _processError(self):
        msg = str(self._process.readAllStandardError())
        self.log(msg)
        self._signalError(msg)

    def _signalStatus(self, status):
        self.status.emit(self._step, status)

    def _signalError(self, msg):
        self.error.emit(self._step, msg)

    @staticmethod
    def gdalPath(self):
        return QSettings().value('/GdalTools/gdalPath', '/usr/bin')

    @staticmethod
    def log(msg):
        QgsMessageLog.logMessage(str(msg), 'ARK', QgsMessageLog.INFO)

    @staticmethod
    def loadGcpFile(self, path):
        inFile = QFile(path)
        if (not inFile.open(QIODevice.ReadOnly | QIODevice.Text)):
            return 'ERROR: Unable to open GCP file for reading'
        inStream = QTextStream(inFile)
        line = inStream.readLine()
        self.log(line)
        # Skip the header line if found
        if (line == 'mapX,mapY,pixelX,pixelY,enable'):
            line = inStream.readLine()
            self.log(line)
        lines = 0
        gc = GroundControl
        while (line):
            lines += 1
            vals = line.split(',')
            if (len(vals) != 5):
                self.log('not 5 vals')
                return None
            map = QPointF(float(vals[0]), float(vals[1]))
            raw = QPointF(float(vals[2]), float(vals[3]))
            enabled = bool(vals[4])
            point = GroundControlPoint(raw, map, enabled)
            gc.setPoint(lines, point)
            line = inStream.readLine()
            self.log(line)
        inFile.close()
        self.log('lines used = ' + str(lines))
        return gc

    @staticmethod
    def writeGcpFile(gcp, path):
        outFile = QFile(path)
        if (not outFile.open(QIODevice.WriteOnly | QIODevice.Text)):
            return 'Unable to open GCP file for writing'
        outStream = QTextStream(outFile)
        outStream << 'mapX,mapY,pixelX,pixelY,enable\n'
        for index in sorted(gcp.points()):
            point = gcp.point(index)
            line = ','.join([str(point.map().x()), str(point.map().y()), str(point.raw().x()), str(point.raw().y()), str(int(point.enabled()))])
            outStream << line << '\n'
        outFile.close()
        return ''
