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

import os

from PyQt4 import uic
from PyQt4.QtCore import Qt, pyqtSignal
from PyQt4.QtGui import QDockWidget, QMenu, QAction, QIcon, QToolButton

from ..libarkqgis.dock import ArkDockWidget

import plan_dock_base

class PlanDock(ArkDockWidget, plan_dock_base.Ui_PlanDockWidget):

    loadRawFileSelected = pyqtSignal()
    loadGeoFileSelected = pyqtSignal()
    loadContextSelected = pyqtSignal()
    loadPlanSelected = pyqtSignal()

    featureNameChanged = pyqtSignal(str)
    autoSchematicSelected = pyqtSignal(str)
    editPointsSelected = pyqtSignal()
    editLinesSelected = pyqtSignal()
    editPolygonsSelected = pyqtSignal()
    sectionChanged = pyqtSignal(object)

    clearSelected = pyqtSignal()
    mergeSelected = pyqtSignal()

    _cgColMax = 3
    _cgCol = 0
    _cgRow = 0
    _fgColMax = 3
    _fgCol = 0
    _fgRow = 0
    _sgColMax = 3
    _sgCol = 0
    _sgRow = 0

    def __init__(self, parent=None):
        super(PlanDock, self).__init__(parent)

    def initGui(self, iface, location, menuAction):
        super(PlanDock, self).initGui(iface, location, menuAction)
        self.setupUi(self)

        self.loadRawButton.clicked.connect(self.loadRawFileSelected)
        self.loadGeoButton.clicked.connect(self.loadGeoFileSelected)
        self.loadContextButton.clicked.connect(self.loadContextSelected)
        self.loadPlanButton.clicked.connect(self.loadPlanSelected)

        self.metadataWidget.initGui()

        self.featureNameEdit.textChanged.connect(self.featureNameChanged)
        self.autoSchematicTool.clicked.connect(self._autoSchematicSelected)
        self.editPointsTool.clicked.connect(self.editPointsSelected)
        self.editLinesTool.clicked.connect(self.editLinesSelected)
        self.editPolygonsTool.clicked.connect(self.editPolygonsSelected)
        self.sectionCombo.currentIndexChanged.connect(self._sectionChanged)

        self.clearButton.clicked.connect(self.clearSelected)
        self.mergeButton.clicked.connect(self.mergeSelected)

    # Metadata Tools

    def initSections(self, itemList):
        self.sectionCombo.clear()
        for section in sorted(itemList):
            if section.name:
                self.sectionCombo.addItem(section.name, section.key)
            else:
                self.sectionCombo.addItem('S' + section.key.itemId, section.key)

    def featureName(self):
        return self.featureNameEdit.text()

    def setFeatureName(self, name):
        self.featureNameEdit.setText(name)

    def sectionKey(self):
        return self.sectionCombo.itemData(self.sectionCombo.currentIndex())

    def setSection(self, itemKey):
        #TODO Doesn't work when it should...
        #idx = self.sectionCombo.findData(itemKey)
        for i in range(0, self.sectionCombo.count()):
            if self.sectionCombo.itemData(i) == itemKey:
                self.sectionCombo.setCurrentIndex(i)
                return

    # Drawing Tools

    def addDrawingTool(self, dockTab, action):
        toolButton = QToolButton(self)
        toolButton.setFixedWidth(40)
        toolButton.setDefaultAction(action)
        if dockTab == 'cxt':
            self.contextToolsLayout.addWidget(toolButton, self._cgRow, self._cgCol, Qt.AlignCenter)
            if self._cgCol == self._cgColMax:
                self._cgRow += 1
                self._cgCol = 0
            else:
                self._cgCol += 1
        elif dockTab == 'sec':
            self.sectionToolsLayout.addWidget(toolButton, self._sgRow, self._sgCol, Qt.AlignCenter)
            if self._sgCol == self._sgColMax:
                self._sgRow += 1
                self._sgCol = 0
            else:
                self._cgCol += 1
        else:
            self.featureToolsLayout.addWidget(toolButton, self._fgRow, self._fgCol, Qt.AlignCenter)
            if self._fgCol == self._fgColMax:
                self._fgRow += 1
                self._fgCol = 0
            else:
                self._fgCol += 1

    def _autoSchematicSelected(self):
        self.autoSchematicSelected.emit(self.metadataWidget.itemId())

    def _sectionChanged(self, idx):
        self.sectionChanged.emit(self.sectionCombo.itemData(idx))
