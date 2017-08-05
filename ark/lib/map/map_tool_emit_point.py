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
        copyright            : 2010 by Jürgen E. Fischer
        copyright            : 2007 by Marco Hugentobler
        copyright            : 2006 by Martin Dobias
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
from PyQt4.QtCore import Qt, pyqtSignal
from qgis.core import QgsPoint
from qgis.gui import QgsVertexMarker

import .MapToolInteractive


class MapToolEmitPoint(MapToolInteractive):

    """Tool to emit mouse clicks as map points."""

    canvasClicked = pyqtSignal(QgsPoint, Qt.MouseButton)

    _vertexMarker = None  # QgsVertexMarker

    def __init__(self, canvas):
        super(MapToolEmitPoint, self).__init__(canvas)
        self._vertexMarker = QgsVertexMarker(canvas)
        self._vertexMarker.setIconType(QgsVertexMarker.ICON_NONE)

    def deactivate(self):
        self._vertexMarker.setCenter(QgsPoint())
        super(MapToolEmitPoint, self).deactivate()

    def canvasReleaseEvent(self, e):
        super(MapToolEmitPoint, self).canvasReleaseEvent(e)
        if e.isAccepted():
            return
        # Emit mode
        mapPoint, snapped = self._snapCursorPoint(e.pos())
        self._vertexMarker.setCenter(mapPoint)
        self.canvasClicked.emit(mapPoint, e.button())
        e.accept()

    def setVertexIcon(self, iconType, iconSize=None, penWidth=None, color=None):
        self._vertexMarker.setIconType(iconType)
        if iconSize is not None:
            self._vertexMarker.setIconSize(iconSize)
        if iconSize is not None:
            self._vertexMarker.setPenWidth(penWidth)
        if iconSize is not None:
            self._vertexMarker.setColor(color)
