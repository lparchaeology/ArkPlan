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

from qgis.core import QgsProject, QgsSnapper, QgsMessageLog
from qgis.gui import QgsMessageBar

# Project setting utilities

def projectCrs():
    # TODO Find why this doesn't work!
    return QgsProject.instance().readEntry('SpatialRefSys', '/ProjectCRSProj4String', u'')[0]

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
