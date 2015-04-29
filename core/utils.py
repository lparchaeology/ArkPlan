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

import os.path

from PyQt4.QtCore import QSettings
from PyQt4.QtGui import QIcon, QAction

from qgis.core import QGis, QgsProject, QgsSnapper, QgsMessageLog, QgsMapLayerRegistry
from qgis.gui import QgsMessageBar

# Message utilities

def showMessage(iface, text, level=QgsMessageBar.INFO, duration=0):
    iface.messageBar().pushMessage(text, level, duration)

def showCriticalMessage(iface, text, duration=0):
    iface.messageBar().pushMessage(text, QgsMessageBar.CRITICAL, duration)

def showStatusMessage(iface, text):
    iface.mainWindow().statusBar().showMessage(text)

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

# Layer management utilities

def getGroupIndex(iface, groupName):
    groupIndex = -1
    i = 0
    for name in iface.legendInterface().groups():
        if (groupIndex < 0 and name == groupName):
            groupIndex = i
        i += 1
    if (groupIndex < 0):
        groupIndex = iface.legendInterface().addGroup(groupName)
    return groupIndex

def getLayerId(layerName):
    layerList = QgsMapLayerRegistry.instance().mapLayersByName(layerName)
    if (len(layerList) > 0):
        return layerList[0].id()
    return None

def wkbToMemoryType(wkbType):
    if (wkbType == QGis.WKBPoint):
        return 'point'
    elif (wkbType == QGis.WKBLineString):
        return 'linestring'
    elif (wkbType == QGis.WKBPolygon):
        return 'polygon'
    elif (wkbType == QGis.WKBMultiPoint):
        return 'multipoint'
    elif (wkbType == QGis.WKBMultiLineString):
        return 'multilinestring'
    elif (wkbType == QGis.WKBMultiPolygon):
        return 'multipolygon'
    elif (wkbType == QGis.WKBPoint25D):
        return 'point'
    elif (wkbType == QGis.WKBLineString25D):
        return 'linestring'
    elif (wkbType == QGis.WKBPolygon25D):
        return 'polygon'
    elif (wkbType == QGis.WKBMultiPoint25D):
        return 'multipoint'
    elif (wkbType == QGis.WKBMultiLineString25D):
        return 'multilinestring'
    elif (wkbType == QGis.WKBMultiPolygon25D):
        return 'multipolygon'
    return 'unknown'

