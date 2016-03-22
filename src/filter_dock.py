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
from PyQt4.QtGui import QWidget, QListWidgetItem, QIcon, QAction, QActionGroup, QMenu

from ..libarkqgis.dock import ToolDockWidget
from ..libarkqgis import utils

import filter_set_widget_base
from filter_clause_widget import *
from enum import FilterType

class FilterSetWidget(QWidget, filter_set_widget_base.Ui_FilterSetWidget):

    def __init__(self, parent=None):
        super(FilterSetWidget, self).__init__(parent)
        self.setupUi(self)
        self._filterSetActionGroup = QActionGroup(self)
        self._filterSetActionGroup.addAction(self.saveFilterSetAction)
        self._filterSetActionGroup.addAction(self.deleteFilterSetAction)
        self._filterSetActionGroup.addAction(self.exportFilterSetAction)
        self._filterSetMenu = QMenu(self)
        self._filterSetMenu.addActions(self._filterSetActionGroup.actions())
        self.filterSetTool.setMenu(self._filterSetMenu)
        self.filterSetTool.setDefaultAction(self.saveFilterSetAction)

    def currentFilterSetKey(self):
        return self.filterSetCombo.itemData(self.filterSetCombo.currentIndex())

    def currentFilterSetName(self):
        return self.filterSetCombo.currentText()

class FilterDock(ToolDockWidget):

    filterChanged = pyqtSignal()

    buildFilterSelected = pyqtSignal()
    buildSelectionSelected = pyqtSignal()
    buildHighlightSelected = pyqtSignal()
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
        super(FilterDock, self).__init__(FilterSetWidget(), parent)

        self.setWindowTitle(u'ARK Filter')
        self.setObjectName(u'FilterDock')

    def initGui(self, iface, location, menuAction):
        super(FilterDock, self).initGui(iface, location, menuAction)

        self._zoomFilterAction = QAction(QIcon(':/plugins/ark/filter/zoomToFilterSet.svg'), "Zoom To Selection", self)
        self._zoomFilterAction.triggered.connect(self.zoomFilterSelected)
        self.toolbar.addAction(self._zoomFilterAction)

        self._buildFilterAction = QAction(QIcon(':/plugins/ark/filter/buildFilter.svg'), "Build Filter", self)
        self._buildFilterAction.triggered.connect(self.buildFilterSelected)
        self.toolbar.addAction(self._buildFilterAction)

        self._buildSelectionAction = QAction(QIcon(':/plugins/ark/filter/buildSelection.svg'), "Build Selection", self)
        self._buildSelectionAction.triggered.connect(self.buildSelectionSelected)
        self.toolbar.addAction(self._buildSelectionAction)

        self._buildHighlightAction = QAction(QIcon(':/plugins/ark/filter/buildHighlight.svg'), "Build Highlight", self)
        self._buildHighlightAction.triggered.connect(self.buildHighlightSelected)
        self.toolbar.addAction(self._buildHighlightAction)

        self._clearFilterAction = QAction(QIcon(':/plugins/ark/filter/removeFilter.svg'), "Clear Filter", self)
        self._clearFilterAction.triggered.connect(self._clearFilterClicked)
        self.toolbar.addAction(self._clearFilterAction)

        #self._loadDataAction = QAction(QIcon(':/plugins/ark/filter/loadData.png'), "Load Data", self)
        #self._loadDataAction.triggered.connect(self.loadDataSelected)
        #self.toolbar.addAction(self._loadDataAction)

        #self._showDataAction = QAction(QIcon(':/plugins/ark/filter/viewData.png'), "Show Data", self)
        #self._showDataAction.triggered.connect(self.showDataSelected)
        #self.toolbar.addAction(self._showDataAction)

        self.widget.filterSetCombo.currentIndexChanged.connect(self._filterSetChanged)

        self.widget.saveFilterSetAction.triggered.connect(self._saveFilterSetSelected)
        self.widget.deleteFilterSetAction.triggered.connect(self._deleteFilterSetSelected)
        self.widget.exportFilterSetAction.triggered.connect(self._exportFilterSetSelected)

        self._createNewFilterClauseWidget()

    def _saveFilterSetSelected(self):
        self.saveFilterSetSelected.emit(self.widget.currentFilterSetKey(), self.widget.currentFilterSetName())

    def _deleteFilterSetSelected(self):
        self.deleteFilterSetSelected.emit(self.widget.currentFilterSetKey())

    def _exportFilterSetSelected(self):
        self.exportFilterSetSelected.emit(self.widget.currentFilterSetKey(), self.widget.currentFilterSetName())

    def addFilterClause(self, filterType, itemKey, filterAction):
        filterClauseWidget = self._createFilterClauseWidget()
        filterClauseWidget.setFilterType(filterType)
        filterClauseWidget.setSiteCode(itemKey.siteCode)
        filterClauseWidget.setClassCode(itemKey.classCode)
        filterClauseWidget.setFilterRange(itemKey.itemId)
        filterClauseWidget.setFilterAction(filterAction)
        return self._addFilterClause(filterClauseWidget)

    def _addNewFilterClause(self):
        self.newFilterClauseWidget.filterAdded.disconnect(self._addNewFilterClause)
        self.newFilterClauseWidget.setSiteCode(self.siteCode())
        self._addFilterClause(self.newFilterClauseWidget)
        self._createNewFilterClauseWidget()
        self.newFilterClauseWidget.filterRangeCombo.setFocus()

    def _addFilterClause(self, filterClauseWidget):
        idx = self._filterIndex
        filterClauseWidget.setIndex(idx)
        self._filterClauses[idx] = filterClauseWidget
        filterClauseWidget.filterRemoved.connect(self._filterClauseRemoved)
        filterClauseWidget.filterChanged.connect(self.filterChanged)
        newItem = QListWidgetItem()
        newItem.setData(Qt.UserRole, idx)
        newItem.setSizeHint(filterClauseWidget.minimumSizeHint())
        self.widget.filterListWidget.addItem(newItem);
        self.widget.filterListWidget.setItemWidget(newItem, filterClauseWidget)
        self._items[idx] = newItem
        self._filterIndex += 1
        return idx

    def removeFilters(self):
        changed = False
        for index in self._filterClauses.keys():
            self.removeFilterClause(index)
            changed = True
        return changed

    def removeSelectFilters(self):
        changed = False
        for index in self._filterClauses.keys():
            if self._filterClauses[index] is not None and self._filterClauses[index].filterType() == FilterType.SelectFilter:
                self.removeFilterClause(index)
                changed = True
        return changed

    def removeHighlightFilters(self):
        changed = False
        for index in self._filterClauses.keys():
            if self._filterClauses[index] is not None and self._filterClauses[index].filterType() == FilterType.HighlightFilter:
                self.removeFilterClause(index)
                changed = True
        return changed

    def _filterClauseRemoved(self, index):
        self.removeFilterClause(index)
        self.filterChanged.emit()

    def removeFilterClause(self, index):
        if index not in self._filterClauses:
            return False
        self.widget.filterListWidget.takeItem(self.widget.filterListWidget.row(self._items[index]))
        self._filterClauses.pop(index)
        self._items.pop(index)
        return True

    def _clearFilters(self):
        for index in self._filterClauses.keys():
            self.removeFilterClause(index)

    def _createNewFilterClauseWidget(self):
        self.newFilterClauseWidget = self._createFilterClauseWidget()
        self.newFilterClauseWidget.filterAdded.connect(self._addNewFilterClause)
        self.widget.newFilterFrame.layout().addWidget(self.newFilterClauseWidget)

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
        self.removeFilters()
        self.clearFilterSelected.emit()

    def currentFilterSet(self):
        return self.widget.filterSetCombo.itemData(self.widget.siteCodeCombo.currentIndex())

    def addFilterSet(self, key, name):
        self.widget.filterSetCombo.addItem(name, key)

    def setFilterSet(self, key):
        self.widget.filterSetCombo.setCurrentIndex(self.widget.filterSetCombo.findData(key))

    def removeFilterSet(self, key):
        self.widget.filterSetCombo.removeItem(self.widget.filterSetCombo.findData(key))

    def _filterSetChanged(self, idx):
        self.filterSetChanged.emit(self.widget.filterSetCombo.itemData(idx))

    def initSiteCodes(self, siteCodes):
        self.widget.siteCodeCombo.clear()
        for site in siteCodes:
            self.widget.siteCodeCombo.addItem(site)

    def siteCode(self):
        return self.widget.siteCodeCombo.currentText()

    def initClassCodes(self, classCodes):
        self._classCodes = classCodes
        self.newFilterClauseWidget.setClassCodes(classCodes)

    def initFilterSets(self, filterSets):
        self.blockSignals(True)
        self.addFilterSet('Default', 'Default')
        for filterSet in filterSets:
            if filterSet[0] != 'Default':
                self.addFilterSet(filterSet[0], filterSet[1])
        self.blockSignals(False)

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
