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
from PyQt4.QtGui import QWidget, QPixmap, QToolButton

from qgis.core import QgsMessageLog

from ..libarkqgis.dock import ToolDockWidget
from ..libarkqgis.event_filters import ReturnPressedFilter

import schematic_widget_base

import resources_rc

class SearchStatus():

    Unknown = 0
    Found = 1
    NotFound = 2

class SchematicWidget(QWidget, schematic_widget_base.Ui_SchematicWidget):

    def __init__(self, parent=None):
        super(SchematicWidget, self).__init__(parent)
        self.setupUi(self)

class SchematicDock(ToolDockWidget):

    findContextSelected = pyqtSignal()
    zoomContextSelected = pyqtSignal()
    editContextSelected = pyqtSignal()
    findSourceSelected = pyqtSignal()
    zoomSourceSelected = pyqtSignal()
    copySourceSelected = pyqtSignal()
    cloneSourceSelected = pyqtSignal()
    editSourceSelected = pyqtSignal()
    autoSchematicSelected = pyqtSignal(int)
    editLinesSelected = pyqtSignal()
    editPolygonsSelected = pyqtSignal()
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
        super(SchematicDock, self).__init__(SchematicWidget(), parent)

    def initGui(self, iface, location, menuAction):
        super(SchematicDock, self).initGui(iface, location, menuAction)

        self.toolbar.addAction(iface.actionPan())
        self.toolbar.addAction(iface.actionZoomIn())
        self.toolbar.addAction(iface.actionZoomOut())
        self.toolbar.addAction(iface.actionZoomFullExtent())
        self.toolbar.addAction(iface.actionZoomLast())
        self.toolbar.addAction(iface.actionZoomNext())

        self.widget.contextSpin.valueChanged.connect(self._contextChanged)
        self._contextSpinFilter = ReturnPressedFilter(self)
        self.widget.contextSpin.installEventFilter(self._contextSpinFilter)
        self._contextSpinFilter.returnPressed.connect(self.findContextSelected)
        self.widget.findContextTool.clicked.connect(self.findContextSelected)
        self.widget.zoomContextTool.clicked.connect(self.zoomContextSelected)
        self.widget.editContextButton.clicked.connect(self.editContextSelected)
        self.widget.sourceContextSpin.valueChanged.connect(self._sourceContextChanged)
        self._sourceSpinFilter = ReturnPressedFilter(self)
        self.widget.sourceContextSpin.installEventFilter(self._sourceSpinFilter)
        self._sourceSpinFilter.returnPressed.connect(self.findSourceSelected)
        self.widget.findSourceTool.clicked.connect(self.findSourceSelected)
        self.widget.zoomSourceTool.clicked.connect(self.zoomSourceSelected)
        self.widget.copySourceButton.clicked.connect(self.copySourceSelected)
        self.widget.cloneSourceButton.clicked.connect(self.cloneSourceSelected)
        self.widget.editSourceButton.clicked.connect(self.editSourceSelected)
        self.widget.metadataWidget.initGui()
        self.widget.autoSchematicTool.clicked.connect(self._autoSchematicSelected)
        self.widget.editLinesTool.clicked.connect(self.editLinesSelected)
        self.widget.editPolygonsTool.clicked.connect(self.editPolygonsSelected)
        self.widget.resetButton.clicked.connect(self.resetSelected)
        self.widget.clearButton.clicked.connect(self.clearSelected)
        self.widget.mergeButton.clicked.connect(self.mergeSelected)

    def unloadGui(self):
        super(SchematicDock, self).unloadGui()

    # Metadata Tools

    def initSourceCodes(self, sourceCodes):
        self.widget.metadataWidget.initSourceCodes(sourceCodes)

    def initSourceClasses(self, sourceClasses):
        self.widget.metadataWidget.initSourceClasses(sourceClasses)

    def metadata(self):
        return self.widget.metadataWidget.metadata()

    def setMetadata(self, md):
        self.widget.metadataWidget.setMetadata(md)

    # Drawing Tools

    def addDrawingTool(self, classCode, action):
        toolButton = QToolButton(self)
        toolButton.setFixedWidth(40)
        toolButton.setDefaultAction(action)
        self.widget.contextToolsLayout.addWidget(toolButton, self._drawRow, self._drawCol, Qt.AlignCenter)
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
        return self.widget.contextSpin.value()

    def setContext(self, context, foundData, foundSchematic):
        self.widget.contextSpin.setValue(context)
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
        self._setStatusLabel(self.widget.contextDataStatusLabel, foundData)
        self._setStatusLabel(self.widget.contextSchematicStatusLabel, foundSchematic)
        self.widget.editContextButton.setEnabled(self.contextStatus() == SearchStatus.Found)
        self._enableSource(foundSchematic == SearchStatus.NotFound)
        self._enableDraw(foundSchematic == SearchStatus.NotFound)
        self._enableAuto()

    def sourceContext(self):
        return self.widget.sourceContextSpin.value()

    def setSourceContext(self, context, foundData, foundSchematic):
        self.widget.sourceContextSpin.setValue(context)
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
        self._setStatusLabel(self.widget.sourceDataStatusLabel, foundData)
        self._setStatusLabel(self.widget.sourceSchematicStatusLabel, foundSchematic)
        self._enableClone(foundSchematic == SearchStatus.Found)
        self.widget.editSourceButton.setEnabled(self.sourceStatus() == SearchStatus.Found)
        self._enableAuto()

    def _setStatusLabel(self, label, status):
        if status == SearchStatus.Found:
            label.setPixmap(QPixmap(':/plugins/ark/plan/statusFound.png'))
        elif status == SearchStatus.NotFound:
            label.setPixmap(QPixmap(':/plugins/ark/plan/statusNotFound.png'))
        else:
            label.setPixmap(QPixmap(':/plugins/ark/plan/statusUnknown.png'))

    def _enableSource(self, enable):
        self.widget.sourceContextSpin.setEnabled(enable)
        self.widget.findSourceTool.setEnabled(enable)
        self.widget.zoomSourceTool.setEnabled(enable)
        if not enable:
            self._enableClone(enable)

    def _enableClone(self, enable):
        self.widget.copySourceButton.setEnabled(enable)
        self.widget.cloneSourceButton.setEnabled(enable)

    def _enableDraw(self, enable):
        self.widget.metadataWidget.setEnabled(enable)
        for tool in self._tools:
            tool.setEnabled(enable)

    def _enableAuto(self):
        auto = (self._contextDataStatus == SearchStatus.Found and self._contextSchematicStatus == SearchStatus.NotFound) or self._sourceDataStatus == SearchStatus.Found
        if auto:
            self.widget.metadataWidget.setEnabled(True)
        self.widget.autoSchematicTool.setEnabled(auto)

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
