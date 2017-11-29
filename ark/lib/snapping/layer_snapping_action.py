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

from PyQt4.QtCore import pyqtSignal
from PyQt4.QtGui import QActionGroup

from qgis.core import QGis, QgsMapLayer, QgsMapLayerRegistry, QgsProject, QgsVectorLayer
from qgis.gui import QgisInterface

from ..gui import ControlMenu
from .layer_snapping_avoid_intersection_action import LayerSnappingAvoidIntersectionsAction
from .layer_snapping_enabled_action import LayerSnappingEnabledAction
from .layer_snapping_tolerance_action import LayerSnappingToleranceAction
from .layer_snapping_type_action import LayerSnappingTypeAction
from .layer_snapping_unit_action import LayerSnappingUnitAction
from .snapping_ import Snapping


class LayerSnappingAction(LayerSnappingEnabledAction):

    """Action to change snapping settings for a QGIS vector layer."""

    snapSettingsChanged = pyqtSignal(str)

    _toleranceAction = None  # LayerSnappingToleranceAction()
    _avoidAction = None  # LayerSnappingAvoidIntersectionsAction()

    def __init__(self, snapLayer, parent=None):
        super(LayerSnappingAction, self).__init__(snapLayer, parent)

        self._vertexAction = LayerSnappingTypeAction(snapLayer, Snapping.Vertex, self)
        self._segmentAction = LayerSnappingTypeAction(snapLayer, Snapping.Segment, self)
        self._vertexSegmentAction = LayerSnappingTypeAction(snapLayer, Snapping.VertexAndSegment, self)

        self._snappingTypeActionGroup = QActionGroup(self)
        self._snappingTypeActionGroup.addAction(self._vertexAction)
        self._snappingTypeActionGroup.addAction(self._segmentAction)
        self._snappingTypeActionGroup.addAction(self._vertexSegmentAction)

        self._toleranceAction = LayerSnappingToleranceAction(snapLayer, parent)

        self._pixelUnitsAction = LayerSnappingUnitAction(snapLayer, Snapping.Pixels, self)
        self._layerUnitsAction = LayerSnappingUnitAction(snapLayer, Snapping.LayerUnits, self)
        self._projectUnitsAction = LayerSnappingUnitAction(snapLayer, Snapping.ProjectUnits, self)

        self._unitTypeActionGroup = QActionGroup(self)
        self._unitTypeActionGroup.addAction(self._pixelUnitsAction)
        self._unitTypeActionGroup.addAction(self._layerUnitsAction)
        self._unitTypeActionGroup.addAction(self._projectUnitsAction)

        menu = ControlMenu(parent)
        menu.addActions(self._snappingTypeActionGroup.actions())
        menu.addSeparator()
        menu.addAction(self._toleranceAction)
        menu.addActions(self._unitTypeActionGroup.actions())
        if (isinstance(snapLayer, QgisInterface)
                or (isinstance(snapLayer, QgsVectorLayer) and snapLayer.geometryType() == QGis.Polygon)):
            self._avoidAction = LayerSnappingAvoidIntersectionsAction(snapLayer, self)
            menu.addSeparator()
            menu.addAction(self._avoidAction)
        self.setMenu(menu)

        self._refreshAction()

        # Make sure we catch changes in the main snapping dialog
        QgsProject.instance().snapSettingsChanged.connect(self._refreshAction)
        # If using current layer, make sure we update when it changes
        if self._iface:
            self._iface.legendInterface().currentLayerChanged.connect(self._refreshAction)
        # If any of the settings change then signal, but don't tell project as actions already have
        self.snappingEnabledChanged.connect(self.snapSettingsChanged)
        self._vertexAction.snappingTypeChanged.connect(self.snapSettingsChanged)
        self._segmentAction.snappingTypeChanged.connect(self.snapSettingsChanged)
        self._vertexSegmentAction.snappingTypeChanged.connect(self.snapSettingsChanged)
        self._toleranceAction.snappingToleranceChanged.connect(self.snapSettingsChanged)
        self._pixelUnitsAction.snappingUnitChanged.connect(self.snapSettingsChanged)
        self._layerUnitsAction.snappingUnitChanged.connect(self.snapSettingsChanged)
        self._projectUnitsAction.snappingUnitChanged.connect(self.snapSettingsChanged)
        if self._avoidAction:
            self._avoidAction.avoidIntersectionsChanged.connect(self.snapSettingsChanged)

    def setInterface(self, iface):
        self._toleranceAction.setInterface(iface)

    def unload(self):
        if not self._layerId:
            return
        super(LayerSnappingAction, self).unload()
        QgsProject.instance().snapSettingsChanged.disconnect(self._refreshAction)
        self.snappingEnabledChanged.disconnect(self.snapSettingsChanged)
        self._vertexAction.snappingTypeChanged.disconnect(self.snapSettingsChanged)
        self._segmentAction.snappingTypeChanged.disconnect(self.snapSettingsChanged)
        self._vertexSegmentAction.snappingTypeChanged.disconnect(self.snapSettingsChanged)
        self._toleranceAction.snappingToleranceChanged.disconnect(self.snapSettingsChanged)
        self._pixelUnitsAction.snappingUnitChanged.disconnect(self.snapSettingsChanged)
        self._layerUnitsAction.snappingUnitChanged.disconnect(self.snapSettingsChanged)
        self._projectUnitsAction.snappingUnitChanged.disconnect(self.snapSettingsChanged)
        if self._avoidAction:
            self._avoidAction.avoidIntersectionsChanged.disconnect(self.snapSettingsChanged)
        self._vertexAction.unload()
        self._segmentAction.unload()
        self._vertexSegmentAction.unload()
        self._toleranceAction.unload()
        self._pixelUnitsAction.unload()
        self._layerUnitsAction.unload()
        self._projectUnitsAction.unload()

    # Private API

    def _refreshAction(self):
        if (self._segmentAction.isChecked()):
            self.setIcon(self._segmentAction.icon())
        elif (self._vertexSegmentAction.isChecked()):
            self.setIcon(self._vertexSegmentAction.icon())
        else:  # Snapping.Vertex or undefined
            self.setIcon(self._vertexAction.icon())
        if self._iface and self._avoidAction:
            layer = QgsMapLayerRegistry.instance().mapLayer(self.layerId())
            isPolygon = (layer is not None and layer.type() ==
                         QgsMapLayer.VectorLayer and layer.geometryType() == QGis.Polygon)
            self._avoidAction.setEnabled(isPolygon)
