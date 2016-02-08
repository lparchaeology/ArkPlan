# -*- coding: utf-8 -*-
"""
/***************************************************************************
                                ARK QGIS
                        A QGIS utilities library.
        Part of the Archaeological Recording Kit by L-P : Archaeology
                        http://ark.lparchaeology.com
                              -------------------
        begin                : 2016-01-25
        git sha              : $Format:%H$
        copyright            : 2016 by L-P : Heritage LLP
        email                : ark@lparchaeology.com
        copyright            : 2016 by John Layt
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
from qgis.core import QGis, QgsGeometry

from ..libarkqgis.map_tools import ArkMapToolAddFeature, FeatureType
from ..libarkqgis import geometry
from ..libarkqgis import utils

# Tool to take a line segment and 'snap' it to a section line then save as a buffer polygon
class ArkMapToolSectionSchematic(ArkMapToolAddFeature):

    _sectionGeometry = None  # QgsGeometry

    def __init__(self, iface, sectionGeometry,  polygonLayer, toolName=''):
        super(ArkMapToolSectionSchematic, self).__init__(iface, polygonLayer, FeatureType.Segment, toolName)
        self._sectionGeometry = sectionGeometry

    def setSectionGeometry(self, sectionGeometry):
        self._sectionGeometry = QgsGeometry(sectionGeometry)

    def addAnyFeature(self, featureType, mapPointList, attributes, layer):
        if featureType == FeatureType.Segment:
            if len(mapPointList) != 2 or self._sectionGeometry is None:
                return False
            sectionPointList = []
            for point in mapPointList:
                sectionPointList.append(geometry.perpendicularPoint(self._sectionGeometry, point))
            lineGeom = geometry.clipLine(self._sectionGeometry, sectionPointList[0], sectionPointList[1])
            polyGeom = lineGeom.buffer(0.1, 0, 2, 2, 5.0)
            if polyGeom and polyGeom.isGeosValid():
                mapPointList = polyGeom.asPolygon()[0]
            else:
                mapPointList = []
            featureType = FeatureType.Polygon
        super(ArkMapToolSectionSchematic, self).addAnyFeature(featureType, mapPointList, attributes, layer)

class ArkMapToolAddBaseline(ArkMapToolAddFeature):

    _pointLayer = None  # QgsVectorLayer()
    _pointAttributes = {}  # QMap<int, QList<QVariant> >
    _idFieldName = ''

    _pointQueryField = None  # QgsField
    _pointQueryTitle = ''
    _pointQueryLabel = ''
    _pointDefaultValue = ''
    _pointQueryMin = 0
    _pointQueryMax = 0
    _pointQueryDecimals = 0
    _pointQueryValues = []

    def __init__(self, iface, lineLayer, pointLayer, pointIdFieldName, toolName=''):
        super(ArkMapToolAddBaseline, self).__init__(iface, lineLayer, toolName)
        self._pointLayer = pointLayer

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
        super(ArkMapToolAddBaseline, self).canvasReleaseEvent(e)
        if (wasDragging):
            pass
        elif (e.button() == Qt.LeftButton):
            self._capturePointData()
        elif (e.button() == Qt.RightButton):
            for mapPoint in mapPointList:
                self.addAnyFeature(FeatureType.Point, [mapPoint], self._pointLayer)

    def _capturePointData(self):
        if self._pointQueryField:
            value, ok = self._getValue(self._pointQueryTitle, self._pointQueryLabel, self._pointQueryField.type(), self._pointDefaultValue, self._pointQueryMin, self._pointQueryMax, self._pointQueryField.precision())
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
