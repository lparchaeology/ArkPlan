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

from qgis.core import NULL, QgsCredentials

from ..libarkqgis.models import TableModel, ParentChildModel

from ..pyARK.ark import Ark

from plan_item import ItemKey
from credentials_dialog import CredentialsDialog

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
                    key = ItemKey(record[keyFields.siteCode], record[keyFields.classCode], record[keyFields.itemId])
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

    _ark = None

    itemKeys = {} # {classCode: [ItemKey]

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
        filePath = path + 'cxt.csv'
        self._cxtModel = ItemModel(filePath, keyFields, self)
        project.logMessage('Loaded Context Model : ' + filePath + ' : ' + str(self._cxtModel.rowCount()) + ' rows')
        self._cxtProxyModel.setSourceModel(self._cxtModel)
        if self._subModel:
            self._subModel.clear()
        filePath = path + 'sgr.csv'
        self._subModel = ItemModel(filePath, keyFields, self)
        project.logMessage('Loaded Subgroup Model : ' + filePath + ' : ' + str(self._subModel.rowCount()) + ' rows')
        self._subProxyModel.setSourceModel(self._subModel)
        if self._grpModel:
            self._grpModel.clear()
        filePath = path + 'grp.csv'
        self._grpModel = ItemModel(filePath, keyFields, self)
        project.logMessage('Loaded Group Model : ' + filePath + ' : ' + str(self._grpModel.rowCount()) + ' rows')
        self._grpProxyModel.setSourceModel(self._grpModel)
        self._linkModel = ParentChildModel(self)
        self._addLinks(self._subModel._table)
        self._addLinks(self._grpModel._table)
        project.logMessage('Loaded Link Model : ' + str(self._linkModel.rowCount()) + ' rows')

    def _createArkSession(self, project):
        if self._ark is None:
            dialog = CredentialsDialog()
            if dialog.exec_():
                self._ark = Ark(project.arkUrl(), dialog.username(), dialog.password())

    def loadAllItems(self, project):
        if not project.arkUrl():
            return
        self.itemKeys = {}
        for classCode in project.plan.uniqueValues(project.fieldName('class')):
            if classCode is not None and classCode != NULL:
                self.loadClassItems(project, classCode)
        self._ark = None

    def loadClassItems(self, project, classCode):
        if not project.arkUrl():
            return
        self._createArkSession(project)
        if self._ark is None:
            return
        response = self._ark.getItems(classCode + '_cd')
        if response.error:
            project.logMessage(response.url)
            project.logMessage(response.message)
            project.logMessage(response.raw)
            self.itemKeys[classCode] = []
        else:
            project.logMessage(classCode + ' = ' + response.url)
            lst = response.data[classCode]
            keys = set()
            for record in lst:
                key = ItemKey(record['ste_cd'], classCode, record[classCode + '_no'])
                keys.add(key)
            self.itemKeys[classCode] = sorted(keys)
            project.logMessage('Items = ' + str(len(self.itemKeys[classCode])))

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
