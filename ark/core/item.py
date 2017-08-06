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

from functools import total_ordering

from qgis.core import QgsFeatureRequest

from ark.lib import utils

from ark.core import Config


def _setAttribute(feature, attribute, value):
    try:
        feature.setAttribute(attribute, utils.strip(value))
    except:
        pass


def _attribute(feature, attribute):
    try:
        return feature.attribute(attribute)
    except:
        return None


@total_ordering
class Item():
    _siteCode = ''
    _classCode = ''
    _itemId = ''

    def __init__(self, siteCode=None, classCode=None, itemId=None):
        self.setItem(siteCode, classCode, itemId)

    def __eq__(self, other):
        return (isinstance(other, Item)
                and self._siteCode == other._siteCode
                and self._classCode == other._classCode
                and self._itemId == other._itemId)

    def __lt__(self, other):
        if self._siteCode == other._siteCode and self._classCode == other._classCode:
            return self._lt(self._itemId, other._itemId)
        elif self._siteCode == other._siteCode:
            return self._classCode < other._classCode and self._lt(self._itemId, other._itemId)
        return (self._siteCode < other._siteCode
                and self._classCode < other._classCode
                and self._lt(self._itemId, other._itemId))

    def _lt(self, id1, id2):
        if isinstance(id1, str) and id1.isdigit() and isinstance(id2, str) and id2.isdigit():
            return int(id1) < int(id2)
        else:
            return str(id1) < str(id2)

    def __hash__(self):
        return hash((self._siteCode, self._classCode, self._itemId))

    def __str__(self):
        return 'Item(' + str(self._siteCode) + ', ' + str(self._classCode) + ', ' + str(self._itemId) + ')'

    def debug(self):
        return 'Item(' + utils.printable(self._siteCode) + ', ' + utils.printable(self._classCode) + ', ' + utils.printable(self._itemId) + ')'

    def isValid(self):
        return (isinstance(self._siteCode, str) and self._siteCode
                and isinstance(self._classCode, str) and self._classCode
                and isinstance(self._itemId, str) and self._itemId)

    def isInvalid(self):
        return (not isinstance(self._siteCode, str) or self._siteCode == ''
                or not isinstance(self._classCode, str) or self._classCode == ''
                or not isinstance(self._itemId, str) or self._itemId == '')

    def isNull(self):
        return (self._siteCode == '' and self._classCode == '' and self._itemId == '')

    def isItemRange(self):
        return isinstance(self._itemId, str) and (self._itemId.contains('-') or self._itemId.contains(' '))

    def label(self):
        if self._classCode:
            return Config.classCodes[self._classCode]['label'] + ' ' + self._itemId
        return ''

    def name(self):
        return self._classCode + '_' + self._siteCode + '_' + self._itemId

    def itemValue(self):
        return self._siteCode + '_' + self._itemId

    def setItem(self, siteCode, classCode, itemId):
        if siteCode and classCode and itemId:
            self.setSiteCode(siteCode)
            self.setClassCode(classCode)
            self.setItemId(itemId)
        else:
            self._siteCode = ''
            self._classCode = ''
            self._itemId = ''

    def siteCode(self):
        return self._siteCode

    def setSiteCode(self, siteCode):
        self._siteCode = utils.string(siteCode)

    def classCode(self):
        return self._classCode

    def setClassCode(self, classCode):
        self._classCode = utils.string(classCode)

    def itemId(self):
        return self._itemId

    def setItemId(self, itemId):
        if isinstance(itemId, list) or isinstance(itemId, set):
            self._itemId = utils.listToRange(itemId)
        else:
            self._itemId = utils.string(itemId)

    def setFromArkItem(self, itemKey, itemValue):
        try:
            keyParts = itemKey.split('_')
            valParts = itemValue.split('_')
            siteCode = valParts[0]
            classCode = keyParts[0]
            itemId = valParts[1]
            self.setItem(siteCode, classCode, itemId)
        except:
            pass

    def attributes(self):
        attrs = {}
        attrs['site'] = utils.strip(self._siteCode)
        attrs['class'] = utils.strip(self._classCode)
        attrs['id'] = utils.strip(self._itemId)
        return attrs

    def setAttributes(self, attributes):
        if 'site' in attributes:
            self.setSiteCode(attributes['site'])
        if 'class' in attributes:
            self.setSiteCode(attributes['class'])
        if 'id' in attributes:
            self.setSiteCode(attributes['id'])

    def toCsv(self):
        return utils.doublequote(self._siteCode) + ',' + utils.doublequote(self._classCode) + ',' + utils.doublequote(self._itemId)

    def toList(self):
        lst = []
        for itemId in self.itemIdList():
            lst.append(Item(self._siteCode, self._classCode, itemId))
        return lst

    def addItemId(self, itemId):
        if self._itemId == '':
            self.setItemId(itemId)
        else:
            lst = self.itemIdList()
            if isinstance(itemId, list) or isinstance(itemId, set):
                lst.extend(itemId)
            else:
                lst.append(utils.string(itemId))
            self.setItemId(lst)

    def itemIdList(self):
        return utils.rangeToList(self._itemId)

    def filterClause(self):
        if self.isInvalid():
            return ''
        clause = '("site" = \'' + self._siteCode + '\'' + ' and "class" = \'' + self._classCode + '\''
        subs = self._itemId.split()
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
            if sub.find('-') >= 0:
                vals = sub.split('-')
                clause = clause + ' ("id" >= ' + vals[0] + ' and "id" <= ' + vals[1] + ')'
            else:
                clause = clause + '"id" = ' + sub
        clause += '))'
        return clause

    def featureRequest(self):
        request = QgsFeatureRequest()
        request.setFilterExpression(self.filterClause())
        return request
