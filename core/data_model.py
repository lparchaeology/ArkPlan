# -*- coding: utf-8 -*-
"""
/***************************************************************************
                                      Ark
                                 A QGIS plugin
             QGIS Plugin for ARK, the Archaeological Recording Kit
                             -------------------
        begin                : 2015-02-28
        git sha              : $Format:%H$
        copyright            : (C) 2014 by John Layt
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

from PyQt4.QtCore import Qt, QObject, QAbstractTableModel, QVariant, QModelIndex, QDir

from ..core.settings import Settings

class TableModel(QAbstractTableModel):

    _table = []
    _fields = []
    _nullRecord = {}

    def __init__(self, parent=None):
        super(QAbstractTableModel, self).__init__(parent)

    def rowCount(self, parent):
        return len(self._table)

    def columnCount(self, parent):
        return len(self._fields)

    def data(self, index, role):
        if (not index.isValid() or index.row() < 0 or index.row() > len(self._table) or role != Qt.DisplayRole):
            return self._nullRecord[self._fields[index.column()]]
        record = self._table[index.row()]
        data = record[self._fields[index.column()]]
        return data

    def headerData(self, section, orientation, role):
        if (role == Qt.DisplayRole and orientation == Qt.Horizontal):
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

    def clear(self):
        self._table = []


class ContextGroupingModel(TableModel):

    def __init__(self, parent=None):
        self._fields = ['context_no', 'sub_group_no', 'group_no']
        self._nullRecord = {'context_no' : 0, 'sub_group_no' : 0, 'group_no' : 0}
        super(TableModel, self).__init__(parent)

    def addGrouping(self, context_no, sub_group_no, group_no):
        record = {'context_no' : context_no, 'sub_group_no' : sub_group_no, 'group_no' : group_no}
        self._table.append(record)

    def updateGrouping(self, context_no, sub_group_no, group_no, insertOnFail=False):
        record = self.getRecord('context_no', context_no)
        if record:
            record['sub_group_no'] = sub_group_no
        elif insertOnFail:
            self.addGrouping({'context_no' : context_no, 'group_no' : group_no, 'sub_group_no' : sub_group_no})

    def updateSubGroup(self, context_no, sub_group_no, insertOnFail=False):
        record = self.getRecord('context_no', context_no)
        if record:
            record['sub_group_no'] = sub_group_no
        elif insertOnFail:
            self.addGrouping({'context_no' : context_no, 'sub_group_no' : sub_group_no, 'group_no' : 0})

    def updateGroup(self, context_no, group_no, insertOnFail=False):
        record = self.getRecord('context_no', context_no)
        if record:
            record['group_no'] = group_no
        elif insertOnFail:
            self.addGrouping({'context_no' : context_no, 'sub_group_no' : 0, 'group_no' : group_no})

    def getContextsForSubGroup(self, sub_group_no):
        contexts = []
        for record in self._table:
            if record['sub_group_no'] == sub_group_no:
                contexts.append(record['context_no'])
        return contexts

    def getContextsForGroup(self, group_no):
        contexts = []
        for record in self._table:
            if record['group_no'] == group_no:
                contexts.append(record['context_no'])
        return contexts


class ContextModel(TableModel):

    def __init__(self, parent=None):
        super(TableModel, self).__init__(parent)
        self._fields = ['context_no', 'context', 'context_type', 'short_description', 'issued_to', 'issued_on']
        self._nullRecord = {'context_no' : 0, 'context' : '', 'context_type' : '', 'short_description' : '', 'issued_to' : '', 'issued_on' : ''}

    def addContext(self, arkRecord):
        context = arkRecord['context']
        context_no = int(context.split('_')[-1])
        record = {}
        record.update(self._nullRecord)
        record.update(arkRecord)
        record.update({'context_no' : context_no})
        self._table.append(record)


class SubGroupModel(TableModel):

    def __init__(self, parent=None):
        super(TableModel, self).__init__(parent)
        self._fields = ['sub_group_no', 'sub_group', 'basic_interp', 'short_description', 'context', 'subgroup_narrative', 'dating_narrative']
        self._nullRecord = {'sub_group_no' : 0, 'sub_group' : '', 'basic_interp' : '', 'short_description' : '', 'context' : '', 'subgroup_narrative' : '', 'dating_narrative' : ''}

    def addSubGroup(self, arkRecord):
        subGroup = arkRecord['sub_group']
        sub_group_no = int(subGroup.split('_')[-1])
        # TODO Fix up contexts
        record = {}
        record.update(self._nullRecord)
        record.update(arkRecord)
        record.update({'sub_group_no' : sub_group_no})
        self._table.append(record)


class GroupModel(TableModel):

    def __init__(self, parent=None):
        super(TableModel, self).__init__(parent)
        self._fields = ['strat_group_no', 'strat_group', 'short_description', 'sub_group']
        self._nullRecord = {'strat_group_no' : 0, 'strat_group' : '', 'short_description' : '', 'sub_group' : ''}

    def addGroup(self, arkRecord):
        group = arkRecord['strat_group']
        group_no = int(group.split('_')[-1])
        # TODO Fix up contexts
        record = {}
        record.update(self._nullRecord)
        record.update(arkRecord)
        record.update({'strat_group_no' : group_no})
        self._table.append(record)


class DataManager(QObject):


    _arkGroupDataFilename = 'PCO06_ark_groups.csv'
    _arkSubGroupDataFilename = 'PCO06_ark_subgroups.csv'
    _arkContextDataFilename = 'PCO06_ark_contexts.csv'

    _contextGroupingModel = ContextGroupingModel()
    _contextModel = ContextModel()
    _subGroupModel = SubGroupModel()
    _groupModel = GroupModel()


    def __init__(self, settings):
        super(DataManager, self).__init__()
        self.settings = settings


    def loadData(self):
        self._contextGroupingModel.clear()
        self._contextModel.clear()
        self._subGroupModel.clear()
        self._groupModel.clear()
        subToGroup = {}
        subToGroup[0] = 0
        with open(self.settings.dataPath() + '/' + self._arkGroupDataFilename) as csvFile:
            reader = csv.DictReader(csvFile)
            for record in reader:
                pass
                self._groupModel.addGroup(record)
        with open(self.settings.dataPath() + '/' + self._arkSubGroupDataFilename) as csvFile:
            reader = csv.DictReader(csvFile)
            for record in reader:
                sub_group_string = record['sub_group']
                sub_group_no = int(sub_group_string.split('_')[-1])
                group_string = record['strat_group']
                group_no = 0
                if group_string:
                    group_no = int(group_string.split('_')[-1])
                subToGroup[sub_group_no] = group_no
                self._subGroupModel.addSubGroup(record)
        with open(self.settings.dataPath() + '/' + self._arkContextDataFilename) as csvFile:
            reader = csv.DictReader(csvFile)
            for record in reader:
                context_string = record['context']
                context_no = int(context_string.split('_')[-1])
                sub_group_string = record['sub_group']
                sub_group_no = 0
                if sub_group_string:
                    sub_group_no = int(sub_group_string.split('_')[-1])
                self._contextGroupingModel.addGrouping(context_no, sub_group_no, subToGroup[sub_group_no])
                self._contextModel.addContext(record)


    def getContextsForSubGroup(self, sub_group_no):
        return _contextGroupingModel.getContextsForSubGroup()


    def getContextsForGroup(self, group_no):
        return _contextGroupingModel.getContextsForGroup()
