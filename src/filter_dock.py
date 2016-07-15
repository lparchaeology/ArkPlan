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
from filter_base import *
from filter_clause_widget import *

class FilterSetWidget(QWidget, filter_set_widget_base.Ui_FilterSetWidget):

    def __init__(self, parent=None):
        super(FilterSetWidget, self).__init__(parent)
        self.setupUi(self)
        self._filterSetActionGroup = QActionGroup(self)
        self._filterSetActionGroup.addAction(self.saveFilterSetAction)
        self._filterSetActionGroup.addAction(self.reloadFilterSetAction)
        self._filterSetActionGroup.addAction(self.deleteFilterSetAction)
        self._filterSetActionGroup.addAction(self.exportFilterSetAction)
        self._filterSetMenu = QMenu(self)
        self._filterSetMenu.addActions(self._filterSetActionGroup.actions())
        self.filterSetTool.setMenu(self._filterSetMenu)
        self.filterSetTool.setDefaultAction(self.saveFilterSetAction)

    def setFilterSet(self, filterSet):
        self.setFilterSetKey(filterSet.key)
        if filterSet.source == 'ark':
            self.saveFilterSetAction.setEnabled(False)
            self.deleteFilterSetAction.setEnabled(False)
            self.filterSetTool.setDefaultAction(self.reloadFilterSetAction)
        else:
            self.saveFilterSetAction.setEnabled(True)
            self.deleteFilterSetAction.setEnabled(True)
            self.filterSetTool.setDefaultAction(self.saveFilterSetAction)

    def setFilterSetKey(self, key):
        self.filterSetCombo.setCurrentIndex(self.filterSetCombo.findData(key))

    def currentFilterSetKey(self):
        return self.filterSetCombo.itemData(self.filterSetCombo.currentIndex())

    def currentFilterSetName(self):
        return self.filterSetCombo.currentText()

class FilterDock(ToolDockWidget):

    filterChanged = pyqtSignal()
    filterClauseAdded = pyqtSignal()

    buildFilterSelected = pyqtSignal()
    buildSelectionSelected = pyqtSignal()
    buildHighlightSelected = pyqtSignal()
    clearFilterSelected = pyqtSignal()
    zoomFilterSelected = pyqtSignal()
    loadDataSelected = pyqtSignal()
    refreshDataSelected = pyqtSignal()
    showDataSelected = pyqtSignal()
    filterSetChanged = pyqtSignal(str)
    saveFilterSetSelected = pyqtSignal(str)
    reloadFilterSetSelected = pyqtSignal(str)
    deleteFilterSetSelected = pyqtSignal(str)
    exportFilterSetSelected = pyqtSignal(str, str)

    newFilterClauseWidget = None  # FilterClauseWidget()

    _filterIndex = 0
    _filterClauses = {}
    _items = {}
    _schematicClauses = []
    _schematicItems = []
    _classCodes = {}
    _history = []

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
        self._clearFilterAction.triggered.connect(self.clearFilterSelected)
        self.toolbar.addAction(self._clearFilterAction)

        self._loadDataAction = QAction(QIcon(':/plugins/ark/data/loadData.svg'), "Load Data", self)
        self._loadDataAction.triggered.connect(self.loadDataSelected)
        self.toolbar.addAction(self._loadDataAction)
        self._loadDataAction.setEnabled(False);

        self._refreshDataAction = QAction(QIcon(':/plugins/ark/data/refreshData.svg'), "Refresh Filter Sets", self)
        self._refreshDataAction.triggered.connect(self.refreshDataSelected)
        self.toolbar.addAction(self._refreshDataAction)
        self._refreshDataAction.setEnabled(False);

        #self._showDataAction = QAction(QIcon(':/plugins/ark/filter/viewData.png'), "Show Data", self)
        #self._showDataAction.triggered.connect(self.showDataSelected)
        #self.toolbar.addAction(self._showDataAction)

        self.widget.filterSetCombo.currentIndexChanged.connect(self._filterSetChanged)

        self.widget.saveFilterSetAction.triggered.connect(self._saveFilterSetSelected)
        self.widget.reloadFilterSetAction.triggered.connect(self._reloadFilterSetSelected)
        self.widget.deleteFilterSetAction.triggered.connect(self._deleteFilterSetSelected)
        self.widget.exportFilterSetAction.triggered.connect(self._exportFilterSetSelected)

        self.widget.schematicClauseList.setHidden(True)

        self._createNewFilterClauseWidget()

    def _saveFilterSetSelected(self):
        self.saveFilterSetSelected.emit(self.widget.currentFilterSetKey())

    def _reloadFilterSetSelected(self):
        self.reloadFilterSetSelected.emit(self.widget.currentFilterSetKey())

    def _deleteFilterSetSelected(self):
        self.deleteFilterSetSelected.emit(self.widget.currentFilterSetKey())

    def _exportFilterSetSelected(self):
        self.exportFilterSetSelected.emit(self.widget.currentFilterSetKey(), self.widget.currentFilterSetName())

    def addFilterClause(self, clause):
        filterClauseWidget = self._createFilterClauseWidget()
        filterClauseWidget.setClause(clause)
        filterClauseWidget.setFilterAction(FilterWidgetAction.RemoveFilter)
        idx = self._addFilterClause(filterClauseWidget)
        self.filterClauseAdded.emit()
        return idx

    def _addNewFilterClause(self):
        self.newFilterClauseWidget.clauseAdded.disconnect(self._addNewFilterClause)
        self.newFilterClauseWidget.setSiteCode(self.siteCode())
        self._history = self.newFilterClauseWidget.history()
        self._addFilterClause(self.newFilterClauseWidget)
        self._createNewFilterClauseWidget()
        self.newFilterClauseWidget.filterRangeCombo.setFocus()
        self.filterClauseAdded.emit()

    def _addFilterClause(self, filterClauseWidget):
        idx = self._filterIndex
        filterClauseWidget.setIndex(idx)
        self._filterClauses[idx] = filterClauseWidget
        filterClauseWidget.clauseRemoved.connect(self._filterClauseRemoved)
        filterClauseWidget.clauseChanged.connect(self.filterChanged)
        newItem = QListWidgetItem()
        newItem.setData(Qt.UserRole, idx)
        newItem.setSizeHint(filterClauseWidget.minimumSizeHint())
        self.widget.filterClauseList.addItem(newItem);
        self.widget.filterClauseList.setItemWidget(newItem, filterClauseWidget)
        self._items[idx] = newItem
        self._filterIndex += 1
        return idx

    def setSchematicFilterSet(self, filterSet):
        self.removeSchematicFilters()
        for clause in filterSet.clauses():
            self.widget.schematicClauseList.setHidden(False)
            clauseWidget = self._createFilterClauseWidget()
            clauseWidget.setClause(clause)
            clauseWidget.setFilterAction(FilterWidgetAction.LockFilter)
            self._schematicClauses.append(clauseWidget)
            newItem = QListWidgetItem()
            newItem.setSizeHint(clauseWidget.minimumSizeHint())
            self.widget.schematicClauseList.addItem(newItem);
            self.widget.schematicClauseList.setItemWidget(newItem, clauseWidget)
            self._schematicItems.append(newItem)

    def removeFilters(self):
        changed = False
        for index in self._filterClauses.keys():
            self._removeFilterClause(index)
            changed = True
        return changed

    def removeSchematicFilters(self):
        self.widget.schematicClauseList.setHidden(True)
        for item in self._schematicItems:
            self.widget.schematicClauseList.takeItem(self.widget.schematicClauseList.row(item))
        del self._schematicClauses[:]
        del self._schematicItems[:]

    def removeSelectFilters(self):
        changed = False
        for index in self._filterClauses.keys():
            if self._filterClauses[index] is not None and self._filterClauses[index].filterType() == FilterType.SelectFilter:
                self._removeFilterClause(index)
                changed = True
        return changed

    def removeHighlightFilters(self):
        changed = False
        for index in self._filterClauses.keys():
            if self._filterClauses[index] is not None and self._filterClauses[index].filterType() == FilterType.HighlightFilter:
                self._removeFilterClause(index)
                changed = True
        return changed

    def _filterClauseRemoved(self, index):
        self._removeFilterClause(index)
        self.filterChanged.emit()

    def _removeFilterClause(self, index):
        if index not in self._filterClauses:
            return False
        self.widget.filterClauseList.takeItem(self.widget.filterClauseList.row(self._items[index]))
        self._filterClauses.pop(index)
        self._items.pop(index)
        return True

    def _clearFilters(self):
        for index in self._filterClauses.keys():
            self._removeFilterClause(index)

    def _createNewFilterClauseWidget(self):
        self.newFilterClauseWidget = self._createFilterClauseWidget()
        self.newFilterClauseWidget.setHistory(self._history)
        self.newFilterClauseWidget.clauseAdded.connect(self._addNewFilterClause)
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

    def currentFilterSet(self):
        if self.widget.filterSetCombo.count() > 0:
            return self.widget.currentFilterSetKey()
        return 'Default'

    def setFilterSet(self, filterSet):
        self.blockSignals(True)
        self.widget.setFilterSet(filterSet)
        self.removeFilters()
        for clause in filterSet.clauses():
            self.addFilterClause(clause)
        self.blockSignals(False)

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

    def initFilterSets(self, filterSets, arkFilterSets):
        self.blockSignals(True)
        currentKey = self.currentFilterSet()
        self.widget.filterSetCombo.clear()
        if 'Default' in filterSets:
            self._addFilterSet(filterSets['Default'])
        for key in filterSets:
            filterSet = filterSets[key]
            if filterSet.key != 'Default':
                self._addFilterSet(filterSet)
        if len(arkFilterSets) > 0:
            self.widget.filterSetCombo.insertSeparator(self.widget.filterSetCombo.count())
            for key in arkFilterSets:
                self._addFilterSet(arkFilterSets[key])
        self.widget.setFilterSetKey(currentKey)
        self.blockSignals(False)

    def _addFilterSet(self, filterSet):
        name = filterSet.name
        if filterSet.source == 'ark':
            name = 'ARK: ' + name
        if filterSet.status == 'edited':
            name = '* ' + name
        self.widget.filterSetCombo.addItem(name, filterSet.key)

    def filterClauses(self):
        clauses = []
        for idx in self._filterClauses.keys():
            clauses.append(self._filterClauses[idx].clause())
        return clauses

    def enableArkData(self, enable=True):
        self._loadDataAction.setEnabled(enable);

    def activateArkData(self):
        self._refreshDataAction.setEnabled(True);
