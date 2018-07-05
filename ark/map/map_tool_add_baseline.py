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

from qgis.PyQt.QtCore import Qt

from ArkSpatial.ark.lib.core import FeatureType
from ArkSpatial.ark.lib.map import MapToolAddFeature


class MapToolAddBaseline(MapToolAddFeature):

    def __init__(self, iface, lineLayer, pointLayer, pointIdFieldName, toolName=''):
        super(MapToolAddBaseline, self).__init__(iface, lineLayer, toolName)

        self._pointLayer = pointLayer  # QgsVectorLayer()
        self._pointAttributes = {}  # QMap<int, QList<QVariant> >
        self._idFieldName = ''
        self._pointQueryField = None  # QgsField
        self._pointQueryTitle = ''
        self._pointQueryLabel = ''
        self._pointDefaultValue = ''
        self._pointQueryMin = 0
        self._pointQueryMax = 0
        self._pointQueryDecimals = 0
        self._pointQueryValues = []

    def pointLayer(self):
        return self._pointLayer

    def setPointAttributes(self, attributes):
        self._pointAttributes = attributes

    def setPointQuery(self, field, title, label, defaultValue, minValue, maxValue):
        self._pointQueryField = field
        self._pointQueryTitle = title
        self._pointQueryLabel = label
        self._pointDefaultValue = defaultValue
        self._pointQueryMin = minValue
        self._pointQueryMax = maxValue

    def canvasReleaseEvent(self, e):
        wasDragging = self._dragging
        mapPointList = self._mapPointList
        super(MapToolAddBaseline, self).canvasReleaseEvent(e)
        if (wasDragging):
            pass
        elif (e.button() == Qt.LeftButton):
            self._capturePointData()
        elif (e.button() == Qt.RightButton):
            for mapPoint in mapPointList:
                self.addAnyFeature(FeatureType.Point, [mapPoint], self._pointLayer)

    def _capturePointData(self):
        if self._pointQueryField:
            value, ok = self._getValue(self._pointQueryTitle, self._pointQueryLabel, self._pointQueryField.type(
            ), self._pointDefaultValue, self._pointQueryMin, self._pointQueryMax, self._pointQueryField.precision())
            if ok:
                self._pointQueryValues.append(value)
            else:
                self._pointQueryValues.append(None)

    def _addPointFeature(self, mapPointList):
        for i in range(0, len(mapPointList)):
            idx = self._pointLayer.pendingFields().fieldNameIndex(self._idFieldName)
            self._pointAttributes[idx] = 'SSS' + '.' + str(i + 1)
            if self._pointQueryField:
                idx = self._pointLayer.pendingFields().fieldNameIndex(self._pointQueryField.name())
                self._pointAttributes[idx] = self._pointQueryValues[i]
            self.addAnyFeature(FeatureType.Point, [mapPointList[i]], self._pointLayer)
