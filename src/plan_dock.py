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

    contextNumberChanged = pyqtSignal(int)
    featureIdChanged = pyqtSignal(int)
    featureNameChanged = pyqtSignal(str)
    autoSchematicSelected = pyqtSignal(int)
    editPointsSelected = pyqtSignal()
    editLinesSelected = pyqtSignal()
    editPolygonsSelected = pyqtSignal()

    clearSelected = pyqtSignal()
    mergeSelected = pyqtSignal()

    _cgColMax = 3
    _cgCol = 0
    _cgRow = 0
    _fgColMax = 3
    _fgCol = 0
    _fgRow = 0

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

        self.contextNumberSpin.valueChanged.connect(self.contextNumberChanged)
        self.featureIdSpin.valueChanged.connect(self.featureIdChanged)
        self.featureNameEdit.textChanged.connect(self.featureNameChanged)
        self.autoSchematicTool.clicked.connect(self._autoSchematicSelected)
        self.editPointsTool.clicked.connect(self.editPointsSelected)
        self.editLinesTool.clicked.connect(self.editLinesSelected)
        self.editPolygonsTool.clicked.connect(self.editPolygonsSelected)

        self.clearButton.clicked.connect(self.clearSelected)
        self.mergeButton.clicked.connect(self.mergeSelected)

    # Metadata Tools

    def initSourceCodes(self, sourceCodes):
        self.metadataWidget.initSourceCodes(sourceCodes)

    def initSourceClasses(self, sourceClasses):
        self.metadataWidget.initSourceClasses(sourceClasses)

    def metadata(self):
        return self.metadataWidget.metadata()

    def setMetadata(self, md):
        self.metadataWidget.setMetadata(md)

    def contextNumber(self):
        return self.contextNumberSpin.value()

    def setContextNumber(self, context):
        if context is None:
            self.contextNumberSpin.setValue(0)
        else:
            self.contextNumberSpin.setValue(context)

    def featureId(self):
        return self.featureIdSpin.value()

    def setFeatureId(self, featureId):
        if featureId is None:
            self.featureIdSpin.setValue(0)
        else:
            self.featureIdSpin.setValue(featureId)

    def featureName(self):
        return self.featureNameEdit.text()

    def setFeatureName(self, name):
        self.featureNameEdit.setText(name)

    # Drawing Tools

    def addDrawingTool(self, classCode, action):
        toolButton = QToolButton(self)
        toolButton.setFixedWidth(40)
        toolButton.setDefaultAction(action)
        if classCode == 'cxt':
            self.contextToolsLayout.addWidget(toolButton, self._cgRow, self._cgCol, Qt.AlignCenter)
            if self._cgCol == self._cgColMax:
                self.newDrawingToolRow(classCode)
            else:
                self._cgCol += 1
        else:
            self.featureToolsLayout.addWidget(toolButton, self._fgRow, self._fgCol, Qt.AlignCenter)
            if self._fgCol == self._fgColMax:
                self.newDrawingToolRow(classCode)
            else:
                self._fgCol += 1

    def newDrawingToolRow(self, classCode):
        if classCode == 'cxt':
            self._cgRow += 1
            self._cgCol = 0
        else:
            self._fgRow += 1
            self._fgCol = 0

    def _autoSchematicSelected(self):
        self.autoSchematicSelected.emit(self.contextNumber())
