# -*- coding: utf-8 -*-
"""
/***************************************************************************
                                ARK Spatial
                    A QGIS plugin for Archaeological Recording.
        Part of the Archaeological Recording Kit by L-P : Archaeology
                        http://ark.lparchaeology.com
                              -------------------
        copyright            : 2017 by L-P : Heritage LLP
        email                : ark@lparchaeology.com
        copyright            : 2017 by John Layt
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

from PyQt4.QtCore import (QCoreApplication, QDir, QFile, QFileInfo, QIODevice, QObject, QPointF, QProcess, QSettings,
                          QTextStream, pyqtSignal)
from PyQt4.QtGui import QPixmap

from qgis.core import QgsPoint

from ArkSpatial.ark.lib.core import ProcessStatus
from ArkSpatial.ark.lib.utils import debug

from .gcp import GroundControlPoint
from .transform import Transform


class Georeferencer(QObject):

    # Step enum
    Start = 0
    Crop = 1
    Translate = 2
    Warp = 3
    Overview = 4
    Stop = 5
    Step = [0, 1, 2, 3, 4, 5]
    Label = ['Start', 'Crop', 'Translate', 'Warp', 'Overview', 'Stop']

    # Georeferencer.Step, ProcessStatus
    status = pyqtSignal(int, int)
    # Georeferencer.Step, Message
    error = pyqtSignal(int, str)

    # Internal variables
    _debug = True
    _gdalDir = QDir()
    _step = 0
    _status = 0
    _translate = QFileInfo()
    _warp = QFileInfo()
    _overview = QFileInfo()
    _command = ''
    _args = ''
    _process = QProcess()

    _gc = Transform()
    _rawFile = QFileInfo()
    _pointFile = QFileInfo()
    _cropFile = QFileInfo()
    _translateFile = QFileInfo()
    _geoFile = QFileInfo()

    def __init__(self, parent=None):
        super(Georeferencer, self).__init__(parent)

        self._cropFile.setFile(QDir.tempPath() + '.ark_georef_crop.png')
        self._translateFile = QFileInfo(QDir.tempPath() + '.ark_georef_translate.tiff')

        self._gdalDir = QDir(self.gdalPath())
        if self._debug:
            debug('GDAL Path: ' + self._gdalDir.absolutePath())
        self._translate.setFile(self._gdalDir, 'gdal_translate')
        self._warp.setFile(self._gdalDir, 'gdalwarp')
        self._overview.setFile(self._gdalDir, 'gdaladdo')
        if (not self._translate.exists() or not self._warp.exists() or not self._overview.exists()):
            self._signalError(
                'GDAL commands not found, please ensure GDAL Tools plugin is installed and has correct path set!')
            return

        self._process.started.connect(self._processStarted)
        self._process.finished.connect(self._processFinished)
        self._process.error.connect(self._processError)
        self._process.readyReadStandardError.connect(self._processError)

    def step(self):
        return self._step

    def processStatus(self):
        return self._status

    def run(self, gc, rawFile, pointFile, geoFile):
        self._step = Georeferencer.Start
        if (not gc.isValid()):
            self._signalError('Invalid ground control points.')
            return
        self._gc = gc

        if (not rawFile.exists()):
            self._signalError('Raw file not found.')
            return
        self._rawFile = rawFile

        self._pointFile = pointFile
        self._geoFile = geoFile

        if (self._debug):
            debug('Raw File: \'' + self._rawFile.absoluteFilePath() + '\'')
            debug('GCP File: \'' + self._pointFile.absoluteFilePath() + '\'')
            debug('Geo File: \'' + self._geoFile.absoluteFilePath() + '\'')

        QCoreApplication.processEvents()
        self._runCropStep()

    def _runCropStep(self):
        if self._debug:
            debug('Crop')
        self._step = Georeferencer.Crop
        self._args = []
        self._command = ''
        pixmap = QPixmap(self._rawFile.absoluteFilePath())
        if pixmap.isNull():
            self._signalError('Loading of raw image failed.')
            return
        pixmap = pixmap.copy(0, 0, pixmap.width(), int(pixmap.height() * 0.84))
        image = pixmap.toImage()
        if image.isNull():
            self._signalError('Cropping of raw image failed.')
            return
        if not image.save(self._cropFile.absoluteFilePath(), 'PNG', 100):
            self._signalError('Saving of cropped image failed.')
            return
        self._signalStatus()
        self._runTranslateStep()

    def _runTranslateStep(self):
        self._step = Georeferencer.Translate
        self._args = []
        self._args.extend(['-of', 'GTiff'])
        self._args.extend(['-a_srs', self._gc.crs])
        self._args.extend(['-gcp', str(self._gc.point(1).raw().x()), str(self._gc.point(1).raw().y()),
                           str(self._gc.point(1).map().x()), str(self._gc.point(1).map().y())])
        self._args.extend(['-gcp', str(self._gc.point(2).raw().x()), str(self._gc.point(2).raw().y()),
                           str(self._gc.point(2).map().x()), str(self._gc.point(2).map().y())])
        self._args.extend(['-gcp', str(self._gc.point(3).raw().x()), str(self._gc.point(3).raw().y()),
                           str(self._gc.point(3).map().x()), str(self._gc.point(3).map().y())])
        self._args.extend(['-gcp', str(self._gc.point(4).raw().x()), str(self._gc.point(4).raw().y()),
                           str(self._gc.point(4).map().x()), str(self._gc.point(4).map().y())])
        self._args.append(self._cropFile.absoluteFilePath())
        self._args.append(self._translateFile.absoluteFilePath())
        self._command = self._translate.absoluteFilePath() + ' ' + ' '.join(self._args)
        self._process.start(self._translate.absoluteFilePath(), self._args)

    def _runWarpStep(self):
        self._step = Georeferencer.Warp
        self._args = []
        self._args.extend(['-order', '1'])
        self._args.extend(['-r', 'cubic'])
        self._args.extend(['-t_srs', self._gc.crs])
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
        self._status = ProcessStatus.Running
        self._signalStatus()
        if self._debug:
            debug(self.Label[self._step])
            debug(self._command)

    def _processFinished(self):
        self._status = ProcessStatus.Success
        self._signalStatus()
        if (self._step == Georeferencer.Translate):
            self._runWarpStep()
        elif (self._step == Georeferencer.Warp):
            self._runOverviewStep()
        elif (self._step == Georeferencer.Overview):
            self.writeGcpFile(self._gc, self._pointFile.absoluteFilePath())
            self._step = Georeferencer.Stop
            self._signalStatus()

    def _processError(self):
        self._status = ProcessStatus.Failure
        msg = str(self._process.readAllStandardError())
        debug(msg)
        self._signalError(msg)

    def _signalStatus(self):
        self.status.emit(self._step, self._status)

    def _signalError(self, msg):
        self.error.emit(self._step, msg)

    @staticmethod
    def gdalPath():
        return QSettings().value('/GdalTools/gdalPath', '/usr/bin')

    @staticmethod
    def loadGcpFile(path):
        inFile = QFile(path)
        if (not inFile.open(QIODevice.ReadOnly | QIODevice.Text)):
            return 'ERROR: Unable to open GCP file for reading'
        inStream = QTextStream(inFile)
        line = inStream.readLine()
        # Skip the header line if found
        if (line == 'mapX,mapY,pixelX,pixelY,enable'):
            line = inStream.readLine()
        lines = 0
        gc = Transform()
        while (line):
            lines += 1
            vals = line.split(',')
            if (len(vals) != 5):
                return None
            map = QgsPoint(float(vals[0]), float(vals[1]))
            raw = QPointF(float(vals[2]), float(vals[3]))
            enabled = bool(vals[4])
            point = GroundControlPoint(raw, map, enabled)
            gc.setPoint(lines, point)
            line = inStream.readLine()
        inFile.close()
        return gc

    @staticmethod
    def writeGcpFile(gc, path):
        outFile = QFile(path)
        if (not outFile.open(QIODevice.WriteOnly | QIODevice.Text)):
            return 'Unable to open GCP file for writing'
        outStream = QTextStream(outFile)
        outStream << gc.asCsv()
        outFile.close()
