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
import re

from PyQt4.QtCore import Qt, QObject, QRegExp, QSettings, pyqtSignal
from PyQt4.QtGui import QAction, QIcon, QFileDialog, QInputDialog

from qgis.core import *
from qgis.gui import QgsExpressionBuilderDialog, QgsMessageBar

from ..libarkqgis.map_tools import ArkMapToolIndentifyFeatures
from ..libarkqgis import layers, utils

from data_dialog import DataDialog
from filter_export_dialog import FilterExportDialog
from filter_dock import FilterDock
from filter_clause_widget import FilterType, FilterAction
from config import Config
from plan_item import ItemKey

import resources

class Filter(QObject):

    filterSetCleared = pyqtSignal()

    project = None # Project()

    # Internal variables
    dock = None # FilterDock()
    _initialised = False
    _dataLoaded = False
    _useGroups = False
    _filterSetGroupIndex = -1

    _schematicIncludeFilter = -1
    _schematicSelectFilter = -1
    _schematicHighlightFilter = -1

    def __init__(self, project):
        super(Filter, self).__init__(project)
        self.project = project

    # Standard Dock methods

    # Create the gui when the plugin is first created
    def initGui(self):
        self.dock = FilterDock(self.project.layerDock)
        action = self.project.addDockAction(':/plugins/ark/filter/filter.png', self.tr(u'Filter Tools'), callback=self.run, checkable=True)
        self.dock.initGui(self.project.iface, Qt.LeftDockWidgetArea, action)

        self.dock.filterChanged.connect(self.applyFilters)
        self.dock.buildFilterSelected.connect(self.buildFilter)
        self.dock.buildSelectionSelected.connect(self.buildSelection)
        self.dock.buildHighlightSelected.connect(self.buildHighlight)
        self.dock.clearFilterSelected.connect(self._clearFilterSet)
        self.dock.clearFilterSelected.connect(self.filterSetCleared)
        self.dock.loadDataSelected.connect(self.loadData)
        self.dock.showDataSelected.connect(self.showDataDialogFilter)
        self.dock.zoomFilterSelected.connect(self.zoomFilter)

        self.dock.filterSetChanged.connect(self._loadFilterSet)
        self.dock.saveFilterSetSelected.connect(self._saveFilterSetSelected)
        self.dock.deleteFilterSetSelected.connect(self._deleteFilterSetSelected)
        self.dock.exportFilterSetSelected.connect(self._exportFilterSetSelected)

    # Load the project settings when project is loaded
    def loadProject(self):
        # Load the Site Codes
        self.dock.initSiteCodes(self.project.siteCodes())

        # Load the Class Codes
        codeList = set()
        for key in Config.classCodes:
            classCode = Config.classCodes[key]
            if classCode['plan']:
                codeList.add(classCode['code'])
        if self.project.data.hasClassData('sgr'):
            codeList.add('sgr')
        if self.project.data.hasClassData('grp'):
            codeList.add('grp')
        codes = {}
        for code in sorted(codeList):
            codes[code] = code
        self.dock.initClassCodes(codes)

        # Load the saved Filter Sets
        self.dock.initFilterSets(self._listFilterSets())

        self._initialised = True
        self._clearFilterSet()
        self.loadFilterSet('Default')
        return self._initialised

    # Save the project
    def writeProject(self):
        if self.dock.currentFilterSet() == 'Default':
            self._saveFilterSet('Default', 'Default')

    # Close the project
    def closeProject(self):
        #FIXME Doesn't clear on quit as layers already unloaded by main program!
        self.removeFilters()
        # Reset the initialisation
        self._initialised = False
        self._dataLoaded = False

    # Unload the gui when the plugin is unloaded
    def unloadGui(self):
        self.dock.unloadGui()

    def run(self, checked):
        if checked and not self._initialised:
            self.dock.menuAction().setChecked(False)

    def showDock(self, show=True):
        self.dock.menuAction().setChecked(show)

    # Filter methods

    def filterItem(self, itemKey):
        if not self._initialised:
            return
        self.dock.removeFilters()
        self.addFilterClause(FilterType.IncludeFilter, itemKey)
        self.zoomFilter()

    def excludeItem(self, itemKey):
        if not self._initialised:
            return
        self.addFilterClause(FilterType.ExcludeFilter, itemKey)

    def highlightItem(self, itemKey):
        if not self._initialised:
            return
        self.dock.removeHighlightFilters()
        self.addFilterClause(FilterType.HighlightFilter, itemKey)

    def addHighlightItem(self, itemKey):
        if not self._initialised:
            return
        self.addFilterClause(FilterType.HighlightFilter, itemKey)

    def applySchematicFilter(self, itemKey):
        if not self._initialised:
            return
        self._clearSchematicFilter()
        if self.hasFilterType(FilterType.IncludeFilter) or self.hasFilterType(FilterType.ExcludeFilter):
            self._schematicIncludeFilter = self.dock.addFilterClause(FilterType.IncludeFilter, itemKey, FilterAction.LockFilter)
        self._schematicSelectFilter = self.dock.addFilterClause(FilterType.SelectFilter, itemKey, FilterAction.LockFilter)
        self._schematicHighlightFilter = self.dock.addFilterClause(FilterType.HighlightFilter, itemKey, FilterAction.LockFilter)
        self.applyFilters()

    def clearSchematicFilter(self):
        self._clearSchematicFilter()
        self.applyFilters()

    def _clearSchematicFilter(self):
        if self._schematicIncludeFilter >= 0:
            self.dock.removeFilterClause(self._schematicIncludeFilter)
            self._schematicIncludeFilter = -1
        if self._schematicSelectFilter >= 0:
            self.dock.removeFilterClause(self._schematicSelectFilter)
            self._schematicSelectFilter = -1
        if self._schematicHighlightFilter >= 0:
            self.dock.removeFilterClause(self._schematicHighlightFilter)
            self._schematicHighlightFilter = -1

    def addFilterClause(self, filterType, itemKey, filterAction=FilterAction.RemoveFilter):
        if not self._initialised:
            return
        idx = self.dock.addFilterClause(filterType, itemKey, filterAction)
        self.applyFilters()
        return idx

    def removeFilterClause(self, filterIndex):
        if not self._initialised:
            return
        if self.dock.removeFilterClause(filterIndex):
            self.applyFilters()

    def removeFilters(self):
        if not self._initialised:
            return
        if self.dock.removeFilters():
            self.applyFilters()

    def removeSelectFilters(self):
        if not self._initialised:
            return
        if self.dock.removeSelectFilters():
            self.applyFilters()

    def removeHighlightFilters(self):
        if not self._initialised:
            return
        if self.dock.removeHighlightFilters():
            self.applyFilters()

    def hasFilterType(self, filterType):
        if not self._initialised:
            return False
        return self.dock.hasFilterType(filterType)

    def applyFilters(self):
        utils.logMessage('Filter.applyFilters()')
        if not self._initialised:
            return
        excludeString = ''
        firstInclude = True
        includeString = ''
        firstExclude = True
        selectString = ''
        firstSelect = True
        activeFilters = self.dock.activeFilters()
        for index in activeFilters:
            if activeFilters[index] is not None:
                filter = activeFilters[index]
                filterItemKey = filter.itemKey()
                if filter.classCode == 'grp':
                    subItemKey = self._childrenItemKey(filterItemKey)
                    filterItemKey = self._childrenItemKey(subItemKey)
                elif filter.classCode() == 'sgr':
                    filterItemKey = self._childrenItemKey(filterItemKey)
                if filter.filterType() == FilterType.SelectFilter:
                    if firstSelect:
                        firstSelect = False
                    else:
                        selectString += ' or '
                    selectString += filterItemKey.filterClause()
                elif filter.filterType() == FilterType.ExcludeFilter:
                    if firstExclude:
                        firstExclude = False
                    else:
                        excludeString += ' or '
                    excludeString += filterItemKey.filterClause()
                elif filter.filterType() == FilterType.IncludeFilter:
                    if firstInclude:
                        firstInclude = False
                    else:
                        includeString += ' or '
                    includeString += filterItemKey.filterClause()
        utils.logMessage(' - include = ' + includeString)
        utils.logMessage(' - exclude = ' + excludeString)
        utils.logMessage(' - select = ' + selectString)
        if includeString and excludeString:
            self.applyFilter('(' + includeString + ') and NOT (' + excludeString + ')')
        elif excludeString:
            self.applyFilter('NOT (' + excludeString + ')')
        else:
            self.applyFilter(includeString)
        self.applySelection(selectString)
        self.applyHighlightFilters()


    def applyHighlightFilters(self):
        utils.logMessage('Filter.applyHighlightFilters() = ' + str(self._initialised))
        if not self._initialised:
            return
        highlightString = ''
        firstHighlight = True
        activeFilters = self.dock.activeFilters()
        self.project.plan.clearHighlight()
        for index in activeFilters:
            if activeFilters[index] is not None:
                filter = activeFilters[index]
                filterItemKey = filter.itemKey()
                if filter.classCode == 'grp':
                    subItemKey = self._childrenItemKey(filterItemKey)
                    filterItemKey = self._childrenItemKey(subItemKey)
                elif filter.classCode() == 'sgr':
                    filterItemKey = self._childrenItemKey(filterItemKey)
                if filter.filterType() == FilterType.HighlightFilter:
                    self.addHighlight(filterItemKey.filterClause(), filter.highlightColor())


    def _clearFilterSet(self):
        self.project.plan.clearFilter()
        self.project.plan.clearSelection()
        self.project.plan.clearHighlight()


    def applyFilter(self, expression):
        if not self._initialised:
            return
        self.project.plan.applyFilter(expression)


    def applySelection(self, expression):
        self.project.plan.applySelection(expression)


    def applyHighlight(self, expression, color=None):
        self.project.plan.applyHighlight(expression, color)


    def addHighlight(self, expression, color=None):
        self.project.plan.addHighlight(expression, color)


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


    def loadData(self):
        self.data.loadData()
        self.dock.enableGroupFilters(True)
        self._dataLoaded = True


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

    def _childrenItemKey(self, parentItemKey):
        childSiteCode = ''
        childClassCode = ''
        childIdSet = set()
        lookupItemKey = parentItemKey.deepcopy()
        for parent in parentItemKey.itemIdList():
            lookupItemKey.itemId = parent
            children = self.project.data.getChildren(lookupItemKey)
            for child in children:
                childSiteCode = child.siteCode
                childClassCode = child.classCode
                childIdSet.add(child.itemId)
        return ItemKey(childSiteCode, childClassCode, childIdSet)

    def _filterSetGroup(self, key):
        return 'filterset/' + key

    def _makeKey(self, name):
        name = re.sub(r'[^\w\s]','', name)
        return re.sub(r'\s+', '', name)

    def _saveFilterSet(self, key, name):
        group = self._filterSetGroup(key)
        settings = QSettings()
        settings.remove(group)
        settings.setValue(group + '/' + 'Name', name)
        settings.beginWriteArray(group)
        self.dock.toSettings(settings)
        settings.endArray()

    def _deleteFilterSet(self, key):
        group = self._filterSetGroup(key)
        settings = QSettings()
        settings.remove(group)

    def _exportFilterSet(self, key):
        pass

    def _listFilterSets(self):
        filterSets = []
        settings = QSettings()
        settings.beginGroup('filterset')
        groups = settings.childGroups()
        for group in groups:
            settings.beginGroup(group)
            filterSets.append([group, settings.value('Name')])
            settings.endGroup()
        settings.endGroup()
        return filterSets

    def loadFilterSet(self, filterSet='Default'):
        if filterSet in self._listFilterSets():
            self._loadFilterSet(filterSet)
            self.dock.setFilterSet(filterSet)
            self.applyFilters()

    def _loadFilterSet(self, key):
        group = self._filterSetGroup(key)
        settings = QSettings()
        x = settings.beginReadArray(group)
        if x > 0:
            self.dock.fromSettings(settings, x)
        settings.endArray()

    def _saveFilterSetSelected(self, key, name):
        saveName, ok = QInputDialog.getText(None, 'Save Filter Set', 'Enter Name of Filter Set', text=name)
        if ok:
            saveKey = self._makeKey(saveName)
            self._saveFilterSet(saveKey, saveName)
            if saveKey != key:
                self.dock.addFilterSet(saveKey, saveName)
                self.dock.setFilterSet(saveKey)

    def _deleteFilterSetSelected(self, key):
        self._deleteFilterSet(key)
        self.dock.removeFilterSet(key)
        self.loadFilterSet('Default')

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
