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
from PyQt4.QtCore import Qt, pyqtSignal
from PyQt4.QtGui import QInputDialog, QColor

from qgis.core import QgsGeometry, QgsPoint
from qgis.gui import QgsMapTool, QgsRubberBand

class SnapMapTool(QgsMapTool):

    toolType = ''
    points = []
    rubberBand = None

    def __init__(self, canvas, type):
        self.canvas = canvas
        self.toolType = type
        QgsMapTool.__init__(self, canvas)

    def type(self):
        return self.toolType

    def setType(self, toolType):
        self.toolType = toolType

class LevelsMapTool(SnapMapTool):

    levelAdded = pyqtSignal(QgsPoint, 'QString', float)

    def __init__(self, canvas, type='lvl'):
        SnapMapTool.__init__(self, canvas, type)

    def canvasPressEvent(self, e):
        if e.button() != Qt.LeftButton:
            return
        elevation, ok = QInputDialog.getDouble(None, 'Add Level', 'Please enter the elevation in meters (m):',
                                               0, -100, 100, 2)
        if ok:
            point = self.toMapCoordinates(e.pos())
            self.levelAdded.emit(point, self.toolType, elevation)

# Map Tool to take two points and draw a line segment, e.g. hachures
class LineSegmentMapTool(SnapMapTool):

    lineSegmentAdded = pyqtSignal(list, 'QString')
    startPoint = None
    endPoint = None

    def __init__(self, canvas, type='hch'):
        SnapMapTool.__init__(self, canvas, type)

    def canvasMoveEvent(self, e):
        if self.startPoint:
            toPoint = self.toMapCoordinates(e.pos())
            if self.rubberBand:
                self.rubberBand.reset()
            else:
                self.rubberBand = QgsRubberBand(self.canvas, False)
                self.rubberBand.setColor(QColor(Qt.red))
            points = [self.startPoint, toPoint]
            self.rubberBand.setToGeometry(QgsGeometry.fromPolyline(points), None)

    def canvasPressEvent(self, e):
        if e.button() != Qt.LeftButton:
            self.rubberBand.reset()
            self.startPoint = None
            self.endPoint = None
            return
        if self.startPoint is None:
            self.startPoint = self.toMapCoordinates(e.pos())
        else:
            self.points = [self.startPoint, self.toMapCoordinates(e.pos())]
            self.rubberBand.reset()
            self.lineSegmentAdded.emit(self.points, self.toolType)
            self.startPoint = None
            self.points = []

# Map Tool to take mulitple points and draw a line
class LineMapTool(SnapMapTool):

    lineAdded = pyqtSignal(list, 'QString')

    def __init__(self, canvas, type='ext'):
        SnapMapTool.__init__(self, canvas, type)

    def canvasMoveEvent(self, e):
        if len(self.points) > 0:
            rbPoints = list(self.points)
            toPoint = self.toMapCoordinates(e.pos())
            rbPoints.append(toPoint)
            if self.rubberBand:
                self.rubberBand.reset()
            else:
                self.rubberBand = QgsRubberBand(self.canvas, False)
                self.rubberBand.setColor(QColor(Qt.red))
            self.rubberBand.setToGeometry(QgsGeometry.fromPolyline(rbPoints), None)

    def canvasPressEvent(self, e):
        if e.button() == Qt.LeftButton:
            point = self.toMapCoordinates(e.pos())
            self.points.append(point)
        elif e.button() == Qt.RightButton:
            self.rubberBand.reset()
            self.lineAdded.emit(self.points, self.toolType)
            self.points = []
        else:
            self.rubberBand.reset()
            self.points = []

# Map Tool to take mulitple points and draw a line
class PolygonMapTool(SnapMapTool):

    polygonAdded = pyqtSignal(list, 'QString')

    def __init__(self, canvas, type='ext'):
        SnapMapTool.__init__(self, canvas, type)

    def canvasMoveEvent(self, e):
        if len(self.points) > 0:
            rbPoints = list(self.points)
            toPoint = self.toMapCoordinates(e.pos())
            rbPoints.append(toPoint)
            if self.rubberBand:
                self.rubberBand.reset()
            else:
                self.rubberBand = QgsRubberBand(self.canvas, False)
                self.rubberBand.setColor(QColor(Qt.red))
            if len(self.points) == 1:
                self.rubberBand.setToGeometry(QgsGeometry.fromPolyline(rbPoints), None)
            else:
                self.rubberBand.setToGeometry(QgsGeometry.fromPolygon([rbPoints]), None)

    def canvasPressEvent(self, e):
        if e.button() == Qt.LeftButton:
            point = self.toMapCoordinates(e.pos())
            self.points.append(point)
        elif e.button() == Qt.RightButton:
            self.rubberBand.reset()
            self.polygonAdded.emit(self.points, self.toolType)
            self.points = []
        else:
            self.rubberBand.reset()
            self.points = []
