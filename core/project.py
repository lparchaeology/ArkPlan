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
from PyQt4.QtCore import Qt, QSettings, QFile, QDir, QObject, QVariant, pyqtSignal
from PyQt4.QtGui import  QIcon, QAction

from qgis.core import QgsProject, QgsSnapper, QgsMessageLog, QgsField, QgsFields
from qgis.gui import QgsMessageBar

from layercollection import *
from settings_dialog import SettingsDialog


class Project(QObject):

    # Signal when the project changes so modules can reload
    projectChanged = pyqtSignal()

    iface = None # QgsInteface()
    project = None # QgsProject()
    pluginName = 'Ark'
    pluginPath = ''
    pluginIconPath = ':/plugins/Ark/icon.png'

    menuName = ''
    toolbar = None  # QToolBar()
    projectAction = None  # QAction()

    projectGroupName = 'Ark'
    projectGroupIndex = -1
    planGroupName = 'Context Plans'
    planGroupIndex = -1

    geoLayer = None  #QgsRasterLayer()
    contexts = None  # LayerCollection()
    grid = None  # LayerCollection()

    fieldDefaults = {
        'site'      : QgsField('site',       QVariant.String, '',  10, 0, 'Site Code'),
        'id'        : QgsField('id',         QVariant.String, '',  10, 0, 'ID'),
        'context'   : QgsField('context',    QVariant.Int,    '',   5, 0, 'Context'),
        'category'  : QgsField('category',   QVariant.String, '',  10, 0, 'Category'),
        'elevation' : QgsField('elevation',  QVariant.Double, '',  10, 3, 'Elevation'),
        'source'    : QgsField('source',     QVariant.String, '',  10, 0, 'Source'),
        'file'      : QgsField('file',       QVariant.String, '',  50, 0, 'File'),
        'local_x'   : QgsField('local_x',    QVariant.Double, '',  10, 3, 'Local Grid X'),
        'local_y'   : QgsField('local_y',    QVariant.Double, '',  10, 3, 'Local Grid Y'),
        'crs_x'     : QgsField('crs_x',      QVariant.Double, '',  10, 3, 'CRS X'),
        'crs_y'     : QgsField('crs_y',      QVariant.Double, '',  10, 3, 'CRS y'),
        'comment'   : QgsField('comment',    QVariant.String, '', 100, 0, 'Comment'),
        'created_on': QgsField('created_on', QVariant.String, '',  20, 0, 'Created On'),  # '2012-01-01T23:59:59Z'
        'created_by': QgsField('created_by', QVariant.String, '',  20, 0, 'Created By')
    }

    moduleDefaults = {
        'contexts' : {
            'path' : '',
            'layersGroupName'  : 'Context Data',
            'buffersGroupName' : 'Edit Context Data',
            'bufferSuffix'     : '_mem',
            'pointsBaseName'   : 'context_pt',
            'linesBaseName'    : 'context_pl',
            'polygonsBaseName' : 'context_pg',
            'schemaBaseName'   : 'context_mpg',
            'pointsFields'     : ['site', 'context', 'category', 'elevation', 'source', 'file', 'comment', 'created_on', 'created_by'],
            'linesFields'      : ['site', 'context', 'category', 'source', 'file', 'comment', 'created_on', 'created_by'],
            'polygonsFields'   : ['site', 'context', 'category', 'source', 'file', 'comment', 'created_on', 'created_by'],
            'schemaFields'     : ['site', 'context', 'category', 'source', 'file', 'comment', 'created_on', 'created_by']
        },
        'grid' : {
            'path' : '',
            'layersGroupName'  : 'Grid',
            'buffersGroupName' : '',
            'bufferSuffix'     : '',
            'pointsBaseName'   : 'grid_pt',
            'linesBaseName'    : 'grid_pl',
            'polygonsBaseName' : 'grid_pg',
            'schemaBaseName'   : '',
            'pointsFields'     : ['site', 'id', 'category', 'local_x', 'local_y', 'crs_x', 'crs_y', 'source', 'created_on', 'created_by'],
            'linesFields'      : ['site', 'id', 'category', 'local_x', 'local_y', 'crs_x', 'crs_y', 'source', 'created_on', 'created_by'],
            'polygonsFields'   : ['site', 'id', 'category', 'local_x', 'local_y', 'crs_x', 'crs_y', 'source', 'created_on', 'created_by'],
            'schemaFields'     : []
        }
    }

    # Private settings
    _initialised = False

    def __init__(self, iface, pluginPath):
        super(Project, self).__init__()
        self.iface = iface

        self.pluginName = self.tr(u'Ark')
        self.pluginPath = pluginPath

        # Declare instance attributes
        self.menuName = self.tr(u'&Ark')
        self.toolbar = self.iface.addToolBar(self.pluginName)
        self.toolbar.setObjectName(self.pluginName)

        # If the legend indexes change make sure we stay updated
        self.iface.legendInterface().groupIndexChanged.connect(self._groupIndexChanged)

    # Load the module when plugin is loaded
    def load(self):
        self.projectAction = self.createMenuAction(self.tr(u'Ark Settings'), self.pluginIconPath, False)
        self.projectAction.triggered.connect(self.showSettingsDialog)

    # Unload the module when plugin is unloaded
    def unload(self):
        if self.contexts is not None:
            self.contexts.unload()
        if self.grid is not None:
            self.grid.unload()
        self.iface.removePluginMenu(self.menuName, self.projectAction)
        self.iface.removeToolBarIcon(self.projectAction)

    # Configure the project, i.e. load all settings for QgsProject but don't load anything until needed
    def configure(self):
        if self.isConfigured():
            return
        ret = self.showSettingsDialog()
        # TODO more validation, check if files exist, etc
        if (self.projectDir().exists() and self.planDir().exists() and self.styleDir().exists() and self.moduleDir('grid').exists() and self.moduleDir('contexts').exists()):
            self._setIsConfigured(True)
        else:
            self._setIsConfigured(False)
            self.showCriticalMessage('ARK Project not configured, unable to continue!')

    def isConfigured(self):
        return QgsProject.instance().readBoolEntry(self.pluginName, 'configured', False)[0]

    def _setIsConfigured(self, configured):
        QgsProject.instance().writeEntry(self.pluginName, 'configured', configured)
        if not configured:
            self._initialised = False

    # Initialise project the first time it is needed, i.e. load the configuration
    def initialise(self):
        if self._initialised:
            return True
        self.configure()
        if self.isConfigured():
            self.grid = self._createCollection('grid')
            self._createCollectionLayers('grid', self.grid._settings)
            self.contexts = self._createCollection('contexts')
            self._createCollectionLayers('contexts', self.contexts._settings)
            self.iface.projectRead.connect(self.projectLoad)
            self.iface.newProjectCreated.connect(self.projectLoad)
            if (self.grid.initialise() and self.contexts.initialise()):
                self._initialised = True
        return self._initialised

    def isInitialised(self):
        return self._initialised

    def projectLoad(self):
        self.projectChanged.emit()

    def createMenuAction(self, actionText, iconPath, checkable, tip='', whatsThis=''):
        icon = QIcon(iconPath)
        action = QAction(icon, actionText, self.iface.mainWindow())
        action.setCheckable(checkable)
        action.setStatusTip(tip)
        action.setWhatsThis(whatsThis)
        self.toolbar.addAction(action)
        self.iface.addPluginToMenu(self.menuName, action)
        return action

    def _groupIndexChanged(self, oldIndex, newIndex):
        if (oldIndex == self.projectGroupIndex):
            self.projectGroupIndex = newIndex

    # Convenience logging functions

    def logMessage(self, text, level=QgsMessageLog.INFO):
        QgsMessageLog.logMessage(text, self.pluginName, level)

    def showCriticalMessage(self, text, duration=0):
        self.iface.messageBar().pushMessage(text, QgsMessageBar.CRITICAL, duration)

    def showMessage(self, text, level=QgsMessageBar.INFO, duration=0):
        self.iface.messageBar().pushMessage(text, level, duration)

    def showStatusMessage(self, text):
        self.iface.mainWindow().statusBar().showMessage(text)


    # Settings utilities

    def _setProjectEntry(self, key, value, default):
        if (value == None or value == '' or value == default):
            QgsProject.instance().removeEntry(self.pluginName, key)
        else:
            QgsProject.instance().writeEntry(self.pluginName, key, value)

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
            self.planGroupIndex = self.getGroupIndex(self.planGroupName)
        self.iface.legendInterface().moveLayer(self.geoLayer, self.planGroupIndex)
        self.iface.mapCanvas().setExtent(self.geoLayer.extent())

    def applyContextFilter(self, contextList):
        self.contexts.applyFieldFilter(self.fieldName('context'), contextList)

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
        lcs.buffersGroupName = self.buffersGroupName(module)
        lcs.bufferSuffix = self._moduleDefault(module, 'bufferSuffix')
        layerName = self.pointsLayerName(module)
        if layerName:
            lcs.pointsLayerProvider = 'ogr'
            lcs.pointsLayerName = layerName
            lcs.pointsLayerPath = self._shapeFile(path, layerName)
            lcs.pointsStylePath = self._styleFile(path, layerName, self.pointsBaseName(module), self.pointsBaseNameDefault(module))
        layerName = self.linesLayerName(module)
        if layerName:
            lcs.linesLayerProvider = 'ogr'
            lcs.linesLayerName = layerName
            lcs.linesLayerPath = self._shapeFile(path, layerName)
            lcs.linesStylePath = self._styleFile(path, layerName, self.linesBaseName(module), self.linesBaseNameDefault(module))
        layerName = self.polygonsLayerName(module)
        if layerName:
            lcs.polygonsLayerProvider = 'ogr'
            lcs.polygonsLayerName = layerName
            lcs.polygonsLayerPath = self._shapeFile(path, layerName)
            lcs.polygonsStylePath = self._styleFile(path, layerName, self.polygonsBaseName(module), self.polygonsBaseNameDefault(module))
        layerName = self.schemaLayerName(module)
        if layerName:
            lcs.schemaLayerProvider = 'ogr'
            lcs.schemaLayerName = layerName
            lcs.schemaLayerPath = self._shapeFile(self.modulePath(module), layerName)
            lcs.schemaStylePath = self._styleFile(self.modulePath(module), layerName, self.schemaBaseName(module), self.schemaBaseNameDefault(module))
        return LayerCollection(self.iface, lcs)

    def _createCollectionLayers(self, module, settings):
        utils.createShapefile(settings.pointsLayerPath, self._layerFields(module, 'pointsFields'), QGis.WKBPoint, self.projectCrs())
        utils.createShapefile(settings.linesLayerPath, self._layerFields(module, 'linesFields'), QGis.WKBLineString, self.projectCrs())
        utils.createShapefile(settings.polygonsLayerPath, self._layerFields(module, 'polygonsFields'), QGis.WKBPolygon, self.projectCrs())
        utils.createShapefile(settings.schemaLayerPath, self._layerFields(module, 'schemaFields'), QGis.WKBMultiPolygon, self.projectCrs())

    def _layerFields(self, module, fieldsKey):
        fieldKeys = self._moduleDefault(module, fieldsKey)
        fields = QgsFields()
        for fieldKey in fieldKeys:
            field = self.fieldDefaults[fieldKey]
            fields.append(field)
        return fields

    # Field settings

    def field(self, fieldKey):
        return self.fieldDefaults[fieldKey]

    def fieldName(self, fieldKey):
        return self.fieldDefaults[fieldKey].name()

    # Project settings

    def projectDir(self):
        return QDir(self.projectPath())

    def projectPath(self):
        return QgsProject.instance().readEntry(self.pluginName, 'projectPath', '')[0]

    def setProjectPath(self, absolutePath):
        QgsProject.instance().writeEntry(self.pluginName, 'projectPath', absolutePath)

    def multiSiteProject(self):
        return QgsProject.instance().readBoolEntry(self.pluginName, 'multiSiteProject', False)[0]

    def setMultiSiteProject(self, multiSite):
        QgsProject.instance().writeEntry(self.pluginName, 'multiSiteProject', multiSite)

    def siteCode(self):
        return QgsProject.instance().readEntry(self.pluginName, 'siteCode', '')[0]

    def setSiteCode(self, siteCode):
        QgsProject.instance().writeEntry(self.pluginName, 'siteCode', siteCode)

    def prependSiteCode(self):
        return QgsProject.instance().readBoolEntry(self.pluginName, 'prependSiteCode', True)[0]

    def setPrependSiteCode(self, prepend):
        QgsProject.instance().writeEntry(self.pluginName, 'prependSiteCode', prepend)

    def useCustomStyles(self):
        return QgsProject.instance().readBoolEntry(self.pluginName, 'useCustomStyles', False)[0]

    def setUseCustomStyles(self, useCustomStyles):
        QgsProject.instance().writeEntry(self.pluginName, 'useCustomStyles', useCustomStyles)

    def styleDir(self):
        return QDir(self.stylePath())

    def stylePath(self):
        path =  QgsProject.instance().readEntry(self.pluginName, 'stylePath', '')[0]
        if (not path):
            return self.pluginPath + '/styles'
        return path

    def setStylePath(self, absolutePath):
        QgsProject.instance().writeEntry(self.pluginName, 'stylePath', absolutePath)


    # Module settings

    def _moduleDefault(self, module, key):
        return self.moduleDefaults[module][key]

    def _moduleEntry(self, module, key):
        return QgsProject.instance().readEntry(self.pluginName, module + '/' + key, self._moduleDefault(module, key))[0]

    def _setModuleEntry(self, module, key, value):
        self._setProjectEntry(module + '/' + key, value, self._moduleDefault(module, key))

    def moduleDir(self, module):
        return QDir(self.modulePath(module))

    def modulePath(self, module):
        path =  self._moduleEntry(module, 'path')
        if (not path):
            return self.projectPath()
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

    def schemaBaseNameDefault(self, module):
        return self._moduleDefault(module, 'schemaBaseName')

    def schemaBaseName(self, module):
        return self._moduleEntry(module, 'schemaBaseName')

    def setSchemaBaseName(self, module, schemaBaseName):
        self._setModuleEntry(module, 'schemaBaseName', schemaBaseName)

    def schemaLayerName(self, module):
        return self._layerName(self.schemaBaseName(module))


    # Plan settings

    def planDir(self):
        return QDir(self.planPath())

    def rawPlanPath(self):
        if self.separatePlanFolders():
            dir = QDir(self.planPath() + '/raw')
            if dir.exists():
                return dir.absolutePath()
        return self.planPath()

    def processedPlanPath(self):
        if self.separatePlanFolders():
            dir = QDir(self.planPath() + '/processed')
            if (not dir.exists()):
                self.planDir().mkdir('processed')
            return dir.absolutePath()
        return self.planPath()

    def planPath(self):
        return QgsProject.instance().readEntry(self.pluginName, 'planPath', '')[0]

    def setPlanPath(self, absolutePath):
        QgsProject.instance().writeEntry(self.pluginName, 'planPath', absolutePath)

    def separatePlanFolders(self):
        return QgsProject.instance().readBoolEntry(self.pluginName, 'separatePlanFolders', True)[0]

    def setSeparatePlanFolders(self, separatePlans):
        QgsProject.instance().writeEntry(self.pluginName, 'separatePlanFolders', separatePlans)

    def planTransparency(self):
        return QgsProject.instance().readNumEntry(self.pluginName, 'planTransparency', 50)[0]

    def setPlanTransparency(self, transparency):
        QgsProject.instance().writeEntry(self.pluginName, 'planTransparency', transparency)


    def projectCrs(self):
        self.iface.mapCanvas().mapRenderer().destinationCrs()

    def showSettingsDialog(self):
        settingsDialog = SettingsDialog(self, self.iface.mainWindow())
        return settingsDialog.exec_()

    def defaultSnappingMode(self):
        defaultSnappingModeString = QSettings().value('/qgis/digitizing/default_snap_mode', 'to vertex')
        defaultSnappingMode = QgsSnapper.SnapToVertex
        if (defaultSnappingModeString == "to vertex and segment" ):
            return QgsSnapper.SnapToVertexAndSegment
        elif (defaultSnappingModeString == 'to segment'):
            return QgsSnapper.SnapToSegment
        return QgsSnapper.SnapToVertex

    def defaultSnappingUnit(self):
        unit = QSettings().value('/qgis/digitizing/default_snapping_tolerance_unit', 0, int)
        # Huh???
        if unit is None:
            return 0
        return unit

    def defaultSnappingTolerance(self):
        tolerance = QSettings().value('/qgis/digitizing/default_snapping_tolerance', 10.0, float)
        # Huh???
        if tolerance is None:
            return 0.0
        return tolerance
