# -*- coding: utf-8 -*-
"""
/***************************************************************************
 ArkPlan
                                 A QGIS plugin
 Plugin to assist in digitising of Archaeological plans.
                              -------------------
        begin                : 2014-12-07
        git sha              : $Format:%H$
        copyright            : (C) 2014 by John Layt
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
from PyQt4.QtCore import Qt, pyqtSignal, QSettings
from PyQt4.QtGui import QInputDialog, QColor

from qgis.core import *
from qgis.gui import QgsMapTool

class LevelsMapTool(QgsMapTool):

    levelAdded = pyqtSignal(QgsPoint, 'QString', float)

    featureAdded = pyqtSignal(list, QGis.GeometryType, 'QString')

    featureType = ''

    def __init__(self, canvas, type='lvl'):
        QgsMapTool.__init__(self, canvas)

    def featureType(self):
        return self.featureType

    def setType(self, featureType):
        self.featureType = featureType

    def canvasPressEvent(self, e):
        if e.button() != Qt.LeftButton:
            return
        elevation, ok = QInputDialog.getDouble(None, 'Add Level', 'Please enter the elevation in meters (m):',
                                               0, -100, 100, 2)
        if ok:
            point = self.toMapCoordinates(e.pos())
            self.levelAdded.emit(point, self.featureType, elevation)
