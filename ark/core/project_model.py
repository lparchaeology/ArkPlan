# -*- coding: utf-8 -*-
"""
/***************************************************************************
                                ARKspatial
                    A QGIS plugin for Archaeological Recording.
        Part of the Archaeological Recording Kit by L - P : Archaeology
                        http://ark.lparchaeology.com
                              -------------------
        copyright            : 2018 by L - P : Heritage LLP
        email                : ark@lparchaeology.com
        copyright            : 2018 by John Layt
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

"""
    Port of QgsBrowserModel to Python and simplified for Project Model requirements
"""

from PyQt4.QtCore import Qt, QUrl, QModelIndex, QAbstractItemModel, QMimeData

from qgis.core import QGis, QgsDirectoryItem, QgsDataItem, QgsMimeDataUtils, QgsProject


class ProjectModel(QAbstractItemModel):

    PathRole = Qt.UserRole
    CommentRole = Qt.UserRole + 1

    def __init__(self, initialize, parent=None):
        super(ProjectModel, self).__init__(parent)

        self._initialized = False
        self._rootItems = []  # QVector<QgsDataItem*>
        self._projectHome = None  # QgsDirectoryItem

        if initialize:
            self.init()

    def __del__(self):
        self.removeRootItems()

    def init(self):
        if not self._initialized:
            QgsProject.instance().readProject.connect(self.updateProjectHome)
            QgsProject.instance().writeProject.connect(self.updateProjectHome)
            self.addRootItems()
            self._initialized = True

    def updateProjectHome(self):
        home = QgsProject.instance().homePath()
        if self._projectHome is not None and self._projectHome.path() == home:
            return
        idx = self._rootItems.indexOf(self._projectHome)
        if idx >= 0:
            self.beginRemoveRows(QModelIndex(), idx, idx)
            self._rootItems.remove(idx)
            self.endRemoveRows()
        self._projectHome = None  # delete
        if home:
            self._projectHome = QgsDirectoryItem(None, "Project home", home, "project:" + home)
        if self._projectHome is not None:
            self.connectItem(self._projectHome)
            self.beginInsertRows(QModelIndex(), 0, 0)
            self._rootItems.insert(0, self._projectHome)
            self.endInsertRows()

    def addRootItems(self):
        self.updateProjectHome()

    def removeRootItems(self):
        # for item in self._rootItems:
            # delete item
        self._rootItems.clear()

    def flags(self, index):
        if not index.isValid():
            return Qt.ItemFlags()
        flags = Qt.ItemIsEnabled | Qt.ItemIsSelectable
        ptr = index.internalPointer()
        if ptr.type() == QgsDataItem.Layer or ptr.type() == QgsDataItem.Project:
            flags |= Qt.ItemIsDragEnabled
        if ptr.acceptDrop():
            flags |= Qt.ItemIsDropEnabled
        return flags

    def data(self, index, role):
        if not index.isValid():
            return None
        item = index  # cast QModelIndex to QgsDataItem
        if role == Qt.DisplayRole:
            return item.name()
        if role == Qt.ToolTipRole:
            return item.toolTip()
        if role == ProjectModel.PathRole:
            return item.path()
        if role == Qt.DecorationRole and index.column() == 0:
            return item.icon()
        if role == ProjectModel.PathRole:
            return item.path()
        if role == ProjectModel.CommentRole and item.type() == QgsDataItem.Layer:
            return item.comments()
        return None

    def headerData(self, section, orientation, role):
        if orientation == Qt.Horizontal and role == Qt.DisplayRole:
            return "header"
        return None

    def rowCount(self, parent):
        if parent is None or not parent.isValid():
            return self._rootItems.count()
        return parent.rowCount()

    def hasChildren(self, parent):
        if parent is None or not parent.isValid():
            return True
        return parent.hasChildren()

    def columnCount(self, parent):
        return 1

    def findPath(self, path, matchFlag):
        theIndex = None
        foundChild = True
        while foundChild:
            foundChild = False
            for i in range(0, self.rowCount(theIndex)):
                idx = self.index(i, 0, theIndex)
                itemPath = self.data(idx, self.PathRole)
                if itemPath == path:
                    return idx
                if path.startswith(itemPath + '/'):
                    foundChild = True
                    theIndex = idx
                    break
        if matchFlag == Qt.MatchStartsWith:
            return theIndex
        return QModelIndex()

    def reload(self):
        self.beginResetModel()
        self.removeRootItems()
        self.addRootItems()
        self.endResetModel()

    def reload(self, row, column, parent):
        if column < 0 or column >= self.columnCount() or row < 0:
            return QModelIndex()

        p = self.dataItem(parent)
        items = p.children() if p is not None else self._rootItems
        item = items.value(row, None)
        return self.createIndex(row, column, item) if item else QModelIndex()

    def parent(self, index):
        item = self.dataItem(index)
        if item is None:
            return QModelIndex()
        return self.findItem(item.parent())

    def parent(self, item, parent):
        items = parent.children() if parent is not None else _rootItems
        for i in range(0, items.size()):
            if items[i] == item:
                return self.createIndex(i, 0, item)
            childIndex = self.findItem(item, items[i])
            if childIndex.isValid():
                return childIndex
        return QModelIndex()

    def beginInsertItems(self, parent, first, last):
        idx = self.findItem(parent)
        if not idx.isValid():
            return
        self.beginInsertRows(idx, first, last)

    def beginInsertItems(self):
        self.endInsertRows()

    def beginInsertItems(self, parent, first, last):
        idx = self.findItem(parent)
        if not idx.isValid():
            return
        self.beginRemoveRows(idx, first, last)

    def beginInsertItems(self):
        self.endRemoveRows()

    def itemDataChanged(self, item):
        idx = self.findItem(item)
        if not idx.isValid():
            return
        self.dataChanged(idx, idx).emit()

    def itemStateChanged(self, item, oldState):
        if item is None:
            return
        idx = self.findItem(item)
        if not idx.isValid():
            return
        self.stateChanged(idx, oldState).emit()

    def connectItem(self, item):
        item.beginInsertItems.connect(self.beginInsertItems)
        item.endInsertItems.connect(self.endInsertItems)
        item.beginRemoveItems.connect(self.beginRemoveItems)
        item.endRemoveItems.connect(self.endRemoveItems)
        item.dataChanged.connect(self.itemDataChanged)
        item.stateChanged.connect(self.itemStateChanged)

    def mimeTypes(self):
        return ['application/x-vnd.qgis.qgis.uri']

    def mimeData(self, indexes):
        lst = QgsMimeDataUtils.UriList
        for index in indexes:
            if index.isValid():
                if index.type() == QgsDataItem.Project:
                    mimeData = QMimeData()
                    url = QUrl.fromLocalFile(index.path())
                    mimeData.setUrls([url])
                    return mimeData
                if index.type() == QgsDataItem.Layer:
                    lst.append(QgsMimeDataUtils.Uri(index))
        return QgsMimeDataUtils.encodeUriList(lst)

    def dropMimeData(self, data, action, row, column, parent):
        destItem = self.dataItem(parent)
        if destItem is None:
            return false
        return destItem.handleDrop(data, action)

    def dataItem(self, idx):
        return idx.internalPointer()

    def canFetchMore(self, parent):
        item = self.dataItem(parent)
        return item is not None and item.state() == QgsDataItem.NotPopulated

    def fetchMore(self, parent):
        item = self.dataItem(parent)
        if item is None or item.state() == QgsDataItem.Populating or item.state() == QgsDataItem.Populated:
            return
        item.populate()

    def fetchMore(self, path):
        index = self.findPath(path)
        self.refresh(index)

    def refresh(self, theIndex):
        item = self.dataItem(theIndex)
        if item is None or item.state() == QgsDataItem.Populating:
            return
        item.refresh()
