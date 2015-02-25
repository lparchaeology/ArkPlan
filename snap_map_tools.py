# -*- coding: utf-8 -*-
"""
/***************************************************************************
 ArkPlan
                                 A QGIS plugin
 Plugin to assist in digitising of Archaeological plans.
                              -------------------
        begin                : 2015-02-23
        git sha              : $Format:%H$
        copyright            : (C) 2015 by John Layt
        copyright            : (C) 2015 by L - P: Heritage LLP
        copyright            : (C) 2010 by Jürgen E. Fischer
        copyright            : (C) 2007 by Marco Hugentobler
        copyright            : (C) 2006 by Martin Dobias
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
from PyQt4.QtCore import Qt, pyqtSignal, QSettings
from PyQt4.QtGui import QInputDialog, QColor, QAction, QPixmap, QCursor

from qgis.core import *
from qgis.gui import QgsMapTool, QgsRubberBand, QgsMapCanvasSnapper, QgsVertexMarker, QgsMessageBar, QgisInterface, QgsAttributeEditorContext, QgsAttributeDialog

# Code ported from QGIS app and adapted to take default attribute values
# Snapping code really should be in the public api classes

capture_point_cursor = [
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


class QgsFeatureAction(QAction):

    _layer = QgsVectorLayer()
    _feature = QgsFeature()
    _action = -1
    _idx = -1
    _featureSaved = False
    _lastUsedValues = {}
    _iface = None

    def __init__(self, name, feature, layer, action=-1, defaultAttr=-1, iface=None, parent=None):
        super(QgsFeatureAction, self).__init__(name, parent)
        self._layer = layer
        self._feature = feature
        self._action = action
        self._idx = defaultAttr
        self._iface = iface

    def execute(self):
        self._layer.actions().doAction(self._action, self._feature, self._idx)

    def _newDialog(self, cloneFeature):
        f = QgsFeature()
        if (cloneFeature):
            f = QgsFeature(self._feature)
        else:
            f = self._feature

        context = QgsAttributeEditorContext()

        myDa = QgsDistanceArea()

        myDa.setSourceCrs(self._layer.crs())
        myDa.setEllipsoidalMode(self._iface.mapCanvas().hasCrsTransformEnabled())
        myDa.setEllipsoid(QgsProject.instance().readEntry('Measure', '/Ellipsoid', GEO_NONE)[0])

        context.setDistanceArea(myDa)
        context.setVectorLayerTools(self._iface.vectorLayerTools())

        dialog = QgsAttributeDialog(self._layer, f, cloneFeature, None, True, context)

        if (self._layer.actions().size() > 0):
            dialog.setContextMenuPolicy(Qt.ActionsContextMenu)

            a = QAction(self.tr('Run actions'), dialog)
            a.setEnabled(False)
            dialog.addAction(a)

            i = 0
            for action in self._layer.actions():
                if (action.runable()):
                    a = QgsFeatureAction(action.name(), f, self._layer, i, -1, self._iface, dialog)
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
        #QgsDebugMsg('reuseLastValues: %1' % reuseLastValues)

        fields = self._layer.pendingFields()
        self._feature.initAttributes(fields.count())
        for idx in range(0, fields.count() - 1):
            v = ''

            if (defaultAttributes.has_key(idx)):
                v = defaultAttributes[idx]
            elif (reuseLastValues and self._lastUsedValues.has_key(self._layer) and self._lastUsedValues[self._layer].has_key(idx)):
                v = self._lastUsedValues[self._layer][idx]
            else:
                v = provider.defaultValue(idx)

            self._feature.setAttribute(idx, v)

        isDisabledAttributeValuesDlg = settings.value('/qgis/digitizing/disable_enter_attribute_values_dialog', False)
        if (self._layer.featureFormSuppress() == QgsVectorLayer.SuppressOn):
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
        form = self.sender()
        self._featureSaved = True

        settings = QSettings()
        reuseLastValues = settings.value('/qgis/digitizing/reuseLastValues', False)
        #QgsDebugMsg('reuseLastValues: %1' % reuseLastValues)

        if (reuseLastValues):
            fields = self._layer.pendingFields()
            for idx in range(0, fields.count() - 1):
                newValues = feature.attributes()
                origValues = self._lastUsedValues[self._layer]
                if (origValues[idx] != newValues[idx]):
                    #QgsDebugMsg('saving %s for %s' % (str(self._lastUsedValues[self._layer][idx]), str(idx)))
                    self._lastUsedValues[self._layer][idx] = newValues[idx]

# Tool to show snapping points
class QgsMapToolSnap(QgsMapTool):

    _snapper = QgsMapCanvasSnapper()
    _snappingMarker = None  # QgsVertexMarker()

    def __init__(self, canvas):
        super(QgsMapToolSnap, self).__init__(canvas)
        self._snapper.setMapCanvas(canvas)

    def __del__(self):
        self._deleteSnappingMarker()

    def deactivate(self):
        self._deleteSnappingMarker()
        super(QgsMapToolSnap, self).deactivate()

    def canvasMoveEvent(self, e):
        mapPoint, snapped = self._snapCursorPoint(e.pos())
        if (snapped):
            self._createSnappingMarker(mapPoint)
        else:
            self._deleteSnappingMarker()
        self.canvas().refresh()

    def _snapCursorPoint(self, cursorPoint):
        res, snapResults = self._snapper.snapToBackgroundLayers(cursorPoint)
        if (res != 0 or len(snapResults) < 1):
            return self.toMapCoordinates(cursorPoint), False
        else:
            return snapResults[0].snappedVertex, True

    def _snapMapPoint(self, mapPoint):
        res, snapResults = self._snapper.snapToBackgroundLayers(mapPoint)
        if (res != 0 or len(snapResults) < 1):
            return mapPoint, False
        else:
            return snapResults[0].snappedVertex, True

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

# Tool to capture and show mouse clicks as geometry using map points
class QgsMapToolCapture(QgsMapToolSnap):

    _iface = None
    _capturing = False
    _useLayerGeometry = True
    _geometryType = QGis.NoGeometry
    _mapPointList = []  #QList<QgsPoint>
    _rubberBand = None  #QgsRubberBand()
    _moveRubberBand = None  #QgsRubberBand()
    _tip = ''
    _validator = None  #QgsGeometryValidator()
    _geometryErrors = []  #QList<QgsGeometry.Error>
    _geometryErrorMarkers = []  #QList<QgsVertexMarker>

    def __init__(self, canvas, iface, geometryType=QGis.UnknownGeometry):
        super(QgsMapToolCapture, self).__init__(canvas)
        self._iface = iface
        self._geometryType = geometryType
        if (geometryType == QGis.UnknownGeometry):
            self._useLayerGeometry = True
            self._geometryType = self._geometryType()
            self._iface.currentLayerChanged.connect(self._currentLayerChanged)
        self.setCursor(QCursor(QPixmap(capture_point_cursor), 8, 8))

    def __del__(self):
        self._stopCapturing();
        if (self._validator is not None):
            self._validator.deleteLater()
        super(QgsMapToolCapture, self).__del__()

    def isEditTool(self):
        return True

    def geometryType(self):
        if (self._useLayerGeometry and self._isVectorLayer()):
            return self.canvas().currentLayer().geometryType()
        else:
            return self._geometryType

    def _currentLayerChanged(self, layer):
        if (not self._useLayerGeometry):
            return
        #TODO Update rubber bands

    def canvasMoveEvent(self, e):
        super(QgsMapToolCapture, self).canvasMoveEvent(e)
        if (self._moveRubberBand is not None):
            mapPoint, snapped = self._snapCursorPoint(e.pos())
            self._moveRubberBand.movePoint(mapPoint)

    def canvasPressEvent(self, e):
        pass

    def keyPressEvent(self, e):
        if (e.key() == Qt.Key_Backspace or e.key() == Qt.Key_Delete):
            self._undo()
            e.ignore()

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

    def _mapPoints(self):
        return self._mapPointList

    def _addVertex(self, pos):
        geometryType = self.geometryType()
        if (geometryType == QGis.NoGeometry or geometryType == QGis.UnknownGeometry):
            self.messageEmitted.emit(self.tr('Cannot capture point, unknown geometry'), QgsMessageBar.CRITICAL)
            return 2

        mapPoint, snapped = self._snapCursorPoint(pos)
        self._mapPointList.append(mapPoint)

        if (geometryType == QGis.Point):
            return 0

        self._rubberBand.addPoint(mapPoint)

        self._moveRubberBand.reset(geometryType)
        if (geometryType == QGis.Polygon):
            firstPoint = self._rubberBand.getPoint(0, 0)
            self._moveRubberBand.addPoint(firstPoint)
            self._moveRubberBand.movePoint(mapPoint)
        self._moveRubberBand.addPoint(mapPoint)

        self._validateGeometry()
        return 0

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

    def _startCapturing(self):
        if (self._capturing):
            return
        geometryType = self.geometryType()
        self._capturing = True
        if (geometryType == QGis.Line or geometryType == QGis.Polygon):
            self._rubberBand = self._createRubberBand(geometryType)
            self._moveRubberBand = self._createRubberBand(geometryType, True)

    def _isCapturing(self):
        return self._capturing

    def _stopCapturing(self):
        self._capturing = False
        self._deleteRubberBand()
        self._deleteMoveRubberBand()
        self._deleteErrorMarkers()
        self._geometryErrors = []
        self._mapPointList = []
        self.canvas().refresh()

    def _deleteErrorMarkers(self):
        for errorMarker in self._geometryErrorMarkers:
            self.canvas().scene().removeItem(errorMarker)
        self._geometryErrorMarkers = []

    def _deleteRubberBand(self):
        if (self._rubberBand is not None):
            self.canvas().scene().removeItem(self._rubberBand)
            self._rubberBand = None

    def _deleteMoveRubberBand(self):
        if (self._moveRubberBand is not None):
            self.canvas().scene().removeItem(self._moveRubberBand)
            self._moveRubberBand = None

    def _validateGeometry(self):
        geometryType = self._geometryType
        if (geometryType == QGis.Point or geometryType == QGis.UnknownGeometry or geometryType == QGis.NoGeometry or len(self._mapPointList) < 2):
            return

        settings = QSettings()
        if (settings.value('/qgis/digitizing/validate_geometries', 1 ) == 0):
            return

        if (self._validator is not None):
            self._validator.deleteLater()
            self._validator = None

        self._tip = '';
        self._geometryErrors = []
        self._deleteErrorMarkers()

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

        sb = self._iface.mainWindow().statusBar()
        sb.showMessage(self.tr('Validation started.'))

    def _addGeometryError(self, error):
        self._geometryErrors.append(error)

        if (self._tip != ''):
            self._tip += '\n'
        self._tip += error.what()

        if (error.hasWhere()):
            vm = QgsVertexMarker(self.canvas())
            vm.setCenter(error.where())
            vm.setIconType(QgsVertexMarker.ICON_X)
            vm.setPenWidth(2)
            vm.setToolTip(error.what())
            vm.setColor(Qt.green)
            vm.setZValue(vm.zValue() + 1)
            self._geometryErrorMarkers.append(vm)

        sb = self._iface.mainWindow().statusBar()
        sb.showMessage(error.what())
        if (self._tip != ''):
            sb.setToolTip(self._tip)

    def validationFinished(self):
        sb = self._iface.mainWindow().statusBar()
        sb.showMessage(self.tr('Validation finished.'))

    def _isVectorLayer(self):
        return (self.canvas().currentLayer().type() == QgsMapLayer.VectorLayer)


class QgsMapToolAddFeature(QgsMapToolCapture):

    NoFeature = 0
    Point = 1
    Segment = 2
    Line = 3
    Polygon = 4

    _featureType = 0  # NoFeature
    _defaultAttributes = {}  # QMap<int, QList<QVariant> >

    def __init__(self, canvas, iface, featureType=0):
        geometryType = QGis.UnknownGeometry
        toolName = 'Add feature'
        if (featureType == QgsMapToolAddFeature.Point):
            geometryType = QGis.Point
            toolName = 'Add point feature'
        elif (featureType == QgsMapToolAddFeature.Segment or featureType == QgsMapToolAddFeature.Line):
            geometryType = QGis.Line
            toolName = 'Add line feature'
        elif (featureType == QgsMapToolAddFeature.Polygon):
            geometryType = QGis.Polygon
            toolName = 'Add polygon feature'
        super(QgsMapToolAddFeature, self).__init__(canvas, iface, geometryType)
        self.mToolName = self.tr(toolName)
        self._featureType = featureType

    def setDefaultAttributes(self, defaultAttributes):
        self._defaultAttributes = defaultAttributes

    def addFeature(self, vlayer, feature, showModal=True):
        action = QgsFeatureAction(self.tr('add feature'), feature, vlayer, -1, -1, self._iface, self)
        res = action.addFeature(self._defaultAttributes, showModal)
        if (showModal):
            action = None
        return res

    def activate(self):
        vlayer = self._currentVectorLayer()
        if (vlayer is not None and vlayer.geometryType() == QGis.NoGeometry):
            self.addFeature(vlayer, QgsFeature(), False)
            return
        super(QgsMapToolAddFeature, self).activate()

    def canvasReleaseEvent(self, e):
        if (not self._isVectorLayer()):
            self._notifyNotVectorLayer()
            return

        vlayer = self._currentVectorLayer()
        layerWKBType = vlayer.wkbType()
        provider = vlayer.dataProvider()

        if (not (provider.capabilities() & QgsVectorDataProvider.AddFeatures)):
            self.messageEmitted.emit(self.tr('The data provider for this layer does not support the addition of features.'), QgsMessageBar.WARNING)
            return

        if (vlayer.geometryType() != self.geometryType()):
            self.messageEmitted.emit(self.tr('The geometry type of this layer is different than the capture tool.'), QgsMessageBar.WARNING)
            return;

        if (not vlayer.isEditable()):
            self._notifyNotEditableLayer()
            return

        # POINT CAPTURING
        if (self._featureType == QgsMapToolAddFeature.Point):
            self.messageEmitted.emit(self.tr('DEBUG: button click point'), QgsMessageBar.INFO)
            if (e.button() != Qt.LeftButton):
                return

            idPoint = QgsPoint()  #point in map coordinates
            savePoint = QgsPoint()  #point in layer coordinates
            idPoint = self._snapCursorPoint(e.pos())
            try:
                savePoint = self.toLayerCoordinates(vlayer, idPoint)
            except:
                self.messageEmitted.emit(self.tr('Cannot transform the point to the layers coordinate system'), QgsMessageBar.WARNING)
                return

            f = QgsFeature(vlayer.pendingFields(), 0)
            g = None
            if (layerWKBType == QGis.WKBPoint or layerWKBType == QGis.WKBPoint25D):
                g = QgsGeometry.fromPoint(savePoint)
            elif (layerWKBType == QGis.WKBMultiPoint or layerWKBType == QGis.WKBMultiPoint25D):
                g = QgsGeometry.fromMultiPoint(QgsMultiPoint(savePoint))
            f.setGeometry(g)
            self.addFeature(vlayer, f, False)
            self.canvas().refresh()

        # LINE AND POLYGON CAPTURING
        elif (self._featureType == QgsMapToolAddFeature.Line or self._featureType == QgsMapToolAddFeature.Segment or self._featureType == QgsMapToolAddFeature.Polygon):
            self.messageEmitted.emit(self.tr('DEBUG: button click line or poly'), QgsMessageBar.INFO)

            #add point to list and to rubber band
            if (e.button() == Qt.LeftButton):
                self._startCapturing();
                error = self._addVertex(e.pos())
                if (error == 1):
                    #current layer is not a vector layer
                    self.messageEmitted.emit(self.tr('Current Layer is not a vector layer'), QgsMessageBar.WARNING)
                    return
                elif (error == 2):
                    #problem with coordinate transformation
                    self.messageEmitted.emit(self.tr('Cannot transform the point to the layers coordinate system'), QgsMessageBar.WARNING)
                    return

                if (self._featureType == QgsMapToolAddFeature.Segment and len(self._mapPointList) == 2):
                    self._captureFeature()

            elif (e.button() == Qt.RightButton):
                self._captureFeature()

    def _captureFeature(self):
        # End of string
        self._deleteMoveRubberBand()

        vlayer = self._currentVectorLayer()
        if (vlayer is None):
            self._stopCapturing()
            self._notifyNotVectorLayer()
            return

        layerWKBType = vlayer.wkbType()

        #segments: bail out if there are not exactly two vertices
        if (self._featureType == QgsMapToolAddFeature.Segment and len(self._mapPointList) != 2):
            self._stopCapturing()
            return

        #lines: bail out if there are not at least two vertices
        if (self._featureType == QgsMapToolAddFeature.Line and len(self._mapPointList) < 2):
            self._stopCapturing()
            return

        #polygons: bail out if there are not at least three vertices
        if (self._featureType == QgsMapToolAddFeature.Polygon and len(self._mapPointList) < 3):
            self._stopCapturing()
            return

        #create QgsFeature with wkb representation
        f = QgsFeature(vlayer.pendingFields(), 0)

        g = None

        if (self._featureType == QgsMapToolAddFeature.Line or self._featureType == QgsMapToolAddFeature.Segment):

            if (layerWKBType == QGis.WKBLineString or layerWKBType == QGis.WKBLineString25D):
                g = QgsGeometry.fromPolyline(self._layerPoints())
            elif (layerWKBType == QGis.WKBMultiLineString or layerWKBType == QGis.WKBMultiLineString25D):
                g = QgsGeometry.fromMultiPolyline([self._layerPoints()])
            else:
                self.messageEmitted.emit(self.tr('Cannot add feature. Unknown WKB type'), QgsMessageBar.CRITICAL)
                self._stopCapturing()
                return #unknown wkbtype

            f.setGeometry( g );

        else: # polygon

            if (layerWKBType == QGis.WKBPolygon or  layerWKBType == QGis.WKBPolygon25D):
                g = QgsGeometry.fromPolygon([self._layerPoints()])
            elif (layerWKBType == QGis.WKBMultiPolygon or  layerWKBType == QGis.WKBMultiPolygon25D):
                g = QgsGeometry.fromMultiPolygon([self._layerPoints()])
            else:
                self.messageEmitted.emit(self.tr('Cannot add feature. Unknown WKB type'), QgsMessageBar.CRITICAL)
                self._stopCapturing()
                return #unknown wkbtype

            if (g is None):
                self._stopCapturing()
                return # invalid geometry; one possibility is from duplicate points
            f.setGeometry(g)

            avoidIntersectionsReturn = f.geometry().avoidIntersections()
            if (avoidIntersectionsReturn == 1):
                #not a polygon type. Impossible to get there
                pass
            elif (avoidIntersectionsReturn == 3):
                self.messageEmitted.emit(self.tr('An error was reported during intersection removal'), QgsMessageBar.CRITICAL)

            if (not f.geometry().asWkb()): #avoid intersection might have removed the whole geometry
                reason = ''
                if (avoidIntersectionsReturn != 2):
                    reason = self.tr('The feature cannot be added because it\'s geometry is empty')
                else:
                    reason = self.tr('The feature cannot be added because it\'s geometry collapsed due to intersection avoidance')
                self.messageEmitted.emit(reason, QgsMessageBar.CRITICAL)
                self._stopCapturing()
                return

        if (self.addFeature(vlayer, f, False)):
            #add points to other features to keep topology up-to-date
            topologicalEditing = QgsProject.instance().readNumEntry('Digitizing', '/TopologicalEditing', 0)

            #use always topological editing for avoidIntersection.
            #Otherwise, no way to guarantee the geometries don't have a small gap in between.
            intersectionLayers = QgsProject.instance().readListEntry('Digitizing', '/AvoidIntersectionsList')
            avoidIntersection = len(intersectionLayers)
            if (avoidIntersection): #try to add topological points also to background layers
                for intersectionLayer in intersectionLayers:
                    vl = QgsMapLayerRegistry.instance().mapLayer(str(intersectionLayer))
                    #can only add topological points if background layer is editable...
                    if (vl is not None and vl.geometryType() == QGis.Polygon and vl.isEditable()):
                        vl.self._addTopologicalPoints(f.geometry())
            elif (topologicalEditing):
                vlayer.self._addTopologicalPoints(f.geometry())

        self._stopCapturing()

    def _addTopologicalPoints(self, geom):
        if self.canvas() is None:
            return 1
        vlayer = self._currentVectorLayer()
        if vlayer is None:
            return 2
        for point in geom:
            vlayer.self._addTopologicalPoints(point)
        return 0

    def _layerPoints(self):
        layerPoints = []
        vlayer = self._currentVectorLayer()
        if vlayer is None:
            return layerPoints
        for mapPoint in self._mapPointList:
            layerPoint = self.toLayerCoordinates(vlayer, mapPoint)
            layerPoints.append(layerPoint)
        return layerPoints

    def _currentVectorLayer(self):
        layer = self.canvas().currentLayer()
        if (layer.type() == QgsMapLayer.VectorLayer):
            return layer
        else:
            return None

    def _notifyNotVectorLayer(self):
        self.messageEmitted.emit(self.tr('No active vector layer'), QgsMessageBar.INFO)

    def _notifyNotEditableLayer(self):
        self.messageEmitted.emit(self.tr('Layer not editable'), QgsMessageBar.INFO)
