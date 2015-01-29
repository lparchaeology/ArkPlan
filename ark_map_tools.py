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
from PyQt4.QtCore import Qt, QSettings, QTranslator, qVersion, QCoreApplication, QVariant, QObject, SIGNAL, pyqtSignal, QFileInfo, QPoint
from PyQt4.QtGui import QAction, QIcon, QDockWidget, QInputDialog, QColor, QFileDialog

from qgis.core import *
from qgis.gui import QgsMapToolEmitPoint, QgsRubberBand

class LevelsMapTool(QgsMapToolEmitPoint):

    levelAdded = pyqtSignal(QgsPoint, float)

    def __init__(self, canvas):
        self.canvas = canvas
        QgsMapToolEmitPoint.__init__(self, canvas)

    def canvasPressEvent(self, e):
        if e.button() != Qt.LeftButton:
            return
        elevation, ok = QInputDialog.getDouble(None, 'Add Level', 'Please enter the elevation in meters (m):',
                                               0, -100, 100, 2)
        if ok:
            point = self.toMapCoordinates(e.pos())
            self.levelAdded.emit(point, elevation)

# Map Tool to take two points and draw a hachure
class HacureMapTool(QgsMapToolEmitPoint):

    hachureAdded = pyqtSignal(QgsPoint, QgsPoint, 'QString')
    startPoint = None
    endPoint = None
    rubberBand = None
    hachureType = 'hch'

    def __init__(self, canvas, type='hch'):
        self.canvas = canvas
        self.hachureType = type
        QgsMapToolEmitPoint.__init__(self, canvas)

    def canvasMoveEvent(self, e):
        if self.startPoint:
            toPoint = self.toMapCoordinates(e.pos())
            if self.rubberBand:
                self.rubberBand.reset()
            else:
                self.rubberBand = QgsRubberBand(self.canvas, False)
                self.rubberBand.setColor(QColor(Qt.red))
            points  = [self.startPoint, toPoint]
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
            self.endPoint = self.toMapCoordinates(e.pos())
            self.rubberBand.reset()
            self.hachureAdded.emit(self.startPoint, self.endPoint, self.hachureType)
            self.startPoint = None
            self.endPoint = None

    def type(self):
        return self.hachureType

    def setType(self, type):
        self.hachureType = type

# Map Tool to take mulitple points and draw a line
class LineMapTool(QgsMapToolEmitPoint):

    lineAdded = pyqtSignal(list, 'QString')
    points = []
    rubberBand = None
    lineType = 'ext'

    def __init__(self, canvas, type='ext'):
        self.canvas = canvas
        self.lineType = type
        QgsMapToolEmitPoint.__init__(self, canvas)

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
            self.lineAdded.emit(self.points, self.lineType)
            self.points = []
        else:
            self.rubberBand.reset()
            self.points = []

    def type(self):
        return self.lineType

    def setType(self, type):
        self.lineType = type

# Map Tool to take mulitple points and draw a line
class PolygonMapTool(QgsMapToolEmitPoint):

    polygonAdded = pyqtSignal(list, 'QString')
    points = []
    rubberBand = None
    polygonType = 'ext'

    def __init__(self, canvas, type='ext'):
        self.canvas = canvas
        self.lineType = type
        QgsMapToolEmitPoint.__init__(self, canvas)

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
            self.polygonAdded.emit(self.points, self.polygonType)
            self.points = []
        else:
            self.rubberBand.reset()
            self.points = []

    def type(self):
        return self.polygonType

    def setType(self, type):
        self.polygonType = type
