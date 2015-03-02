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

import csv

from PyQt4.QtCore import Qt, QVariant, QFileInfo, QObject, QDir
from PyQt4.QtGui import QAction, QIcon, QFileDialog

from qgis.core import *

from ..core.settings import Settings
from ..core.layers import LayerManager
from ..core.data_model import *

from filter_dock import FilterDock

class Filter(QObject):

    # Project settings
    settings = None # Settings()

    # Internal variables
    initialised = False

    layers = None  # LayerManager

    arkDataDir = QDir('/Users/odysseus/Dropbox/LP Archaeology/context_data')
    arkGroupDataFilename = 'PCO06_ark_groups.csv'
    arkSubGroupDataFilename = 'PCO06_ark_subgroups.csv'
    arkContextDataFilename = 'PCO06_ark_contexts.csv'

    filter = ''

    _contextGroupingModel = ContextGroupingModel()
    _contextModel = ContextModel()
    _subGroupModel = SubGroupModel()
    _groupModel = GroupModel()

    def __init__(self, settings, layers):
        super(Filter, self).__init__()
        self.settings = settings
        self.layers = layers


    def initGui(self):
        self.dock = FilterDock()
        self.dock.load(self.settings, Qt.LeftDockWidgetArea, self.tr(u'Filter context layers'), ':/plugins/Ark/icon.png')
        self.dock.toggled.connect(self.run)

        self.dock.contextFilterChanged.connect(self.applyContextFilter)
        self.dock.subGroupFilterChanged.connect(self.applySubGroupFilter)
        self.dock.groupFilterChanged.connect(self.applyGroupFilter)
        self.dock.buildFilterSelected.connect(self.buildFilter)
        self.dock.clearFilterSelected.connect(self.clearFilter)
        self.dock.loadDataSelected.connect(self.loadData)
        self.dock.zoomSelected.connect(self.zoomFilter)


    def unload(self):

        # Unload the dock
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

        self.initialised = True


    # Filter methods

    def applyContextFilter(self, contextList):
        clause = '"' + self.settings.contextAttributeName + '" = %d'
        filter = ''
        if (len(contextList) > 0):
            filter += clause % contextList[0]
            for context in contextList[1:]:
                filter += ' or '
                filter += clause % context
        self.filter = filter
        self.applyFilter()


    def applySubGroupFilter(self, subList):
        contextList = []
        for sub in subList:
            contextList.extend(self._contextGroupingModel.getContextsForSubGroup(sub))
        self.applyContextFilter(contextList)


    def applyGroupFilter(self, groupList):
        contextList = []
        for group in groupList:
            contextList.extend(self._contextGroupingModel.getContextsForGroup(group))
        self.applyContextFilter(contextList)


    def clearFilter(self):
        self.filter = ''
        self.applyFilter()


    def setFilter(self, filter):
        self.filter = filter
        self.applyFilter()


    def applyFilter(self):
        self.applyLayerFilter(self.layers.pointsLayer)
        self.applyLayerFilter(self.layers.linesLayer)
        self.applyLayerFilter(self.layers.polygonsLayer)
        self.applyLayerFilter(self.layers.schematicLayer)
        self.dock.displayFilter(self.filter)


    def applyLayerFilter(self, layer):
        if (self.settings.iface.mapCanvas().isDrawing()):
            QMessageBox.information(self.dock, 'applyLayerFilter', 'Cannot apply filter: Canvas is drawing')
            return
        if (layer is None):
            QMessageBox.information(self.dock, 'applyLayerFilter', 'Cannot apply filter: Layer is invalid')
            return
        if (layer.type() != QgsMapLayer.VectorLayer):
            QMessageBox.information(self.dock, 'applyLayerFilter', 'Cannot apply filter: Not a vector layer')
            return
        if (layer.isEditable()):
            QMessageBox.information(self.dock, 'applyLayerFilter', 'Cannot apply filter: Layer is in editing mode')
            return
        if (not layer.dataProvider().supportsSubsetString()):
            QMessageBox.information(self.dock, 'applyLayerFilter', 'Cannot apply filter: Subsets not supported by layer')
            return
        if (len(layer.vectorJoins()) > 0):
            QMessageBox.information(self.dock, 'applyLayerFilter', 'Cannot apply filter: Layer has joins')
            return
        layer.setSubsetString(self.filter)
        self.settings.iface.mapCanvas().refresh()
        self.settings.iface.legendInterface().refreshLayerSymbology(layer)


    def buildFilter(self):
        dialog = QgsExpressionBuilderDialog(self.layers.linesLayer)
        dialog.setExpressionText(self.filter)
        if (dialog.exec_()):
            self.setFilter(dialog.expressionText())


    def loadData(self):
        self._contextGroupingModel.clear()
        self._contextModel.clear()
        self._subGroupModel.clear()
        self._groupModel.clear()
        subToGroup = {}
        subToGroup[0] = 0
        with open(self.arkDataDir.absolutePath() + '/' + self.arkGroupDataFilename) as csvFile:
            reader = csv.DictReader(csvFile)
            for record in reader:
                pass
                #self._groupModel.addGroup(record)
        with open(self.arkDataDir.absolutePath() + '/' + self.arkSubGroupDataFilename) as csvFile:
            reader = csv.DictReader(csvFile)
            for record in reader:
                sub_group_string = record['sub_group']
                sub_group_no = int(sub_group_string.split('_')[-1])
                group_string = record['strat_group']
                group_no = 0
                if group_string:
                    group_no = int(group_string.split('_')[-1])
                subToGroup[sub_group_no] = group_no
                #self._subGroupModel.addSubGroup(record)
        with open(self.arkDataDir.absolutePath() + '/' + self.arkContextDataFilename) as csvFile:
            reader = csv.DictReader(csvFile)
            for record in reader:
                context_string = record['context']
                context_no = int(context_string.split('_')[-1])
                sub_group_string = record['sub_group']
                sub_group_no = 0
                if sub_group_string:
                    sub_group_no = int(sub_group_string.split('_')[-1])
                self._contextGroupingModel.addGrouping(context_no, sub_group_no, subToGroup[sub_group_no])
                #self._contextModel.addContext(record)
        self.dock.enableGroupFilters(True)

    def zoomFilter(self):
        self.layers.pointsLayer.updateExtents()
        self.layers.linesLayer.updateExtents()
        self.layers.polygonsLayer.updateExtents()
        self.layers.schematicLayer.updateExtents()
        extent = QgsRectangle()
        extent = self.extendExtent(extent, self.layers.pointsLayer)
        extent = self.extendExtent(extent, self.layers.linesLayer)
        extent = self.extendExtent(extent, self.layers.polygonsLayer)
        extent = self.extendExtent(extent, self.layers.schematicLayer)
        if not extent.isNull():
            extent.scale(1.05)
            self.settings.iface.mapCanvas().setExtent(extent)
            self.settings.iface.mapCanvas().refresh()


    def extendExtent(self, extent, layer):
        if not self.settings.iface.legendInterface().isLayerVisible(layer):
            return extent
        if (extent is None or extent.isNull()):
            return layer.extent()
        return extent.combineExtentWith(layer.extent())
