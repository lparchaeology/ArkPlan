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

from PyQt4.QtCore import QPointF

from qgis.core import QgsPointV2

from ArkSpatial.ark.lib import utils


class GroundControlPoint():

    def __init__(self, raw=None, map=None, enabled=True):

        self._raw = QPointF()
        self._map = QgsPointV2()
        self._local = QPointF()
        self._enabled = True

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
            return QgsPointV2()
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
        return utils.csv([self.map().x(), self.map().y(), self.raw().x(), self.raw().y(), int(self._enabled)])
