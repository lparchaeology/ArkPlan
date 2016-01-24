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

from PyQt4.QtCore import Qt, QObject, QAbstractTableModel, QVariant, QModelIndex, QFile
from PyQt4.QtGui import QSortFilterProxyModel

class TableModel(QAbstractTableModel):

    _table = []
    _fields = []
    _nullRecord = {}

    def __init__(self, fields=[], nullRecord={}, parent=None):
        super(QAbstractTableModel, self).__init__(parent)
        self._fields = fields
        self._nullRecord = nullRecord
        self._table = []

    def rowCount(self):
        return len(self._table)

    def columnCount(self):
        return len(self._fields)

    def data(self, index, role):
        if (role != Qt.DisplayRole):
            return None
        if (not index.isValid() or index.row() < 0 or index.row() > len(self._table)):
            return self._nullRecord[self._fields[index.column()]]
        record = self._table[index.row()]
        data = record[self._fields[index.column()]]
        return data

    def headerData(self, section, orientation, role):
        if (role != Qt.DisplayRole):
            return None
        if (orientation == Qt.Horizontal):
            return self._fields[section]
        return ''

    def insertRows(self, position, rows, parent=QModelIndex()):
        beginInsertRows(QModelIndex(), position, position + rows - 1)
        for row in range(0, rows - 1):
            self._table.insert(position, self._nullRecord)
        endInsertRows()
        return True

    def removeRows(self, position, rows, parent=QModelIndex()):
        beginRemoveRows(QModelIndex(), position, position + rows - 1)
        for row in range(position + rows - 1, position):
            del self._table[row]
        endRemoveRows()
        return true

    def setData(self, index, value, role=Qt.EditRole):
        if (not index.isValid() or role != Qt.EditRole):
            return False
        record = self._table[index.row()]
        record[self._fields[index.column()]] = value
        return True

    def flags(self, index):
        if not index.isValid():
            return Qt.ItemIsEnabled
        return super(QAbstractTableModel, self).flags(index) | Qt.ItemIsEditable

    def getList(self):
        return self._table

    def getRecord(self, key, value):
        for record in self._table:
            if record[key] == value:
                return record

    def getRecords(self, key, value):
        results = []
        for record in self._table:
            if record[key] == value:
                results.append(record)
        return results

    def deleteRecords(self, key, value):
        for record in self._table:
            if record[key] == value:
                self._table.remove(record)

    def clear(self):
        self._table = []


class ParentChildModel(TableModel):

    def __init__(self, parent=None):
        super(TableModel, self).__init__(parent)
        self._fields = ['parent', 'child']
        self._nullRecord = {'parent' : None, 'child' : None}

    def addChild(self, parent, child):
        self.deleteRecords('child', child)
        record = {'parent' : parent, 'child' : child}
        self._table.append(record)

    def getChildren(self, parent):
        children = []
        for record in self._table:
            if record['parent'] == parent:
                children.append(record['child'])
        return children

    def getParent(self, child):
        for record in self._table:
            if record['child'] == child:
                return record['parent']
        return None

class ItemKey():
    siteCode = ''
    classCode = ''
    itemId = ''

    def __init__(self, siteCode=None, classCode=None, itemId=None):
        self.siteCode = siteCode
        self.classCode = classCode
        self.itemId = itemId

    def __eq__(self, other):
        return self.siteCode == self.siteCode and self.classCode == other.classCode and self.itemId == other.itemId

    def __ne__(self, other):
        return self.siteCode != self.siteCode or self.classCode != other.classCode or self.itemId != other.itemId

    def isValid(self):
        return siteCode and  classCode and itemId

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

    _cxtModel = None  # ContextModel()
    _cxtProxyModel = QSortFilterProxyModel()
    _subModel = None  # SubGroupModel()
    _subProxyModel = QSortFilterProxyModel()
    _grpModel = None  # GroupModel()
    _grpProxyModel = QSortFilterProxyModel()
    _linkModel = None  # ParentChildModel()

    def __init__(self):
        super(DataManager, self).__init__()

    def hasData(self):
        return self._cxtModel.rowCount() > 0 or self._subModel.rowCount() > 0 or self._grpModel.rowCount() > 0

    def hasClassData(self, classCode):
        if classCode == 'cxt':
            return self._cxtModel.rowCount() > 0
        elif classCode == 'sgr':
            return self._subModel.rowCount() > 0
        elif classCode == 'grp':
            return self._grpModel.rowCount() > 0
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

    def _addLinks(self, table):
        for record in table:
            parentItem = record['key']
            siteCode = record['ste_cd']
            childModule = record['child_module']
            children = str(record['children']).split()
            for child in children:
                childItem = ItemKey(siteCode, childModule, str(child))
                self._linkModel.addChild(parentItem, childItem)

    def getItem(self, classCode, siteCode, itemId):
        if classCode == 'cxt':
            return self._cxtModel.getItem(ItemKey(str(siteCode), str(classCode), str(itemId)))
        elif classCode == 'sgr':
            return self._subModel.getItem(ItemKey(str(siteCode), str(classCode), str(itemId)))
        elif classCode == 'grp':
            return self._grpModel.getItem(ItemKey(str(siteCode), str(classCode), str(itemId)))
        return {}

    def getChildren(self, siteCode, classCode, itemId):
        return self._linkModel.getChildren(ItemKey(str(siteCode), str(classCode), str(itemId)))

    def getParent(self, siteCode, classCode, itemId):
        return self._linkModel.getParent(ItemKey(str(siteCode), str(classCode), str(itemId)))
