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

from qgis.core import QGis

from ArkSpatial.ark.lib import utils

from ..project import Project

from collection_field_settings import CollectionFieldSettings


class CollectionLayerSettings:

    layer = ''
    crs = ''
    geometry = QGis.NoGeometry
    label = ''
    name = ''
    fields = []

    path = ''
    stylePath = ''

    bufferLayer = False
    bufferName = ''
    bufferPath = ''

    logLayer = False
    logName = ''
    logPath = ''

    @staticmethod
    def fromArray(config):
        utils.debug('CollectionLayerSettings')
        utils.debug(config)
        settings = CollectionLayerSettings()
        settings.layer = config['layer']
        settings.crs = config['crs']
        settings.geometry = config['geometry']
        settings.label = config['label']
        settings.name = config['name']
        settings.path = config['path']
        settings.stylePath = config['stylePath']
        settings.bufferLayer = config['buffer']
        settings.bufferName = config['bufferName']
        settings.bufferPath = config['bufferPath']
        settings.logLayer = config['log']
        settings.logName = config['logName']
        settings.logPath = config['logPath']
        for field in config['fields']:
            settings.fields.append(CollectionFieldSettings.fromArray(field))
        return settings

    @staticmethod
    def fromProject(scope, path, layer):
        settings = CollectionLayerSettings()
        settings.layer = layer
        path = path + layer + '/'
        settings.label = Project.readEntry(scope, path + 'label')
        settings.name = Project.readEntry(scope, path + 'name')
        settings.path = Project.readEntry(scope, path + 'path')
        settings.bufferLayer = Project.readBoolEntry(scope, path + 'bufferLayer')
        settings.bufferName = Project.readEntry(scope, path + 'bufferName')
        settings.bufferPath = Project.readEntry(scope, path + 'bufferPath')
        settings.logLayer = Project.readBoolEntry(scope, path + 'logLayer')
        settings.logName = Project.readEntry(scope, path + 'logName')
        settings.logPath = Project.readEntry(scope, path + 'logPath')
        fields = Project.readListEntry(scope, path + 'fields')
        for field in fields:
            settings.fields[field] = CollectionFieldSettings.fromProject(scope, path, field)

    def toProject(self, scope, path):
        path = path + self.layer + '/'
        Project.writeEntry(scope, path + 'label', self.label)
        Project.writeEntry(scope, path + 'name', self.name)
        Project.writeEntry(scope, path + 'path', self.path)
        Project.writeEntry(scope, path + 'bufferLayer', self.bufferLayer)
        Project.writeEntry(scope, path + 'bufferName', self.bufferName)
        Project.writeEntry(scope, path + 'bufferPath', self.bufferPath)
        Project.writeEntry(scope, path + 'logLayer', self.logLayer)
        Project.writeEntry(scope, path + 'logName', self.logName)
        Project.writeEntry(scope, path + 'logPath', self.logPath)
        for field in self.fields:
            field.toProject(scope, path)
