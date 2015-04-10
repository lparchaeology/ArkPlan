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

from ..core.settings import Settings
from ..core.layers import LayerManager
from ..core.data_model import *
from ..core.map_tools import MapToolIndentifyFeatures

from data_dialog import DataDialog
from filter_dock import FilterDock

class Filter(QObject):

    settings = None # Settings()
    layers = None  # LayerManager()
    data = None  # DataManager()

    # Internal variables
    initialised = False
    dataLoaded = False
    contextList = []

    identifyMapTool = None  # MapToolIndentifyFeatures()

    def __init__(self, settings, layers):
        super(Filter, self).__init__()
        self.settings = settings
        self.layers = layers
        self.data = DataManager(settings)


    # Standard Dock methods

    # Load the module when plugin is loaded
    def load(self):
        self.identifyAction = self.settings.createMenuAction(self.settings.iface, self.tr(u'Identify contexts'), ':/plugins/Ark/filter/edit-node.png', True)
        self.identifyAction.triggered.connect(self.triggerIdentifyAction)

        self.dock = FilterDock()
        self.dock.load(self.settings.iface, Qt.LeftDockWidgetArea, self.settings.createMenuAction(self.tr(u'Filter contexts'), ':/plugins/Ark/filter/view-filter.png', True))
        self.dock.toggled.connect(self.run)

        self.dock.contextFilterChanged.connect(self.applyContextFilter)
        self.dock.subGroupFilterChanged.connect(self.applySubGroupFilter)
        self.dock.groupFilterChanged.connect(self.applyGroupFilter)
        self.dock.buildFilterSelected.connect(self.buildFilter)
        self.dock.clearFilterSelected.connect(self.clearFilter)
        self.dock.loadDataSelected.connect(self.loadData)
        self.dock.showDataSelected.connect(self.showDataDialogFilter)
        self.dock.zoomSelected.connect(self.zoomFilter)

        self.identifyMapTool = MapToolIndentifyFeatures(self.settings.iface.mapCanvas())
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

        if (not self.settings.isConfigured()):
            self.settings.configure()
        self.layers.initialise()
        self.dock.showPointsChanged.connect(self.layers.contexts.showPoints)
        self.dock.showLinesChanged.connect(self.layers.contexts.showLines)
        self.dock.showPolygonsChanged.connect(self.layers.contexts.showPolygons)
        self.dock.showSchematicsChanged.connect(self.layers.contexts.showScope)

        self.initialised = True


    # Filter methods

    def applyContextFilter(self, contextList):
        del self.contextList[:]
        self.contextList = contextList
        self.layers.applyContextFilter(self.contextList)
        self.dock.displayFilter(self.layers.filter)


    def applySubGroupFilter(self, subList):
        del self.contextList[:]
        for sub in subList:
            self.contextList.extend(self.data._contextGroupingModel.getContextsForSubGroup(sub))
        self.layers.applyContextFilter(self.contextList)
        self.dock.displayFilter(self.layers.filter)


    def applyGroupFilter(self, groupList):
        del self.contextList[:]
        for group in groupList:
            self.contextList.extend(self.data._contextGroupingModel.getContextsForGroup(group))
        self.layers.applyContextFilter(self.contextList)
        self.dock.displayFilter(self.layers.filter)


    def clearFilter(self):
        del self.contextList[:]
        self.applyFilter('')


    def applyFilter(self, filter):
        self.layers.applyFilter(filter)
        self.dock.displayFilter(self.layers.filter)


    def buildFilter(self):
        dialog = QgsExpressionBuilderDialog(self.layers.linesLayer)
        dialog.setExpressionText(self.layers.filter)
        if (dialog.exec_()):
            self.applyFilter(dialog.expressionText())


    def loadData(self):
        self.data.loadData()
        self.dock.enableGroupFilters(True)
        self.dataLoaded = True


    def zoomFilter(self):
        self.layers.zoomToLayers(False)


    def triggerIdentifyAction(self, checked):
        if checked:
            if not self.dataLoaded:
                self.data.loadData()
            self.settings.iface.mapCanvas().setMapTool(self.identifyMapTool)
        else:
            self.settings.iface.mapCanvas().unsetMapTool(self.identifyMapTool)


    def showIdentifyDialog(self, feature):
        context = feature.attribute(self.settings.contextAttributeName)
        self.showDataDialogList([context])


    def showDataDialogFilter(self):
        return self.showDataDialogList(self.contextList)


    def showDataDialogList(self, contextList):
        subList = []
        groupList = []
        for context in contextList:
            subList.append(self.data.subGroupForContext(context))
            groupList.append(self.data.groupForContext(context))
        dataDialog = DataDialog(self, self.settings.iface.mainWindow())
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


    def _listToRegExp(self, lst):
        if (len(lst) < 1):
            return QRegExp()
        exp = str(lst[0])
        if (len(lst) > 1):
            for element in lst[1:]:
                exp = exp + '|' + str(element)
        return QRegExp('\\b(' + exp + ')\\b')
