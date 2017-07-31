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

import os

from PyQt4 import uic
from PyQt4.QtCore import Qt, QFileInfo, QPoint, QPointF, QProcess, QSettings, QDir, QTextStream, QFile, QIODevice, QCoreApplication, QRectF
from PyQt4.QtGui import QDialog, QGraphicsScene, QPixmap

from qgis.core import QgsPoint, QgsMapLayerRegistry, QgsRasterLayer, QgsVectorLayer, QgsMessageLog

from ..src.plan_util import *

from georeferencer import Georeferencer, Scale, ProcessStatus
from gcp import GroundControl, GroundControlPoint
import georef_dialog_base
import georef_graphics_view

import resources

class GeorefDialog(QDialog, georef_dialog_base.Ui_GeorefDialogBase):

    # Internal variables
    _closeOnDone = False
    _types = {}
    _georeferencer = None

    def __init__(self, types, parent=None):
        super(GeorefDialog, self).__init__(parent)
        self.setupUi(self)

        self._types = types
        self._scene = QGraphicsScene(self)
        self._georeferencer = Georeferencer(self)
        self._georeferencer.status.connect(self._updateStatus)
        self._georeferencer.error.connect(self._updateError)

        # Init the gui
        for group in self._types:
            self.typeCombo.addItem(self._types[group]['name'], group)
        self.typeCombo.setCurrentIndex(0)

        for scale in Scale.Scale:
            self.scaleCombo.addItem(Scale.Label[scale], scale)
        self.scaleCombo.setCurrentIndex(Scale.OneToTwenty)

        self.processButton.clicked.connect(self._process)
        self.saveButton.clicked.connect(self._save)
        self.runButton.clicked.connect(self._run)
        self.closeButton.clicked.connect(self._close)
        self.siteEdit.textChanged.connect(self._updateGeoreference)
        self.typeCombo.currentIndexChanged.connect(self._updateGeoreference)
        self.scaleCombo.currentIndexChanged.connect(self._updateGeoreference)
        self.numberSpin.valueChanged.connect(self._updateGeoreference)
        self.suffixEdit.textChanged.connect(self._updateGeoreference)
        self.eastSpin.valueChanged.connect(self._updateGeoreference)
        self.northSpin.valueChanged.connect(self._updateGeoreference)

    def loadImage(self, inputFile):
        self._setStatusLabel(self.loadStatusLabel, ProcessStatus.Running)
        if (not inputFile.exists()):
            self._showStatus('ERROR: Input file not found! File path was ' + inputFile.absoluteFilePath())
            self._setStatusLabel(self.loadStatusLabel, ProcessStatus.Failure)
            return false

        self._inputFile = inputFile
        pixmap = QPixmap(self._inputFile.absoluteFilePath())
        if pixmap.isNull():
            self._signalError('Loading of raw image failed.')
            return
        inputDir = inputFile.absoluteDir()

        pixmap = QPixmap(self._inputFile.absoluteFilePath())
        w = pixmap.width()
        h = pixmap.height()

        self._scene.addPixmap(pixmap)
        self._scene.setSceneRect(QRectF(0, 0, w, h))

        self.planView.setSceneView(self._scene, QRectF(0, 0, w, h))
        self.headerView.setSceneView(self._scene, QRectF(0, 0, w, 200))
        self.footerView.setSceneView(self._scene, QRectF(100, h - 600, w - 200, 500))

        self.gcpWidget1.setScene(self._scene, 250, 100, 2)
        self.gcpWidget2.setScene(self._scene, 250, 3050, 2)
        self.gcpWidget3.setScene(self._scene, 3200, 3050, 2)
        self.gcpWidget4.setScene(self._scene, 3200, 100, 2)

        md = PlanMetadata()
        md.setFile(self._inputFile)
        self.inputFileEdit.setText(self._inputFile.baseName())
        self.siteEdit.setText(md.siteCode)
        self.typeCombo.setCurrentIndex(self.typeCombo.findData(md.sourceClass))
        if md.sourceId is not None:
            self.numberSpin.setValue(md.sourceId)
        else:
            self.numberSpin.setValue(0)
        if md.easting is not None:
            self.eastSpin.setValue(md.easting)
        else:
            self.eastSpin.setValue(0)
        if md.northing is not None:
            self.northSpin.setValue(md.northing)
        else:
            self.northSpin.setValue(0)
        self.suffixEdit.setText(md.suffix)
        self._updateFileNames(md)
        self._updateGeoPoints()

        self._setStatusLabel(self.loadStatusLabel, ProcessStatus.Success)
        QCoreApplication.processEvents()
        return True

    def _updateGeoPoints(self):
        mapUnits = Scale.Factor[self.drawingScale()]
        local1 = QPointF(self.eastSpin.value(), self.northSpin.value() + mapUnits)
        local2 = QPointF(self.eastSpin.value(), self.northSpin.value())
        local3 = QPointF(self.eastSpin.value() + mapUnits, self.northSpin.value())
        local4 = QPointF(self.eastSpin.value() + mapUnits, self.northSpin.value() + mapUnits)
        gridLayer = self._types[self.drawingType()]['grid']
        features = gridLayer.getFeatures()
        localX = self._types[self.drawingType()]['local_x']
        localX = gridLayer.fieldNameIndex(localX)
        localY = self._types[self.drawingType()]['local_y']
        localY = gridLayer.fieldNameIndex(localY)
        for feature in features:
            local = QPoint(feature.attributes()[localX], feature.attributes()[localY])
            map = feature.geometry().asPoint()
            if local == local1:
                self._log('Is 1')
                self.gcpWidget1.setGeo(local, map)
            elif local == local2:
                self._log('Is 2')
                self.gcpWidget2.setGeo(local, map)
            elif local == local3:
                self._log('Is 3')
                self.gcpWidget3.setGeo(local, map)
            elif local == local4:
                self._log('Is 4')
                self.gcpWidget4.setGeo(local, map)

    def _updateGeoreference(self):
        md = PlanMetadata()
        md.setMetadata(
            self.siteEdit.text(),
            self.drawingType(),
            self.numberSpin.value(),
            self.eastSpin.value(),
            self.northSpin.value(),
            self.suffixEdit.text()
        )
        self._updateFileNames(md)
        self._updateGeoPoints()

    def _updateFileNames(self, md):
        self.rawFileEdit.setText(md.baseName() + '.tif')
        self.geoFileEdit.setText(md.baseName() + self._types[self.drawingType()]['suffix'] + '.tif')

    def _toggleUi(self, status):
        self.processButton.setEnabled(status)
        self.saveButton.setEnabled(status)
        self.runButton.setEnabled(status)
        self.closeButton.setEnabled(status)
        self.siteEdit.setEnabled(status)
        self.typeCombo.setEnabled(status)
        self.numberSpin.setEnabled(status)
        self.suffixEdit.setEnabled(status)
        self.eastSpin.setEnabled(status)
        self.northSpin.setEnabled(status)
        self.cropCheck.setEnabled(status)
        self.addToMapCheck.setEnabled(status)
        self.gcpWidget1.setEnabled(status)
        self.gcpWidget2.setEnabled(status)
        self.gcpWidget3.setEnabled(status)
        self.gcpWidget4.setEnabled(status)
        self.planView.setEnabled(status)
        if (status):
            self.progressBar.setRange(0, 100)
        else:
            self.progressBar.setRange(0, 0)

    def drawingType(self):
        return self.typeCombo.itemData(self.typeCombo.currentIndex())

    def drawingScale(self):
        return self.scaleCombo.itemData(self.scaleCombo.currentIndex())

    def geoFileName(self):
        return self.geoFileEdit.text()

    def _updateStatus(self, step, status):
        self._setStatusLabel(self.loadStatusLabel, status)

    def _updateError(self, step, msg):
        self._setStatusLabel(self.loadStatusLabel, status)
        self._showStatus(msg)

    def _showStatus(self, text):
        self.statusBar.showMessage(text)

    def _log(self, msg):
        QgsMessageLog.logMessage(str(msg), 'ARK', QgsMessageLog.INFO)

    def _save(self):
        # Save raw, save points if set
        pass

    def _run(self):
        self._runGeoreference(False)

    def _process(self):
        self._runGeoreference(True)

    def _close(self):
        if (self._georeferencer.step() == Georeferencer.Stop):
            self.accept()
        else:
            self.reject()

    def _runGeoreference(self, closeOnDone):
        if (self.gcpWidget1.gcp().isNull() or self.gcpWidget2.gcp().isNull() or self.gcpWidget3.gcp().isNull() or self.gcpWidget4.gcp().isNull()):
            self._showStatus('ERROR: Please set all 4 Ground Control Points!')
            return
        self._toggleUi(False)
        QCoreApplication.processEvents()
        self._georeferencer.run()
        if closeOnDone:
            self._close()
        else:
            self._toggleUi(True)

    def _setStatusLabel(self, label, status):
        if status == ProcessStatus.Success:
            label.setPixmap(QPixmap(':/plugins/ark/georef/success.png'))
        elif status == ProcessStatus.Failure:
            label.setPixmap(QPixmap(':/plugins/ark/georef/failure.png'))
        elif status == ProcessStatus.Running:
            label.setPixmap(QPixmap(':/plugins/ark/georef/running.png'))
        else:
            label.setPixmap(QPixmap(':/plugins/ark/georef/unknown.png'))
