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
from PyQt4.QtGui import QToolButton, QMenu, QAction, QIcon, QActionGroup, QWidgetAction, QSpinBox

from qgis.core import QGis, QgsTolerance, QgsProject, QgsSnapper, QgsMapLayer

class TopoEditButton(QToolButton):

    topologicalEditingChanged = pyqtSignal(bool)

    _project = None

    def __init__(self, parent=None):
        QToolButton.__init__(self, parent)

        self._project = QgsProject.instance()

        self._refreshButton()
        self.toggled.connect(self._topoToggled)
        self.toggled.connect(self.topologicalEditingChanged)

        # Make sure we catch changes in the main snapping dialog
        # TODO Respond to project changing?
        self._project.snapSettingsChanged.connect(self._refreshButton)

    def _topoToggled(self, status):
        self._project.setTopologicalEditing(status)

    def _refreshButton(self):
        self.setChecked(self._project.topologicalEditing())


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
        self.vertexAction.setCheckable(True)

        self.segmentIcon = QIcon(':/plugins/ArkPlan/iconSnapSegment.png')
        self.segmentAction = QAction(self.segmentIcon, 'Segment', self)
        self.segmentAction.setStatusTip('Snap to segment')
        self.segmentAction.setCheckable(True)

        self.vertexSegmentIcon = QIcon(':/plugins/ArkPlan/iconSnapVertexSegment.png')
        self.vertexSegmentAction = QAction(self.vertexSegmentIcon, 'Vertex and Segment', self)
        self.vertexSegmentAction.setStatusTip('Snap to vertex and segment')
        self.vertexSegmentAction.setCheckable(True)

        self.typeActionGroup = QActionGroup(self)
        self.typeActionGroup.addAction(self.vertexAction)
        self.typeActionGroup.addAction(self.segmentAction)
        self.typeActionGroup.addAction(self.vertexSegmentAction)

        self.pixelUnitsAction = QAction('Pixels', self)
        self.pixelUnitsAction.setStatusTip('Use Pixels')
        self.pixelUnitsAction.setCheckable(True)

        self.mapUnitsAction = QAction('Map Units', self)
        self.mapUnitsAction.setStatusTip('Use Map Units')
        self.mapUnitsAction.setCheckable(True)

        self.unitActionGroup = QActionGroup(self)
        self.unitActionGroup.addAction(self.pixelUnitsAction)
        self.unitActionGroup.addAction(self.mapUnitsAction)

        self.avoidAction = QAction('Avoid Intersections', self)
        self.avoidAction.setStatusTip('Avoid Intersections in Topological editing')
        self.avoidAction.setCheckable(True)

        self.toleranceSpin = QSpinBox(self)
        self.toleranceAction = QWidgetAction(self)
        self.toleranceAction.setDefaultWidget(self.toleranceSpin)
        #self.toleranceAction = QAction('Tolerance', self)
        #self.toleranceAction.setStatusTip('Set the snapping tolerance')

        self.menu = QMenu(self)
        self.menu.addActions(self.typeActionGroup.actions())
        self.menu.addSeparator()
        self.menu.addActions(self.unitActionGroup.actions())
        self.menu.addAction(self.toleranceAction)
        self.menu.addSeparator()
        self.menu.addAction(self.avoidAction)
        self.setMenu(self.menu)

        self.toggled.connect(self.snapToggled)
        self.vertexAction.triggered.connect(self.snapToVertex)
        self.segmentAction.triggered.connect(self.snapToSegment)
        self.vertexSegmentAction.triggered.connect(self.snapToVertexSegment)
        self.pixelUnitsAction.triggered.connect(self.usePixelUnits)
        self.mapUnitsAction.triggered.connect(self.useMapUnits)
        self.avoidAction.toggled.connect(self.avoidToggled)

        # Make sure we catch changes in the main snapping dialog
        # TODO This responds to all updates, make it only respond to our layer changing
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
            self.vertexAction.setChecked(True)
        elif (self.snappingType == QgsSnapper.SnapToSegment):
            self.setIcon(self.segmentIcon)
            self.segmentAction.setChecked(True)
        elif (self.snappingType == QgsSnapper.SnapToVertexAndSegment):
            self.setIcon(self.vertexSegmentIcon)
            self.vertexSegmentAction.setChecked(True)

        if (self.unit == QgsTolerance.Pixels):
            self.pixelUnitsAction.setChecked(True)
        else:
            self.mapUnitsAction.setChecked(True)

        self.avoidAction.setChecked(self.avoidIntersections)

    def setLayer(self, layer):
        if (layer is not None and layer.isValid() and layer.type() == QgsMapLayer.VectorLayer):
            self.layerId = layer.id()
            self.setEnabled(True)
            self.avoidAction.setEnabled(layer.geometryType() == QGis.Polygon)
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

    def usePixelUnits(self):
        self.unit = QgsTolerance.Pixels
        self.updateSnapSettings()

    def useMapUnits(self):
        self.unit = QgsTolerance.MapUnits
        self.updateSnapSettings()

    def avoidToggled(self, status):
        self.avoidIntersections = status
        self.updateSnapSettings()
