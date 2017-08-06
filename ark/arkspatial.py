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

from PyQt4.QtCore import QDir, QFile, QFileInfo, Qt
from PyQt4.QtGui import QAction, QDockWidget, QIcon

from qgis.core import (QGis, QgsField, QgsFields, QgsLayerTreeModel, QgsMapLayer, QgsMapLayerRegistry, QgsProject,
                       QgsRasterLayer)
from qgis.gui import QgsLayerTreeView

from ark.lib import Plugin
from ark.lib.core import LayerCollection, LayerCollectionSettings, layers
from ark.lib.gui import ToolDockWidget
from ark.lib.snapping import (IntersectionSnappingAction, LayerSnappingAction, ProjectSnappingAction,
                              TopologicalEditingAction)

from ark.core import Config
from ark.grid import GridModule
from ark.gui import LayerTreeMenu, SelectItemDialog, SettingsDialog, SettingsWizard
from ark.map import MapToolIndentifyItems

from data_module import DataModule
from filter_module import FilterModule
from plan_module import PlanModule


class ArkSpatial(Plugin):

    """QGIS Plugin Implementation."""

    project = None  # QgsProject()

    # Tools
    identifyMapTool = None  # MapToolIndentifyItems()

    # Modules
    data = None  # Data()
    gridModule = None  # Grid()
    planModule = None  # Plan()
    filterModule = None  # FilterModule()

    projectGroupIndex = -1
    drawingsGroupIndex = -1
    drawingsGroupName = ''

    geoLayer = None  # QgsRasterLayer()
    plan = None  # LayerCollection()
    section = None  # LayerCollection()
    grid = None  # LayerCollection()
    site = None  # LayerCollection()

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
        super(ArkSpatial, self).__init__(iface, Config.pluginName, ':/plugins/ark/icon.png', pluginPath,
                                         Plugin.PluginsGroup, Plugin.PluginsGroup, checkable=True)
        # Set display / menu name now we have tr() set up
        self.setDisplayName(self.tr(u'&ARK Spatial'))

        # TODO Make own plugin!
        self._snappingAction = ProjectSnappingAction(iface.mainWindow())
        self._snappingAction.setInterface(iface)
        self.iface.addToolBarIcon(self._snappingAction)
        self._interAction = IntersectionSnappingAction(iface.mainWindow())
        self.iface.addToolBarIcon(self._interAction)
        self._topoAction = TopologicalEditingAction(iface.mainWindow())
        self.iface.addToolBarIcon(self._topoAction)

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
        super(ArkSpatial, self).initGui()

        # Init the main dock so we have somethign to show on first run
        self.projectLayerView = QgsLayerTreeView()
        self.layerDock = ToolDockWidget(self.projectLayerView)
        self.layerDock.initGui(self.iface, Qt.LeftDockWidgetArea, self.pluginAction)
        self.layerDock.setWindowTitle(self.tr(u'ARK Spatial'))
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
            checkable=True)
        self.identifyMapTool = MapToolIndentifyItems(self)
        self.identifyMapTool.setAction(self.identifyAction)

        # Init the Load Item tool and add to the toolbar
        self.showItemAction = self.addDockAction(
            ':/plugins/ark/filter/showContext.png', self.tr(u'Show Item'), callback=self._showItem)

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
        self._snappingAction.unload()
        del self._snappingAction
        self._interAction.unload()
        del self._interAction
        self._topoAction.unload()
        del self._topoAction

        # Unload this dock and uninitialise
        del self.projectLayerView
        self.projectLayerView = None
        self.layerDock.unloadGui()
        del self.layerDock
        self.layerDock = None

        # Removes the plugin menu item and icon from QGIS GUI.
        super(ArkSpatial, self).unload()

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
            for dock in self._userDocks:
                self.iface.mainWindow().findChild(QDockWidget, dock).setVisible(True)
            self._userDocks = []

    # Configure the project, i.e. load all settings for QgsProject but don't load anything until needed
    def configure(self):
        if self.isConfigured():
            return True
        # TODO more validation, check if files exist, etc
        wizard = SettingsWizard()
        if (wizard.exec_()
                and wizard.projectPath()
                and (wizard.projectCode() or wizard.siteCodes())
                and QDir(wizard.projectPath()).mkpath('.')):

            if (self.project.isDirty() and self.project.fileName()):
                self.project.write()
            self.project.clear()

            QDir(wizard.projectPath()).mkdir('project')
            info = QFileInfo(wizard.projectPath() + '/project/' + wizard.projectFile() + '.qgs')
            self.project.setFileName(info.filePath())

            self.setProjectCode(wizard.projectCode())
            self.setSiteCodes(wizard.siteCodes())
            self.setArkUrl(wizard.arkUrl())

            self.setUserName(wizard.userFullname())
            self.setUserInitials(wizard.userInitials())
            self.setArkUserId(wizard.arkUserId())

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
        lcs = LayerCollectionSettings()
        lcs.collection = grp
        lcs.collectionPath = path
        lcs.parentGroupName = Config.projectGroupName
        lcs.collectionGroupName = config['groupName']
        lcs.bufferGroupName = config['bufferGroupName']
        lcs.log = config['log']
        if config['pointsBaseName']:
            lcs.pointsLayerLabel = config['pointsLabel']
            lcs.pointsLayerName = self._layerName(config['pointsBaseName'])
            lcs.pointsLayerPath = self._shapeFile(path, lcs.pointsLayerName)
            lcs.pointsStylePath = self._styleFile(path, lcs.pointsLayerName, config['pointsBaseName'])
            if config['buffer']:
                lcs.pointsBufferName = lcs.pointsLayerName + Config.bufferSuffix
                lcs.pointsBufferPath = self._shapeFile(bufferPath, lcs.pointsBufferName)
            if config['log']:
                lcs.pointsLogName = lcs.pointsLayerName + Config.logSuffix
                lcs.pointsLogPath = self._shapeFile(logPath, lcs.pointsLogName)
        if config['linesBaseName']:
            lcs.linesLayerLabel = config['linesLabel']
            lcs.linesLayerName = self._layerName(config['linesBaseName'])
            lcs.linesLayerPath = self._shapeFile(path, lcs.linesLayerName)
            lcs.linesStylePath = self._styleFile(path, lcs.linesLayerName, config['linesBaseName'])
            if config['buffer']:
                lcs.linesBufferName = lcs.linesLayerName + Config.bufferSuffix
                lcs.linesBufferPath = self._shapeFile(bufferPath, lcs.linesBufferName)
            if config['log']:
                lcs.linesLogName = lcs.linesLayerName + Config.logSuffix
                lcs.linesLogPath = self._shapeFile(logPath, lcs.linesLogName)
        if config['polygonsBaseName']:
            lcs.polygonsLayerLabel = config['polygonsLabel']
            lcs.polygonsLayerName = self._layerName(config['polygonsBaseName'])
            lcs.polygonsLayerPath = self._shapeFile(path, lcs.polygonsLayerName)
            lcs.polygonsStylePath = self._styleFile(path, lcs.polygonsLayerName, config['polygonsBaseName'])
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

    def _layerName(self, baseName):
        if self.siteCode():
            return self.siteCode() + '_' + baseName
        return 'ARK_' + baseName

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
                or name == self.plan.settings.collectionGroupName
                or name == self.plan.settings.bufferGroupName
                or name == self.section.settings.collectionGroupName
                or name == self.section.settings.bufferGroupName
                or name == self.grid.settings.collectionGroupName
                or name == self.grid.settings.bufferGroupName
                or name == self.site.settings.collectionGroupName
                or name == self.site.settings.bufferGroupName
                or name == self.drawingsGroupName)

    def isArkLayer(self, layerId):
        return (layerId == self.plan.pointsLayerId
                or layerId == self.plan.linesLayerId
                or layerId == self.plan.polygonsLayerId
                or layerId == self.plan.pointsBufferId
                or layerId == self.plan.linesBufferId
                or layerId == self.plan.polygonsBufferId
                or layerId == self.section.pointsLayerId
                or layerId == self.section.linesLayerId
                or layerId == self.section.polygonsLayerId
                or layerId == self.section.pointsBufferId
                or layerId == self.section.linesBufferId
                or layerId == self.section.polygonsBufferId
                or layerId == self.site.pointsLayerId
                or layerId == self.site.linesLayerId
                or layerId == self.site.polygonsLayerId
                or layerId == self.site.pointsBufferId
                or layerId == self.site.linesBufferId
                or layerId == self.site.polygonsBufferId
                or layerId == self.grid.pointsLayerId
                or layerId == self.grid.linesLayerId
                or layerId == self.grid.polygonsLayerId
                or layerId == self.grid.pointsBufferId
                or layerId == self.grid.linesBufferId
                or layerId == self.grid.polygonsBufferId)

    def _shapeFile(self, layerPath, layerName):
        return layerPath + '/' + layerName + '.shp'

    def _styleFile(self, layerPath, layerName, baseName):
        # First see if the layer itself has a default style saved
        filePath = layerPath + '/' + layerName + '.qml'
        if QFile.exists(filePath):
            return filePath
        # Next see if the layer name has a style in the styles folder (which may
        # be a special folder, the site folder or the plugin folder)
        filePath = self.stylePath() + '/' + layerName + '.qml'
        if QFile.exists(filePath):
            return filePath
        # Next see if the default name has a style in the style folder
        filePath = self.stylePath() + '/' + baseName + '.qml'
        if QFile.exists(filePath):
            return filePath
        # Finally, check the plugin folder for the default style
        filePath = self.pluginPath + '/styles/' + baseName + '.qml'
        if QFile.exists(filePath):
            return filePath
        # If we didn't find that then something is wrong!
        return ''

    def _loadCollection(self, collection):
        lcs = LayerCollectionSettings.fromProject(self.pluginName, collection)
        if (lcs.collection == ''):
            lcs = self._configureCollection(collection)
        if lcs.pointsStylePath == '':
            lcs.pointsStylePath = self._stylePath(
                lcs.collection, lcs.collectionPath, lcs.pointsLayerName, 'pointsBaseName')
        if lcs.linesStylePath == '':
            lcs.linesStylePath = self._stylePath(
                lcs.collection, lcs.collectionPath, lcs.linesLayerName, 'linesBaseName')
        if lcs.polygonsStylePath == '':
            lcs.polygonsStylePath = self._stylePath(
                lcs.collection, lcs.collectionPath, lcs.polygonsLayerName, 'polygonsBaseName')
        return LayerCollection(self.iface, self.projectPath(), lcs)

    def _stylePath(self, collection, collectionPath, layerName, baseName):
        return self._styleFile(collectionPath, layerName, Config.collections[collection][baseName])

    def _createCollectionLayers(self, collection, settings):
        path = self.projectPath() + '/' + settings.pointsLayerPath
        if settings.pointsLayerPath and not QFile.exists(self.projectPath() + '/' + settings.pointsLayerPath):
            layers.createShapefile(path,
                                   settings.pointsLayerName,
                                   QGis.WKBPoint,
                                   self.projectCrs(),
                                   self._layerFields(collection, 'pointsFields'))
        path = self.projectPath() + '/' + settings.linesLayerPath
        if (settings.linesLayerPath and not QFile.exists(path)):
            layers.createShapefile(path,
                                   settings.linesLayerName,
                                   QGis.WKBLineString,
                                   self.projectCrs(),
                                   self._layerFields(collection, 'linesFields'))
        path = self.projectPath() + '/' + settings.polygonsLayerPath
        if (settings.polygonsLayerPath and not QFile.exists(path)):
            layers.createShapefile(path,
                                   settings.polygonsLayerName,
                                   QGis.WKBPolygon,
                                   self.projectCrs(),
                                   self._layerFields(collection, 'polygonsFields'))

    def _createCollectionMultiLayers(self, collection, settings):
        path = self.projectPath() + '/' + settings.pointsLayerPath
        if (settings.pointsLayerPath and not QFile.exists(path)):
            layers.createShapefile(path,
                                   settings.pointsLayerName,
                                   QGis.WKBMultiPoint,
                                   self.projectCrs(),
                                   self._layerFields(collection, 'pointsFields'))
        path = self.projectPath() + '/' + settings.linesLayerPath
        if (settings.linesLayerPath and not QFile.exists(path)):
            layers.createShapefile(path,
                                   settings.linesLayerName,
                                   QGis.WKBMultiLineString,
                                   self.projectCrs(),
                                   self._layerFields(collection, 'linesFields'))
        path = self.projectPath() + '/' + settings.polygonsLayerPath
        if (settings.polygonsLayerPath and not QFile.exists(path)):
            layers.createShapefile(path,
                                   settings.polygonsLayerName,
                                   QGis.WKBMultiPolygon,
                                   self.projectCrs(),
                                   self._layerFields(collection, 'polygonsFields'))

    def _layerFields(self, collection, fieldsKey):
        fieldKeys = self._collectionDefault(collection, fieldsKey)
        fields = QgsFields()
        for fieldKey in fieldKeys:
            fields.append(self.field(fieldKey))
        return fields

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

    # Field settings

    def field(self, fieldKey):
        config = Config.fields[fieldKey]
        return QgsField(config['attribute'], config['type'], '', config['len'], config['decimals'], config['label'])

    # Project level settings
    # TODO Move to json file

    def projectDir(self):
        return QDir(self.projectPath())

    def projectPath(self):
        legacy = self.readEntry('projectPath', '')
        if legacy:
            return legacy
        return self.project.fileInfo().absolutePath() + '/..'

    def logUpdates(self):
        return self.readBoolEntry('logUpdates', True)

    def setLogUpdates(self, logUpdates):
        self.writeEntry('logUpdates', logUpdates)

    def arkUrl(self):
        return self.readEntry('arkUrl', '')

    def setArkUrl(self, arkUrl):
        self.writeEntry('arkUrl', arkUrl)

    def projectCode(self):
        return self.readEntry('projectCode', '')

    def setProjectCode(self, projectCode):
        self.writeEntry('projectCode', projectCode)

    def siteCode(self):
        return self.siteCodes()[0]

    def siteCodes(self):
        return self.readListEntry('siteCodes', [self.projectCode()])

    def setSiteCodes(self, siteCodes):
        self.writeEntry('siteCodes', siteCodes)

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

    # User level settings

    def userName(self):
        return self.readEntry('userName', '')

    def setUserName(self, userName):
        self.writeEntry('userName', userName)

    def userInitials(self):
        return self.readEntry('userInitials', '')

    def setUserInitials(self, userInitials):
        self.writeEntry('userInitials', userInitials)

    def arkUserId(self):
        return self.readEntry('arkUserId', '')

    def setArkUserId(self, arkUserId):
        self.writeEntry('arkUserId', arkUserId)

    # Group settings

    def _collectionDefault(self, group, key):
        return Config.collections[group][key]

    def _drawingDefault(self, group, key):
        return Config.drawings[group][key]

    def _drawingEntry(self, group, key, default=None):
        if default is None:
            default = self._drawingDefault(group, key)
        return self.readEntry(group + '/' + key, default)

    def _drawingBoolEntry(self, group, key, default=None):
        if default is None:
            default = self._drawingDefault(group, key)
        return self.readBoolEntry(group + '/' + key, default)

    def _setdrawingEntry(self, group, key, value, default=None):
        if default is None:
            default = self._drawingDefault(group, key)
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
