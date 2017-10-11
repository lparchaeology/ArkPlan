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

from qgis.core import QgsField

from ..project import Project


class CollectionFieldSettings:

    attribute = ''
    type = None  # QVariant.Type
    length = None
    decimals = None
    min = None
    max = None
    default = None
    label = ''
    query = ''

    @staticmethod
    def fromArray(config):
        settings = CollectionFieldSettings()
        settings.attribute = config['attribute']
        settings.type = config['type']
        settings.length = config['len']
        settings.decimals = config['decimals']
        settings.min = config['min']
        settings.max = config['max']
        settings.default = config['default']
        settings.label = config['label']
        settings.query = config['query']
        return settings

    @staticmethod
    def fromProject(scope, path, attribute):
        settings = CollectionFieldSettings()
        path = path + 'attributes/' + attribute + '/'
        settings.attribute = attribute
        settings.type = Project.readNumEntry(scope, path + 'type')
        settings.length = Project.readNumEntry(scope, path + 'length')
        settings.decimals = Project.readNumEntry(scope, path + 'decimals')
        settings.min = Project.readNumEntry(scope, path + 'min')
        settings.max = Project.readNumEntry(scope, path + 'max')
        settings.default = Project.readEntry(scope, path + 'default')
        settings.label = Project.readEntry(scope, path + 'label')
        settings.query = Project.readEntry(scope, path + 'query')
        return settings

    def toProject(self, scope, path):
        path = path + 'attributes/' + self.attribute + '/'
        Project.writeEntry(scope, path + 'type', self.type)
        Project.writeEntry(scope, path + 'length', self.length)
        Project.writeEntry(scope, path + 'decimals', self.decimals)
        Project.writeEntry(scope, path + 'min', self.min)
        Project.writeEntry(scope, path + 'max', self.max)
        Project.writeEntry(scope, path + 'default', self.default)
        Project.writeEntry(scope, path + 'label', self.label)
        Project.writeEntry(scope, path + 'query', self.query)

    def toField(self):
        return QgsField(self.attribute, self.type, '', self.length, self.decimals, self.label)
