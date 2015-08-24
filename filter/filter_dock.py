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

from PyQt4 import uic
from PyQt4.QtCore import Qt, pyqtSignal

from ..arklib.dock import ArkDockWidget

import filter_dock_base

class FilterDock(ArkDockWidget, filter_dock_base.Ui_FilterDock):

    contextFilterChanged = pyqtSignal(str)
    subGroupFilterChanged = pyqtSignal(str)
    groupFilterChanged = pyqtSignal(str)

    buildFilterSelected = pyqtSignal()
    clearFilterSelected = pyqtSignal()
    zoomFilterSelected = pyqtSignal()
    loadDataSelected = pyqtSignal()
    showDataSelected = pyqtSignal()

    showPointsChanged = pyqtSignal(int)
    showLinesChanged = pyqtSignal(int)
    showPolygonsChanged = pyqtSignal(int)

    def __init__(self, parent=None):
        super(FilterDock, self).__init__(parent)
        self.setupUi(self)

        self.contextFilterCombo.activated.connect(self._contextFilterSelected)
        self.contextFilterLineEdit = self.contextFilterCombo.lineEdit()
        self.contextFilterLineEdit.returnPressed.connect(self._contextFilterSelected)
        self.contextFilterButton.clicked.connect(self._contextFilterSelected)

        self.subGroupFilterLabel.setHidden(True)
        self.subGroupFilterCombo.activated.connect(self._subGroupFilterSelected)
        self.subGroupFilterCombo.setHidden(True)
        self.subGroupFilterLineEdit = self.subGroupFilterCombo.lineEdit()
        self.subGroupFilterLineEdit.returnPressed.connect(self._subGroupFilterSelected)
        self.subGroupFilterLineEdit.setHidden(True)
        self.subGroupFilterButton.clicked.connect(self._subGroupFilterSelected)
        self.subGroupFilterButton.setHidden(True)

        self.groupFilterLabel.setHidden(True)
        self.groupFilterCombo.activated.connect(self._groupFilterSelected)
        self.groupFilterCombo.setHidden(True)
        self.groupFilterLineEdit = self.groupFilterCombo.lineEdit()
        self.groupFilterLineEdit.returnPressed.connect(self._groupFilterSelected)
        self.groupFilterLineEdit.setHidden(True)
        self.groupFilterButton.clicked.connect(self._groupFilterSelected)
        self.groupFilterButton.setHidden(True)

        self.zoomFilterAction.triggered.connect(self.zoomFilterSelected)
        self.zoomFilterTool.setDefaultAction(self.zoomFilterAction)

        self.buildFilterAction.triggered.connect(self.buildFilterSelected)
        self.buildFilterTool.setDefaultAction(self.buildFilterAction)

        self.clearFilterAction.triggered.connect(self._clearFilterClicked)
        self.clearFilterTool.setDefaultAction(self.clearFilterAction)

        self.loadDataAction.triggered.connect(self.loadDataSelected)
        self.loadDataTool.setDefaultAction(self.loadDataAction)
        self.loadDataTool.setHidden(True)

        self.showDataAction.triggered.connect(self.showDataSelected)
        self.showDataTool.setDefaultAction(self.showDataAction)
        self.showDataTool.setHidden(True)

        self.showPointsCheck.stateChanged.connect(self.showPointsChanged)
        self.showLinesCheck.stateChanged.connect(self.showLinesChanged)
        self.showPolygonsCheck.stateChanged.connect(self.showPolygonsChanged)

        self.enableGroupFilters(False)

    def _contextFilterSelected(self):
        self.subGroupFilterLineEdit.clear()
        self.groupFilterLineEdit.clear()
        contextRange = self._normaliseRange(self.contextFilterCombo.currentText())
        self.contextFilterChanged.emit(contextRange)

    def _subGroupFilterSelected(self):
        self.contextFilterLineEdit.clear()
        self.groupFilterLineEdit.clear()
        subRange = self._normaliseRange(self.subGroupFilterCombo.currentText())
        self.subGroupFilterChanged.emit(subRange)

    def _groupFilterSelected(self):
        self.contextFilterLineEdit.clear()
        self.subGroupFilterLineEdit.clear()
        groupRange = self._normaliseRange(self.groupFilterCombo.currentText())
        self.groupFilterChanged.emit(groupRange)

    def _clearFilterClicked(self):
        self.contextFilterLineEdit.clear()
        self.subGroupFilterLineEdit.clear()
        self.groupFilterLineEdit.clear()
        self.clearFilterSelected.emit()

    def enableGroupFilters(self, status):
        self.subGroupFilterCombo.setEnabled(status)
        self.subGroupFilterButton.setEnabled(status)
        self.groupFilterCombo.setEnabled(status)
        self.groupFilterButton.setEnabled(status)

    def displayFilter(self, filter):
        self.filterEdit.setText(filter)

    def _normaliseRange(self, text):
        filter = text.replace(' - ', '-')
        filter = filter.replace(',', ' ')
        return filter
