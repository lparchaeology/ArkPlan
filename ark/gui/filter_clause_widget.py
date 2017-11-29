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

from PyQt4.QtCore import pyqtSignal
from PyQt4.QtGui import QAction, QActionGroup, QIcon, QMenu, QPixmap, QWidget, QWidgetAction

from qgis.gui import QgsColorButtonV2

from ArkSpatial.ark.lib import Application

from ArkSpatial.ark.core import FilterClause, FilterType, Item
from ArkSpatial.ark.core.enum import FilterWidgetAction

from .ui.filter_clause_widget_base import Ui_FilterClauseWidget


class FilterClauseWidget(QWidget, Ui_FilterClauseWidget):

    clauseAdded = pyqtSignal()
    clauseRemoved = pyqtSignal(int)
    clauseChanged = pyqtSignal(int)

    _filterIndex = -1
    _filterType = FilterType.Include
    _filterActionStatus = -1
    _siteCode = ''

    def __init__(self, parent=None):
        super(FilterClauseWidget, self).__init__(parent)
        self.setupUi(self)

        self._addIcon = QIcon(':/plugins/ark/filter/addFilter.svg')
        self._addAction = QAction(self._addIcon, 'Add filter', self)
        self._addAction.setStatusTip('Add filter')
        self._addAction.triggered.connect(self._addFilterClicked)

        self._removeIcon = QIcon(':/plugins/ark/filter/removeFilter.svg')
        self._removeAction = QAction(self._removeIcon, 'Remove filter', self)
        self._removeAction.setStatusTip('Remove filter')
        self._removeAction.triggered.connect(self._removeFilterClicked)

        self.setFilterAction(FilterWidgetAction.AddFilter)

        self._includeIcon = QIcon(':/plugins/ark/filter/includeFilter.png')
        self._includeAction = QAction(self._includeIcon, 'Include', self)
        self._includeAction.setStatusTip('Include items in selection')
        self._includeAction.setCheckable(True)
        self._includeAction.triggered.connect(self._includeFilterChecked)

        self._excludeIcon = QIcon(':/plugins/ark/filter/excludeFilter.png')
        self._excludeAction = QAction(self._excludeIcon, 'Exclude', self)
        self._excludeAction.setStatusTip('Exclude items from selection')
        self._excludeAction.setCheckable(True)
        self._excludeAction.triggered.connect(self._excludeFilterChecked)

        self._selectIcon = QIcon(':/plugins/ark/filter/selectFilter.svg')
        self._selectAction = QAction(self._selectIcon, 'Select', self)
        self._selectAction.setStatusTip('Select items')
        self._selectAction.setCheckable(True)
        self._selectAction.triggered.connect(self._selectFilterChecked)

        self._highlightIcon = QIcon(':/plugins/ark/filter/highlightFilter.svg')
        self._highlightAction = QAction(self._highlightIcon, 'Highlight', self)
        self._highlightAction.setStatusTip('Highlight items')
        self._highlightAction.setCheckable(True)
        self._highlightAction.triggered.connect(self._highlightFilterChecked)

        self._typeActionGroup = QActionGroup(self)
        self._typeActionGroup.addAction(self._includeAction)
        self._typeActionGroup.addAction(self._excludeAction)
        self._typeActionGroup.addAction(self._selectAction)
        self._typeActionGroup.addAction(self._highlightAction)

        self._colorTool = QgsColorButtonV2(self)
        self._colorTool.setAllowAlpha(True)
        self._colorTool.setColorDialogTitle('Choose Highlight Color')
        self._colorTool.setContext('Choose Highlight Color')
        self._colorTool.setDefaultColor(Application.highlightFillColor())
        self._colorTool.setToDefaultColor()
        self._colorTool.colorChanged.connect(self._colorChanged)
        self._colorAction = QWidgetAction(self)
        self._colorAction.setDefaultWidget(self._colorTool)

        self._typeMenu = QMenu(self)
        self._typeMenu.addActions(self._typeActionGroup.actions())
        self._typeMenu.addSeparator()
        self._typeMenu.addAction(self._colorAction)
        self.filterTypeTool.setMenu(self._typeMenu)

        self._setFilterType(FilterType.Include)

    def index(self):
        return self._filterIndex

    def setIndex(self, index):
        self._filterIndex = index

    def clause(self):
        cl = FilterClause()
        cl.item = Item(self.siteCode(), self.classCode(), self.filterRange())
        cl.action = self.filterType()
        cl.color = self.color()
        return cl

    def setClause(self, clause):
        self.blockSignals(True)
        self._colorTool.blockSignals(True)
        self._siteCode = clause.item.siteCode()
        self.filterClassCombo.setCurrentIndex(self.filterClassCombo.findData(clause.item.classCode()))
        self.filterRangeCombo.setEditText(clause.item.itemId())
        self._setFilterType(clause.action)
        # self._colorTool.setColor(clause.color)
        self._colorTool.blockSignals(False)
        self.blockSignals(False)

    def _setFilterType(self, filterType):
        self._filterType = filterType
        if filterType == FilterType.Exclude:
            self._excludeAction.setChecked(True)
            self.filterTypeTool.setDefaultAction(self._excludeAction)
        elif filterType == FilterType.Select:
            self._selectAction.setChecked(True)
            self.filterTypeTool.setDefaultAction(self._selectAction)
        elif filterType == FilterType.Highlight:
            self._highlightAction.setChecked(True)
            self.filterTypeTool.setDefaultAction(self._highlightAction)
        else:
            self._includeAction.setChecked(True)
            self.filterTypeTool.setDefaultAction(self._includeAction)

    def filterType(self):
        return self._filterType

    def siteCode(self):
        return self._siteCode

    def setSiteCode(self, siteCode):
        self._siteCode = siteCode

    def classCode(self):
        return self.filterClassCombo.itemData(self.filterClassCombo.currentIndex())

    def filterRange(self):
        return self._normaliseRange(self.filterRangeCombo.currentText())

    def color(self):
        return self._colorTool.color()

    def setClassCodes(self, codes):
        self.filterClassCombo.clear()
        keys = codes.keys()
        keys.sort()
        for key in keys:
            self.filterClassCombo.addItem(codes[key], key)

    def setHistory(self, history):
        self.filterRangeCombo.addItems(history)
        self.filterRangeCombo.clearEditText()

    def history(self):
        history = []
        for idx in range(0, self.filterRangeCombo.count()):
            history.append(self.filterRangeCombo.itemText(idx))
        return history

    def clearFilterRange(self):
        self.filterRangeCombo.clearEditText()

    def setFilterAction(self, action):
        if self._filterActionStatus == FilterWidgetAction.AddFilter:
            self.filterRangeCombo.lineEdit().returnPressed.disconnect(self._addFilterClicked)
        elif self._filterActionStatus == FilterWidgetAction.RemoveFilter:
            self.filterRangeCombo.lineEdit().editingFinished.disconnect(self._filterRangeChanged)
        self._filterActionStatus = action
        if action == FilterWidgetAction.LockFilter:
            self.filterActionTool.removeAction(self._addAction)
            self.filterActionTool.setDefaultAction(self._removeAction)
            self.setEnabled(False)
        elif action == FilterWidgetAction.RemoveFilter:
            self.filterActionTool.removeAction(self._addAction)
            self.filterActionTool.setDefaultAction(self._removeAction)
            self.filterRangeCombo.lineEdit().editingFinished.connect(self._filterRangeChanged)
            self.setEnabled(True)
        else:
            self.filterActionTool.removeAction(self._removeAction)
            self.filterActionTool.setDefaultAction(self._addAction)
            self.filterRangeCombo.lineEdit().returnPressed.connect(self._addFilterClicked)
            self.setEnabled(True)

    def _normaliseRange(self, text):
        return text.replace(' - ', '-').replace(',', ' ').strip()

    def _addFilterClicked(self):
        self.setFilterAction(FilterWidgetAction.RemoveFilter)
        self.clauseAdded.emit()

    def _removeFilterClicked(self):
        self.clauseRemoved.emit(self._filterIndex)

    def _includeFilterChecked(self):
        self._setFilterType(FilterType.Include)
        self.clauseChanged.emit(self._filterIndex)

    def _excludeFilterChecked(self):
        self._setFilterType(FilterType.Exclude)
        self.clauseChanged.emit(self._filterIndex)

    def _highlightFilterChecked(self):
        self._setFilterType(FilterType.Highlight)
        self.clauseChanged.emit(self._filterIndex)

    def _selectFilterChecked(self):
        self._setFilterType(FilterType.Select)
        self.clauseChanged.emit(self._filterIndex)

    def _filterRangeChanged(self):
        self.clauseChanged.emit(self._filterIndex)

    def _colorChanged(self, color):
        pix = QPixmap(22, 22)
        pix.fill(color)
        self._highlightIcon = QIcon(pix)
        self._highlightAction.setIcon(self._highlightIcon)
        self._setFilterType(FilterType.Highlight)
        self.clauseChanged.emit(self._filterIndex)
