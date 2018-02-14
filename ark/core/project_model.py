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

from PyQt4.QtCore import Qt, QFile, QDir, QApplication, QStyle, QtConcurrentMap, QUrl, QSettings, QModelIndex, QAbstractItemModel

from qgis.core import QGis, QgsApplication, QgsDirectoryItem, QgsDataItem, QgsDataItemProvider, QgsDataItemProviderRegistry, QgsDataProvider, QgsMimeDataUtils, QgsLogger, QgsProviderRegistry, QgsProject, QgsBrowserModel

from ArkSpatial.ark.lib.core import TableModel

from ArkSpatial.ark.core import Item


class ProjectModel(QAbstractItemModel):

    PathRole = Qt.UserRole
    CommentRole = Qt.UserRole + 1

    mInitialized = False
    mRootItems = []  # QVector<QgsDataItem*>
    mProjectHome = None  # QgsDirectoryItem

    def __init__(self, initialize, parent=None):
        super(ProjectModel, self).__init__(parent)
        if initialize:
            self.init()

    def __del__(self):
        self.removeRootItems()

    def init(self):
        if not self.mInitialized:
            QgsProject.instance().readProject.connect(self.updateProjectHome)
            QgsProject.instance().writeProject.connect(self.updateProjectHome)
            self.addRootItems()
            self.mInitialized = True

    def updateProjectHome(self):
        home = QgsProject.instance().homePath()
        if self.mProjectHome is not None and self.mProjectHome.path() == home:
            return
        idx = self.mRootItems.indexOf(self.mProjectHome)
        if idx >= 0:
            self.beginRemoveRows(QModelIndex(), idx, idx)
            self.mRootItems.remove(idx)
            self.endRemoveRows()
        self.mProjectHome = None  # delete
        if home:
            self.mProjectHome = QgsDirectoryItem(None, "Project home", home, "project:" + home)
        if self.mProjectHome is not None:
            self.connectItem(self.mProjectHome)
            self.beginInsertRows(QModelIndex(), 0, 0)
            self.mRootItems.insert(0, self.mProjectHome)
            self.endInsertRows()

    def addRootItems(self):
        self.updateProjectHome()

    def removeRootItems(self):
        # for item in self.mRootItems:
            # delete item
        self.mRootItems.clear()

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
        if role == QgsBrowserModel.PathRole:
            return item.path()
        if role == Qt.DecorationRole and index.column() == 0:
            return item.icon()
        if role == QgsBrowserModel.PathRole:
            return item.path()
        if role == QgsBrowserModel.CommentRole and item.type() == QgsDataItem.Layer:
            return item.comments()
        return None

    def headerData(self, section, orientation, role):
        if orientation == Qt.Horizontal and role == Qt.DisplayRole:
            return "header"
        return None
