# -*- coding: utf-8 -*-
"""
/***************************************************************************
                                ARK Spatial
                    A QGIS plugin for Archaeological Recording.
        Part of the Archaeological Recording Kit by L-P : Archaeology
                        http://ark.lparchaeology.com
                              -------------------
        begin                : 2014-12-07
        git sha              : $Format:%H$
        copyright            : 2014, 2015 by L-P : Heritage LLP
        email                : ark@lparchaeology.com
        copyright            : 2014, 2015 by John Layt
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
from PyQt4.QtGui import QWidget, QIcon

from qgis.core import QgsPoint

from ..libarkqgis.dock import ToolDockWidget

import grid_widget_base

class GridWidget(QWidget, grid_widget_base.Ui_GridWidget):

    gridSelectionChanged = pyqtSignal(str, str)
    mapPointChanged = pyqtSignal()
    copyMapPointSelected = pyqtSignal()
    localPointChanged = pyqtSignal()
    copyLocalPointSelected = pyqtSignal()

    def __init__(self, parent=None):
        super(GridWidget, self).__init__(parent)

    def initGui(self):
        self.setupUi(self)
        self.copyMapPointTool.setDefaultAction(self.copyMapPointAction)
        self.copyLocalPointTool.setDefaultAction(self.copyLocalPointAction)

        self.gridCombo.activated.connect(self._gridComboChanged)
        self.mapEastingSpin.editingFinished.connect(self.mapPointChanged)
        self.mapNorthingSpin.editingFinished.connect(self.mapPointChanged)
        self.copyMapPointAction.triggered.connect(self.copyMapPointSelected)
        self.localEastingSpin.editingFinished.connect(self.localPointChanged)
        self.localNorthingSpin.editingFinished.connect(self.localPointChanged)
        self.copyLocalPointAction.triggered.connect(self.copyLocalPointSelected)

    def siteCode(self):
        data = self.gridCombo.itemData(self.gridCombo.currentIndex())
        if data is not None:
            return data[0]
        else:
            return ''

    def gridName(self):
        data = self.gridCombo.itemData(self.gridCombo.currentIndex())
        if data is not None:
            return data[1]
        else:
            return ''

    def setGrid(self, siteCode, gridName):
        for idx in range(0, self.gridCombo.count()):
            data = self.gridCombo.itemData(idx)
            if data[0] == siteCode and data[1] == gridName:
                self.gridCombo.setCurrentIndex(idx)
                self.gridSelectionChanged.emit(siteCode, gridName)
                return

    def setGridNames(self, names):
        self.gridCombo.clear()
        for name in names:
            self.gridCombo.addItem(name[0] + ' / ' + name[1], name)

    def mapPoint(self):
        return QgsPoint(self.mapEastingSpin.value(), self.mapNorthingSpin.value())

    def setMapPoint(self, point):
        self.mapEastingSpin.setValue(point.x())
        self.mapNorthingSpin.setValue(point.y())

    def localPoint(self):
        return QgsPoint(self.localEastingSpin.value(), self.localNorthingSpin.value())

    def setLocalPoint(self, point):
        self.localEastingSpin.setValue(point.x())
        self.localNorthingSpin.setValue(point.y())

    def _gridComboChanged(self, i):
        data = self.gridCombo.itemData(i)
        if data:
            self.gridSelectionChanged.emit(data[0], data[1])

class GridDock(ToolDockWidget):

    def __init__(self, parent=None):
        super(GridDock, self).__init__(GridWidget(), parent)

        self.setWindowTitle(self.tr(u'ARK Grid'))
        self.setObjectName(u'GridDock')

    def initGui(self, iface, location, menuAction):
        super(GridDock, self).initGui(iface, location, menuAction)
        self.widget.initGui()
