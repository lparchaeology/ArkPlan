# -*- coding: utf-8 -*-
"""
/***************************************************************************
                                      Ark
                                 A QGIS plugin
             QGIS Plugin for ARK, the Archaeological Recording Kit
                             -------------------
        begin                : 2015-09-09
        git sha              : $Format:%H$
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

import resources_rc

from PyQt4 import uic
from PyQt4.QtCore import Qt, pyqtSignal
from PyQt4.QtGui import QWidget, QMenu, QAction, QActionGroup, QIcon

import filter_widget_base

class FilterType():
    IncludeFilter = 0
    ExcludeFilter = 1
    HighlightFilter = 2

class FilterWidget(QWidget, filter_widget_base.Ui_FilterWidget):

    filterAdded = pyqtSignal()
    filterRemoved = pyqtSignal(int)
    filterChanged = pyqtSignal(int)

    _filterIndex = -1
    _filterType = FilterType.IncludeFilter

    def __init__(self, parent=None):
        super(FilterWidget, self).__init__(parent)
        self.setupUi(self)

        self._addIcon = QIcon(':/plugins/ArkPlan/mActionAdd.svg')
        self._addAction = QAction(self._addIcon, 'Add filter', self)
        self._addAction.setStatusTip('Add filter')
        self._addAction.triggered.connect(self._addFilterClicked)
        self.filterRangeCombo.lineEdit().returnPressed.connect(self._addFilterClicked)

        self._removeIcon = QIcon(':/plugins/ArkPlan/mActionRemove.svg')
        self._removeAction = QAction(self._removeIcon, 'Remove filter', self)
        self._removeAction.setStatusTip('Remove filter')
        self._removeAction.triggered.connect(self._removeFilterClicked)

        self.filterActionTool.setDefaultAction(self._addAction)

        self._includeIcon = QIcon(':/plugins/ArkPlan/list-add.png')
        self._includeAction = QAction(self._includeIcon, 'Include', self)
        self._includeAction.setStatusTip('Include items in selection')
        self._includeAction.setCheckable(True)
        self._includeAction.triggered.connect(self._includeFilterChecked)

        self._excludeIcon = QIcon(':/plugins/ArkPlan/list-remove.png')
        self._excludeAction = QAction(self._excludeIcon, 'Exclude', self)
        self._excludeAction.setStatusTip('Exclude items from selection')
        self._excludeAction.setCheckable(True)
        self._excludeAction.triggered.connect(self._excludeFilterChecked)

        self._highlightIcon = QIcon(':/plugins/ArkPlan/mIconSelected.svg')
        self._highlightAction = QAction(self._highlightIcon, 'Highlight', self)
        self._highlightAction.setStatusTip('Highlight items')
        self._highlightAction.setCheckable(True)
        self._highlightAction.triggered.connect(self._highlightFilterChecked)

        self._typeActionGroup = QActionGroup(self)
        self._typeActionGroup.addAction(self._includeAction)
        self._typeActionGroup.addAction(self._excludeAction)
        self._typeActionGroup.addAction(self._highlightAction)

        self._typeMenu = QMenu(self)
        self._typeMenu.addActions(self._typeActionGroup.actions())
        self.filterTypeTool.setMenu(self._typeMenu)

        self.filterTypeTool.setDefaultAction(self._includeAction)

    def index(self):
        return self._filterIndex

    def setIndex(self, index):
        self._filterIndex = index

    def filterType(self):
        return self._filterType

    def classCode(self):
        return self.filterClassCombo.itemData(self.filterClassCombo.currentIndex())

    def setClassCodes(self, codes):
        self.filterClassCombo.clear()
        keys = codes.keys()
        keys.sort()
        for key in keys:
            self.filterClassCombo.addItem(codes[key], key)

    def setClassCode(self, code):
        self.filterClassCombo.setCurrentItem(self.filterClassCombo.findData(code))

    def filterRange(self):
        return self._normaliseRange(self.filterRangeCombo.currentText())

    def setFilterRange(self, filterRange):
        self.filterRangeCombo.setText(filterRange)

    def clearFilterRange(self):
        self.filterRangeCombo.setText('')

    def _normaliseRange(self, text):
        return text.replace(' - ', '-').replace(',', ' ').strip()

    def _addFilterClicked(self):
        self.filterActionTool.removeAction(self._addAction)
        self.filterActionTool.setDefaultAction(self._removeAction)
        self.filterAdded.emit()
        self.filterRangeCombo.lineEdit().returnPressed.disconnect(self._addFilterClicked)
        self.filterRangeCombo.lineEdit().editingFinished.connect(self._filterRangeChanged)

    def _removeFilterClicked(self):
        self.filterRemoved.emit(self._filterIndex)

    def _includeFilterChecked(self):
        self._filterType = FilterType.IncludeFilter
        self.filterTypeTool.setDefaultAction(self._includeAction)
        self.filterChanged.emit(self._filterIndex)

    def _excludeFilterChecked(self):
        self._filterType = FilterType.ExcludeFilter
        self.filterTypeTool.setDefaultAction(self._excludeAction)
        self.filterChanged.emit(self._filterIndex)

    def _highlightFilterChecked(self):
        self._filterType = FilterType.HighlightFilter
        self.filterTypeTool.setDefaultAction(self._highlightAction)
        self.filterChanged.emit(self._filterIndex)

    def _filterRangeChanged(self):
        self.filterChanged.emit(self._filterIndex)
