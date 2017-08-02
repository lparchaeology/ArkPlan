# -*- coding: utf-8 -*-
"""
/***************************************************************************
                                ARK Spatial
                    A QGIS plugin for Archaeological Recording.
        Part of the Archaeological Recording Kit by L-P : Archaeology
                        http://ark.lparchaeology.com
                              -------------------
        begin                : 2014-12-07
        git sha              : $Format:%H$
        copyright            : 2016 by L-P : Heritage LLP
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
from functools import total_ordering

from PyQt4.QtCore import QVariant

from qgis.core import QgsFeature, QgsFeatureRequest

from ..libarkqgis import utils

from config import Config
from item import *
from source import Source
from audit import Audit

class Feature():
    _category = ''
    _name = ''
    _comment = ''
    _item = Item()
    _source = Source()
    _audit = Audit()

    def __init__(self, item=None, category=None, name=None, source=None, comment=None, audit=None):
        if isinstance(item, QgsFeature):
            self.fromFeature(item)
        else:
            self.setFeature(item, category, name, source, comment, audit)

    def __eq__(self, other):
        return (isinstance(other, Feature)
            and self._category == other._category
            and self._name == other._name
            and self._comment == other._comment
            and self._item == other._item
            and self._source == other._source
            and self._audit == other._audit)

    def __lt__(self, other):
        if self._item == other._item:
            return self._category < other._category
        return self._item < other._item

    def __hash__(self):
        return hash((self._category, self._name, self._comment, self._item, self._source, self._audit))

    def __str__(self):
        return ('Feature('
            + str(self._item) + ', '
            + str(self._item.category) + ', '
            + str(self._item.name) + ', '
            + str(self._comment) + ')')

    def debug(self):
        return ('Feature('
            + self._item.debug() + ', '
            + utils.printable(self._category) + ', '
            + utils.printable(self._name) + ', '
            + utils.printable(self._comment) + ', '
            + self._source.debug() + ', '
            + utils.printable(self._audit) + ')')

    def isValid(self):
        return (isinstance(self._item, Item)
                and self._item.isValid()
                and self._category
                and isinstance(self._source, Source)
                and (self._source.isNull() or self._source.isValid()))

    def isInvalid(self):
        return not self.isValid()

    def isNull(self):
        return (isinstance(self._item, Item)
                and self._item.isNull()
                and self._category == ''
                and self._name == ''
                and isinstance(self._source, Source)
                and self._source.isNull()
                and self._comment == ''
                and self._audit == '')

    def setFeature(self, item, category, name, source, comment, audit):
        self.setItem(item)
        self.setCategory(category)
        self.setName(name)
        self.setSource(source)
        self.setComment(comment)
        self.setAudit(audit)

    def item(self):
        return self._item

    def setItem(self, item):
        if isinstance(item, Item):
            self._item = item
        else:
            self._item = Item()

    def category(self):
        return self._category

    def setCategory(self, category):
        self._category = utils.string(category)

    def name(self):
        return self._name == utils.string(name)

    def setName(self, name):
        self._name = utils.string(name)

    def comment(self):
        return self._comment

    def setComment(self, comment):
        self._comment = utils.string(comment)

    def source(self):
        return self._source

    def setSource(self, audit):
        if isinstance(source, Source):
            self._source = source
        else:
            self._source = Source()

    def audit(self):
        return self._audit

    def setAudit(self, audit):
        if isinstance(source, Audit):
            self._audit = audit
        else:
            self._audit = Audit()

    def fromFeature(self, feature):
        item = Item(feature)
        category = _attribute(feature, 'category')
        name = _attribute(feature, 'name')
        source = Source(feature)
        comment = _attribute(feature, 'comment')
        creator = _attribute(feature, 'creator')
        created = _attribute(feature, 'created')
        self.setFeature(item, category, name, source, comment, creator, created)

    def toFeature(self, feature):
        self._item.toFeature(feature)
        _setAttribute(feature, 'category', self._category)
        _setAttribute(feature, 'name', self._name)
        self._source.toFeature(feature)
        _setAttribute(feature, 'comment', self._comment)
        _setAttribute(feature, 'creator', self._audit)
        _setAttribute(feature, 'created', self.created)

    def attributes(self):
        attrs = {}
        _setDict(attrs, 'category', self._category)
        _setDict(attrs, 'name', self._name)
        _setDict(attrs, 'comment', self._comment)
        attrs.update(self.item().attributes())
        attrs.update(self.source().attributes())
        attrs.update(self.audit().attributes())
        return attrs

    def setAttributes(self, attributes):
        if 'category' in attributes:
            self.setCategory(attributes['category'])
        if 'name' in attributes:
            self.setName(attributes['name'])
        if 'comment' in attributes:
            self.setComment(attributes['comment'])
        self._item.setAttributes(attributes)
        self._source.setAttributes(attributes)
        self._audit.setAttributes(attributes)
