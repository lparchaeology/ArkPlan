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

from enum import Enum

from qgis.core import Qgis


class FeatureType(Enum):

    NoFeature = 0
    Point = 1
    Elevation = 2
    Segment = 3
    Line = 4
    Polygon = 5

    @staticmethod
    def toGeometryType(featureType):
        if featureType == FeatureType.Point or featureType == FeatureType.Elevation:
            return Qgis.Point
        elif (featureType == FeatureType.Line or featureType == FeatureType.Segment):
            return Qgis.Line
        elif featureType == FeatureType.Polygon:
            return Qgis.Polygon
        return Qgis.UnknownGeometry
