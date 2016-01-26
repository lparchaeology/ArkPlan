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
        copyright            : 2014, 2015 by L-P : Heritage LLP
        email                : ark@lparchaeology.com
        copyright            : 2014, 2015 by John Layt
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

from qgis.core import QgsField, QgsFeatureRequest

from ..libarkqgis import utils

from config import Config

class ItemKey():
    siteCode = ''
    classCode = ''
    itemId = ''

    def __init__(self, siteCode=None, classCode=None, itemId=None):
        self.setKey(siteCode, classCode, itemId)

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
            self.siteCode = str(siteCode).strip()
            self.classCode = str(classCode).strip()
            self.setItemId(itemId)
        else:
            self.siteCode = ''
            self.classCode = ''
            self.itemId = ''

    def setItemId(self, itemId):
        if type(itemId) == list or type(itemId) == set:
            self.itemId = utils.listToRange(itemId)
        else:
            self.itemId = str(itemId).strip()

    def addItemId(self, itemId):
        if self.itemId == '':
            self.setItemId(itemId)
        else:
            lst = self.itemIdList()
            if type(itemId) == list or type(itemId) == set:
                lst.extend(itemId)
            else:
                lst.append(str(itemId).strip())
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
