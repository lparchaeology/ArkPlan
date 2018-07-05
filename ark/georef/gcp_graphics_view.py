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


from qgis.PyQt.QtCore import QPointF, Qt, pyqtSignal
from qgis.PyQt.QtWidgets import QGraphicsView


class GcpGraphicsView(QGraphicsView):

    pointSelected = pyqtSignal(QPointF)

    def __init__(self, parent=None):
        super(GcpGraphicsView, self).__init__(parent)

        self.buttonDown = False
        self.panning = False

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
