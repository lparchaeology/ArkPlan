# -*- coding: utf-8 -*-
"""
/***************************************************************************
 ArkPlan
                                 A QGIS plugin
 Plugin to assist in digitising of Archaeological plans.
                              -------------------
        begin                : 2014-12-07
        git sha              : $Format:%H$
        copyright            : (C) 2014 by John Layt
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
from PyQt4.QtGui import QInputDialog, QColor

from qgis.core import *
from qgis.gui import QgsMapTool, QgsRubberBand, QgsMapCanvasSnapper, QgsVertexMarker

from snap_map_tools import *

class SnapVertexMarker(QgsVertexMarker):

    def __init__(self, canvas):
      QgsVertexMarker.__init__(self, canvas)
      sel.setIconType(QgsVertexMarker.ICON_CROSS )
      self.setColor(Qt.magenta)
      self.setPenWidth(3)

# Code adapted from QGIS QgsMapToolEdit and QgsMapToolCapture classes
class SnapMapTool(QgsMapTool):

    featureAdded = pyqtSignal(list, QGis.GeometryType, 'QString')

    featureType = ''
    geometryType = QGis.Point
    points = []
    snapper = QgsMapCanvasSnapper()
    pointsRubberBand = None
    mouseRubberBand = None

    def __init__(self, canvas, geometryType, featureType):
        self.canvas = canvas
        self.snapper.setMapCanvas(self.canvas)
        self.geometryType = geometryType
        self.featureType = featureType
        self.pointsRubberBand = self.createRubberBand(False)
        self.mouseRubberBand = self.createRubberBand(True)
        QgsMapTool.__init__(self, canvas)

    def featureType(self):
        return self.featureType

    def setType(self, featureType):
        self.featureType = featureType

    def snapPoint(self, canvasPoint):
        snapResults = []
        res, snapResults = self.snapper.snapToBackgroundLayers(canvasPoint)
        if (res != 0 or len(snapResults) < 1):
            return self.toMapCoordinates(canvasPoint)
        return snapResults[0].snappedVertex

    def snapPointFromResults(self, snapResults, screenCoords):
        if (len(snapResults) < 1):
            return self.toMapCoordinates(screenCoords)
        return snapResults[0].snappedVertex

    def createRubberBand(self, alternativeBand):
        rb = QgsRubberBand(self.canvas, self.geometryType)
        settings = QSettings()
        rb.setWidth(int(settings.value('/qgis/digitizing/line_width', 1)))
        r = int(settings.value('/qgis/digitizing/line_color_red', 255))
        g = int(settings.value('/qgis/digitizing/line_color_green', 0))
        b = int(settings.value('/qgis/digitizing/line_color_green', 0))
        a = int(settings.value('/qgis/digitizing/line_color_alpha', 0)) / 255.0
        color = QColor(r, g, b)
        if alternativeBand:
            scale = float(settings.value('/qgis/digitizing/line_color_alpha_scale', 0.75))
            a = a * scale
            rb.setLineStyle(Qt.DotLine)
        color.setAlphaF(a)
        rb.setColor(color)
        rb.show()
        return rb

    def drawSnapPoints(self):
        snapResultList = []
        res, snapResultList = self.snapper.snapToBackgroundLayers(e.pos())
        if (res == 0):
            snapMarkers = []
            for snapResult in snapResultList:
                snapMarker = SnapVertexMarker(self.canvas)
                snapMarker.setCenter(snapResult.snappedVertex)
                snapMarkers.append(snapMarker)

    # Add a clicked point to the vertices and rubberbands
    def addPoint(self, canvasPoint):
        layer = QProject.currentLayer()
        if layer.type() != QgsMapLayer.VectorLayer:
            return

        # Snap results are in project CRS
        projectPoint = self.snapPoint(canvasPoint)
        # Drawing layer may be in different CRS
        layerPoint = self.toLayerCoordinates(layer, projectPoint)

        self.points.append(layerPoint)
        if self.geometryType == QGis.Point:
            return
        self.pointsRubberBand.addPoint(projectPoint)
        self.mouseRubberBand.reset(self.geometryType)
        if (self.geometryType == QGis.Line):
            self.mouseRubberBand.addPoint(projectPoint)
        elif (self.geometryType == QGis.Polygon):
            firstPoint = self.pointsRubberBand.getPoint(0, 0)
            self.mouseRubberBand.addPoint(firstPoint)
            self.mouseRubberBand.movePoint(projectPoint)
            self.mouseRubberBand.addPoint(projectPoint)

        self.validateGeometry()

    def removeLastPoint(self):
        self.points.pop()
        if (self.pointsRubberBand.numberOfVertices() > 0):
            self.pointsRubberBand.removePoint(-1)
        if (self.mouseRubberBand.numberOfVertices() > 1):
            point = self.pointsRubberBand.getPoint(0, self.pointsRubberBand.numberOfVertices() - 2)
            self.mouseRubberBand.movePoint(self.mouseRubberBand.numberOfVertices() - 2, point)
        else:
            self.mouseRubberBand.reset(self.geometryType)
        self.validateGeometry()

    def validateGeometry(self):
        return

    def keyPressEvent(self,  e):
        if (e.key() == Qt.Key_Backspace or e.key() == Qt.Key_Delete):
            self.removeLastPoint()

    def canvasMoveEvent(self,  e):
        mapPoint = QgsPoint()
        #if ( mCaptureMode != CapturePoint && mTempRubberBand && mCapturing )
            #mapPoint = snapPointFromResults( snapResults, e.os() );
            #mTempRubberBand->movePoint( mapPoint );



class LevelsMapTool(SnapMapTool):

    levelAdded = pyqtSignal(QgsPoint, 'QString', float)

    def __init__(self, canvas, type='lvl'):
        SnapMapTool.__init__(self, canvas, QGis.Point, type)

    def canvasPressEvent(self, e):
        if e.button() != Qt.LeftButton:
            return
        elevation, ok = QInputDialog.getDouble(None, 'Add Level', 'Please enter the elevation in meters (m):',
                                               0, -100, 100, 2)
        if ok:
            point = self.toMapCoordinates(e.pos())
            self.levelAdded.emit(point, self.featureType, elevation)

    def canvasMoveEvent(self,  e):
        pass

# Map Tool to take two points and draw a line segment, e.g. hachures
class LineSegmentMapTool(SnapMapTool):

    lineSegmentAdded = pyqtSignal(list, 'QString')
    startPoint = None
    endPoint = None

    def __init__(self, canvas, type='hch'):
        SnapMapTool.__init__(self, canvas, QGis.Line, type)

    def canvasMoveEvent(self, e):
        if self.startPoint:
            toPoint = self.toMapCoordinates(e.pos())
            if self.pointsRubberBand:
                self.pointsRubberBand.reset()
            else:
                self.pointsRubberBand = self.createRubberBand(QGis.Line, False)
            points = [self.startPoint, toPoint]
            self.pointsRubberBand.setToGeometry(QgsGeometry.fromPolyline(points), None)

    def canvasPressEvent(self, e):
        if e.button() != Qt.LeftButton:
            self.pointsRubberBand.reset()
            self.startPoint = None
            self.endPoint = None
            return
        if self.startPoint is None:
            self.startPoint = self.toMapCoordinates(e.pos())
        else:
            self.points = [self.startPoint, self.toMapCoordinates(e.pos())]
            self.pointsRubberBand.reset()
            self.lineSegmentAdded.emit(self.points, self.featureType)
            self.startPoint = None
            self.points = []

# Map Tool to take mulitple points and draw a line
class LineMapTool(SnapMapTool):

    lineAdded = pyqtSignal(list, 'QString')

    def __init__(self, canvas, type='ext'):
        SnapMapTool.__init__(self, canvas, QGis.Line, type)

    def canvasMoveEvent(self, e):
        if len(self.points) > 0:
            rbPoints = list(self.points)
            toPoint = self.toMapCoordinates(e.pos())
            rbPoints.append(toPoint)
            if self.pointsRubberBand:
                self.pointsRubberBand.reset()
            else:
                self.pointsRubberBand = self.createRubberBand(QGis.Line, False)
            self.pointsRubberBand.setToGeometry(QgsGeometry.fromPolyline(rbPoints), None)

    def canvasPressEvent(self, e):
        if e.button() == Qt.LeftButton:
            point = self.toMapCoordinates(e.pos())
            self.points.append(point)
        elif e.button() == Qt.RightButton:
            self.pointsRubberBand.reset()
            self.lineAdded.emit(self.points, self.featureType)
            self.points = []
        else:
            self.pointsRubberBand.reset()
            self.points = []

# Map Tool to take mulitple points and draw a line
class PolygonMapTool(SnapMapTool):

    polygonAdded = pyqtSignal(list, 'QString')

    def __init__(self, canvas, type='ext'):
        SnapMapTool.__init__(self, canvas, QGis.Polygon, type)

    def canvasMoveEvent(self, e):
        if len(self.points) > 0:
            rbPoints = list(self.points)
            toPoint = self.toMapCoordinates(e.pos())
            rbPoints.append(toPoint)
            if self.pointsRubberBand:
                self.pointsRubberBand.reset()
            else:
                self.pointsRubberBand = self.createRubberBand(QGis.Polygon, False)
            if len(self.points) == 1:
                self.pointsRubberBand.setToGeometry(QgsGeometry.fromPolyline(rbPoints), None)
            else:
                self.pointsRubberBand.setToGeometry(QgsGeometry.fromPolygon([rbPoints]), None)

    def canvasPressEvent(self, e):
        if e.button() == Qt.LeftButton:
            self.addPoint(e.pos())
        elif (e.button() == Qt.RightButton and len(self.points) > 2):
            self.pointsRubberBand.reset()
            self.polygonAdded.emit(self.points, self.featureType)
            self.points = []
        else:
            self.pointsRubberBand.reset()
            self.points = []
