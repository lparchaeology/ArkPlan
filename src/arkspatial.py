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
from PyQt4.QtGui import  QIcon, QAction, QDockWidget, QProgressBar, QApplication, QInputDialog

from qgis.core import QgsProject, QgsRasterLayer, QgsMapLayerRegistry, QgsSnapper, QgsMessageLog, QgsFields, QgsLayerTreeModel
from qgis.gui import QgsMessageBar, QgsLayerTreeView

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

import resources_rc

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
        self.layerDock.setWindowTitle(u'ARK Spatial Layers')
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
        self.projectLayerView.setCurrentLayer(self.iface.activeLayer())
        self.projectLayerView.doubleClicked.connect(self.iface.actionOpenTable().trigger)
        self.projectLayerView.currentLayerChanged.connect(self.mapCanvas().setCurrentLayer)
        self.projectLayerView.currentLayerChanged.connect(self.iface.setActiveLayer)
        self.iface.currentLayerChanged.connect(self.projectLayerView.setCurrentLayer)

        self.addDockAction(':/plugins/ark/settings.svg', self.tr(u'Settings'), self._triggerSettingsDialog)

        # Init the identify tool
        self.layerDock.toolbar.addSeparator()
        self.identifyAction = self.addDockAction(':/plugins/ark/filter/identify.png', self.tr(u'Identify contexts'), callback=self.triggerIdentifyAction, checkable=True)
        self.identifyMapTool = MapToolIndentifyItems(self)
        self.identifyMapTool.setAction(self.identifyAction)

        # Init the Load Context tool
        self.showItemAction = self.addDockAction(':/plugins/ark/filter/showContext.png', self.tr(u'Show Item'), callback=self._showItem)

        # Init the modules
        self.layerDock.toolbar.addSeparator()
        self.gridModule = GridModule(self)
        self.gridModule.initGui()
        self.filterModule = Filter(self)
        self.filterModule.initGui()
        self.layerDock.toolbar.addSeparator()
        self.planModule = Plan(self)
        self.planModule.initGui()
        self.data = DataManager()

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
            self.grid = self._createCollection('grid')
            self._createCollectionLayers('grid', self.grid.settings)
            self.plan = self._createCollection('plan')
            self._createCollectionMultiLayers('plan', self.plan.settings)
            self.base = self._createCollection('base')
            self._createCollectionLayers('base', self.base.settings)
            if self.grid.initialise() and self.plan.initialise() and self.base.initialise():
                self.gridModule.loadProject()
                self.planModule.loadProject()
                self.data.loadProject(self)
                self.data.loadItems(self, 'sec')
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

            self.identifyMapTool.deactivate()

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
        if wizard.exec_() and (not wizard.advancedMode() or self.showSettingsDialog()):
            if not wizard.advancedMode():
                self.setProjectPath(wizard.projectPath())
                self.setMultiSiteProject(wizard.multiSiteProject())
                self.setSiteCode(wizard.siteCode())
                self.setUseArkDB(wizard.useArkDB())
                self.setArkUrl(wizard.arkUrl())
            if (self.siteCode()
                and self.projectDir().mkpath('.')
                and self.siteCode()
                and self.groupDir('cxt').mkpath('.')
                and self.rawDrawingDir('cxt').mkpath('.')
                and self.georefDrawingDir('cxt').mkpath('.')
                and self.groupDir('pln').mkpath('.')
                and self.rawDrawingDir('pln').mkpath('.')
                and self.georefDrawingDir('pln').mkpath('.')
                and self.groupDir('grid').mkpath('.')
                and self.groupDir('plan').mkpath('.')
                and self.groupDir('base').mkpath('.')):
                self._setIsConfigured(True)
        if not self.isConfigured():
            self.showCriticalMessage('ARK Project not configured, unable to continue!')
            self.layerDock.menuAction().setChecked(False)
            return False
        else:
            return True

    def _triggerSettingsDialog(self):
        if self.isConfigured():
            self.showSettingsDialog()
        else:
            self.configure()

    def _groupIndexChanged(self, oldIndex, newIndex):
        if (oldIndex == self.projectGroupIndex):
            self.projectGroupIndex = newIndex

    def _layerName(self, baseName):
        if (baseName and not self.multiSiteProject() and self.siteCode()):
            return self.siteCode() + '_' + baseName
        return 'ark_' + baseName

    def loadGeoLayer(self, geoFile, zoomToLayer=True):
        #TODO Check if already loaded, remove old one?
        self.geoLayer = QgsRasterLayer(geoFile.absoluteFilePath(), geoFile.completeBaseName())
        self.geoLayer.renderer().setOpacity(self.drawingTransparency()/100.0)
        QgsMapLayerRegistry.instance().addMapLayer(self.geoLayer)
        if (self.planGroupIndex < 0):
            self.planGroupIndex = layers.createLayerGroup(self.iface, self.layersGroupName('cxt'), Config.projectGroupName)
        self.legendInterface().moveLayer(self.geoLayer, self.planGroupIndex)
        if zoomToLayer:
            self.mapCanvas().setExtent(self.geoLayer.extent())

    def _shapeFile(self, layerPath, layerName):
        return layerPath + '/' + layerName + '.shp'

    def _styleFile(self, layerPath, layerName, baseName, defaultName):
        # First see if the layer itself has a default style saved
        filePath = layerPath + '/' + layerName + '.qml'
        if QFile.exists(filePath):
            return filePath
        # Next see if the base name has a style in the styles folder (which may be a special folder, the site folder or the plugin folder)
        filePath = self.stylePath() + '/' + baseName + '.qml'
        if QFile.exists(filePath):
            return filePath
        # Next see if the default name has a style in the style folder
        filePath = self.stylePath() + '/' + defaultName + '.qml'
        if QFile.exists(filePath):
            return filePath
        # Finally, check the plugin folder for the default style
        filePath = self.stylePath() + '/' + defaultName + '.qml'
        if QFile.exists(filePath):
            return filePath
        # If we didn't find that then something is wrong!
        return ''

    def _createCollection(self, collection):
        path = self.groupPath(collection)
        lcs = LayerCollectionSettings()
        lcs.collectionGroupName = self.layersGroupName(collection)
        lcs.parentGroupName = Config.projectGroupName
        lcs.buffersGroupName = self.buffersGroupName(collection)
        lcs.bufferSuffix = self._groupDefault(collection, 'bufferSuffix')
        layerName = self.pointsLayerName(collection)
        if layerName:
            lcs.pointsLayerProvider = 'ogr'
            lcs.pointsLayerLabel = self._groupDefault(collection, 'pointsLabel')
            lcs.pointsLayerName = layerName
            lcs.pointsLayerPath = self._shapeFile(path, layerName)
            lcs.pointsStylePath = self._styleFile(path, layerName, self.pointsBaseName(collection), self.pointsBaseNameDefault(collection))
        layerName = self.linesLayerName(collection)
        if layerName:
            lcs.linesLayerProvider = 'ogr'
            lcs.linesLayerLabel = self._groupDefault(collection, 'linesLabel')
            lcs.linesLayerName = layerName
            lcs.linesLayerPath = self._shapeFile(path, layerName)
            lcs.linesStylePath = self._styleFile(path, layerName, self.linesBaseName(collection), self.linesBaseNameDefault(collection))
        layerName = self.polygonsLayerName(collection)
        if layerName:
            lcs.polygonsLayerProvider = 'ogr'
            lcs.poolygonsLayerLabel = self._groupDefault(collection, 'polygonsLabel')
            lcs.polygonsLayerName = layerName
            lcs.polygonsLayerPath = self._shapeFile(path, layerName)
            lcs.polygonsStylePath = self._styleFile(path, layerName, self.polygonsBaseName(collection), self.polygonsBaseNameDefault(collection))
        return LayerCollection(self.iface, lcs)

    def _createCollectionLayers(self, collection, settings):
        if (settings.pointsLayerPath and not QFile.exists(settings.pointsLayerPath)):
            layers.createShapefile(settings.pointsLayerPath,   QGis.WKBPoint,        self.projectCrs(), self._layerFields(collection, 'pointsFields'))
        if (settings.linesLayerPath and not QFile.exists(settings.linesLayerPath)):
            layers.createShapefile(settings.linesLayerPath,    QGis.WKBLineString,   self.projectCrs(), self._layerFields(collection, 'linesFields'))
        if (settings.polygonsLayerPath and not QFile.exists(settings.polygonsLayerPath)):
            layers.createShapefile(settings.polygonsLayerPath, QGis.WKBPolygon,      self.projectCrs(), self._layerFields(collection, 'polygonsFields'))

    def _createCollectionMultiLayers(self, collection, settings):
        if (settings.pointsLayerPath and not QFile.exists(settings.pointsLayerPath)):
            layers.createShapefile(settings.pointsLayerPath,   QGis.WKBMultiPoint,        self.projectCrs(), self._layerFields(collection, 'pointsFields'))
        if (settings.linesLayerPath and not QFile.exists(settings.linesLayerPath)):
            layers.createShapefile(settings.linesLayerPath,    QGis.WKBMultiLineString,   self.projectCrs(), self._layerFields(collection, 'linesFields'))
        if (settings.polygonsLayerPath and not QFile.exists(settings.polygonsLayerPath)):
            layers.createShapefile(settings.polygonsLayerPath, QGis.WKBMultiPolygon,      self.projectCrs(), self._layerFields(collection, 'polygonsFields'))

    def _layerFields(self, collection, fieldsKey):
        fieldKeys = self._groupDefault(collection, fieldsKey)
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
        return sorted(set(self.plan.uniqueValues(self.fieldName('site'))))

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

    def _groupDefault(self, group, key):
        return Config.groupDefaults[group][key]

    def _groupEntry(self, group, key, default=None):
        if default is None:
            default = self._groupDefault(group, key)
        return self.readEntry(group + '/' + key, default)

    def _groupBoolEntry(self, group, key, default=None):
        if default is None:
            default = self._groupDefault(group, key)
        return self.readBoolEntry(group + '/' + key, default)

    def _setGroupEntry(self, group, key, value, default=None):
        if default is None:
            default = self._groupDefault(group, key)
        self.setEntry(group + '/' + key, value, default)

    def groupDir(self, group):
        return QDir(self.groupPath(group))

    def groupPath(self, group):
        path =  self._groupEntry(group, 'path')
        if (not path):
            return self.groupPathDefault(group)
        return path

    def groupPathDefault(self, group):
        path = self._groupDefault(group, 'path')
        if not path:
            path = self.projectPath()
            suffix = self._groupDefault(group, 'pathSuffix')
            if path and suffix:
                path = path + '/' + suffix
        return path

    def setGroupPath(self, group, useCustomFolder, absolutePath):
        self._setGroupEntry(group, 'useCustomFolder', useCustomFolder, False)
        if useCustomFolder:
            self._setGroupEntry(group, 'path', absolutePath)
        else:
            self._setGroupEntry(group, 'path', '')

    def useCustomPath(self, group):
        return self._groupBoolEntry(group, 'useCustomPath', False)

    def layersGroupName(self, group):
        return self._groupEntry(group, 'layersGroupName')

    def setLayersGroupName(self, group, layersGroupName):
        self._setGroupEntry(group, 'layersGroupName', layersGroupName)

    # Vector Collection settings

    def buffersGroupName(self, collection):
        return self._groupEntry(collection, 'buffersGroupName')

    def setBuffersGroupName(self, collection, buffersGroupName):
        self._setGroupEntry(collection, 'buffersGroupName', buffersGroupName)

    def pointsBaseNameDefault(self, collection):
        return self._groupDefault(collection, 'pointsBaseName')

    def pointsBaseName(self, collection):
        return self._groupEntry(collection, 'pointsBaseName')

    def setPointsBaseName(self, collection, pointsBaseName):
        self._setGroupEntry(collection, 'pointsBaseName', pointsBaseName)

    def pointsLayerName(self, collection):
        return self._layerName(self.pointsBaseName(collection))

    def linesBaseNameDefault(self, collection):
        return self._groupDefault(collection, 'linesBaseName')

    def linesBaseName(self, collection):
        return self._groupEntry(collection, 'linesBaseName')

    def setLinesBaseName(self, collection, linesBaseName):
        self._setGroupEntry(collection, 'linesBaseName', linesBaseName)

    def linesLayerName(self, collection):
        return self._layerName(self.linesBaseName(collection))

    def polygonsBaseNameDefault(self, collection):
        return self._groupDefault(collection, 'polygonsBaseName')

    def polygonsBaseName(self, collection):
        return self._groupEntry(collection, 'polygonsBaseName')

    def setPolygonsBaseName(self, collection, polygonsBaseName):
        self._setGroupEntry(collection, 'polygonsBaseName', polygonsBaseName)

    def polygonsLayerName(self, collection):
        return self._layerName(self.polygonsBaseName(collection))

    def collection(self, collection):
        if collection == 'plan':
            return self.plan
        elif collection == 'grid':
            return self.grid
        elif collection == 'base':
            return self.base

    # Raster Drawings settings

    def rawDrawingDir(self, group):
        return QDir(self.rawDrawingPath(group))

    def rawDrawingPath(self, group):
        return self.groupPath(group)

    def georefDrawingDir(self, group):
        return QDir(self.georefDrawingPath(group))

    def georefDrawingPath(self, group):
        if self.useGeorefFolder():
            return QDir(self.groupPath(group) + '/georef').absolutePath()
        return self.groupPath(group)

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
