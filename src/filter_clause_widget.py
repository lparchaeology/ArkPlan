# -*- coding: utf-8 -*-
"""
/***************************************************************************
                                ARK Spatial
                    A QGIS plugin for Archaeological Recording.
        Part of the Archaeological Recording Kit by L-P : Archaeology
                        http://ark.lparchaeology.com
                              -------------------
        begin                : 2014-12-07
        git sha              : $Format:%H$
        copyright            : 2014, 2015 by L-P : Heritage LLP
        email                : ark@lparchaeology.com
        copyright            : 2014, 2015 by John Layt
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

import resources

from PyQt4 import uic
from PyQt4.QtCore import Qt, pyqtSignal
from PyQt4.QtGui import QWidget, QMenu, QAction, QActionGroup, QIcon, QWidgetAction, QPixmap, QColor

from qgis.gui import QgsColorButtonV2

from ..libarkqgis.project import Project
from ..libarkqgis.utils import *

from enum import FilterType, FilterAction
from plan_item import ItemKey

import filter_clause_widget_base


class FilterClauseWidget(QWidget, filter_clause_widget_base.Ui_FilterClauseWidget):

    filterAdded = pyqtSignal()
    filterRemoved = pyqtSignal(int)
    filterChanged = pyqtSignal(int)

    _filterIndex = -1
    _filterType = FilterType.IncludeFilter
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

        self.setFilterAction(FilterAction.AddFilter)

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

        self._highlightColorTool = QgsColorButtonV2(self)
        self._highlightColorTool.setAllowAlpha(True)
        self._highlightColorTool.setColorDialogTitle('Choose Highlight Color')
        self._highlightColorTool.setContext('Choose Highlight Color')
        self._highlightColorTool.setDefaultColor(Project.highlightFillColor())
        self._highlightColorTool.setToDefaultColor()
        self._highlightColorTool.colorChanged.connect(self._colorChanged)
        self._highlightColorAction = QWidgetAction(self)
        self._highlightColorAction.setDefaultWidget(self._highlightColorTool)

        self._typeMenu = QMenu(self)
        self._typeMenu.addActions(self._typeActionGroup.actions())
        self._typeMenu.addSeparator()
        self._typeMenu.addAction(self._highlightColorAction)
        self.filterTypeTool.setMenu(self._typeMenu)

        self.setFilterType(FilterType.IncludeFilter)

    def toSettings(self, settings):
        settings.setValue('filterType', self.filterType())
        settings.setValue('siteCode', self.siteCode())
        settings.setValue('classCode', self.classCode())
        settings.setValue('filterRange', self.filterRange())
        if self.filterType() == FilterType.HighlightFilter:
            settings.setValue('highlightColor', self.highlightColor())

    def fromSettings(self, settings):
        self.setFilterType(int(settings.value('filterType')))
        self.setSiteCode(settings.value('siteCode'))
        self.setClassCode(settings.value('classCode'))
        self.setFilterRange(settings.value('filterRange'))
        self.setFilterAction(FilterAction.RemoveFilter)
        if self.filterType() == FilterType.HighlightFilter:
            self.setHighlightColor(settings.value('highlightColor', QColor))

    def index(self):
        return self._filterIndex

    def setIndex(self, index):
        self._filterIndex = index

    def setFilterType(self, filterType):
        self._filterType = filterType
        if filterType == FilterType.ExcludeFilter:
            self._excludeAction.setChecked(True)
            self.filterTypeTool.setDefaultAction(self._excludeAction)
        elif filterType == FilterType.SelectFilter:
            self._selectAction.setChecked(True)
            self.filterTypeTool.setDefaultAction(self._selectAction)
        elif filterType == FilterType.HighlightFilter:
            self._highlightAction.setChecked(True)
            self.filterTypeTool.setDefaultAction(self._highlightAction)
        else:
            self._includeAction.setChecked(True)
            self.filterTypeTool.setDefaultAction(self._includeAction)

    def filterType(self):
        return self._filterType

    def setItemKey(self, itemKey):
        self.setSiteCode(itemKey.siteCode)
        self.setClassCode(itemKey.classCode)
        self.filterRange(itemKey.itemId)

    def itemKey(self):
        return ItemKey(self.siteCode(), self.classCode(), self.filterRange())

    def setSiteCode(self, siteCode):
        self._siteCode = siteCode

    def siteCode(self):
        return self._siteCode

    def classCode(self):
        return self.filterClassCombo.itemData(self.filterClassCombo.currentIndex())

    def setClassCodes(self, codes):
        self.filterClassCombo.clear()
        keys = codes.keys()
        keys.sort()
        for key in keys:
            self.filterClassCombo.addItem(codes[key], key)

    def setClassCode(self, code):
        self.filterClassCombo.setCurrentIndex(self.filterClassCombo.findData(code))

    def filterRange(self):
        return self._normaliseRange(self.filterRangeCombo.currentText())

    def setFilterRange(self, filterRange):
        self.filterRangeCombo.setEditText(filterRange)

    def clearFilterRange(self):
        self.filterRangeCombo.clearEditText()

    def setFilterAction(self, action):
        if self._filterActionStatus == FilterAction.AddFilter:
            self.filterRangeCombo.lineEdit().returnPressed.disconnect(self._addFilterClicked)
        elif self._filterActionStatus == FilterAction.RemoveFilter:
            self.filterRangeCombo.lineEdit().editingFinished.disconnect(self._filterRangeChanged)
        self._filterActionStatus = action
        if action == FilterAction.LockFilter:
            self.filterActionTool.removeAction(self._addAction)
            self.filterActionTool.setDefaultAction(self._removeAction)
            self.setEnabled(False)
        elif action == FilterAction.RemoveFilter:
            self.filterActionTool.removeAction(self._addAction)
            self.filterActionTool.setDefaultAction(self._removeAction)
            self.filterRangeCombo.lineEdit().editingFinished.connect(self._filterRangeChanged)
            self.setEnabled(True)
        else:
            self.filterActionTool.removeAction(self._removeAction)
            self.filterActionTool.setDefaultAction(self._addAction)
            self.filterRangeCombo.lineEdit().returnPressed.connect(self._addFilterClicked)
            self.setEnabled(True)

    def setHighlightColor(self, color):
        return self._highlightColorTool.setColor(color)

    def highlightColor(self):
        return self._highlightColorTool.color()

    def _normaliseRange(self, text):
        return text.replace(' - ', '-').replace(',', ' ').strip()

    def _addFilterClicked(self):
        self.setFilterAction(FilterAction.RemoveFilter)
        self.filterAdded.emit()

    def _removeFilterClicked(self):
        self.filterRemoved.emit(self._filterIndex)

    def _includeFilterChecked(self):
        self.setFilterType(FilterType.IncludeFilter)
        self.filterChanged.emit(self._filterIndex)

    def _excludeFilterChecked(self):
        self.setFilterType(FilterType.ExcludeFilter)
        self.filterChanged.emit(self._filterIndex)

    def _highlightFilterChecked(self):
        self.setFilterType(FilterType.HighlightFilter)
        self.filterChanged.emit(self._filterIndex)

    def _selectFilterChecked(self):
        self.setFilterType(FilterType.SelectFilter)
        self.filterChanged.emit(self._filterIndex)

    def _filterRangeChanged(self):
        self.filterChanged.emit(self._filterIndex)

    def _colorChanged(self, color):
        pix = QPixmap(22, 22)
        pix.fill(color)
        self._highlightIcon = QIcon(pix)
        self._highlightAction.setIcon(self._highlightIcon)
        self.setFilterType(FilterType.HighlightFilter)
        self.filterChanged.emit(self._filterIndex)
