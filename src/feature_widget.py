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

from PyQt4 import uic
from PyQt4.QtCore import Qt, pyqtSignal
from PyQt4.QtGui import QWidget, QToolButton, QIcon

from ..libarkqgis.map_tools import *

from audit import Audit
from config import Config
from feature import Feature
from source import Source
from item import *

import feature_widget_base

class FeatureWidget(QWidget, feature_widget_base.Ui_FeatureWidget):

    featureChanged = pyqtSignal()
    autoToolSelected = pyqtSignal()

    _item = Item()
    _source = Source()
    _audit = Audit()
    _actions = {}
    _mapTools = {}
    _currentMapTool = None
    _pointsBuffer = None
    _linesBuffer = None
    _polygonsBuffer = None
    _iface = None
    _colMax = 5
    _pointTool = 0
    _lineTool = 0
    _polygonTool = 0

    def __init__(self, parent=None):
        super(FeatureWidget, self).__init__(parent)
        self.setupUi(self)

    def initGui(self, iface, collection):
        self._iface = iface
        for key in sorted(Config.classCodes.keys()):
            classCode = Config.classCodes[key]
            if classCode['source']:
                self.classCombo.addItem(classCode['label'], classCode['code'])

        for feature in Config.featureCategories[collection]:
            if 'query' not in feature:
                feature['query'] = None
            self._addDrawingTool(feature['class'], feature['category'], feature['name'], QIcon(), feature['type'], feature['query'])

        self.idSpin.valueChanged.connect(self.featureChanged)
        self.commentEdit.editingFinished.connect(self.featureChanged)
        self.autoTool.clicked.connect(self.autoToolSelected)

    def unloadGui(self):
        for action in self._actions.values():
            if action.isChecked():
                action.setChecked(False)


    def loadProject(self, project, collection):
        self._pointsBuffer = project.collection(collection).pointsBuffer
        self._linesBuffer = project.collection(collection).linesBuffer
        self._polygonsBuffer = project.collection(collection).polygonsBuffer

    def closeProject(self):
        pass

    def feature(self):
        return Feature(self.source())

    def setItem(self, item):
        self._item = item

    def setSource(self, source):
        self._source = source

    def setFeature(self, feature):
        self.blockSignals(True)
        self.setItem(feature.item())
        self.setSource(feature.source())

        self.sourceCodeCombo.setCurrentIndex(self.sourceCodeCombo.findData(source.sourceCode()))
        self.commentEdit.setText(feature.comment())

        idx = self.siteCodeCombo.findData(source.item().siteCode())
        if idx >= 0:
            self.siteCodeCombo.setCurrentIndex(idx)
        self.sourceClassCombo.setCurrentIndex(self.sourceClassCombo.findData(source.item.classCode()))
        sourceId = source.item().itemId()
        if (isinstance(sourceId, int) and sourceId >=0) or (isinstance(sourceId, str) and sourceId.isdigit() and int(sourceId) >= 0):
            self.sourceIdSpin.setValue(int(sourceId))
        else:
            self.sourceIdSpin.setValue(0)

        self.blockSignals(False)

    def _item(self):
        return Item(self._source.siteCode(), self._sourceClass(), self._sourceId())

    def _classCode(self):
        return self.classCodeCombo.itemData(self.sourceClassCombo.currentIndex())

    def _itemId(self):
        return str(self.itemIdSpin.value())

    def _comment(self):
        return self.commentEdit.text()

    # Drawing Tools

    def _addDrawingTool(self, classCode, category, toolName, icon, featureType, query=None):
        data = {}
        data['class'] = classCode
        data['category'] = category
        action = QAction(icon, category, self)
        action.setData(data)
        action.setToolTip(toolName)
        action.setCheckable(True)

        layer = None
        if (featureType == FeatureType.Line or featureType == FeatureType.Segment):
            layer = self._linesBuffer
        elif featureType == FeatureType.Polygon:
            layer = self._polygonsBuffer
        else:
            layer = self._pointsBuffer

        mapTool = ArkMapToolAddFeature(self._iface, layer, featureType, toolName)
        mapTool.setAction(action)
        mapTool.setPanningEnabled(True)
        mapTool.setZoomingEnabled(True)
        mapTool.setSnappingEnabled(True)
        mapTool.setShowSnappableVertices(True)
        mapTool.activated.connect(self._mapToolActivated)
        if query is not None:
            query = Config.attributeQuery[query]
            mapTool.setAttributeQuery(
                query['attribute'],
                query['type'],
                query['default'],
                query['title'],
                query['label'],
                query['min'],
                query['max'],
                query['decimals']
            )

        toolButton = QToolButton(self)
        toolButton.setFixedWidth(40)
        toolButton.setDefaultAction(action)
        if featureType == FeatureType.Point:
            self._addToolWidget(self.pointToolLayout, toolButton, self._pointTool)
            self._pointTool += 1
        if featureType == FeatureType.Line or featureType == FeatureType.Segment:
            self._addToolWidget(self.lineToolLayout, toolButton, self._lineTool)
            self._lineTool += 1
        if featureType == FeatureType.Polygon:
            self._addToolWidget(self.polygonToolLayout, toolButton, self._polygonTool)
            self._polygonTool += 1

        self._actions[category] = action
        self._mapTools[category] = mapTool

    def _mapToolActivated(self):
        for mapTool in self.mapTools.values():
            if mapTool.action().isChecked():
                if not mapTool.layer().isEditable():
                    mapTool.layer().startEditing()
                self._setMapToolAttributes(mapTool)

    def _updateMapToolAttributes(self):
        for mapTool in self.mapTools.values():
            if mapTool.action().isChecked():
                self._setMapToolAttributes(mapTool)

    def _setMapToolAttributes(self, mapTool):
        if mapTool is None:
            return
        toolData = mapTool.action().data()
        if toolData['class'] != self.metadata.classCode():
            self.metadata.setItemId('')
        self.metadata.setClassCode(toolData['class'])
        self.metadata.setCategory(toolData['category'])
        mapTool.setDefaultAttributes(self.metadata.itemFeature.toAttributes())

    def _clearDrawingTools(self):
        self._clearDrawingTools(self.pointToolLayout)
        self._clearDrawingTools(self.lineToolLayout)
        self._clearDrawingTools(self.polygonToolLayout)

    def _clearDrawingTools(self, layout):
        if layout.count():
            for i in range(layout.count() - 1, 0):
                layout.takeAt(i)

    def _addToolWidget(self, layout, toolButton, counter):
        layout.addWidget(toolButton, counter // self._colMax, counter % self._colMax, Qt.AlignCenter)
