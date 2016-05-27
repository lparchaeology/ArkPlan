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
import re, copy

from PyQt4.QtCore import Qt, QObject, QRegExp, QSettings, pyqtSignal
from PyQt4.QtGui import QAction, QIcon, QFileDialog, QInputDialog, QColor

from qgis.core import *
from qgis.gui import QgsExpressionBuilderDialog, QgsMessageBar

from ..libarkqgis.map_tools import ArkMapToolIndentifyFeatures
from ..libarkqgis import layers, utils
from ..libarkqgis.project import Project

from enum import *
from data_dialog import DataDialog
from filter_export_dialog import FilterExportDialog
from filter_dock import FilterDock
from filter_base import *
from config import Config
from plan_item import ItemKey

import resources

class FilterModule(QObject):

    filterSetCleared = pyqtSignal()

    project = None # Project()

    # Internal variables
    dock = None # FilterDock()
    _initialised = False
    _useGroups = False
    _filterSetGroupIndex = -1
    _filterSets = {}  # {str: FilterSet()}
    _arkFilterSets = {}  # {str: FilterSet()}
    _schematicFilterSet = FilterSet()  # FilterSet()

    def __init__(self, project):
        super(FilterModule, self).__init__(project)
        self.project = project

    # Standard Dock methods

    # Create the gui when the plugin is first created
    def initGui(self):
        self.dock = FilterDock(self.project.layerDock)
        action = self.project.addDockAction(':/plugins/ark/filter/filter.png', self.tr(u'Filter Tools'), callback=self.run, checkable=True)
        self.dock.initGui(self.project.iface, Qt.LeftDockWidgetArea, action)

        self.dock.filterChanged.connect(self._filterChanged)
        self.dock.filterClauseAdded.connect(self._filterChanged)

        self.dock.buildFilterSelected.connect(self.buildFilter)
        self.dock.buildSelectionSelected.connect(self.buildSelection)
        self.dock.buildHighlightSelected.connect(self.buildHighlight)
        self.dock.clearFilterSelected.connect(self.clearFilters)
        self.dock.clearFilterSelected.connect(self.filterSetCleared)
        self.dock.loadDataSelected.connect(self._loadArkData)
        self.dock.refreshDataSelected.connect(self._refreshArkData)
        self.dock.showDataSelected.connect(self.showDataDialogFilter)
        self.dock.zoomFilterSelected.connect(self.zoomFilter)

        self.dock.filterSetChanged.connect(self.setFilterSet)
        self.dock.saveFilterSetSelected.connect(self._saveFilterSetSelected)
        self.dock.reloadFilterSetSelected.connect(self._reloadFilterSetSelected)
        self.dock.deleteFilterSetSelected.connect(self._deleteFilterSetSelected)
        self.dock.exportFilterSetSelected.connect(self._exportFilterSetSelected)

    # Load the project settings when project is loaded
    def loadProject(self):
        # Load the Site Codes
        self.dock.initSiteCodes(self.project.siteCodes())

        # Load the Class Codes
        self._loadClassCodes()

        # Load the saved Filter Sets
        self._loadFilterSets()

        # Respond to ARK data load
        self._enableArkData()
        self.project.data.dataLoaded.connect(self._activateArkData)

        # Init the schematic filter set
        self._schematicFilterSet = FilterSet.fromSchematic(self.project)

        self._initialised = True
        self.setFilterSet('Default')
        return self._initialised

    # Save the project
    def writeProject(self):
        if self.currentFilterSetKey() == 'Default':
            self._saveFilterSet('Default')

    # Close the project
    def closeProject(self):
        self.project.data.dataLoaded.disconnect(self._activateArkData)
        #FIXME Doesn't clear on quit as layers already unloaded by main program!
        self.removeFilters()
        # Reset the initialisation
        self._initialised = False

    # Unload the gui when the plugin is unloaded
    def unloadGui(self):
        self.dock.unloadGui()

    def run(self, checked):
        if checked and not self._initialised:
            self.dock.menuAction().setChecked(False)

    def showDock(self, show=True):
        self.dock.menuAction().setChecked(show)

    def _loadClassCodes(self):
        # Load the Class Codes
        codeList = set()
        for key in Config.classCodes:
            classCode = Config.classCodes[key]
            if classCode['plan']:
                codeList.add(classCode['code'])
            elif Config.isGroupClass(classCode['code']) and self.project.data.hasClassData(classCode['code']):
                codeList.add(classCode['code'])
        codes = {}
        for code in sorted(codeList):
            codes[code] = code
        self.dock.initClassCodes(codes)

    def _enableArkData(self, enable=True):
        if self.project.useArkDB() and self.project.arkUrl():
            self.dock.enableArkData(enable);

    def _activateArkData(self):
        self._loadClassCodes()
        self._loadArkFilterSets()
        self.dock.activateArkData()

    # Filter methods

    def _typeForAction(self, filterAction):
        if (filterAction == FilterAction.IncludeFilter or filterAction == FilterAction.ExclusiveFilter):
            return FilterType.IncludeFilter
        elif (filterAction == FilterAction.SelectFilter or filterAction == FilterAction.ExclusiveSelectFilter):
            return FilterType.SelectFilter
        elif (filterAction == FilterAction.HighlightFilter or filterAction == FilterAction.ExclusiveHighlightFilter):
            return FilterType.HighlightFilter
        elif (filterAction == FilterAction.ExcludeFilter):
            return FilterType.ExcludeFilter
        return -1

    def applyItemAction(self, itemKey, filterAction):
        if not self._initialised or filterAction == FilterAction.NoFilterAction:
            return

        if (filterAction == FilterAction.ExclusiveFilter
            or filterAction == FilterAction.ExclusiveSelectFilter
            or filterAction == FilterAction.ExclusiveHighlightFilter):
            self.dock.removeFilters()

        filterType = self._typeForAction(filterAction)

        if filterType >= 0:
            return self.addFilterClause(filterType, itemKey)
        return -1

    def filterItem(self, itemKey):
        if not self._initialised:
            return
        self.dock.removeFilters()
        ret = self.addFilterClause(FilterType.IncludeFilter, itemKey)
        self.zoomFilter()
        return ret

    def excludeItem(self, itemKey):
        if not self._initialised:
            return
        return self.addFilterClause(FilterType.ExcludeFilter, itemKey)

    def highlightItem(self, itemKey):
        if not self._initialised:
            return
        self.dock.removeHighlightFilters()
        return self.addFilterClause(FilterType.HighlightFilter, itemKey)

    def addHighlightItem(self, itemKey):
        if not self._initialised:
            return
        return self.addFilterClause(FilterType.HighlightFilter, itemKey)

    def applySchematicFilter(self, itemKey, filterAction):
        if not self._initialised:
            return
        self._schematicFilterSet.clearClauses()
        cl = FilterClause()
        cl.key = itemKey
        if ((filterAction == FilterAction.SelectFilter or filterAction == FilterAction.ExclusiveSelectFilter
             or filterAction == FilterAction.HighlightFilter or filterAction == FilterAction.ExclusiveHighlightFilter)
            and (self.hasFilterType(FilterType.IncludeFilter) or self.hasFilterType(FilterType.ExcludeFilter))):
            cl.action = FilterType.IncludeFilter
            self._schematicFilterSet.addClause(cl)
        cl.action = self._typeForAction(filterAction)
        self._schematicFilterSet.addClause(cl)
        self.dock.setSchematicFilterSet(self._schematicFilterSet)
        self.project.logMessage(self._schematicFilterSet.debug(True))
        self._applyFilters()

    def clearSchematicFilter(self):
        if len(self._schematicFilterSet.clauses()) > 0:
            self._schematicFilterSet.clearClauses()
            self.dock.removeSchematicFilters()
            self._applyFilters()

    def addFilterClause(self, filterType, itemKey):
        if not self._initialised:
            return
        idx = self.dock.addFilterClause(filterType, itemKey)
        self._applyFilters()
        return idx

    def removeFilters(self):
        if not self._initialised:
            return
        if self.dock.removeFilters():
            self._applyFilters()

    def removeSelectFilters(self):
        if not self._initialised:
            return
        if self.dock.removeSelectFilters():
            self._applyFilters()

    def removeHighlightFilters(self):
        if not self._initialised:
            return
        if self.dock.removeHighlightFilters():
            self._applyFilters()

    def hasFilterType(self, filterType):
        if not self._initialised:
            return False
        return self.dock.hasFilterType(filterType)

    def _filterChanged(self):
        self.currentFilterSet().setClauses(self.dock.filterClauses())
        self.dock.initFilterSets(self._filterSets, self._arkFilterSets)
        self._applyFilters()

    def _applyFilters(self):
        if not self._initialised:
            return

        # Filter
        filterString = self.currentFilterSet().expression
        schematicString = self._schematicFilterSet.expression
        self.project.logMessage('Main filter = ' + filterString)
        self.project.logMessage('Schematic filter = ' + schematicString)
        if filterString and schematicString:
            self.applyFilter('(' + filterString + ') or (' + schematicString + ')')
        elif schematicString:
            self.applyFilter(schematicString)
        else:
            self.applyFilter(filterString)

        # Selection
        filterString = self.currentFilterSet().selection
        schematicString = self._schematicFilterSet.selection
        self.project.logMessage('Main select = ' + filterString)
        self.project.logMessage('Schematic select = ' + schematicString)
        if filterString and schematicString:
            self.applySelection('(' + filterString + ') or (' + schematicString + ')')
        elif schematicString:
            self.applySelection(schematicString)
        else:
            self.applySelection(filterString)

        self.applyHighlightFilters()


    def applyHighlightFilters(self):
        if not self._initialised:
            return
        highlightString = ''
        firstHighlight = True
        self.project.plan.clearHighlight()
        self._applyHighlightClauses(self.currentFilterSet().clauses())
        self._applyHighlightClauses(self._schematicFilterSet.clauses())

    def _applyHighlightClauses(self, clauses):
        for clause in clauses:
            if clause.action == FilterType.HighlightFilter:
                filterItemKey = self.project.data.nodesItemKey(clause.key)
                self.addHighlight(filterItemKey.filterClause(), clause.lineColor(), clause.color)

    def clearFilters(self):
        self._filterSets['Default'].clearClauses()
        self.setFilterSet('Default')

    def _clearFilters(self):
        self.project.plan.clearFilter()
        self.project.plan.clearSelection()
        self.project.plan.clearHighlight()

    def applyFilter(self, expression):
        if not self._initialised:
            return
        self.project.logMessage('applyFilter = ' + expression)
        self.project.plan.applyFilter(expression)


    def applySelection(self, expression):
        self.project.logMessage('applySelection = ' + expression)
        self.project.plan.applySelection(expression)


    def applyHighlight(self, expression, lineColor=None, fillColor=None):
        self.project.plan.applyHighlight(expression, lineColor, fillColor, 0.1, 0.1)


    def addHighlight(self, expression, lineColor=None, fillColor=None):
        self.project.logMessage('Add highlight = ' + expression)
        self.project.plan.addHighlight(expression, lineColor, fillColor, 0.1, 0.1)


    def buildFilter(self):
        dialog = QgsExpressionBuilderDialog(self.project.plan.linesLayer)
        dialog.setExpressionText(self.project.plan.filter)
        if (dialog.exec_()):
            self.applyFilter(dialog.expressionText())


    def buildSelection(self):
        dialog = QgsExpressionBuilderDialog(self.project.plan.linesLayer)
        dialog.setExpressionText(self.project.plan.selection)
        if (dialog.exec_()):
            self.applySelection(dialog.expressionText())


    def buildHighlight(self):
        dialog = QgsExpressionBuilderDialog(self.project.plan.linesLayer)
        dialog.setExpressionText(self.project.plan.highlight)
        if (dialog.exec_()):
            self.applyHighlight(dialog.expressionText())


    def _loadArkData(self):
        self.project.data.loadData()


    def _refreshArkData(self):
        self.project.data.refreshData()


    def zoomFilter(self):
        self.project.plan.zoomToExtent()


    def showIdentifyDialog(self, feature):
        context = feature.attribute(self.project.fieldName('id'))
        self.showDataDialogList([context])


    def showDataDialogFilter(self):
        #TODO Create Context list from filter set
        return self.showDataDialogList([])


    def showDataDialogList(self, contextList):
        subList = []
        groupList = []
        for context in contextList:
            subList.append(self.data.subGroupForContext(context))
            groupList.append(self.data.groupForContext(context))
        dataDialog = DataDialog(self.project.iface.mainWindow())
        dataDialog.contextTableView.setModel(self.data._contextProxyModel)
        self.data._contextProxyModel.setFilterRegExp(utils._listToRegExp(contextList))
        dataDialog.contextTableView.resizeColumnsToContents()
        dataDialog.subGroupTableView.setModel(self.data._subGroupProxyModel)
        self.data._subGroupProxyModel.setFilterRegExp(utils._listToRegExp(subList))
        dataDialog.subGroupTableView.resizeColumnsToContents()
        dataDialog.groupTableView.setModel(self.data._groupProxyModel)
        self.data._groupProxyModel.setFilterRegExp(utils._listToRegExp(groupList))
        dataDialog.groupTableView.resizeColumnsToContents()
        return dataDialog.exec_()

    # Filter Set methods

    def currentFilterSet(self):
        key = self.currentFilterSetKey()
        if key[0:4] == 'ark_':
            return self._arkFilterSets[key]
        return self._filterSets[key]

    def currentFilterSetKey(self):
        return self.dock.currentFilterSet()

    def _filterSetGroup(self, key):
        return 'filterset/' + key

    def _makeKey(self, name):
        name = re.sub(r'[^\w\s]','', name)
        return re.sub(r'\s+', '', name)

    def _loadFilterSets(self):
        self._filterSets = {}
        settings = QSettings()
        settings.beginGroup('filterset')
        groups = settings.childGroups()
        settings.endGroup()
        self.project.logMessage('_loadFilterSets = ' + str(groups))
        for group in groups:
            self.project.logMessage('Loading FilterSet = ' + group)
            filterSet = FilterSet.fromSettings(self.project, 'filterset', group)
            self.project.logMessage('FilterSet = ' + filterSet.debug(True))
            self._filterSets[filterSet.key] = filterSet
        self.dock.initFilterSets(self._filterSets, self._arkFilterSets)

    def _loadArkFilterSets(self):
        self._arkFilterSets = {}
        filters = self.project.data.getFilters()
        self.project.logMessage('ARK Filters = ' + str(filters))
        for key in filters:
            self.project.logMessage('Loading ARK FilterSet = ' + str(key) + ' ' + str(filters[key]))
            filterSet = FilterSet.fromArk(self.project, key, filters[key])
            self.project.logMessage('FilterSet = ' + filterSet.debug(True))
            self._arkFilterSets[filterSet.key] = filterSet
        self.dock.initFilterSets(self._filterSets, self._arkFilterSets)

    def _exportFilterSet(self, key):
        pass

    def setFilterSet(self, key='Default'):
        if key in self._filterSets:
            self._setFilterSet(self._filterSets[key])
        if key in self._arkFilterSets:
            self._setFilterSet(self._arkFilterSets[key])

    def _setFilterSet(self, filterSet):
        self.project.logMessage('_setFilterSet = ' + filterSet.key)
        self.dock.setFilterSet(filterSet)
        self.project.logMessage('FilterSet now = ' + filterSet.debug(True))
        self._applyFilters()

    def _saveFilterSetSelected(self, name):
        saveName, ok = QInputDialog.getText(None, 'Save Filter Set', 'Enter Name of Filter Set', text=name)
        if ok:
            self._saveFilterSet(saveName)

    def _saveFilterSet(self, name):
        key = self._makeKey(name)
        if key in self._filterSets:
            self._filterSets[key].setClauses(self.dock.filterClauses())
            self._filterSets[key].save()
        else:
            filterSet = FilterSet.fromName(self.project, 'filterset', key, name)
            filterSet.setClauses(self.dock.filterClauses())
            filterSet.save()
            self._filterSets[key] = filterSet
        if key != self.currentFilterSetKey():
            self.currentFilterSet().reloadClauses()
        self.dock.initFilterSets(self._filterSets, self._arkFilterSets)
        self.setFilterSet(key)

    def _reloadFilterSetSelected(self, key):
        if key in self._filterSets:
            self._filterSets[key].reloadClauses()
        if key in self._arkFilterSets:
            self._arkFilterSets[key].reloadClauses()
        self.dock.initFilterSets(self._filterSets, self._arkFilterSets)
        self.setFilterSet(key)

    def _deleteFilterSetSelected(self, key):
        if key in self._filterSets:
            self._filterSets[key].delete()
            del self._filterSets[key]
            self.dock.initFilterSets(self._filterSets, self._arkFilterSets)
            self.setFilterSet('Default')

    def _exportFilterSetSelected(self, key, name):
        dialog = FilterExportDialog()
        dialog.setFilterSetName(name)
        dialog.setExportName(name)
        if dialog.exec_():
            exportName = dialog.exportName()
            exportKey = self._makeKey(exportName)
            if dialog.exportSchematic():
                self._exportSchematic(exportKey, exportName, dialog.schematicColor())
            elif dialog.exportData():
                self._exportLayers(exportKey, exportName)

    def _exportSchematic(self, key, name, schematicColor):
        if self._filterSetGroupIndex < 0:
            self._filterSetGroupIndex = layers.createLayerGroup(self.project.iface, Config.filterSetGroupName, Config.projectGroupName)
        layer = self.project.plan.polygonsLayer
        mem = layers.cloneAsMemoryLayer(layer, name, 'DefaultStyle')
        mem.rendererV2().symbols()[0].setColor(schematicColor)
        mem.startEditing()
        fi = layer.getFeatures()
        for feature in fi:
            if feature.attribute(self.project.fieldName('category')) == 'sch':
                mem.addFeature(feature)
        mem.commitChanges()
        mem = layers.addLayerToLegend(self.project.iface, mem, self._filterSetGroupIndex)

    def _exportLayers(self, key, name):
        if self._filterSetGroupIndex < 0:
            self._filterSetGroupIndex = layers.createLayerGroup(self.project.iface, Config.filterSetGroupName, Config.projectGroupName)
        exportGroup = layers.createLayerGroup(self.project.iface, name, Config.filterSetGroupName)
        pgMem = layers.duplicateAsMemoryLayer(self.project.plan.polygonsLayer, key + '_pg')
        plMem = layers.duplicateAsMemoryLayer(self.project.plan.linesLayer, key + '_pl')
        ptMem = layers.duplicateAsMemoryLayer(self.project.plan.pointsLayer, key + '_pt')
        layers.addLayerToLegend(self.project.iface, pgMem, exportGroup)
        layers.addLayerToLegend(self.project.iface, plMem, exportGroup)
        layers.addLayerToLegend(self.project.iface, ptMem, exportGroup)
