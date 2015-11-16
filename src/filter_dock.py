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
from PyQt4.QtGui import QListWidgetItem, QLabel, QActionGroup, QMenu

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
    filterSetChanged = pyqtSignal(str)
    saveFilterSetSelected = pyqtSignal(str, str)
    deleteFilterSetSelected = pyqtSignal(str)
    exportFilterSetSelected = pyqtSignal(str, str)

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

        self.filterSetCombo.currentIndexChanged.connect(self._filterSetChanged)

        self.saveFilterSetAction.triggered.connect(self._saveFilterSetSelected)
        self.deleteFilterSetAction.triggered.connect(self._deleteFilterSetSelected)
        self.exportFilterSetAction.triggered.connect(self._exportFilterSetSelected)
        self._filterSetActionGroup = QActionGroup(self)
        self._filterSetActionGroup.addAction(self.saveFilterSetAction)
        self._filterSetActionGroup.addAction(self.deleteFilterSetAction)
        self._filterSetActionGroup.addAction(self.exportFilterSetAction)
        self._filterSetMenu = QMenu(self)
        self._filterSetMenu.addActions(self._filterSetActionGroup.actions())
        self.filterSetTool.setMenu(self._filterSetMenu)
        self.filterSetTool.setDefaultAction(self.saveFilterSetAction)

        self._createNewFilterWidget()

    def _currentFilterSetKey(self):
        return self.filterSetCombo.itemData(self.filterSetCombo.currentIndex())

    def _currentFilterSetName(self):
        return self.filterSetCombo.currentText()

    def _saveFilterSetSelected(self):
        self.saveFilterSetSelected.emit(self._currentFilterSetKey(), self._currentFilterSetName())

    def _deleteFilterSetSelected(self):
        self.deleteFilterSetSelected.emit(self._currentFilterSetKey())

    def _exportFilterSetSelected(self):
        self.exportFilterSetSelected.emit(self._currentFilterSetKey(), self._currentFilterSetName())

    def addFilter(self, filterType, siteCode, classCode, filterRange, filterAction):
        filterWidget = self._createFilterWidget()
        filterWidget.setFilterType(filterType)
        filterWidget.setSiteCode(siteCode)
        filterWidget.setClassCode(classCode)
        filterWidget.setFilterRange(filterRange)
        filterWidget.setFilterAction(filterAction)
        return self._addFilter(filterWidget)

    def _addNewFilter(self):
        self.newFilterWidget.filterAdded.disconnect(self._addNewFilter)
        self._addFilter(self.newFilterWidget)
        self._createNewFilterWidget()

    def _addFilter(self, filterWidget):
        idx = self._filterIndex
        filterWidget.setIndex(idx)
        self._filters[idx] = filterWidget
        filterWidget.filterRemoved.connect(self.removeFilter)
        filterWidget.filterChanged.connect(self.filterChanged)
        newItem = QListWidgetItem()
        newItem.setData(Qt.UserRole, idx)
        newItem.setSizeHint(filterWidget.minimumSizeHint())
        self.filterListWidget.addItem(newItem);
        self.filterListWidget.setItemWidget(newItem, filterWidget)
        self._items[idx] = newItem
        self._filterIndex += 1
        self.filterChanged.emit()
        return idx

    def removeFilter(self, index):
        self._removeFilter(index)
        self.filterChanged.emit()

    def _removeFilter(self, index):
        if index not in self._filters:
            return
        self.filterListWidget.takeItem(self.filterListWidget.row(self._items[index]))
        self._filters.pop(index)
        self._items.pop(index)

    def _clearFilters(self):
        for index in self._filters.keys():
            self._removeFilter(index)

    def _createNewFilterWidget(self):
        self.newFilterWidget = self._createFilterWidget()
        self.newFilterWidget.filterAdded.connect(self._addNewFilter)
        self.newFilterFrame.layout().addWidget(self.newFilterWidget)

    def _createFilterWidget(self):
        widget = FilterWidget(self)
        widget.setClassCodes(self._classCodes)
        widget.setSiteCode(self.siteCode())
        return widget

    def hasFilterType(self, filterType):
        for index in self._filters.keys():
            if self._filters[index] is not None and self._filters[index].filterType() == filterType:
                return True
        return False

    def _clearFilterClicked(self):
        for index in self._filters.keys():
            self._removeFilter(index)
        self.filterChanged.emit()
        self.clearFilterSelected.emit()

    def filterSet(self):
        return self.siteCodeCombo.currentText()

    def addFilterSet(self, key, name):
        self.filterSetCombo.addItem(name, key)

    def setFilterSet(self, key):
        self.filterSetCombo.setCurrentIndex(self.filterSetCombo.findData(key))

    def removeFilterSet(self, key):
        self.filterSetCombo.removeItem(self.filterSetCombo.findData(key))

    def _filterSetChanged(self, idx):
        self.filterSetChanged.emit(self.filterSetCombo.itemData(idx))

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

    def activeFilterSet(self):
        fs = []
        for idx in self._filters.keys():
            fs.append(self._filters[idx].settings())
        return fs

    def toSettings(self, settings):
        i = 0
        for idx in self._filters.keys():
            settings.setArrayIndex(i)
            self._filters[idx].toSettings(settings)
            i += 1

    def fromSettings(self, settings, count):
        self._clearFilters()
        for i in range(0, count):
            settings.setArrayIndex(i)
            flt = self._createFilterWidget()
            flt.fromSettings(settings)
            self._addFilter(flt)
        self.filterChanged.emit()
