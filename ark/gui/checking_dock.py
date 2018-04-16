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
from PyQt4.QtGui import QIcon

from ArkSpatial.ark.lib import utils
from ArkSpatial.ark.lib.gui import ToolDockWidget

from .schematic_widget import SchematicWidget


class CheckingDock(ToolDockWidget):

    # Schematic Signals
    loadArkData = pyqtSignal()
    mapActionChanged = pyqtSignal(int)
    filterActionChanged = pyqtSignal(int)
    drawingActionChanged = pyqtSignal(int)
    openContextData = pyqtSignal()
    openSourceContextData = pyqtSignal()
    findContextSelected = pyqtSignal()
    firstContextSelected = pyqtSignal()
    lastContextSelected = pyqtSignal()
    prevContextSelected = pyqtSignal()
    nextContextSelected = pyqtSignal()
    editContextSelected = pyqtSignal()
    deleteSectionSchematicSelected = pyqtSignal()
    nextMissingSelected = pyqtSignal()
    prevMissingSelected = pyqtSignal()
    findSourceSelected = pyqtSignal()
    zoomSourceSelected = pyqtSignal()
    copySourceSelected = pyqtSignal()
    cloneSourceSelected = pyqtSignal()
    editSourceSelected = pyqtSignal()
    contextChanged = pyqtSignal()
    resetSchematicSelected = pyqtSignal()
    schematicReportSelected = pyqtSignal()

    def __init__(self, parent=None):
        super(CheckingDock, self).__init__(SchematicWidget(), parent)

        self.setWindowTitle(u'ARK Checking')
        self.setObjectName(u'CheckingDock')

    def initGui(self, iface, location, menuAction):
        super(CheckingDock, self).initGui(iface, location, menuAction)

        # Init the main widget
        self.widget.initGui()

        # Cascade the child widget signals
        self.widget.loadArkData.connect(self.loadArkData)
        self.widget.mapActionChanged.connect(self.mapActionChanged)
        self.widget.filterActionChanged.connect(self.filterActionChanged)
        self.widget.drawingActionChanged.connect(self.drawingActionChanged)
        self.widget.openContextData.connect(self.openContextData)
        self.widget.openSourceContextData.connect(self.openSourceContextData)
        self.widget.findContextSelected.connect(self.findContextSelected)
        self.widget.firstContextSelected.connect(self.firstContextSelected)
        self.widget.lastContextSelected.connect(self.lastContextSelected)
        self.widget.prevContextSelected.connect(self.prevContextSelected)
        self.widget.nextContextSelected.connect(self.nextContextSelected)
        self.widget.prevMissingSelected.connect(self.prevMissingSelected)
        self.widget.nextMissingSelected.connect(self.nextMissingSelected)
        self.widget.schematicReportSelected.connect(self.schematicReportSelected)
        self.widget.editContextSelected.connect(self.editContextSelected)
        self.widget.deleteSectionSchematicSelected.connect(self.deleteSectionSchematicSelected)
        self.widget.findSourceSelected.connect(self.findSourceSelected)
        self.widget.copySourceSelected.connect(self.copySourceSelected)
        self.widget.cloneSourceSelected.connect(self.cloneSourceSelected)
        self.widget.editSourceSelected.connect(self.editSourceSelected)
        self.widget.contextChanged.connect(self.contextChanged)
        self.widget.resetSelected.connect(self.resetSchematicSelected)

    def unloadGui(self):
        self.widget.unloadGui()
        super(CheckingDock, self).unloadGui()

    # Load the project settings when project is loaded
    def loadProject(self, plugin):
        self.widget.loadProject(plugin)

    # Close the project
    def closeProject(self):
        self.widget.closeProject()

    def activateArkData(self):
        self.widget.activateArkData()

    def activateSchematicCheck(self):
        self.widget.contextSpin.setFocus()

    def contextItem(self):
        return self.widget.contextItem()

    def context(self):
        return self.widget.context()

    def resetContext(self):
        self.widget.resetContext()

    def setContext(self,
                   context,
                   foundArkData,
                   contextType,
                   contextDescription,
                   foundFeatureData,
                   foundSchematic,
                   foundSectionSchematic):
        self.widget.setContext(context,
                               foundArkData,
                               contextType,
                               contextDescription,
                               foundFeatureData,
                               foundSchematic,
                               foundSectionSchematic)

    def contextStatus(self):
        return self.widget.contextStatus()

    def sourceItem(self):
        return self.widget.sourceItem()

    def sourceContext(self):
        return self.widget.sourceContext()

    def resetSourceContext(self):
        self.widget.resetSourceContext()

    def setSourceContext(self, context, foundArk, contextType, contextDescription, foundFeature, foundSchematic):
        self.widget.setSourceContext(
            context, foundArk, contextType, contextDescription, foundFeature, foundSchematic)

    def sourceStatus(self):
        return self.widget.sourceStatus()
