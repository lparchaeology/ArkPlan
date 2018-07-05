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

from qgis.PyQt.QtCore import pyqtSignal
from qgis.PyQt.QtGui import QPixmap
from qgis.PyQt.QtWidgets import QWidget

from ArkSpatial.ark.lib import utils
from ArkSpatial.ark.lib.core import ReturnPressedFilter

from ArkSpatial.ark.core import Item, Settings
from ArkSpatial.ark.core.enum import FilterAction, SearchStatus

from .ui.schematic_widget_base import Ui_SchematicWidget


class SchematicWidget(QWidget, Ui_SchematicWidget):

    loadArkData = pyqtSignal()
    mapActionChanged = pyqtSignal(int)
    filterActionChanged = pyqtSignal(int)
    drawingActionChanged = pyqtSignal(int)
    openContextData = pyqtSignal()
    openSourceContextData = pyqtSignal()
    findContextSelected = pyqtSignal()
    firstContextSelected = pyqtSignal()
    lastContextSelected = pyqtSignal()
    nextContextSelected = pyqtSignal()
    prevContextSelected = pyqtSignal()
    nextMissingSelected = pyqtSignal()
    prevMissingSelected = pyqtSignal()
    editContextSelected = pyqtSignal()
    deleteSectionSchematicSelected = pyqtSignal()
    findSourceSelected = pyqtSignal()
    copySourceSelected = pyqtSignal()
    cloneSourceSelected = pyqtSignal()
    editSourceSelected = pyqtSignal()
    contextChanged = pyqtSignal()
    resetSelected = pyqtSignal()
    schematicReportSelected = pyqtSignal()

    def __init__(self, parent=None):
        super(SchematicWidget, self).__init__(parent)
        self.setupUi(self)

        self._contextSearchStatus = SearchStatus.Unknown
        self._contextArkDataStatus = SearchStatus.Unknown
        self._contextFeatureDataStatus = SearchStatus.Unknown
        self._contextSchematicStatus = SearchStatus.Unknown
        self._sourceDataStatus = SearchStatus.Unknown
        self._sourceSchematicStatus = SearchStatus.Unknown

    def initGui(self):
        self.loadArkTool.clicked.connect(self.loadArkData)
        self.actionSettingsTool.setFilterAction(FilterAction.HighlightFilter)
        self.actionSettingsTool.mapActionChanged.connect(self.mapActionChanged)
        self.actionSettingsTool.filterActionChanged.connect(self.filterActionChanged)
        self.actionSettingsTool.drawingActionChanged.connect(self.drawingActionChanged)
        self.openContextTool.clicked.connect(self.openContextData)
        self.openSourceContextTool.clicked.connect(self.openSourceContextData)
        self.siteCodeCombo.currentIndexChanged.connect(self._contextChanged)
        self.contextSpin.valueChanged.connect(self._contextChanged)
        self._contextSpinFilter = ReturnPressedFilter(self)
        self.contextSpin.installEventFilter(self._contextSpinFilter)
        self._contextSpinFilter.returnPressed.connect(self.findContextSelected)
        self.findContextTool.clicked.connect(self.findContextSelected)
        self.firstContextTool.clicked.connect(self.firstContextSelected)
        self.lastContextTool.clicked.connect(self.lastContextSelected)
        self.nextContextTool.clicked.connect(self.nextContextSelected)
        self.prevContextTool.clicked.connect(self.prevContextSelected)
        self.nextMissingTool.clicked.connect(self.nextMissingSelected)
        self.prevMissingTool.clicked.connect(self.prevMissingSelected)
        self.schematicReportTool.clicked.connect(self.schematicReportSelected)
        self.editContextButton.clicked.connect(self.editContextSelected)
        self.deleteSectionButton.clicked.connect(self.deleteSectionSchematicSelected)
        self.sourceContextSpin.valueChanged.connect(self._sourceContextChanged)
        self._sourceSpinFilter = ReturnPressedFilter(self)
        self.sourceContextSpin.installEventFilter(self._sourceSpinFilter)
        self._sourceSpinFilter.returnPressed.connect(self.findSourceSelected)
        self.findSourceTool.clicked.connect(self.findSourceSelected)
        self.copySourceButton.clicked.connect(self.copySourceSelected)
        self.cloneSourceButton.clicked.connect(self.cloneSourceSelected)
        self.editSourceButton.clicked.connect(self.editSourceSelected)
        self.resetButton.clicked.connect(self.resetSelected)

    def unloadGui(self):
        pass

    def loadProject(self, plugin):
        if Settings.siteServerUrl():
            self.loadArkTool.setEnabled(True)
        self._enableArkNav(False)
        self.siteCodeCombo.clear()
        for siteCode in sorted(set(Settings.siteCodes())):
            self.siteCodeCombo.addItem(siteCode, siteCode)
        idx = self.siteCodeCombo.findData(Settings.siteCode())
        if idx >= 0:
            self.siteCodeCombo.setCurrentIndex(idx)
        self.resetContext()

    def closeProject(self):
        pass

    # Context Tools

    def siteCode(self):
        return self.siteCodeCombo.itemData(self.siteCodeCombo.currentIndex())

    def contextItem(self):
        return Item(self.siteCode(), 'context', self.context())

    def context(self):
        return self.contextSpin.value()

    def resetContext(self):
        self.setContext(Item())

    def setContext(self,
                   context,
                   foundArkData=SearchStatus.Unknown,
                   contextType='',
                   contextDescription='',
                   foundFeatureData=SearchStatus.Unknown,
                   foundSchematic=SearchStatus.Unknown,
                   foundSectionSchematic=SearchStatus.Unknown):
        self.resetSourceContext()
        if context.isValid():
            self._contextSearchStatus = SearchStatus.Found
            self.blockSignals(True)
            self.contextSpin.setValue(int(context.itemId()))
            self._setContextStatus(
                foundArkData, contextType, contextDescription, foundFeatureData, foundSchematic, foundSectionSchematic)
            self.blockSignals(False)
        else:
            self._contextSearchStatus = SearchStatus.Unknown
            self.contextSpin.setValue(0)
            self._setContextStatus()
        if not self.sourceContextSpin.isEnabled():
            self.contextSpin.setFocus()
            self.contextSpin.selectAll()

    def contextStatus(self):
        if self._contextFeatureDataStatus == SearchStatus.Unknown or self._contextSchematicStatus == SearchStatus.Unknown:
            return SearchStatus.Unknown
        if self._contextFeatureDataStatus == SearchStatus.Found or self._contextSchematicStatus == SearchStatus.Found:
            return SearchStatus.Found
        return SearchStatus.NotFound

    def _setContextStatus(self,
                          foundArkData=SearchStatus.Unknown,
                          contextType='',
                          contextDescription='',
                          foundFeatureData=SearchStatus.Unknown,
                          foundSchematic=SearchStatus.Unknown,
                          foundSectionSchematic=SearchStatus.Unknown):
        self._contextArkDataStatus = foundArkData
        self._contextFeatureDataStatus = foundFeatureData
        self._contextSchematicStatus = foundSchematic
        self.openContextTool.setEnabled(self._contextArkDataStatus == SearchStatus.Found)
        self.contextTypeEdit.setText(contextType)
        self.contextDescriptionEdit.setText(contextDescription)
        self._setStatusLabel(self.featureDataStatusLabel, foundFeatureData)
        self._setStatusLabel(self.schematicStatusLabel, foundSchematic)
        self._setStatusLabel(self.sectionSchematicStatusLabel, foundSectionSchematic)
        self.editContextButton.setEnabled(self.contextStatus() == SearchStatus.Found)
        self._enableSource(foundSchematic == SearchStatus.NotFound, self.context() + 1)
        self.deleteSectionButton.setEnabled(foundSectionSchematic == SearchStatus.Found)

    def sourceItem(self):
        return Item(self.siteCode(), 'context', self.sourceContext())

    def sourceContext(self):
        return self.sourceContextSpin.value()

    def resetSourceContext(self):
        self.setSourceContext(Item())

    def setSourceContext(self,
                         context,
                         foundArk=SearchStatus.Unknown,
                         contextType='',
                         contextDescription='',
                         foundFeature=SearchStatus.Unknown,
                         foundSchematic=SearchStatus.Unknown):
        if context.isValid():
            self.sourceContextSpin.setValue(int(context.itemId()))
            self._setSourceStatus(foundArk, contextType, contextDescription, foundFeature, foundSchematic)
        else:
            self.sourceContextSpin.setValue(0)
            self._setSourceStatus()
        if self.sourceContextSpin.isEnabled():
            self.sourceContextSpin.setFocus()
            self.sourceContextSpin.selectAll()

    def sourceStatus(self):
        if self._sourceDataStatus == SearchStatus.Unknown or self._sourceSchematicStatus == SearchStatus.Unknown:
            return SearchStatus.Unknown
        if self._sourceDataStatus == SearchStatus.Found or self._sourceSchematicStatus == SearchStatus.Found:
            return SearchStatus.Found
        return SearchStatus.NotFound

    def _setSourceStatus(self,
                         foundArk=SearchStatus.Unknown,
                         contextType='',
                         contextDescription='',
                         foundFeature=SearchStatus.Unknown,
                         foundSchematic=SearchStatus.Unknown):
        self._sourceDataStatus = foundFeature
        self._sourceSchematicStatus = foundSchematic
        self.openSourceContextTool.setEnabled(self._sourceDataStatus == SearchStatus.Found)
        self.sourceContextTypeEdit.setText(contextType)
        self.sourceContextDescriptionEdit.setText(contextDescription)
        self._setStatusLabel(self.sourceFeatureDataStatusLabel, foundFeature)
        self._setStatusLabel(self.sourceSchematicStatusLabel, foundSchematic)
        self._enableClone(foundSchematic == SearchStatus.Found)
        self.editSourceButton.setEnabled(self.sourceStatus() == SearchStatus.Found)

    def _setStatusLabel(self, label, status):
        if status == SearchStatus.Found:
            label.setPixmap(QPixmap(':/plugins/ark/plan/statusFound.png'))
        elif status == SearchStatus.NotFound:
            label.setPixmap(QPixmap(':/plugins/ark/plan/statusNotFound.png'))
        else:
            label.setPixmap(QPixmap(':/plugins/ark/plan/statusUnknown.png'))

    def activateArkData(self):
        self._enableArkNav()

    def _enableArkNav(self, enabled=True):
        self.firstContextTool.setEnabled(enabled)
        self.lastContextTool.setEnabled(enabled)
        self.prevContextTool.setEnabled(enabled)
        self.nextContextTool.setEnabled(enabled)
        self.prevMissingTool.setEnabled(enabled)
        self.nextMissingTool.setEnabled(enabled)
        self.schematicReportTool.setEnabled(enabled)

    def _enableSource(self, enable, context):
        self.sourceContextSpin.setEnabled(enable)
        if enable:
            self.sourceContextSpin.setValue(context)
            self.sourceContextSpin.setFocus()
            self.sourceContextSpin.selectAll()
        self.findSourceTool.setEnabled(enable)
        if not enable:
            self._enableClone(enable)

    def _enableClone(self, enable):
        self.copySourceButton.setEnabled(enable)
        self.cloneSourceButton.setEnabled(enable)

    def _contextChanged(self):
        if self._contextSearchStatus != SearchStatus.Unknown:
            self._contextSearchStatus = SearchStatus.Unknown
            self._setContextStatus()
            self.resetSourceContext()
            self.contextChanged.emit()

    def _sourceContextChanged(self):
        self._setSourceStatus()
