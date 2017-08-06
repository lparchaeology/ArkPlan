# -*- coding: utf-8 -*-
"""
/***************************************************************************
                                ARK Spatial
                    A QGIS plugin for Archaeological Recording.
        Part of the Archaeological Recording Kit by L-P : Archaeology
                        http://ark.lparchaeology.com
                              -------------------
        copyright            : 2017 by L-P : Heritage LLP
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

from ark.lib.gui import ToolDockWidget

import .PlanWidget


class PlanDock(ToolDockWidget):

    # Toolbar Signals
    loadAnyFileSelected = pyqtSignal()
    loadRawFileSelected = pyqtSignal()
    loadGeoFileSelected = pyqtSignal()

    # Drawing Signals
    resetSelected = pyqtSignal()
    mergeSelected = pyqtSignal()

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
        super(PlanDock, self).__init__(PlanWidget(), parent)

        self.setWindowTitle(u'ARK Drawing')
        self.setObjectName(u'PlanDock')

    def initGui(self, iface, location, menuAction):
        super(PlanDock, self).initGui(iface, location, menuAction)

        # Init the toolbar
        self.toolbar.addAction(iface.actionPan())
        self.toolbar.addAction(iface.actionZoomIn())
        self.toolbar.addAction(iface.actionZoomOut())
        self.toolbar.addAction(iface.actionZoomLast())
        self.toolbar.addAction(iface.actionZoomNext())

        self.toolbar.addSeparator()

        self.toolbar.addAction(
            QIcon(':/plugins/ark/plan/georef.png'), self.tr(u'Georeference Any Drawing'), self.loadAnyFileSelected)
        self.toolbar.addAction(
            QIcon(':/plugins/ark/grid/grid.png'), self.tr(u'Georeference Raw Drawings'), self.loadRawFileSelected)
        self.toolbar.addAction(QIcon(':/plugins/ark/plan/loadDrawings.svg'),
                               self.tr(u'Load Georeferenced Drawings'), self.loadGeoFileSelected)

        # Init the child widgets
        self.widget.drawingWidget.initGui(iface)
        self.widget.schematicWidget.initGui()
        self.widget.snappingWidget.initGui()

        # Cascade the child widget signals
        self.widget.drawingWidget.resetButton.clicked.connect(self.resetSelected)
        self.widget.drawingWidget.mergeButton.clicked.connect(self.mergeSelected)

        self.widget.schematicWidget.loadArkData.connect(self.loadArkData)
        self.widget.schematicWidget.mapActionChanged.connect(self.mapActionChanged)
        self.widget.schematicWidget.filterActionChanged.connect(self.filterActionChanged)
        self.widget.schematicWidget.drawingActionChanged.connect(self.drawingActionChanged)
        self.widget.schematicWidget.openContextData.connect(self.openContextData)
        self.widget.schematicWidget.openSourceContextData.connect(self.openSourceContextData)
        self.widget.schematicWidget.findContextSelected.connect(self.findContextSelected)
        self.widget.schematicWidget.firstContextSelected.connect(self.firstContextSelected)
        self.widget.schematicWidget.lastContextSelected.connect(self.lastContextSelected)
        self.widget.schematicWidget.prevContextSelected.connect(self.prevContextSelected)
        self.widget.schematicWidget.nextContextSelected.connect(self.nextContextSelected)
        self.widget.schematicWidget.prevMissingSelected.connect(self.prevMissingSelected)
        self.widget.schematicWidget.nextMissingSelected.connect(self.nextMissingSelected)
        self.widget.schematicWidget.schematicReportSelected.connect(self.schematicReportSelected)
        self.widget.schematicWidget.editContextSelected.connect(self.editContextSelected)
        self.widget.schematicWidget.deleteSectionSchematicSelected.connect(self.deleteSectionSchematicSelected)
        self.widget.schematicWidget.findSourceSelected.connect(self.findSourceSelected)
        self.widget.schematicWidget.copySourceSelected.connect(self.copySourceSelected)
        self.widget.schematicWidget.cloneSourceSelected.connect(self.cloneSourceSelected)
        self.widget.schematicWidget.editSourceSelected.connect(self.editSourceSelected)
        self.widget.schematicWidget.contextChanged.connect(self.contextChanged)
        self.widget.schematicWidget.resetSelected.connect(self.resetSchematicSelected)

    def unloadGui(self):
        self.widget.drawingWidget.unloadGui()
        self.widget.schematicWidget.unloadGui()
        self.widget.snappingWidget.unloadGui()
        del self.widget.snappingWidget
        super(PlanDock, self).unloadGui()

    # Load the project settings when project is loaded
    def loadProject(self, project):
        self.widget.drawingWidget.loadProject(project)
        self.widget.schematicWidget.loadProject(project)
        self.widget.snappingWidget.loadProject(project)

    # Close the project
    def closeProject(self):
        self.widget.drawingWidget.closeProject()
        self.widget.schematicWidget.closeProject()
        self.widget.snappingWidget.closeProject()

    # Drawing methods pass-through

    def source(self):
        return self.widget.drawingWidget.source()

    def setSource(self, source):
        self.widget.drawingWidget.setSource(source)

    # Schematic methods pass-through

    def activateArkData(self):
        self.widget.schematicWidget.activateArkData()

    def activateSchematicCheck(self):
        self.widget.setCurrentIndex(1)
        self.widget.schematicWidget.contextSpin.setFocus()

    def contextItem(self):
        return self.widget.schematicWidget.contextItem()

    def context(self):
        return self.widget.schematicWidget.context()

    def resetContext(self):
        self.widget.schematicWidget.resetContext()

    def setContext(self, context, foundArkData, contextType, contextDescription, foundFeatureData, foundSchematic, foundSectionSchematic):
        self.widget.schematicWidget.setContext(
            context, foundArkData, contextType, contextDescription, foundFeatureData, foundSchematic, foundSectionSchematic)

    def contextStatus(self):
        return self.widget.schematicWidget.contextStatus()

    def sourceItem(self):
        return self.widget.schematicWidget.sourceItem()

    def sourceContext(self):
        return self.widget.schematicWidget.sourceContext()

    def resetSourceContext(self):
        self.widget.schematicWidget.resetSourceContext()

    def setSourceContext(self, context, foundArk, contextType, contextDescription, foundFeature, foundSchematic):
        self.widget.schematicWidget.setSourceContext(
            context, foundArk, contextType, contextDescription, foundFeature, foundSchematic)

    def sourceStatus(self):
        return self.widget.schematicWidget.sourceStatus()
