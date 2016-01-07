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

    def __init__(self, parent=None):
        super(GridWidget, self).__init__(parent)
        self.setupUi(self)

class GridDock(ToolDockWidget):

    createGridSelected = pyqtSignal()
    identifyGridSelected = pyqtSignal(bool)
    updateLayerSelected = pyqtSignal()
    translateFeaturesSelected = pyqtSignal()
    panMapSelected = pyqtSignal()
    copyMapPointSelected = pyqtSignal()
    copyLocalPointSelected = pyqtSignal()
    pasteMapPointSelected = pyqtSignal()
    addMapPointSelected = pyqtSignal()
    gridSelectionChanged = pyqtSignal(str, str)
    convertMapSelected = pyqtSignal()
    convertLocalSelected = pyqtSignal()

    def __init__(self, parent=None):
        super(GridDock, self).__init__(GridWidget(), parent)

    def initGui(self, iface, location, menuAction):
        super(GridDock, self).initGui(iface, location, menuAction)

        self._createGridAction = self.toolbar.addAction(QIcon(':/plugins/ark/grid/newGrid.png'), 'Create New Grid', self.createGridSelected)
        self._identifyGridAction = self.toolbar.addAction(QIcon(':/plugins/ark/grid/identifyCoordinates.png'), 'Identify Grid Coordinates', self.identifyGridSelected)
        self._identifyGridAction.setCheckable(True)
        self._panToAction = self.toolbar.addAction(QIcon(':/plugins/ark/grid/panToSelected.svg'), 'Pan to map point', self.panMapSelected)
        self._pasteMapPointAction = self.toolbar.addAction(QIcon(':/plugins/ark/grid/pastePoint.png'), 'Paste Map Point', self.pasteMapPointSelected)
        self._addMapPointAction = self.toolbar.addAction(QIcon(':/plugins/ark/grid/addPoint.png'), 'Add point to current layer', self.addMapPointSelected)
        self._updateLayerAction = self.toolbar.addAction(QIcon(':/plugins/ark/grid/updateLayer.png'), 'Update Layer Coordinates', self.updateLayerSelected)
        self._translateFeaturesAction = self.toolbar.addAction(QIcon(':/plugins/ark/grid/translateFeature.png'), 'Translate features', self.translateFeaturesSelected)

        self.widget.gridCombo.activated.connect(self.gridComboChanged)
        self.widget.mapEastingSpin.editingFinished.connect(self.convertMapSelected)
        self.widget.mapNorthingSpin.editingFinished.connect(self.convertMapSelected)
        self.widget.copyMapPointAction.triggered.connect(self.copyMapPointSelected)
        self.widget.localEastingSpin.editingFinished.connect(self.convertLocalSelected)
        self.widget.localNorthingSpin.editingFinished.connect(self.convertLocalSelected)
        self.widget.copyLocalPointAction.triggered.connect(self.copyLocalPointSelected)

    def siteCode(self):
        data = self.widget.gridCombo.itemData(self.widget.gridCombo.currentIndex())
        if data is not None:
            return data[0]
        else:
            return ''

    def gridName(self):
        data = self.widget.gridCombo.itemData(self.widget.gridCombo.currentIndex())
        if data is not None:
            return data[1]
        else:
            return ''

    def setGridNames(self, names):
        self.widget.gridCombo.clear()
        for name in names:
            self.widget.gridCombo.addItem(name[0] + ' / ' + name[1], name)

    def gridComboChanged(self, i):
        data = self.widget.gridCombo.itemData(i)
        self.gridSelectionChanged.emit(data[0], data[1])

    def mapPoint(self):
        return QgsPoint(self.widget.mapEastingSpin.value(), self.widget.mapNorthingSpin.value())

    def setMapPoint(self, point):
        self.widget.mapEastingSpin.setValue(point.x())
        self.widget.mapNorthingSpin.setValue(point.y())

    def localPoint(self):
        return QgsPoint(self.widget.localEastingSpin.value(), self.widget.localNorthingSpin.value())

    def setLocalPoint(self, point):
        self.widget.localEastingSpin.setValue(point.x())
        self.widget.localNorthingSpin.setValue(point.y())

    def setReadOnly(self, status):
        self._identifyGridAction.setEnabled(not status)
        self._updateLayerAction.setEnabled(not status)
        self._translateFeaturesAction.setEnabled(not status)
        self._panToAction.setEnabled(not status)
        self.widget.copyMapPointAction.setEnabled(not status)
        self.widget.copyLocalPointAction.setEnabled(not status)
        self._pasteMapPointAction.setEnabled(not status)
        self._addMapPointAction.setEnabled(not status)
        self.widget.gridCombo.setEnabled(not status)
        self.widget.mapEastingSpin.setReadOnly(status)
        self.widget.mapNorthingSpin.setReadOnly(status)
        self.widget.localEastingSpin.setReadOnly(status)
        self.widget.localNorthingSpin.setReadOnly(status)
