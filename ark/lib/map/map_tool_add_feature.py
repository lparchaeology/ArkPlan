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
        copyright            : 2010 by Jürgen E. Fischer
        copyright            : 2007 by Marco Hugentobler
        copyright            : 2006 by Martin Dobias
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

from qgis.PyQt.QtCore import Qt, QVariant
from qgis.PyQt.QtWidgets import QInputDialog

from qgis.core import QgsFeature, QgsGeometry, QgsMapLayer, QgsMapLayerRegistry, QgsVectorDataProvider, QgsWkbTypes
from qgis.gui import QgsMessageBar

from .. import utils
from ..core import FeatureType
from ..gui import FeatureAction
from ..snapping import Snapping
from .map_tool_capture import MapToolCapture


class MapToolAddFeature(MapToolCapture):

    def __init__(self, iface, featureType, toolName=''):

        super().__init__(iface, FeatureType.toGeometryType(featureType))

        self._layer = None  # QgsVectorLayer()
        self._featureType = featureType
        self._defaultAttributes = {}  # key = fieldName, value = fieldValue
        self.mToolName = toolName if toolName else self.tr('Add feature')

        # TODO Eventually merge this with the input action?
        self._queryAttributeName = None
        self._queryType = None
        self._queryAttributeDefault = None
        self._queryTitle = ''
        self._queryLabel = ''
        self._queryDecimals = 0
        self._queryMin = 0
        self._queryMax = 0

    def featureType(self):
        return self._featureType

    def layer(self):
        return self._layer

    def setLayer(self, layer):
        self._layer = layer

    def isEditTool(self):
        return True

    def setDefaultAttributes(self, defaultAttributes):
        self._defaultAttributes = defaultAttributes

    # TODO Eventually merge this with the input action?
    def setAttributeQuery(self, attributeName, attributeType, attributeDefault, title, label, min=0, max=0, decimals=0):
        self._queryAttributeName = attributeName
        self._queryType = attributeType
        self._queryAttributeDefault = attributeDefault
        self._queryTitle = title
        self._queryLabel = label
        self._queryMin = min
        self._queryMax = max
        self._queryDecimals = decimals

    def activate(self):
        super().activate()
        if self._layer is not None:
            self.canvas().setCurrentLayer(self._layer)
            self._iface.legendInterface().setCurrentLayer(self._layer)
            if self._layer.geometryType() == QgsWkbTypes.NullGeometry:
                self._addFeatureAction(QgsFeature(), False)

    def canvasReleaseEvent(self, e):
        super().canvasReleaseEvent(e)
        if (e.isAccepted()):
            return
        if (self.geometryType() == QgsWkbTypes.PointGeometry):
            if (e.button() == Qt.LeftButton):
                self.addFeature()
                e.accept()
        else:
            if (e.button() == Qt.LeftButton):
                if (self.featureType() == FeatureType.Segment and len(self._mapPointList) == 2):
                    self.addFeature()
            elif (e.button() == Qt.RightButton):
                self.addFeature()
                e.accept()

    def addFeature(self):
        if self._queryForAttribute():
            self.addAnyFeature(self._featureType, self._mapPointList, self._defaultAttributes, self._layer)
        self.resetCapturing()

    def addAnyFeature(self, featureType, mapPointList, attributes, layer):
        geometryType = FeatureType.toGeometryType(featureType)

        # points: bail out if there is not exactly one vertex
        if (geometryType == QgsWkbTypes.PointGeometry and len(mapPointList) != 1):
            return False

        # segments: bail out if there are not exactly two vertices
        if (featureType == FeatureType.Segment and len(mapPointList) != 2):
            return False

        # lines: bail out if there are not at least two vertices
        if (featureType == FeatureType.Line and len(mapPointList) < 2):
            return False

        # polygons: bail out if there are not at least three vertices
        if (geometryType == QgsWkbTypes.PolygonGeometry and len(mapPointList) < 3):
            return False

        if (geometryType != layer.geometryType()):
            self.messageEmitted.emit(
                self.tr('Cannot add feature: Layer and Feature geometry type mismatch'), QgsMessageBar.CRITICAL)
            return False

        if (layer.type() != QgsMapLayer.VectorLayer):
            self.messageEmitted.emit(
                self.tr('Cannot add feature: Current layer not a vector layer'), QgsMessageBar.CRITICAL)
            return False

        if (not layer.isEditable()):
            self.messageEmitted.emit(self.tr('Cannot add feature: Current layer not editable'), QgsMessageBar.CRITICAL)
            return False

        provider = layer.dataProvider()
        if (not (provider.capabilities() & QgsVectorDataProvider.AddFeatures)):
            self.messageEmitted.emit(
                self.tr('Cannot add feature: Data provider does not support the addition of features.'),
                QgsMessageBar.CRITICAL)
            return False

        multiType = QgsWkbTypes.isMultiType(layer.wkbType())
        layerPoints = self._layerPoints(mapPointList, layer)
        feature = QgsFeature(layer.pendingFields(), 0)
        geometry = None

        if (geometryType == QgsWkbTypes.PointGeometry):
            if multiType:
                geometry = QgsGeometry.fromMultiPoint([layerPoints[0]])
            else:
                geometry = QgsGeometry(layerPoints[0])
        elif (geometryType == QgsWkbTypes.LineGeometry):
            if multiType:
                geometry = QgsGeometry.fromMultiPolyline([layerPoints])
            else:
                geometry = QgsGeometry.fromPolyline(layerPoints)
        elif (geometryType == QgsWkbTypes.PolygonGeometry):
            if multiType:
                geometry = QgsGeometry.fromMultiPolygon([layerPoints])
            else:
                geometry = QgsGeometry.fromPolygon([layerPoints])
        else:
            self.messageEmitted.emit(self.tr('Cannot add feature. Unknown geometry type'), QgsMessageBar.CRITICAL)
            return False

        if (geometry is None or geometry.isEmpty()):
            self.messageEmitted.emit(self.tr('Cannot add feature. Invalid geometry'), QgsMessageBar.CRITICAL)
            return False
        feature.setGeometry(geometry)

        if (geometryType == QgsWkbTypes.PolygonGeometry):

            avoidIntersectionsReturn = feature.geometry().avoidIntersections()
            if (avoidIntersectionsReturn == 1):
                # not a polygon type. Impossible to get there
                pass
            elif (avoidIntersectionsReturn == 3):
                self.messageEmitted.emit(
                    self.tr('An error was reported during intersection removal'), QgsMessageBar.CRITICAL)

            if (not feature.geometry().asWkb()):  # avoid intersection might have removed the whole geometry
                reason = ''
                if (avoidIntersectionsReturn != 2):
                    reason = self.tr('The feature cannot be added because it\'s geometry is empty')
                else:
                    reason = self.tr(
                        'The feature cannot be added because it\'s geometry collapsed due to intersection avoidance')
                self.messageEmitted.emit(reason, QgsMessageBar.CRITICAL)
                return False

        featureSaved = self._addFeatureAction(feature, attributes, layer, False)

        if (featureSaved and geometryType != QgsWkbTypes.PointGeometry):
            # add points to other features to keep topology up-to-date
            topologicalEditing = Snapping.topologicalEditing()

            # use always topological editing for avoidIntersection.
            # Otherwise, no way to guarantee the geometries don't have a small gap in between.
            intersectionLayers = Snapping.intersectionLayers()
            avoidIntersection = len(intersectionLayers)
            if (avoidIntersection):  # try to add topological points also to background layers
                for intersectionLayer in intersectionLayers:
                    vl = QgsMapLayerRegistry.instance().mapLayer(str(intersectionLayer))
                    # can only add topological points if background layer is editable...
                    if (vl is not None and vl.geometryType() == QgsWkbTypes.PolygonGeometry and vl.isEditable()):
                        vl.addTopologicalPoints(feature.geometry())
            elif (topologicalEditing):
                self._layer.addTopologicalPoints(feature.geometry())

        self.canvas().refresh()

        return True

    def _queryForAttribute(self):
        # TODO Eventually merge this with the input action?
        value = None
        ok = True
        if self._queryAttributeName:
            value, ok = self._getValue(self._queryTitle, self._queryLabel, self._queryType,
                                       self._queryAttributeDefault, self._queryMin, self._queryMax, self._queryDecimals)
            if ok:
                self._defaultAttributes[self._queryAttributeName] = value
        return ok

    def _getValue(self, title, label, valueType=QVariant.String, defaultValue='', minValue=0, maxValue=0, decimals=0):
        if valueType == QVariant.Double:
            return QInputDialog.getDouble(None, title, label, defaultValue, minValue, maxValue, decimals)
        elif valueType == QVariant.Int:
            return QInputDialog.getInt(None, title, label, defaultValue, minValue, maxValue)
        else:
            return QInputDialog.getText(None, title, label, text=defaultValue)

    def _addFeatureAction(self, feature, attributes, layer, showModal=True):
        action = FeatureAction(self.tr('add feature'), feature, layer, -1, -1, self._iface, self)
        res = action.addFeature(attributes, showModal)
        if (showModal):
            action = None
        return res

    def _layerPoints(self, mapPointList, layer):
        layerPoints = []
        if layer is None:
            return layerPoints
        for mapPoint in mapPointList:
            layerPoints.append(self.toLayerCoordinates(layer, mapPoint))
        return layerPoints
