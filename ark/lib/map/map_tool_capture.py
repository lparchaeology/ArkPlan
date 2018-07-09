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

from qgis.PyQt.QtCore import QSettings, Qt, pyqtSignal
from qgis.PyQt.QtGui import QColor

from qgis.core import Qgis, QgsGeometry, QgsGeometryValidator, QgsMapLayer, QgsPointV2
from qgis.gui import QgsRubberBand, QgsVertexMarker

from ..gui.cursors import CapturePointCursor
from .map_tool_intractive import MapToolInteractive


class MapToolCapture(MapToolInteractive):

    """Tool to capture and show mouse clicks as geometry using map points."""

    canvasClicked = pyqtSignal(QgsPointV2, Qt.MouseButton)

    def __init__(self, iface, geometryType=Qgis.UnknownGeometry):
        super().__init__(iface.mapCanvas())

        self._iface = iface
        self._useCurrentLayerGeometry = False
        self._geometryType = geometryType
        self._mapPointList = []  # QList<QgsPointV2>
        self._rubberBand = None  # QgsRubberBand()
        self._moveRubberBand = None  # QgsRubberBand()
        self._tip = ''
        self._validator = None  # QgsGeometryValidator()
        self._geometryErrors = []  # QList<QgsGeometry.Error>
        self._geometryErrorMarkers = []  # QList<QgsVertexMarker>

        if (geometryType == Qgis.UnknownGeometry):
            self._useCurrentLayerGeometry = True
        self.setCursor(CapturePointCursor)

    def __del__(self):
        self.deactivate()
        super().__del__()

    def activate(self):
        super().activate()
        geometryType = self.geometryType()
        self._rubberBand = self._createRubberBand(geometryType)
        self._moveRubberBand = self._createRubberBand(geometryType, True)
        if (self._useCurrentLayerGeometry is True):
            self._iface.currentLayerChanged.connect(self._currentLayerChanged)

    def deactivate(self):
        self.resetCapturing()
        if (self._rubberBand is not None):
            self.canvas().scene().removeItem(self._rubberBand)
            self._rubberBand = None
        if (self._moveRubberBand is not None):
            self.canvas().scene().removeItem(self._moveRubberBand)
            self._moveRubberBand = None
        if (self._useCurrentLayerGeometry is True):
            self._iface.currentLayerChanged.disconnect(self._currentLayerChanged)
        super().deactivate()

    def geometryType(self):
        if (self._useCurrentLayerGeometry and self.canvas().currentLayer().type() == QgsMapLayer.VectorLayer):
            return self.canvas().currentLayer().geometryType()
        else:
            return self._geometryType

    def _currentLayerChanged(self, layer):
        if (not self._useCurrentLayerGeometry):
            return
        # TODO Update rubber bands
        if (self._rubberBand is not None):
            self._rubberBand.reset(self.geometryType())
            for point in self._mapPointList[:-1]:
                self._rubberBand.addPoint(point, False)
        self._updateMoveRubberBand(self._mapPointList[-1])
        self._validateGeometry()
        self.canvas().refresh()

    def canvasMoveEvent(self, e):
        super().canvasMoveEvent(e)
        if e.isAccepted():
            return
        if (self._moveRubberBand is not None):
            # Capture mode
            mapPoint, mapPointV2, snapped = self._snapCursorPoint(e.pos())
            self._moveRubberBand.movePoint(mapPoint)

    def canvasReleaseEvent(self, e):
        super().canvasReleaseEvent(e)
        if e.isAccepted():
            return
        mapPoint, mapPointV2, snapped = self._snapCursorPoint(e.pos())
        if (e.button() == Qt.LeftButton):
            # Capture mode
            self._addVertex(mapPoint, mapPointV2)
        # Emit mode
        self.canvasClicked.emit(mapPointV2, e.button())

    def keyPressEvent(self, e):
        if (e.key() == Qt.Key_Escape):
            self.resetCapturing()
            e.accept()
        elif (e.key() == Qt.Key_Backspace or e.key() == Qt.Key_Delete):
            self._undo()
            e.accept()
        else:
            super().keyPressEvent(e)

    def _createRubberBand(self, geometryType, moveBand=False):
        settings = QSettings()
        rb = QgsRubberBand(self.canvas(), geometryType)
        rb.setWidth(int(settings.value('/qgis/digitizing/line_width', 1)))
        color = QColor(int(settings.value('/qgis/digitizing/line_color_red', 255)),
                       int(settings.value('/qgis/digitizing/line_color_green', 0)),
                       int(settings.value('/qgis/digitizing/line_color_blue', 0)))
        myAlpha = int(settings.value('/qgis/digitizing/line_color_alpha', 200)) / 255.0
        if (moveBand):
            myAlpha = myAlpha * float(settings.value('/qgis/digitizing/line_color_alpha_scale', 0.75))
            rb.setLineStyle(Qt.DotLine)
        if (geometryType == Qgis.Polygon):
            color.setAlphaF(myAlpha)
        color.setAlphaF(myAlpha)
        rb.setColor(color)
        rb.show()
        return rb

    def _addVertex(self, mapPoint, mapPointV2):
        self._mapPointList.append(mapPoint)
        self._rubberBand.addPoint(mapPoint)
        self._updateMoveRubberBand(mapPoint)
        self._validateGeometry()
        return

    def _updateMoveRubberBand(self, mapPoint):
        if (self._moveRubberBand is None):
            return
        geometryType = self.geometryType()
        self._moveRubberBand.reset(geometryType)
        if (geometryType == Qgis.Polygon):
            self._moveRubberBand.addPoint(self._rubberBand.getPoint(0, 0), False)
            self._moveRubberBand.movePoint(mapPoint, False)
        self._moveRubberBand.addPoint(mapPoint)

    def _undo(self):
        if (self._rubberBand is not None):
            rubberBandSize = self._rubberBand.numberOfVertices()
            moveRubberBandSize = self._moveRubberBand.numberOfVertices()

            if (rubberBandSize < 1 or len(self._mapPointList) < 1):
                return

            self._rubberBand.removePoint(-1)

            if (rubberBandSize > 1):
                if (moveRubberBandSize > 1):
                    point = self._rubberBand.getPoint(0, rubberBandSize - 2)
                    self._moveRubberBand.movePoint(moveRubberBandSize - 2, point)
            else:
                self._moveRubberBand.reset(self.geometryType())

            self._mapPointList.pop()
            self._validateGeometry()

    def resetCapturing(self):
        if (self._rubberBand is not None):
            self._rubberBand.reset(self.geometryType())
        if (self._moveRubberBand is not None):
            self._moveRubberBand.reset(self.geometryType())
        self._deleteGeometryValidation()
        del self._mapPointList[:]
        self.canvas().refresh()

    def _deleteGeometryValidation(self):
        if (self._validator is not None):
            self._validator.errorFound.disconnect(self._addGeometryError)
            self._validator.finished.disconnect(self.validationFinished)
            self._validator.deleteLater()
            self._validator = None
        for errorMarker in self._geometryErrorMarkers:
            self.canvas().scene().removeItem(errorMarker)
        del self._geometryErrorMarkers[:]
        self._geometryErrors[:]
        self._tip = ''

    def _validateGeometry(self):
        geometryType = self.geometryType()
        if (geometryType == Qgis.Point
                or geometryType == Qgis.UnknownGeometry
                or geometryType == Qgis.NoGeometry
                or len(self._mapPointList) < 2):
            return

        settings = QSettings()
        if (settings.value('/qgis/digitizing/validate_geometries', 1) == 0):
            return

        self._deleteGeometryValidation()

        geometry = None  # QgsGeometry()

        if (geometryType == Qgis.Line):
            geometry = QgsGeometry.fromPolyline(self._mapPointList)
        elif (geometryType == Qgis.Polygon):
            if (len(self._mapPointList) < 3):
                return
            closed = list(self._mapPointList)
            closed.append(self._mapPointList[0])
            geometry = QgsGeometry.fromPolygon([closed])

        if (geometry is None):
            return

        self._validator = QgsGeometryValidator(geometry)
        self._validator.errorFound.connect(self._addGeometryError)
        self._validator.finished.connect(self.validationFinished)
        self._validator.start()

        self._iface.mainWindow().statusBar().showMessage(self.tr('Geometry validation started.'))

    def _addGeometryError(self, error):
        self._geometryErrors.append(error)

        if (self._tip != ''):
            self._tip += '\n'
        self._tip += error.what()

        if (error.hasWhere()):
            marker = QgsVertexMarker(self.canvas())
            marker.setCenter(error.where())
            marker.setIconType(QgsVertexMarker.ICON_X)
            marker.setPenWidth(2)
            marker.setToolTip(error.what())
            marker.setColor(Qt.green)
            marker.setZValue(marker.zValue() + 1)
            self._geometryErrorMarkers.append(marker)

        self._iface.mainWindow().statusBar().showMessage(error.what())
        if (self._tip != ''):
            self._iface.mainWindow().statusBar().setToolTip(self._tip)

    def validationFinished(self):
        self._iface.mainWindow().statusBar().showMessage(self.tr('Geometry validation finished.'))
