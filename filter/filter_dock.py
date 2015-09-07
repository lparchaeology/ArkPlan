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
from PyQt4.QtCore import Qt, pyqtSignal, QSize
from PyQt4.QtGui import QListWidgetItem, QLabel

from ..libarkqgis.dock import ArkDockWidget

import filter_dock_base
from filter_widget import FilterWidget

class FilterDock(ArkDockWidget, filter_dock_base.Ui_FilterDock):

    filterChanged = pyqtSignal()

    buildFilterSelected = pyqtSignal()
    buildSelectionSelected = pyqtSignal()
    clearFilterSelected = pyqtSignal()
    zoomFilterSelected = pyqtSignal()
    loadDataSelected = pyqtSignal()
    showDataSelected = pyqtSignal()

    newFilterWidget = None  # FilterWidget()
    _filterIndex = 0
    _filters = {}
    _items = {}
    _classCodes = {}

    def __init__(self, parent=None):
        super(FilterDock, self).__init__(parent)
        self.setupUi(self)

        self.zoomFilterAction.triggered.connect(self.zoomFilterSelected)
        self.zoomFilterTool.setDefaultAction(self.zoomFilterAction)

        self.buildFilterAction.triggered.connect(self.buildFilterSelected)
        self.buildFilterTool.setDefaultAction(self.buildFilterAction)

        self.buildSelectionAction.triggered.connect(self.buildSelectionSelected)
        self.buildSelectionTool.setDefaultAction(self.buildSelectionAction)

        self.clearFilterAction.triggered.connect(self._clearFilterClicked)
        self.clearFilterTool.setDefaultAction(self.clearFilterAction)

        self.loadDataAction.triggered.connect(self.loadDataSelected)
        self.loadDataTool.setDefaultAction(self.loadDataAction)
        self.loadDataTool.setHidden(True)

        self.showDataAction.triggered.connect(self.showDataSelected)
        self.showDataTool.setDefaultAction(self.showDataAction)
        self.showDataTool.setHidden(True)

        self._createNewFilterWidget()

    def _addFilter(self):
        self.newFilterWidget.filterAdded.disconnect(self._addFilter)
        self.newFilterWidget.setIndex(self._filterIndex)
        self._filters[self._filterIndex] = self.newFilterWidget
        self.newFilterWidget.filterRemoved.connect(self._removeFilter)
        self.newFilterWidget.filterChanged.connect(self.filterChanged)
        newItem = QListWidgetItem()
        newItem.setData(Qt.UserRole, self._filterIndex)
        newItem.setSizeHint(self.newFilterWidget.minimumSizeHint())
        self.filterListWidget.addItem(newItem);
        self.filterListWidget.setItemWidget(newItem, self.newFilterWidget)
        self._items[self._filterIndex] = newItem
        self._filterIndex += 1
        self._createNewFilterWidget()
        self.filterChanged.emit()

    def _removeFilter(self, index):
        if index is None or index < 0 or self._filters[index] == None:
            return
        self.filterListWidget.takeItem(self.filterListWidget.row(self._items[index]))
        self._filters[index] = None
        self._items[index] = None
        self.filterChanged.emit()

    def _createNewFilterWidget(self):
        self.newFilterWidget = FilterWidget(self)
        self.newFilterWidget.setClassCodes(self._classCodes)
        self.newFilterWidget.filterAdded.connect(self._addFilter)
        self.newFilterFrame.layout().addWidget(self.newFilterWidget)

    def _clearFilterClicked(self):
        for index in self._filters.keys():
            self._removeFilter(index)
        self.clearFilterSelected.emit()

    def setSiteCodes(self, siteCodes):
        for site in siteCodes:
            self.siteCodeCombo.addItem(site)

    def siteCode(self):
        return self.siteCodeCombo.currentText()

    def setClassCodes(self, classCodes):
        self._classCodes = classCodes
        self.newFilterWidget.setClassCodes(classCodes)

    def activeFilters(self):
        return self._filters
