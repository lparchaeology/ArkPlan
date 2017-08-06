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
        copyright            : 2014 by Olivier Dalang
        copyright            : 2013 by Piotr Pociask
        copyright            : 2013 by Victor Olaya
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

from qgis.core import QgsFeature, QgsGeometry, QgsPoint

from shapely.geometry import LineString, MultiLineString, Point
from shapely.ops import polygonize, unary_union


def polygonizeFeatures(features, fields=None):
    # Adapted from QGIS Processing plugin Polygonize by Piotr Pociask
    lineList = []
    for inFeat in features:
        inGeom = inFeat.geometry()
        if inGeom is None:
            pass
        elif inGeom.isMultipart():
            lineList.extend(inGeom.asMultiPolyline())
        else:
            lineList.append(inGeom.asPolyline())
    allLines = MultiLineString(lineList)
    allLines = unary_union(allLines)
    polygons = list(polygonize([allLines]))
    outList = []
    for polygon in polygons:
        outFeat = QgsFeature(fields)
        outFeat.setGeometry(QgsGeometry.fromWkt(polygon.wkt))
        outList.append(outFeat)
    return outList


def dissolveFeatures(features, fields=None, attributes=None):
    # Adapted from QGIS Processing plugin Dissolve by Victor Olaya
    outFeat = QgsFeature(fields)
    first = True
    for inFeat in features:
        if first:
            tmpInGeom = QgsGeometry(inFeat.geometry())
            outFeat.setGeometry(tmpInGeom)
            first = False
        else:
            tmpInGeom = QgsGeometry(inFeat.geometry())
            tmpOutGeom = QgsGeometry(outFeat.geometry())
            try:
                tmpOutGeom = QgsGeometry(tmpOutGeom.combine(tmpInGeom))
                outFeat.setGeometry(tmpOutGeom)
            except:
                pass
    if attributes is not None:
        outFeat.setAttributes(attributes)
    return outFeat


def perpendicularPoint(lineGeometry, point):
    """Returns a point on the given line that is perpendicular to the given point."""
    if lineGeometry is None or lineGeometry.isEmpty() or point is None:
        return QgsPoint()
    return lineGeometry.nearestPoint(point)
    # In 2.14 use QgsGeometry.nearestPoint()
    line = toMultiLineString(lineGeometry)
    perp = line.interpolate(line.project(Point(point)))
    return QgsPoint(perp.x, perp.y)


def clipLine(lineGeometry, pt1, pt2):
    """Returns a line cliipped to the extent of two given points"""
    # Assumes pt1, pt2 lie on line
    if lineGeometry is None or lineGeometry.isEmpty() or pt1 is None or pt2 is None:
        return QgsGeometry()
    line = LineString(lineGeometry.asPolyline())
    d1 = line.project(Point(pt1))
    d2 = line.project(Point(pt2))
    if d1 < d2:
        start = pt1
        ds = d1
        end = pt2
        de = d2
    else:
        start = pt2
        ds = d2
        end = pt1
        de = d1
    clip = []
    clip.append(start)
    for coord in line.coords:
        pt = Point(coord)
        dp = line.project(pt)
        if dp > ds and dp < de:
            clip.append(QgsPoint(pt.x, pt.y))
    clip.append(end)
    return QgsGeometry.fromPolyline(clip)


def toMultiLineString(lineGeometry):
    lineList = []
    if lineGeometry.isMultipart():
        lineList.extend(lineGeometry.asMultiPolyline())
    else:
        lineList.append(lineGeometry.asPolyline())
    return MultiLineString(lineList)
