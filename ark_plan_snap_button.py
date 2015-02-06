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

from qgis.core import QgsTolerance, QgsProject, QgsSnapper

class ArkPlanSnapButton(QToolButton):

    snapSettingsChanged = pyqtSignal(bool, str, float, str)

    project = None
    layerId = ''
    enabled = False
    snappingType = QgsSnapper.SnapToVertex
    unit = QgsTolerance.Pixels
    tolerance = 10.0
    avoidIntersections = False

    def __init__(self, parent=0):
        QToolButton.__init__(self, parent=None)

        #Disable until we have a layerId
        self.setEnabled(False)

        self.vertexIcon = QIcon(':/plugins/ArkPlan/iconSnapVertex.png')
        self.vertexAction = QAction(self.vertexIcon, 'Vertex', self)
        self.vertexAction.setStatusTip('Snap to vertex')

        self.segmentIcon = QIcon(':/plugins/ArkPlan/iconSnapSegment.png')
        self.segmentAction = QAction(self.segmentIcon, 'Segment', self)
        self.segmentAction.setStatusTip('Snap to segment')

        self.vertexSegmentIcon = QIcon(':/plugins/ArkPlan/iconSnapVertexSegment.png')
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

        # Make sure we catch changes in the main snapping dialog
        # TODO This respods to all updates, make it only respond to our layer changing
        # TODO Respond to project changing?
        self.project = QgsProject.instance()
        self.project.snapSettingsChanged.connect(self.updateButtonSettings)

    def updateSnapSettings(self):
        self.project.setSnapSettingsForLayer(self.layerId, self.enabled, self.snappingType, self.unit, self.tolerance, self.avoidIntersections)
        self.refreshButton()

    def updateButtonSettings(self):
        ok, self.enabled, self.snappingType, self.unit, self.tolerance, self.avoidIntersections = self.project.snapSettingsForLayer(self.layerId)
        self.refreshButton()

    def refreshButton(self):
        self.setChecked(self.enabled)
        if (self.snappingType == QgsSnapper.SnapToVertex):
            self.setIcon(self.vertexIcon)
        elif (self.snappingType == QgsSnapper.SnapToSegment):
            self.setIcon(self.segmentIcon)
        elif (self.snappingType == QgsSnapper.SnapToVertexAndSegment):
            self.setIcon(self.vertexSegmentIcon)

    def setLayerId(self, layerId):
        if (layerId):
            self.layerId = layerId
            self.setEnabled(True)
            self.updateButtonSettings()

    def snapToggled(self, enabled):
        self.enabled = bool(enabled)
        self.updateSnapSettings()

    def snapToVertex(self):
        self.snappingType = QgsSnapper.SnapToVertex
        self.updateSnapSettings()

    def snapToSegment(self):
        self.snappingType = QgsSnapper.SnapToSegment
        self.updateSnapSettings()

    def snapToVertexSegment(self):
        self.snappingType = QgsSnapper.SnapToVertexAndSegment
        self.updateSnapSettings()
