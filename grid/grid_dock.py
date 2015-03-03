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

from ..core.dock import *

import grid_dock_base


class GridDock(QgsDockWidget, grid_dock_base.Ui_GridDock):

    mapToolSelected = pyqtSignal()
    enterCrsSelected = pyqtSignal()
    enterLocalSelected = pyqtSignal()

    def __init__(self, parent=None):
        super(GridDock, self).__init__(parent)
        self.setupUi(self)

        self.mapToolButton.clicked.connect(self.mapToolClicked)
        self.mapToolButton.clicked.connect(self.mapToolSelected)
        self.enterCrsButton.clicked.connect(self.enterCrsClicked)
        self.enterCrsButton.clicked.connect(self.enterCrsSelected)
        self.enterLocalButton.clicked.connect(self.enterLocalClicked)
        self.enterLocalButton.clicked.connect(self.enterLocalSelected)


    def mapToolClicked(self):
        self.crsEastingSpin.setReadOnly(True)
        self.crsNorthingSpin.setReadOnly(True)
        self.localEastingSpin.setReadOnly(True)
        self.localNorthingSpin.setReadOnly(True)


    def enterCrsClicked(self):
        self.crsEastingSpin.setReadOnly(False)
        self.crsNorthingSpin.setReadOnly(False)
        self.localEastingSpin.setReadOnly(True)
        self.localNorthingSpin.setReadOnly(True)


    def enterLocalClicked(self):
        self.crsEastingSpin.setReadOnly(True)
        self.crsNorthingSpin.setReadOnly(True)
        self.localEastingSpin.setReadOnly(False)
        self.localNorthingSpin.setReadOnly(False)
