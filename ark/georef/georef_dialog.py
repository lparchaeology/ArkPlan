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

from qgis.PyQt.QtCore import QCoreApplication, QFile, QFileInfo, QPoint, QPointF, QRectF
from qgis.PyQt.QtGui import QPixmap
from qgis.PyQt.QtWidgets import QDialog, QGraphicsScene

from qgis.core import QgsPoint

from ArkSpatial.ark.lib import utils
from ArkSpatial.ark.lib.core import ProcessStatus, Scale, geometry

from ArkSpatial.ark.core import Drawing, Item

from .georeferencer import Georeferencer, GeoreferenceStep
from .transform import Transform
from .ui.georef_dialog_base import Ui_GeorefDialogBase


class GeorefDialog(QDialog, Ui_GeorefDialogBase):

    def __init__(self, types, parent=None):
        super().__init__(parent)
        self.setupUi(self)

        # Internal variables
        self._closeOnDone = False
        self._types = {}
        self._georeferencer = None

        self._types = types
        self._scene = QGraphicsScene(self)
        self._georeferencer = Georeferencer(self)
        self._georeferencer.status.connect(self._updateStatus)
        self._georeferencer.error.connect(self._updateError)

        # Init the gui
        for group in self._types:
            self.typeCombo.addItem(self._types[group]['name'], group)
        self.typeCombo.setCurrentIndex(0)

        for scale in Scale:
            self.scaleCombo.addItem(scale.label, scale)
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
        self._setStatusLabel('load', ProcessStatus.Running)
        if (not inputFile.exists()):
            self._showStatus('ERROR: Input file not found! File path was ' + inputFile.absoluteFilePath())
            self._setStatusLabel('load', ProcessStatus.Failure)
            return False

        self._inputFile = inputFile
        pixmap = QPixmap(self._inputFile.absoluteFilePath())
        if pixmap.isNull():
            self._signalError('Loading of raw image failed.')
            return

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

        self.inputFileNameLabel.setText(self._inputFile.baseName())
        drawing = Drawing(self._inputFile)
        if drawing.isValid():
            self.siteEdit.setText(drawing.item().siteCode())
            self.typeCombo.setCurrentIndex(self.typeCombo.findData(drawing.item().classCode()))
            self.numberSpin.setValue(int(drawing.item().itemId()) or 0)
            self.eastSpin.setValue(drawing.easting() or 0)
            self.northSpin.setValue(drawing.northing() or 0)
            self.suffixEdit.setText(drawing.suffix())
            self._updateFileNames(drawing)
            self._updateGeoPoints()
            pointFile = self.pointFileInfo()
            if pointFile.exists():
                self._loadGcp(pointFile.absoluteFilePath())
            self._setStatusLabel('load', ProcessStatus.Success)
            QCoreApplication.processEvents()
            return True

        return False

    def _loadGcp(self, path):
        gc = Georeferencer.loadGcpFile(path)
        gcTo = Transform()
        for index in gc.points():
            gcp = gc.point(index)
            if gcp.map() == self.gcpWidget1.gcp().map():
                gcTo.setPoint(1, gcp)
            elif gcp.map() == self.gcpWidget2.gcp().map():
                gcTo.setPoint(2, gcp)
            elif gcp.map() == self.gcpWidget3.gcp().map():
                gcTo.setPoint(3, gcp)
            elif gcp.map() == self.gcpWidget4.gcp().map():
                gcTo.setPoint(4, gcp)

        if gcTo.isValid() and len(gcTo.points()) == 4:
            self.gcpWidget1.setRaw(gcTo.point(1).raw())
            self.gcpWidget2.setRaw(gcTo.point(2).raw())
            self.gcpWidget3.setRaw(gcTo.point(3).raw())
            self.gcpWidget4.setRaw(gcTo.point(4).raw())

    def _updateGeoPoints(self):
        mapUnits = self.drawingScale().factor
        local1 = QPointF(self.eastSpin.value(), self.northSpin.value() + mapUnits)
        local2 = QPointF(self.eastSpin.value(), self.northSpin.value())
        local3 = QPointF(self.eastSpin.value() + mapUnits, self.northSpin.value())
        local4 = QPointF(self.eastSpin.value() + mapUnits, self.northSpin.value() + mapUnits)

        if self.drawingType() == 'sec':
            self.gcpWidget1.setGeo(local1, QgsPoint(local1))
            self.gcpWidget2.setGeo(local2, QgsPoint(local2))
            self.gcpWidget3.setGeo(local3, QgsPoint(local3))
            self.gcpWidget4.setGeo(local4, QgsPoint(local4))
            return

        typ = self._type()
        gridLayer = typ['grid']
        features = gridLayer.getFeatures()
        localX = gridLayer.lookupField(typ['local_x'])
        localY = gridLayer.lookupField(typ['local_y'])
        for feature in features:
            local = QPoint(feature.attributes()[localX], feature.attributes()[localY])
            map = feature.geometry().geometry()
            if local == local1:
                self.gcpWidget1.setGeo(local, map)
            elif local == local2:
                self.gcpWidget2.setGeo(local, map)
            elif local == local3:
                self.gcpWidget3.setGeo(local, map)
            elif local == local4:
                self.gcpWidget4.setGeo(local, map)

    def _updateGeoreference(self):
        self._updateFileNames(self.drawing())
        self._updateGeoPoints()

    def _updateFileNames(self, drawing):
        self.rawFileNameLabel.setText(drawing.baseName())
        self.geoFileNameLabel.setText(drawing.baseName() + self._type()['suffix'])

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

    def drawing(self):
        return Drawing(self.item(), self.easting(), self.northing(), self.suffix(), self.rawFileName())

    def item(self):
        return Item(self.siteCode(), self.classCode(), self.itemId())

    def siteCode(self):
        return self.siteEdit.text().strip()

    def classCode(self):
        return self.drawingType()

    def itemId(self):
        return str(self.numberSpin.value())

    def drawingType(self):
        return self.typeCombo.itemData(self.typeCombo.currentIndex())

    def drawingScale(self):
        return self.scaleCombo.itemData(self.scaleCombo.currentIndex())

    def easting(self):
        return self.eastSpin.value()

    def northing(self):
        return self.northSpin.value()

    def suffix(self):
        return self.suffixEdit.text().strip()

    def inputFileName(self):
        return self.inputFileNameLabel.text().strip()

    def rawFileName(self):
        return self.rawFileNameLabel.text().strip()

    def rawFileInfo(self):
        return QFileInfo(self._type()['raw'], self.rawFileName() + '.' + self._inputFile.suffix())

    def pointFileInfo(self):
        return QFileInfo(self._type()['raw'], self.rawFileName() + '.' + self._inputFile.suffix() + '.points')

    def geoFileName(self):
        return self.geoFileNameLabel.text().strip()

    def geoFileInfo(self):
        return QFileInfo(self._type()['geo'], self.geoFileName() + '.tif')

    def _type(self):
        return self._types[self.drawingType()]

    def _updateStatus(self, step, status):
        self._setStatusLabel(step, status)
        self._showStatus(self.tr(step.label) + ': ' + self.tr(status.label))
        if step == GeoreferenceStep.Stop and status == ProcessStatus.Success:
            if self._closeOnDone:
                self._close()
            else:
                self._toggleUi(True)

    def _updateError(self, step, msg):
        self._setStatusLabel(step, ProcessStatus.Failure)
        self._showStatus(msg)
        self._toggleUi(True)

    def _showStatus(self, text):
        self.statusBar.showMessage(text)

    def _save(self):
        self._copyInputFile()
        self._saveGcp()
        self._close()

    def _copyInputFile(self):
        if self.inputFileName() != self.rawFileName() or self._inputFile.dir() != self._type()['raw']:
            QFile.copy(self._inputFile.absoluteFilePath(), self.rawFileInfo().absoluteFilePath())

    def _saveGcp(self):
        gc = self._gc()
        if (gc.isValid()):
            Georeferencer.writeGcpFile(gc, self.pointFileInfo().absoluteFilePath())

    def _run(self):
        self._runGeoreference(False)

    def _process(self):
        self._runGeoreference(True)

    def _close(self):
        if (self._georeferencer.step() == GeoreferenceStep.Stop):
            self.accept()
        else:
            self.reject()

    def _gc(self):
        gc = Transform()
        gc.crs = self._type()['crs']
        gc.setPoint(1, self.gcpWidget1.gcp())
        gc.setPoint(2, self.gcpWidget2.gcp())
        gc.setPoint(3, self.gcpWidget3.gcp())
        gc.setPoint(4, self.gcpWidget4.gcp())
        return gc

    def _runGeoreference(self, closeOnDone):
        self._closeOnDone = closeOnDone
        gc = self._gc()
        if (not gc.isValid()):
            self._showStatus('ERROR: Please set all 4 Ground Control Points!')
            return
        self._toggleUi(False)
        self._copyInputFile()
        QCoreApplication.processEvents()
        self._georeferencer.run(gc, self.rawFileInfo(), self.pointFileInfo(), self.geoFileInfo())

    def _finished(self, step, status):
        if step == GeoreferenceStep.Stop and status == ProcessStatus.Success and self._closeOnDone:
            self._close()
        else:
            self._toggleUi(True)

    def _setStatusLabel(self, step, status):
        if step == 'load':
            label = self.loadStatusLabel
        elif step == GeoreferenceStep.Crop:
            label = self.cropStatusLabel
        elif step == GeoreferenceStep.Translate:
            label = self.translateStatusLabel
        elif step == GeoreferenceStep.Warp:
            label = self.warpStatusLabel
        elif step == GeoreferenceStep.Overview:
            label = self.overviewStatusLabel
        else:
            return

        if status == ProcessStatus.Success:
            label.setPixmap(QPixmap(':/plugins/ark/georef/success.png'))
        elif status == ProcessStatus.Failure:
            label.setPixmap(QPixmap(':/plugins/ark/georef/failure.png'))
        elif status == ProcessStatus.Running:
            label.setPixmap(QPixmap(':/plugins/ark/georef/running.png'))
        else:
            label.setPixmap(QPixmap(':/plugins/ark/georef/unknown.png'))
