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
from copy import deepcopy

from PyQt4.QtCore import Qt, QPointF

from qgis.core import QgsPoint, QgsMessageLog

class GroundControl():

    crs = 'EPSG:27700'
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
            if not self._points[index].isValid():
                return False
        return True

    def asCsv(self):
        csv = 'mapX,mapY,pixelX,pixelY,enable\n'
        for index in sorted(self._points):
            csv += self._points[index].asCsv() + '\n'
        return csv

    def _log(self, msg):
        QgsMessageLog.logMessage(str(msg), 'ARK', QgsMessageLog.INFO)

class GroundControlPoint():

    _raw = QPointF()
    _map = QgsPoint()
    _local = QPointF()
    _enabled = True

    def __init__(self, raw=None, map=None, enabled=True):
        self.setRaw(raw)
        self.setMap(map)
        self.setEnabled(enabled)

    def isValid(self):
        return self.isRawSet() and self.isMapSet()

    def isRawSet(self):
        return self._raw is not None

    def raw(self):
        if self._raw is None:
            return QPointF()
        else:
            return self._raw

    def setRaw(self, raw):
        if raw is None:
            self._raw = None
        else:
            self._raw = raw

    def setRawX(self, x):
        if self._raw is None:
            self._raw = QPointF()
        self._raw.setX(x)

    def setRawY(self, y):
        if self._raw is None:
            self._raw = QPointF()
        self._raw.setY(y)

    def isMapSet(self):
        return self._raw is not None

    def map(self):
        if self._map is None:
            return QgsPoint()
        else:
            return self._map

    def setMap(self, map):
        if map is None:
            self._map = None
        else:
            self._map = map

    def local(self):
        if self._local is None:
            return QPointF()
        else:
            return self._local

    def setLocal(self, local):
        if local is None:
            self._local = None
        else:
            self._local = local

    def isEnabled(self):
        return self._enabled

    def setEnabled(self, enabled):
        self._enabled = enabled

    def asCsv(self):
        return ','.join([str(self.map().x()), str(self.map().y()), str(self.raw().x()), str(self.raw().y()), str(int(self._enabled))])

    def _log(self, msg):
        QgsMessageLog.logMessage(str(msg), 'ARK', QgsMessageLog.INFO)
