# -*- coding: utf-8 -*-
"""
/***************************************************************************
                                ARK QGIS
                        A QGIS utilities library.
        Part of the Archaeological Recording Kit by L-P : Archaeology
                        http://ark.lparchaeology.com
                              -------------------
        copyright            : 2017 by L-P : Heritage LLP
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
import ..utils

# Project setting utilities

class Snapping():

    # SnappingMode
    CurrentLayer = 0
    AllLayers = 1
    SelectedLayers = 2

    # SnappingType == QgsSnapper.SnappingType, plus Off, keep values the same
    Vertex = 0
    Segment = 1
    VertexAndSegment = 2
    Off = 3

    # SnappingUnit == QgsTolerance.UnitType, keep values the same
    LayerUnits = 0
    Pixels = 1
    ProjectUnits = 2

    # Snapping Mode, i.e. what snapping mode currently applies

    @staticmethod
    def snappingMode():
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
        return Project.writeEntry("Digitizing", "/SnappingMode", mode);

    # Default Snapping Type, i.e. the system-wdie default

    @staticmethod
    def defaultSnappingType(defaultValue=Off):
        defaultValue = Snapping._toDefaultSnapType(defaultValue)
        value = QSettings().value('/qgis/digitizing/default_snap_mode', defaultValue , str)
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

    # Project Snapping Type, i.e. when snapping mode is CurrentLayer or AllLayers

    @staticmethod
    def projectSnappingType(defaultValue=Off):
        defaultValue = Snapping.defaultSnappingType(defaultValue)
        value = Project.readEntry("Digitizing", "/DefaultSnapType", Snapping._toDefaultSnapType(defaultValue));
        return Snapping._fromSnapType(value)

    @staticmethod
    def setProjectSnappingType(snapType=Off):
        return Project.writeEntry("Digitizing", "/DefaultSnapType", Snapping._toDefaultSnapType(snapType));

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

    # Default Snapping Unit, i.e. the system-wide default

    @staticmethod
    def defaultSnappingUnit(defaultValue=ProjectUnits):
        unit = QSettings().value('/qgis/digitizing/default_snapping_tolerance_unit', defaultValue, int)
        # FIXME Sometimes None gets returned even though we give a valid default?
        if unit is None:
            unit = defaultValue
        return unit

    def setDefaultSnappingUnit(unit=ProjectUnits):
        return QSettings().setValue('/qgis/digitizing/default_snapping_tolerance_unit', unit, int)

    # Project Snapping Unit, i.e. when snapping mode is CurrentLayer or AllLayers

    @staticmethod
    def projectSnappingUnit(defaultValue=ProjectUnits):
        defaultValue = Snapping.defaultSnappingUnit(defaultValue)
        return Project.readNumEntry("Digitizing", "/DefaultSnapToleranceUnit", defaultValue)

    @staticmethod
    def setProjectSnappingUnit(unit=ProjectUnits):
        return Project.writeEntry("Digitizing", "/DefaultSnapToleranceUnit", unit)

    # Default Snapping Tolerance, i.e. the system-wide default

    @staticmethod
    def defaultSnappingTolerance(defaultValue=0.0):
        tolerance = QSettings().value('/qgis/digitizing/default_snapping_tolerance', defaultValue, float)
        # FIXME Sometimes None gets returned even though we give a valid default?
        if tolerance is None:
            tolerance = defaultValue
        return tolerance

    @staticmethod
    def setDefaultSnappingTolerance(tolerance=0.0):
        return QSettings().setValue('/qgis/digitizing/default_snapping_tolerance', tolerance, float)

    # Project Snapping Tolerance, i.e. when snapping mode is CurrentLayer or AllLayers

    @staticmethod
    def projectSnappingTolerance(defaultValue=0.0):
        defaultValue = Snapping.defaultSnappingTolerance(defaultValue)
        return Project.readDoubleEntry("Digitizing", "/DefaultSnapTolerance", defaultValue)

    @staticmethod
    def setProjectSnappingTolerance(tolerance=0.0):
        return Project.writeEntry("Digitizing", "/DefaultSnapTolerance", tolerance)

    # Topological Editing, i.e. the system-wide setting

    @staticmethod
    def topologicalEditing():
        return QgsProject.instance().topologicalEditing()

    @staticmethod
    def setTopologicalEditing(enabled=True):
        return QgsProject.instance().setTopologicalEditing(enabled)

    # Intersection Snapping, i.e. the system-wide setting

    @staticmethod
    def intersectionSnapping(defaultValue=True):
        res = Project.readNumEntry("Digitizing", "/IntersectionSnapping", int(defaultValue));
        return bool(res)

    @staticmethod
    def setIntersectionSnapping(enabled=True):
        return Project.writeEntry("Digitizing", "/IntersectionSnapping", int(enabled));

    # Intersection Layers, i.e. the system-wide setting

    @staticmethod
    def intersectionLayers(defaultValue=[]):
        return Project.readListEntry("Digitizing", "/AvoidIntersectionsList", defaultValue);

    # Selected Layer Snapping, i.e when snapping mode is SelectedLayers

    @staticmethod
    def snapSettingsForLayer(layerId):
        return QgsProject.instance().snapSettingsForLayer(layerId)

    @staticmethod
    def setSnapSettingsForLayer(layerId, enabled, snapType, units, tolerance, avoidIntersections):
        return QgsProject.instance().setSnapSettingsForLayer(layerId, enabled,snapType, units, tolerance, avoidIntersections)

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
        except:
            return False

    @staticmethod
    def setLayerSnappingAvoidIntersections(layerId, avoid):
        layerIdList = Project.readListEntry("Digitizing", "/AvoidIntersectionsList")
        try:
            idx = layerIdList.index(layerId)
            if not avoid:
                layerIdList.pop(idx)
        except:
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
        except:
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
        except:
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
