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

from qgis.core import QGis, QgsField, QgsFields, QgsLayerTreeModel, QgsMapLayer, QgsMapLayerRegistry, QgsProject

from ..project import Project
from collection import Collection, Collectionsettings, layers


class CollectionFactory:

    def _configureCollection(self, grp):
        config = Config.collections[grp]
        path = config['path']
        bufferPath = path + '/buffer'
        logPath = path + '/log'
        QDir(projectPath + '/' + path).mkpath('.')
        if config['buffer']:
            QDir(projectPath + '/' + bufferPath).mkpath('.')
        if config['log']:
            QDir(projectPath + '/' + logPath).mkpath('.')
        settings = Collectionsettings()
        settings.collection = grp
        settings.collectionPath = path
        settings.parentGroupName = Config.projectGroupName
        settings.collectionGroupName = config['groupName']
        settings.bufferGroupName = config['bufferGroupName']
        settings.log = config['log']
        if config['pointsBaseName']:
            settings.pointsLayerLabel = config['pointsLabel']
            settings.pointsLayerName = self._layerName(config['pointsBaseName'])
            settings.pointsLayerPath = self._shapeFile(path, settings.pointsLayerName)
            settings.pointsStylePath = self._styleFile(path, settings.pointsLayerName, config['pointsBaseName'])
            if config['buffer']:
                settings.pointsBufferName = settings.pointsLayerName + Config.bufferSuffix
                settings.pointsBufferPath = self._shapeFile(bufferPath, settings.pointsBufferName)
            if config['log']:
                settings.pointsLogName = settings.pointsLayerName + Config.logSuffix
                settings.pointsLogPath = self._shapeFile(logPath, settings.pointsLogName)
        if config['linesBaseName']:
            settings.linesLayerLabel = config['linesLabel']
            settings.linesLayerName = self._layerName(config['linesBaseName'])
            settings.linesLayerPath = self._shapeFile(path, settings.linesLayerName)
            settings.linesStylePath = self._styleFile(path, settings.linesLayerName, config['linesBaseName'])
            if config['buffer']:
                settings.linesBufferName = settings.linesLayerName + Config.bufferSuffix
                settings.linesBufferPath = self._shapeFile(bufferPath, settings.linesBufferName)
            if config['log']:
                settings.linesLogName = settings.linesLayerName + Config.logSuffix
                settings.linesLogPath = self._shapeFile(logPath, settings.linesLogName)
        if config['polygonsBaseName']:
            settings.polygonsLayerLabel = config['polygonsLabel']
            settings.polygonsLayerName = self._layerName(config['polygonsBaseName'])
            settings.polygonsLayerPath = self._shapeFile(path, settings.polygonsLayerName)
            settings.polygonsStylePath = self._styleFile(path, settings.polygonsLayerName, config['polygonsBaseName'])
            if config['buffer']:
                settings.polygonsBufferName = settings.polygonsLayerName + Config.bufferSuffix
                settings.polygonsBufferPath = self._shapeFile(bufferPath, settings.polygonsBufferName)
            if config['log']:
                settings.polygonsLogName = settings.polygonsLayerName + Config.logSuffix
                settings.polygonsLogPath = self._shapeFile(logPath, settings.polygonsLogName)
        settings.toProject(self.pluginName)
        if config['multi']:
            self._createCollectionMultiLayers(grp, settings)
        else:
            self._createCollectionLayers(grp, settings)
        return settings

    def loadCollection(self, iface, projectPath, scope, collection):
        settings = Collectionsettings.fromProject(scope, collection)
        if (settings.collection == ''):
            settings = self._configureCollection(collection)
        if settings.pointsStylePath == '':
            settings.pointsStylePath = self._stylePath(
                settings.collection, settings.collectionPath, settings.pointsLayerName, 'pointsBaseName')
        if settings.linesStylePath == '':
            settings.linesStylePath = self._stylePath(
                settings.collection, settings.collectionPath, settings.linesLayerName, 'linesBaseName')
        if settings.polygonsStylePath == '':
            settings.polygonsStylePath = self._stylePath(
                settings.collection, settings.collectionPath, settings.polygonsLayerName, 'polygonsBaseName')
        return Collection(iface, projectPath, settings)

    def _stylePath(self, collection, collectionPath, layerName, baseName):
        return self._styleFile(collectionPath, layerName, Config.collections[collection][baseName])

    def createCollectionLayers(self, projectPath, collection, settings):
        path = projectPath + '/' + settings.pointsLayerPath
        if settings.pointsLayerPath and not QFile.exists(projectPath + '/' + settings.pointsLayerPath):
            layers.createShapefile(path,
                                   settings.pointsLayerName,
                                   QGis.WKBPoint25D,
                                   settings.crs,
                                   self._layerFields(collection, 'pointsFields'))
        path = projectPath + '/' + settings.linesLayerPath
        if (settings.linesLayerPath and not QFile.exists(path)):
            layers.createShapefile(path,
                                   settings.linesLayerName,
                                   QGis.WKBLineString25D,
                                   settings.crs,
                                   self._layerFields(collection, 'linesFields'))
        path = projectPath + '/' + settings.polygonsLayerPath
        if (settings.polygonsLayerPath and not QFile.exists(path)):
            layers.createShapefile(path,
                                   settings.polygonsLayerName,
                                   QGis.WKBPolygon25D,
                                   settings.crs,
                                   self._layerFields(collection, 'polygonsFields'))

    def _createCollectionMultiLayers(self, collection, settings):
        path = projectPath + '/' + settings.pointsLayerPath
        if (settings.pointsLayerPath and not QFile.exists(path)):
            layers.createShapefile(path,
                                   settings.pointsLayerName,
                                   QGis.WKBMultiPoint25D,
                                   self.projectCrs(),
                                   settings.crs,
                                   self._layerFields(collection, 'pointsFields'))
        path = projectPath + '/' + settings.linesLayerPath
        if (settings.linesLayerPath and not QFile.exists(path)):
            layers.createShapefile(path,
                                   settings.linesLayerName,
                                   QGis.WKBMultiLineString25D,
                                   settings.crs,
                                   self._layerFields(collection, 'linesFields'))
        path = projectPath + '/' + settings.polygonsLayerPath
        if (settings.polygonsLayerPath and not QFile.exists(path)):
            layers.createShapefile(path,
                                   settings.polygonsLayerName,
                                   QGis.WKBMultiPolygon25D,
                                   settings.crs,
                                   self._layerFields(collection, 'polygonsFields'))

    def _layerFields(self, collection, fieldsKey):
        fieldKeys = self._collectionDefault(collection, fieldsKey)
        fields = QgsFields()
        for fieldKey in fieldKeys:
            fields.append(self.field(fieldKey))
        return fields
