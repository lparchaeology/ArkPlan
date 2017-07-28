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

import os

from PyQt4.QtCore import Qt, QPoint, QPointF

from qgis.core import QgsPoint

class GroundControl():

    crt = 'EPSG:27700'
    _points = {}

    def points(self):
        return self._points

    def point(self, index):
        return self._points[index]

    def setPoint(self, index, point):
        self._points[index] = point

    def appendPoint(self, point):
        size = len(self._points)
        if size == 0:
            index = 1;
        else:
            keys = sorted(self._points, reverse=True)
            index = keys[0] + 1
        self.setPoint(index, point)

    def isValid(self):
        for index in self._points:
            if !self._point[index].isValid():
                return false
        return true

    def isNull(self):
        for index in self._points:
            if !self._point[index].isNull():
                return false
        return true

class GroundControlPoint():

    _raw = QPointF()
    _map = QgsPoint()
    _local = QPoint()
    _enabled = True

    def __init__(self, raw, map, enabled=True):
        self.setRaw(raw)
        self.setMap(map)
        self.setEnabled(enabled)

    def isValid(self):
        return !self._map.isNull() and !self._map.isNull()

    def isNull(self):
        return self._map.isNull() and self._map.isNull()

    def raw(self):
        return self._raw

    def setRaw(self, raw):
        self._raw = raw

    def setRawX(self, x):
        self._raw.setX(x)

    def setRawY(self, y):
        self._raw.setY(y)

    def map(self):
        return self._map

    def setMap(self, map):
        self._map = map

    def local(self):
        return self._local

    def setLocal(self, local):
        self._local = local

    def isEnabled(self):
        return self._enabled

    def setEnabled(self, enabled):
        self._enabled = enabled
