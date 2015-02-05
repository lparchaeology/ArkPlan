# -*- coding: utf-8 -*-
"""
/***************************************************************************
 ArkPlanDialog
                                 A QGIS plugin
 Plugin to assist in digitising of Archaeological plans.
                             -------------------
        begin                : 2015-02-05
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
from PyQt4 import uic
from PyQt4.QtCore import Qt, pyqtSignal
from PyQt4.QtGui import QToolButton, QMenu, QAction, QIcon

class ArkPlanSnapButton(QToolButton):

    snappingChanged = pyqtSignal(bool, str, float, str)

    #TODO get defaults from QGIS settings?
    status = False
    geometry = 'vertex'
    tolerance = 10.0
    unit = 'pixel'

    def __init__(self, parent=0):
        QToolButton.__init__(self, parent=None)

        self.vertexIcon = QIcon()
        self.vertexAction = QAction(self.vertexIcon, 'Vertex', self)
        self.vertexAction.setStatusTip('Snap to vertex')

        self.segmentIcon = QIcon()
        self.segmentAction = QAction(self.segmentIcon, 'Segment', self)
        self.segmentAction.setStatusTip('Snap to segment')

        self.vertexSegmentIcon = QIcon()
        self.vertexSegmentAction = QAction(self.vertexSegmentIcon, 'Vertex and Segment', self)
        self.vertexSegmentAction.setStatusTip('Snap to vertex and segment')

        self.menu = QMenu()
        self.menu.addAction(self.vertexAction)
        self.menu.addAction(self.segmentAction)
        self.menu.addAction(self.vertexSegmentAction)
        self.setMenu(self.menu)

        self.toggled.connect(self.snapToggled)
        self.vertexAction.triggered.connect(self.snapToVertex)
        self.segmentAction.triggered.connect(self.snapToSegment)
        self.vertexSegmentAction.triggered.connect(self.snapToVertexSegment)

    def snapToggled(self, status):
        self.status = bool(status)
        self.emitState()

    def snapToVertex(self):
        self.setIcon(self.vertexIcon)
        self.geometry = 'vertex'
        self.emitState()

    def snapToSegment(self):
        self.setIcon(self.segmentIcon)
        self.geometry = 'segment'
        self.emitState()

    def snapToVertexSegment(self):
        self.setIcon(self.vertexSegmentIcon)
        self.geometry = 'vertex_and_segment'
        self.emitState()

    def emitState(self):
        self.snappingChanged.emit(self.status, self.geometry, self.tolerance, self.unit)
