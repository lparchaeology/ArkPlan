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

    def addFilter(self, filterType, classCode, filterRange):
        filterWidget = self.createFilterWidget()
        filterWidget.setFilterType(filterType)
        filterWidget.setClassCode(classCode)
        filterWidget.setFilterRange(filterRange)
        return self._addFilter(filterWidget)

    def _addNewFilter(self):
        self.newFilterWidget.filterAdded.disconnect(self._addNewFilter)
        self._addFilter(self.newFilterWidget)
        self._createNewFilterWidget()

    def _addFilter(self, filterWidget):
        idx = self._filterIndex
        filterWidget.setIndex(idx)
        self._filters[idx] = self.newFilterWidget
        self.newFilterWidget.filterRemoved.connect(self.removeFilter)
        self.newFilterWidget.filterChanged.connect(self.filterChanged)
        newItem = QListWidgetItem()
        newItem.setData(Qt.UserRole, idx)
        newItem.setSizeHint(self.newFilterWidget.minimumSizeHint())
        self.filterListWidget.addItem(newItem);
        self.filterListWidget.setItemWidget(newItem, self.newFilterWidget)
        self._items[idx] = newItem
        self._filterIndex += 1
        self.filterChanged.emit()
        return idx

    def removeFilter(self, index):
        if index is None or index < 0 or self._filters[index] == None:
            return
        self.filterListWidget.takeItem(self.filterListWidget.row(self._items[index]))
        self._filters[index] = None
        self._items[index] = None
        self.filterChanged.emit()

    def _createNewFilterWidget(self):
        self.newFilterWidget = self._createFilterWidget()
        self.newFilterWidget.filterAdded.connect(self._addNewFilter)
        self.newFilterFrame.layout().addWidget(self.newFilterWidget)

    def _createFilterWidget(self):
        widget = FilterWidget(self)
        widget.setClassCodes(self._classCodes)
        return widget

    def hasFilterType(self, filterType):
        for index in self._filters.keys():
            if self._filters[index].filterType() == filterType:
                return True
        return False

    def _clearFilterClicked(self):
        for index in self._filters.keys():
            self.removeFilter(index)
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
