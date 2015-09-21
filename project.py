# -*- coding: utf-8 -*-
"""
/***************************************************************************
                                      Ark
                                 A QGIS plugin
             QGIS Plugin for ARK, the Archaeological Recording Kit
                              -------------------
        begin                : 2015-03-02
        git sha              : $Format:%H$
        copyright            : (C) 2015 by L - P: Heritage LLP
        copyright            : (C) 2015 by John Layt
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
from PyQt4.QtCore import Qt, QSettings, QFile, QDir, QObject, QVariant, QDateTime, pyqtSignal
from PyQt4.QtGui import  QIcon, QAction, QDockWidget

from qgis.core import QgsProject, QgsSnapper, QgsMessageLog, QgsField, QgsFields, QgsLayerTreeModel
from qgis.gui import QgsMessageBar

from libarkqgis import utils, layers, layercollection
from libarkqgis.layercollection import *

from project_dock import ProjectDock
from settings_dialog import SettingsDialog


class Project(QObject):

    # Signal when the project changes so modules can reload
    projectChanged = pyqtSignal()

    project = None # QgsProject()
    plugin = None # Plugin()

    projectGroupName = 'Ark'
    projectGroupIndex = -1
    planGroupName = 'Context Plans'
    planGroupIndex = -1

    geoLayer = None  #QgsRasterLayer()
    plan = None  # LayerCollection()
    grid = None  # LayerCollection()
    base = None  # LayerCollection()

    # Field deafults to use if *not* using ARK DB, so as not to confuse normal users
    fieldDefaults = {
        'site'      : QgsField('site',       QVariant.String, '',  10, 0, 'Site Code'),
        'class'     : QgsField('class',      QVariant.String, '',  10, 0, 'Class'),
        'id'        : QgsField('id',         QVariant.Int,    '',   5, 0, 'ID'),
        'name'      : QgsField('name',       QVariant.String, '',  10, 0, 'Name'),
        'category'  : QgsField('category',   QVariant.String, '',  10, 0, 'Category'),
        'elevation' : QgsField('elevation',  QVariant.Double, '',  10, 3, 'Elevation'),
        'source_cd' : QgsField('source_cd',  QVariant.String, '',  10, 0, 'Source Code'),
        'source_id' : QgsField('source_id',  QVariant.Int,    '',   5, 0, 'Source ID'),
        'file'      : QgsField('file',       QVariant.String, '', 100, 0, 'Source File'),
        'local_x'   : QgsField('local_x',    QVariant.Double, '',  10, 3, 'Local Grid X'),
        'local_y'   : QgsField('local_y',    QVariant.Double, '',  10, 3, 'Local Grid Y'),
        'map_x'     : QgsField('map_x',      QVariant.Double, '',  10, 3, 'Map X'),
        'map_y'     : QgsField('map_y',      QVariant.Double, '',  10, 3, 'Map Y'),
        'comment'   : QgsField('comment',    QVariant.String, '', 100, 0, 'Comment'),
        'created_on': QgsField('created_on', QVariant.String, '',  20, 0, 'Created On'),  # '2012-01-01T23:59:59.999Z' in UTC
        'created_by': QgsField('created_by', QVariant.String, '',  20, 0, 'Created By')
    }

    # Field defaults to use if using ARK DB, matches field names in ARK
    arkFieldDefaults = {
        'site'      : QgsField('ste_cd',     QVariant.String, '',  10, 0, 'Site Code'),
        'class'     : QgsField('module',     QVariant.String, '',  10, 0, 'ARK Module'),
        'id'        : QgsField('item_no',    QVariant.Int,    '',   5, 0, 'ARK Item Number'),
        'name'      : QgsField('name',       QVariant.String, '',  10, 0, 'Name'),
        'category'  : QgsField('category',   QVariant.String, '',  10, 0, 'Category'),
        'elevation' : QgsField('elevation',  QVariant.Double, '',  10, 3, 'Elevation'),
        'source_cd' : QgsField('source_cd',  QVariant.String, '',  10, 0, 'Source Code'),
        'source_id' : QgsField('source_no',  QVariant.Int,    '',   5, 0, 'Source Item Number'),
        'file'      : QgsField('file',       QVariant.String, '', 100, 0, 'File'),
        'local_x'   : QgsField('local_x',    QVariant.Double, '',  10, 3, 'Local Grid X'),
        'local_y'   : QgsField('local_y',    QVariant.Double, '',  10, 3, 'Local Grid Y'),
        'map_x'     : QgsField('map_x',      QVariant.Double, '',  10, 3, 'Map X'),
        'map_y'     : QgsField('map_y',      QVariant.Double, '',  10, 3, 'Map Y'),
        'comment'   : QgsField('comment',    QVariant.String, '', 100, 0, 'Comment'),
        'created_on': QgsField('cre_on',     QVariant.String, '',  20, 0, 'Created On'),  # '2012-01-01T23:59:59.999Z' in UTC
        'created_by': QgsField('cre_by',     QVariant.String, '',  20, 0, 'Created By')
    }

    moduleDefaults = {
        'plan' : {
            'path'             : '',
            'pathSuffix'       : 'vectors/plan',
            'layersGroupName'  : 'Plan Data',
            'buffersGroupName' : 'Edit Data',
            'bufferSuffix'     : '_mem',
            'pointsLabel'      : 'Plan Points',
            'linesLabel'       : 'Plan Lines',
            'polygonsLabel'    : 'Plan Polygons',
            'pointsBaseName'   : 'plan_pt',
            'linesBaseName'    : 'plan_pl',
            'polygonsBaseName' : 'plan_pg',
            'pointsFields'     : ['site', 'class', 'id', 'name', 'category', 'elevation', 'source_cd', 'source_id', 'file', 'comment', 'created_on', 'created_by'],
            'linesFields'      : ['site', 'class', 'id', 'name', 'category', 'source_cd', 'source_id', 'file', 'comment', 'created_on', 'created_by'],
            'polygonsFields'   : ['site', 'class', 'id', 'name', 'category', 'source_cd', 'source_id', 'file', 'comment', 'created_on', 'created_by'],
        },
        'grid' : {
            'path'             : '',
            'pathSuffix'       : 'vectors/grid',
            'layersGroupName'  : 'Grid',
            'buffersGroupName' : '',
            'bufferSuffix'     : '',
            'pointsLabel'      : 'Grid Points',
            'linesLabel'       : 'Grid Lines',
            'polygonsLabel'    : 'Grid Polygons',
            'pointsBaseName'   : 'grid_pt',
            'linesBaseName'    : 'grid_pl',
            'polygonsBaseName' : 'grid_pg',
            'pointsFields'     : ['site', 'name', 'local_x', 'local_y', 'map_x', 'map_y', 'created_on', 'created_by'],
            'linesFields'      : ['site', 'name', 'local_x', 'local_y', 'map_x', 'map_y', 'created_on', 'created_by'],
            'polygonsFields'   : ['site', 'name', 'local_x', 'local_y', 'map_x', 'map_y', 'created_on', 'created_by'],
        },
        'base' : {
            'path'             : '',
            'pathSuffix'       : 'vectors/base',
            'layersGroupName'  : 'Base Data',
            'buffersGroupName' : 'Edit Data',
            'bufferSuffix'     : '_mem',
            'pointsLabel'      : 'Base Points',
            'linesLabel'       : 'Base Lines',
            'polygonsLabel'    : 'Base Polygons',
            'pointsBaseName'   : 'base_pt',
            'linesBaseName'    : 'base_pl',
            'polygonsBaseName' : 'base_pg',
            'pointsFields'     : ['site', 'name', 'category', 'elevation', 'source_cd', 'source_id', 'file', 'comment', 'created_on', 'created_by'],
            'linesFields'      : ['site', 'name', 'category', 'source_cd', 'source_id', 'file', 'comment', 'created_on', 'created_by'],
            'polygonsFields'   : ['site', 'name', 'category', 'source_cd', 'source_id', 'file', 'comment', 'created_on', 'created_by'],
        },
        'planRaster' : {
            'path'             : '',
            'pathSuffix'       : 'plans',
            'layersGroupName'  : 'Context Plans'
        }
    }

    # Private settings
    _initialised = False

    def __init__(self, plugin):
        super(Project, self).__init__()
        self.plugin = plugin

        # If the legend indexes change make sure we stay updated
        self.plugin.legendInterface().groupIndexChanged.connect(self._groupIndexChanged)

    # Load the module when plugin is loaded
    def load(self):
        self._showLayersDock = self.plugin.iface.mainWindow().findChild(QDockWidget, "Layers").isVisible()
        self._showBrowserDock = self.plugin.iface.mainWindow().findChild(QDockWidget, "Browser").isVisible()
        self.dock = ProjectDock()
        action = self.plugin.addAction(self.plugin.pluginIconPath, self.tr(u'Ark Plan'), checkable=True)
        self.addAction(':/plugins/ArkPlan/settings.svg', self.tr(u'Ark Settings'), self.triggerSettingsDialog)
        self.dock.load(self.plugin.iface, Qt.LeftDockWidgetArea, action)
        self.dock.toggled.connect(self.run)

    def triggerSettingsDialog(self):
        if self.isConfigured():
            self.showSettingsDialog()
        else:
            self.configure()

    # Unload the module when plugin is unloaded
    def unload(self):
        if self.plan is not None:
            self.plan.unload()
        if self.grid is not None:
            self.grid.unload()
        if self.base is not None:
            self.base.unload()
        self.dock.unload()

    def run(self, checked):
        if checked:
            self.plugin.iface.mainWindow().findChild(QDockWidget, "Layers").setVisible(False)
            self.plugin.iface.mainWindow().findChild(QDockWidget, "Browser").setVisible(False)
            self.initialise()
        else:
            self.plugin.iface.mainWindow().findChild(QDockWidget, "Layers").setVisible(self._showLayersDock)
            self.plugin.iface.mainWindow().findChild(QDockWidget, "Browser").setVisible(self._showBrowserDock)

    # Configure the project, i.e. load all settings for QgsProject but don't load anything until needed
    def configure(self):
        if self.isConfigured():
            return
        # TODO more validation, check if files exist, etc
        if (self.showSettingsDialog() and self.siteCode() and self.projectDir().mkpath('.') and self.siteCode() and
            self.planRasterDir().mkpath('.') and self.planRasterDir().mkpath('.') and self.processedPlanDir().mkpath('.') and self.rawPlanDir().mkpath('.') and
            self.moduleDir('grid').mkpath('.') and self.moduleDir('plan').mkpath('.') and self.moduleDir('base').mkpath('.')):
            self._setIsConfigured(True)
        else:
            self._setIsConfigured(False)
            self.showCriticalMessage('ARK Project not configured, unable to continue!')

    def isConfigured(self):
        return self.plugin.readBoolEntry('configured', False)

    def _setIsConfigured(self, configured):
        self.plugin.writeEntry('configured', configured)
        if not configured:
            self._initialised = False

    # Initialise project the first time it is needed, i.e. load the configuration
    def initialise(self):
        if self._initialised:
            return True
        self.configure()
        if self.isConfigured():
            self.projectGroupIndex = layers.createLayerGroup(self.plugin.iface, self.projectGroupName)
            #self.projectLayerModel = QgsLayerTreeModel(QgsProject.instance().layerTreeRoot().findGroup(self.projectGroupName), self);
            self.projectLayerModel = QgsLayerTreeModel(QgsProject.instance().layerTreeRoot(), self);
            self.projectLayerModel.setFlag(QgsLayerTreeModel.ShowLegend)
            self.projectLayerModel.setFlag(QgsLayerTreeModel.ShowLegendAsTree)
            self.projectLayerModel.setFlag(QgsLayerTreeModel.AllowNodeReorder, False)
            self.projectLayerModel.setFlag(QgsLayerTreeModel.AllowNodeRename, False)
            self.projectLayerModel.setFlag(QgsLayerTreeModel.AllowNodeChangeVisibility)
            self.projectLayerModel.setFlag(QgsLayerTreeModel.AllowLegendChangeState)
            self.projectLayerModel.setFlag(QgsLayerTreeModel.AllowSymbologyChangeState)
            self.projectLayerModel.setAutoCollapseLegendNodes(-1)
            self.dock.projectLayerView.setModel(self.projectLayerModel)
            self.grid = self._createCollection('grid')
            self._createCollectionLayers('grid', self.grid._settings)
            self.plan = self._createCollection('plan')
            self._createCollectionMultiLayers('plan', self.plan._settings)
            self.base = self._createCollection('base')
            self._createCollectionLayers('base', self.base._settings)
            self.plugin.iface.projectRead.connect(self.projectLoad)
            self.plugin.iface.newProjectCreated.connect(self.projectLoad)
            if (self.grid.initialise() and self.plan.initialise() and self.base.initialise()):
                self._initialised = True
        return self._initialised

    def isInitialised(self):
        return self._initialised

    def projectLoad(self):
        self.projectChanged.emit()

    def _groupIndexChanged(self, oldIndex, newIndex):
        if (oldIndex == self.projectGroupIndex):
            self.projectGroupIndex = newIndex

    def _layerName(self, baseName):
        if (baseName and self.prependSiteCode() and self.siteCode()):
            return self.siteCode() + '_' + baseName
        return baseName

    def loadGeoLayer(self, geoFile):
        #TODO Check if already loaded, remove old one?
        self.geoLayer = QgsRasterLayer(geoFile.absoluteFilePath(), geoFile.completeBaseName())
        self.geoLayer.renderer().setOpacity(self.planTransparency()/100.0)
        QgsMapLayerRegistry.instance().addMapLayer(self.geoLayer)
        if (self.planGroupIndex < 0):
            self.planGroupIndex = layers.createLayerGroup(self.plugin.iface, self.planGroupName, self.projectGroupName)
        self.plugin.legendInterface().moveLayer(self.geoLayer, self.planGroupIndex)
        self.plugin.mapCanvas().setExtent(self.geoLayer.extent())

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

    def _createCollection(self, module):
        path = self.modulePath(module)
        lcs = LayerCollectionSettings()
        lcs.collectionGroupName = self.layersGroupName(module)
        lcs.parentGroupName = self.projectGroupName
        lcs.buffersGroupName = self.buffersGroupName(module)
        lcs.bufferSuffix = self._moduleDefault(module, 'bufferSuffix')
        layerName = self.pointsLayerName(module)
        if layerName:
            lcs.pointsLayerProvider = 'ogr'
            lcs.pointsLayerLabel = self._moduleDefault(module, 'pointsLabel')
            lcs.pointsLayerName = layerName
            lcs.pointsLayerPath = self._shapeFile(path, layerName)
            lcs.pointsStylePath = self._styleFile(path, layerName, self.pointsBaseName(module), self.pointsBaseNameDefault(module))
        layerName = self.linesLayerName(module)
        if layerName:
            lcs.linesLayerProvider = 'ogr'
            lcs.linesLayerLabel = self._moduleDefault(module, 'linesLabel')
            lcs.linesLayerName = layerName
            lcs.linesLayerPath = self._shapeFile(path, layerName)
            lcs.linesStylePath = self._styleFile(path, layerName, self.linesBaseName(module), self.linesBaseNameDefault(module))
        layerName = self.polygonsLayerName(module)
        if layerName:
            lcs.polygonsLayerProvider = 'ogr'
            lcs.poolygonsLayerLabel = self._moduleDefault(module, 'polygonsLabel')
            lcs.polygonsLayerName = layerName
            lcs.polygonsLayerPath = self._shapeFile(path, layerName)
            lcs.polygonsStylePath = self._styleFile(path, layerName, self.polygonsBaseName(module), self.polygonsBaseNameDefault(module))
        return LayerCollection(self.plugin.iface, lcs)

    def _createCollectionLayers(self, module, settings):
        if (settings.pointsLayerPath and not QFile.exists(settings.pointsLayerPath)):
            layers.createShapefile(settings.pointsLayerPath,   QGis.WKBPoint,        self.plugin.projectCrs(), self._layerFields(module, 'pointsFields'))
        if (settings.linesLayerPath and not QFile.exists(settings.linesLayerPath)):
            layers.createShapefile(settings.linesLayerPath,    QGis.WKBLineString,   self.plugin.projectCrs(), self._layerFields(module, 'linesFields'))
        if (settings.polygonsLayerPath and not QFile.exists(settings.polygonsLayerPath)):
            layers.createShapefile(settings.polygonsLayerPath, QGis.WKBPolygon,      self.plugin.projectCrs(), self._layerFields(module, 'polygonsFields'))

    def _createCollectionMultiLayers(self, module, settings):
        if (settings.pointsLayerPath and not QFile.exists(settings.pointsLayerPath)):
            layers.createShapefile(settings.pointsLayerPath,   QGis.WKBMultiPoint,        self.plugin.projectCrs(), self._layerFields(module, 'pointsFields'))
        if (settings.linesLayerPath and not QFile.exists(settings.linesLayerPath)):
            layers.createShapefile(settings.linesLayerPath,    QGis.WKBMultiLineString,   self.plugin.projectCrs(), self._layerFields(module, 'linesFields'))
        if (settings.polygonsLayerPath and not QFile.exists(settings.polygonsLayerPath)):
            layers.createShapefile(settings.polygonsLayerPath, QGis.WKBMultiPolygon,      self.plugin.projectCrs(), self._layerFields(module, 'polygonsFields'))

    def _layerFields(self, module, fieldsKey):
        fieldKeys = self._moduleDefault(module, fieldsKey)
        fields = QgsFields()
        for fieldKey in fieldKeys:
            fields.append(self.field(fieldKey))
        return fields

    def addAction(self, iconPath, text, callback=None, enabled=True, checkable=False, tip=None, whatsThis=None):
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
            return self.arkFieldDefaults[fieldKey]
        else:
            return self.fieldDefaults[fieldKey]

    def fieldName(self, fieldKey):
        if self.useArkDB():
            return self.arkFieldDefaults[fieldKey].name()
        else:
            return self.fieldDefaults[fieldKey].name()

    # Project settings

    def useArkDB(self):
        return self.plugin.readBoolEntry('useArkDB', False)

    def setUseArkDB(self, useArkDB):
        self.plugin.writeEntry('useArkDB', useArkDB)

    def projectDir(self):
        return QDir(self.projectPath())

    def projectPath(self):
        return self.plugin.readEntry('projectPath', '')

    def setProjectPath(self, absolutePath):
        self.plugin.writeEntry('projectPath', absolutePath)

    def multiSiteProject(self):
        return self.plugin.readBoolEntry('multiSiteProject', False)

    def setMultiSiteProject(self, multiSite):
        self.plugin.writeEntry('multiSiteProject', multiSite)

    def siteCode(self):
        return self.plugin.readEntry('siteCode', '')

    def setSiteCode(self, siteCode):
        self.plugin.writeEntry('siteCode', siteCode)

    def prependSiteCode(self):
        return self.plugin.readBoolEntry('prependSiteCode', True)

    def setPrependSiteCode(self, prepend):
        self.plugin.writeEntry('prependSiteCode', prepend)

    def useCustomStyles(self):
        return self.plugin.readBoolEntry('useCustomStyles', False)

    def setUseCustomStyles(self, useCustomStyles):
        self.plugin.writeEntry('useCustomStyles', useCustomStyles)

    def styleDir(self):
        return QDir(self.stylePath())

    def stylePath(self):
        path =  self.plugin.readEntry('stylePath', '')
        if (not path):
            return self.plugin.pluginPath + '/styles'
        return path

    def setStylePath(self, absolutePath):
        self.plugin.writeEntry('stylePath', absolutePath)


    # Module settings

    def _moduleDefault(self, module, key):
        return self.moduleDefaults[module][key]

    def _moduleEntry(self, module, key):
        return self.plugin.readEntry(module + '/' + key, self._moduleDefault(module, key))

    def _setModuleEntry(self, module, key, value):
        self.plugin.setEntry(module + '/' + key, value, self._moduleDefault(module, key))

    def moduleDir(self, module):
        return QDir(self.modulePath(module))

    def modulePath(self, module):
        path =  self._moduleEntry(module, 'path')
        if (not path):
            return self.modulePathDefault(module)
        return path

    def modulePathDefault(self, module):
        path = self._moduleDefault(module, 'path')
        if not path:
            path = self.projectPath()
            suffix = self._moduleDefault(module, 'pathSuffix')
            if path and suffix:
                path = path + '/' + suffix
        return path

    def setModulePath(self, module, absolutePath):
        self._setModuleEntry(module, 'path', absolutePath)

    def layersGroupName(self, module):
        return self._moduleEntry(module, 'layersGroupName')

    def setLayersGroupName(self, module, layersGroupName):
        self._setModuleEntry(module, 'layersGroupName', layersGroupName)

    def buffersGroupName(self, module):
        return self._moduleEntry(module, 'buffersGroupName')

    def setBuffersGroupName(self, module, buffersGroupName):
        self._setModuleEntry(module, 'buffersGroupName', buffersGroupName)

    def pointsBaseNameDefault(self, module):
        return self._moduleDefault(module, 'pointsBaseName')

    def pointsBaseName(self, module):
        return self._moduleEntry(module, 'pointsBaseName')

    def setPointsBaseName(self, module, pointsBaseName):
        self._setModuleEntry(module, 'pointsBaseName', pointsBaseName)

    def pointsLayerName(self, module):
        return self._layerName(self.pointsBaseName(module))

    def linesBaseNameDefault(self, module):
        return self._moduleDefault(module, 'linesBaseName')

    def linesBaseName(self, module):
        return self._moduleEntry(module, 'linesBaseName')

    def setLinesBaseName(self, module, linesBaseName):
        self._setModuleEntry(module, 'linesBaseName', linesBaseName)

    def linesLayerName(self, module):
        return self._layerName(self.linesBaseName(module))

    def polygonsBaseNameDefault(self, module):
        return self._moduleDefault(module, 'polygonsBaseName')

    def polygonsBaseName(self, module):
        return self._moduleEntry(module, 'polygonsBaseName')

    def setPolygonsBaseName(self, module, polygonsBaseName):
        self._setModuleEntry(module, 'polygonsBaseName', polygonsBaseName)

    def polygonsLayerName(self, module):
        return self._layerName(self.polygonsBaseName(module))

    def collection(self, module):
        if module == 'plan':
            return self.plan
        elif module == 'grid':
            return self.grid
        elif module == 'base':
            return self.base

    # Plan Raster settings

    def planRasterDir(self):
        return QDir(self.planRasterPath())

    def rawPlanDir(self):
        return QDir(self.rawPlanPath())

    def processedPlanDir(self):
        return QDir(self.processedPlanPath())

    def rawPlanPath(self):
        if self.separateProcessedPlanFolder():
            return QDir(self.planRasterPath() + '/raw').absolutePath()
        return self.planRasterPath()

    def processedPlanPath(self):
        if self.separateProcessedPlanFolder():
            return QDir(self.planRasterPath() + '/processed').absolutePath()
        return self.planRasterPath()

    def planRasterPath(self):
        return self.modulePath('planRaster')

    def setPlanRasterPath(self, absolutePath):
        self.plugin.writeEntry('planRasterPath', absolutePath)

    def separateProcessedPlanFolder(self):
        return self.plugin.readBoolEntry('separateProcessedPlanFolder', True)

    def setSeparateProcessedPlanFolder(self, separatePlans):
        self.plugin.writeEntry('separateProcessedPlanFolder', separatePlans)

    def planTransparency(self):
        return self.plugin.readNumEntry('planTransparency', 50)

    def setPlanTransparency(self, transparency):
        self.plugin.writeEntry('planTransparency', transparency)

    def showSettingsDialog(self):
        settingsDialog = SettingsDialog(self, self.plugin.iface.mainWindow())
        return settingsDialog.exec_()
