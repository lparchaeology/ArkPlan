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

import csv, json, urllib2, bisect, webbrowser

from PyQt4.QtCore import Qt, QObject, QSettings, QFile, pyqtSignal
from PyQt4.QtGui import QApplication, QAction, QIcon, QSortFilterProxyModel
from PyQt4.QtWebKit import QWebView

from qgis.core import NULL, QgsCredentials

from ..libarkqgis import utils
from ..libarkqgis.models import TableModel, ParentChildModel

from ..pyARK.ark import Ark

from enum import *
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

    dataLoaded = pyqtSignal()

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
    _dataLoaded = False
    _prevItem = ItemKey()

    _mapAction = MapAction.MoveMap
    _filterAction = FilterAction.ExclusiveHighlightFilter
    _drawingAction = DrawingAction.NoDrawingAction

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

        self.dock.itemChanged.connect(self._itemChanged)

        self.dock.loadDataSelected.connect(self.loadData)
        self.dock.refreshDataSelected.connect(self.refreshData)
        self.dock.firstItemSelected.connect(self._firstItemSelected)
        self.dock.prevItemSelected.connect(self._prevItemSelected)
        self.dock.openItemData.connect(self._openItemData)
        self.dock.nextItemSelected.connect(self._nextItemSelected)
        self.dock.lastItemSelected.connect(self._lastItemSelected)

        self.dock.showItemSelected.connect(self._showItemSelected)
        self.dock.zoomItemSelected.connect(self._zoomItemSelected)
        self.dock.filterItemSelected.connect(self._filterItemSelected)
        self.dock.editItemSelected.connect(self._editItemSelected)
        self.dock.loadDrawingsSelected.connect(self._loadDrawingsSelected)
        self.dock.itemLinkClicked.connect(self._itemLinkClicked)

        self.dock.mapActionChanged.connect(self._mapActionChanged)
        self.dock.filterActionChanged.connect(self._filterActionChanged)
        self.dock.drawingActionChanged.connect(self._drawingActionChanged)

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

    def _loadCsvData(self):
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
        dialog = CredentialsDialog()
        if dialog.exec_():
            self._ark = Ark(self.project.arkUrl(), dialog.username(), dialog.password())
            self.dock.setItemNavEnabled(True)

    def loadAllItems(self):
        if not self.project.arkUrl():
            return
        self.itemKeys = {}
        for classCode in Config.classCodes.keys():
            if classCode is not None and classCode != NULL:
                self.loadClassItems(classCode)

    def loadClassItems(self, classCode):
        self.itemKeys[classCode] = []
        if not self._loadClassItemsArk(classCode):
            self._loadClassItemsCsv(classCode)

    def _loadClassItemsArk(self, classCode):
        if not self.project.arkUrl():
            return False
        if self._ark is None:
            self._createArkSession()
        if self._ark is None:
            return False
        response = self._ark.getItems(classCode + '_cd')
        if response.error:
            self.project.logMessage(response.url)
            self.project.logMessage(response.message)
            self.project.logMessage(response.raw)
        else:
            self.project.logMessage(classCode + ' = ' + response.url)
            lst = response.data[classCode]
            keys = set()
            for record in lst:
                key = ItemKey(record['ste_cd'], classCode, record[classCode + '_no'])
                if key.isValid():
                    keys.add(key)
            self.itemKeys[classCode] = sorted(keys)
            self.project.logMessage('Items = ' + str(len(self.itemKeys[classCode])))
            if (len(self.itemKeys[classCode]) > 0):
                self._dataLoaded = True
                return True
        return False

    def _loadClassItemsCsv(self, classCode):
        filePath = self.project.projectPath() + '/data/' + self.project.siteCode() + '_' + classCode + '.csv'
        if QFile.exists(filePath):
            with open(filePath) as csvFile:
                keyFields = ItemKey(self.project.fieldName('site'), self.project.fieldName('class'), self.project.fieldName('id'))
                keys = set()
                reader = csv.DictReader(csvFile)
                fields = reader.fieldnames
                for record in reader:
                    key = ItemKey(record[keyFields.siteCode], record[keyFields.classCode], record[keyFields.itemId])
                    keys.add(key)
            self.itemKeys[classCode] = sorted(keys)
            if len(self.itemKeys[classCode]) > 0:
                self._dataLoaded = True
            self.project.logMessage('Items = ' + str(len(self.itemKeys[classCode])))

    def haveItem(self, itemKey):
        try:
            return itemKey in self.project.data.itemKeys[itemKey.classCode]
        except:
            return False

    def firstItem(self, classCode):
        try:
            return self.itemKeys[classCode][0]
        except:
            return ItemKey()

    def lastItem(self, classCode):
        try:
            return self.itemKeys[classCode][-1]
        except:
            return ItemKey()

    def prevItem(self, itemKey):
        idx = -1
        try:
            if itemKey.isValid():
                idx = bisect.bisect_left(self.itemKeys[itemKey.classCode], itemKey) - 1
            if idx >= 0 and idx < len(self.itemKeys[itemKey.classCode]) - 1:
                return self.itemKeys[itemKey.classCode][idx]
        except:
            pass
        return ItemKey()

    def nextItem(self, itemKey):
        idx = -1
        if itemKey.isValid():
            idx = bisect.bisect(self.itemKeys[itemKey.classCode], itemKey)
        if idx >= 0 and idx < len(self.itemKeys[itemKey.classCode]) - 1:
            return self.itemKeys[itemKey.classCode][idx]
        return ItemKey()

    def openItem(self, itemKey):
        if not self.project.useArkDB() or not self.project.arkUrl():
            self.project.showWarningMessage('ARK link not configured, please set the ARK URL in Settings.')
        elif not self.haveItem(itemKey):
            self.project.showWarningMessage('Item not in ARK.')
        else:
            mod_cd = itemKey.classCode + '_cd'
            item_cd = itemKey.siteCode + '_' + itemKey.itemId
            url = self.project.arkUrl() + '/micro_view.php?item_key=' + mod_cd + '&' + mod_cd + '=' + item_cd
            try:
                webbrowser.get().open_new_tab(url)
            except:
                QApplication.clipboard().setText(url)
                self.project.showWarningMessage('Unable to open browser, ARK link has been copied to the clipboard')

    def linkedItems(self, itemKey, linkClassCode):
        xmi = unicode('conf_field_' + itemKey.classCode + linkClassCode + 'xmi')
        data = self.getItemFields(itemKey, [xmi])
        items = []
        try:
            for link in data[xmi]:
                utils.logMessage(str(link))
                itemkey = link[u'xmi_itemkey']
                itemvalue = link[u'xmi_itemvalue'].split(u'_')
                item = ItemKey(itemvalue[0], itemkey[:3], itemvalue[1])
                items.append(item)
        except:
            return []
        return items

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

    def getChildren(self, itemKey, childClassCode):
        children = self.linkedItems(itemKey, childClassCode)
        utils.logMessage(str(children))
        if len(children) > 0:
            return children
        return self._linkModel.getChildren(itemKey)

    def getParent(self, itemKey):
        return self._linkModel.getParent(itemKey)

    def getItemFields(self, itemKey, fields):
        if self._ark is None or itemKey is None or itemKey.isInvalid():
            return {}
        response = self._ark.getFields(itemKey.classCode + '_cd', itemKey.itemValue(), fields)
        if response.error:
            utils.logMessage(response.url)
            utils.logMessage(response.message)
            utils.logMessage(response.raw)
        else:
            self.project.logMessage(str(response.url))
            self.project.logMessage(str(response.data))
        return response.data

    def getItemSubform(self, itemKey, subform):
        if self._ark is None or itemKey is None or itemKey.isInvalid():
            return {}
        if response.error:
            utils.logMessage(response.url)
            utils.logMessage(response.message)
            utils.logMessage(response.raw)
        else:
            self.project.logMessage(str(response.url))
            self.project.logMessage(str(response.data))
        return response.url

    def loadData(self):
        self._ark = None
        self.refreshData()

    def refreshData(self):
        self._dataLoaded = False
        self._loadCsvData()
        self.loadAllItems()
        if self._dataLoaded:
            self.dataLoaded.emit()

    def showItemData(self, item, mapAction=MapAction.NoMapAction, filterAction=FilterAction.NoFilterAction, drawingAction=DrawingAction.NoDrawingAction):
        self.dock.setItem(item)
        self._showItem(item)
        self.project.planModule.applyItemActions(item, mapAction, filterAction, drawingAction)

    def _itemChanged(self):
        item = self.dock.item()
        if self._prevItem == item:
            return
        self._showItem(item)
        self.project.planModule.applyItemActions(item, self._mapAction, self._filterAction, self._drawingAction)

    def _showItem(self, item):
        self._prevItem = item
        url = ''
        if item.isValid() and self.haveItem(item):
            url = self._ark.transcludeSubformUrl(item.classCode + '_cd', item.itemValue(), item.classCode + '_apisum')
        self.dock.setItemUrl(url)

    def _value(self, value):
        if value == False:
            return ''
        if isinstance(value, list):
            return self._value(value[-1])
        if isinstance(value, dict):
            try:
                return value[u'current']
            except:
                return ''
        return value

    def _firstItemSelected(self):
        self.dock.setItem(self.firstItem(self.dock.classCode()))
        self._itemChanged()

    def _prevItemSelected(self):
        self.dock.setItem(self.prevItem(self.dock.item()))
        self._itemChanged()

    def _openItemData(self):
        self.project.planModule.openItemInArk(self.dock.item())

    def _nextItemSelected(self):
        self.dock.setItem(self.nextItem(self.dock.item()))
        self._itemChanged()

    def _lastItemSelected(self):
        self.dock.setItem(self.lastItem(self.dock.classCode()))
        self._itemChanged()

    def _showItemSelected(self):
        self.project.planModule.showItem(self.dock.item())

    def _zoomItemSelected(self):
        self.project.planModule.zoomToItem(self.dock.item())

    def _filterItemSelected(self):
        self.project.planModule.filterItem(self.dock.item())

    def _editItemSelected(self):
        self.project.planModule.editInBuffers(self.dock.item())

    def _loadDrawingsSelected(self):
        self.project.planModule.loadSourceDrawings(self.dock.item())

    def _itemLinkClicked(self, url):
        item_key = ''
        item_value = []
        self.project.logMessage(url.toString())
        self.project.logMessage(url.path())
        self.project.logMessage(url.path()[:5])
        if 'download.php' in url.toString():
            #web = QWebView()
            #web.load(url)
            self.project.logMessage('load it')
            self.dock.widget.itemDataView.load(url)
            return
        if url.hasQueryItem('item_key'):
            item_key = url.queryItemValue('item_key')
            item_value = url.queryItemValue(item_key).split('_')
        elif url.hasQueryItem('itemkey'):
            item_key = url.queryItemValue('itemkey')
            item_value = url.queryItemValue(item_key).split('_')
        else:
            parts = url.path().split('/')
            self.project.logMessage(str(parts))
            if len(parts) >= 2:
                item_key = parts[-2]
                item_value = parts[-1].split('_')
        if item_key and len(item_value) == 2:
            item = ItemKey(item_value[0], item_key[:3], item_value[1])
            if self.haveItem(item):
                self.dock.setItem(item)
                self._itemChanged()

    def _mapActionChanged(self, mapAction):
        self._mapAction = mapAction

    def _filterActionChanged(self, filterAction):
        self._filterAction = filterAction

    def _drawingActionChanged(self, drawingAction):
        self._drawingAction = drawingAction
