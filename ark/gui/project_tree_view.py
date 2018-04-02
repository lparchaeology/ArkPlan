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
    Port of QgsBrowserTreeView to python and modified for Project use
"""

from PyQt4.QtCore import Qt, QSettings, QModelIndex, QRegExp
from PyQt4.QtGui import QTreeView

from qgis.core import QgsDataItem

from ArkSpatial.ark.core import ProjectModel


class ProjectTreeView(QTreeView):

    def __init__(self, parent):
        super(ProjectTreeView, self).__init__(parent)
        self.mSettingsSection = 'browser'
        self.mExpandPaths = []
        self._projectModel = None  # ProjectModel

    def setProjectModel(self, model):
        self._projectModel = model

    def setModel(self, model):
        super(ProjectTreeView, self).setModel(model)
        self.restoreState()

    def showEvent(self, event):
        if self.model() is not None:
            self.restoreState()
        super(ProjectTreeView, self).showEvent(event)

    def hideEvent(self, event):
        if self.model() is not None:
            self.saveState()
        super(ProjectTreeView, self).hideEvent(event)

    def saveState(self):
        expandedPaths = self.expandedPathsList(QModelIndex())
        QSettings().setValue(self.expandedPathsKey(), expandedPaths)

    def restoreState(self):
        self.mExpandPaths = QSettings().value(self.expandedPathsKey())

        if self.mExpandPaths:
            expandIndexSet = {}  # QSet<QModelIndex>
            for path in self.mExpandPaths:
                expandIndex = ProjectModel.findPath(self.model(), path, Qt.MatchStartsWith)
                if expandIndex.isValid():
                    modelIndex = self.browserModel().findPath(path, Qt.MatchExactly)
                    if modelIndex.isValid():
                        ptr = self.browserModel().dataItem(modelIndex)
                        if ptr is not None and (ptr.capabilities2() & QgsDataItem.Capability.Collapse):
                            parentIndex = self.model().parent(expandIndex)
                            if parentIndex.isValid():
                                expandIndexSet.insert(parentIndex)
                        else:
                            expandIndexSet.insert(expandIndex)

                for expandIndex in expandIndexSet:
                    self.expandTree(expandIndex)
        else:
            index = ProjectModel.findPath(self.model(), "favourites:")
            self.expand(index)

    def expandTree(self, index):
        if self.model() is None:
            return
        self.expand(index)
        parentIndex = self.model().parent(index)
        if parentIndex.isValid():
            self.expandTree(parentIndex)

    def treeExpanded(self, index):
        if self.model() is None:
            return False
        if not self.isExpanded(index):
            return False
        parentIndex = self.model().parent(index)
        if parentIndex.isValid():
            return self.treeExpanded(parentIndex)
        return True

    def hasExpandedDescendant(self, index):
        if self.model() is None:
            return False
        for i in range(0, self.model().rowCount()):
            childIndex = self.model().index(i, 0, index)
            if self.isExpanded(childIndex):
                return True
            if self.hasExpandedDescendant(childIndex):
                return True
        return False

    def rowsInserted(self, parentIndex, start, end):
        super(ProjectTreeView, self).rowsInserted(parentIndex, start, end)
        if self.model() is None:
            return
        if not self.mExpandPaths:
            return
        parentPath = self.model().data(parentIndex, ProjectModel.PathRole)
        self.mExpandPaths.remove(parentPath)
        if not self.treeExpanded(parentIndex):
            for path in self.mExpandPaths:
                if path.startswith(parentPath + '/'):
                    self.mExpandPaths.remove(path)
            return
        for i in range(start, end):
            childIndex = self.model().index(i, 0, parentIndex)
            childPath = self.model().data(childIndex, ProjectModel.PathRole)
            escapedChildPath = childPath
            escapedChildPath.replace('|', "\\|")
            if self.mExpandPaths.contains(childPath) or self.mExpandPaths.indexOf(QRegExp("^" + escapedChildPath + "/.*")) != -1:
                self.expand(childIndex)

    def expandedPathsKey(self):
        return '/' + self.mSettingsSection + "/expandedPaths"

    def expandedPathsList(self, index):
        paths = []
        if self.model() is None:
            return paths
        for i in range(0, self.model().rowCount(index)):
            childIndex = self.model().index(i, 0, index)
            if self.isExpanded(childIndex):
                childrenPaths = self.expandedPathsList(childIndex)
                if childrenPaths:
                    paths.append(childrenPaths)
                else:
                    paths.append(self.model().data(childIndex, ProjectModel.PathRole))
        return paths
