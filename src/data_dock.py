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
from PyQt4.QtCore import Qt, pyqtSignal
from PyQt4.QtGui import QWidget, QPixmap, QToolButton, QAction, QIcon

from ..libarkqgis.dock import ToolDockWidget
from ..libarkqgis import utils

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
    firstItemSelected = pyqtSignal()
    prevItemSelected = pyqtSignal()
    openItemData = pyqtSignal()
    nextItemSelected = pyqtSignal()
    lastItemSelected = pyqtSignal()
    zoomItemSelected = pyqtSignal()
    filterItemSelected = pyqtSignal()
    loadDrawingsSelected = pyqtSignal()

    def __init__(self, parent=None):
        super(DataDock, self).__init__(DataWidget(), parent)

        self.setWindowTitle(u'ARK Data')
        self.setObjectName(u'DataDock')

    def initGui(self, iface, location, menuAction):
        super(DataDock, self).initGui(iface, location, menuAction)

        for key in sorted(Config.classCodes.keys()):
            classCode = Config.classCodes[key]
            if classCode['plan']:
                self.widget.classCodeCombo.addItem(classCode['label'], classCode['code'])

        self._loadDataAction = QAction(QIcon(':/plugins/ark/data/loadData.svg'), "Load Data", self)
        self._loadDataAction.triggered.connect(self.loadDataSelected)
        self.toolbar.addAction(self._loadDataAction)

        self._firstItemAction = QAction(QIcon(':/plugins/ark/data/goFirstItem.svg'), "Go to first item", self)
        self._firstItemAction.triggered.connect(self.firstItemSelected)
        self.toolbar.addAction(self._firstItemAction)

        self._previousItemAction = QAction(QIcon(':/plugins/ark/data/goPrevItem.svg'), "Go to previous item", self)
        self._previousItemAction.triggered.connect(self.prevItemSelected)
        self.toolbar.addAction(self._previousItemAction)

        self._openItemAction = QAction(QIcon(':/plugins/ark/data/openData.svg'), "Open item in ARK", self)
        self._openItemAction.triggered.connect(self.nextItemSelected)
        self.toolbar.addAction(self._openItemAction)

        self._nextItemAction = QAction(QIcon(':/plugins/ark/data/goNextItem.svg'), "Go to next item", self)
        self._nextItemAction.triggered.connect(self.nextItemSelected)
        self.toolbar.addAction(self._nextItemAction)

        self._lastItemAction = QAction(QIcon(':/plugins/ark/data/goLastItem.svg'), "Go to last item", self)
        self._lastItemAction.triggered.connect(self.lastItemSelected)
        self.toolbar.addAction(self._lastItemAction)

        self._zoomItemAction = QAction(QIcon(':/plugins/ark/plan/zoomToItem.svg'), "Zoom to item", self)
        self._zoomItemAction.triggered.connect(self.zoomItemSelected)
        self.toolbar.addAction(self._zoomItemAction)

        self._filterItemAction = QAction(QIcon(':/plugins/ark/filter/filter.png'), "Filter item", self)
        self._filterItemAction.triggered.connect(self.filterItemSelected)
        self.toolbar.addAction(self._filterItemAction)

        self._loadDrawingsAction = QAction(QIcon(':/plugins/ark/plan/loadDrawings.svg'), "Load Drawings", self)
        self._loadDrawingsAction.triggered.connect(self.loadDrawingsSelected)
        self.toolbar.addAction(self._loadDrawingsAction)

        self.widget.siteCodeCombo.currentIndexChanged.connect(self._itemChanged)
        self.widget.classCodeCombo.currentIndexChanged.connect(self._itemChanged)
        self.widget.itemIdSpin.valueChanged.connect(self._itemChanged)

    def initSiteCodes(self, siteCodes):
        self.widget.siteCodeCombo.clear()
        for site in siteCodes:
            self.widget.siteCodeCombo.addItem(site)

    def item(self):
        return ItemKey(self.siteCode(), self.classCode(), self.itemId())

    def siteCode(self):
        return self.widget.siteCodeCombo.currentText()

    def classCode(self):
        return self.widget.classCodeCombo.itemData(self.widget.classCodeCombo.currentIndex())

    def itemId(self):
        return str(self.widget.itemIdSpin.value())

    def subgroup(self):
        return ItemKey(self.siteCode(), 'sgr', self.itemId())

    def subgroupId(self):
        return str(self.widget.idSpin.value())

    def _itemChanged(self):
        self.itemChanged.emit()
