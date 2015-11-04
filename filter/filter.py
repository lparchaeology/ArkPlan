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

from PyQt4.QtCore import Qt, QObject, QRegExp, QSettings
from PyQt4.QtGui import QAction, QIcon, QFileDialog

from qgis.core import *
from qgis.gui import QgsExpressionBuilderDialog, QgsMessageBar

from ..libarkqgis.map_tools import ArkMapToolIndentifyFeatures

from ..data_model import *

from data_dialog import DataDialog
from filter_export_dialog import FilterExportDialog
from filter_dock import FilterDock
from filter_widget import FilterWidget, FilterType

class Filter(QObject):

    project = None # Project()
    data = None  # DataManager()

    # Internal variables
    initialised = False
    dataLoaded = False
    contextList = []
    _useGroups = False

    identifyMapTool = None  # ArkMapToolIndentifyFeatures()

    def __init__(self, project):
        super(Filter, self).__init__()
        self.project = project
        self.data = DataManager(project)


    # Standard Dock methods

    # Load the module when plugin is loaded
    def load(self):
        self.identifyAction = self.project.addDockAction(':/plugins/ArkPlan/filter/edit-node.png', self.tr(u'Identify contexts'), checkable=True)
        self.identifyAction.triggered.connect(self.triggerIdentifyAction)

        self.dock = FilterDock()
        action = self.project.addDockAction(':/plugins/ArkPlan/filter/view-filter.png', self.tr(u'Filter contexts'), checkable=True)
        self.dock.load(self.project.iface, Qt.LeftDockWidgetArea, action)
        self.dock.toggled.connect(self.run)

        self.dock.filterChanged.connect(self.applyFilters)
        self.dock.buildFilterSelected.connect(self.buildFilter)
        self.dock.buildSelectionSelected.connect(self.buildSelection)
        self.dock.clearFilterSelected.connect(self.clearFilter)
        self.dock.loadDataSelected.connect(self.loadData)
        self.dock.showDataSelected.connect(self.showDataDialogFilter)
        self.dock.zoomFilterSelected.connect(self.zoomFilter)
        self.dock.filterSetChanged.connect(self.setFilterSet)
        self.dock.saveFilterSetSelected.connect(self._saveFilterSetSelected)

        self.identifyMapTool = ArkMapToolIndentifyFeatures(self.project.mapCanvas())
        self.identifyMapTool.setAction(self.identifyAction)
        self.identifyMapTool.featureIdentified.connect(self.showIdentifyDialog)


    # Unload the module when plugin is unloaded
    def unload(self):
        self.saveFilterSet()
        #FIXME Can't clear as layers already unloaded by main program!
        #self.clearFilter()
        self.dock.unload()


    def run(self, checked):
        if checked:
            self.initialise()


    def initialise(self):
        if self.initialised:
            return False

        self.dock.setSiteCodes(self.project.plan.uniqueValues(self.project.fieldName('site')))
        codeList = self.project.plan.uniqueValues(self.project.fieldName('class'))
        if 'cxt' in codeList and self._useGroups:
            codeList.append('sub')
            codeList.append('grp')
        codes = {}
        for code in codeList:
            codes[code] = code
        self.dock.setClassCodes(codes)

        self.loadFilterSet()

        self.initialised = True
        return True


    # Filter methods

    def addFilter(self, filterType, siteCode, classCode, filterRange):
        self.initialise()
        return self.dock.addFilter(filterType, siteCode, classCode, filterRange)

    def removeFilter(self, filterIndex):
        self.dock.removeFilter(filterIndex)

    def hasFilterType(self, filterType):
        return self.dock.hasFilterType(filterType)

    def applyFilters(self):
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


    def applyContextFilter(self, contextRange):
        del self.contextList[:]
        self.contextList = self._rangeToList(contextRange)
        self.project.plan.applyFieldFilterRange(self.project.fieldName('id'), contextRange)
        self.dock.displayFilter(self.project.plan.filter)


    def applySubGroupFilter(self, subRange):
        del self.contextList[:]
        sublist = self._rangeToList(subRange)
        for sub in subList:
            self.contextList.extend(self.data._contextGroupingModel.getContextsForSubGroup(sub))
        self.project.plan.applyFieldFilterList(self.project.fieldName('id'), self.contextList)
        self.dock.displayFilter(self.project.plan.filter)


    def applyGroupFilter(self, groupRange):
        del self.contextList[:]
        groupList = self._rangeToList(groupRange)
        for group in groupList:
            self.contextList.extend(self.data._contextGroupingModel.getContextsForGroup(group))
        self.project.plan.applyFieldFilterList(self.project.fieldName('id'), self.contextList)
        self.dock.displayFilter(self.project.plan.filter)


    def clearFilter(self):
        del self.contextList[:]
        self.applyFilter('')
        self.applySelection('')


    def applyFilter(self, expression):
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
        self.dataLoaded = True


    def zoomFilter(self):
        self.project.plan.zoomToExtent()


    def triggerIdentifyAction(self, checked):
        if checked:
            #if not self.dataLoaded:
                #self.data.loadData()
            self.project.mapCanvas().setMapTool(self.identifyMapTool)
        else:
            self.project.mapCanvas().unsetMapTool(self.identifyMapTool)


    def showIdentifyDialog(self, feature):
        context = feature.attribute(self.project.fieldName('id'))
        self.showDataDialogList([context])


    def showDataDialogFilter(self):
        return self.showDataDialogList(self.contextList)


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

    def setFilterSet(self, name):
        return

    def saveFilterSet(self, name, key):
        group = 'filterset/' + key
        settings = QSettings()
        settings.remove(group)
        settings.beginWriteArray(group)
        self.dock.toSettings(settings)
        settings.endArray()

    def loadFilterSet(self):
        settings = QSettings()
        x = settings.beginReadArray('filterSet')
        self.dock.fromSettings(settings, x)
        settings.endArray()

    def _saveFilterSetSelected(self):
        dialog = FilterExportDialog()
        dialog.setName('')
        if dialog.exec_():
            if dialog.saveFilterSet():
                pass
            elif dialog.exportSchematic():
                pass
            elif dialog.exportData():
                pass
