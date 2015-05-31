# -*- coding: utf-8 -*-
"""
/***************************************************************************
                                      Ark
                                 A QGIS plugin
             QGIS Plugin for ARK, the Archaeological Recording Kit
                              -------------------
        begin                : 2015-03-02
        git sha              : $Format:%H$
        copyright            : (C) 2015 by L - P: Heritage LLP
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

"""
Widgets to use to configure QGIS project snapping settings

This module provides a set of widgets to allow easy configuration of QGIS vector layer snapping.

SnappingToolButton: A button to configure snapping options for a given layer.
TopoEditToolButton: A button to configure topological editing for a project.
"""

from PyQt4.QtCore import Qt, pyqtSignal, QSettings
from PyQt4.QtGui import QToolButton, QMenu, QIcon, QAction, QActionGroup, QWidgetAction, QDoubleSpinBox

from qgis.core import QGis, QgsTolerance, QgsProject, QgsSnapper, QgsMapLayer

import resources_rc

# Project setting utilities

def defaultSnappingMode():
    defaultSnappingModeString = QSettings().value('/qgis/digitizing/default_snap_mode', 'to vertex')
    defaultSnappingMode = QgsSnapper.SnapToVertex
    if (defaultSnappingModeString == "to vertex and segment" ):
        return QgsSnapper.SnapToVertexAndSegment
    elif (defaultSnappingModeString == 'to segment'):
        return QgsSnapper.SnapToSegment
    return QgsSnapper.SnapToVertex

def defaultSnappingUnit():
    unit = QSettings().value('/qgis/digitizing/default_snapping_tolerance_unit', 0, int)
    # Huh???
    if unit is None:
        return 0
    return unit

def defaultSnappingTolerance():
    tolerance = QSettings().value('/qgis/digitizing/default_snapping_tolerance', 10.0, float)
    # Huh???
    if tolerance is None:
        return 10.0
    return tolerance

def topologicalEditing():
    return QgsProject.instance().readNumEntry('Digitizing', '/TopologicalEditing', 0)

def intersectionLayers():
    return QgsProject.instance().readListEntry('Digitizing', '/AvoidIntersectionsList')

# Snapping Widgets

class SnappingToolButton(QToolButton):

    """Tool button to change snapping settings for a QGIS vector layer

    Signals:
        snapSettingsChanged(str, bool, str, QgsSnapper.SnappingType, QgsTolerance.UnitType, float, bool): Signal that the layer's snap settings have been changed by the button
    """

    snapSettingsChanged = pyqtSignal(str, bool, QgsSnapper.SnappingType, QgsTolerance.UnitType, float, bool)

    _layerId = ''
    _snapEnabled = False
    _snappingType = QgsSnapper.SnapToVertex
    _unitType = QgsTolerance.Pixels
    _tolerance = 10.0
    _avoidIntersections = False

    def __init__(self, parent=None):
        """Initialises the snapping tool button

        After creating the button, you must call setLayer().

        Args:
            parent (QWidget): The parent widget, defaults to None.
        """

        QToolButton.__init__(self, parent)

        self._project = QgsProject.instance()

        #Disable until we have a _layerId
        self.setEnabled(False)

        self._vertexIcon = QIcon(':/plugins/Ark/iconSnapVertex.png')
        self._vertexAction = QAction(self._vertexIcon, 'Vertex', self)
        self._vertexAction.setStatusTip('Snap to vertex')
        self._vertexAction.setCheckable(True)

        self._segmentIcon = QIcon(':/plugins/Ark/iconSnapSegment.png')
        self._segmentAction = QAction(self._segmentIcon, 'Segment', self)
        self._segmentAction.setStatusTip('Snap to segment')
        self._segmentAction.setCheckable(True)

        self._vertexSegmentIcon = QIcon(':/plugins/Ark/iconSnapVertexSegment.png')
        self._vertexSegmentAction = QAction(self._vertexSegmentIcon, 'Vertex and Segment', self)
        self._vertexSegmentAction.setStatusTip('Snap to vertex and segment')
        self._vertexSegmentAction.setCheckable(True)

        self._snappingTypeActionGroup = QActionGroup(self)
        self._snappingTypeActionGroup.addAction(self._vertexAction)
        self._snappingTypeActionGroup.addAction(self._segmentAction)
        self._snappingTypeActionGroup.addAction(self._vertexSegmentAction)

        self._pixelUnitsAction = QAction('Pixels', self)
        self._pixelUnitsAction.setStatusTip('Use Pixels')
        self._pixelUnitsAction.setCheckable(True)

        self._mapUnitsAction = QAction('Map Units', self)
        self._mapUnitsAction.setStatusTip('Use Map Units')
        self._mapUnitsAction.setCheckable(True)

        self._unitTypeActionGroup = QActionGroup(self)
        self._unitTypeActionGroup.addAction(self._pixelUnitsAction)
        self._unitTypeActionGroup.addAction(self._mapUnitsAction)

        self._avoidAction = QAction('Snap overlapping edges', self)
        self._avoidAction.setStatusTip('Snap to edges of any overlapping polygons, aka "Avoid Intersections"')
        self._avoidAction.setCheckable(True)

        self._toleranceSpin = QDoubleSpinBox(self)
        self._toleranceSpin.setDecimals(5)
        self._toleranceSpin.setMinimum(0.0)
        self._toleranceAction = QWidgetAction(self)
        self._toleranceAction.setDefaultWidget(self._toleranceSpin)
        self._toleranceAction.setStatusTip('Set the snapping tolerance')

        self._menu = QMenu(self)
        self._menu.addActions(self._snappingTypeActionGroup.actions())
        self._menu.addSeparator()
        self._menu.addActions(self._unitTypeActionGroup.actions())
        self._menu.addAction(self._toleranceAction)
        self._menu.addSeparator()
        self._menu.addAction(self._avoidAction)
        self.setMenu(self._menu)

        self.toggled.connect(self._snapToggled)
        self._vertexAction.triggered.connect(self._snapToVertex)
        self._segmentAction.triggered.connect(self._snapToSegment)
        self._vertexSegmentAction.triggered.connect(self._snapToVertexSegment)
        self._pixelUnitsAction.triggered.connect(self._usePixelUnits)
        self._mapUnitsAction.triggered.connect(self._useMapUnits)
        self._toleranceSpin.valueChanged.connect(self._toleranceChanged)
        self._avoidAction.toggled.connect(self._avoidToggled)

        # Make sure we catch changes in the main snapping dialog
        # TODO This responds to all updates, make it only respond to our layer changing
        self._project.snapSettingsChanged.connect(self.updateButton)
        # If a new _project is read then layer is no longer valid
        self._project.readProject.connect(self.disableButton)

    # Public API

    def layerId(self):
        """Returns the ID of the layer the button applies to"""
        return self._layerId

    def setLayer(self, layer):
        """Sets the layer the button applies to

        Args:
            layer (QgsVectorLayer): Vector layer the button is to apply to.
        """
        if (layer is None):
            self._layerId = ''
            self.setEnabled(False)
            self._snapEnabled = False
            self._refreshButton()
        elif (layer.isValid() and layer.type() == QgsMapLayer.VectorLayer):
            self._layerId = layer.id()
            self.setEnabled(True)
            self._avoidAction.setEnabled(layer.geometryType() == QGis.Polygon)
            self.updateButton()

    def updateButton(self):
        """Updates the button with the current snapping settings."""
        if (self._layerId == ''):
            return
        ok, self._snapEnabled, self._snappingType, self._unitType, self._tolerance, self._avoidIntersections = self._project.snapSettingsForLayer(self._layerId)
        self._refreshButton()

    def disableButton(self):
        """Disables the button and unlinks from the layer."""
        self.setLayer(None)

    # Private API

    def _updateSnapSettings(self):
        self._project.setSnapSettingsForLayer(self._layerId, self._snapEnabled, self._snappingType, self._unitType, self._tolerance, self._avoidIntersections)
        self._refreshButton()
        self.snapSettingsChanged.emit(self._layerId, self._snapEnabled, self._snappingType, self._unitType, self._tolerance, self._avoidIntersections)

    def _refreshButton(self):

        self.setChecked(self._snapEnabled)

        if (self._snappingType == QgsSnapper.SnapToVertex):
            self.setIcon(self._vertexIcon)
            self._vertexAction.setChecked(True)
        elif (self._snappingType == QgsSnapper.SnapToSegment):
            self.setIcon(self._segmentIcon)
            self._segmentAction.setChecked(True)
        elif (self._snappingType == QgsSnapper.SnapToVertexAndSegment):
            self.setIcon(self._vertexSegmentIcon)
            self._vertexSegmentAction.setChecked(True)

        if (self._unitType == QgsTolerance.Pixels):
            self._pixelUnitsAction.setChecked(True)
            self._toleranceSpin.setSuffix(' px')
        else:
            self._mapUnitsAction.setChecked(True)
            self._toleranceSpin.setSuffix(' mu')

        self._toleranceSpin.setValue(self._tolerance)

        self._avoidAction.setChecked(self._avoidIntersections)

    def _snapToggled(self, _snapEnabled):
        self._snapEnabled = bool(_snapEnabled)
        self._updateSnapSettings()

    def _snapToVertex(self):
        self._snappingType = QgsSnapper.SnapToVertex
        self._updateSnapSettings()

    def _snapToSegment(self):
        self._snappingType = QgsSnapper.SnapToSegment
        self._updateSnapSettings()

    def _snapToVertexSegment(self):
        self._snappingType = QgsSnapper.SnapToVertexAndSegment
        self._updateSnapSettings()

    def _usePixelUnits(self):
        self._unitType = QgsTolerance.Pixels
        self._updateSnapSettings()

    def _useMapUnits(self):
        self._unitType = QgsTolerance.MapUnits
        self._updateSnapSettings()

    def _toleranceChanged(self, _tolerance):
        self._tolerance = _tolerance
        self._updateSnapSettings()

    def _avoidToggled(self, status):
        self._avoidIntersections = status
        self._updateSnapSettings()


class TopoEditToolButton(QToolButton):

    """Tool Button to toggle topological editing for a project

    Signals:
        topologicalEditingChanged(bool): Signal that topological editing has been changed by the button
    """

    topologicalEditingChanged = pyqtSignal(bool)

    def __init__(self, parent=None):
        """Initialises the topological editing tool button

        Args:
            parent (QWidget): The parent widget, defaults to None.
        """

        QToolButton.__init__(self, parent)

        self._project = QgsProject.instance()

        self._refreshButton()
        self.toggled.connect(self._topoToggled)
        self.toggled.connect(self.topologicalEditingChanged)

        # Make sure we catch changes in the main snapping dialog
        self._project.snapSettingsChanged.connect(self._refreshButton)
        # If a new _project is read, update to that _project's setting
        self._project.readProject.connect(self._refreshButton)

    # Private API

    def _topoToggled(self, status):
        self._project.setTopologicalEditing(status)

    def _refreshButton(self):
        self.setChecked(self._project.topologicalEditing())
