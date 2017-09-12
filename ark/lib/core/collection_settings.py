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

from ..project import Project
from collection_layer_settings import CollectionLayerSettings


class CollectionSettings:

    collection = ''
    collectionPath = ''

    parentGroupName = ''
    collectionGroupName = ''
    bufferGroupName = ''
    log = False

    points = None
    lines = None
    polygons = None

    @staticmethod
    def fromProject(scope, collection):
        path = 'collections/' + collection + '/'
        cs = CollectionSettings()
        cs.collection = Project.readEntry(scope, path + 'collection')
        cs.collectionPath = Project.readEntry(scope, path + 'collectionPath')
        cs.collectionGroupName = Project.readEntry(scope, path + 'collectionGroupName')
        cs.parentGroupName = Project.readEntry(scope, path + 'parentGroupName')
        cs.bufferGroupName = Project.readEntry(scope, path + 'bufferGroupName')
        cs.log = Project.readBoolEntry(scope, path + 'log')
        cs.points = CollectionLayerSettings.fromProject(scope, path, 'points')
        cs.lines = CollectionLayerSettings.fromProject(scope, path, 'points')
        cs.polygons = CollectionLayerSettings.fromProject(scope, path, 'points')
        return cs

    def toProject(self, scope):
        path = 'collections/' + self.collection + '/'
        Project.writeEntry(scope, path + 'collection', self.collection)
        Project.writeEntry(scope, path + 'collectionPath', self.collectionPath)
        Project.writeEntry(scope, path + 'collectionGroupName', self.collectionGroupName)
        Project.writeEntry(scope, path + 'parentGroupName', self.parentGroupName)
        Project.writeEntry(scope, path + 'bufferGroupName', self.bufferGroupName)
        Project.writeEntry(scope, path + 'log', self.log)
        self.points.toProject(scope, path)
        self.lines.toProject(scope, path)
        self.polygons.toProject(scope, path)
