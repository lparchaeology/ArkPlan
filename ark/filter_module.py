# -*- coding: utf-8 -*-
"""
/***************************************************************************
                                ARKspatial
                    A QGIS plugin for Archaeological Recording.
        Part of the Archaeological Recording Kit by L - P : Archaeology
                        http://ark.lparchaeology.com
                              -------------------
        copyright            : 2017 by L - P : Heritage LLP
        email                : ark@lparchaeology.com
        copyright            : 2017 by John Layt
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

from PyQt4.QtCore import QObject, QSettings, Qt, pyqtSignal
from PyQt4.QtGui import QInputDialog

from qgis.gui import QgsExpressionBuilderDialog

from ArkSpatial.ark.lib.core import layers

from ArkSpatial.ark.core import Config, FilterClause, FilterSet, FilterType, Settings
from ArkSpatial.ark.core.enum import FilterAction
from ArkSpatial.ark.gui import FilterDock, FilterExportDialog


class FilterModule(QObject):

    filterSetCleared = pyqtSignal()

    def __init__(self, plugin):
        super(FilterModule, self).__init__(plugin)

        self._plugin = plugin  # Plugin()

        # Internal variables
        self.dock = None  # FilterDock()
        self._initialised = False
        self._useGroups = False
        self._filterSetGroupIndex = -1
        self._filterSets = {}  # {str: FilterSet()}
        self._arkFilterSets = {}  # {str: FilterSet()}
        self._schematicFilterSet = FilterSet()  # FilterSet()

    # Standard Dock methods

    # Create the gui when the plugin is first created
    def initGui(self):
        self.dock = FilterDock(self._plugin.iface.mainWindow())
        action = self._plugin.project().addDockAction(
            ':/plugins/ark/filter/filter.png', self.tr(u'Filter Tools'), callback=self.run, checkable=True)
        self.dock.initGui(self._plugin.iface, Qt.LeftDockWidgetArea, action)

        self.dock.filterChanged.connect(self._filterChanged)
        self.dock.filterClauseAdded.connect(self._filterChanged)

        self.dock.buildFilterSelected.connect(self.buildFilter)
        self.dock.buildSelectionSelected.connect(self.buildSelection)
        self.dock.buildHighlightSelected.connect(self.buildHighlight)
        self.dock.clearFilterSelected.connect(self.clearFilters)
        self.dock.clearFilterSelected.connect(self.filterSetCleared)
        self.dock.loadDataSelected.connect(self._loadArkData)
        self.dock.refreshDataSelected.connect(self._refreshArkData)
        self.dock.zoomFilterSelected.connect(self.zoomFilter)

        self.dock.filterSetChanged.connect(self.setFilterSet)
        self.dock.saveFilterSetSelected.connect(self._saveFilterSetSelected)
        self.dock.reloadFilterSetSelected.connect(self._reloadFilterSetSelected)
        self.dock.deleteFilterSetSelected.connect(self._deleteFilterSetSelected)
        self.dock.exportFilterSetSelected.connect(self._exportFilterSetSelected)

    # Load the project settings when project is loaded
    def loadProject(self):
        # Load the Site Codes
        self.dock.initSiteCodes([Settings.siteCode()])

        # Load the Class Codes
        self._loadClassCodes()

        # Load the saved Filter Sets
        self._loadFilterSets()

        # Respond to ARK data load
        self._enableArkData()
        self._plugin.data().dataLoaded.connect(self._activateArkData)

        # Init the schematic filter set
        self._schematicFilterSet = FilterSet.fromSchematic(self._plugin)

        self._initialised = True
        self.setFilterSet('Default')
        return self._initialised

    # Save the project
    def writeProject(self):
        if self.currentFilterSetKey() == 'Default':
            self._saveFilterSet('Default')

    # Close the project
    def closeProject(self):
        self._plugin.data().dataLoaded.disconnect(self._activateArkData)
        # FIXME Doesn't clear on quit as layers already unloaded by main program!
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

    def collection(self):
        return self._plugin.project().collection('plan')

    def _loadClassCodes(self):
        # Load the Class Codes
        codeList = set()
        for key in Config.classCodes:
            classCode = Config.classCodes[key]
            if classCode['collection']:
                codeList.add(key)
            elif classCode['group']:
                codeList.add(classCode['code'])
        codes = {}
        for code in sorted(codeList):
            codes[code] = code
        self.dock.initClassCodes(codes)

    def _enableArkData(self, enable=True):
        if Settings.siteServerUrl():
            self.dock.enableArkData(enable)

    def _activateArkData(self):
        self._loadClassCodes()
        self._loadArkFilterSets()
        self.dock.activateArkData()

    # Filter methods

    def _typeForAction(self, filterAction):
        if (filterAction == FilterAction.IncludeFilter or filterAction == FilterAction.ExclusiveFilter):
            return FilterType.Include
        elif (filterAction == FilterAction.SelectFilter or filterAction == FilterAction.ExclusiveSelectFilter):
            return FilterType.Select
        elif (filterAction == FilterAction.HighlightFilter or filterAction == FilterAction.ExclusiveHighlightFilter):
            return FilterType.Highlight
        elif (filterAction == FilterAction.ExcludeFilter):
            return FilterType.Exclude
        return -1

    def applyItemAction(self, item, filterAction):
        if not self._initialised or filterAction == FilterAction.NoFilterAction:
            return

        if (filterAction == FilterAction.ExclusiveFilter
                or filterAction == FilterAction.ExclusiveSelectFilter
                or filterAction == FilterAction.ExclusiveHighlightFilter):
            self.dock.removeFilters()

        filterType = self._typeForAction(filterAction)

        if filterType >= 0:
            return self.addFilterClause(filterType, item)
        return -1

    def filterItem(self, item):
        if not self._initialised:
            return
        self.dock.removeFilters()
        ret = self.addFilterClause(FilterType.Include, item)
        self.zoomFilter()
        return ret

    def excludeItem(self, item):
        if not self._initialised:
            return
        return self.addFilterClause(FilterType.Exclude, item)

    def highlightItem(self, item):
        if not self._initialised:
            return
        self.dock.removeHighlightFilters()
        return self.addFilterClause(FilterType.Highlight, item)

    def addHighlightItem(self, item):
        if not self._initialised:
            return
        return self.addFilterClause(FilterType.Highlight, item)

    def applySchematicFilter(self, item, filterAction):
        if not self._initialised:
            return
        self._schematicFilterSet.clearClauses()
        cl = FilterClause()
        cl.item = item
        if ((filterAction == FilterAction.SelectFilter or filterAction == FilterAction.ExclusiveSelectFilter
             or filterAction == FilterAction.HighlightFilter or filterAction == FilterAction.ExclusiveHighlightFilter)
                and (self.hasFilterType(FilterType.Include) or self.hasFilterType(FilterType.Exclude))):
            cl.action = FilterType.Include
            self._schematicFilterSet.addClause(cl)
        cl.action = self._typeForAction(filterAction)
        self._schematicFilterSet.addClause(cl)
        self.dock.setSchematicFilterSet(self._schematicFilterSet)
        self._applyFilters()

    def clearSchematicFilter(self):
        if len(self._schematicFilterSet.clauses()) > 0:
            self._schematicFilterSet.clearClauses()
            self.dock.removeSchematicFilters()
            self._applyFilters()

    def addFilterClause(self, filterType, item):
        if not self._initialised:
            return
        clause = FilterClause()
        clause.item = item
        clause.action = filterType
        idx = self.dock.addFilterClause(clause)
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
        if filterString and schematicString:
            self.applyFilter('(' + filterString + ') or (' + schematicString + ')')
        elif schematicString:
            self.applyFilter(schematicString)
        else:
            self.applyFilter(filterString)

        # Selection
        filterString = self.currentFilterSet().selection
        schematicString = self._schematicFilterSet.selection
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
        self.collection().clearHighlight()
        self._applyHighlightClauses(self.currentFilterSet().clauses())
        self._applyHighlightClauses(self._schematicFilterSet.clauses())

    def _applyHighlightClauses(self, clauses):
        for clause in clauses:
            if clause.action == FilterType.Highlight:
                filterItem = self._plugin.data().nodesItem(clause.item)
                self.addHighlight(filterItem.filterClause(), clause.lineColor(), clause.color)

    def clearFilters(self):
        self._filterSets['Default'].clearClauses()
        self.setFilterSet('Default')

    def _clearFilters(self):
        self.collection().clearFilter()
        self.collection().clearSelection()
        self.collection().clearHighlight()

    def applyFilter(self, expression):
        if not self._initialised:
            return
        self.collection().applyFilter(expression)

    def applySelection(self, expression):
        self.collection().applySelection(expression)

    def applyHighlight(self, expression, lineColor=None, fillColor=None):
        self.collection().applyHighlight(expression, lineColor, fillColor, 0.1, 0.1)

    def addHighlight(self, expression, lineColor=None, fillColor=None):
        self.collection().addHighlight(expression, lineColor, fillColor, 0.1, 0.1)

    def buildFilter(self):
        dialog = QgsExpressionBuilderDialog(self.collection().layer('lines'))
        dialog.setExpressionText(self.collection().filter)
        if (dialog.exec_()):
            self.applyFilter(dialog.expressionText())

    def buildSelection(self):
        dialog = QgsExpressionBuilderDialog(self.collection().layer('lines'))
        dialog.setExpressionText(self.collection().selection)
        if (dialog.exec_()):
            self.applySelection(dialog.expressionText())

    def buildHighlight(self):
        dialog = QgsExpressionBuilderDialog(self.collection().layer('lines'))
        dialog.setExpressionText(self.collection().highlight)
        if (dialog.exec_()):
            self.applyHighlight(dialog.expressionText())

    def _loadArkData(self):
        self._plugin.data().loadData()

    def _refreshArkData(self):
        self._plugin.data().refreshData()

    def zoomFilter(self):
        self.collection().zoomToExtent()

    # Filter Set methods

    def currentFilterSet(self):
        key = self.currentFilterSetKey()
        if not key:
            return FilterSet()
        if key[0:4] == 'ark_':
            return self._arkFilterSets[key]
        return self._filterSets[key]

    def currentFilterSetKey(self):
        return self.dock.currentFilterSet()

    def _filterSetGroup(self, key):
        return 'ARK.filterset/' + key

    def _makeKey(self, name):
        name = re.sub(r'[^\w\s]', '', name)
        return re.sub(r'\s+', '', name)

    def _loadFilterSets(self):
        self._filterSets = {}
        settings = QSettings()
        settings.beginGroup('ARK.filterset')
        groups = settings.childGroups()
        settings.endGroup()
        for group in groups:
            filterSet = FilterSet.fromSettings(self._plugin, 'ARK.filterset', group)
            self._filterSets[filterSet.key] = filterSet
        if 'Default' not in self._filterSets:
            filterSet = FilterSet.fromName(self._plugin, 'ARK.filterset', 'Default', 'Default')
            self._filterSets[filterSet.key] = filterSet
        self.dock.initFilterSets(self._filterSets, self._arkFilterSets)

    def _loadArkFilterSets(self):
        self._arkFilterSets = {}
        filters = self._plugin.data().getFilters()
        for key in filters:
            filterSet = FilterSet.fromArk(self._plugin, key, filters[key])
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
        self.dock.setFilterSet(filterSet)
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
            filterSet = FilterSet.fromName(self._plugin, 'ARK.filterset', key, name)
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
            self._filterSetGroupIndex = layers.createLayerGroup(
                self._plugin.iface, Config.filterSetGroupName, Config.projectGroupName)
        layer = self.collection().layer('polygons')
        mem = layers.cloneAsMemoryLayer(layer, name, 'DefaultStyle')
        mem.rendererV2().symbols()[0].setColor(schematicColor)
        mem.startEditing()
        fi = layer.getFeatures()
        for feature in fi:
            if feature.attribute('category') == 'sch':
                mem.addFeature(feature)
        mem.commitChanges()
        mem = layers.addLayerToLegend(self._plugin.iface, mem, self._filterSetGroupIndex)

    def _exportLayers(self, key, name):
        if self._filterSetGroupIndex < 0:
            self._filterSetGroupIndex = layers.createLayerGroup(
                self._plugin.iface, Config.filterSetGroupName, Config.projectGroupName)
        exportGroup = layers.createLayerGroup(self._plugin.iface, name, Config.filterSetGroupName)
        pgMem = layers.duplicateAsMemoryLayer(self.collection().layer('polygons'), key + '_pg')
        plMem = layers.duplicateAsMemoryLayer(self.collection().layer('lines'), key + '_pl')
        ptMem = layers.duplicateAsMemoryLayer(self.collection().layer('points'), key + '_pt')
        layers.addLayerToLegend(self._plugin.iface, pgMem, exportGroup)
        layers.addLayerToLegend(self._plugin.iface, plMem, exportGroup)
        layers.addLayerToLegend(self._plugin.iface, ptMem, exportGroup)
