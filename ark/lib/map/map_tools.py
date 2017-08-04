# -*- coding: utf-8 -*-
"""
/***************************************************************************
                                ARK QGIS
                        A QGIS utilities library.
        Part of the Archaeological Recording Kit by L-P : Archaeology
                        http://ark.lparchaeology.com
                              -------------------
        begin                : 2014-12-07
        git sha              : $Format:%H$
        copyright            : 2014, 2015 by L-P : Heritage LLP
        email                : ark@lparchaeology.com
        copyright            : 2014, 2015 by John Layt
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
from PyQt4.QtCore import Qt, pyqtSignal, QSettings, QSize, QRect, QVariant
from PyQt4.QtGui import QInputDialog, QColor, QAction, QPixmap, QCursor, QBitmap

from qgis.core import *
from qgis.gui import QgsMapTool, QgsRubberBand, QgsMapCanvasSnapper, QgsVertexMarker, QgsMessageBar, QgisInterface, QgsAttributeEditorContext, QgsAttributeDialog, QgsMapToolIdentify
import utils
from snapping import Snapping

# Code ported from QGIS app and adapted to take default attribute values
# Snapping code really should be in the public api classes

capture_point_cursor_xpm = [
  "16 16 3 1",
  " »     c None",
  ".»     c #000000",
  "+»     c #FFFFFF",
  "                ",
  "       +.+      ",
  "      ++.++     ",
  "     +.....+    ",
  "    +.     .+   ",
  "   +.   .   .+  ",
  "  +.    .    .+ ",
  " ++.    .    .++",
  " ... ...+... ...",
  " ++.    .    .++",
  "  +.    .    .+ ",
  "   +.   .   .+  ",
  "   ++.     .+   ",
  "    ++.....+    ",
  "      ++.++     ",
  "       +.+      "
]
capture_point_cursor = QCursor(QPixmap(capture_point_cursor_xpm), 8, 8)


class FeatureType():

    NoFeature = 0
    Point = 1
    Elevation = 2
    Segment = 3
    Line = 4
    Polygon = 5


class ArkMapToolIndentifyFeatures(QgsMapToolIdentify):

    featureIdentified = pyqtSignal(QgsFeature)

    def __init__(self, canvas):
        super(ArkMapToolIndentifyFeatures, self).__init__(canvas)
        mToolName = self.tr('Identify feature')

    def canvasReleaseEvent(self, e):
        if e.button() != Qt.LeftButton:
            return
        results = self.identify(e.x(), e.y(), QgsMapToolIdentify.LayerSelection, QgsMapToolIdentify.VectorLayer)
        if (len(results) < 1):
            return
        # TODO: display a menu when several features identified
        self.featureIdentified.emit(results[0].mFeature)

    def keyPressEvent(self, e):
        if (e.key() == Qt.Key_Escape):
            self.canvas().unsetMapTool(self)


# Tool to interact with map, including panning, zooming, and snapping
class ArkMapToolInteractive(QgsMapTool):

    _active = False

    _dragging = False
    _panningEnabled = False

    _zoomingEnabled = False
    _zoomRubberBand = None  #QgsRubberBand()
    _zoomRect = None # QRect()

    _snappingEnabled = False
    _snapper = None  #QgsMapCanvasSnapper()
    _snappingMarker = None  # QgsVertexMarker()

    _showSnappableVertices = False
    _snappableVertices = []  # [QgsPoint()]
    _snappableMarkers = []  # [QgsVertexMarker()]

    def __init__(self, canvas, snappingEnabled=False, showSnappableVertices=False):
        super(ArkMapToolInteractive, self).__init__(canvas)
        self._snappingEnabled = snappingEnabled
        self._showSnappableVertices = showSnappableVertices

    def __del__(self):
        if self._active:
            self.deactivate()

    def isActive(self):
        return self._active

    def activate(self):
        super(ArkMapToolInteractive, self).activate()
        self._active = True
        self._startSnapping()

    def deactivate(self):
        self._active = False
        if self._snappingEnabled:
            self._stopSnapping()
        if (self._zoomRubberBand is not None):
            self.canvas().scene().removeItem(self._zoomRubberBand)
            self._zoomRubberBand = None
        super(ArkMapToolInteractive, self).deactivate()

    def setAction(self, action):
        super(ArkMapToolInteractive, self).setAction(action)
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
        super(ArkMapToolInteractive, self).canvasMoveEvent(e)
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
            mapPoint, snapped = self._snapCursorPoint(e.pos())
            if (snapped):
                self._createSnappingMarker(mapPoint)
            else:
                self._deleteSnappingMarker()

    def canvasReleaseEvent(self, e):
        super(ArkMapToolInteractive, self).canvasReleaseEvent(e)
        e.ignore()
        if (e.button() == Qt.LeftButton):
            if self._dragging:
                # Pan map mode
                self.canvas().panActionEnd(e.pos())
                self.setCursor(capture_point_cursor)
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
        super(ArkMapToolInteractive, self).keyPressEvent(e)
        if (e.key() == Qt.Key_Escape):
            self.canvas().unsetMapTool(self)
            e.accept()

    def _snapCursorPoint(self, cursorPoint):
        res, snapResults = self._snapper.snapToBackgroundLayers(cursorPoint)
        if (res != 0 or len(snapResults) < 1):
            return self.toMapCoordinates(cursorPoint), False
        else:
            # Take a copy as QGIS will delete the result!
            snappedVertex = QgsPoint(snapResults[0].snappedVertex)
            return snappedVertex, True

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
        if (not self._showSnappableVertices or not self._snappingEnabled):
            return
        extent = self.canvas().extent()
        for vertex in self._snappableVertices.asMultiPoint():
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
                        vertices.extend([geometry.asPoint()])
                    elif geometry.type() == QGis.Line:
                        vertices.extend(geometry.asPolyline())
                    elif geometry.type() == QGis.Polygon:
                        lines = geometry.asPolygon()
                        for line in lines:
                            vertices.extend(line)
        self._snappableVertices = QgsGeometry.fromMultiPoint(vertices)
        self._snappableVertices.simplify(0)


# Tool to emit mouse clicks as map points
class ArkMapToolEmitPoint(ArkMapToolInteractive):

    canvasClicked = pyqtSignal(QgsPoint, Qt.MouseButton)

    _vertexMarker = None  # QgsVertexMarker

    def __init__(self, canvas):
        super(ArkMapToolEmitPoint, self).__init__(canvas)
        self._vertexMarker = QgsVertexMarker(canvas)
        self._vertexMarker.setIconType(QgsVertexMarker.ICON_NONE)

    def deactivate(self):
        self._vertexMarker.setCenter(QgsPoint())
        super(ArkMapToolEmitPoint, self).deactivate()

    def canvasReleaseEvent(self, e):
        super(ArkMapToolEmitPoint, self).canvasReleaseEvent(e)
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


# Tool to capture and show mouse clicks as geometry using map points
class ArkMapToolCapture(ArkMapToolInteractive):

    canvasClicked = pyqtSignal(QgsPoint, Qt.MouseButton)

    _iface = None
    _useCurrentLayerGeometry = False
    _geometryType = QGis.NoGeometry
    _mapPointList = []  #QList<QgsPoint>
    _rubberBand = None  #QgsRubberBand()
    _moveRubberBand = None  #QgsRubberBand()
    _tip = ''
    _validator = None  #QgsGeometryValidator()
    _geometryErrors = []  #QList<QgsGeometry.Error>
    _geometryErrorMarkers = []  #QList<QgsVertexMarker>

    def __init__(self, iface, geometryType=QGis.UnknownGeometry):
        super(ArkMapToolCapture, self).__init__(iface.mapCanvas())
        self._iface = iface
        self._geometryType = geometryType
        if (geometryType == QGis.UnknownGeometry):
            self._useCurrentLayerGeometry = True
        self.setCursor(capture_point_cursor)

    def __del__(self):
        self.deactivate();
        super(ArkMapToolCapture, self).__del__()

    def activate(self):
        super(ArkMapToolCapture, self).activate()
        geometryType = self.geometryType()
        self._rubberBand = self._createRubberBand(geometryType)
        self._moveRubberBand = self._createRubberBand(geometryType, True)
        if (self._useCurrentLayerGeometry == True):
            self._iface.currentLayerChanged.connect(self._currentLayerChanged)

    def deactivate(self):
        self.resetCapturing()
        if (self._rubberBand is not None):
            self.canvas().scene().removeItem(self._rubberBand)
            self._rubberBand = None
        if (self._moveRubberBand is not None):
            self.canvas().scene().removeItem(self._moveRubberBand)
            self._moveRubberBand = None
        if (self._useCurrentLayerGeometry == True):
            self._iface.currentLayerChanged.disconnect(self._currentLayerChanged)
        super(ArkMapToolCapture, self).deactivate()

    def geometryType(self):
        if (self._useCurrentLayerGeometry and self.canvas().currentLayer().type() == QgsMapLayer.VectorLayer):
            return self.canvas().currentLayer().geometryType()
        else:
            return self._geometryType

    def _currentLayerChanged(self, layer):
        if (not self._useCurrentLayerGeometry):
            return
        #TODO Update rubber bands
        if (self._rubberBand is not None):
            self._rubberBand.reset(self.geometryType())
            for point in self._mapPointList[:-1]:
                self._rubberBand.addPoint(point, False)
        self._updateMoveRubberBand(self._mapPointList[-1])
        self._validateGeometry()
        self.canvas().refresh()

    def canvasMoveEvent(self, e):
        super(ArkMapToolCapture, self).canvasMoveEvent(e)
        if e.isAccepted():
            return
        if (self._moveRubberBand is not None):
            # Capture mode
            mapPoint, snapped = self._snapCursorPoint(e.pos())
            self._moveRubberBand.movePoint(mapPoint)

    def canvasReleaseEvent(self, e):
        super(ArkMapToolCapture, self).canvasReleaseEvent(e)
        if e.isAccepted():
            return
        mapPoint, snapped = self._snapCursorPoint(e.pos())
        if (e.button() == Qt.LeftButton):
            # Capture mode
            self._addVertex(mapPoint)
        # Emit mode
        self.canvasClicked.emit(mapPoint, e.button())

    def keyPressEvent(self, e):
        if (e.key() == Qt.Key_Escape):
            self.resetCapturing()
            e.accept()
        elif (e.key() == Qt.Key_Backspace or e.key() == Qt.Key_Delete):
            self._undo()
            e.accept()
        else:
            super(ArkMapToolCapture, self).keyPressEvent(e)

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
        if (geometryType == QGis.Polygon):
            color.setAlphaF(myAlpha)
        color.setAlphaF(myAlpha)
        rb.setColor(color)
        rb.show()
        return rb

    def _addVertex(self, mapPoint):
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
        if (geometryType == QGis.Polygon):
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
        self._tip = '';

    def _validateGeometry(self):
        geometryType = self.geometryType()
        if (geometryType == QGis.Point or geometryType == QGis.UnknownGeometry or geometryType == QGis.NoGeometry or len(self._mapPointList) < 2):
            return

        settings = QSettings()
        if (settings.value('/qgis/digitizing/validate_geometries', 1 ) == 0):
            return

        self._deleteGeometryValidation()

        geometry = None #QgsGeometry()

        if (geometryType == QGis.Line):
            geometry = QgsGeometry.fromPolyline(self._mapPointList)
        elif (geometryType == QGis.Polygon):
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


class ArkMapToolAddFeature(ArkMapToolCapture):

    _layer = None  # QgsVectorLayer()
    _featureType = 0  # NoFeature
    _defaultAttributes = {}  # key = fieldName, value = fieldValue

    #TODO Eventually merge this with the input action?
    _queryAttributeName = None
    _queryType = None
    _queryAttributeDefault = None
    _queryTitle = ''
    _queryLabel = ''
    _queryDecimals = 0
    _queryMin = 0
    _queryMax = 0

    def __init__(self, iface, layer, featureType=0, toolName=''):
        geometryType = QGis.UnknownGeometry
        if (layer is not None and layer.isValid()):
            geometryType = layer.geometryType()
        super(ArkMapToolAddFeature, self).__init__(iface, geometryType)
        self._layer = layer

        if (featureType == FeatureType.NoFeature):
            if (geometryType == QGis.Point):
                self._featureType = FeatureType.Point
            elif (geometryType == QGis.Line):
                self._featureType = FeatureType.Line
            elif (geometryType == QGis.Polygon):
                self._featureType = FeatureType.Polygon
            else:
                self._featureType = FeatureType.NoFeature
        else:
            self._featureType = featureType

        if (toolName):
            self.mToolName = toolName
        else:
            self.mToolName = self.tr('Add feature')

    def layer(self):
        return self._layer

    def isEditTool(self):
        return True

    def setDefaultAttributes(self, defaultAttributes):
        self._defaultAttributes = defaultAttributes

    #TODO Eventually merge this with the input action?
    def setAttributeQuery(self, attributeName, attributeType, attributeDefault, title, label, min=0, max=0, decimals=0):
            self._queryAttributeName = attributeName
            self._queryType = attributeType
            self._queryAttributeDefault = attributeDefault
            self._queryTitle = title
            self._queryLabel = label
            self._queryMin = min
            self._queryMax = max
            self._queryDecimals = decimals

    def activate(self):
        super(ArkMapToolAddFeature, self).activate()
        if self._layer is not None:
            self.canvas().setCurrentLayer(self._layer)
            self._iface.legendInterface().setCurrentLayer(self._layer)
            if self._layer.geometryType() == QGis.NoGeometry:
                self._addFeatureAction(QgsFeature(), False)

    def canvasReleaseEvent(self, e):
        super(ArkMapToolAddFeature, self).canvasReleaseEvent(e)
        if (e.isAccepted()):
            return
        if (self._featureType == FeatureType.Point or self._featureType == FeatureType.Elevation):
            if (e.button() == Qt.LeftButton):
                self.addFeature()
                e.accept()
        else:
            if (e.button() == Qt.LeftButton):
                if (self._featureType == FeatureType.Segment and len(self._mapPointList) == 2):
                    self.addFeature()
            elif (e.button() == Qt.RightButton):
                self.addFeature()
                e.accept()

    def addFeature(self):
        if self._queryForAttribute():
            self.addAnyFeature(self._featureType, self._mapPointList, self._defaultAttributes, self._layer)
        self.resetCapturing()

    def addAnyFeature(self, featureType, mapPointList, attributes, layer):
        #points: bail out if there is not exactly one vertex
        if ((featureType == FeatureType.Point or featureType == FeatureType.Elevation) and len(mapPointList) != 1):
            return False

        #segments: bail out if there are not exactly two vertices
        if (featureType == FeatureType.Segment and len(mapPointList) != 2):
            return False

        #lines: bail out if there are not at least two vertices
        if (featureType == FeatureType.Line and len(mapPointList) < 2):
            return False

        #polygons: bail out if there are not at least three vertices
        if (featureType == FeatureType.Polygon and len(mapPointList) < 3):
            return False

        if (layer.type() != QgsMapLayer.VectorLayer):
            self.messageEmitted.emit(self.tr('Cannot add feature: Current layer not a vector layer'), QgsMessageBar.CRITICAL)
            return False

        if (not layer.isEditable()):
            self.messageEmitted.emit(self.tr('Cannot add feature: Current layer not editable'), QgsMessageBar.CRITICAL)
            return False

        provider = layer.dataProvider()
        if (not (provider.capabilities() & QgsVectorDataProvider.AddFeatures)):
            self.messageEmitted.emit(self.tr('Cannot add feature: The data provider for this layer does not support the addition of features.'), QgsMessageBar.CRITICAL)
            return False

        layerWKBType = layer.wkbType()
        layerPoints = self._layerPoints(mapPointList, layer)
        feature = QgsFeature(layer.pendingFields(), 0)
        geometry = None

        if (layerWKBType == QGis.WKBPoint or layerWKBType == QGis.WKBPoint25D):
            geometry = QgsGeometry.fromPoint(layerPoints[0])
        elif (layerWKBType == QGis.WKBMultiPoint or layerWKBType == QGis.WKBMultiPoint25D):
            geometry = QgsGeometry.fromMultiPoint([layerPoints[0]])
        elif (layerWKBType == QGis.WKBLineString or layerWKBType == QGis.WKBLineString25D):
            geometry = QgsGeometry.fromPolyline(layerPoints)
        elif (layerWKBType == QGis.WKBMultiLineString or layerWKBType == QGis.WKBMultiLineString25D):
            geometry = QgsGeometry.fromMultiPolyline([layerPoints])
        elif (layerWKBType == QGis.WKBPolygon or  layerWKBType == QGis.WKBPolygon25D):
            geometry = QgsGeometry.fromPolygon([layerPoints])
        elif (layerWKBType == QGis.WKBMultiPolygon or  layerWKBType == QGis.WKBMultiPolygon25D):
            geometry = QgsGeometry.fromMultiPolygon([layerPoints])
        else:
            self.messageEmitted.emit(self.tr('Cannot add feature. Unknown WKB type'), QgsMessageBar.CRITICAL)
            return False

        if (geometry is None):
            self.messageEmitted.emit(self.tr('Cannot add feature. Invalid geometry'), QgsMessageBar.CRITICAL)
            return False
        feature.setGeometry(geometry)

        if (featureType == FeatureType.Polygon):

            avoidIntersectionsReturn = feature.geometry().avoidIntersections()
            if (avoidIntersectionsReturn == 1):
                #not a polygon type. Impossible to get there
                pass
            elif (avoidIntersectionsReturn == 3):
                self.messageEmitted.emit(self.tr('An error was reported during intersection removal'), QgsMessageBar.CRITICAL)

            if (not feature.geometry().asWkb()): #avoid intersection might have removed the whole geometry
                reason = ''
                if (avoidIntersectionsReturn != 2):
                    reason = self.tr('The feature cannot be added because it\'s geometry is empty')
                else:
                    reason = self.tr('The feature cannot be added because it\'s geometry collapsed due to intersection avoidance')
                self.messageEmitted.emit(reason, QgsMessageBar.CRITICAL)
                return False

        featureSaved = self._addFeatureAction(feature, attributes, layer, False)

        if (featureSaved and featureType != FeatureType.Point and featureType != FeatureType.Elevation):
            #add points to other features to keep topology up-to-date
            topologicalEditing = Snapping.topologicalEditing()

            #use always topological editing for avoidIntersection.
            #Otherwise, no way to guarantee the geometries don't have a small gap in between.
            intersectionLayers = Snapping.intersectionLayers()
            avoidIntersection = len(intersectionLayers)
            if (avoidIntersection): #try to add topological points also to background layers
                for intersectionLayer in intersectionLayers:
                    vl = QgsMapLayerRegistry.instance().mapLayer(str(intersectionLayer))
                    #can only add topological points if background layer is editable...
                    if (vl is not None and vl.geometryType() == QGis.Polygon and vl.isEditable()):
                        vl.addTopologicalPoints(feature.geometry())
            elif (topologicalEditing):
                self._layer.addTopologicalPoints(feature.geometry())

        self.canvas().refresh()

        return True

    def _queryForAttribute(self):
        #TODO Eventually merge this with the input action?
        value = None
        ok = True
        if self._queryAttributeName:
            value, ok = self._getValue(self._queryTitle, self._queryLabel, self._queryType, self._queryAttributeDefault, self._queryMin, self._queryMax, self._queryDecimals)
            if ok:
                self._defaultAttributes[self._queryAttributeName] = value
        return ok

    def _getValue(self, title, label, valueType=QVariant.String, defaultValue='', minValue=0, maxValue=0, decimals=0):
        if valueType == QVariant.Double:
            return QInputDialog.getDouble(None, title, label, defaultValue, minValue, maxValue, decimals)
        elif valueType == QVariant.Int:
            return QInputDialog.getInt(None, title, label, defaultValue, minValue, maxValue)
        else:
            return QInputDialog.getText(None, title, label, text=defaultValue)

    def _addFeatureAction(self, feature, attributes, layer, showModal=True):
        action = ArkFeatureAction(self.tr('add feature'), feature, layer, -1, -1, self._iface, self)
        res = action.addFeature(attributes, showModal)
        if (showModal):
            action = None
        return res

    def _layerPoints(self, mapPointList, layer):
        layerPoints = []
        if layer is None:
            return layerPoints
        for mapPoint in mapPointList:
            layerPoints.append(self.toLayerCoordinates(layer, mapPoint))
        return layerPoints


# Tool to take a line segment and then save as a buffer polygon
class ArkMapToolAddBufferSegment(ArkMapToolAddFeature):

    _bufferDistance = 0.1  # Map Units

    def __init__(self, iface, distance,  polygonLayer, toolName=''):
        super(ArkMapToolSectionSchematic, self).__init__(iface, polygonLayer, FeatureType.Segment, toolName)
        self.setBuffer(distance)

    def setBuffer(self, distance):
        self._bufferDistance = 0.1  # Map Units

    def addAnyFeature(self, featureType, mapPointList, attributes, layer):
        if featureType == FeatureType.Segment:
            if len(mapPointList) != 2:
                return False
            lineGeom = QgsGeometry.fromPolyline(mapPointList)
            polyGeom = lineGeom.buffer(self._bufferDistance, 0, 2, 2, 5.0)
            if polyGeom and polyGeom.isGeosValid():
                mapPointList = polyGeom.asPolygon()[0]
            else:
                mapPointList = []
            featureType = FeatureType.Polygon
        super(ArkMapToolSectionSchematic, self).addAnyFeature(featureType, mapPointList, attributes, layer)


# TODO Clean up this and fix dialog problems
class ArkFeatureAction(QAction):

    _layer = QgsVectorLayer()
    _feature = QgsFeature()
    _action = -1
    _idx = -1
    _featureSaved = False
    _lastUsedValues = {}
    _iface = None

    def __init__(self, name, feature, layer, action=-1, defaultAttr=-1, iface=None, parent=None):
        super(ArkFeatureAction, self).__init__(name, parent)
        self._layer = layer
        self._feature = feature
        self._action = action
        self._idx = defaultAttr
        self._iface = iface

    def execute(self):
        self._layer.actions().doAction(self._action, self._feature, self._idx)

    def _newDialog(self, cloneFeature):
        feature = QgsFeature()
        if (cloneFeature):
            feature = QgsFeature(self._feature)
        else:
            feature = self._feature

        context = QgsAttributeEditorContext()

        myDa = QgsDistanceArea()

        myDa.setSourceCrs(self._layer.crs())
        myDa.setEllipsoidalMode(self._iface.mapCanvas().mapSettings().hasCrsTransformEnabled())
        myDa.setEllipsoid(QgsProject.instance().readEntry('Measure', '/Ellipsoid', GEO_NONE)[0])

        context.setDistanceArea(myDa)
        context.setVectorLayerTools(self._iface.vectorLayerTools())

        dialog = QgsAttributeDialog(self._layer, feature, cloneFeature, None, True, context)

        if (self._layer.actions().size() > 0):
            dialog.setContextMenuPolicy(Qt.ActionsContextMenu)

            a = QAction(self.tr('Run actions'), dialog)
            a.setEnabled(False)
            dialog.addAction(a)

            i = 0
            for action in self._layer.actions():
                if (action.runable()):
                    a = ArkFeatureAction(action.name(), feature, self._layer, i, -1, self._iface, dialog)
                    dialog.addAction(a)
                    a.triggered.connect(a.execute)
                    pb = dialog.findChild(action.name())
                    if (pb):
                        pb.clicked.connect(a.execute)
                i += 1

        return dialog

    def viewFeatureForm(self, h=0):
        if (not self._layer):
            return False
        dialog = self._newDialog(True)
        dialog.setHighlight(h)
        dialog.show()
        return True

    def editFeature(self, showModal=True):
        if (not self._layer):
            return False

        dialog = self._newDialog(False)

        if (not self._feature.isValid()):
            dialog.setIsAddDialog(True)

        if (showModal):
            dialog.setAttribute(Qt.WA_DeleteOnClose)
            rv = dialog.exec_()
            self._feature.setAttributes(dialog.feature().attributes())
            return rv
        else:
            dialog.show()
        return True

    def addFeature(self, defaultAttributes={}, showModal=True):
        if (self._layer is None or not self._layer.isEditable()):
            return False

        provider = self._layer.dataProvider()

        settings = QSettings()
        reuseLastValues = settings.value('/qgis/digitizing/reuseLastValues', False)

        fields = self._layer.pendingFields()
        self._feature.initAttributes(fields.count())
        for idx in range(0, fields.count()):
            v = None
            field = fields[idx]

            if (defaultAttributes.has_key(field.name())):
                v = defaultAttributes[field.name()]
            elif (reuseLastValues and self._lastUsedValues.has_key(self._layer.id()) and self._lastUsedValues[self._layer.id()].has_key(idx)):
                v = self._lastUsedValues[self._layer.id()][idx]
            else:
                v = provider.defaultValue(idx)

            self._feature.setAttribute(idx, v)

        isDisabledAttributeValuesDlg = settings.value('/qgis/digitizing/disable_enter_attribute_values_dialog', False)
        if (fields.count() == 0 or self._layer.featureFormSuppress() == QgsVectorLayer.SuppressOn):
            isDisabledAttributeValuesDlg = True
        elif (self._layer.featureFormSuppress() == QgsVectorLayer.SuppressOff):
            isDisabledAttributeValuesDlg = False

        if (isDisabledAttributeValuesDlg):
            self._layer.beginEditCommand(self.text())
            self._featureSaved = self._layer.addFeature(self._feature)
            if (self._featureSaved):
                self._layer.endEditCommand()
            else:
                self._layer.destroyEditCommand()
        else:
            dialog = self._newDialog(False)
            dialog.setIsAddDialog(True)
            dialog.setEditCommandMessage(self.text())

            attributeForm = dialog.attributeForm()
            attributeForm.featureSaved.connect(self._onFeatureSaved)

            if (not showModal):
                self.setParent(dialog)
                dialog.show()
                return True

            dialog.setAttribute(Qt.WA_DeleteOnClose)
            dialog.exec_()

        return self._featureSaved;

    def _onFeatureSaved(self, feature):
        self._featureSaved = True

        reuseLastValues = QSettings().value('/qgis/digitizing/reuseLastValues', False)

        if (reuseLastValues):
            fields = self._layer.pendingFields()
            for idx in range(0, fields.count() - 1):
                newValues = feature.attributes()
                origValues = self._lastUsedValues[self._layer.id()]
                if (origValues[idx] != newValues[idx]):
                    self._lastUsedValues[self._layer.id()][idx] = newValues[idx]
