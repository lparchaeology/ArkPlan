# -*- coding: utf-8 -*-
"""
/***************************************************************************
 ArkPlanDialog
                                 A QGIS plugin
 Plugin to assist in digitising of Archaeological plans.
                             -------------------
        begin                : 2015-01-10
        git sha              : $Format:%H$
        copyright            : (C) 2015 by John Layt
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

import os

from PyQt4.QtCore import Qt, QEvent, qDebug, pyqtSignal, QPointF
from PyQt4.QtGui import QGraphicsView

class ArkGeorefGraphicsView(QGraphicsView):

    pointSelected = pyqtSignal(QPointF)
    buttonDown = False
    panning = False

    def __init__(self, parent=None):
        super(ArkGeorefGraphicsView, self).__init__(parent)
        self.setCursor(Qt.CrossCursor)

    def viewRect(self):
        return self.mapToScene(self.viewport().geometry()).boundingRect()

    def wheelEvent(self, event):
        factor = 1.41 ** (event.delta() / 240.0)
        self.scale(factor, factor)

    def mousePressEvent(self, event):
        if event.button() == Qt.LeftButton:
            self.buttonDown = True
            self.prevPos = event.pos()
            event.accept()
        else:
            event.ignore()

    def mouseReleaseEvent(self, event):
        if event.button() == Qt.LeftButton:
            self.buttonDown = False
            if self.panning:
                self.panning = False
                self.setCursor(Qt.CrossCursor)
            else:
                self.pointSelected.emit(self.mapToScene(event.pos()))
            event.accept()
        else:
            event.ignore()

    def mouseMoveEvent(self, event):
        if self.buttonDown:
            if not self.panning:
                self.panning = True
                self.setCursor(Qt.ClosedHandCursor)
            dX = event.x() - self.prevPos.x()
            dY = event.y() - self.prevPos.y()
            self.horizontalScrollBar().setValue(self.horizontalScrollBar().value() - dX)
            self.verticalScrollBar().setValue(self.verticalScrollBar().value() - dY)
            self.prevPos = event.pos()
            event.accept()
        else:
            event.ignore()
