# -*- coding: utf-8 -*-
"""
/***************************************************************************
                                      Ark
                                 A QGIS plugin
             QGIS Plugin for ARK, the Archaeological Recording Kit
                              -------------------
        begin                : 2015-03-02
        git sha              : $Format:%H$
        copyright            : (C) 2015 by L - P: Heritage LLP
        copyright            : (C) 2015 by John Layt
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

import os

from PyQt4 import uic
from PyQt4.QtCore import Qt, QFileInfo, QPoint, QPointF, QProcess, QSettings, QDir, QTextStream, QFile, QIODevice, QCoreApplication, QRectF
from PyQt4.QtGui import QDialog, QGraphicsScene, QPixmap

from qgis.core import QgsPoint, QgsMapLayerRegistry, QgsRasterLayer, QgsVectorLayer, QgsMessageLog

from ..src.plan_util import *

import georef_dialog_base
import georef_graphics_view

import resources_rc

class ProcessStatus():

    Unknown = 0
    Running = 1
    Success = 2
    Failure = 3

class GeorefDialog(QDialog, georef_dialog_base.Ui_GeorefDialogBase):

    # Internal variables
    closeOnDone = False
    gdalStep = ''
    crt = 'EPSG:27700'

    #TODO Get from settings
    destinationDir = QDir()
    rawFile = QFileInfo()
    pointFile = QFileInfo()
    geoFile = QFileInfo()
    geoSuffix = '_r'

    gdal_translate = QFileInfo()
    gdalwarp = QFileInfo()
    gdalCommand = ''
    gdalArgs = ''
    gdalProcess = QProcess()

    gridLayer = QgsVectorLayer()
    gridXField = ''
    gridYField = ''

    def __init__(self, rawFile, destinationDir, crt, gridLayerName, gridX, gridY, parent=None):
        super(GeorefDialog, self).__init__(parent)
        self.setupUi(self)
        self.m_runButton.setEnabled(False)
        self.m_runCloseButton.setEnabled(False)

        self.m_typeCombo.addItem('Context', 'cxt')
        self.m_typeCombo.addItem('Plan', 'pln')
        self.m_typeCombo.addItem('Section', 'sec')
        self.m_typeCombo.setCurrentIndex(0)

        self.gdal_translate.setFile(QDir(self.gdalPath()), 'gdal_translate')
        self.gdalwarp.setFile(QDir(self.gdalPath()), 'gdalwarp')
        self.logText('GDAL Path: ' + self.gdalPath())
        if (not self.gdal_translate.exists() or not self.gdalwarp.exists()):
            self.showStatus('ERROR: GDAL commands not found, please ensure GDAL Tools plugin is installed and has correct path set!')
            return

        self._setStatusLabel(self.loadStatusLabel, ProcessStatus.Running)
        self.crt = crt
        self.rawFile = rawFile
        self.destinationDir = destinationDir
        self.logText('Raw File: \'' + self.rawFile.absoluteFilePath() + '\'')
        if (not self.rawFile.exists()):
            self.showStatus('ERROR: Raw file not found! File path was ' + self.rawFile.absoluteFilePath())
            self._setStatusLabel(self.loadStatusLabel, ProcessStatus.Failure)
            return
        self.pointFile = QFileInfo(self.rawFile.absoluteFilePath() + '.points')
        self.logText('GCP File: \'' + self.pointFile.absoluteFilePath() + '\'')
        if (self.pointFile.exists()):
            self.logText('GCP file found, will be used for default ground control points')
        self.geoFile = QFileInfo(self.destinationDir, self.rawFile.completeBaseName() + self.geoSuffix + '.tif')
        self.logText('Geo File: \'' + self.geoFile.absoluteFilePath() + '\'')
        if (self.pointFile.exists()):
            self.showStatus('Warning: Georeferenced file found, will be overwritten with new file!')

        layerList = QgsMapLayerRegistry.instance().mapLayersByName(gridLayerName)
        if (len(layerList) > 0):
            self.gridLayer = layerList[0]
            self.gridXField = self.gridLayer.fieldNameIndex(gridX)
            self.gridYField = self.gridLayer.fieldNameIndex(gridY)
        else:
            self.showStatus('ERROR: Grid Layer not found, unable to georeference!')
            self._setStatusLabel(self.loadStatusLabel, ProcessStatus.Failure)
            return

        self._setStatusLabel(self.loadStatusLabel, ProcessStatus.Success)

        self.m_runButton.setEnabled(True)
        self.m_runCloseButton.setEnabled(True)

        self.gdalProcess.started.connect(self.gdalProcessStarted)
        self.gdalProcess.finished.connect(self.gdalProcessFinished)
        self.gdalProcess.error.connect(self.gdalProcessError)
        self.gdalProcess.readyReadStandardError.connect(self.gdalProcessError)

        # Init the gui
        self.m_runButton.clicked.connect(self.run)
        self.m_runCloseButton.clicked.connect(self.runClose)
        self.m_closeButton.clicked.connect(self.closeDialog)
        self.m_siteEdit.textChanged.connect(self.updateGeoFile)
        self.m_typeCombo.currentIndexChanged.connect(self.updateGeoFile)
        self.m_numberSpin.valueChanged.connect(self.updateGeoFile)
        self.m_suffixEdit.textChanged.connect(self.updateGeoFile)
        self.m_eastSpin.valueChanged.connect(self.updateGeoFile)
        self.m_northSpin.valueChanged.connect(self.updateGeoFile)
        self.m_eastSpin.valueChanged.connect(self.updateGridPoints)
        self.m_northSpin.valueChanged.connect(self.updateGridPoints)

        self.rawPixmap = QPixmap(self.rawFile.absoluteFilePath())
        self.scene = QGraphicsScene(self)
        self.rawItem = self.scene.addPixmap(self.rawPixmap)

        self.gcpWidget1.setScene(self.scene, 250, 100, 2)
        self.gcpWidget2.setScene(self.scene, 250, 3050, 2)
        self.gcpWidget3.setScene(self.scene, 3200, 3050, 2)
        self.gcpWidget4.setScene(self.scene, 3200, 100, 2)

        self.planView.setScene(self.scene)
        #FIXME No idea why this doesn't work!
        #self.planView.fitInView(self.rawItem, Qt.KeepAspectRatio)
        self.planView.setSceneRect(self.rawItem.boundingRect())
        scale = self.rawItem.boundingRect().width() / (self.planView.width() * 150.0)
        self.planView.scale(scale, scale)
        #TODO Make clicks set focus of other views

        md = PlanMetadata()
        md.setFile(self.rawFile)
        self.setMetadata(md)
        self.updateGridPoints()
        self.updateGeoPoints()
        if (self.pointFile.exists()):
            self.loadGcpFile()
            self.logText('')

    def updateGridPoints(self):
        self.gcpWidget1.setLocalPoint(QPoint(self.m_eastSpin.value(), self.m_northSpin.value() + 5))
        self.gcpWidget2.setLocalPoint(QPoint(self.m_eastSpin.value(), self.m_northSpin.value()))
        self.gcpWidget3.setLocalPoint(QPoint(self.m_eastSpin.value() + 5, self.m_northSpin.value()))
        self.gcpWidget4.setLocalPoint(QPoint(self.m_eastSpin.value() + 5, self.m_northSpin.value() + 5))

    def updateGeoPoints(self):
        # Find the geo points for the grid points
        features = self.gridLayer.getFeatures()
        for feature in features:
            if feature.attributes()[self.gridXField] == self.gcpWidget1.localPoint().x() and feature.attributes()[self.gridYField] == self.gcpWidget1.localPoint().y():
                   self.gcpWidget1.setMapPoint(feature.geometry().asPoint())
            if feature.attributes()[self.gridXField] == self.gcpWidget2.localPoint().x() and feature.attributes()[self.gridYField] == self.gcpWidget2.localPoint().y():
                   self.gcpWidget2.setMapPoint(feature.geometry().asPoint())
            if feature.attributes()[self.gridXField] == self.gcpWidget3.localPoint().x() and feature.attributes()[self.gridYField] == self.gcpWidget3.localPoint().y():
                   self.gcpWidget3.setMapPoint(feature.geometry().asPoint())
            if feature.attributes()[self.gridXField] == self.gcpWidget4.localPoint().x() and feature.attributes()[self.gridYField] == self.gcpWidget4.localPoint().y():
                   self.gcpWidget4.setMapPoint(feature.geometry().asPoint())

    def updateGeoFile(self):
        self.geoFile = QFileInfo(self.geoFile.absoluteDir(), self.metadata().baseName() + self.geoSuffix + '.tif')

    def enableUi(self, status):
        self.m_runButton.setEnabled(status)
        self.m_closeButton.setEnabled(status)
        self.m_runCloseButton.setEnabled(status)
        self.m_siteEdit.setEnabled(status)
        self.m_typeCombo.setEnabled(status)
        self.m_numberSpin.setEnabled(status)
        self.m_suffixEdit.setEnabled(status)
        self.m_eastSpin.setEnabled(status)
        self.m_northSpin.setEnabled(status)
        self.gcpWidget1.setEnabled(status)
        self.gcpWidget2.setEnabled(status)
        self.gcpWidget3.setEnabled(status)
        self.gcpWidget4.setEnabled(status)
        self.planView.setEnabled(status)
        if (status):
            self.m_progressBar.setRange(0, 100)
        else:
            self.m_progressBar.setRange(0, 0)

    def setMetadata(self, md):
        self.m_fileEdit.setText(self.rawFile.baseName())
        self.m_siteEdit.setText(md.siteCode)
        self.m_typeCombo.setCurrentIndex(self.m_typeCombo.findData(md.sourceClass))
        if md.sourceId is not None:
            self.m_numberSpin.setValue(md.sourceId)
        else:
            self.m_numberSpin.setValue(0)
        if md.easting is not None:
            self.m_eastSpin.setValue(md.easting)
        else:
            self.m_eastSpin.setValue(0)
        if md.northing is not None:
            self.m_northSpin.setValue(md.northing)
        else:
            self.m_northSpin.setValue(0)
        self.m_suffixEdit.setText(md.suffix)

    def metadata(self):
        md = PlanMetadata()
        md.setMetadata(self.m_siteEdit.text(), self.m_typeCombo.itemData(self.m_typeCombo.currentIndex()), self.m_numberSpin.value(), self.m_eastSpin.value(), self.m_northSpin.value(), self.m_suffixEdit.text())
        return md

    def geoRefFile(self):
        return self.geoFile

    def showStatus(self, text):
        self.statusBar.showMessage(text)
        self.logText(text)

    def logText(self, text):
        QgsMessageLog.logMessage(text, 'Ark', QgsMessageLog.INFO)

    def gdalPath(self):
        settings = QSettings()
        return settings.value('/GdalTools/gdalPath', '/usr/bin')

    def run(self):
        self.closeOnDone = False
        self.runGeoreference()

    def runClose(self):
        self.closeOnDone = True
        self.runGeoreference()

    def closeDialog(self):
        if (self.gdalStep == 'done'):
            self.accept()
        else:
            self.reject()

    def runGeoreference(self):
        if (self.gcpWidget1.rawPoint().isNull() or self.gcpWidget2.rawPoint().isNull() or self.gcpWidget3.rawPoint().isNull() or self.gcpWidget4.rawPoint().isNull()):
            self.showStatus('ERROR: Please set all 3 Ground Control Points!')
            return
        self.enableUi(False)
        QCoreApplication.processEvents()
        self.runCropStep()

    def runCropStep(self):
        self._setStatusLabel(self.cropStatusLabel, ProcessStatus.Running)
        self.showStatus('Cropping input file to required size...')
        self.gdalStep = 'crop'
        self.gdalArgs = []
        self.gdalCommand = ''
        cropped = self.rawPixmap.copy(0, 0, self.rawPixmap.width(), int(self.rawPixmap.height() * 0.84))
        image = cropped.toImage()
        if image.isNull():
            self._setStatusLabel(self.cropStatusLabel, ProcessStatus.Failure)
            self.showStatus('ERROR: Cropping image failed!')
            self.enableUi(True)
        elif image.save(self.rawFile.absoluteDir().absolutePath() + '/arkplan_crop.png', 'PNG', 100):
            self._setStatusLabel(self.cropStatusLabel, ProcessStatus.Success)
            self.showStatus('Cropping finished')
            self.runTranslateStep()
        else:
            self._setStatusLabel(self.cropStatusLabel, ProcessStatus.Failure)
            self.showStatus('ERROR: Saving Crop file ' + self.rawFile.absoluteDir().absolutePath() + '/arkplan_crop.png failed!')
            self.enableUi(True)

    def runTranslateStep(self):
        self.gdalStep = 'translate'
        self.gdalArgs = []
        self.gdalArgs.extend(['-of', 'GTiff'])
        self.gdalArgs.extend(['-a_srs', self.crt])
        self.gdalArgs.extend(['-gcp', str(self.gcpWidget1.rawPoint().x()), str(self.gcpWidget1.rawPoint().y()), str(self.gcpWidget1.mapPoint().x()), str(self.gcpWidget1.mapPoint().y())])
        self.gdalArgs.extend(['-gcp', str(self.gcpWidget2.rawPoint().x()), str(self.gcpWidget2.rawPoint().y()), str(self.gcpWidget2.mapPoint().x()), str(self.gcpWidget2.mapPoint().y())])
        self.gdalArgs.extend(['-gcp', str(self.gcpWidget3.rawPoint().x()), str(self.gcpWidget3.rawPoint().y()), str(self.gcpWidget3.mapPoint().x()), str(self.gcpWidget3.mapPoint().y())])
        self.gdalArgs.extend(['-gcp', str(self.gcpWidget4.rawPoint().x()), str(self.gcpWidget4.rawPoint().y()), str(self.gcpWidget4.mapPoint().x()), str(self.gcpWidget4.mapPoint().y())])
        self.gdalArgs.append(self.rawFile.absoluteDir().absolutePath() + '/arkplan_crop.png')
        self.gdalArgs.append(self.rawFile.absoluteDir().absolutePath() + '/arkplan_trans.tiff')
        self.gdalCommand = self.gdal_translate.absoluteFilePath() + ' ' + ' '.join(self.gdalArgs)
        self.gdalProcess.start(self.gdal_translate.absoluteFilePath(), self.gdalArgs)

    def runWarpStep(self):
        self.gdalStep = 'warp'
        self.gdalArgs = []
        self.gdalArgs.extend(['-order', '1'])
        self.gdalArgs.extend(['-r', 'cubic'])
        self.gdalArgs.extend(['-t_srs', self.crt])
        self.gdalArgs.extend(['-of', 'GTiff'])
        self.gdalArgs.extend(['-co', 'COMPRESS=LZW'])
        self.gdalArgs.append('-dstalpha')
        self.gdalArgs.append('-overwrite')
        self.gdalArgs.append('\"' + self.rawFile.absoluteDir().absolutePath() + '/arkplan_trans.tiff' + '\"')
        self.gdalArgs.append('\"' + self.geoFile.absoluteFilePath() + '\"')
        self.gdalCommand = self.gdalwarp.absoluteFilePath() + ' ' + ' '.join(self.gdalArgs)
        self.gdalProcess.start(self.gdalCommand)

    def gdalProcessStarted(self):
        if (self.gdalStep == 'translate'):
            self._setStatusLabel(self.translateStatusLabel, ProcessStatus.Running)
            self.showStatus('Running GDAL translate command...')
            self.logText(self.gdalCommand)
        elif (self.gdalStep == 'warp'):
            self._setStatusLabel(self.warpStatusLabel, ProcessStatus.Running)
            self.showStatus('Running GDAL warp command...')
            self.logText(self.gdalCommand)

    def gdalProcessFinished(self):
        if (self.gdalProcess.exitCode() != 0):
            if (self.gdalStep == 'translate'):
                self._setStatusLabel(self.translateStatusLabel, ProcessStatus.Failure)
            elif (self.gdalStep == 'warp'):
                self._setStatusLabel(self.warpStatusLabel, ProcessStatus.Failure)
            self.gdalStep = ''
            self.showStatus('Process failed!')
            self.enableUi(True)
        elif (self.gdalStep == 'translate'):
            self._setStatusLabel(self.translateStatusLabel, ProcessStatus.Success)
            self.showStatus('GDAL translate finished')
            self.runWarpStep()
        elif (self.gdalStep == 'warp'):
            self._setStatusLabel(self.warpStatusLabel, ProcessStatus.Success)
            self.gdalStep = 'done'
            self.showStatus('GDAL warp finished')
            self.writeGcpFile()
            self.enableUi(True)
            if (self.closeOnDone):
                self.closeDialog()

    def gdalProcessError(self):
        self.showProcessError(self.gdalProcess)

    def showProcessError(self, process):
        self.logText(str(process.readAllStandardError()))

    def loadGcpFile(self):
        if (not self.pointFile.exists()):
            self.showStatus('ERROR: GCP file does not exist')
            return
        inFile = QFile(self.pointFile.absoluteFilePath())
        if (not inFile.open(QIODevice.ReadOnly | QIODevice.Text)):
            self.showStatus('ERROR: Unable to open GCP file for reading')
            return
        inStream = QTextStream(inFile)
        line = inStream.readLine()
        self.logText(line)
        # Skip the header line if found
        if (line == 'mapX,mapY,pixelX,pixelY,enable'):
            line = inStream.readLine()
            self.logText(line)
        valid = True
        pix1 = QPointF()
        pix2 = QPointF()
        pix3 = QPointF()
        pix4 = QPointF()
        lines = 0
        while (line and valid):
            vals = line.split(',')
            if (len(vals) != 5):
                self.logText('not 5 vals')
                valid = False
            elif (vals[4] == '0'):
                self.logText('not used point')
                pass
            elif (vals[0] == str(self.gcpWidget1.mapPoint().x()) and vals[1] == str(self.gcpWidget1.mapPoint().y())):
                self.logText('match point 1')
                lines += 1
                pix1 = QPointF(float(vals[2]), float(vals[3]))
            elif (vals[0] == str(self.gcpWidget2.mapPoint().x()) and vals[1] == str(self.gcpWidget2.mapPoint().y())):
                self.logText('match point 1')
                lines += 1
                pix2 = QPointF(float(vals[2]), float(vals[3]))
            elif (vals[0] == str(self.gcpWidget3.mapPoint().x()) and vals[1] == str(self.gcpWidget3.mapPoint().y())):
                self.logText('match point 1')
                lines += 1
                pix3 = QPointF(float(vals[2]), float(vals[3]))
            elif (vals[0] == str(self.gcpWidget4.mapPoint().x()) and vals[1] == str(self.gcpWidget4.mapPoint().y())):
                self.logText('match point 4')
                lines += 1
                pix4 = QPointF(float(vals[2]), float(vals[3]))
            else:
                self.logText('not matching line!')
            line = inStream.readLine()
            self.logText(line)
        inFile.close()
        self.logText('lines used = ' + str(lines))
        self.gcpWidget1.setRawPoint(pix1)
        self.gcpWidget2.setRawPoint(pix2)
        self.gcpWidget3.setRawPoint(pix3)
        self.gcpWidget4.setRawPoint(pix4)
        if (lines != 4 or pix1.isNull() or pix2.isNull() or pix3.isNull() or pix4.isNull()):
            self.showStatus('GCP file did not contain a fully valid set of points matching the grid')
        else:
            self.showStatus('GCP file points successfully loaded')

    def writeGcpFile(self):
        outFile = QFile(self.pointFile.absoluteFilePath())
        if (not outFile.open(QIODevice.WriteOnly | QIODevice.Text)):
            self.showStatus('ERROR: Unable to open GCP file for writing')
            return
        outStream = QTextStream(outFile)
        outStream << 'mapX,mapY,pixelX,pixelY,enable\n'
        outStream << ','.join([str(self.gcpWidget1.mapPoint().x()), str(self.gcpWidget1.mapPoint().y()), str(self.gcpWidget1.rawPoint().x()), str(self.gcpWidget1.rawPoint().y())]) << ',1\n'
        outStream << ','.join([str(self.gcpWidget2.mapPoint().x()), str(self.gcpWidget2.mapPoint().y()), str(self.gcpWidget2.rawPoint().x()), str(self.gcpWidget2.rawPoint().y())]) << ',1\n'
        outStream << ','.join([str(self.gcpWidget3.mapPoint().x()), str(self.gcpWidget3.mapPoint().y()), str(self.gcpWidget3.rawPoint().x()), str(self.gcpWidget3.rawPoint().y())]) << ',1\n'
        outStream << ','.join([str(self.gcpWidget4.mapPoint().x()), str(self.gcpWidget4.mapPoint().y()), str(self.gcpWidget4.rawPoint().x()), str(self.gcpWidget4.rawPoint().y())]) << ',1\n'
        outFile.close()
        self.showStatus('GCP file written')

    def _setStatusLabel(self, label, status):
        if status == ProcessStatus.Success:
            label.setPixmap(QPixmap(':/plugins/Ark/georef/success.png'))
        elif status == ProcessStatus.Failure:
            label.setPixmap(QPixmap(':/plugins/Ark/georef/failure.png'))
        elif status == ProcessStatus.Running:
            label.setPixmap(QPixmap(':/plugins/Ark/georef/running.png'))
        else:
            label.setPixmap(QPixmap(':/plugins/Ark/georef/unknown.png'))
