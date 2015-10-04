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

from PyQt4.QtCore import Qt, QFileInfo, QPoint, QPointF, QObject, qDebug, QProcess, QFileInfo, QSettings, QDir, QTextStream, QFile, QIODevice, QCoreApplication
from PyQt4 import QtGui, uic

from qgis.core import QgsPoint, QgsMapLayerRegistry, QgsRasterLayer, QgsVectorLayer, QgsMessageLog

from ..plan.plan_util import *

import georef_dialog_base
import georef_graphics_view

class GeorefDialog(QtGui.QDialog, georef_dialog_base.Ui_GeorefDialogBase):

    # Internal variables
    closeOnDone = False
    gdalStep = ''
    crt = 'EPSG:27700'

    #TODO Get from settings
    projectPlanFolder = QDir()
    rawFolder = QDir()
    processedFolder = QDir()
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

    def __init__(self, rawFile, projectPlanFolder, useRawProcessedFolders, crt, gridLayerName, gridX, gridY, parent=None):
        super(GeorefDialog, self).__init__(parent)
        self.setupUi(self)

        self.gdal_translate.setFile(QDir(self.gdalPath()), 'gdal_translate')
        self.gdalwarp.setFile(QDir(self.gdalPath()), 'gdalwarp')
        self.showText('GDAL Path: ' + self.gdalPath())
        if (not self.gdal_translate.exists() or not self.gdalwarp.exists()):
            self.showText('ERROR: GDAL commands not found, please ensure GDAL Tools plugin is installed and has correct path set!')
            self.showText('')
            self.m_runButton.setEnabled(False)
            self.m_runCloseButton.setEnabled(False)

        self.crt = crt
        self.projectPlanFolder = projectPlanFolder
        if useRawProcessedFolders:
            self.rawFolder = QDir(self.projectPlanFolder.absolutePath() + '/raw')
            if (not self.rawFolder.exists()):
                self.rawFolder = self.projectPlanFolder
            self.processedFolder = QDir(self.projectPlanFolder.absolutePath() + '/processed')
            if (not self.processedFolder.exists()):
                self.projectPlanFolder.mkdir('processed')
        else:
            self.rawFolder = self.projectPlanFolder
            self.processedFolder = self.projectPlanFolder
        self.rawFile = rawFile
        self.showText('Raw File: \'' + self.rawFile.absoluteFilePath() + '\'')
        if (not self.rawFile.exists()):
            self.showText('ERROR: Raw file not found!')
            self.m_runButton.setEnabled(False)
            self.m_runCloseButton.setEnabled(False)
        self.pointFile = QFileInfo(self.rawFile.absoluteFilePath() + '.points')
        self.showText('GCP File: \'' + self.pointFile.absoluteFilePath() + '\'')
        if (self.pointFile.exists()):
            self.showText('GCP file found, will be used for default ground control points')
        self.geoFile = QFileInfo(self.processedFolder, self.rawFile.completeBaseName() + self.geoSuffix + '.tif')
        self.showText('Geo File: \'' + self.geoFile.absoluteFilePath() + '\'')
        if (self.pointFile.exists()):
            self.showText('Warning: Georeferenced file found, will be overwritten with new file!')
        self.showText('')

        layerList = QgsMapLayerRegistry.instance().mapLayersByName(gridLayerName)
        if (len(layerList) > 0):
            self.gridLayer = layerList[0]
            self.gridXField = self.gridLayer.fieldNameIndex(gridX)
            self.gridYField = self.gridLayer.fieldNameIndex(gridY)
        else:
            self.showText('ERROR: Grid Layer not found, unable to georeference!')
            self.showText('')
            self.m_runButton.setEnabled(False)
            self.m_runCloseButton.setEnabled(False)

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

        self.rawPixmap = QtGui.QPixmap(self.rawFile.absoluteFilePath())
        self.scene = QtGui.QGraphicsScene(self)
        self.rawItem = self.scene.addPixmap(self.rawPixmap)

        self.gcpWidget1.setScene(self.scene, 250, 100, 2)
        self.gcpWidget2.setScene(self.scene, 250, 3050, 2)
        self.gcpWidget3.setScene(self.scene, 3200, 3050, 2)

        self.planView.setScene(self.scene)
        self.planView.fitInView(self.scene.sceneRect(), Qt.KeepAspectRatio)
        #TODO Make clicks set focus of other views

        md = PlanMetadata()
        md.setFile(self.rawFile)
        self.setMetadata(md)
        self.updateGridPoints()
        self.updateGeoPoints()
        if (self.pointFile.exists()):
            self.loadGcpFile()
            self.showText('')

        self.m_outputText.setHidden(True)

    def updateGridPoints(self):
        self.gcpWidget1.setLocalPoint(QPoint(self.m_eastSpin.value(), self.m_northSpin.value() + 5))
        self.gcpWidget2.setLocalPoint(QPoint(self.m_eastSpin.value(), self.m_northSpin.value()))
        self.gcpWidget3.setLocalPoint(QPoint(self.m_eastSpin.value() + 5, self.m_northSpin.value()))

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
        self.planView.setEnabled(status)
        if (status):
            self.m_progressBar.setRange(0, 100)
        else:
            self.m_progressBar.setRange(0, 0)

    def setMetadata(self, md):
        self.m_fileEdit.setText(self.rawFile.baseName())
        self.m_siteEdit.setText(md.siteCode)
        if (md.sourceClass == 'cxt'):
            self.m_typeCombo.setCurrentIndex(0)
        elif (md.sourceClass == 'pln'):
            self.m_typeCombo.setCurrentIndex(1)
        elif (md.sourceClass == 'sec'):
            self.m_typeCombo.setCurrentIndex(2)
        elif (md.sourceClass == 'mtx'):
            self.m_typeCombo.setCurrentIndex(3)
        self.m_numberSpin.setValue(md.sourceId)
        self.m_eastSpin.setValue(md.easting)
        self.m_northSpin.setValue(md.northing)
        self.m_suffixEdit.setText(md.suffix)

    def metadata(self):
        md = PlanMetadata()
        md.setMetadata(self.m_siteEdit.text(), self.m_typeCombo.currentText(), self.m_numberSpin.value(), self.m_eastSpin.value(), self.m_northSpin.value(), self.m_suffixEdit.text())
        return md

    def geoRefFile(self):
        return self.geoFile

    def showText(self, text):
        self.m_outputText.append(text)
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
        if (self.gcpWidget1.rawPoint().isNull() or self.gcpWidget2.rawPoint().isNull() or self.gcpWidget3.rawPoint().isNull()):
            self.showText('ERROR: Please set all 3 Ground Control Points!')
            return
        self.enableUi(False)
        QCoreApplication.processEvents()
        self.runCropStep()

    def runCropStep(self):
        self.gdalStep = 'crop'
        self.gdalArgs = []
        self.gdalCommand = ''
        cropped = self.rawPixmap.copy(0, 0, self.rawPixmap.width(), int(self.rawPixmap.height() * 0.84))
        image = cropped.toImage()
        image.save(self.projectPlanFolder.absolutePath() + '/arkplan_crop.png', 'PNG', 100)
        self.runTranslateStep()

    def runTranslateStep(self):
        self.gdalStep = 'translate'
        self.gdalArgs = []
        self.gdalArgs.extend(['-of', 'GTiff'])
        self.gdalArgs.extend(['-a_srs', self.crt])
        self.gdalArgs.extend(['-gcp', str(self.gcpWidget1.rawPoint().x()), str(self.gcpWidget1.rawPoint().y()), str(self.gcpWidget1.mapPoint().x()), str(self.gcpWidget1.mapPoint().y())])
        self.gdalArgs.extend(['-gcp', str(self.gcpWidget2.rawPoint().x()), str(self.gcpWidget2.rawPoint().y()), str(self.gcpWidget2.mapPoint().x()), str(self.gcpWidget2.mapPoint().y())])
        self.gdalArgs.extend(['-gcp', str(self.gcpWidget3.rawPoint().x()), str(self.gcpWidget3.rawPoint().y()), str(self.gcpWidget3.mapPoint().x()), str(self.gcpWidget3.mapPoint().y())])
        self.gdalArgs.append(self.projectPlanFolder.absolutePath() + '/arkplan_crop.png')
        self.gdalArgs.append(self.projectPlanFolder.absolutePath() + '/arkplan_trans.tiff')
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
        self.gdalArgs.append('\"' + self.projectPlanFolder.absolutePath() + '/arkplan_trans.tiff' + '\"')
        self.gdalArgs.append('\"' + self.geoFile.absoluteFilePath() + '\"')
        self.gdalCommand = self.gdalwarp.absoluteFilePath() + ' ' + ' '.join(self.gdalArgs)
        self.gdalProcess.start(self.gdalCommand)

    def gdalProcessStarted(self):
        if (self.gdalStep == 'crop'):
            self.showText('Cropping input file to required size...')
        elif (self.gdalStep == 'translate'):
            self.showText('Running GDAL translate command:')
            self.showText(self.gdalCommand)
        elif (self.gdalStep == 'warp'):
            self.showText('Running GDAL warp command:')
            self.showText(self.gdalCommand)
        self.showText('')

    def gdalProcessFinished(self):
        if (self.gdalProcess.exitCode() != 0):
            self.gdalStep = ''
            self.showText('Process failed!')
            self.showText('')
            self.enableUi(True)
        elif (self.gdalStep == 'crop'):
            self.showText('Cropping finished')
            self.showText('')
            self.runTranslateStep()
        elif (self.gdalStep == 'translate'):
            self.showText('GDAL translate finished')
            self.showText('')
            self.runWarpStep()
        elif (self.gdalStep == 'warp'):
            self.gdalStep = 'done'
            self.showText('GDAL warp finished')
            self.writeGcpFile()
            self.showText('')
            self.enableUi(True)
            if (self.closeOnDone):
                self.closeDialog()

    def gdalProcessError(self):
        self.showProcessError(self.gdalProcess)

    def showProcessError(self, process):
        self.showText(str(process.readAllStandardError()))
        self.showText('')

    def loadGcpFile(self):
        if (not self.pointFile.exists()):
            self.showText('ERROR: GCP file does not exist')
            return
        inFile = QFile(self.pointFile.absoluteFilePath())
        if (not inFile.open(QIODevice.ReadOnly | QIODevice.Text)):
            self.showText('ERROR: Unable to open GCP file for reading')
            return
        inStream = QTextStream(inFile)
        line = inStream.readLine()
        self.showText(line)
        # Skip the header line if found
        if (line == 'mapX,mapY,pixelX,pixelY,enable'):
            line = inStream.readLine()
            self.showText(line)
        valid = True
        pix1 = QPointF()
        pix2 = QPointF()
        pix3 = QPointF()
        lines = 0
        while (line and valid):
            vals = line.split(',')
            if (len(vals) != 5):
                self.showText('not 5 vals')
                valid = False
            elif (vals[4] == '0'):
                self.showText('not used point')
                pass
            elif (vals[0] == str(self.gcpWidget1.mapPoint().x()) and vals[1] == str(self.gcpWidget1.mapPoint().y())):
                self.showText('match point 1')
                lines += 1
                pix1 = QPointF(float(vals[2]), float(vals[3]))
            elif (vals[0] == str(self.gcpWidget2.mapPoint().x()) and vals[1] == str(self.gcpWidget2.mapPoint().y())):
                self.showText('match point 1')
                lines += 1
                pix2 = QPointF(float(vals[2]), float(vals[3]))
            elif (vals[0] == str(self.gcpWidget3.mapPoint().x()) and vals[1] == str(self.gcpWidget3.mapPoint().y())):
                self.showText('match point 1')
                lines += 1
                pix3 = QPointF(float(vals[2]), float(vals[3]))
            else:
                self.showText('not matching line!')
            line = inStream.readLine()
            self.showText(line)
        inFile.close()
        self.showText('lines used = ' + str(lines))
        if (lines != 3 or pix1.isNull() or pix2.isNull() or pix3.isNull()):
            self.showText('GCP file did not contain a valid set of points matching the grid')
        else:
            self.gcpWidget1.setRawPoint(pix1)
            self.gcpWidget2.setRawPoint(pix2)
            self.gcpWidget3.setRawPoint(pix3)
            self.showText('GCP file points loaded')

    def writeGcpFile(self):
        outFile = QFile(self.pointFile.absoluteFilePath())
        if (not outFile.open(QIODevice.WriteOnly | QIODevice.Text)):
            self.showText('ERROR: Unable to open GCP file for writing')
            return
        outStream = QTextStream(outFile)
        outStream << 'mapX,mapY,pixelX,pixelY,enable\n'
        outStream << ','.join([str(self.gcpWidget1.mapPoint().x()), str(self.gcpWidget1.mapPoint().y()), str(self.gcpWidget1.rawPoint().x()), str(self.gcpWidget1.rawPoint().y())]) << ',1\n'
        outStream << ','.join([str(self.gcpWidget2.mapPoint().x()), str(self.gcpWidget2.mapPoint().y()), str(self.gcpWidget2.rawPoint().x()), str(self.gcpWidget2.rawPoint().y())]) << ',1\n'
        outStream << ','.join([str(self.gcpWidget3.mapPoint().x()), str(self.gcpWidget3.mapPoint().y()), str(self.gcpWidget3.rawPoint().x()), str(self.gcpWidget3.rawPoint().y())]) << ',1\n'
        outFile.close()
        self.showText('GCP file written')
