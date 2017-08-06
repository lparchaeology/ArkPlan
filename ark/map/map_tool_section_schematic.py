# -*- coding: utf-8 -*-
"""
/***************************************************************************
                                ARK QGIS
                        A QGIS utilities library.
        Part of the Archaeological Recording Kit by L-P : Archaeology
                        http://ark.lparchaeology.com
                              -------------------
        copyright            : 2017 by L-P : Heritage LLP
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

from ark.lib.core import FeatureType, geometry
from ark.lib.map import MapToolAddFeature


class MapToolSectionSchematic(MapToolAddFeature):
    # Tool to take a line segment and 'snap' it to a section line then save as a buffer polygon

    _sectionGeometry = None  # QgsGeometry

    def __init__(self, iface, sectionGeometry,  polygonLayer, toolName=''):
        super(MapToolSectionSchematic, self).__init__(iface, polygonLayer, FeatureType.Segment, toolName)
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
        super(MapToolSectionSchematic, self).addAnyFeature(featureType, mapPointList, attributes, layer)
