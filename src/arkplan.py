# -*- coding: utf-8 -*-
"""
/***************************************************************************
 Ark
                                 A QGIS plugin
 Plugin to assist in digitising of Archaeological plans.
                              -------------------
        begin                : 2014-12-07
        git sha              : $Format:%H$
        copyright            : (C) 2014 by John Layt
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
from PyQt4.QtGui import  QIcon, QAction, QDockWidget, QProgressBar, QApplication

from qgis.core import QgsProject, QgsSnapper, QgsMessageLog, QgsFields, QgsLayerTreeModel
from qgis.gui import QgsMessageBar

from ..libarkqgis.plugin import Plugin
from ..libarkqgis.layercollection import *
from ..libarkqgis import utils, layers

from ..grid.grid import GridModule

from plan import Plan
from filter import Filter

from config import Config
from arkplan_dock import ArkPlanDock
from settings_wizard import SettingsWizard
from settings_dialog import SettingsDialog

import resources_rc

class ArkPlan(Plugin):
    """QGIS Plugin Implementation."""

    # Signal when the project changes so modules can reload
    projectChanged = pyqtSignal()

    project = None # QgsProject()

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

    # Private settings
    _initialised = False

    def __init__(self, iface, pluginPath):
        super(ArkPlan, self).__init__(iface, u'ArkPlan', ':/plugins/ArkPlan/icon.png',
                                       pluginPath, Plugin.PluginsMenu)
        # Set display / menu name now we have tr() set up
        self.setDisplayName(self.tr(u'&ArkPlan'))

        # If the legend indexes change make sure we stay updated
        self.legendInterface().groupIndexChanged.connect(self._groupIndexChanged)

        self.gridModule = GridModule(self)
        self.planModule = Plan(self)
        self.filterModule = Filter(self)

    # Load the plugin
    def initGui(self):
        super(ArkPlan, self).initGui()

        # Load the Plugin
        self._showLayersDock = self.iface.mainWindow().findChild(QDockWidget, "Layers").isVisible()
        self._showBrowserDock = self.iface.mainWindow().findChild(QDockWidget, "Browser").isVisible()
        self.dock = ArkPlanDock()
        action = self.addAction(self.pluginIconPath, self.tr(u'Ark Plan'), checkable=True)
        self.addDockAction(':/plugins/ArkPlan/settings.svg', self.tr(u'Ark Settings'), self._triggerSettingsDialog)
        self.dock.load(self.iface, Qt.LeftDockWidgetArea, action)
        self.dock.toggled.connect(self.run)

        # Load the Modules
        self.dock.addSeparator()
        self.gridModule.load()
        self.filterModule.load()
        self.dock.addSeparator()
        self.planModule.load()

    # Unload the plugin
    def unload(self):

        # Restore the original QGIS gui
        self.dock.menuAction().setChecked(False)

        # Unload the modules in dependence order
        self.planModule.unload()
        self.filterModule.unload()
        self.gridModule.unload()

        # Unload the layers
        if self.plan is not None:
            self.plan.unload()
        if self.grid is not None:
            self.grid.unload()
        if self.base is not None:
            self.base.unload()

        # Unload this dock and uninitialise
        self.dock.unload()
        self._initialised = False

        # Removes the plugin menu item and icon from QGIS GUI.
        super(ArkPlan, self).unload()

    def run(self, checked):
        if checked:
            self._showLayersDock = self.iface.mainWindow().findChild(QDockWidget, "Layers").isVisible()
            self._showBrowserDock = self.iface.mainWindow().findChild(QDockWidget, "Browser").isVisible()
            self.iface.mainWindow().findChild(QDockWidget, "Layers").setVisible(False)
            self.iface.mainWindow().findChild(QDockWidget, "Browser").setVisible(False)
            self.initialise()
        else:
            self.iface.mainWindow().findChild(QDockWidget, "Layers").setVisible(self._showLayersDock)
            self.iface.mainWindow().findChild(QDockWidget, "Browser").setVisible(self._showBrowserDock)
            self.planModule.dock.menuAction().setChecked(False)
            self.planModule.editDock.menuAction().setChecked(False)
            self.planModule.schematicDock.menuAction().setChecked(False)
            self.gridModule.dock.menuAction().setChecked(False)
            self.filterModule.dock.menuAction().setChecked(False)

    # Configure the project, i.e. load all settings for QgsProject but don't load anything until needed
    def configure(self):
        if self.isConfigured():
            return
        # TODO more validation, check if files exist, etc
        wizard = SettingsWizard()
        if wizard.exec_() and (not wizard.advancedMode() or self.showSettingsDialog()):
            if not wizard.advancedMode():
                self.setProjectPath(wizard.projectPath())
                self.setMultiSiteProject(wizard.multiSiteProject())
                self.setSiteCode(wizard.siteCode())
                self.setUseArkDB(wizard.useArkDB())
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
            self.dock.menuAction().setChecked(False)

    def isConfigured(self):
        return self.readBoolEntry('configured', False)

    def _setIsConfigured(self, configured):
        self.writeEntry('configured', configured)
        if not configured:
            self._initialised = False

    # Initialise project the first time it is needed, i.e. load the configuration
    def initialise(self):
        if self._initialised:
            return True

        self.configure()
        if self.isConfigured():
            #Show a loading indicator
            progressMessageBar = self.iface.messageBar().createMessage("Loading ArkPlan, please wait...")
            progress = QProgressBar()
            progress.setMinimum(0)
            progress.setMaximum(0)
            progress.setAlignment(Qt.AlignLeft|Qt.AlignVCenter)
            progressMessageBar.layout().addWidget(progress)
            self.iface.messageBar().pushWidget(progressMessageBar, self.iface.messageBar().INFO)
            QApplication.setOverrideCursor(Qt.WaitCursor)

            # Create the Layer Model and View
            self.projectGroupIndex = layers.createLayerGroup(self.iface, Config.projectGroupName)
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
            self.dock.projectLayerView.setModel(self.projectLayerModel)
            self.dock.projectLayerView.doubleClicked.connect(self.iface.actionOpenTable().trigger)
            self.dock.projectLayerView.currentLayerChanged.connect(self.mapCanvas().setCurrentLayer)
            self.dock.projectLayerView.currentLayerChanged.connect(self.iface.setActiveLayer)
            self.dock.projectLayerView.setCurrentLayer(self.iface.activeLayer())
            self.iface.currentLayerChanged.connect(self.dock.projectLayerView.setCurrentLayer)

            #Load the layer collections
            self.grid = self._createCollection('grid')
            self._createCollectionLayers('grid', self.grid._settings)
            self.plan = self._createCollection('plan')
            self._createCollectionMultiLayers('plan', self.plan._settings)
            self.base = self._createCollection('base')
            self._createCollectionLayers('base', self.base._settings)
            self.iface.projectRead.connect(self.projectLoad)
            self.iface.newProjectCreated.connect(self.projectLoad)
            if self.grid.initialise() and self.plan.initialise() and self.base.initialise():
                self._initialised = True

            #Remove the loading indicator
            self.iface.messageBar().clearWidgets()
            QApplication.restoreOverrideCursor()

        return self._initialised

    def isInitialised(self):
        return self._initialised

    def projectLoad(self):
        self.projectChanged.emit()

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

    def loadGeoLayer(self, geoFile):
        #TODO Check if already loaded, remove old one?
        self.geoLayer = QgsRasterLayer(geoFile.absoluteFilePath(), geoFile.completeBaseName())
        self.geoLayer.renderer().setOpacity(self.drawingTransparency()/100.0)
        QgsMapLayerRegistry.instance().addMapLayer(self.geoLayer)
        if (self.planGroupIndex < 0):
            self.planGroupIndex = layers.createLayerGroup(self.iface, self.layersGroupName('cxt'), Config.projectGroupName)
        self.legendInterface().moveLayer(self.geoLayer, self.planGroupIndex)
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
        icon = QIcon(iconPath)
        parent = self.dock
        action = QAction(icon, text, parent)
        if callback is not None:
            action.triggered.connect(callback)
        action.setEnabled(enabled)
        action.setCheckable(checkable)
        if tip is not None:
            action.setStatusTip(tip)
        if whatsThis is not None:
            action.setWhatsThis(whatsThis)
        self.dock.addAction(action)
        #self.actions.append(action)
        return action

    # Field settings

    def field(self, fieldKey):
        if self.useArkDB():
            return Config.arkFieldDefaults[fieldKey]
        else:
            return Config.fieldDefaults[fieldKey]

    def fieldName(self, fieldKey):
        if self.useArkDB():
            return Config.arkFieldDefaults[fieldKey].name()
        else:
            return Config.fieldDefaults[fieldKey].name()

    # Project settings

    def useArkDB(self):
        return self.readBoolEntry('useArkDB', True)

    def setUseArkDB(self, useArkDB):
        self.writeEntry('useArkDB', useArkDB)

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
