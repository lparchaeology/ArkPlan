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

from PyQt4.QtCore import QSettings

from qgis.core import QgsProject

from ..project import Project


class Snapping():

    """Project snapping settings utilities."""

    """SnappingMode."""
    CurrentLayer = 0
    AllLayers = 1
    SelectedLayers = 2

    """SnappingType == QgsSnapper.SnappingType, plus Off, keep values the same."""
    Vertex = 0
    Segment = 1
    VertexAndSegment = 2
    Off = 3

    """SnappingUnit == QgsTolerance.UnitType, keep values the same."""
    LayerUnits = 0
    Pixels = 1
    ProjectUnits = 2

    @staticmethod
    def snappingMode():
        """Snapping Mode, i.e. what snapping mode currently applies."""
        mode = Project.readEntry("Digitizing", "/SnappingMode", "current_layer")
        if mode == 'advanced':
            return Snapping.SelectedLayers
        elif mode == 'all_layers':
            return Snapping.AllLayers
        else:
            return Snapping.CurrentLayer

    @staticmethod
    def setSnappingMode(mode):
        if mode == Snapping.SelectedLayers:
            Snapping._setSnappingMode('advanced')
        elif mode == Snapping.AllLayers:
            Snapping._setSnappingMode('all_layers')
        elif mode == Snapping.CurrentLayer:
            Snapping._setSnappingMode('current_layer')

    @staticmethod
    def _setSnappingMode(mode='current_layer'):
        return Project.writeEntry("Digitizing", "/SnappingMode", mode)

    @staticmethod
    def defaultSnappingType(defaultValue=Off):
        """Default Snapping Type, i.e. the system-wdie default."""
        defaultValue = Snapping._toDefaultSnapType(defaultValue)
        value = QSettings().value('/qgis/digitizing/default_snap_mode', defaultValue, str)
        return Snapping._fromSnapType(value)

    @staticmethod
    def setDefaultSnappingType(snapType=Off):
        snapType = Snapping._toDefaultSnapType(snapType)
        return QSettings().setValue('/qgis/digitizing/default_snap_mode', snapType, str)

    @staticmethod
    def _toDefaultSnapType(val):
        if val == Snapping.Off or val == 'off':
            return 'off'
        elif val == Snapping.Vertex or val == 'to_vertex':
            return 'to vertex'
        elif val == Snapping.Segment or val == 'to_segment':
            return 'to segment'
        elif val == Snapping.VertexAndSegment or val == 'to_vertex_and_segment':
            return 'to vertex and segment'
        return 'off'

    @staticmethod
    def projectSnappingType(defaultValue=Off):
        """Project Snapping Type, i.e. when snapping mode is CurrentLayer or AllLayers."""
        defaultValue = Snapping.defaultSnappingType(defaultValue)
        value = Project.readEntry("Digitizing", "/DefaultSnapType", Snapping._toDefaultSnapType(defaultValue))
        return Snapping._fromSnapType(value)

    @staticmethod
    def setProjectSnappingType(snapType=Off):
        return Project.writeEntry("Digitizing", "/DefaultSnapType", Snapping._toDefaultSnapType(snapType))

    @staticmethod
    def _fromSnapType(value):
        if value == 'off':
            return Snapping.Off
        elif value == 'to_vertex' or value == 'to vertex':
            return Snapping.Vertex
        elif value == 'to_segment' or value == 'to segment':
            return Snapping.Segment
        elif value == 'to_vertex_and_segment' or value == 'to vertex and segment':
            return Snapping.VertexAndSegment
        return Snapping.Off

    @staticmethod
    def _toSnapType(val):
        if val == Snapping.Off:
            return 'off'
        elif val == Snapping.Vertex:
            return 'to_vertex'
        elif val == Snapping.Segment:
            return 'to_segment'
        elif val == Snapping.VertexAndSegment:
            return 'to_vertex_and_segment'
        return 'off'

    @staticmethod
    def defaultSnappingUnit(defaultValue=ProjectUnits):
        """Default Snapping Unit, i.e. the system-wide default."""
        unit = QSettings().value('/qgis/digitizing/default_snapping_tolerance_unit', defaultValue, int)
        # FIXME Sometimes None gets returned even though we give a valid default?
        if unit is None:
            unit = defaultValue
        return unit

    def setDefaultSnappingUnit(unit=ProjectUnits):
        return QSettings().setValue('/qgis/digitizing/default_snapping_tolerance_unit', unit, int)

    @staticmethod
    def projectSnappingUnit(defaultValue=ProjectUnits):
        """Project Snapping Unit, i.e. when snapping mode is CurrentLayer or AllLayers."""
        defaultValue = Snapping.defaultSnappingUnit(defaultValue)
        return Project.readNumEntry("Digitizing", "/DefaultSnapToleranceUnit", defaultValue)

    @staticmethod
    def setProjectSnappingUnit(unit=ProjectUnits):
        return Project.writeEntry("Digitizing", "/DefaultSnapToleranceUnit", unit)

    @staticmethod
    def defaultSnappingTolerance(defaultValue=0.0):
        """Default Snapping Tolerance, i.e. the system-wide default."""
        tolerance = QSettings().value('/qgis/digitizing/default_snapping_tolerance', defaultValue, float)
        # FIXME Sometimes None gets returned even though we give a valid default?
        if tolerance is None:
            tolerance = defaultValue
        return tolerance

    @staticmethod
    def setDefaultSnappingTolerance(tolerance=0.0):
        return QSettings().setValue('/qgis/digitizing/default_snapping_tolerance', tolerance, float)

    @staticmethod
    def projectSnappingTolerance(defaultValue=0.0):
        """Project Snapping Tolerance, i.e. when snapping mode is CurrentLayer or AllLayers."""
        defaultValue = Snapping.defaultSnappingTolerance(defaultValue)
        return Project.readDoubleEntry("Digitizing", "/DefaultSnapTolerance", defaultValue)

    @staticmethod
    def setProjectSnappingTolerance(tolerance=0.0):
        return Project.writeEntry("Digitizing", "/DefaultSnapTolerance", tolerance)

    @staticmethod
    def topologicalEditing():
        """Topological Editing, i.e. the system-wide setting."""
        return QgsProject.instance().topologicalEditing()

    @staticmethod
    def setTopologicalEditing(enabled=True):
        return QgsProject.instance().setTopologicalEditing(enabled)

    @staticmethod
    def intersectionSnapping(defaultValue=True):
        """Intersection Snapping, i.e. the system-wide setting."""
        res = Project.readNumEntry("Digitizing", "/IntersectionSnapping", int(defaultValue))
        return bool(res)

    @staticmethod
    def setIntersectionSnapping(enabled=True):
        return Project.writeEntry("Digitizing", "/IntersectionSnapping", int(enabled))

    @staticmethod
    def intersectionLayers(defaultValue=[]):
        """Intersection Layers, i.e. the system-wide setting."""
        return Project.readListEntry("Digitizing", "/AvoidIntersectionsList", defaultValue)

    @staticmethod
    def snapSettingsForLayer(layerId):
        """Selected Layer Snapping, i.e when snapping mode is SelectedLayers."""
        return QgsProject.instance().snapSettingsForLayer(layerId)

    @staticmethod
    def setSnapSettingsForLayer(layerId, enabled, snapType, units, tolerance, avoidIntersections):
        return QgsProject.instance().setSnapSettingsForLayer(layerId,
                                                             enabled,
                                                             snapType,
                                                             units,
                                                             tolerance,
                                                             avoidIntersections)

    @staticmethod
    def layerSnappingEnabled(layerId):
        value = Snapping._layerSnappingValue(layerId, "/LayerSnappingEnabledList", u'disabled')
        return (value == u'enabled')

    @staticmethod
    def setLayerSnappingEnabled(layerId, enabled):
        value = u'disabled'
        if enabled:
            value = u'enabled'
        Snapping._setLayerSnappingValue(layerId, "/LayerSnappingEnabledList", value)

    @staticmethod
    def layerSnappingType(layerId):
        value = Snapping._layerSnappingValue(layerId, "/LayerSnapToList", Snapping.Vertex)
        return Snapping._fromSnapType(value)

    @staticmethod
    def setLayerSnappingType(layerId, snapType):
        Snapping._setLayerSnappingValue(layerId, "/LayerSnapToList", Snapping._toSnapType(snapType))

    @staticmethod
    def layerSnappingUnit(layerId):
        return int(Snapping._layerSnappingValue(layerId, "/LayerSnappingToleranceUnitList", Snapping.Pixels))

    @staticmethod
    def setLayerSnappingUnit(layerId, snapUnit):
        Snapping._setLayerSnappingValue(layerId, "/LayerSnappingToleranceUnitList", snapUnit)

    @staticmethod
    def layerSnappingTolerance(layerId):
        return float(Snapping._layerSnappingValue(layerId, "/LayerSnappingToleranceList", 0.0))

    @staticmethod
    def setLayerSnappingTolerance(layerId, tolerance):
        Snapping._setLayerSnappingValue(layerId, "/LayerSnappingToleranceList", tolerance)

    @staticmethod
    def layerSnappingAvoidIntersections(layerId):
        layerIdList = Project.readListEntry("Digitizing", "/AvoidIntersectionsList")
        try:
            idx = layerIdList.index(layerId)
            return True
        except Exception:
            return False

    @staticmethod
    def setLayerSnappingAvoidIntersections(layerId, avoid):
        layerIdList = Project.readListEntry("Digitizing", "/AvoidIntersectionsList")
        try:
            idx = layerIdList.index(layerId)
            if not avoid:
                layerIdList.pop(idx)
        except Exception:
            if avoid:
                layerIdList.append(layerId)
        Project.writeEntry("Digitizing", "/AvoidIntersectionsList", layerIdList)

    @staticmethod
    def _layerSnappingValue(layerId, layerListId, defaultValue):
        if not layerId:
            return defaultValue
        layerIdList = Project.readListEntry("Digitizing", "/LayerSnappingList")
        valueList = Project.readListEntry("Digitizing", layerListId)
        try:
            idx = layerIdList.index(layerId)
            return valueList[idx]
        except Exception:
            return defaultValue

    @staticmethod
    def _setLayerSnappingValue(layerId, layerListId, value):
        if not layerId:
            return
        layerIdList = Project.readListEntry("Digitizing", "/LayerSnappingList")
        valueList = Project.readListEntry("Digitizing", layerListId)
        try:
            idx = layerIdList.index(layerId)
            valueList[idx] = str(value)
            Project.writeEntry("Digitizing", layerListId, valueList)
        except Exception:
            pass

    @staticmethod
    def layerSnappingEnabledLayers():
        enabledLayers = []
        layerIdList = Project.readListEntry("Digitizing", "/LayerSnappingList")
        enabledList = Project.readListEntry("Digitizing", "/LayerSnappingEnabledList")
        for idx in range(0, len(layerIdList)):
            if enabledList[idx] == u'enabled':
                enabledLayers.append(layerIdList[idx])
        return enabledLayers

    @staticmethod
    def setLayerSnappingEnabledLayers(enabledLayers):
        enabledList = []
        layerIdList = Project.readListEntry("Digitizing", "/LayerSnappingList")
        for layerId in layerIdList:
            if layerId in enabledLayers:
                enabledList.append(u'enabled')
            else:
                enabledList.append(u'disabled')
        Project.writeEntry("Digitizing", "/LayerSnappingEnabledList", enabledList)
