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

import csv
import json
import urllib2

from PyQt4.QtCore import QObject, QFile
from PyQt4.QtGui import QSortFilterProxyModel

from ..libarkqgis.models import TableModel, ParentChildModel

from plan_item import ItemKey

class ItemModel(TableModel):

    def __init__(self, filePath, keyFields, parent=None):
        super(ItemModel, self).__init__(parent)

        if QFile.exists(filePath):
            with open(filePath) as csvFile:
                reader = csv.DictReader(csvFile)
                self._fields = reader.fieldnames
                self._nullRecord = {}
                for field in self._fields:
                    self._nullRecord[field] = ''
                for record in reader:
                    key = ItemKey()
                    key.siteCode = str(record[keyFields.siteCode])
                    key.classCode = str(record[keyFields.classCode])
                    key.itemId = str(record[keyFields.itemId])
                    self._addItem(key, record)

    def getItem(self, itemKey):
        return self.getRecord('key', itemKey)

    def _addItem(self, key, itemRecord):
        record = {}
        record.update(self._nullRecord)
        record.update({'key' : key})
        record.update(itemRecord)
        self._table.append(record)

class DataManager(QObject):

    _cxtModel = None  # ItemModel()
    _cxtProxyModel = QSortFilterProxyModel()
    _subModel = None  # ItemModel()
    _subProxyModel = QSortFilterProxyModel()
    _grpModel = None  # ItemModel()
    _grpProxyModel = QSortFilterProxyModel()
    _linkModel = None  # ParentChildModel()

    def __init__(self):
        super(DataManager, self).__init__()

    def hasData(self):
        return self.hasClassData('cxt') or self.hasClassData('sgr') or self.hasClassData('grp')

    def hasClassData(self, classCode):
        if classCode == 'cxt':
            return (self._cxtModel is not None and self._cxtModel.rowCount() > 0)
        elif classCode == 'sgr':
            return (self._subModel is not None and self._subModel.rowCount() > 0)
        elif classCode == 'grp':
            return (self._grpModel is not None and self._grpModel.rowCount() > 0)
        return False

    def loadProject(self, project):
        keyFields = ItemKey(project.fieldName('site'), project.fieldName('class'), project.fieldName('id'))
        path = project.projectPath() + '/data/' + project.siteCode() + '_'
        if self._cxtModel:
            self._cxtModel.clear()
        self._cxtModel = ItemModel(path + 'cxt.csv', keyFields, self)
        self._cxtProxyModel.setSourceModel(self._cxtModel)
        if self._subModel:
            self._subModel.clear()
        self._subModel = ItemModel(path + 'sgr.csv', keyFields, self)
        self._subProxyModel.setSourceModel(self._subModel)
        if self._grpModel:
            self._grpModel.clear()
        self._grpModel = ItemModel(path + 'grp.csv', keyFields, self)
        self._grpProxyModel.setSourceModel(self._grpModel)
        self._linkModel = ParentChildModel(self)
        self._addLinks(self._subModel._table)
        self._addLinks(self._grpModel._table)

    def loadItems(self, project, classCode):
        project.logMessage('loadItems: ' + classCode)
        if not project.arkUrl():
            return
        user = 'user'
        password = 'password'
        url = project.arkUrl() + '/api.php?req=getItems&itemkey=' + classCode + '_cd&handle=' + user + '&passwd=' + password
        project.logMessage('Calling: ' + url)
        try:
            response = urllib2.urlopen(url)
            project.logMessage(str(response.geturl()))
            project.logMessage(str(response.getcode()))
            project.logMessage(str(response.info()))
            if response.getcode() == 200:
                project.logMessage(str(response.read()))
                data = json.load(response)
            else:
                project.logMessage('Not 200!')
        except urllib2.HTTPError as e:
            project.logMessage('HTTPError! ' + str(e.code) + ' ' + str(e.reason))
        except urllib2.URLError as e:
            project.logMessage('URLError! ' + str(e.reason))
        except ValueError:
            project.logMessage('ValueError!')

    def _addLinks(self, table):
        for record in table:
            parentItem = record['key']
            siteCode = record['ste_cd']
            childModule = record['child_module']
            children = str(record['children']).split()
            for child in children:
                childItem = ItemKey(siteCode, childModule, child)
                self._linkModel.addChild(parentItem, childItem)

    def getItem(self, itemKey):
        if itemKey is not None and itemKey.isValid() and self.hasClassData(itemKey.classCode):
            if itemKey.classCode == 'cxt':
                return self._cxtModel.getItem(itemKey)
            elif itemKey.classCode == 'sgr':
                return self._subModel.getItem(itemKey)
            elif itemKey.classCode == 'grp':
                return self._grpModel.getItem(itemKey)
        return {}

    def getChildren(self, itemKey):
        return self._linkModel.getChildren(itemKey)

    def getParent(self, siteCode, classCode, itemId):
        return self._linkModel.getParent(itemKey)
