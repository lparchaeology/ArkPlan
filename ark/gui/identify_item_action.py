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

from qgis.PyQt.QtCore import pyqtSignal
from qgis.PyQt.QtWidgets import QAction, QMenu

from qgis.core import Qgis

from ArkSpatial.ark.lib.gui import ClipboardAction

from ArkSpatial.ark.core import Config, Item, Settings, Source

from .open_ark_action import OpenArkAction


class IdentifyItemAction(QAction):

    openInArkSelected = pyqtSignal(object)
    editItemSelected = pyqtSignal(object)
    deleteItemSelected = pyqtSignal(object)
    panToItemSelected = pyqtSignal(object)
    zoomToItemSelected = pyqtSignal(object)
    filterItemSelected = pyqtSignal(object)
    excludeFilterItemSelected = pyqtSignal(object)
    highlightItemSelected = pyqtSignal(object)
    addHighlightItemSelected = pyqtSignal(object)
    openDrawingsSelected = pyqtSignal(object)

    def __init__(self, item, plugin, parent=None):
        super().__init__(parent)

        self._iface = plugin.iface
        self.item = item

        self.setText(item.itemLabel())
        menu = QMenu()
        sourceSet = set()
        area = []
        haveSchematic = False
        sectionSchematics = []
        for feature in plugin.project().collection('plan').layer('polygons').getFeatures(item.featureRequest()):
            category = feature.attribute('category')
            if category == 'sch' or category == 'scs':
                haveSchematic = True
                source = Source()
                source.fromFeature(feature)
                if source.isValid():
                    sourceSet.add(source)
                if category == 'sch':
                    area.append(feature.geometry().area())
        sourceDict = {}
        for source in sourceSet:
            if source.sourceCode not in sourceDict:
                sourceDict[source.sourceCode] = set()
            sourceDict[source.sourceCode].add(source.items)
        self.zoomAction = QAction('Zoom to Item', parent)
        self.zoomAction.triggered.connect(self._zoomToItem)
        menu.addAction(self.zoomAction)
        self.panAction = QAction('Pan to Item', parent)
        self.panAction.triggered.connect(self._panToItem)
        menu.addAction(self.panAction)
        self.filterAction = QAction('Filter Item', parent)
        self.filterAction.triggered.connect(self._filterItem)
        menu.addAction(self.filterAction)
        self.excludeFilterAction = QAction('Exclude Item from Filter', parent)
        self.excludeFilterAction.triggered.connect(self._excludeFilterItem)
        menu.addAction(self.excludeFilterAction)
        self.highlightAction = QAction('Select Item', parent)
        self.highlightAction.triggered.connect(self._highlightItem)
        menu.addAction(self.highlightAction)
        self.addHighlightAction = QAction('Add Item to Selection', parent)
        self.addHighlightAction.triggereConfigd.connect(self._addHighlightItem)
        menu.addAction(self.addHighlightAction)
        if Settings.siteServerUrl():
            self.linkAction = OpenArkAction(Settimgs.siteServerUrl(), item, 'Open in ARK', parent)
            menu.addAction(self.linkAction)
        self.drawingAction = QAction('Open Drawings', parent)
        self.drawingAction.triggered.connect(self._openDrawings)
        menu.addAction(self.drawingAction)
        menu.addSeparator()
        self.editAction = QAction('Edit Item', parent)
        self.editAction.triggered.connect(self._editItem)
        menu.addAction(self.editAction)
        self.deleteAction = QAction('Delete Item', parent)
        self.deleteAction.triggered.connect(self._deleteItem)
        menu.addAction(self.deleteAction)
        menu.addSeparator()
        if len(sourceDict) > 0:
            for sourceCode in list(sourceDict.keys()):
                menu.addAction(Config.sourceCodes[sourceCode]['label'] + ':')
                sources = sorted(sourceDict[sourceCode])
                for item in sources:
                    if item.isValid():
                        menu.addAction(item.itemLabel())
        elif haveSchematic:
            menu.addAction('Unknown Source')
        else:
            menu.addAction('No Schematic')
        if item.classCode() == 'context':
            subItem = plugin.data().parentItem(item)
            if subItem and subItem.isValid():
                menu.addSeparator()
                grpItem = plugin.data().parentItem(subItem)
                if Settings.siteServerUrl():
                    self.subAction = OpenArkAction(
                        Settings.siteServerUrl(), subItem, 'Sub-group: ' + str(subItem.itemId()), parent)
                    menu.addAction(self.subAction)
                    if grpItem:
                        self.grpAction = OpenArkAction(
                            Settings.siteServerUrl(), grpItem, 'Group: ' + str(grpItem.itemId()), parent)
                        menu.addAction(self.grpAction)
                else:
                    menu.addAction('Sub-group: ' + str(subItem.itemId()))
                    if grpItem:
                        menu.addAction('Group: ' + str(grpItem.itemId()))
        if len(area) > 0:
            menu.addSeparator()
            tot = 0
            for a in area:
                tot += a
            units = self._iface.mapCanvas().mapUnits()
            suffix = ''
            if units == Qgis.Meters:
                suffix = ' m²'
            elif units == Qgis.Feet:
                suffix = ' ft²'
            elif units == Qgis.NauticalMiles:
                suffix = ' NM²'
            menu.addAction(ClipboardAction('Area: ', '%.3f' % tot + suffix, parent))
        self.setMenu(menu)

    def _editItem(self):
        self.editItemSelected.emit(self.item)

    def _deleteItem(self):
        self.deleteItemSelected.emit(self.item)

    def _panToItem(self):
        self.panToItemSelected.emit(self.item)

    def _zoomToItem(self):
        self.zoomToItemSelected.emit(self.item)

    def _filterItem(self):
        self.filterItemSelected.emit(self.item)

    def _excludeFilterItem(self):
        self.excludeFilterItemSelected.emit(self.item)

    def _highlightItem(self):
        self.highlightItemSelected.emit(self.item)

    def _addHighlightItem(self):
        self.addHighlightItemSelected.emit(self.item)

    def _openDrawings(self):
        self.openDrawingsSelected.emit(self.item)
