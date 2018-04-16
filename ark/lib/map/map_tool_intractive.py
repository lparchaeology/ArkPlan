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

from PyQt4.QtCore import QRect, Qt
from PyQt4.QtGui import QColor, QCursor

from qgis.core import QGis, QgsGeometry, QgsPoint, QgsPointV2, QgsProject, QgsRectangle
from qgis.gui import QgsMapCanvasSnapper, QgsMapTool, QgsRubberBand, QgsVertexMarker

from ..gui import CapturePointCursor


class MapToolInteractive(QgsMapTool):

    """Tool to interact with map, including panning, zooming, and snapping"""

    def __init__(self, canvas, snappingEnabled=False, showSnappableVertices=False):
        super(MapToolInteractive, self).__init__(canvas)
        self._active = False
        self._dragging = False
        self._panningEnabled = False
        self._zoomingEnabled = False
        self._zoomRubberBand = None  # QgsRubberBand()
        self._zoomRect = None  # QRect()
        self._snappingEnabled = False
        self._snapper = None  # QgsMapCanvasSnapper()
        self._snappingMarker = None  # QgsVertexMarker()
        self._showSnappableVertices = False
        self._snappableVertices = []  # [QgsPointV2()]
        self._snappableMarkers = []  # [QgsVertexMarker()]
        self._snappingEnabled = snappingEnabled
        self._showSnappableVertices = showSnappableVertices

    def __del__(self):
        if self._active:
            self.deactivate()

    def isActive(self):
        return self._active

    def activate(self):
        super(MapToolInteractive, self).activate()
        self._active = True
        self._startSnapping()

    def deactivate(self):
        self._active = False
        if self._snappingEnabled:
            self._stopSnapping()
        if (self._zoomRubberBand is not None):
            self.canvas().scene().removeItem(self._zoomRubberBand)
            self._zoomRubberBand = None
        super(MapToolInteractive, self).deactivate()

    def setAction(self, action):
        super(MapToolInteractive, self).setAction(action)
        self.action().triggered.connect(self._activate)

    def _activate(self):
        self.canvas().setMapTool(self)

    def panningEnabled(self):
        return self._panningEnabled

    def setPanningEnabled(self, enabled):
        self._panningEnabled = enabled

    def zoomingEnabled(self):
        return self._zoomingEnabled

    def setZoomingEnabled(self, enabled):
        self._zoomingEnabled = enabled

    def snappingEnabled(self):
        return self._snappingEnabled

    def setSnappingEnabled(self, enabled):
        if (self._snappingEnabled == enabled):
            return
        self._snappingEnabled = enabled
        if not self._active:
            return
        if enabled:
            self._startSnapping()
        else:
            self._stopSnapping()

    def _startSnapping(self):
        self._snapper = QgsMapCanvasSnapper()
        self._snapper.setMapCanvas(self.canvas())
        if self._showSnappableVertices:
            self._startSnappableVertices()

    def _stopSnapping(self):
        self._deleteSnappingMarker()
        self._snapper = None
        if self._showSnappableVertices:
            self._stopSnappableVertices()

    def showSnappableVertices(self):
        return self._showSnappableVertices

    def setShowSnappableVertices(self, show):
        if (self._showSnappableVertices == show):
            return
        self._showSnappableVertices = show
        if not self._active:
            return
        if show:
            self._startSnappableVertices()
        else:
            self._stopSnappableVertices()

    def _startSnappableVertices(self):
        self.canvas().layersChanged.connect(self._layersChanged)
        self.canvas().extentsChanged.connect(self._redrawSnappableMarkers)
        QgsProject.instance().snapSettingsChanged.connect(self._layersChanged)
        self._layersChanged()

    def _stopSnappableVertices(self):
        self._deleteSnappableMarkers()
        self._snappableLayers = []
        self.canvas().layersChanged.disconnect(self._layersChanged)
        self.canvas().extentsChanged.disconnect(self._redrawSnappableMarkers)
        QgsProject.instance().snapSettingsChanged.disconnect(self._layersChanged)

    def canvasMoveEvent(self, e):
        super(MapToolInteractive, self).canvasMoveEvent(e)
        if not self._active:
            return
        e.ignore()
        if (self._panningEnabled and e.buttons() & Qt.LeftButton):
            # Pan map mode
            if not self._dragging:
                self._dragging = True
                self.setCursor(QCursor(Qt.ClosedHandCursor))
            self.canvas().panAction(e)
            e.accept()
        elif (self._zoomingEnabled and e.buttons() & Qt.RightButton):
            # Zoom map mode
            if not self._dragging:
                self._dragging = True
                self.setCursor(QCursor(Qt.ClosedHandCursor))
                self._zoomRubberBand = QgsRubberBand(self.canvas(), QGis.Polygon)
                color = QColor(Qt.blue)
                color.setAlpha(63)
                self._zoomRubberBand.setColor(color)
                self._zoomRect = QRect(0, 0, 0, 0)
                self._zoomRect.setTopLeft(e.pos())
            self._zoomRect.setBottomRight(e.pos())
            if self._zoomRubberBand is not None:
                self._zoomRubberBand.setToCanvasRectangle(self._zoomRect)
                self._zoomRubberBand.show()
            e.accept()
        elif self._snappingEnabled:
            mapPoint, mapPointV2, snapped = self._snapCursorPoint(e.pos())
            if (snapped):
                self._createSnappingMarker(mapPoint)
            else:
                self._deleteSnappingMarker()

    def canvasReleaseEvent(self, e):
        super(MapToolInteractive, self).canvasReleaseEvent(e)
        e.ignore()
        if (e.button() == Qt.LeftButton):
            if self._dragging:
                # Pan map mode
                self.canvas().panActionEnd(e.pos())
                self.setCursor(CapturePointCursor)
                self._dragging = False
                e.accept()
        elif (e.button() == Qt.RightButton):
            if self._dragging:
                # Zoom mode
                self._zoomRect.setBottomRight(e.pos())
                if (self._zoomRect.topLeft() != self._zoomRect.bottomRight()):
                    coordinateTransform = self.canvas().getCoordinateTransform()
                    ll = coordinateTransform.toMapCoordinates(self._zoomRect.left(), self._zoomRect.bottom())
                    ur = coordinateTransform.toMapCoordinates(self._zoomRect.right(), self._zoomRect.top())
                    r = QgsRectangle()
                    r.setXMinimum(ll.x())
                    r.setYMinimum(ll.y())
                    r.setXMaximum(ur.x())
                    r.setYMaximum(ur.y())
                    r.normalize()
                    if (r.width() != 0 and r.height() != 0):
                        self.canvas().setExtent(r)
                        self.canvas().refresh()
                self._dragging = False
                if (self._zoomRubberBand is not None):
                    self.canvas().scene().removeItem(self._zoomRubberBand)
                    self._zoomRubberBand = None
                e.accept()

    def keyPressEvent(self, e):
        super(MapToolInteractive, self).keyPressEvent(e)
        if (e.key() == Qt.Key_Escape):
            self.canvas().unsetMapTool(self)
            e.accept()

    def _snapCursorPoint(self, cursorPoint):
        res, snapResults = self._snapper.snapToBackgroundLayers(cursorPoint)
        if (res != 0 or len(snapResults) < 1):
            clicked = self.toMapCoordinates(cursorPoint)
            clickedV2 = QgsPointV2(clicked)
            return clicked, clickedV2, False
        else:
            # Take a copy as QGIS will delete the result!
            snapped = QgsPoint(snapResults[0].snappedVertex)
            snappedV2 = QgsPointV2(snapped)
            return snapped, snappedV2, True

    def _createSnappingMarker(self, snapPoint):
        if (self._snappingMarker is None):
            self._snappingMarker = QgsVertexMarker(self.canvas())
            self._snappingMarker.setIconType(QgsVertexMarker.ICON_CROSS)
            self._snappingMarker.setColor(Qt.magenta)
            self._snappingMarker.setPenWidth(3)
        self._snappingMarker.setCenter(snapPoint)

    def _deleteSnappingMarker(self):
        if (self._snappingMarker is not None):
            self.canvas().scene().removeItem(self._snappingMarker)
            self._snappingMarker = None

    def _createSnappableMarkers(self):
        return
        if (not self._showSnappableVertices or not self._snappingEnabled):
            return
        extent = self.canvas().extent()
        for vertex in self._snappableVertices.geometry():
            if (extent.contains(vertex)):
                marker = QgsVertexMarker(self.canvas())
                marker.setIconType(QgsVertexMarker.ICON_X)
                marker.setColor(Qt.gray)
                marker.setPenWidth(1)
                marker.setCenter(vertex)
                self._snappableMarkers.append(marker)

    def _deleteSnappableMarkers(self):
        for marker in self._snappableMarkers:
            self.canvas().scene().removeItem(marker)
        del self._snappableMarkers[:]

    def _layersChanged(self):
        if (not self._showSnappableVertices or not self._snappingEnabled):
            return
        self._buildSnappableLayers()
        self._deleteSnappableMarkers()
        self._createSnappableMarkers()

    def _redrawSnappableMarkers(self):
        if (not self._showSnappableVertices or not self._snappingEnabled):
            return
        self._deleteSnappableMarkers()
        self._createSnappableMarkers()

    def _buildSnappableLayers(self):
        if (not self._showSnappableVertices or not self._snappingEnabled):
            return
        vertices = []
        for layer in self.canvas().layers():
            ok, enabled, type, units, tolerance, avoid = QgsProject.instance().snapSettingsForLayer(layer.id())
            if (ok and enabled and not layer.isEditable()):
                for feature in layer.getFeatures():
                    geometry = feature.geometry()
                    if geometry is None:
                        pass
                    elif geometry.type() == QGis.Point:
                        vertices.extend([geometry.geometry()])
                    elif geometry.type() == QGis.Line:
                        vertices.extend(geometry.geometry())
                    elif geometry.type() == QGis.Polygon:
                        lines = geometry.geometry()
                        for line in lines:
                            vertices.extend(line)
        self._snappableVertices = QgsGeometry.fromMultiPoint(vertices)
        self._snappableVertices.simplify(0)
