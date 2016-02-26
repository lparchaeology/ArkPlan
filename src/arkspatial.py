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

from PyQt4 import uic
from PyQt4.QtCore import Qt, QSettings, QFile, QDir, QObject, QDateTime, pyqtSignal
from PyQt4.QtGui import  QIcon, QAction, QDockWidget, QProgressBar, QApplication, QInputDialog, QMenu

from qgis.core import QgsProject, QgsRasterLayer, QgsMapLayerRegistry, QgsSnapper, QgsMessageLog, QgsFields, QgsLayerTreeModel
from qgis.gui import QgsMessageBar, QgsLayerTreeView, QgsLayerTreeViewMenuProvider, QgsLayerTreeViewDefaultActions

from ..libarkqgis.plugin import Plugin
from ..libarkqgis.layercollection import *
from ..libarkqgis import utils, layers
from ..libarkqgis.dock import ToolDockWidget

from ..grid.grid import GridModule

from plan import Plan
from filter import Filter
from identify import MapToolIndentifyItems

from config import Config
from settings_wizard import SettingsWizard
from settings_dialog import SettingsDialog
from select_item_dialog import SelectItemDialog
from data_model import *

import resources

class LayerTreeMenu(QgsLayerTreeViewMenuProvider):

    _iface = None
    _view = None

    def __init__(self, iface, view):
        QgsLayerTreeViewMenuProvider.__init__(self)
        self._iface = iface
        self._view = view

    def createContextMenu(self):
        if not self._view.currentLayer():
            return None
        menu = QMenu()
        action = self._view.defaultActions().actionZoomToLayer(self._iface.mapCanvas(), menu)
        action.triggered.connect(self._view.defaultActions().zoomToLayer(self._iface.mapCanvas()))
        menu.addAction(action)
        return menu


class ArkSpatial(Plugin):
    """QGIS Plugin Implementation."""

    project = None # QgsProject()

    # Tools
    identifyMapTool = None  # MapToolIndentifyItems()

    # Modules
    gridModule = None  # Grid()
    planModule = None  # Plan()
    filterModule = None  # Filter()

    projectGroupIndex = -1
    planGroupIndex = -1

    geoLayer = None  #QgsRasterLayer()
    plan = None  # LayerCollection()
    grid = None  # LayerCollection()
    base = None  # LayerCollection()

    data = None  # DataManager()

    projectLayerView = None  # QgsLayerTreeView()
    layerDock = None  # ToolDockWidget()

    # Private settings
    _initialised = False
    _loaded = False

    def __init__(self, iface, pluginPath):
        super(ArkSpatial, self).__init__(iface, Config.pluginName, ':/plugins/ark/icon.png', pluginPath,
                                         Plugin.PluginsGroup, Plugin.PluginsGroup, checkable=True)
        # Set display / menu name now we have tr() set up
        self.setDisplayName(self.tr(u'&ARK Spatial'))

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
        self.layerDock.setObjectName(u'LayerDock')


    # Initialise plugin gui
    def initialise(self):
        if self._initialised:
            return True

        # Create the Layer Model and View
        #TODO Should only show our subgroup but crashes!
        #self.projectLayerModel = QgsLayerTreeModel(QgsProject.instance().layerTreeRoot().findGroup(Config.projectGroupName), self);
        self.projectLayerModel = QgsLayerTreeModel(QgsProject.instance().layerTreeRoot(), self);
        self.projectLayerModel.setFlag(QgsLayerTreeModel.ShowLegend)
        self.projectLayerModel.setFlag(QgsLayerTreeModel.ShowLegendAsTree)
        self.projectLayerModel.setFlag(QgsLayerTreeModel.AllowNodeReorder, True)
        self.projectLayerModel.setFlag(QgsLayerTreeModel.AllowNodeRename, False)
        self.projectLayerModel.setFlag(QgsLayerTreeModel.AllowNodeChangeVisibility)
        self.projectLayerModel.setFlag(QgsLayerTreeModel.AllowLegendChangeState)
        self.projectLayerModel.setFlag(QgsLayerTreeModel.AllowSymbologyChangeState)
        self.projectLayerModel.setAutoCollapseLegendNodes(-1)
        self.projectLayerView.setModel(self.projectLayerModel)
        menuProvider = LayerTreeMenu(self.iface, self.projectLayerView)
        self.projectLayerView.setMenuProvider(menuProvider)
        self.projectLayerView.setCurrentLayer(self.iface.activeLayer())
        self.projectLayerView.doubleClicked.connect(self.iface.actionOpenTable().trigger)
        self.projectLayerView.currentLayerChanged.connect(self.mapCanvas().setCurrentLayer)
        self.projectLayerView.currentLayerChanged.connect(self.iface.setActiveLayer)
        self.iface.currentLayerChanged.connect(self.projectLayerView.setCurrentLayer)

        # Init the identify tool and add to the toolbar
        self.identifyAction = self.addDockAction(':/plugins/ark/filter/identify.png', self.tr(u'Identify Items'), callback=self.triggerIdentifyAction, checkable=True)
        self.identifyMapTool = MapToolIndentifyItems(self)
        self.identifyMapTool.setAction(self.identifyAction)

        # Init the Load Item tool and add to the toolbar
        self.showItemAction = self.addDockAction(':/plugins/ark/filter/showContext.png', self.tr(u'Show Item'), callback=self._showItem)

        # Init the modules and add to the toolbar
        self.layerDock.toolbar.addSeparator()
        self.gridModule = GridModule(self)
        self.gridModule.initGui()
        self.filterModule = Filter(self)
        self.filterModule.initGui()
        self.planModule = Plan(self)
        self.planModule.initGui()
        self.data = DataManager()

        # Add Settings to the toolbar
        self.layerDock.toolbar.addSeparator()
        self.addDockAction(':/plugins/ark/settings.svg', self.tr(u'Settings'), self._triggerSettingsDialog)

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
        if self.isInitialised() and self.isConfigured():
            self.projectGroupIndex = layers.createLayerGroup(self.iface, Config.projectGroupName)
            #Load the layer collections
            self.grid = self._loadCollection('grid')
            self.plan = self._loadCollection('plan')
            self.base = self._loadCollection('base')
            if self.grid.initialise() and self.plan.initialise() and self.base.initialise():
                self.gridModule.loadProject()
                self.planModule.loadProject()
                self.data.loadProject(self)
                self.filterModule.loadProject()
                self._loaded = True

    # Write the project for saving
    def writeProject(self):
        if  self.isLoaded():
            self.gridModule.writeProject()
            self.planModule.writeProject()
            self.filterModule.writeProject()

    # Close the project
    def closeProject(self):
        if self.identifyMapTool.action().isChecked():
            self.iface.actionPan().trigger()
        if self.isLoaded():
            self.writeProject()
            self.gridModule.closeProject()
            self.planModule.closeProject()
            self.filterModule.closeProject()
            # Unload the layers
            if self.plan is not None:
                self.plan.unload()
                self.plan = None
            if self.grid is not None:
                self.grid.unload()
                self.grid = None
            if self.base is not None:
                self.base.unload()
                self.base = None
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

            self._initialised = False

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
            self.iface.mainWindow().findChild(QDockWidget, "Layers").setVisible(False)
            self.iface.mainWindow().findChild(QDockWidget, "Browser").setVisible(False)
        else:
            if self._initialised:
                self.planModule.dock.setVisible(False)
                self.gridModule.dock.setVisible(False)
                self.filterModule.dock.setVisible(False)
            self.iface.mainWindow().findChild(QDockWidget, "Browser").setVisible(True)
            self.iface.mainWindow().findChild(QDockWidget, "Layers").setVisible(True)

    # Configure the project, i.e. load all settings for QgsProject but don't load anything until needed
    def configure(self):
        if self.isConfigured():
            return True
        # TODO more validation, check if files exist, etc
        wizard = SettingsWizard()
        if wizard.exec_() and wizard.projectPath() and wizard.siteCode() and QDir(wizard.projectPath()).mkpath('.'):
            self.setProjectPath(wizard.projectPath())
            self.setMultiSiteProject(wizard.multiSiteProject())
            self.setSiteCode(wizard.siteCode())
            self.setUseArkDB(wizard.useArkDB())
            self.setArkUrl(wizard.arkUrl())

            self._configureVectorGroup('plan')
            self._configureVectorGroup('grid')
            self._configureVectorGroup('base')

            self._configureRasterGroup('cxt')
            self._configureRasterGroup('pln')
            self._configureRasterGroup('sec')

            self._setIsConfigured(True)

        if not self.isConfigured():
            self.showCriticalMessage('ARK Project not configured, unable to continue!')
            self.layerDock.menuAction().setChecked(False)
            return False
        else:
            return True

    def _configureVectorGroup(self, grp):
        config = Config.vectorGroups[grp]
        path = config['pathSuffix']
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

    def _configureRasterGroup(self, grp):
        self.rawDrawingDir(grp).mkpath('.')
        self.georefDrawingDir(grp).mkpath('.')

    def _triggerSettingsDialog(self):
        if self.isConfigured():
            self.showSettingsDialog()
        else:
            self.configure()

    def _groupIndexChanged(self, oldIndex, newIndex):
        if (oldIndex == self.projectGroupIndex):
            self.projectGroupIndex = newIndex

    def _layerName(self, baseName):
        if self.multiSiteProject():
            return 'ARK_' + baseName
        return self.siteCode() + '_' + baseName

    def loadGeoLayer(self, geoFile, zoomToLayer=True):
        #TODO Check if already loaded, remove old one?
        self.geoLayer = QgsRasterLayer(geoFile.absoluteFilePath(), geoFile.completeBaseName())
        self.geoLayer.renderer().setOpacity(self.drawingTransparency()/100.0)
        QgsMapLayerRegistry.instance().addMapLayer(self.geoLayer)
        if (self.planGroupIndex < 0):
            self.planGroupIndex = layers.createLayerGroup(self.iface, Config.rasterGroups['cxt']['layersGroupName'], Config.projectGroupName)
        self.legendInterface().moveLayer(self.geoLayer, self.planGroupIndex)
        if zoomToLayer:
            self.mapCanvas().setExtent(self.geoLayer.extent())

    def _shapeFile(self, layerPath, layerName):
        return layerPath + '/' + layerName + '.shp'

    def _styleFile(self, layerPath, layerName, baseName):
        # First see if the layer itself has a default style saved
        filePath = layerPath + '/' + layerName + '.qml'
        if QFile.exists(filePath):
            return filePath
        # Next see if the layer name has a style in the styles folder (which may be a special folder, the site folder or the plugin folder)
        filePath = self.stylePath() + '/' + layerName + '.qml'
        if QFile.exists(filePath):
            return filePath
        # Next see if the default name has a style in the style folder
        filePath = self.stylePath() + '/' + baseName + '.qml'
        if QFile.exists(filePath):
            return filePath
        # Finally, check the plugin folder for the default style
        filePath = self.pluginPath() + '/styles/' + baseName + '.qml'
        if QFile.exists(filePath):
            return filePath
        # If we didn't find that then something is wrong!
        return ''

    def _loadCollection(self, collection):
        lcs = LayerCollectionSettings.fromProject(self.pluginName, collection)
        return LayerCollection(self.iface, self.projectPath(), lcs)

    def _createCollectionLayers(self, collection, settings):
        if (settings.pointsLayerPath and not QFile.exists(self.projectPath() + '/' + settings.pointsLayerPath)):
            layers.createShapefile(self.projectPath() + '/' + settings.pointsLayerPath,   settings.pointsLayerName,   QGis.WKBPoint,
                                   self.projectCrs(), self._layerFields(collection, 'pointsFields'))
        if (settings.linesLayerPath and not QFile.exists(self.projectPath() + '/' + settings.linesLayerPath)):
            layers.createShapefile(self.projectPath() + '/' + settings.linesLayerPath,    settings.linesLayerName,    QGis.WKBLineString,
                                   self.projectCrs(), self._layerFields(collection, 'linesFields'))
        if (settings.polygonsLayerPath and not QFile.exists(self.projectPath() + '/' + settings.polygonsLayerPath)):
            layers.createShapefile(self.projectPath() + '/' + settings.polygonsLayerPath, settings.polygonsLayerName, QGis.WKBPolygon,
                                   self.projectCrs(), self._layerFields(collection, 'polygonsFields'))

    def _createCollectionMultiLayers(self, collection, settings):
        if (settings.pointsLayerPath and not QFile.exists(self.projectPath() + '/' + settings.pointsLayerPath)):
            layers.createShapefile(self.projectPath() + '/' + settings.pointsLayerPath,   settings.pointsLayerName,   QGis.WKBMultiPoint,
                                   self.projectCrs(), self._layerFields(collection, 'pointsFields'))
        if (settings.linesLayerPath and not QFile.exists(self.projectPath() + '/' + settings.linesLayerPath)):
            layers.createShapefile(self.projectPath() + '/' + settings.linesLayerPath,    settings.linesLayerName,    QGis.WKBMultiLineString,
                                   self.projectCrs(), self._layerFields(collection, 'linesFields'))
        if (settings.polygonsLayerPath and not QFile.exists(self.projectPath() + '/' + settings.polygonsLayerPath)):
            layers.createShapefile(self.projectPath() + '/' + settings.polygonsLayerPath, settings.polygonsLayerName, QGis.WKBMultiPolygon,
                                   self.projectCrs(), self._layerFields(collection, 'polygonsFields'))

    def _layerFields(self, collection, fieldsKey):
        fieldKeys = self._vectorGroupDefault(collection, fieldsKey)
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
        #self.actions.append(action)
        return action

    # Field settings

    def field(self, fieldKey):
        if self.useArkDB():
            return Config.arkFieldDefaults[fieldKey]
        else:
            return Config.fieldDefaults[fieldKey]

    def fieldName(self, fieldKey):
        try:
            if self.useArkDB():
                return Config.arkFieldDefaults[fieldKey].name()
            else:
                return Config.fieldDefaults[fieldKey].name()
        except:
            return ''

    # Project settings

    def logUpdates(self):
        return self.readBoolEntry('logUpdates', True)

    def setLogUpdates(self, logUpdates):
        self.writeEntry('logUpdates', logUpdates)

    def useArkDB(self):
        return self.readBoolEntry('useArkDB', True)

    def setUseArkDB(self, useArkDB):
        self.writeEntry('useArkDB', useArkDB)

    def arkUrl(self):
        return self.readEntry('arkUrl', '')

    def setArkUrl(self, arkUrl):
        self.writeEntry('arkUrl', arkUrl)

    def projectDir(self):
        return QDir(self.projectPath())

    def projectPath(self):
        return self.readEntry('projectPath', '')

    def setProjectPath(self, absolutePath):
        self.writeEntry('projectPath', absolutePath)

    def multiSiteProject(self):
        return self.readBoolEntry('multiSiteProject', False)

    def setMultiSiteProject(self, multiSite):
        self.writeEntry('multiSiteProject', multiSite)

    def siteCode(self):
        return self.readEntry('siteCode', '')

    def siteCodes(self):
        # TODO Make a stored list, updated via settings
        vals = set()
        vals.add(self.siteCode())
        vals.update(self.plan.uniqueValues(self.fieldName('site')))
        return sorted(vals)

    def setSiteCode(self, siteCode):
        self.writeEntry('siteCode', siteCode)

    def useCustomStyles(self):
        return self.readBoolEntry('useCustomStyles', False)

    def styleDir(self):
        return QDir(self.stylePath())

    def stylePath(self):
        path =  self.readEntry('stylePath', '')
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

    def _vectorGroupDefault(self, group, key):
        return Config.vectorGroups[group][key]

    def _rasterGroupDefault(self, group, key):
        return Config.rasterGroups[group][key]

    def _rasterGroupEntry(self, group, key, default=None):
        if default is None:
            default = self._rasterGroupDefault(group, key)
        return self.readEntry(group + '/' + key, default)

    def _rasterGroupBoolEntry(self, group, key, default=None):
        if default is None:
            default = self._rasterGroupDefault(group, key)
        return self.readBoolEntry(group + '/' + key, default)

    def _setRasterGroupEntry(self, group, key, value, default=None):
        if default is None:
            default = self._rasterGroupDefault(group, key)
        self.setEntry(group + '/' + key, value, default)

    def collection(self, collection):
        if collection == 'plan':
            return self.plan
        elif collection == 'grid':
            return self.grid
        elif collection == 'base':
            return self.base

    # Raster Drawings settings

    def rasterGroupDir(self, group):
        return QDir(self.rasterGroupPath(group))

    def rasterGroupPath(self, group):
        if self.useCustomPath(group):
            return self._rasterGroupEntry(group, path)
        else:
            return self.projectPath() + '/' + Config.rasterGroups[group]['pathSuffix']

    def setRasterGroupPath(self, group, useCustomPath, absolutePath):
        self._setRasterGroupEntry(group, 'useCustomPath', useCustomPath, False)
        if useCustomPath:
            self._setRasterGroupEntry(group, 'pathSuffix', absolutePath)
        else:
            self._setRasterGroupEntry(group, 'pathSuffix', '')

    def useCustomPath(self, group):
        return self._rasterGroupBoolEntry(group, 'useCustomPath', False)

    def rawDrawingDir(self, group):
        return QDir(self.rawDrawingPath(group))

    def rawDrawingPath(self, group):
        return self.rasterGroupPath(group)

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
        classCodes = sorted(set(self.plan.uniqueValues(self.fieldName('class'))))
        dialog = SelectItemDialog(self.siteCodes(), self.siteCode(), classCodes, self.iface.mainWindow())
        if dialog.exec_():
            item = dialog.item()
            self.showMessage('Loading ' + item.itemLabel())
            self.filterModule.filterItem(item)
            self.filterModule.showDock()
            if dialog.loadDrawings():
                self.planModule.loadSourceDrawings(item)
            if dialog.zoomToItem():
                self.filterModule.zoomFilter()
