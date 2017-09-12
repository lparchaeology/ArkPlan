# -*- coding: utf-8 -*-
"""
/***************************************************************************
                                ARK QGIS
                        A QGIS utilities library.
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

from qgis.core import QGis, QgsField, QgsFields, QgsLayerTreeModel, QgsMapLayer, QgsMapLayerRegistry, QgsProject

from ..project import Project
from collection import Collection, CollectionSettings, layers


class CollectionFactory:

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

    def _loadCollection(self, collection):
        lcs = CollectionSettings.fromProject(self.pluginName, collection)
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
        return Collection(self.iface, self.projectPath(), lcs)

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
