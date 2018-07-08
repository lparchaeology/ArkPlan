# -*- coding: utf-8 -*-
"""
/***************************************************************************
                                ARKspatial
                    A QGIS plugin for Archaeological Recording.
        Part of the Archaeological Recording Kit by L - P : Archaeology
                        http://ark.lparchaeology.com
                              -------------------
        copyright            : 2017 by L - P : Heritage LLP
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

from enum import Enum

from qgis.PyQt.QtCore import (QCoreApplication, QDir, QFile, QFileInfo, QIODevice, QObject, QPointF, QProcess,
                              QSettings, QTextStream, pyqtSignal)
from qgis.PyQt.QtGui import QPixmap

from qgis.core import QgsPoint

from ArkSpatial.ark.lib import utils
from ArkSpatial.ark.lib.core import ProcessStatus
from ArkSpatial.ark.lib.utils import debug

from .gcp import GroundControlPoint
from .transform import Transform


class GeoreferenceStep(Enum):

    Start = (0, 'Start')
    Crop = (1, 'Crop')
    Translate = (2, 'Translate')
    Warp = (3, 'Warp')
    Overview = (4, 'Overview')
    Stop = (5, 'Stop')

    def __new__(cls, value, label):
        obj = object.__new__(cls)
        obj._value_ = value
        obj.label = label
        return obj


class Georeferencer(QObject):

    # GeoreferenceStep, ProcessStatus
    status = pyqtSignal(GeoreferenceStep, ProcessStatus)
    # GeoreferenceStep, Message
    error = pyqtSignal(GeoreferenceStep, str)

    def __init__(self, parent=None):
        super(Georeferencer, self).__init__(parent)

        # Internal variables
        self._debug = True
        self._gdalDir = QDir()
        self._step = GeoreferenceStep.Start
        self._status = ProcessStatus.Unknown
        self._translate = QFileInfo()
        self._warp = QFileInfo()
        self._overview = QFileInfo()
        self._command = ''
        self._args = ''
        self._process = QProcess()
        self._gc = Transform()
        self._rawFile = QFileInfo()
        self._pointFile = QFileInfo()
        self._cropFile = QFileInfo()
        self._translateFile = QFileInfo()
        self._geoFile = QFileInfo()

        tempDir = QDir.temp()
        self._cropFile.setFile(tempDir.absoluteFilePath('.ark_georef_crop.png'))
        self._translateFile = QFileInfo(tempDir.absoluteFilePath('.ark_georef_translate.tiff'))

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
        self._step = GeoreferenceStep.Start
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
        if not self._geoFile.absoluteDir().exists():
            self._geoFile.absoluteDir().mkpath('.')

        if (self._debug):
            debug('Raw File: \'' + self._rawFile.absoluteFilePath() + '\'')
            debug('GCP File: \'' + self._pointFile.absoluteFilePath() + '\'')
            debug('Crop File: \'' + self._cropFile.absoluteFilePath() + '\'')
            debug('Translate File: \'' + self._translateFile.absoluteFilePath() + '\'')
            debug('Geo File: \'' + self._geoFile.absoluteFilePath() + '\'')

        QCoreApplication.processEvents()
        self._runCropStep()

    def _runCropStep(self):
        if self._debug:
            debug('Crop')
        self._step = GeoreferenceStep.Crop
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

    def _formatGcp(self, point):
        point = self._gc.point(point)
        return "{0:f} {1:f} {2:f} {3:f}".format(point.raw().x(), point.raw().y(), point.map().x(), point.map().y())

    def _runTranslateStep(self):
        self._step = GeoreferenceStep.Translate
        self._args = []
        self._args.extend(['-of', 'GTiff'])
        self._args.extend(['-a_srs', self._gc.crs])
        # self._args.extend(['-gcp', self._formatGcp(1)])
        # self._args.extend(['-gcp', self._formatGcp(2)])
        # self._args.extend(['-gcp', self._formatGcp(3)])
        # self._args.extend(['-gcp', self._formatGcp(4)])
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
        self._step = GeoreferenceStep.Warp
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
        self._step = GeoreferenceStep.Overview
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
        if (self._step == GeoreferenceStep.Translate):
            self._runWarpStep()
        elif (self._step == GeoreferenceStep.Warp):
            self._runOverviewStep()
        elif (self._step == GeoreferenceStep.Overview):
            self.writeGcpFile(self._gc, self._pointFile.absoluteFilePath())
            self._step = GeoreferenceStep.Stop
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
