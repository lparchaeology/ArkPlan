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


class Transform():

    def __init__(self):
        self.crs = 'EPSG:27700'
        self._points = {}

    def points(self):
        return self._points

    def point(self, index):
        return self._points[index]

    def setPoint(self, index, point):
        self._points[index] = point

    def appendPoint(self, point):
        size = len(self._points)
        if size == 0:
            index = 1
        else:
            keys = sorted(self._points, reverse=True)
            index = keys[0] + 1
        self.setPoint(index, point)

    def isValid(self):
        for index in self._points:
            if not self._points[index].isValid():
                return False
        return True

    def asCsv(self):
        csv = 'mapX,mapY,pixelX,pixelY,enable\n'
        for index in sorted(self._points):
            csv += self._points[index].asCsv() + '\n'
        return csv
