# -*- coding: utf-8 -*-
"""
/***************************************************************************
                                ARK Spatial
                    A QGIS plugin for Archaeological Recording.
        Part of the Archaeological Recording Kit by L-P : Archaeology
                        http://ark.lparchaeology.com
                              -------------------
        begin                : 2016-03-11
        git sha              : $Format:%H$
        copyright            : 2016 by L-P : Heritage LLP
        email                : ark@lparchaeology.com
        copyright            : 2016 by John Layt
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

import csv, json, urllib2

from PyQt4.QtCore import Qt, QObject, QSettings, QFile, pyqtSignal
from PyQt4.QtGui import QAction, QIcon, QSortFilterProxyModel

from qgis.core import NULL, QgsCredentials

from ..libarkqgis import utils
from ..libarkqgis.models import TableModel, ParentChildModel

from ..pyARK.ark import Ark

from data_dock import DataDock
from config import Config
from plan_item import ItemKey
from credentials_dialog import CredentialsDialog

import resources

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

class Data(QObject):

    project = None # Project()

    # Internal variables
    dock = None # DataDock()

    _cxtModel = None  # ItemModel()
    _cxtProxyModel = QSortFilterProxyModel()
    _subModel = None  # ItemModel()
    _subProxyModel = QSortFilterProxyModel()
    _grpModel = None  # ItemModel()
    _grpProxyModel = QSortFilterProxyModel()
    _linkModel = None  # ParentChildModel()

    _ark = None

    itemKeys = {} # {classCode: [ItemKey]

    def __init__(self, project):
        super(Data, self).__init__(project)
        self.project = project

    # Standard Dock methods

    # Create the gui when the plugin is first created
    def initGui(self):
        self.dock = DataDock(self.project.layerDock)
        action = self.project.addDockAction(':/plugins/ark/data/data.svg', self.tr(u'Query Item Data'), callback=self.run, checkable=True)
        self.dock.initGui(self.project.iface, Qt.LeftDockWidgetArea, action)

        self.dock.loadDataSelected.connect(self._loadDataSelected)
        self.dock.firstItemSelected.connect(self._firstItemSelected)
        self.dock.prevItemSelected.connect(self._prevItemSelected)
        self.dock.openItemData.connect(self._openItemData)
        self.dock.nextItemSelected.connect(self._nextItemSelected)
        self.dock.lastItemSelected.connect(self._lastItemSelected)
        self.dock.zoomItemSelected.connect(self._zoomItemSelected)
        self.dock.filterItemSelected.connect(self._filterItemSelected)
        self.dock.loadDrawingsSelected.connect(self._loadDrawingsSelected)

    # Load the project settings when project is loaded
    def loadProject(self):
        # Load the Site Codes
        self.dock.initSiteCodes(self.project.siteCodes())
        return True

    # Save the project
    def writeProject(self):
        pass

    # Close the project
    def closeProject(self):
        pass

    # Unload the gui when the plugin is unloaded
    def unloadGui(self):
        self.dock.unloadGui()

    def run(self, checked):
        pass

    def showDock(self, show=True):
        self.dock.menuAction().setChecked(show)

    # Data methods

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

    def _loadData(self):
        keyFields = ItemKey(self.project.fieldName('site'), self.project.fieldName('class'), self.project.fieldName('id'))
        path = self.project.projectPath() + '/data/' + self.project.siteCode() + '_'
        if self._cxtModel:
            self._cxtModel.clear()
        filePath = path + 'cxt.csv'
        self._cxtModel = ItemModel(filePath, keyFields, self)
        self.project.logMessage('Loaded Context Model : ' + filePath + ' : ' + str(self._cxtModel.rowCount()) + ' rows')
        self._cxtProxyModel.setSourceModel(self._cxtModel)
        if self._subModel:
            self._subModel.clear()
        filePath = path + 'sgr.csv'
        self._subModel = ItemModel(filePath, keyFields, self)
        self.project.logMessage('Loaded Subgroup Model : ' + filePath + ' : ' + str(self._subModel.rowCount()) + ' rows')
        self._subProxyModel.setSourceModel(self._subModel)
        if self._grpModel:
            self._grpModel.clear()
        filePath = path + 'grp.csv'
        self._grpModel = ItemModel(filePath, keyFields, self)
        self.project.logMessage('Loaded Group Model : ' + filePath + ' : ' + str(self._grpModel.rowCount()) + ' rows')
        self._grpProxyModel.setSourceModel(self._grpModel)
        self._linkModel = ParentChildModel(self)
        self._addLinks(self._subModel._table)
        self._addLinks(self._grpModel._table)
        self.project.logMessage('Loaded Link Model : ' + str(self._linkModel.rowCount()) + ' rows')

    def _createArkSession(self):
        if self._ark is None:
            dialog = CredentialsDialog()
            if dialog.exec_():
                self._ark = Ark(self.project.arkUrl(), dialog.username(), dialog.password())

    def loadAllItems(self):
        if not self.project.arkUrl():
            return
        self.itemKeys = {}
        for classCode in self.project.plan.uniqueValues(self.project.fieldName('class')):
            if classCode is not None and classCode != NULL:
                self.loadClassItems(classCode)

    def loadClassItems(self, classCode):
        if not self.project.arkUrl():
            return
        self._createArkSession()
        if self._ark is None:
            return
        response = self._ark.getItems(classCode + '_cd')
        if response.error:
            self.project.logMessage(response.url)
            self.project.logMessage(response.message)
            self.project.logMessage(response.raw)
            self.itemKeys[classCode] = []
        else:
            self.project.logMessage(classCode + ' = ' + response.url)
            lst = response.data[classCode]
            keys = set()
            for record in lst:
                key = ItemKey(record['ste_cd'], classCode, record[classCode + '_no'])
                keys.add(key)
            self.itemKeys[classCode] = sorted(keys)
            self.project.logMessage('Items = ' + str(len(self.itemKeys[classCode])))

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

    def getParent(self, itemKey):
        return self._linkModel.getParent(itemKey)

    def getItemFields(self, itemKey, fields):
        if self._ark is None or itemKey is None or itemKey.isInvalid():
            utils.logMessage('none')
            return {}
        response = self._ark.getFields(itemKey.classCode + '_cd', itemKey.itemValue(), fields)
        if response.error:
            utils.logMessage(response.url)
            utils.logMessage(response.message)
            utils.logMessage(response.raw)
        return response.data

    def _loadDataSelected(self):
        pass

    def _firstItemSelected(self):
        pass

    def _prevItemSelected(self):
        pass

    def _openItemData(self):
        pass

    def _nextItemSelected(self):
        pass

    def _lastItemSelected(self):
        pass

    def _zoomItemSelected(self):
        pass

    def _filterItemSelected(self):
        pass

    def _loadDrawingsSelected(self):
        pass
