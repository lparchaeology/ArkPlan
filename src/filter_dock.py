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
from PyQt4.QtCore import Qt, pyqtSignal, QSize
from PyQt4.QtGui import QListWidgetItem, QLabel, QActionGroup, QMenu

from ..libarkqgis.dock import ArkDockWidget

import filter_dock_base
from filter_clause_widget import FilterClauseWidget, FilterType

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

    newFilterClauseWidget = None  # FilterClauseWidget()
    _filterIndex = 0
    _filterClauses = {}
    _items = {}
    _classCodes = {}

    def __init__(self, parent=None):
        super(FilterDock, self).__init__(parent)

    def initGui(self, iface, location, menuAction):
        super(FilterDock, self).initGui(iface, location, menuAction)
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

        self._createNewFilterClauseWidget()

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

    def addFilterClause(self, filterType, siteCode, classCode, filterRange, filterAction):
        filterClauseWidget = self._createFilterClauseWidget()
        filterClauseWidget.setFilterType(filterType)
        filterClauseWidget.setSiteCode(siteCode)
        filterClauseWidget.setClassCode(classCode)
        filterClauseWidget.setFilterRange(filterRange)
        filterClauseWidget.setFilterAction(filterAction)
        return self._addFilterClause(filterClauseWidget)

    def _addNewFilterClause(self):
        self.newFilterClauseWidget.filterAdded.disconnect(self._addNewFilterClause)
        self._addFilterClause(self.newFilterClauseWidget)
        self._createNewFilterClauseWidget()

    def _addFilterClause(self, filterClauseWidget):
        idx = self._filterIndex
        filterClauseWidget.setIndex(idx)
        self._filterClauses[idx] = filterClauseWidget
        filterClauseWidget.filterRemoved.connect(self.removeFilterClause)
        filterClauseWidget.filterChanged.connect(self.filterChanged)
        newItem = QListWidgetItem()
        newItem.setData(Qt.UserRole, idx)
        newItem.setSizeHint(filterClauseWidget.minimumSizeHint())
        self.filterListWidget.addItem(newItem);
        self.filterListWidget.setItemWidget(newItem, filterClauseWidget)
        self._items[idx] = newItem
        self._filterIndex += 1
        self.filterChanged.emit()
        return idx

    def removeFilters(self):
        changed = False
        for index in self._filterClauses.keys():
            self._removeFilterClause(index)
            changed = True
        if changed:
            self.filterChanged.emit()

    def removeHighlightFilters(self):
        changed = False
        for index in self._filterClauses.keys():
            if self._filterClauses[index] is not None and self._filterClauses[index].filterType() == FilterType.HighlightFilter:
                self._removeFilterClause(index)
                changed = True
        if changed:
            self.filterChanged.emit()

    def removeFilterClause(self, index):
        self._removeFilterClause(index)
        self.filterChanged.emit()

    def _removeFilterClause(self, index):
        if index not in self._filterClauses:
            return
        self.filterListWidget.takeItem(self.filterListWidget.row(self._items[index]))
        self._filterClauses.pop(index)
        self._items.pop(index)

    def _clearFilters(self):
        for index in self._filterClauses.keys():
            self._removeFilterClause(index)

    def _createNewFilterClauseWidget(self):
        self.newFilterClauseWidget = self._createFilterClauseWidget()
        self.newFilterClauseWidget.filterAdded.connect(self._addNewFilterClause)
        self.newFilterFrame.layout().addWidget(self.newFilterClauseWidget)

    def _createFilterClauseWidget(self):
        widget = FilterClauseWidget(self)
        widget.setClassCodes(self._classCodes)
        widget.setSiteCode(self.siteCode())
        return widget

    def hasFilterType(self, filterType):
        for index in self._filterClauses.keys():
            if self._filterClauses[index] is not None and self._filterClauses[index].filterType() == filterType:
                return True
        return False

    def _clearFilterClicked(self):
        for index in self._filterClauses.keys():
            self._removeFilterClause(index)
        self.filterChanged.emit()
        self.clearFilterSelected.emit()

    def currentFilterSet(self):
        return self.filterSetCombo.itemData(self.siteCodeCombo.currentIndex())

    def addFilterClauseSet(self, key, name):
        self.filterSetCombo.addItem(name, key)

    def setFilterSet(self, key):
        self.filterSetCombo.setCurrentIndex(self.filterSetCombo.findData(key))

    def removeFilterSet(self, key):
        self.filterSetCombo.removeItem(self.filterSetCombo.findData(key))

    def _filterSetChanged(self, idx):
        self.filterSetChanged.emit(self.filterSetCombo.itemData(idx))

    def initSiteCodes(self, siteCodes):
        self.siteCodeCombo.clear()
        for site in siteCodes:
            self.siteCodeCombo.addItem(site)

    def siteCode(self):
        return self.siteCodeCombo.currentText()

    def initClassCodes(self, classCodes):
        self._classCodes = classCodes
        self.newFilterClauseWidget.setClassCodes(classCodes)

    def initFilterSets(self, filterSets):
        self.addFilterClauseSet('Default', 'Default')
        for filterSet in filterSets:
            if filterSet[0] != 'Default':
                self.addFilterClauseSet(filterSet[0], filterSet[1])

    def activeFilters(self):
        return self._filterClauses

    def activeFilterSet(self):
        fs = []
        for idx in self._filterClauses.keys():
            fs.append(self._filterClauses[idx].settings())
        return fs

    def toSettings(self, settings):
        i = 0
        for idx in self._filterClauses.keys():
            settings.setArrayIndex(i)
            self._filterClauses[idx].toSettings(settings)
            i += 1

    def fromSettings(self, settings, count):
        self._clearFilters()
        for i in range(0, count):
            settings.setArrayIndex(i)
            flt = self._createFilterClauseWidget()
            flt.fromSettings(settings)
            self._addFilterClause(flt)
        self.filterChanged.emit()
