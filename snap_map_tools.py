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
from PyQt4.QtGui import QInputDialog, QColor, QAction

from qgis.core import QGis, QgsGeometry, QgsPoint, QgsVectorLayer, QgsFeature
from qgis.gui import QgsMapTool, QgsRubberBand, QgsMapCanvasSnapper, QgsVertexMarker

# Code ported from QGIS app and adapted to take default attribute values
# Snapping code really should be in the public api classes

typedef QMap<int, QVariant> QgsAttributeMap

class QgsFeatureAction(QAction):

    _layer = QgsVectorLayer()
    _feature = QgsFeature()
    _action = -1
    _idx = -1
    _featureSaved = False
    _lastUsedValues = {}

    def __init__(self, name, feature, layer, action=-1, defaultAttr=-1, parent=None):
        super(QgsFeatureAction, self).__init__(name, parent)
        self._layer = layer
        self._feature = feature
        self._action = action
        self._idx = defaultAttr

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
        myDa.setEllipsoidalMode(QgsInterface.instance().mapCanvas().mapSettings().hasCrsTransformEnabled())
        myDa.setEllipsoid(QgsProject.instance().readEntry('Measure', '/Ellipsoid', GEO_NONE))

        context.setDistanceArea(myDa)
        context.setVectorLayerTools(QgsInterface.instance().vectorLayerTools())

        dialog = QgsAttributeDialog(self._layer, f, cloneFeature, None, True, context)

        if (self._layer.actions().size() > 0):
            dialog.setContextMenuPolicy(Qt.ActionsContextMenu)

            a = QAction(self.tr('Run actions'), dialog)
            a.setEnabled(False)
            dialog.addAction(a)

            i = 0
            for action in self._layer.actions():
                if (action.runable()):
                    a = QgsFeatureAction(action.name(), f, self._layer, i, -1, dialog)
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

    def addFeature(self, defaultAttributes=QgsAttributeMap(), showModal=True):
        if (self._layer is None or not self._layer.isEditable()):
            return False

        provider = self._layer.dataProvider()

        settings = QSettings()
        reuseLastValues = settings.value('/qgis/digitizing/reuseLastValues', False).toBool()
        QgsDebugMsg('reuseLastValues: %1' % reuseLastValues)

        fields = self._layer.pendingFields()
        self._feature.initAttributes(fields.count())
        for idx in range(0, fields.count() - 1):
            v = ''

            if (defaultAttributes.contains(idx)):
                v = defaultAttributes.value(idx)
            elif (reuseLastValues and self._lastUsedValues.contains(self._layer) and self._lastUsedValues[self._layer].contains(idx)):
                v = self._lastUsedValues[self._layer][idx]
            else:
                v = provider.defaultValue(idx)

            self._feature.setAttribute(idx, v)

        isDisabledAttributeValuesDlg = settings.value('/qgis/digitizing/disable_enter_attribute_values_dialog', False).toBool()
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

            dialog.attributeForm.featureSaved.connect(self._onFeatureSaved)

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
        reuseLastValues = settings.value('/qgis/digitizing/reuseLastValues', False).toBool()
        QgsDebugMsg('reuseLastValues: %1' % reuseLastValues)

        if (reuseLastValues):
            fields = self._layer.pendingFields()
            for idx in range(0, fields.count() - 1):
                newValues = feature.attributes()
                origValues = self._lastUsedValues[self._layer]
                if (origValues[idx] != newValues[idx]):
                    QgsDebugMsg('saving %s for %s' % (self._lastUsedValues[self._layer][idx].toString(), idx))
                    self._lastUsedValues[self._layer][idx] = newValues[idx]


class QgsMapToolEdit(QgsMapTool):

    _snapper = QgsMapCanvasSnapper()

    def __init__(self, canvas):
        super(QgsMapToolEdit, self).__init__(canvas)
        self._snapper.setCanvas(canvas)

    def isEditTool(self):
        return True

    def _insertSegmentVerticesForSnap(self, snapResults, editedLayer):
        layerPoint = QgsPoint()
        if (editedLayer is None or not editedLayer.isEditable()):
            return 1
        transformedSnapResults = snapResults
        for snapResult in transformedSnapResults:
            layerPoint = self.toLayerCoordinates(editedLayer, snapResult.snappedVertex)
            snapResult.snappedVertex = layerPoint
        return editedLayer.insertSegmentVerticesForSnap(transformedSnapResults)

    def _snapPointFromResults(self, snapResults, screenCoords):
        if (snapResults.size() < 1):
            return self.toMapCoordinates(screenCoords)
        else:
            return snapResults[0].snappedVertex

    def _createRubberBand(self, geometryType, alternativeBand):
        settings = QSettings()
        rb = QgsRubberBand(self.canvas(), geometryType)
        rb.setWidth(settings.value('/qgis/digitizing/line_width', 1).toInt())
        color = QColor(settings.value('/qgis/digitizing/line_color_red', 255).toInt(),
                       settings.value('/qgis/digitizing/line_color_green', 0).toInt(),
                       settings.value('/qgis/digitizing/line_color_blue', 0).toInt() )
        myAlpha = settings.value('/qgis/digitizing/line_color_alpha', 200).toInt() / 255.0
        if (alternativeBand):
            myAlpha = myAlpha * settings.value('/qgis/digitizing/line_color_alpha_scale', 0.75 ).toDouble()
            rb.setLineStyle(Qt.DotLine)
        if (geometryType == QGis.Polygon):
            color.setAlphaF(myAlpha)
        color.setAlphaF(myAlpha)
        rb.setColor(color)
        rb.show()
        return rb

    def _currentVectorLayer(self):
        layer = self.canvas().currentLayer()
        if (layer.type() != QgsMapLayer.Vector):
            return layer
        else:
            return None

    def _addTopologicalPoints(self, geom):
        if self.canvas() is None:
            return 1
        vlayer = self._currentVectorLayer()
        if vlayer is None:
            return 2
        for point in geom:
            vlayer.self._addTopologicalPoints(point)
        return 0

    def _notifyNotVectorLayer(self):
        self.messageEmitted.emit(self.tr('No active vector layer'))

    def _notifyNotEditableLayer(self):
        self.messageEmitted.emit(self.tr('Layer not editable'))


class QgsMapToolCapture(QgsMapToolEdit):

    CaptureNone = 0
    CapturePoint = 1
    CaptureLine = 2
    CapturePolygon = 3

    _captureMode = 0 #QgsMapToolEdit.CapturePoint
    _capturing = False
    _rubberBand = None #QgsRubberBand()
    _tempRubberBand = None #QgsRubberBand()
    _captureList = [] #QList<QgsPoint>
    _tip = ''
    _validator = None #QgsGeometryValidator()
    _geomErrors = [] #QList<QgsGeometry.Error>
    _geomErrorMarkers = [] #QList<QgsVertexMarker >
    _captureModeFromLayer = False
    _snappingMarker = None # QgsVertexMarker()

    def __init__(self, canvas, mode=0):
        super(QgsMapToolCapture, self).__init__(canvas)
        self._captureMode = mode
        self._captureModeFromLayer = (mode == QgsMapToolCapture.CaptureNone)

        mySelectQPixmap = QPixmap(capture_point_cursor)
        self.setCursor(QCursor(mySelectQPixmap, 8, 8))

        QgsInterface().currentLayerChanged.connect(self.currentLayerChanged)

    def __del__(self):
        self._snappingMarker = None
        self._stopCapturing();
        if (self._validator is not None):
            self._validator.deleteLater()
        super(QgsMapToolCapture, self).__del__()

    def deactivate(self):
        self._snappingMarker = None
        super(QgsMapToolCapture, self).deactivate()

    def currentLayerChanged(self, layer):
        if not self._captureModeFromLayer:
            return
        self._captureMode = QgsMapToolCapture.CaptureNone;
        if (layer.type() != QgsMapLayer.Vector):
            return
        if (layer.geometryType() == QGis.Point):
            self._captureMode = QgsMapToolCapture.CapturePoint
        elif (layer.geometryType() == QGis.Line):
            self._captureMode = QgsMapToolCapture.CaptureLine
        elif (layer.geometryType() == QGis.Polygon):
            self._captureMode = QgsMapToolCapture.CapturePolygon

    def canvasMoveEvent(self, e):
        res, snapResults = self._snapper.snapToBackgroundLayers(e.pos())
        if (res != 0 or len(snapResults) < 1):
            self._snappingMarker = None
        else:
            if (self._snappingMarker is None):
                self._snappingMarker = QgsVertexMarker(self.canvas())
                self._snappingMarker.setIconType(QgsVertexMarker.ICON_CROSS)
                self._snappingMarker.setColor(Qt.magenta)
                self._snappingMarker.setPenWidth(3)
            self._snappingMarker.setCenter(snapResults[0].snappedVertex)

        if (self._captureMode != QgsMapToolCapture.CapturePoint and self._tempRubberBand is not None and self._capturing):
            mapPoint = self._snapPointFromResults(snapResults, e.pos())
            self._tempRubberBand.movePoint(mapPoint)

    def canvasPressEvent(self, e):
        pass

    def _points(self):
        return self._captureList

    def _setPoints(self, pointList):
        self._captureList = pointList

    def _nextPoint(self, p):
        res = 0
        layerPoint = QqsPoint()
        mapPoint = QgsPoint()
        vlayer = self._currentVectorLayer()
        if vlayer is None:
            QgsDebugMsg('no vector layer')
            res = 1
        res, snapResults = self._snapper.snapToBackgroundLayers(p)
        if (res == 0):
            mapPoint = self._snapPointFromResults(snapResults, p)
            try:
                layerPoint = self.toLayerCoordinates(vlayer, mapPoint)
            except:
                QgsDebugMsg('transformation to layer coordinate failed')
                res = 2
        return res, layerPoint, mapPoint

    def _addVertex(self, p):
        if (self._mode() == QgsMapToolCapture.CaptureNone):
            QgsDebugMsg('invalid capture mode')
            return 2

        res = 0
        res, layerPoint, mapPoint = self._nextPoint(p)
        if (res != 0):
            QgsDebugMsg('nextPoint failed: ' + str(res))
            return res

        type = QGis.Line
        if self._captureMode == QgsMapToolCapture.CapturePolygon:
            type = QGis.Polygon
        if (self._rubberBand is None):
            self._rubberBand = self._createRubberBand(type)
        self._rubberBand.addPoint(mapPoint)
        self._captureList.append(layerPoint)

        if (self._tempRubberBand is None):
            self._tempRubberBand = self._createRubberBand(type)
        else:
            self._tempRubberBand.reset(self._captureMode == QgsMapToolCapture.CapturePolygon)
        if (self._captureMode == QgsMapToolCapture.CaptureLine):
            self._tempRubberBand.addPoint(mapPoint)
        elif (self._captureMode == QgsMapToolCapture.CapturePolygon):
            firstPoint = self._rubberBand.getPoint(0, 0)
            self._tempRubberBand.addPoint(firstPoint)
            self._tempRubberBand.movePoint(mapPoint)
            self._tempRubberBand.addPoint(mapPoint)

        self._validateGeometry();
        return 0

    def _undo(self):
        if (self._rubberBand is not None):
            rubberBandSize = self._rubberBand.numberOfVertices();
            tempRubberBandSize = self._tempRubberBand.numberOfVertices();
            captureListSize = self._captureList.size();

            if (rubberBandSize < 1 or captureListSize < 1):
                return

            self._rubberBand.removePoint(-1)

            if (rubberBandSize > 1):
                if (tempRubberBandSize > 1):
                    point = self._rubberBand.getPoint(0, rubberBandSize - 2)
                    self._tempRubberBand.movePoint(tempRubberBandSize - 2, point)
            else:
                self._tempRubberBand.reset(self._captureMode == QgsMapToolCapture.CapturePolygon)

            self._captureList.pop()
            self._validateGeometry()

    def keyPressEvent(self, e):
        if (e.key() == Qt.Key_Backspace or e.key() == Qt.Key_Delete):
            self._undo()
            e.ignore()

    def _startCapturing(self):
        self._capturing = True

    def _isCapturing(self):
        return self._capturing

    def _stopCapturing(self):
        self._rubberBand = None
        self._tempRubberBand = None
        self._geomErrorMarkers = []
        self._geomErrors = []
        self._capturing = False
        self._captureList = []
        self.canvas().refresh()

    def _deleteTempRubberBand(self):
        self._tempRubberBand = None

    def _mode(self):
        return self._captureMode

    def _closePolygon(self):
        self._captureList.append(self._captureList[0])

    def _validateGeometry(self):
        settings = QSettings()
        if (settings.value('/qgis/digitizing/validate_geometries', 1 ).toInt() == 0):
            return

        if (self._validator is not None):
            self._validator.deleteLater()
            self._validator = None

        self._tip = '';
        self._geomErrors = []
        self._geomErrorMarkers = []

        g = None #QgsGeometry()

        if (self._captureMode == QgsMapToolCapture.CaptureNone or self._captureMode == QgsMapToolCapture.CapturePoint):
            return
        elif (self._captureMode == QgsMapToolCapture.CaptureLine):
            if (self._captureList.size() < 2):
                return
            g = QgsGeometry.fromPolyline(self._captureList.toVector())
        elif (self._captureMode == QgsMapToolCapture.CapturePolygon):
            if (self._captureList.size() < 3):
                return
            closed = self._captureList
            closed.append(self._captureList[0])
            g = QgsGeometry.fromPolygon(QgsPolygon(QgsPolyline(closed)))

        if (g is None):
            return

        self._validator = QgsGeometryValidator(g)
        self._validator.errorFound.connect(self._addError)
        self._validator.finished.connect(self.validationFinished)
        self._validator.start()

        sb = QgsInstance().statusBar()
        sb.showMessage(self.tr('Validation started.'))

    def _addError(self, e):
        self._geomErrors.append(e)
        vlayer = self._currentVectorLayer()
        if (vlayer is None):
            return

        if (self._tip != ''):
            self._tip += '\n'

        self._tip += e.what()

        if (e.hasWhere()):
            vm = QgsVertexMarker(self.canvas())
            vm.setCenter(self.canvas().mapSettings().layerToMapCoordinates(vlayer, e.where()))
            vm.setIconType(QgsVertexMarker.ICON_X)
            vm.setPenWidth(2)
            vm.setToolTip(e.what())
            vm.setColor(Qt.green)
            vm.setZValue(vm.zValue() + 1)
            self._geomErrorMarkers.append(vm)

        sb = QgsInstance().statusBar()
        sb.showMessage(e.what())
        if (self._tip != ''):
            sb.setToolTip(self._tip)

    def validationFinished(self):
        sb = QgsInstance().statusBar()
        sb.showMessage(self.tr('Validation finished.'))


class QgsMapToolAddFeature(QgsMapToolCapture):

    def __init__(self, canvas, mode=QgsMapToolCapture.CaptureNone):
        super(QgsMapToolCapture, self).__init__(canvas)
        self.setToolName(self.tr('Add feature'))

    def addFeature(self, vlayer, feature, showModal=True):
        action = QgsFeatureAction(self.tr('add feature'), feature, vlayer, -1, -1, self)
        res = action.addFeature(QgsAttributeMap(), showModal)
        if (showModal):
            action = None
        return res

    def activate(self):
        vlayer = self._currentVectorLayer()
        if (vlayer is not None and vlayer.geometryType() == QGis.NoGeometry):
            self.addFeature(vlayer, QgsFeature(), False)
            return
        super(QgsMapToolCapture, self).activate()

    def canvasReleaseEvent(self, e):
        QgsDebugMsg('entered.')

        vlayer = self._currentVectorLayer()
        if (vlayer is None):
            self._notifyNotVectorLayer()
            return

        layerWKBType = vlayer.wkbType()

        provider = vlayer.dataProvider()

        if (not (provider.capabilities() & QgsVectorDataProvider.AddFeatures)):
            self.messageEmitted.emit(self.tr('The data provider for this layer does not support the addition of features.'), QgsMessageBar.WARNING)
            return

        if (not vlayer.isEditable()):
            self._notifyNotEditableLayer()
            return

        # POINT CAPTURING
        if (self._mode() == QgsMapToolCapture.CapturePoint):
            if (e.button() != Qt.LeftButton):
                return

            #check we only use this tool for point/multipoint layers
            if (vlayer.geometryType() != QGis.Point):
                self.messageEmitted.emit(self.tr('Wrong editing tool, cannot apply the "capture point" tool on this vector layer'), QgsMessageBar.WARNING)
                return;

            idPoint = QgsPoint() #point in map coordinates
            savePoint = QgsPoint() #point in layer coordinates
            res, snapResults = self._snapper.snapToBackgroundLayers(e.pos())

            if (res == 0):
                idPoint = self._snapPointFromResults(snapResults, e.pos())
                try:
                    savePoint = self.toLayerCoordinates(vlayer, idPoint)
                    QgsDebugMsg('savePoint = ' + savePoint.toString())
                except:
                    self.messageEmitted.emit(self.tr('Cannot transform the point to the layers coordinate system'), QgsMessageBar.WARNING)
                    return

            #only do the rest for provider with feature addition support
            #note that for the grass provider, this will return False since
            #grass provider has its own mechanism of feature addition
            if (provider.capabilities() & QgsVectorDataProvider.AddFeatures):
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
        elif (self._mode() == QgsMapToolCapture.CaptureLine or self._mode() == QgsMapToolCapture.CapturePolygon):

            #check we only use the line tool for line/multiline layers
            if (self._mode() == QgsMapToolCapture.CaptureLine and vlayer.geometryType() != QGis.Line):
                self.messageEmitted.emit(self.tr('Wrong editing tool, cannot apply the "capture line" tool on this vector layer'), QgsMessageBar.WARNING)
                return;

            #check we only use the polygon tool for polygon/multipolygon layers
            if (self._mode() == QgsMapToolCapture.CapturePolygon and vlayer.geometryType() != QGis.Polygon):
                self.messageEmitted.emit(self.tr('Wrong editing tool, cannot apply the "capture polygon" tool on this vector layer'), QgsMessageBar.WARNING)
                return

            #add point to list and to rubber band
            if (e.button() == Qt.LeftButton):

                error = self._addVertex(e.pos())
                if (error == 1):
                    #current layer is not a vector layer
                    return;
                elif (error == 2):
                    #problem with coordinate transformation
                    self.messageEmitted.emit(self.tr('Cannot transform the point to the layers coordinate system'), QgsMessageBar.WARNING)
                    return
                self._startCapturing();

            elif (e.button() == Qt.RightButton):
                # End of string
                self._deleteTempRubberBand()

                #lines: bail out if there are not at least two vertices
                if (self._mode() == QgsMapToolCapture.CaptureLine and self._captureList.size() < 2):
                    self._stopCapturing()
                    return

                #polygons: bail out if there are not at least two vertices
                if (self._mode() == QgsMapToolCapture.CapturePolygon and self._captureList.size() < 3):
                    self._stopCapturing()
                    return

                #create QgsFeature with wkb representation
                f = QgsFeature(vlayer.pendingFields(), 0)

                g = None

                if (self._mode() == QgsMapToolCapture.CaptureLine):

                    if (layerWKBType == QGis.WKBLineString or layerWKBType == QGis.WKBLineString25D):
                        g = QgsGeometry.fromPolyline(self._points())
                    elif (layerWKBType == QGis.WKBMultiLineString or layerWKBType == QGis.WKBMultiLineString25D):
                        g = QgsGeometry.fromMultiPolyline(QgsMultiPolyline(self._points()))
                    else:
                        self.messageEmitted.emit(self.tr('Cannot add feature. Unknown WKB type'), QgsMessageBar.CRITICAL)
                        self._stopCapturing()
                        return #unknown wkbtype

                    f.setGeometry( g );

                else: # polygon

                    if (layerWKBType == QGis.WKBPolygon or  layerWKBType == QGis.WKBPolygon25D):
                        g = QgsGeometry.fromPolygon(QgsPolygon(self._points()))
                    elif (layerWKBType == QGis.WKBMultiPolygon or  layerWKBType == QGis.WKBMultiPolygon25D):
                        g = QgsGeometry.fromMultiPolygon(QgsMultiPolygon(QgsPolygon(self._points())))
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
                            vl = QgsMapLayerRegistry.instance().mapLayer(intersectionLayer)
                            #can only add topological points if background layer is editable...
                            if (vl is not None and vl.geometryType() == QGis.Polygon and vl.isEditable()):
                                vl.self._addTopologicalPoints(f.geometry())
                    elif (topologicalEditing):
                        vlayer.self._addTopologicalPoints(f.geometry())

                self._stopCapturing()
