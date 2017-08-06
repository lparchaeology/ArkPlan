# -*- coding: utf-8 -*-
"""
/***************************************************************************
                                ARK Spatial
                    A QGIS plugin for Archaeological Recording.
        Part of the Archaeological Recording Kit by L-P : Archaeology
                        http://ark.lparchaeology.com
                              -------------------
        copyright            : 2017 by L-P : Heritage LLP
        email                : ark@lparchaeology.com
        copyright            : 2016 by John Layt
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

from qgis.core import QgsFeature

from ark.lib import utils

from ark.core import Config, Item


class Source():
    _sourceCode = ''
    _item = Item()
    _filename = ''

    def __init__(self, sourceCode=None, item=None, filename=None):
        if isinstance(sourceCode, QgsFeature):
            self.fromFeature(sourceCode)
        else:
            self.setSource(sourceCode, item, filename)

    def __eq__(self, other):
        return (isinstance(other, Source)
                and self._code == other.sourceCode
                and self._item == other.item
                and self._filename == other.filename)

    def __hash__(self):
        return hash((self._code, self._item, self._filename))

    def __str__(self):
        return ('Source('
                + str(self._code) + ', '
                + str(self._item) + ', '
                + str(self._filename) + ')')

    def debug(self):
        return ('Source('
                + utils.printable(self._code) + ', '
                + self._item.debug() + ', '
                + utils.printable(self._filename) + ')')

    def isValid(self):
        if self._code == '':
            return False
        if Config.sourceCodes[self._code]['sourceItem']:
            return self._item.isValid()
        return isinstance(self._item, Item) and (self._item.isValid() or self._item.isNull())

    def isInvalid(self):
        return not self.isValid()

    def isNull(self):
        return self._code == '' and isinstance(item, Item) and self._item.isNull() and self._filename == ''

    def label(self):
        return Config.sourceCodes[self._code]['label']

    def setSource(self, sourceCode, item, filename):
        self._code = utils.string(sourceCode)
        if isinstance(item, Item):
            self._item = item
        else:
            self._item = Item()
        self._filename = utils.string(filename)

    def sourceCode(self):
        return self._code

    def setSourceCode(self, sourceCode):
        self._code = utils.string(sourceCode)

    def item(self):
        return self._item

    def setItem(self, item):
        self._item = item

    def filename(self):
        return self._filename

    def setFilename(self, filename):
        self._filename = utils.string(filename)

    def attributes(self):
        attrs = {}
        attrs = self._item.toAttributes()
        _setDict(attrs, 'source_cd', self.sourceCode())
        _setDict(attrs, 'source_cl', self.item().classCode())
        _setDict(attrs, 'source_id', self.item().itemId())
        _setDict(attrs, 'file', self.filename())
        return attrs

    def setAttributes(self, attributes):
        if 'source_cd' in attributes:
            self.setSourceCode(attributes['source_cd'])
        if 'file' in attributes:
            self.setFilename(attributes['file'])
        attr = {}
        if 'site' in attributes:
            attr['site'] = attributes['site']
        if 'source_cl' in attributes:
            attr['class'] = attributes['source_cl']
        if 'source_id' in attributes:
            attr['id'] = attributes['source_id']
        self._item.setAttributes(attr)
