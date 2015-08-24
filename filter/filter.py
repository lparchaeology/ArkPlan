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

from PyQt4.QtCore import Qt, QObject, QRegExp
from PyQt4.QtGui import QAction, QIcon, QFileDialog

from qgis.core import *
from qgis.gui import QgsExpressionBuilderDialog, QgsMessageBar

from ..arklib.map_tools import ArkMapToolIndentifyFeatures

from ..core.project import Project
from ..core.data_model import *

from data_dialog import DataDialog
from filter_dock import FilterDock

class Filter(QObject):

    project = None # Project()
    data = None  # DataManager()

    # Internal variables
    initialised = False
    dataLoaded = False
    contextList = []

    identifyMapTool = None  # ArkMapToolIndentifyFeatures()

    def __init__(self, project):
        super(Filter, self).__init__()
        self.project = project
        self.data = DataManager(project)


    # Standard Dock methods

    # Load the module when plugin is loaded
    def load(self):
        self.identifyAction = self.project.plugin.addAction(':/plugins/ArkPlan/filter/edit-node.png', self.tr(u'Identify contexts'), checkable=True)
        self.identifyAction.triggered.connect(self.triggerIdentifyAction)

        self.dock = FilterDock()
        action = self.project.plugin.addAction(':/plugins/ArkPlan/filter/view-filter.png', self.tr(u'Filter contexts'), checkable=True)
        self.dock.load(self.project.plugin.iface, Qt.LeftDockWidgetArea, action)
        self.dock.toggled.connect(self.run)

        self.dock.contextFilterChanged.connect(self.applyContextFilter)
        self.dock.subGroupFilterChanged.connect(self.applySubGroupFilter)
        self.dock.groupFilterChanged.connect(self.applyGroupFilter)
        self.dock.buildFilterSelected.connect(self.buildFilter)
        self.dock.clearFilterSelected.connect(self.clearFilter)
        self.dock.loadDataSelected.connect(self.loadData)
        self.dock.showDataSelected.connect(self.showDataDialogFilter)
        self.dock.zoomFilterSelected.connect(self.zoomFilter)

        self.identifyMapTool = ArkMapToolIndentifyFeatures(self.project.plugin.mapCanvas())
        self.identifyMapTool.setAction(self.identifyAction)
        self.identifyMapTool.featureIdentified.connect(self.showIdentifyDialog)


    # Unload the module when plugin is unloaded
    def unload(self):
        self.dock.unload()


    def run(self, checked):
        if checked:
            self.initialise()


    def initialise(self):
        if self.initialised:
            return

        self.project.initialise()
        if (not self.project.isInitialised()):
            return
        self.dock.showPointsChanged.connect(self.project.plan.showPoints)
        self.dock.showLinesChanged.connect(self.project.plan.showLines)
        self.dock.showPolygonsChanged.connect(self.project.plan.showPolygons)

        self.initialised = True


    # Filter methods

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


    def applyFilter(self, filter):
        self.project.plan.applyFilter(filter)
        self.dock.displayFilter(self.project.plan.filter)


    def buildFilter(self):
        dialog = QgsExpressionBuilderDialog(self.project.plan.linesLayer)
        dialog.setExpressionText(self.project.plan.filter)
        if (dialog.exec_()):
            self.applyFilter(dialog.expressionText())


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
            self.project.plugin.mapCanvas().setMapTool(self.identifyMapTool)
        else:
            self.project.plugin.mapCanvas().unsetMapTool(self.identifyMapTool)


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
        dataDialog = DataDialog(self.project.plugin.iface.mainWindow())
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
