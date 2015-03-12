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

from PyQt4 import uic
from PyQt4.QtCore import Qt, pyqtSignal

from qgis.core import *

from ..core.dock import *

import grid_dock_base


class GridDock(QgsDockWidget, grid_dock_base.Ui_GridDock):

    convertCrsSelected = pyqtSignal()
    convertLocalSelected = pyqtSignal()

    def __init__(self, parent=None):
        super(GridDock, self).__init__(parent)
        self.setupUi(self)

        self.crsEastingSpin.editingFinished.connect(self.convertCrsSelected)
        self.crsNorthingSpin.editingFinished.connect(self.convertCrsSelected)

        self.localEastingSpin.editingFinished.connect(self.convertLocalSelected)
        self.localNorthingSpin.editingFinished.connect(self.convertLocalSelected)


    def crsPoint(self):
        return QgsPoint(self.crsEastingSpin.value(), self.crsNorthingSpin.value())


    def setCrsPoint(self, point):
        self.crsEastingSpin.setValue(point.x())
        self.crsNorthingSpin.setValue(point.y())


    def localPoint(self):
        return QgsPoint(self.localEastingSpin.value(), self.localNorthingSpin.value())


    def setLocalPoint(self, point):
        self.localEastingSpin.setValue(point.x())
        self.localNorthingSpin.setValue(point.y())


    def setReadOnly(self, status):
        self.crsEastingSpin.setReadOnly(status)
        self.crsNorthingSpin.setReadOnly(status)
        self.localEastingSpin.setReadOnly(status)
        self.localNorthingSpin.setReadOnly(status)
