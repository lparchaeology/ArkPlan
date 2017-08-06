# -*- coding: utf-8 -*-
"""
/***************************************************************************
                                ARK Spatial
                    A QGIS plugin for Archaeological Recording.
        Part of the Archaeological Recording Kit by L-P : Archaeology
                        http://ark.lparchaeology.com
                              -------------------
        copyright            : 2017 by L-P : Heritage LLP
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

from PyQt4.QtCore import QUrl, pyqtSignal
from PyQt4.QtGui import QAction, QIcon
from PyQt4.QtWebKit import QWebPage

from ark.lib import Project
from ark.lib.gui import ToolDockWidget

from ark.core import Config, Item
from ark.gui import ActionSettingsTool

import .DataWidget

import resources


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

        self.toolbar.addSeparator()
        self._settingsTool = ActionSettingsTool(self)
        self._settingsTool.mapActionChanged.connect(self.mapActionChanged)
        self._settingsTool.filterActionChanged.connect(self.filterActionChanged)
        self._settingsTool.drawingActionChanged.connect(self.drawingActionChanged)
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
        return Item(self.siteCode(), self.classCode(), self.itemId())

    def setItem(self, item):
        if item.isInvalid():
            return
        self.blockSignals(True)
        idx = self.widget.siteCodeCombo.findData(item.siteCode())
        if idx >= 0:
            self.widget.siteCodeCombo.setCurrentIndex(idx)

        idx = self.widget.classCodeCombo.findData(item.classCode())
        if idx >= 0:
            self.widget.classCodeCombo.setCurrentIndex(idx)

        if (item.itemId().isdigit() and int(item.itemId()) >= 0):
            self.widget.itemIdSpin.setValue(int(item.itemId()))
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
