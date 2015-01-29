# -*- coding: utf-8 -*-
"""
/***************************************************************************
 ArkPlanDialog
                                 A QGIS plugin
 Plugin to assist in digitising of Archaeological plans.
                             -------------------
        begin                : 2015-01-10
        git sha              : $Format:%H$
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

from PyQt4.QtCore import Qt, QFileInfo, QPoint, QPointF, QObject, SIGNAL, qDebug, QProcess, QFileInfo, QSettings, QDir, QTextStream, QFile, QIODevice
from PyQt4 import QtGui, uic
from qgis.core import QgsPoint, QgsMapLayerRegistry, QgsRasterLayer
import ark_georef_dialog_base
import ark_georef_graphics_view

class ArkGeorefDialog(QtGui.QDialog, ark_georef_dialog_base.Ui_ArkGeorefDialogBase):

    # Internal variables
    gridPoint1 = QPoint()
    gridPoint2 = QPoint()
    gridPoint3 = QPoint()

    geo1 = QgsPoint()
    geo2 = QgsPoint()
    geo3 = QgsPoint()

    gcp1 = QPointF()
    gcp2 = QPointF()
    gcp3 = QPointF()

    closeOnDone = False
    gdalStep = ''
    crt = 'EPSG:27700'

    #TODO Get from settings
    tempFile = QFileInfo('/filebin/Development/arkplan_temp.tiff')
    rawFile = QFileInfo()
    pointFile = QFileInfo()
    geoFile = QFileInfo()

    gdalPath = ''
    gdal_translate = QFileInfo()
    gdalwarp = QFileInfo()
    gdalCommand = ''
    gdalArgs = ''
    gdalProcess = QProcess()

    def __init__(self, rawFile, geoFile, crt, gridReference, gridLayerId, gridX, gridY, parent=None):
        super(ArkGeorefDialog, self).__init__(parent)
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
        self.geoFile = geoFile
        self.showText('Geo File: \'' + self.geoFile.absoluteFilePath() + '\'')
        if (self.pointFile.exists()):
            self.showText('Warning: Georeferenced file found, will be overwritten with new file!')
        self.showText('')

        self.gridReference = gridReference
        self.rawPixmap = QtGui.QPixmap(self.rawFile.absoluteFilePath())
        self.scene = QtGui.QGraphicsScene(self)
        self.rawItem = self.scene.addPixmap(self.rawPixmap)

        self.m_runButton.clicked.connect(self.run)
        self.m_runCloseButton.clicked.connect(self.runClose)
        self.m_closeButton.clicked.connect(self.closeDialog)

        self.gdalProcess.started.connect(self.gdalProcessStarted)
        self.gdalProcess.finished.connect(self.gdalProcessFinished)
        self.gdalProcess.error.connect(self.gdalProcessError)
        self.gdalProcess.readyReadStandardError.connect(self.gdalProcessError)

        self.gridPoint1 = QPoint(self.gridReference.x(), self.gridReference.y() + 5)
        self.m_gridLabel1.setText('%d / %d' % (self.gridPoint1.x(), self.gridPoint1.y()))
        self.m_gridView1.setScene(self.scene)
        self.m_gridView1.centerOn(250, 100)
        self.m_gridView1.scale(2, 2)
        self.gridItem1 = self.scene.addEllipse(-1.5, -1.5, 3.0, 3.0, QtGui.QPen(Qt.red))
        self.gridItem1.setVisible(False)
        self.m_gridView1.pointSelected.connect(self.setGcp1)

        self.gridPoint2 = QPoint(self.gridReference.x(), self.gridReference.y())
        self.m_gridLabel2.setText('%d / %d' % (self.gridPoint2.x(), self.gridPoint2.y()))
        self.m_gridView2.setScene(self.scene)
        self.m_gridView2.centerOn(250, 3050)
        self.m_gridView2.scale(2, 2)
        self.gridItem2 = self.scene.addEllipse(-1.5, -1.5, 3.0, 3.0, QtGui.QPen(Qt.red))
        self.gridItem2.setVisible(False)
        self.m_gridView2.pointSelected.connect(self.setGcp2)

        self.gridPoint3 = QPoint(self.gridReference.x() + 5, self.gridReference.y())
        self.m_gridLabel3.setText('%d / %d' % (self.gridPoint3.x(), self.gridPoint3.y()))
        self.m_gridView3.setScene(self.scene)
        self.m_gridView3.centerOn(3200, 3050)
        self.m_gridView3.scale(2, 2)
        self.gridItem3 = self.scene.addEllipse(-1.5, -1.5, 3.0, 3.0, QtGui.QPen(Qt.red))
        self.gridItem3.setVisible(False)
        self.m_gridView3.pointSelected.connect(self.setGcp3)

        # Find the geo points for the grid points
        gridLayer = QgsMapLayerRegistry.instance().mapLayersByName(gridLayerId)[0]
        iX = gridLayer.fieldNameIndex(gridX)
        iY = gridLayer.fieldNameIndex(gridY)
        features = gridLayer.getFeatures()
        for feature in features:
            if feature.attributes()[iX] == self.gridPoint1.x() and feature.attributes()[iY] == self.gridPoint1.y():
                   self.geo1 = feature.geometry().asPoint()
            if feature.attributes()[iX] == self.gridPoint2.x() and feature.attributes()[iY] == self.gridPoint2.y():
                   self.geo2 = feature.geometry().asPoint()
            if feature.attributes()[iX] == self.gridPoint3.x() and feature.attributes()[iY] == self.gridPoint3.y():
                   self.geo3 = feature.geometry().asPoint()

        self.m_gcpTable.item(0, 2).setText(str(self.gridPoint1.x()))
        self.m_gcpTable.item(0, 3).setText(str(self.gridPoint1.y()))
        self.m_gcpTable.item(0, 4).setText(str(self.geo1.x()))
        self.m_gcpTable.item(0, 5).setText(str(self.geo1.y()))

        self.m_gcpTable.item(1, 2).setText(str(self.gridPoint2.x()))
        self.m_gcpTable.item(1, 3).setText(str(self.gridPoint2.y()))
        self.m_gcpTable.item(1, 4).setText(str(self.geo2.x()))
        self.m_gcpTable.item(1, 5).setText(str(self.geo2.y()))

        self.m_gcpTable.item(2, 2).setText(str(self.gridPoint3.x()))
        self.m_gcpTable.item(2, 3).setText(str(self.gridPoint3.y()))
        self.m_gcpTable.item(2, 4).setText(str(self.geo3.x()))
        self.m_gcpTable.item(2, 5).setText(str(self.geo3.y()))
        self.resizeGcpTable()

        if (self.pointFile.exists()):
            self.loadGcpFile()
            self.showText('')

    def resizeGcpTable(self):
        self.m_gcpTable.resizeColumnsToContents()
        self.m_gcpTable.resizeRowsToContents()

    def enableUi(self, status):
        self.m_runButton.setEnabled(status)
        self.m_closeButton.setEnabled(status)
        self.m_runCloseButton.setEnabled(status)
        self.m_gridView1.setEnabled(status)
        self.m_gridView2.setEnabled(status)
        self.m_gridView3.setEnabled(status)
        self.m_gcpTable.setEnabled(status)
        self.m_outputText.setEnabled(status)
        if (status):
            self.m_progressBar.setRange(0, 100)
        else:
            self.m_progressBar.setRange(0, 0)

    def showText(self, text):
        self.m_outputText.append(text)

    def setGcp1(self, point):
        self.gcp1 = point
        self.gridItem1.setPos(point)
        self.gridItem1.setVisible(True)
        self.m_gcpTable.item(0, 0).setText(str(point.x()))
        self.m_gcpTable.item(0, 1).setText(str(point.y()))
        self.resizeGcpTable()

    def setGcp2(self, point):
        self.gcp2 = point
        self.gridItem2.setPos(point)
        self.gridItem2.setVisible(True)
        self.m_gcpTable.item(1, 0).setText(str(point.x()))
        self.m_gcpTable.item(1, 1).setText(str(point.y()))
        self.resizeGcpTable()

    def setGcp3(self, point):
        self.gcp3 = point
        self.gridItem3.setPos(point)
        self.gridItem3.setVisible(True)
        self.m_gcpTable.item(2, 0).setText(str(point.x()))
        self.m_gcpTable.item(2, 1).setText(str(point.y()))
        self.resizeGcpTable()

    def gdalPath(self):
        settings = QSettings()
        return settings.value('/GdalTools/gdalPath', '')

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
        if (self.gcp1.isNull() or self.gcp2.isNull() or self.gcp3.isNull()):
            self.showText('ERROR: Please set all 3 Ground Control Points!')
            return
        self.enableUi(False)
        self.gdalStep = 'translate'
        self.gdalArgs = []
        self.gdalArgs.extend(['-of', 'GTiff'])
        self.gdalArgs.extend(['-a_srs', self.crt])
        self.gdalArgs.extend(['-gcp', str(self.gcp1.x()), str(self.gcp1.y()), str(self.geo1.x()), str(self.geo1.y())])
        self.gdalArgs.extend(['-gcp', str(self.gcp2.x()), str(self.gcp2.y()), str(self.geo2.x()), str(self.geo2.y())])
        self.gdalArgs.extend(['-gcp', str(self.gcp3.x()), str(self.gcp3.y()), str(self.geo3.x()), str(self.geo3.y())])
        self.gdalArgs.append(self.rawFile.absoluteFilePath())
        self.gdalArgs.append(self.tempFile.absoluteFilePath())
        self.gdalCommand = self.gdal_translate.absoluteFilePath() + ' ' + ' '.join(self.gdalArgs)
        self.gdalProcess.start(self.gdal_translate.absoluteFilePath(), self.gdalArgs)

    def gdalProcessStarted(self):
        if (self.gdalStep == 'translate'):
            self.showText('Running GDAL translate command:')
        elif (self.gdalStep == 'warp'):
            self.showText('Running GDAL warp command:')
        self.showText(self.gdalCommand)
        self.showText('')

    def gdalProcessFinished(self):
        if (self.gdalProcess.exitCode() != 0):
            self.gdalStep = ''
            self.showText('GDAL command failed!')
            self.showText('')
            self.enableUi(True)
        elif (self.gdalStep == 'translate'):
            self.gdalStep = 'warp'
            self.showText('GDAL translate finished')
            self.showText('')
            self.gdalArgs = []
            self.gdalArgs.extend(['-order', '1'])
            self.gdalArgs.extend(['-r', 'cubic'])
            self.gdalArgs.extend(['-t_srs', self.crt])
            self.gdalArgs.extend(['-of', 'GTiff'])
            self.gdalArgs.extend(['-co', 'COMPRESS=LZW'])
            self.gdalArgs.append('-dstalpha')
            self.gdalArgs.append('-overwrite')
            self.gdalArgs.append('\"' + self.tempFile.absoluteFilePath() + '\"')
            self.gdalArgs.append('\"' + self.geoFile.absoluteFilePath() + '\"')
            self.gdalCommand = self.gdalwarp.absoluteFilePath() + ' ' + ' '.join(self.gdalArgs)
            self.gdalProcess.start(self.gdalCommand)
        else:
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
            elif (vals[0] == str(self.geo1.x()) and vals[1] == str(self.geo1.y())):
                self.showText('match point 1')
                lines += 1
                pix1 = QPointF(float(vals[2]), float(vals[3]))
            elif (vals[0] == str(self.geo2.x()) and vals[1] == str(self.geo2.y())):
                self.showText('match point 1')
                lines += 1
                pix2 = QPointF(float(vals[2]), float(vals[3]))
            elif (vals[0] == str(self.geo3.x()) and vals[1] == str(self.geo3.y())):
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
            self.setGcp1(pix1)
            self.setGcp2(pix2)
            self.setGcp3(pix3)
            self.showText('GCP file points loaded')

    def writeGcpFile(self):
        outFile = QFile(self.pointFile.absoluteFilePath())
        if (not outFile.open(QIODevice.WriteOnly | QIODevice.Text)):
            self.showText('ERROR: Unable to open GCP file for writing')
            return
        outStream = QTextStream(outFile)
        outStream << 'mapX,mapY,pixelX,pixelY,enable\n'
        outStream << ','.join([str(self.geo1.x()), str(self.geo1.y()), str(self.gcp1.x()), str(self.gcp1.y())]) << ',1\n'
        outStream << ','.join([str(self.geo2.x()), str(self.geo2.y()), str(self.gcp2.x()), str(self.gcp2.y())]) << ',1\n'
        outStream << ','.join([str(self.geo3.x()), str(self.geo3.y()), str(self.gcp3.x()), str(self.gcp3.y())]) << ',1\n'
        outFile.close()
        self.showText('GCP file written')
