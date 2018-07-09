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

from qgis.PyQt.QtCore import QRectF, Qt
from qgis.PyQt.QtWidgets import QGraphicsView


class FixedGraphicsView(QGraphicsView):

    def __init__(self, parent=None):
        super().__init__(parent)
        self.setCursor(Qt.ArrowCursor)
        self._rect = QRectF()

    def setSceneView(self, scene, rect):
        self.setScene(scene)
        self._rect = rect
        self.fitInView(self._rect, Qt.KeepAspectRatioByExpanding)

    def viewRect(self):
        return self.mapToScene(self.viewport().geometry()).boundingRect()

    def resizeEvent(self, event):
        self.fitInView(self._rect, Qt.KeepAspectRatioByExpanding)
        event.accept()

    def wheelEvent(self, event):
        event.ignore()

    def mousePressEvent(self, event):
        event.ignore()

    def mouseReleaseEvent(self, event):
        event.ignore()

    def mouseMoveEvent(self, event):
        event.ignore()
