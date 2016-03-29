# -*- coding: utf-8 -*-
"""
/***************************************************************************
                                ARK Spatial
                    A QGIS plugin for Archaeological Recording.
        Part of the Archaeological Recording Kit by L-P : Archaeology
                        http://ark.lparchaeology.com
                              -------------------
        begin                : 2016-03-11
        git sha              : $Format:%H$
        copyright            : 2016 by L-P : Heritage LLP
        email                : ark@lparchaeology.com
        copyright            : 2016 by John Layt
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
from PyQt4.QtCore import Qt, pyqtSignal, QUrl
from PyQt4.QtGui import QWidget, QPixmap, QToolButton, QAction, QIcon, QMenu, QActionGroup
from PyQt4.QtWebKit import QWebPage

from ..libarkqgis.dock import ToolDockWidget
from ..libarkqgis.project import Project
from ..libarkqgis import utils

from enum import *
from config import Config
from plan_item import ItemKey

import data_widget_base

import resources

class DataWidget(QWidget, data_widget_base.Ui_DataWidget):

    def __init__(self, parent=None):
        super(DataWidget, self).__init__(parent)
        self.setupUi(self)

class DataDock(ToolDockWidget):

    itemChanged = pyqtSignal()
    loadDataSelected = pyqtSignal()
    refreshDataSelected = pyqtSignal()
    firstItemSelected = pyqtSignal()
    prevItemSelected = pyqtSignal()
    openItemData = pyqtSignal()
    nextItemSelected = pyqtSignal()
    lastItemSelected = pyqtSignal()
    showItemSelected = pyqtSignal()
    zoomItemSelected = pyqtSignal()
    filterItemSelected = pyqtSignal()
    editItemSelected = pyqtSignal()
    loadDrawingsSelected = pyqtSignal()
    itemLinkClicked = pyqtSignal(object)
    mapActionChanged = pyqtSignal(int)
    filterActionChanged = pyqtSignal(int)
    drawingActionChanged = pyqtSignal(int)

    def __init__(self, parent=None):
        super(DataDock, self).__init__(DataWidget(), parent)

        self.setWindowTitle(u'ARK Data')
        self.setObjectName(u'DataDock')

    def initGui(self, iface, location, menuAction):
        super(DataDock, self).initGui(iface, location, menuAction)

        for key in sorted(Config.classCodes.keys()):
            classCode = Config.classCodes[key]
            self.widget.classCodeCombo.addItem(classCode['label'], classCode['code'])

        self._showItemAction = QAction(QIcon(':/plugins/ark/filter/showContext.png'), self.tr(u'Show Item'), self)
        self._showItemAction.triggered.connect(self.showItemSelected)
        self.toolbar.addAction(self._showItemAction)

        self._zoomItemAction = QAction(QIcon(':/plugins/ark/plan/zoomToItem.svg'), "Zoom to item", self)
        self._zoomItemAction.triggered.connect(self.zoomItemSelected)
        self.toolbar.addAction(self._zoomItemAction)

        self._filterItemAction = QAction(QIcon(':/plugins/ark/filter/filter.png'), "Filter item", self)
        self._filterItemAction.triggered.connect(self.filterItemSelected)
        self.toolbar.addAction(self._filterItemAction)

        self._loadItemDrawingsAction = QAction(QIcon(':/plugins/ark/plan/loadDrawings.svg'), "Load Drawings", self)
        self._loadItemDrawingsAction.triggered.connect(self.loadDrawingsSelected)
        self.toolbar.addAction(self._loadItemDrawingsAction)

        self._editItemAction = QAction(Project.getThemeIcon('mActionToggleEditing.svg'), "Edit Item", self)
        self._editItemAction.triggered.connect(self.editItemSelected)
        self.toolbar.addAction(self._editItemAction)

        self._mapActionGroup = QActionGroup(self)
        self._noMapAction = self._addMapAction(MapAction.NoMapAction, 'No map action')
        self._zoomMapAction = self._addMapAction(MapAction.ZoomMap, 'Zoom map view')
        self._panMapAction = self._addMapAction(MapAction.PanMap, 'Pan map view')
        self._moveMapAction = self._addMapAction(MapAction.MoveMap, 'Move map view')
        self._moveMapAction.setChecked(True)

        self._filterActionGroup = QActionGroup(self)
        self._noFilterAction = self._addFilterAction(FilterAction.NoFilterAction, 'No filter action')
        self._includeFilterAction = self._addFilterAction(FilterAction.IncludeFilter, 'Add to filter')
        self._exclusiveFilterAction = self._addFilterAction(FilterAction.ExclusiveFilter, 'Exclusive filter')
        self._selectFilterAction = self._addFilterAction(FilterAction.SelectFilter, 'Add to selection')
        self._exclusiveSelectFilterAction = self._addFilterAction(FilterAction.ExclusiveSelectFilter, 'Exclusive selection')
        self._highlightFilterAction = self._addFilterAction(FilterAction.HighlightFilter, 'Add to highlight')
        self._exclusiveHighlightFilterAction = self._addFilterAction(FilterAction.ExclusiveHighlightFilter, 'Exclusive highlight')
        self._exclusiveHighlightFilterAction.setChecked(True)

        self._drawingActionGroup = QActionGroup(self)
        self._noDrawingAction = self._addDrawingAction(FilterAction.NoFilterAction, 'No drawing action')
        self._noDrawingAction.setChecked(True)
        self._loadDrawingsAction = self._addDrawingAction(FilterAction.IncludeFilter, 'Load drawings')
        self._addDrawingsAction = self._addDrawingAction(FilterAction.ExclusiveFilter, 'Add drawings')

        self._settingsMenu = QMenu(self)
        self._settingsMenu.addActions(self._mapActionGroup.actions())
        self._settingsMenu.addSeparator()
        self._settingsMenu.addActions(self._filterActionGroup.actions())
        self._settingsMenu.addSeparator()
        self._settingsMenu.addActions(self._drawingActionGroup.actions())

        self.toolbar.addSeparator()
        self._settingsAction = QAction(QIcon(':/plugins/ark/settings.svg'), "Action Settings", self)
        self._settingsAction.setMenu(self._settingsMenu)
        self._settingsTool = QToolButton()
        self._settingsTool.setDefaultAction(self._settingsAction)
        self._settingsTool.setPopupMode(QToolButton.InstantPopup)
        self.toolbar.addWidget(self._settingsTool)

        self.toolbar2.setVisible(True)

        self._loadDataAction = QAction(QIcon(':/plugins/ark/data/loadData.svg'), "Load Data", self)
        self._loadDataAction.triggered.connect(self.loadDataSelected)
        self.toolbar2.addAction(self._loadDataAction)

        self._refreshDataAction = QAction(QIcon(':/plugins/ark/data/refreshData.svg'), "Refresh Data", self)
        self._refreshDataAction.triggered.connect(self.refreshDataSelected)
        self.toolbar2.addAction(self._refreshDataAction)

        self._firstItemAction = QAction(QIcon(':/plugins/ark/data/goFirstItem.svg'), "Go to first item", self)
        self._firstItemAction.triggered.connect(self.firstItemSelected)
        self.toolbar2.addAction(self._firstItemAction)

        self._previousItemAction = QAction(QIcon(':/plugins/ark/data/goPrevItem.svg'), "Go to previous item", self)
        self._previousItemAction.triggered.connect(self.prevItemSelected)
        self.toolbar2.addAction(self._previousItemAction)

        self._openItemAction = QAction(QIcon(':/plugins/ark/data/openData.svg'), "Open item in ARK", self)
        self._openItemAction.triggered.connect(self.openItemData)
        self.toolbar2.addAction(self._openItemAction)

        self._nextItemAction = QAction(QIcon(':/plugins/ark/data/goNextItem.svg'), "Go to next item", self)
        self._nextItemAction.triggered.connect(self.nextItemSelected)
        self.toolbar2.addAction(self._nextItemAction)

        self._lastItemAction = QAction(QIcon(':/plugins/ark/data/goLastItem.svg'), "Go to last item", self)
        self._lastItemAction.triggered.connect(self.lastItemSelected)
        self.toolbar2.addAction(self._lastItemAction)

        self.setItemNavEnabled(False)

        self.widget.siteCodeCombo.currentIndexChanged.connect(self._itemChanged)
        self.widget.classCodeCombo.currentIndexChanged.connect(self._itemChanged)
        self.widget.itemIdSpin.editingFinished.connect(self._itemChanged)

        self.widget.itemDataView.page().setLinkDelegationPolicy(QWebPage.DelegateAllLinks)
        self.widget.itemDataView.linkClicked.connect(self._linkClicked)

    def initSiteCodes(self, siteCodes):
        self.widget.siteCodeCombo.clear()
        for site in siteCodes:
            self.widget.siteCodeCombo.addItem(site)

    def item(self):
        return ItemKey(self.siteCode(), self.classCode(), self.itemId())

    def setItem(self, item):
        if item.isInvalid():
            return
        self.blockSignals(True)
        idx = self.widget.siteCodeCombo.findData(item.siteCode)
        if idx >= 0:
            self.widget.siteCodeCombo.setCurrentIndex(idx)

        idx = self.widget.classCodeCombo.findData(item.classCode)
        if idx >= 0:
            self.widget.classCodeCombo.setCurrentIndex(idx)

        if (item.itemId.isdigit() and int(item.itemId) >= 0):
            self.widget.itemIdSpin.setValue(int(item.itemId))
        else:
            self.widget.itemIdSpin.setValue(0)
        self.blockSignals(False)

    def siteCode(self):
        return self.widget.siteCodeCombo.currentText()

    def classCode(self):
        return self.widget.classCodeCombo.itemData(self.widget.classCodeCombo.currentIndex())

    def itemId(self):
        return str(self.widget.itemIdSpin.value())

    def setItemNavEnabled(self, enabled=True):
        self._refreshDataAction.setEnabled(enabled)
        self._firstItemAction.setEnabled(enabled)
        self._previousItemAction.setEnabled(enabled)
        self._openItemAction.setEnabled(enabled)
        self._nextItemAction.setEnabled(enabled)
        self._lastItemAction.setEnabled(enabled)

    def setItemUrl(self, url=''):
        self.widget.itemDataView.load(QUrl(url))

    def _itemChanged(self):
        self.itemChanged.emit()

    def _linkClicked(self, url):
        self.itemLinkClicked.emit(url)

    def _addMapAction(self, mapAction, text):
        action = QAction(text, self)
        action.setCheckable(True)
        action.setData(mapAction)
        action.triggered.connect(self._mapActionSelected)
        self._mapActionGroup.addAction(action)
        return action

    def _mapActionSelected(self):
        self.mapActionChanged.emit(self.sender().data())

    def _addFilterAction(self, filterAction, text):
        action = QAction(text, self)
        action.setCheckable(True)
        action.setData(filterAction)
        action.triggered.connect(self._filterActionSelected)
        self._filterActionGroup.addAction(action)
        return action

    def _filterActionSelected(self):
        self.filterActionChanged.emit(self.sender().data())

    def _addDrawingAction(self, drawingAction, text):
        action = QAction(text, self)
        action.setCheckable(True)
        action.setData(drawingAction)
        action.triggered.connect(self._drawingActionSelected)
        self._drawingActionGroup.addAction(action)
        return action

    def _drawingActionSelected(self):
        self.drawingActionChanged.emit(self.sender().data())
