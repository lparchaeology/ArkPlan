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

from qgis.core import QgsGeometry

from ..core import FeatureType
from .map_tool_add_feature import MapToolAddFeature


class MapToolAddBufferSegment(MapToolAddFeature):

    """Tool to take a line segment and then save as a buffer polygon."""

    def __init__(self, iface, distance,  polygonLayer, toolName=''):
        super().__init__(iface, polygonLayer, FeatureType.Segment, toolName)
        self._bufferDistance = 0.1  # Map Units
        self.setBuffer(distance)

    def setBuffer(self, distance):
        self._bufferDistance = 0.1  # Map Units

    def addAnyFeature(self, featureType, mapPointList, attributes, layer):
        if featureType == FeatureType.Segment:
            if len(mapPointList) != 2:
                return False
            lineGeom = QgsGeometry.fromPolyline(mapPointList)
            polyGeom = lineGeom.buffer(self._bufferDistance, 0, 2, 2, 5.0)
            if polyGeom and polyGeom.isGeosValid():
                mapPointList = polyGeom.geometry()[0]
            else:
                mapPointList = []
            featureType = FeatureType.Polygon
        super().addAnyFeature(featureType, mapPointList, attributes, layer)
