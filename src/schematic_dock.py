# -*- coding: utf-8 -*-
"""
/***************************************************************************
                                      Ark
                                 A QGIS plugin
             QGIS Plugin for ARK, the Archaeological Recording Kit
                              -------------------
        begin                : 2015-10-27
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

import os

from PyQt4 import uic
from PyQt4.QtCore import Qt, pyqtSignal
from PyQt4.QtGui import QDockWidget, QPixmap, QToolButton

from qgis.core import QgsMessageLog

from ..libarkqgis.dock import ArkDockWidget

from event_filters import ReturnPressedFilter

import schematic_dock_base

import resources_rc

class SearchStatus():

    Unknown = 0
    Found = 1
    NotFound = 2


class SchematicDock(ArkDockWidget, schematic_dock_base.Ui_SchematicDockWidget):

    findContextSelected = pyqtSignal()
    zoomContextSelected = pyqtSignal()
    editContextSelected = pyqtSignal()
    findSourceSelected = pyqtSignal()
    zoomSourceSelected = pyqtSignal()
    copySourceSelected = pyqtSignal()
    cloneSourceSelected = pyqtSignal()
    editSourceSelected = pyqtSignal()
    autoSchematicSelected = pyqtSignal(int)
    resetSelected = pyqtSignal()
    clearSelected = pyqtSignal()
    mergeSelected = pyqtSignal()

    _contextDataStatus = SearchStatus.Unknown
    _contextSchematicStatus = SearchStatus.Unknown
    _sourceDataStatus = SearchStatus.Unknown
    _sourceSchematicStatus = SearchStatus.Unknown

    _drawColMax = 3
    _drawCol = 0
    _drawRow = 0

    _tools = []

    def __init__(self, parent=None):
        super(SchematicDock, self).__init__(parent)

    def initGui(self, iface, location, menuAction):
        super(SchematicDock, self).initGui(iface, location, menuAction)
        self.setupUi(self)

        self.contextSpin.valueChanged.connect(self._contextChanged)
        self.contextSpinFilter = ReturnPressedFilter(self)
        self.contextSpin.installEventFilter(self.contextSpinFilter)
        self.contextSpinFilter.returnPressed.connect(self.findContextSelected)
        self.findContextTool.clicked.connect(self.findContextSelected)
        self.zoomContextTool.clicked.connect(self.zoomContextSelected)
        self.editContextButton.clicked.connect(self.editContextSelected)
        self.sourceContextSpin.valueChanged.connect(self._sourceContextChanged)
        self.sourceSpinFilter = ReturnPressedFilter(self)
        self.sourceContextSpin.installEventFilter(self.sourceSpinFilter)
        self.sourceSpinFilter.returnPressed.connect(self.findSourceSelected)
        self.findSourceTool.clicked.connect(self.findSourceSelected)
        self.zoomSourceTool.clicked.connect(self.zoomSourceSelected)
        self.copySourceButton.clicked.connect(self.copySourceSelected)
        self.cloneSourceButton.clicked.connect(self.cloneSourceSelected)
        self.editSourceButton.clicked.connect(self.editSourceSelected)
        self.metadataWidget.initGui()
        self.autoSchematicTool.clicked.connect(self._autoSchematicSelected)
        self.resetButton.clicked.connect(self.resetSelected)
        self.clearButton.clicked.connect(self.clearSelected)
        self.mergeButton.clicked.connect(self.mergeSelected)

    def unloadGui(self):
        self.sourceSpinFilter.returnPressed.disconnect(self.findSourceSelected)
        self.sourceContextSpin.removeEventFilter(self.sourceSpinFilter)
        del self.sourceSpinFilter
        self.sourceSpinFilter = None
        super(SchematicDock, self).unloadGui()

    # Metadata Tools

    def initSourceCodes(self, sourceCodes):
        self.metadataWidget.initSourceCodes(sourceCodes)

    def initSourceClasses(self, sourceClasses):
        self.metadataWidget.initSourceClasses(sourceClasses)

    def metadata(self):
        return self.metadataWidget.metadata()

    def setMetadata(self, md):
        self.metadataWidget.setMetadata(md)

    # Drawing Tools

    def addDrawingTool(self, classCode, action):
        toolButton = QToolButton(self)
        toolButton.setFixedWidth(40)
        toolButton.setDefaultAction(action)
        self.contextToolsLayout.addWidget(toolButton, self._drawRow, self._drawCol, Qt.AlignCenter)
        self._tools.append(toolButton)
        if self._drawCol == self._drawColMax:
            self.newDrawingToolRow()
        else:
            self._drawCol += 1

    def newDrawingToolRow(self):
        self._drawRow += 1
        self._drawCol = 0

    # Context Tools

    def context(self):
        return self.contextSpin.value()

    def setContext(self, context, foundData, foundSchematic):
        self.contextSpin.setValue(context)
        self._setContextStatus(foundData, foundSchematic)
        self.setSourceContext(0, SearchStatus.Unknown, SearchStatus.Unknown)

    def contextStatus(self):
        if self._contextDataStatus == SearchStatus.Unknown or self._contextSchematicStatus == SearchStatus.Unknown:
            return SearchStatus.Unknown
        if self._contextDataStatus == SearchStatus.Found or self._contextSchematicStatus == SearchStatus.Found:
            return SearchStatus.Found
        return SearchStatus.NotFound

    def _setContextStatus(self, foundData, foundSchematic):
        self._contextDataStatus = foundData
        self._contextSchematicStatus = foundSchematic
        self._setStatusLabel(self.contextDataStatusLabel, foundData)
        self._setStatusLabel(self.contextSchematicStatusLabel, foundSchematic)
        self.editContextButton.setEnabled(self.contextStatus() == SearchStatus.Found)
        self._enableSource(foundSchematic == SearchStatus.NotFound)
        self._enableDraw(foundSchematic == SearchStatus.NotFound)
        self._enableAuto()

    def sourceContext(self):
        return self.sourceContextSpin.value()

    def setSourceContext(self, context, foundData, foundSchematic):
        self.sourceContextSpin.setValue(context)
        self._setSourceStatus(foundData, foundSchematic)

    def sourceStatus(self):
        if self._sourceDataStatus == SearchStatus.Unknown or self._sourceSchematicStatus == SearchStatus.Unknown:
            return SearchStatus.Unknown
        if self._sourceDataStatus == SearchStatus.Found or self._sourceSchematicStatus == SearchStatus.Found:
            return SearchStatus.Found
        return SearchStatus.NotFound

    def _setSourceStatus(self, foundData, foundSchematic):
        self._sourceDataStatus = foundData
        self._sourceSchematicStatus = foundSchematic
        self._setStatusLabel(self.sourceDataStatusLabel, foundData)
        self._setStatusLabel(self.sourceSchematicStatusLabel, foundSchematic)
        self._enableClone(foundSchematic == SearchStatus.Found)
        self.editSourceButton.setEnabled(self.sourceStatus() == SearchStatus.Found)
        self._enableAuto()

    def _setStatusLabel(self, label, status):
        if status == SearchStatus.Found:
            label.setPixmap(QPixmap(':/plugins/ArkPlan/plan/statusFound.png'))
        elif status == SearchStatus.NotFound:
            label.setPixmap(QPixmap(':/plugins/ArkPlan/plan/statusNotFound.png'))
        else:
            label.setPixmap(QPixmap(':/plugins/ArkPlan/plan/statusUnknown.png'))

    def _enableSource(self, enable):
        self.sourceContextSpin.setEnabled(enable)
        self.findSourceTool.setEnabled(enable)
        self.zoomSourceTool.setEnabled(enable)
        if not enable:
            self._enableClone(enable)

    def _enableClone(self, enable):
        self.copySourceButton.setEnabled(enable)
        self.cloneSourceButton.setEnabled(enable)

    def _enableDraw(self, enable):
        self.metadataWidget.setEnabled(enable)
        for tool in self._tools:
            tool.setEnabled(enable)

    def _enableAuto(self):
        auto = (self._contextDataStatus == SearchStatus.Found and self._contextSchematicStatus == SearchStatus.NotFound) or self._sourceDataStatus == SearchStatus.Found
        if auto:
            self.metadataWidget.setEnabled(True)
        self.autoSchematicTool.setEnabled(auto)

    def _contextChanged(self):
        self._setContextStatus(SearchStatus.Unknown, SearchStatus.Unknown)
        self.setSourceContext(0, SearchStatus.Unknown, SearchStatus.Unknown)

    def _sourceContextChanged(self):
        self._setSourceStatus(SearchStatus.Unknown, SearchStatus.Unknown)

    def _autoSchematicSelected(self):
        if self._sourceDataStatus == SearchStatus.Found:
            self.metadata().validate()
            self.autoSchematicSelected.emit(self.sourceContext())
        elif self._contextDataStatus == SearchStatus.Found:
            self.metadata().validate()
            self.autoSchematicSelected.emit(self.context())
