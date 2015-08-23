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
    zoomSelected = pyqtSignal()
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

        self.subGroupFilterCombo.activated.connect(self._subGroupFilterSelected)
        self.subGroupFilterLineEdit = self.subGroupFilterCombo.lineEdit()
        self.subGroupFilterLineEdit.returnPressed.connect(self._subGroupFilterSelected)
        self.subGroupFilterButton.clicked.connect(self._subGroupFilterSelected)

        self.groupFilterCombo.activated.connect(self._groupFilterSelected)
        self.groupFilterLineEdit = self.groupFilterCombo.lineEdit()
        self.groupFilterLineEdit.returnPressed.connect(self._groupFilterSelected)
        self.groupFilterButton.clicked.connect(self._groupFilterSelected)

        self.buildFilterButton.clicked.connect(self.buildFilterSelected)
        self.clearFilterButton.clicked.connect(self._clearFilterClicked)
        self.loadDataButton.clicked.connect(self.loadDataSelected)
        self.showDataButton.clicked.connect(self.showDataSelected)
        self.zoomButton.clicked.connect(self.zoomSelected)

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
