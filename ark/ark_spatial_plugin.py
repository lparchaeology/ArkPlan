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

from PyQt4.QtCore import QDir, QFile, Qt
from PyQt4.QtGui import QAction, QDockWidget, QIcon

from qgis.core import QgsLayerTreeModel, QgsMapLayer, QgsMapLayerRegistry, QgsProject, QgsRasterLayer
from qgis.gui import QgsLayerTreeView

from ArkSpatial.ark.lib import Plugin, Project
from ArkSpatial.ark.lib.core import Collection, CollectionSettings, layers
from ArkSpatial.ark.lib.gui import ToolDockWidget
from ArkSpatial.ark.lib.snapping import (IntersectionSnappingAction, LayerSnappingAction, ProjectSnappingAction,
                                         TopologicalEditingAction)

from ArkSpatial.ark.core import Config, Settings
from ArkSpatial.ark.grid import GridModule
from ArkSpatial.ark.gui import (LayerTreeMenu, ProjectDialog, ProjectDock, SelectItemDialog, SettingsDialog,
                                ProjectWizard, PreferencesWizard, PreferencesDialog)
from ArkSpatial.ark.map import MapToolIndentifyItems

from .data_module import DataModule
from .filter_module import FilterModule
from .plan_module import PlanModule
from .trench_module import TrenchModule

import georef.ui.resources
import grid.ui.resources
import gui.ui.resources
import lib.snapping.resources


class ArkSpatialPlugin(Plugin):

    """QGIS Plugin Implementation."""

    # Tools
    identifyMapTool = None  # MapToolIndentifyItems()

    # Modules
    data = None  # Data()
    gridModule = None  # Grid()
    planModule = None  # Plan()
    filterModule = None  # FilterModule()
    trenchModule = None  # TrenchModule()

    projectGroupIndex = -1
    drawingsGroupIndex = -1
    drawingsGroupName = ''

    geoLayer = None  # QgsRasterLayer()
    plan = None  # Collection()
    section = None  # Collection()
    grid = None  # Collection()
    site = None  # Collection()

    # projectLayerView = None  # QgsLayerTreeView()
    projectDock = None  # ProjectDock()

    # Private settings
    _initialised = False
    _loaded = False
    _layerSnappingAction = None  # LayerSnappingAction()
    _snappingAction = None  # ProjectSnappingAction()
    _interAction = None  # IntersectionSnappingAction()
    _topoAction = None  # TopologicalEditingAction()

    def __init__(self, iface, pluginPath):
        super(ArkSpatialPlugin, self).__init__(
            iface=iface,
            pluginName=Config.pluginName,
            pluginScope=Config.pluginScope,
            pluginIconPath=':/plugins/ark/icon.png',
            pluginPath=pluginPath,
            menuGroup=Plugin.PluginsGroup,
            toolbarGroup=Plugin.PluginsGroup,
            checkable=True
        )
        # Set display / menu name now we have tr() set up
        self.setDisplayName(self.tr(u'&ARKspatial'))

        self._snappingAction = ProjectSnappingAction(iface.mainWindow())
        # TODO Snapping Tools - Make own plugin!
        self._snappingAction.setInterface(iface)
        self.iface.addToolBarIcon(self._snappingAction)
        self._interAction = IntersectionSnappingAction(iface.mainWindow())
        self.iface.addToolBarIcon(self._interAction)
        self._topoAction = TopologicalEditingAction(iface.mainWindow())
        self.iface.addToolBarIcon(self._topoAction)

        # TODO Excalibur Tools - Make own plugin
        self._excalibur = QAction(QIcon(':/plugins/ark/excalibur.svg'), 'Excalibur', self.iface.mainWindow())
        self._excalibur.triggered.connect(self.pullExcalibur)
        self._excalibur.setEnabled(True)
        self._excalibur.setCheckable(False)
        self.iface.addToolBarIcon(self._excalibur)

    def isInitialised(self):
        return self._initialised

    def isLoaded(self):
        return self._loaded

    # Load the plugin gui
    def initGui(self):
        super(ArkSpatialPlugin, self).initGui()

        # Init the main dock so we have somethign to show on first run
        self.projectDock = ProjectDock()
        self.projectDock.initGui(self.iface, Qt.LeftDockWidgetArea, self.pluginAction)
        # self.projectLayerView = QgsLayerTreeView()
        # self._layerSnappingAction = LayerSnappingAction(self.iface, self.projectLayerView)
        # self.iface.legendInterface().addLegendLayerAction(
        #    self._layerSnappingAction, '', 'arksnap', QgsMapLayer.VectorLayer, True)
        self.addNewAction(':/plugins/ark/settings.svg', self.tr(u'Preferences'),
                          self.configurePlugin(), addToToolbar=False)

    # Initialise plugin gui
    def initialise(self):
        if self._initialised:
            return True

        """
        # Create the Layer Model and View
        # TODO Should only show our subgroup but crashes!
        # self.projectLayerModel
        # = QgsLayerTreeModel(QgsProject.instance().layerTreeRoot().findGroup(Config.projectGroupName), self);
        self.projectLayerModel = QgsLayerTreeModel(QgsProject.instance().layerTreeRoot(), self)
        self.projectLayerModel.setFlag(QgsLayerTreeModel.ShowLegend)
        self.projectLayerModel.setFlag(QgsLayerTreeModel.ShowLegendAsTree)
        self.projectLayerModel.setFlag(QgsLayerTreeModel.AllowNodeReorder, True)
        self.projectLayerModel.setFlag(QgsLayerTreeModel.AllowNodeRename, False)
        self.projectLayerModel.setFlag(QgsLayerTreeModel.AllowNodeChangeVisibility)
        self.projectLayerModel.setFlag(QgsLayerTreeModel.AllowLegendChangeState)
        self.projectLayerModel.setFlag(QgsLayerTreeModel.AllowSymbologyChangeState)
        self.projectLayerModel.setAutoCollapseLegendNodes(-1)
        self.projectLayerView.setModel(self.projectLayerModel)
        menuProvider = LayerTreeMenu(self, self.projectLayerView)
        self.projectLayerView.setMenuProvider(menuProvider)
        self.projectLayerView.setCurrentLayer(self.iface.activeLayer())
        self.projectLayerView.doubleClicked.connect(self.iface.actionOpenTable().trigger)
        self.projectLayerView.currentLayerChanged.connect(self.mapCanvas().setCurrentLayer)
        self.projectLayerView.currentLayerChanged.connect(self.iface.setActiveLayer)
        self.iface.currentLayerChanged.connect(self.projectLayerView.setCurrentLayer)
        self.layerViewAction = self.addDockAction(
            ':/plugins/ark/tree.svg', self.tr(u'Toggle Layer View'), callback=self._toggleLayerView, checkable=True)
        self.layerViewAction.setChecked(True)
        """

        # Init the identify tool and add to the toolbar
        self.identifyAction = self.addDockAction(
            ':/plugins/ark/filter/identify.png',
            self.tr(u'Identify Items'),
            callback=self.triggerIdentifyAction,
            checkable=True
        )
        self.identifyMapTool = MapToolIndentifyItems(self)
        self.identifyMapTool.setAction(self.identifyAction)

        # Init the Load Item tool and add to the toolbar
        self.showItemAction = self.addDockAction(
            ':/plugins/ark/filter/showContext.png',
            self.tr(u'Show Item'),
            callback=self._showItem
        )

        # Init the modules and add to the toolbar
        self.data = DataModule(self)
        self.data.initGui()
        self.projectDock.toolbar.addSeparator()
        self.gridModule = GridModule(self)
        self.gridModule.initGui()
        self.filterModule = FilterModule(self)
        self.filterModule.initGui()
        self.planModule = PlanModule(self)
        self.planModule.initGui()
        self.trenchModule = TrenchModule(self)
        self.trenchModule.initGui()

        # Add Settings to the toolbar
        self.projectDock.toolbar.addSeparator()
        self.addDockAction(':/plugins/ark/settings.svg', self.tr(u'Project Settings'), self._triggerSettingsDialog)

        # If the project or layers or legend indexes change make sure we stay updated
        self.legendInterface().groupIndexChanged.connect(self._groupIndexChanged)
        self.iface.projectRead.connect(self.loadProject)
        self.iface.newProjectCreated.connect(self.closeProject)

        self._initialised = True
        return self._initialised

    # Load the project settings when project is loaded
    def loadProject(self):
        if self.isLoaded():
            self.closeProject()
        if self.isInitialised() and Settings.isProjectConfigured():
            self.projectGroupIndex = layers.createLayerGroup(self.iface, Config.projectGroupName)
            # Load the layer collections
            self.grid = self._loadCollection('grid')
            self.plan = self._loadCollection('plan')
            self.section = self._loadCollection('section')
            self.site = self._loadCollection('site')
            self.drawingsGroupName = Config.drawings['context']['layersGroupName']
            if (self.grid.initialise()
                    and self.plan.initialise()
                    and self.section.initialise()
                    and self.site.initialise()):
                self.data.loadProject()
                self.gridModule.loadProject()
                self.planModule.loadProject()
                self.filterModule.loadProject()
                self._loaded = True

    # Write the project for saving
    def writeProject(self):
        if self.isLoaded():
            self.data.writeProject()
            self.gridModule.writeProject()
            self.planModule.writeProject()
            self.filterModule.writeProject()

    # Close the project
    def closeProject(self):
        if self.identifyMapTool.action() and self.identifyMapTool.action().isChecked():
            self.iface.actionPan().trigger()
        if self.isLoaded():
            self.writeProject()
            self.data.closeProject()
            self.gridModule.closeProject()
            self.planModule.closeProject()
            self.filterModule.closeProject()
            # Unload the layers
            if self.plan is not None:
                self.plan.unload()
                self.plan = None
            if self.section is not None:
                self.section.unload()
                self.section = None
            if self.grid is not None:
                self.grid.unload()
                self.grid = None
            if self.site is not None:
                self.site.unload()
                self.site = None
            self._loaded = False

    # Unload the plugin
    def unload(self):
        if self.isInitialised():
            self.closeProject()

            # Restore the original QGIS gui
            self.projectDock.menuAction().setChecked(False)

            # Unload the modules in dependence order
            self.planModule.unloadGui()
            self.filterModule.unloadGui()
            self.gridModule.unloadGui()
            self.data.unloadGui()

            self._initialised = False

        self.iface.legendInterface().removeLegendLayerAction(self._layerSnappingAction)
        self.iface.removeToolBarIcon(self._snappingAction)
        self._snappingAction.unload()
        del self._snappingAction
        self.iface.removeToolBarIcon(self._interAction)
        self._interAction.unload()
        del self._interAction
        self.iface.removeToolBarIcon(self._topoAction)
        self._topoAction.unload()
        del self._topoAction

        self.iface.removeToolBarIcon(self._excalibur)

        # Unload this dock and uninitialise
        # del self.projectLayerView
        # self.projectLayerView = None
        self.projectDock.unloadGui()
        del self.projectDock
        self.projectDock = None

        # Removes the plugin menu item and icon from QGIS GUI.
        super(ArkSpatialPlugin, self).unload()

    def run(self, checked):
        if checked and self.initialise() and self.configure():
            if not self._loaded:
                self.loadProject()
        else:
            if self._initialised:
                self.data.dock.setVisible(False)
                self.planModule.dock.setVisible(False)
                self.gridModule.dock.setVisible(False)
                self.filterModule.dock.setVisible(False)
                self.trenchModule.dock.setVisible(False)

    def configurePlugin(self):
        if Settings.isPluginConfigured():
            prefs = PreferencesDialog(self.iface.mainWindow())
        else:
            prefs = PreferencesWizard(self.iface.mainWindow())

        ok = prefs.exec_() and prefs.preferences().projectsDir().exists()

        if ok:
            Settings.setUserFullName(prefs.preferences().userFullName())
            Settings.setUserInitials(prefs.preferences().userInitials())
            Settings.setUserOrganisation(prefs.preferences().userOrganisation())
            Settings.setProjectsFolder(prefs.preferences().projectsFolder())

            Settings.setServerUrl(prefs.server().url())
            Settings.setServerCredentials(prefs.server().user(), prefs.server().password())

            Settings.setPluginConfigured()

        return ok

    def configureProject(self):
        if Settings.isProjectConfigured():
            settings = ProjectDialog(self.iface.mainWindow())
        else:
            settings = ProjectWizard(self.iface.mainWindow())

        ok = settings.exec_()

        if ok and settings.projectDir().mkpath('.'):

            if wizard.clearProject():
                if Project.exists():
                    Project.write()
                Project.clear()

            Project.setFileName(wizard.projectFileInfo().absoluteFilePath())
            Project.setTitle(wizard.projectName())

            Settings.setServerUrl(wizard.server().url())
            Settings.setServerCredentials(wizard.server().user(), wizard.server().password())

            Settings.setProjectCode(wizard.projectCode())
            Settings.setSiteCode(wizard.siteCode())

            # self._configureDrawing('context')
            # self._configureDrawing('plan')
            # self._configureDrawing('section')

            self.writeProject()
            self._initialised = Project.write()
            if self._initialised:
                Settings.setProjectConfigured()

    # Configure the project, i.e. load all settings for QgsProject but don't load anything until needed
    def configure(self):
        if Settings.isProjectConfigured():
            return True
        # TODO more validation, check if files exist, etc
        wizard = ProjectWizard()
        if wizard.exec_() and wizard.projectDir().mkpath('.'):

            if wizard.clearProject():
                if Project.exists():
                    Project.write()
                Project.clear()

            Project.setFileName(wizard.projectFileInfo().absoluteFilePath())
            Project.setTitle(wizard.projectName())

            Settings.setServerUrl(wizard.server().url())
            Settings.setServerCredentials(wizard.server().user(), wizard.server().password())

            Settings.setProjectCode(wizard.projectCode())
            Settings.setSiteCode(wizard.siteCode())

            # self._configureDrawing('context')
            # self._configureDrawing('plan')
            # self._configureDrawing('section')

            self.writeProject()
            self._initialised = Project.write()
            if self._initialised:
                Settings.setProjectConfigured()

        if not Settings.isProjectConfigured():
            self.showCriticalMessage('ARK Project not configured, unable to continue!')
            self.projectDock.menuAction().setChecked(False)
            return False
        else:
            return True

    def _configureDrawing(self, grp):
        self.rawDrawingDir(grp).mkpath('.')
        self.georefDrawingDir(grp).mkpath('.')

    def _triggerSettingsDialog(self):
        if Settings.isProjectConfigured():
            self.showSettingsDialog()
        else:
            self.configure()

    def _groupIndexChanged(self, oldIndex, newIndex):
        if (oldIndex == self.projectGroupIndex):
            self.projectGroupIndex = newIndex

    def loadGeoLayer(self, geoFile, zoomToLayer=True):
        # TODO Check if already loaded, remove old one?
        self.geoLayer = QgsRasterLayer(geoFile.absoluteFilePath(), geoFile.completeBaseName())
        self.geoLayer.renderer().setOpacity(self.drawingTransparency() / 100.0)
        QgsMapLayerRegistry.instance().addMapLayer(self.geoLayer)
        if (self.drawingsGroupIndex < 0):
            self.drawingsGroupIndex = layers.createLayerGroup(
                self.iface, self.drawingsGroupName, Config.projectGroupName)
        self.legendInterface().moveLayer(self.geoLayer, self.drawingsGroupIndex)
        if zoomToLayer:
            self.mapCanvas().setExtent(self.geoLayer.extent())

    def clearDrawings(self):
        if (self.drawingsGroupIndex >= 0):
            self.drawingsLayerTreeGroup().removeAllChildren()

    def drawingsLayerTreeGroup(self):
        if (self.drawingsGroupIndex >= 0):
            return QgsProject.instance().layerTreeRoot().findGroup(self.drawingsGroupName)
        else:
            return None

    def isArkGroup(self, name):
        return (name == Config.projectGroupName
                or self.plan.isCollectionGroup(name)
                or self.section.isCollectionGroup(name)
                or self.site.isCollectionGroup(name)
                or self.grid.isCollectionGroup(name)
                or name == self.drawingsGroupName)

    def isArkLayer(self, layerId):
        return (layerId == self.plan.pointsLayerId
                or self.plan.isCollectionLayer(layerId)
                or self.section.isCollectionLayer(layerId)
                or self.site.isCollectionLayer(layerId)
                or self.grid.isCollectionLayer(layerId))

    def _shapeFile(self, layerPath, layerName):
        return layerPath + '/' + layerName + '.shp'

    def _styleFile(self, layerPath, layerName):
        # First see if the layer itself has a default style saved
        filePath = layerPath + '/' + layerName + '.qml'
        if QFile.exists(filePath):
            return filePath
        # Next see if the layer name has a style in the styles folder (which may
        # be a special folder, the site folder or the plugin folder)
        filePath = self.stylePath() + '/' + layerName + '.qml'
        if QFile.exists(filePath):
            return filePath
        # Finally, check the plugin folder for the default style
        filePath = self.pluginPath + '/ark/styles/' + layerName + '.qml'
        if QFile.exists(filePath):
            return filePath
        # If we didn't find that then something is wrong!
        return ''

    def _loadCollection(self, collection):
        lcs = CollectionSettings.fromProject(self.pluginName, collection)
        if (lcs.collection == ''):
            lcs = self._configureCollection(collection)
        if lcs.pointsStylePath == '':
            lcs.pointsStylePath = self._stylePath(
                lcs.collection, lcs.collectionPath, lcs.pointsLayerName)
        if lcs.linesStylePath == '':
            lcs.linesStylePath = self._stylePath(
                lcs.collection, lcs.collectionPath, lcs.linesLayerName)
        if lcs.polygonsStylePath == '':
            lcs.polygonsStylePath = self._stylePath(
                lcs.collection, lcs.collectionPath, lcs.polygonsLayerName)
        return Collection(self.iface, self.projectPath(), lcs)

    def _stylePath(self, collection, collectionPath, layerName):
        return self._styleFile(collectionPath, layerName)

    def addDockAction(self, iconPath, text, callback=None, enabled=True, checkable=False, tip=None, whatsThis=None):
        action = QAction(QIcon(iconPath), text, self.projectDock)
        if callback is not None:
            action.triggered.connect(callback)
        action.setEnabled(enabled)
        action.setCheckable(checkable)
        if tip is not None:
            action.setStatusTip(tip)
        if whatsThis is not None:
            action.setWhatsThis(whatsThis)
        self.projectDock.toolbar.addAction(action)
        # self.actions.append(action)
        return action

    def collection(self, collection):
        if collection == 'plan':
            return self.plan
        elif collection == 'section':
            return self.section
        elif collection == 'grid':
            return self.grid
        elif collection == 'site':
            return self.site

    # Identify Tool

    def triggerIdentifyAction(self, checked):
        if checked:
            self.mapCanvas().setMapTool(self.identifyMapTool)
        else:
            self.mapCanvas().unsetMapTool(self.identifyMapTool)

    # Show Items Tool

    def _showItem(self):
        classCodes = sorted(set(self.plan.uniqueValues('class')))
        dialog = SelectItemDialog(Settings.siteCodes(), Settings.siteCode(), classCodes, self.iface.mainWindow())
        if dialog.exec_():
            self.planModule.showItem(dialog.item(), dialog.loadDrawings(), dialog.zoomToItem())

    def pullExcalibur(self):
        dialog = ProjectDialog(self.iface.mainWindow())
        return dialog.exec_()
