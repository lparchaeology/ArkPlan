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
from PyQt4.QtGui import QDockWidget, QTabWidget, QMenu, QAction, QIcon, QToolButton

from qgis.core import QgsProject

from ..libarkqgis.dock import ToolDockWidget
from ..libarkqgis.snapping import *

import plan_widget_base

class PlanWidget(QTabWidget, plan_widget_base.Ui_PlanWidget):

    def __init__(self, parent=None):
        super(PlanWidget, self).__init__(parent)
        self.setupUi(self)


class PlanDock(ToolDockWidget):

    # Toolbar Signals
    loadRawFileSelected = pyqtSignal()
    loadGeoFileSelected = pyqtSignal()

    # Drawing Signals
    autoSchematicSelected = pyqtSignal()
    editPointsSelected = pyqtSignal()
    editLinesSelected = pyqtSignal()
    editPolygonsSelected = pyqtSignal()
    featureNameChanged = pyqtSignal(str)
    sectionChanged = pyqtSignal(object)
    clearSelected = pyqtSignal()
    mergeSelected = pyqtSignal()

    # Schematic Signals
    findContextSelected = pyqtSignal()
    zoomContextSelected = pyqtSignal()
    editContextSelected = pyqtSignal()
    findSourceSelected = pyqtSignal()
    zoomSourceSelected = pyqtSignal()
    copySourceSelected = pyqtSignal()
    cloneSourceSelected = pyqtSignal()
    editSourceSelected = pyqtSignal()
    resetSelected = pyqtSignal()

    _iface = None # QgsisInterface()
    _snappingAction = None  # ProjectSnappingAction()
    _interAction = None  # IntersectionSnappingAction()
    _topoAction = None  # TopologicalEditingAction()

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
        self._snappingAction = ProjectSnappingAction(self)
        self._snappingAction.setInterface(iface)
        self.toolbar.addAction(self._snappingAction)
        self._interAction = IntersectionSnappingAction(self)
        self.toolbar.addAction(self._interAction)
        self._topoAction = TopologicalEditingAction(self)
        self.toolbar.addAction(self._topoAction)

        self.toolbar2.setVisible(True)
        self.toolbar2.addAction(QIcon(':/plugins/ark/plan/georef.png'), self.tr(u'Georeference Raw Drawings'), self.loadRawFileSelected)
        self.toolbar2.addAction(QIcon(':/plugins/ark/plan/loadDrawings.svg'), self.tr(u'Load Georeferenced Drawings'), self.loadGeoFileSelected)
        self.toolbar2.addSeparator()
        self.toolbar2.addAction(QIcon(':/plugins/ark/plan/editPoints.svg'), self.tr(u'Edit Points in Buffer'), self.editPointsSelected)
        self.toolbar2.addAction(QIcon(':/plugins/ark/plan/editLines.svg'), self.tr(u'Edit Lines in Buffer'), self.editLinesSelected)
        self.toolbar2.addAction(QIcon(':/plugins/ark/plan/editPolygons.svg'), self.tr(u'Edit Polygons in Buffer'), self.editPolygonsSelected)

        # Init the child widgets
        self.widget.metadataWidget.initGui()
        self.widget.drawingWidget.initGui()
        self.widget.schematicWidget.initGui()
        self.widget.snappingWidget.initGui()

        # Cascade the child widget signals
        self.widget.drawingWidget.autoSchematicSelected.connect(self.autoSchematicSelected)
        self.widget.drawingWidget.featureNameChanged.connect(self.featureNameChanged)
        self.widget.drawingWidget.sectionChanged.connect(self.sectionChanged)

        self.widget.clearButton.clicked.connect(self.clearSelected)
        self.widget.mergeButton.clicked.connect(self.mergeSelected)

        self.widget.schematicWidget.findContextSelected.connect(self.findContextSelected)
        self.widget.schematicWidget.zoomContextSelected.connect(self.zoomContextSelected)
        self.widget.schematicWidget.editContextSelected.connect(self.editContextSelected)
        self.widget.schematicWidget.findSourceSelected.connect(self.findSourceSelected)
        self.widget.schematicWidget.zoomSourceSelected.connect(self.zoomSourceSelected)
        self.widget.schematicWidget.copySourceSelected.connect(self.copySourceSelected)
        self.widget.schematicWidget.cloneSourceSelected.connect(self.cloneSourceSelected)
        self.widget.schematicWidget.editSourceSelected.connect(self.editSourceSelected)

        self.widget.schematicWidget.resetButton.clicked.connect(self.resetSelected)

    def unloadGui(self):
        self.widget.metadataWidget.unloadGui()
        self.widget.drawingWidget.unloadGui()
        self.widget.schematicWidget.unloadGui()
        self.widget.snappingWidget.unloadGui()
        del self.widget.snappingWidget
        self._snappingAction.unload()
        del self._snappingAction
        self._interAction.unload()
        del self._interAction
        self._topoAction.unload()
        del self._topoAction
        super(PlanDock, self).unloadGui()

    # Load the project settings when project is loaded
    def loadProject(self, project):
        self.widget.metadataWidget.loadProject(project)
        self.widget.drawingWidget.loadProject(project)
        self.widget.schematicWidget.loadProject(project)
        self.widget.snappingWidget.loadProject(project)

    # Close the project
    def closeProject(self):
        self.widget.metadataWidget.closeProject()
        self.widget.drawingWidget.closeProject()
        self.widget.schematicWidget.closeProject()
        self.widget.snappingWidget.closeProject()

    # Drawing methods pass-through
    def setFeatureName(self, name):
        self.widget.drawingWidget.setFeatureName(name)

    def initSections(self, itemList):
        self.widget.drawingWidget.initSections(itemList)

    def sectionKey(self):
        return self.widget.drawingWidget.sectionKey()

    def setSection(self, itemKey):
        self.widget.drawingWidget.setSection(itemList)

    def addDrawingTool(self, dockTab, action):
        self.widget.drawingWidget.addDrawingTool(dockTab, action)

    # Schematic methods pass-through

    def activateSchematicCheck(self):
        self.widget.setCurrentIndex(1)
        self.widget.schematicWidget.contextSpin.setFocus()

    def contextItemKey(self):
        return self.widget.schematicWidget.contextItemKey()

    def context(self):
        return self.widget.schematicWidget.context()

    def setContext(self, context, foundData, foundSchematic, foundSectionSchematic):
        self.widget.schematicWidget.setContext(context, foundData, foundSchematic, foundSectionSchematic)

    def contextStatus(self):
        return self.widget.schematicWidget.contextStatus()

    def sourceItemKey(self):
        return self.widget.schematicWidget.sourceItemKey()

    def sourceContext(self):
        return self.widget.schematicWidget.sourceContext()

    def setSourceContext(self, context, foundData, foundSchematic):
        self.widget.schematicWidget.setSourceContext(context, foundData, foundSchematic)

    def sourceStatus(self):
        return self.widget.schematicWidget.sourceStatus()
