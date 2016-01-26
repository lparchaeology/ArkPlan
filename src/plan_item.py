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

from PyQt4.QtCore import QVariant

from qgis.core import QgsFeature, QgsFeatureRequest

from ..libarkqgis import utils

from config import Config

class ItemKey():
    siteCode = ''
    classCode = ''
    itemId = ''

    def __init__(self, siteCode=None, classCode=None, itemId=None):
        if type(siteCode) == QgsFeature:
            self.setFeature(siteCode)
        else:
            self.setKey(siteCode, classCode, itemId)

    def __eq__(self, other):
        return self.siteCode == other.siteCode and self.classCode == other.classCode and self.itemId == other.itemId

    def __lt__(self, other):
        if self.siteCode == other.siteCode and self.classCode == other.classCode:
            return self._lt(self.itemId, other.itemId)
        elif self.siteCode == other.siteCode:
            return self.classCode < other.classCode and self._lt(self.itemId, other.itemId)
        return self.siteCode < other.siteCode and self.classCode < other.classCode and self._lt(self.itemId, other.itemId)

    def _lt(self, id1, id2):
        if type(id1) == str and id1.isdigit() and type(id2) == str and id2.isdigit():
            return int(id1) < int(id2)
        else:
            return id1 < id2

    def __hash__(self):
        return hash((self.siteCode, self.classCode, self.itemId))

    def __str__(self):
        return 'ItemKey(' + str(self.siteCode) + ', ' +  str(self.classCode) + ', ' +  str(self.itemId) + ')'

    def isValid(self):
        return self.siteCode and self.classCode and self.itemId

    def isInvalid(self):
        return (self.siteCode == '' or self.classCode == '' or self.itemId == '')

    def isNull(self):
        return (self.siteCode == '' and self.classCode == '' and self.itemId == '')

    def isItemRange(self):
        return self.itemId.contains('-') or self.itemId.contains(' ')

    def setKey(self, siteCode, classCode, itemId):
        if siteCode and classCode and itemId:
            self.siteCode = utils.string(siteCode)
            self.classCode = utils.string(classCode)
            self.setItemId(itemId)
        else:
            self.siteCode = ''
            self.classCode = ''
            self.itemId = ''

    def setFeature(self, feature):
        siteCode = feature.attribute(Config.fieldName('site'))
        classCode = feature.attribute(Config.fieldName('class'))
        itemId = feature.attribute(Config.fieldName('id'))
        self.setKey(siteCode, classCode, itemId)

    def setItemId(self, itemId):
        if type(itemId) == list or type(itemId) == set:
            self.itemId = utils.listToRange(itemId)
        else:
            self.itemId = utils.string(itemId)

    def addItemId(self, itemId):
        if self.itemId == '':
            self.setItemId(itemId)
        else:
            lst = self.itemIdList()
            if type(itemId) == list or type(itemId) == set:
                lst.extend(itemId)
            else:
                lst.append(utils.string(itemId))
            self.setItemId(lst)

    def itemIdList(self):
        return utils.rangeToList(self.itemId)

    def filterClause(self):
        if self.isInvalid():
            return ''
        clause = '("' + Config.fieldName('site') + '" = \'' + self.siteCode + '\''
        clause = clause + ' and "' + Config.fieldName('class') + '" = \'' + self.classCode + '\''
        subs = self.itemId.split()
        if len(subs) == 0:
            clause += ')'
            return clause
        clause += ' and ('
        first = True
        for sub in subs:
            if first:
                first = False
            else:
                clause = clause + ' or '
            field = Config.fieldName('id')
            if sub.find('-') >= 0:
                vals = sub.split('-')
                clause = clause + ' ("' + field + '" >= ' + vals[0] + ' and "' + field + '" <= ' + vals[1] + ')'
            else:
                clause = clause + '"' + field + '" = ' + sub
        clause += '))'
        return clause

    def featureRequest(self):
        request = QgsFeatureRequest()
        request.setFilterExpression(self.filterClause())
        return request


class ItemSource():
    sourceCode = ''
    key = ItemKey()
    filename = ''

    def __init__(self, sourceCode=None, sourceKey=None, filename=None):
        if type(sourceCode) == QgsFeature:
            self.setFeature(sourceCode)
        else:
            self.setSource(sourceCode, sourceKey, filename)

    def __eq__(self, other):
        return self.sourceCode == other.sourceCode and self.key == other.key and self.filename == other.filename

    def __hash__(self):
        return hash((self.sourceCode, self.key, self.filename))

    def __str__(self):
        return 'ItemSource(' + str(self.sourceCode) + ', ' + str(self.key.siteCode) + ', ' +  str(self.key.classCode) + ', ' +  str(self.key.itemId) + ')'

    def isValid(self):
        return self.sourceCode and self.key.isValid()

    def isInvalid(self):
        return not self.isValid()

    def isNull(self):
        return self.sourceCode == '' and self.key.isNull() and filename == ''

    def setSource(self, sourceCode, sourceKey, filename):
        if sourceCode:
            self.sourceCode = utils.string(sourceCode)
            self.key = sourceKey
            self.filename = utils.string(filename)
        else:
            self.sourceCode = ''
            self.key = ItemKey()
            self.filename = ''

    def setFeature(self, feature):
        sourceCode = feature.attribute(Config.fieldName('source_cd'))
        siteCode = feature.attribute(Config.fieldName('site'))
        classCode = feature.attribute(Config.fieldName('source_cl'))
        itemId = feature.attribute(Config.fieldName('source_id'))
        sourceKey = ItemKey(siteCode, classCode, itemId)
        filename = feature.attribute(Config.fieldName('file'))
        self.setSource(sourceCode, sourceKey, filename)

class Item():
    key = ItemKey()
    name = ''
    source = ItemSource()
    comment = ''

    def __init__(self, key=None, name=None, source=None, comment=None):
        if type(key) == QgsFeature:
            self.setFeature(key)
        else:
            self.setItem(key, name, source, comment)

    def __eq__(self, other):
        return self.key == other.key and self.name == other.name and self.source == other.source and self.comment == other.comment

    def __lt__(self, other):
        if self.key == other.key:
            return self.name < other.name
        return self.key < other.key

    def __hash__(self):
        return hash((self.key, self.name, self.source, self.comment))

    def __str__(self):
        return 'Item(' + str(self.key.siteCode) + ', ' +  str(self.key.classCode) + ', ' +  str(self.key.itemId) + ')'

    def isValid(self):
        return self.key.isValid()

    def isInvalid(self):
        return self.key.isInvalid()

    def isNull(self):
        return self.key.isNull()

    def setItem(self, key, name, source, comment):
        if key.isValid():
            self.key = key
            self.name = utils.string(name)
            self.source = source
            self.comment = utils.string(comment)
        else:
            self.key = ItemKey()
            self.name = ''
            self.source = ItemSource()
            self.comment = ''

    def setFeature(self, feature):
        key = ItemKey(feature)
        name = feature.attribute(Config.fieldName('name'))
        source = ItemSource(feature)
        comment = feature.attribute(Config.fieldName('comment'))
        self.setItem(key, name, source, comment)
