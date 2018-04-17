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

from PyQt4.QtCore import Qt, pyqtSignal
from PyQt4.QtGui import QAction, QIcon, QLabel, QToolButton, QWidget

from ArkSpatial.ark.lib.core import FeatureType, geometry
from ArkSpatial.ark.lib.map import MapToolAddFeature

from ArkSpatial.ark.core import Audit, Config, Feature, Item, Source

from .ui.feature_widget_base import Ui_FeatureWidget


class FeatureWidget(QWidget, Ui_FeatureWidget):

    featureChanged = pyqtSignal()
    autoToolSelected = pyqtSignal()

    def __init__(self, parent=None):
        super(FeatureWidget, self).__init__(parent)
        self.setupUi(self)

        self._item = Item()
        self._source = Source()
        self._audit = Audit()
        self._actions = {}
        self._mapTools = {}
        self._currentMapTool = None
        self._collection = None
        self._iface = None
        self._definitiveCategories = set()
        self._colMax = 6
        self._pointTool = 0
        self._lineTool = 0
        self._polygonTool = 0

    def initGui(self, iface, collection):
        self._iface = iface
        for key in sorted(Config.classCodes.keys()):
            classCode = Config.classCodes[key]
            if classCode['source']:
                self.classCombo.addItem(classCode['label'], classCode['class'])

        self._addStandardTool(
            FeatureType.Point, ':/plugins/ark/plan/editPoints.svg', u'Points Node Tool', self._editPointsLayer)
        self._addStandardTool(
            FeatureType.Point, ':/plugins/ark/plan/selectPoints.svg', u'Points Select Tool', self._selectPointsLayer
        )

        self._addStandardTool(
            FeatureType.Line, ':/plugins/ark/plan/editLines.svg', u'Lines Node Tool', self._editLinesLayer
        )
        self._addStandardTool(
            FeatureType.Line, ':/plugins/ark/plan/selectLines.svg', u'Lines Select Tool', self._selectLinesLayer
        )

        self._addStandardTool(
            FeatureType.Polygon, ':/plugins/ark/plan/editPolygons.svg', u'Polygons Node Tool', self._editPolygonsLayer
        )
        self._addStandardTool(
            FeatureType.Polygon, ':/plugins/ark/plan/selectPolygons.svg', u'Polygons Select Tool', self._selectPolygonsLayer
        )
        # TODO Make generic somehow
        if collection == 'plan':
            self._addStandardTool(
                FeatureType.Polygon, ':/plugins/ark/plan/addPolygons.svg', u'Auto-Schematic Tool', self._autoSchematicSelected
            )

        self._addToolSpacer(self.pointToolLayout)
        self._pointTool = self._colMax
        self._addToolSpacer(self.lineToolLayout)
        self._lineTool = self._colMax
        self._addToolSpacer(self.polygonToolLayout)
        self._polygonTool = self._colMax

        for feature in Config.featureCollections[collection]:
            category = Config.featureCategories[feature['category']]
            if 'query' not in category:
                category['query'] = None
            self._addDrawingTool(
                feature['class'], feature['category'], category['name'], QIcon(), category['type'], category['query']
            )
            if category['definitive'] is True:
                self._definitiveCategories.add(feature['category'])

        self.idEdit.editingFinished.connect(self.featureChanged)
        self.commentEdit.editingFinished.connect(self.featureChanged)

    def unloadGui(self):
        for action in self._actions.values():
            if action.isChecked():
                action.setChecked(False)

    def loadProject(self, plugin, collection):
        self._collection = plugin.project().collection(collection)
        for category in self._mapTools:
            mapTool = self._mapTools[category]
            layer = None
            if mapTool.featureType() == FeatureType.Point:
                layer = self._collection.buffer('points')
            elif mapTool.featureType() == FeatureType.Polygon:
                layer = self._collection.buffer('polygons')
            elif mapTool.featureType() == FeatureType.Line or mapTool.featureType() == FeatureType.Segment:
                layer = self._collection.buffer('lines')
            self._mapTools[category].setLayer(layer)

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

        self.sourceCodeCombo.setCurrentIndex(self.sourceCodeCombo.findData(self._source.sourceCode()))
        self.commentEdit.setText(feature.comment())

        idx = self.siteCodeCombo.findData(self._source.item().siteCode())
        if idx >= 0:
            self.siteCodeCombo.setCurrentIndex(idx)
        self.sourceClassCombo.setCurrentIndex(self.sourceClassCombo.findData(self._source.item.classCode()))
        self.sourceIdEdit.setText(self._source.item().itemId())

        self.blockSignals(False)

    def _item(self):
        return Item(self._source.siteCode(), self._sourceClass(), self._sourceId())

    def _classCode(self):
        return self.classCodeCombo.itemData(self.sourceClassCombo.currentIndex())

    def _itemId(self):
        return self.idEdit.text().strip()

    def _label(self):
        return self.commentEdit.text().strip()

    def _comment(self):
        return self.commentEdit.text().strip()

    # Drawing Tools

    def _addToolButton(self, action, featureType):
        toolButton = QToolButton(self)
        toolButton.setFixedWidth(30)
        toolButton.setFixedHeight(30)
        toolButton.setDefaultAction(action)
        if featureType == FeatureType.Point:
            self._addToolWidget(self.pointToolLayout, toolButton, self._pointTool)
            self._pointTool += 1
        elif featureType == FeatureType.Line or featureType == FeatureType.Segment:
            self._addToolWidget(self.lineToolLayout, toolButton, self._lineTool)
            self._lineTool += 1
        elif featureType == FeatureType.Polygon:
            self._addToolWidget(self.polygonToolLayout, toolButton, self._polygonTool)
            self._polygonTool += 1

    def _addStandardTool(self, featureType, icon, tooltip, slot=None):
        action = QAction(QIcon(icon), '', self)
        action.setToolTip(tooltip)
        action.setCheckable(False)
        action.triggered.connect(slot)
        self._addToolButton(action, featureType)

    def _addDrawingTool(self, classCode, category, toolName, icon, featureType, query=None):
        data = {}
        data['class'] = classCode
        data['category'] = category
        action = QAction(icon, category, self)
        action.setData(data)
        action.setToolTip(toolName)
        action.setCheckable(True)

        mapTool = MapToolAddFeature(self._iface, featureType, toolName)
        mapTool.setAction(action)
        mapTool.setPanningEnabled(True)
        mapTool.setZoomingEnabled(True)
        mapTool.setSnappingEnabled(True)
        mapTool.setShowSnappableVertices(True)
        mapTool.activated.connect(self._mapToolActivated)
        if query is not None:
            field = Config.fields[query]
            mapTool.setAttributeQuery(
                field['attribute'],
                field['type'],
                field['default'],
                field['label'],
                field['query'],
                field['min'],
                field['max'],
                field['decimals']
            )

        self._addToolButton(action, featureType)
        self._actions[category] = action
        self._mapTools[category] = mapTool

    def _mapToolActivated(self):
        for mapTool in self._mapTools.values():
            if mapTool.action().isChecked():
                if not mapTool.layer().isEditable():
                    mapTool.layer().startEditing()
                self._setMapToolAttributes(mapTool)

    def _updateMapToolAttributes(self):
        for mapTool in self._mapTools.values():
            if mapTool.action().isChecked():
                self._setMapToolAttributes(mapTool)

    def _setMapToolAttributes(self, mapTool):
        return
        if mapTool is None:
            return
        toolData = mapTool.action().data()
        if toolData['class'] != self.metadata.classCode():
            self.metadata.setItemId('')
        self.metadata.setClassCode(toolData['class'])
        self.metadata.setCategory(toolData['category'])
        mapTool.setDefaultAttributes(self.metadata.feature.toAttributes())

    def clearDrawingTools(self):
        self._clearDrawingTools(self.pointToolLayout)
        self._clearDrawingTools(self.lineToolLayout)
        self._clearDrawingTools(self.polygonToolLayout)

    def _clearDrawingTools(self, layout):
        if layout.count():
            for i in range(layout.count() - 1, 0):
                layout.takeAt(i)

    def _addToolWidget(self, layout, toolButton, counter):
        layout.addWidget(toolButton, counter // self._colMax, counter % self._colMax, Qt.AlignCenter)

    def _addToolSpacer(self, layout):
        while layout.columnCount() < self._colMax:
            label = QLabel()
            layout.addWidget(label, 0, layout.columnCount() % self._colMax)

    def _editLayer(self, layer):
        self._iface.setActiveLayer(layer)
        if not layer.isEditable():
            layer.startEditing()
        self._iface.actionNodeTool().trigger()

    def _editPointsLayer(self):
        self._editLayer(self._collection.layer('points'))

    def _editLinesLayer(self):
        self._editLayer(self._collection.layer('lines'))

    def _editPolygonsLayer(self):
        self._editLayer(self._collection.layer('polygons'))

    def _selectLayer(self, layer):
        self._iface.setActiveLayer(layer)
        self._iface.actionSelect().trigger()

    def _selectPointsLayer(self):
        self._selectLayer(self._collection.layer('points'))

    def _selectLinesLayer(self):
        self._selectLayer(self._collection.layer('lines'))

    def _selectPolygonsLayer(self):
        self._selectLayer(self._collection.layer('polygons'))

    def _autoSchematicSelected(self):
        self.actions['sch'].trigger()
        self._autoSchematic(self.metadata, self._collection.layer('lines'), self._collection.layer('polygons'))

    def _autoSchematic(self, md, inLayer, outLayer):
        definitiveFeatures = []
        if inLayer.selectedFeatureCount() > 0:
            definitiveFeatures = inLayer.selectedFeatures()
        else:
            featureIter = inLayer.getFeatures()
            for feature in featureIter:
                if (feature.attribute('id') == self.itemId()
                        and feature.attribute('category') in self._definitiveCategories):
                    definitiveFeatures.append(feature)
        if len(definitiveFeatures) <= 0:
            return
        schematicFeatures = geometry.polygonizeFeatures(definitiveFeatures, outLayer.pendingFields())
        if len(schematicFeatures) <= 0:
            return
        schematic = geometry.dissolveFeatures(schematicFeatures, outLayer.pendingFields())
        attrs = md.feature.toAttributes()
        for attr in attrs.keys():
            schematic.setAttribute(attr, attrs[attr])
        outLayer.beginEditCommand("Add Auto Schematic")
        outLayer.addFeature(schematic)
        outLayer.endEditCommand()
        self.plugin.mapCanvas().refresh()
