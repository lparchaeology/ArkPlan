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

from PyQt4.QtCore import QObject, pyqtSignal

from qgis.core import QgsFeature

from ArkSpatial.ark.lib import utils

from ArkSpatial.ark.core import Audit

from .item import Item
from .source import Source


class ItemFeature(QObject):

    changed = pyqtSignal()

    def __init__(self, item=None, category=None, label=None, source=None, comment=None, audit=None, parent=None):
        super(ItemFeature, self).__init__(parent)

        self._category = ''
        self._label = ''
        self._comment = ''
        self._item = Item()
        self._source = Source()
        self._audit = Audit()

        if isinstance(item, QgsFeature):
            self.fromFeature(item)
        else:
            self.setFeature(item, category, label, source, comment, audit)

    def __eq__(self, other):
        return (isinstance(other, ItemFeature)
                and self._category == other._category
                and self._label == other._label
                and self._comment == other._comment
                and self._item == other._item
                and self._source == other._source
                and self._audit == other._audit)

    def __lt__(self, other):
        if self._item == other._item:
            return self._category < other._category
        return self._item < other._item

    def __hash__(self):
        return hash((self._category, self._label, self._comment, self._item, self._source, self._audit))

    def __str__(self):
        return ('ItemFeature('
                + str(self._item) + ', '
                + str(self._category) + ', '
                + str(self._label) + ', '
                + str(self._comment) + ')')

    def debug(self):
        return ('ItemFeature('
                + self._item.debug() + ', '
                + utils.printable(self._category) + ', '
                + utils.printable(self._label) + ', '
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
                and self._label == ''
                and isinstance(self._source, Source)
                and self._source.isNull()
                and self._comment == ''
                and self._audit == '')

    def setFeature(self, item, category, label, source, comment, audit):
        self.blockSignals(True)
        self.setItem(item)
        self.setCategory(category)
        self.setLabel(label)
        self.setSource(source)
        self.setComment(comment)
        self.setAudit(audit)
        self.blockSignals(False)
        self.changed.emit()

    def item(self):
        return self._item

    def setItem(self, item):
        if isinstance(item, Item):
            self._item = item
        else:
            self._item = Item()
        self.changed.emit()

    def category(self):
        return self._category

    def setCategory(self, category):
        self._category = utils.string(category)
        self.changed.emit()

    def label(self):
        return self._label

    def setLabel(self, label):
        self._label = utils.string(label)
        self.changed.emit()

    def comment(self):
        return self._comment

    def setComment(self, comment):
        self._comment = utils.string(comment)
        self.changed.emit()

    def source(self):
        return self._source

    def setSource(self, source):
        if isinstance(source, Source):
            self._source = source
        else:
            self._source = Source()
        self.changed.emit()

    def audit(self):
        return self._audit

    def setAudit(self, audit):
        if isinstance(audit, Audit):
            self._audit = audit
        else:
            self._audit = Audit()

    def fromFeature(self, feature):
        item = Item(feature)
        category = feature.attribute('category')
        label = feature.attribute('label')
        source = Source(feature)
        audit = Audit(feature)
        comment = feature.attribute('comment')
        self.setFeature(item, category, label, source, comment, audit)

    def toFeature(self, feature):
        self._item.toFeature(feature)
        feature.setAttribute('category', utils.strip(self._category))
        feature.setAttribute('label', utils.strip(self._label))
        feature.setAttribute('comment', utils.strip(self._comment))
        self._source.toFeature(feature)
        self._audit.toFeature(feature)

    def attributes(self):
        attrs = {}
        attrs['category'] = utils.strip(self._category)
        attrs['label'] = utils.strip(self._label)
        attrs['comment'] = utils.strip(self._comment)
        attrs.update(self.item().attributes())
        attrs.update(self.source().attributes())
        attrs.update(self.audit().attributes())
        return attrs

    def setAttributes(self, attributes):
        self.blockSignals(True)
        if 'category' in attributes:
            self.setCategory(attributes['category'])
        if 'label' in attributes:
            self.selLabel(attributes['label'])
        if 'comment' in attributes:
            self.setComment(attributes['comment'])
        self._item.setAttributes(attributes)
        self._source.setAttributes(attributes)
        self._audit.setAttributes(attributes)
        self.blockSignals(False)
        self.changed.emit()
