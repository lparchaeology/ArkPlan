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

from ..project import Project
from .collection_field_settings import CollectionFieldSettings
from .collection_layer_settings import CollectionLayerSettings


class CollectionSettings:

    def __init__(self):
        self.collection = ''
        self.collectionPath = ''
        self.parentGroupName = ''
        self.collectionGroupName = ''
        self.bufferGroupName = ''
        self.buffer = False
        self.log = False
        self.multi = False
        self.layers = []
        self.crs = ''

    @staticmethod
    def fromArray(config):
        settings = CollectionSettings()
        settings.collection = config['collection']
        settings.collectionPath = config['path']
        settings.collectionGroupName = config['groupName']
        settings.parentGroupName = config['parentGroupName']
        settings.buffer = config['buffer']
        settings.bufferGroupName = config['bufferGroupName']
        settings.log = config['log']
        settings.multi = config['multi']
        settings.crs = config['crs']
        for layer in config['layers']:
            settings.layers.append(CollectionLayerSettings.fromArray(layer))
        return settings

    @staticmethod
    def fromProject(scope, collection):
        path = 'collections/' + collection + '/'
        settings = CollectionSettings()
        settings.collection = Project.readEntry(scope, path + 'collection')
        settings.collectionPath = Project.readEntry(scope, path + 'collectionPath')
        settings.collectionGroupName = Project.readEntry(scope, path + 'collectionGroupName')
        settings.parentGroupName = Project.readEntry(scope, path + 'parentGroupName')
        settings.bufferGroupName = Project.readEntry(scope, path + 'bufferGroupName')
        settings.log = Project.readBoolEntry(scope, path + 'log')
        layers = Project.readListEntry(scope, path + 'layers')
        for layer in layers:
            settings.layers.append(CollectionLayerSettings.fromProject(scope, path, layer))
        settings.crs = Project.readEntry(scope, path + 'crs')
        return settings

    def toProject(self, scope):
        path = 'collections/' + self.collection + '/'
        Project.writeEntry(scope, path + 'collection', self.collection)
        Project.writeEntry(scope, path + 'collectionPath', self.collectionPath)
        Project.writeEntry(scope, path + 'collectionGroupName', self.collectionGroupName)
        Project.writeEntry(scope, path + 'parentGroupName', self.parentGroupName)
        Project.writeEntry(scope, path + 'bufferGroupName', self.bufferGroupName)
        Project.writeEntry(scope, path + 'log', self.log)
        for layer in self.layers:
            layer.toProject(scope, path)
        Project.writeEntry(scope, path + 'crs', self.crs.authid())
