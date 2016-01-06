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
from ..libarkqgis import layers

from data_model import *
from data_dialog import DataDialog
from filter_export_dialog import FilterExportDialog
from filter_dock import FilterDock
from filter_widget import FilterWidget, FilterType, FilterAction
from config import Config

import resources_rc

class Filter(QObject):

    filterSetCleared = pyqtSignal()

    project = None # Project()
    data = None  # DataManager()

    # Internal variables
    dock = None # FilterDock()
    _initialised = False
    _dataLoaded = False
    _useGroups = False
    _filterSetGroupIndex = -1

    def __init__(self, project):
        super(Filter, self).__init__(project)
        self.project = project
        self.data = DataManager(project)

    # Standard Dock methods

    # Create the gui when the plugin is first created
    def initGui(self):
        self.dock = FilterDock(self.project.layerDock)
        action = self.project.addDockAction(':/plugins/ark/filter/filter.png', self.tr(u'Filter contexts'), callback=self.run, checkable=True)
        self.dock.initGui(self.project.iface, Qt.LeftDockWidgetArea, action)

        self.dock.filterChanged.connect(self.applyFilters)
        self.dock.buildFilterSelected.connect(self.buildFilter)
        self.dock.buildSelectionSelected.connect(self.buildSelection)
        self.dock.clearFilterSelected.connect(self.clearFilterSet)
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
        self.dock.initSiteCodes(self.project.plan.uniqueValues(self.project.fieldName('site')))

        # Load the Class Codes
        codeList = self.project.plan.uniqueValues(self.project.fieldName('class'))
        if 'cxt' in codeList and self._useGroups:
            codeList.append('sub')
            codeList.append('grp')
        codes = {}
        for code in codeList:
            codes[code] = code
        self.dock.initClassCodes(codes)

        # Load the saved Filter Sets
        self.dock.initFilterSets(self._listFilterSets())

        self._initialised = True
        self.loadFilterSet('Default')
        self.dock.menuAction().setChecked(False)
        return self._initialised

    # Save the project
    def writeProject(self):
        if self.dock.currentFilterSet() == 'Default':
            self._saveFilterSet('Default', 'Default')

    # Close the project
    def closeProject(self):
        self.writeProject()
        #FIXME Doesn't clear on quit as layers already unloaded by main program!
        self.clearFilterSet()
        # Reset the initialisation
        self._initialised = False
        self._dataLoaded = False

    # Unload the gui when the plugin is unloaded
    def unloadGui(self):
        self.dock.unloadGui()

    def run(self, checked):
        if checked and not self._initialised:
            self.dock.menuAction().setChecked(False)

    # Filter methods

    def addFilter(self, filterType, siteCode, classCode, filterRange, filterAction=FilterAction.RemoveFilter):
        if not self._initialised:
            return
        return self.dock.addFilter(filterType, siteCode, classCode, filterRange, filterAction)

    def removeFilter(self, filterIndex):
        if not self._initialised:
            return
        self.dock.removeFilter(filterIndex)

    def removeFilters(self):
        if not self._initialised:
            return
        return self.dock.removeFilters()

    def removeHighlightFilters(self):
        if not self._initialised:
            return
        return self.dock.removeHighlightFilters()

    def hasFilterType(self, filterType):
        if not self._initialised:
            return
        return self.dock.hasFilterType(filterType)

    def applyFilters(self):
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
                clause = self._rangeToClause(self.dock.siteCode(), filter.classCode(), filter.filterRange())
                if filter.filterType() == FilterType.HighlightFilter:
                    if firstSelect:
                        firstSelect = False
                    else:
                        selectString += ' or '
                    selectString += clause
                elif filter.filterType() == FilterType.ExcludeFilter:
                    if firstExclude:
                        firstExclude = False
                    else:
                        excludeString += ' or '
                    excludeString += clause
                else:
                    if firstInclude:
                        firstInclude = False
                    else:
                        includeString += ' or '
                    includeString += clause
        if includeString and excludeString:
            self.applyFilter('(' + includeString + ') and NOT (' + excludeString + ')')
        elif excludeString:
            self.applyFilter('NOT (' + excludeString + ')')
        else:
            self.applyFilter(includeString)
        self.applySelection(selectString)


    def clearFilterSet(self):
        if not self._initialised:
            return
        self.project.plan.clearFilter()
        self.project.plan.clearSelection()


    def applyFilter(self, expression):
        if not self._initialised:
            return
        self.project.plan.applyFilter(expression)


    def applySelection(self, expression):
        self.project.plan.applySelection(expression)


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
        self.data._contextProxyModel.setFilterRegExp(self._listToRegExp(contextList))
        dataDialog.contextTableView.resizeColumnsToContents()
        dataDialog.subGroupTableView.setModel(self.data._subGroupProxyModel)
        self.data._subGroupProxyModel.setFilterRegExp(self._listToRegExp(subList))
        dataDialog.subGroupTableView.resizeColumnsToContents()
        dataDialog.groupTableView.setModel(self.data._groupProxyModel)
        self.data._groupProxyModel.setFilterRegExp(self._listToRegExp(groupList))
        dataDialog.groupTableView.resizeColumnsToContents()
        return dataDialog.exec_()


    def _rangeToList(self, valueRange):
        lst = []
        for clause in valueRange.split():
            if clause.find('-') >= 0:
                valueList = clause.split('-')
                for i in range(int(valueList[0]), int(valueList[1])):
                    lst.append(i)
            else:
                lst.append(int(clause))
        return lst


    def _listToRegExp(self, lst):
        if (len(lst) < 1):
            return QRegExp()
        exp = str(lst[0])
        if (len(lst) > 1):
            for element in lst[1:]:
                exp = exp + '|' + str(element)
        return QRegExp('\\b(' + exp + ')\\b')


    def _rangeToClause(self, siteCode, filterClass, filterRange):
        if siteCode is None or filterClass is None or filterRange is None:
            return ''
        clause = '("' + self.project.fieldName('site') + '" = \'' + siteCode + '\''
        clause = clause + ' and "' + self.project.fieldName('class') + '" = \'' + filterClass + '\''
        subs = filterRange.split()
        if len(subs) == 0:
            clause += ')'
            return clause
        clause += ' and ('
        first = True
        for sub in subs:
            if first:
                first = False
            else:
                clause = clause + ' or '
            field = self.project.fieldName('id')
            if sub.find('-') >= 0:
                vals = sub.split('-')
                clause = clause + ' ("' + field + '" >= ' + vals[0] + ' and "' + field + '" <= ' + vals[1] + ')'
            else:
                clause = clause + '"' + field + '" = ' + sub
        clause += '))'
        return clause

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
        self._loadFilterSet(filterSet)
        self.dock.setFilterSet(filterSet)
        self.applyFilters()

    def _loadFilterSet(self, key):
        group = self._filterSetGroup(key)
        settings = QSettings()
        x = settings.beginReadArray(group)
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
