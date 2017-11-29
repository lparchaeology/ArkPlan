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

from PyQt4.QtCore import QDir, QFile, QFileInfo, Qt
from PyQt4.QtGui import QAction, QDockWidget, QIcon

from qgis.core import QgsLayerTreeModel, QgsMapLayer, QgsMapLayerRegistry, QgsProject, QgsRasterLayer
from qgis.gui import QgsLayerTreeView

from ArkSpatial.ark.lib import Plugin
from ArkSpatial.ark.lib.core import Collection, CollectionSettings, layers
from ArkSpatial.ark.lib.gui import ToolDockWidget
from ArkSpatial.ark.lib.snapping import (IntersectionSnappingAction, LayerSnappingAction, ProjectSnappingAction,
                                         TopologicalEditingAction)

from ArkSpatial.ark.core import Config, Settings
from ArkSpatial.ark.grid import GridModule
from ArkSpatial.ark.gui import LayerTreeMenu, ProjectDialog, SelectItemDialog, SettingsDialog, SettingsWizard
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

    project = None  # QgsProject()

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

    projectLayerView = None  # QgsLayerTreeView()
    layerDock = None  # ToolDockWidget()

    # Private settings
    _initialised = False
    _loaded = False
    _layerSnappingAction = None  # LayerSnappingAction()
    _userDocks = []
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

        # TODO Excalibur Tools - Make wn plugin
        self._excalibur = QAction(QIcon(':/plugins/ark/excalibur.svg'), 'Excalibur', self.iface.mainWindow())
        self._excalibur.triggered.connect(self.pullExcalibur)
        self._excalibur.setEnabled(True)
        self._excalibur.setCheckable(False)
        self.iface.addToolBarIcon(self._excalibur)

    def isInitialised(self):
        return self._initialised

    def isLoaded(self):
        return self._loaded

    def isConfigured(self):
        return self.readBoolEntry('configured', False)

    def _setIsConfigured(self, configured):
        self.writeEntry('configured', configured)
        if not configured:
            self._initialised = False

    # Load the plugin gui
    def initGui(self):
        super(ArkSpatialPlugin, self).initGui()

        # Init the main dock so we have somethign to show on first run
        self.projectLayerView = QgsLayerTreeView()
        self.layerDock = ToolDockWidget(self.projectLayerView)
        self.layerDock.initGui(self.iface, Qt.LeftDockWidgetArea, self.pluginAction)
        self.layerDock.setWindowTitle(self.pluginName)
        self.layerDock.setObjectName(u'ArkLayerDock')
        self._layerSnappingAction = LayerSnappingAction(self.iface, self.projectLayerView)
        self.iface.legendInterface().addLegendLayerAction(
            self._layerSnappingAction, '', 'arksnap', QgsMapLayer.VectorLayer, True)

    # Initialise plugin gui
    def initialise(self):
        if self._initialised:
            return True

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
        self.layerDock.toolbar.addSeparator()
        self.gridModule = GridModule(self)
        self.gridModule.initGui()
        self.filterModule = FilterModule(self)
        self.filterModule.initGui()
        self.planModule = PlanModule(self)
        self.planModule.initGui()
        self.trenchModule = TrenchModule(self)
        self.trenchModule.initGui()

        # Add Settings to the toolbar
        self.layerDock.toolbar.addSeparator()
        self.addDockAction(':/plugins/ark/settings.svg', self.tr(u'Settings'), self._triggerSettingsDialog)

        # If the project or layers or legend indexes change make sure we stay updated
        self.legendInterface().groupIndexChanged.connect(self._groupIndexChanged)
        self.iface.projectRead.connect(self.loadProject)
        self.iface.newProjectCreated.connect(self.closeProject)

        self.project = QgsProject.instance()
        self._initialised = True
        return self._initialised

    # Load the project settings when project is loaded
    def loadProject(self):
        if self.isLoaded():
            self.closeProject()
        if self.isInitialised() and self.isConfigured():
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
            self.layerDock.menuAction().setChecked(False)

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
        del self.projectLayerView
        self.projectLayerView = None
        self.layerDock.unloadGui()
        del self.layerDock
        self.layerDock = None

        # Removes the plugin menu item and icon from QGIS GUI.
        super(ArkSpatialPlugin, self).unload()

    def run(self, checked):
        if checked and self.initialise() and self.configure():
            if not self._loaded:
                self.loadProject()
            # Close all open docks
            self._userDocks = []
            docks = self.iface.mainWindow().findChildren(QDockWidget)
            for dock in docks:
                if dock.isVisible() and dock.objectName() != 'ArkLayerDock':
                    self._userDocks.append(dock.objectName())
                    dock.setVisible(False)
        else:
            if self._initialised:
                self.data.dock.setVisible(False)
                self.planModule.dock.setVisible(False)
                self.gridModule.dock.setVisible(False)
                self.filterModule.dock.setVisible(False)
                self.trenchModule.dock.setVisible(False)
            for dock in self._userDocks:
                self.iface.mainWindow().findChild(QDockWidget, dock).setVisible(True)
            self._userDocks = []

    # Configure the project, i.e. load all settings for QgsProject but don't load anything until needed
    def configure(self):
        if self.isConfigured():
            return True
        # TODO more validation, check if files exist, etc
        wizard = SettingsWizard()
        if (wizard.exec_() and QDir(wizard.projectPath()).mkpath('.')):

            if (self.project.isDirty() and self.project.fileName()):
                self.project.write()
            self.project.clear()

            info = QFileInfo(wizard.projectPath() + '/' + wizard.projectFile() + '.qgs')
            self.project.setFileName(info.filePath())

            Settings.setArkUrl(wizard.arkUrl())
            Settings.setArkUser(wizard.arkUser())
            Settings.setArkPassword(wizard.arkPassword())

            Settings.setUserName(wizard.userFullname())
            Settings.setUserInitials(wizard.userInitials())

            Settings.setProjectCode(wizard.projectCode())
            Settings.setSiteCode(wizard.siteCode())

            self._configureCollection('grid')
            self._configureCollection('plan')
            self._configureCollection('section')
            self._configureCollection('site')

            self._configureDrawing('context')
            self._configureDrawing('plan')
            self._configureDrawing('section')

            self.writeProject()
            self._setIsConfigured(self.project.write())

        if not self.isConfigured():
            self.showCriticalMessage('ARK Project not configured, unable to continue!')
            self.layerDock.menuAction().setChecked(False)
            return False
        else:
            return True

    def _configureCollection(self, grp):
        config = Config.collections[grp]
        path = config['path']
        bufferPath = path + '/buffer'
        logPath = path + '/log'
        QDir(self.projectPath() + '/' + path).mkpath('.')
        if config['buffer']:
            QDir(self.projectPath() + '/' + bufferPath).mkpath('.')
        if config['log']:
            QDir(self.projectPath() + '/' + logPath).mkpath('.')
        lcs = CollectionSettings()
        lcs.collection = grp
        lcs.collectionPath = path
        lcs.parentGroupName = Config.projectGroupName
        lcs.collectionGroupName = config['groupName']
        lcs.bufferGroupName = config['bufferGroupName']
        lcs.log = config['log']

        lcs.pointsLayerLabel = config['pointsLabel']
        lcs.pointsLayerName = self._layerName(config['pointsBaseName'])
        lcs.pointsLayerPath = self._shapeFile(path, lcs.pointsLayerName)
        lcs.pointsStylePath = self._styleFile(path, lcs.pointsLayerName)
        if config['buffer']:
            lcs.pointsBufferName = lcs.pointsLayerName + Config.bufferSuffix
            lcs.pointsBufferPath = self._shapeFile(bufferPath, lcs.pointsBufferName)
        if config['log']:
            lcs.pointsLogName = lcs.pointsLayerName + Config.logSuffix
            lcs.pointsLogPath = self._shapeFile(logPath, lcs.pointsLogName)

        lcs.linesLayerLabel = config['linesLabel']
        lcs.linesLayerName = self._layerName(config['linesBaseName'])
        lcs.linesLayerPath = self._shapeFile(path, lcs.linesLayerName)
        lcs.linesStylePath = self._styleFile(path, lcs.linesLayerName)
        if config['buffer']:
            lcs.linesBufferName = lcs.linesLayerName + Config.bufferSuffix
            lcs.linesBufferPath = self._shapeFile(bufferPath, lcs.linesBufferName)
        if config['log']:
            lcs.linesLogName = lcs.linesLayerName + Config.logSuffix
            lcs.linesLogPath = self._shapeFile(logPath, lcs.linesLogName)

        lcs.polygonsLayerLabel = config['polygonsLabel']
        lcs.polygonsLayerName = self._layerName(config['polygonsBaseName'])
        lcs.polygonsLayerPath = self._shapeFile(path, lcs.polygonsLayerName)
        lcs.polygonsStylePath = self._styleFile(path, lcs.polygonsLayerName)
        if config['buffer']:
            lcs.polygonsBufferName = lcs.polygonsLayerName + Config.bufferSuffix
            lcs.polygonsBufferPath = self._shapeFile(bufferPath, lcs.polygonsBufferName)
        if config['log']:
            lcs.polygonsLogName = lcs.polygonsLayerName + Config.logSuffix
            lcs.polygonsLogPath = self._shapeFile(logPath, lcs.polygonsLogName)
        lcs.toProject(self.pluginName)
        if config['multi']:
            self._createCollectionMultiLayers(grp, lcs)
        else:
            self._createCollectionLayers(grp, lcs)
        return lcs

    def _configureDrawing(self, grp):
        self.rawDrawingDir(grp).mkpath('.')
        self.georefDrawingDir(grp).mkpath('.')

    def _toggleLayerView(self, enabled):
        self.projectLayerView.setVisible(enabled)
        self.layerDock.adjustSize()

    def _triggerSettingsDialog(self):
        if self.isConfigured():
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
        action = QAction(QIcon(iconPath), text, self.layerDock)
        if callback is not None:
            action.triggered.connect(callback)
        action.setEnabled(enabled)
        action.setCheckable(checkable)
        if tip is not None:
            action.setStatusTip(tip)
        if whatsThis is not None:
            action.setWhatsThis(whatsThis)
        self.layerDock.toolbar.addAction(action)
        # self.actions.append(action)
        return action

    # Project level settings
    # TODO Move to json file

    def logUpdates(self):
        return self.readBoolEntry('logUpdates', True)

    def setLogUpdates(self, logUpdates):
        self.writeEntry('logUpdates', logUpdates)

    def useCustomStyles(self):
        return self.readBoolEntry('useCustomStyles', False)

    def styleDir(self):
        return QDir(self.stylePath())

    def stylePath(self):
        path = self.readEntry('stylePath', '')
        if (not path):
            return self.pluginPath + '/styles'
        return path

    def setStylePath(self, useCustomStyles, absolutePath):
        self.writeEntry('useCustomStyles', useCustomStyles)
        if useCustomStyles:
            self.writeEntry('stylePath', absolutePath)
        else:
            self.writeEntry('stylePath', '')

    # Group settings

    def _drawingEntry(self, group, key, default=None):
        if default is None:
            default = Config.drawings[group][key]
        return self.readEntry(group + '/' + key, default)

    def _drawingBoolEntry(self, group, key, default=None):
        if default is None:
            default = Config.drawings[group][key]
        return self.readBoolEntry(group + '/' + key, default)

    def _setdrawingEntry(self, group, key, value, default=None):
        if default is None:
            default = Config.drawings[group][key]
        self.setEntry(group + '/' + key, value, default)

    def collection(self, collection):
        if collection == 'plan':
            return self.plan
        elif collection == 'section':
            return self.section
        elif collection == 'grid':
            return self.grid
        elif collection == 'site':
            return self.site

    # Raster Drawings settings

    def drawingDir(self, group):
        return QDir(self.drawingPath(group))

    def drawingPath(self, group):
        if self.useCustomPath(group):
            return self._drawingEntry(group, 'path')
        else:
            return self.projectPath() + '/' + Config.drawings[group]['path']

    def setDrawingPath(self, group, useCustomPath, absolutePath):
        self._setDrawingEntry(group, 'useCustomPath', useCustomPath, False)
        if useCustomPath:
            self._setDrawingEntry(group, 'path', absolutePath)
        else:
            self._setDrawingEntry(group, 'path', '')

    def useCustomPath(self, group):
        return self._drawingBoolEntry(group, 'useCustomPath', False)

    def rawDrawingDir(self, group):
        return QDir(self.rawDrawingPath(group))

    def rawDrawingPath(self, group):
        return self.drawingPath(group)

    def georefDrawingDir(self, group):
        return QDir(self.georefDrawingPath(group))

    def georefDrawingPath(self, group):
        if self.useGeorefFolder():
            return self.rawDrawingPath(group) + '/georef'
        return self.rawDrawingPath(group)

    def useGeorefFolder(self):
        return self.readBoolEntry('useGeorefFolder', True)

    def setUseGeorefFolder(self, useGeorefFolder):
        self.writeEntry('useGeorefFolder', useGeorefFolder)

    def drawingTransparency(self):
        return self.readNumEntry('drawingTransparency', 50)

    def setDrawingTransparency(self, transparency):
        self.writeEntry('drawingTransparency', transparency)

    def showSettingsDialog(self):
        settingsDialog = SettingsDialog(self, self.iface.mainWindow())
        return settingsDialog.exec_()

    # Identify Tool

    def triggerIdentifyAction(self, checked):
        if checked:
            self.mapCanvas().setMapTool(self.identifyMapTool)
        else:
            self.mapCanvas().unsetMapTool(self.identifyMapTool)

    # Show Items Tool

    def _showItem(self):
        classCodes = sorted(set(self.plan.uniqueValues('class')))
        dialog = SelectItemDialog(self.siteCodes(), self.siteCode(), classCodes, self.iface.mainWindow())
        if dialog.exec_():
            self.planModule.showItem(dialog.item(), dialog.loadDrawings(), dialog.zoomToItem())

    def pullExcalibur(self):
        dialog = ProjectDialog(self.iface.mainWindow())
        return dialog.exec_()
