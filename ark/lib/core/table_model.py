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

from PyQt4.QtCore import QAbstractTableModel, QModelIndex, Qt


class TableModel(QAbstractTableModel):

    _table = []
    _fields = []
    _nullRecord = {}

    def __init__(self, fields=[], nullRecord={}, parent=None):
        super(QAbstractTableModel, self).__init__(parent)
        self._fields = fields
        self._nullRecord = nullRecord
        self._table = []

    def rowCount(self, parent=None):
        if parent and parent.isValid():
            return 0
        return len(self._table)

    def columnCount(self, parent=None):
        if parent and parent.isValid():
            return 0
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
        self.beginInsertRows(QModelIndex(), position, position + rows - 1)
        for row in range(0, rows - 1):
            self._table.insert(position, self._nullRecord)
        self.endInsertRows()
        return True

    def removeRows(self, position, rows, parent=QModelIndex()):
        self.beginRemoveRows(QModelIndex(), position, position + rows - 1)
        for row in range(position + rows - 1, position):
            del self._table[row]
        self.endRemoveRows()
        return True

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

    def appendRecord(self, record):
        self._table.append(record)
