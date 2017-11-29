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

import bisect
import csv
import webbrowser

from PyQt4.QtCore import QFile, QObject, Qt, pyqtSignal
from PyQt4.QtGui import QApplication, QSortFilterProxyModel

from ArkSpatial.ark.lib import utils
from ArkSpatial.ark.lib.core import ParentChildModel
from ArkSpatial.ark.lib.gui import CredentialsDialog

from ArkSpatial.ark.core import Config, Item, ItemModel
from ArkSpatial.ark.core.enum import DrawingAction, FilterAction, MapAction
from ArkSpatial.ark.gui import DataDock
from ArkSpatial.ark.pyARK import Ark


class DataModule(QObject):

    dataLoaded = pyqtSignal()

    project = None  # Project()

    # Internal variables
    dock = None  # DataDock()

    _classDataModels = {}  # {classCode: ItemModel()}
    _classDataProxyModels = {}  # {classCode: QSortFilterProxyModel()}
    _linkModel = ParentChildModel()

    _ark = None
    _indexLoaded = False
    _dataMode = ''
    _prevItem = Item()

    _mapAction = MapAction.MoveMap
    _filterAction = FilterAction.ExclusiveHighlightFilter
    _drawingAction = DrawingAction.NoDrawingAction

    items = {}  # {classCode: [Item]}

    def __init__(self, project):
        super(DataModule, self).__init__(project)
        self.project = project

    # Standard Dock methods

    # Create the gui when the plugin is first created
    def initGui(self):
        self.dock = DataDock(self.project.layerDock)
        action = self.project.addDockAction(
            ':/plugins/ark/data/data.svg', self.tr(u'Query Item Data'), callback=self.run, checkable=True)
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

    def loadData(self):
        self._ark = None
        self.refreshData()

    def refreshData(self):
        self._loadIndex()
        self._loadOfflineData()
        if self._indexLoaded or self._hasOfflineData():
            self.dataLoaded.emit()

    def hasClassData(self, classCode):
        try:
            return (len(self.items[classCode]) > 0)
        except Exception:
            return False

    def _hasOfflineData(self):
        return len(self._classDataModels) > 0

    def _loadOfflineData(self):
        for classCode in Config.classCodes.keys():
            keyFields = Item('site', 'class', 'id')
            filePath = self.project.projectPath() + '/data/' + self.project.siteCode() + '_' + classCode + '.csv'
            if classCode in self._classDataModels:
                self._classDataModels[classCode].clear()
            if QFile.exists(filePath):
                self._classDataModels[classCode] = ItemModel(filePath, keyFields, self)
                self._classDataProxyModels[classCode] = QSortFilterProxyModel()
                self._classDataProxyModels[classCode].setSourceModel(self._classDataModels[classCode])
                if Config.classCodes[classCode]['group']:
                    self._loadOfflineLinks(self._classDataModels[classCode].getList())
        if self._hasOfflineData():
            self._dataMode = 'offline'

    def _loadOfflineLinks(self, table):
        for record in table:
            parentItem = record['item']
            siteCode = record['ste_cd']
            childModule = record['child_module']
            children = str(record['children']).split()
            for child in children:
                childItem = Item(siteCode, childModule, child)
                self._linkModel.addChild(parentItem, childItem)

    def _createArkSession(self):
        dialog = CredentialsDialog()
        if dialog.exec_():
            self._ark = Ark(self.project.arkUrl(), dialog.username(), dialog.password())

    def _loadIndex(self):
        self._indexLoaded = False
        self.items = {}
        for classCode in Config.classCodes.keys():
            self.items[classCode] = []
            if not self._loadOfflineClassIndex(classCode):
                self._loadOnlineClassIndex(classCode)
        self.dock.setItemNavEnabled(self._indexLoaded)

    def _loadOfflineClassIndex(self, classCode):
        filePath = self.project.projectPath() + '/data/' + self.project.siteCode() + '_' + classCode + '.csv'
        if QFile.exists(filePath):
            with open(filePath) as csvFile:
                keyFields = Item('site', 'class', 'id')
                items = set()
                reader = csv.DictReader(csvFile)
                for record in reader:
                    item = Item(record[keyFields.siteCode], record[keyFields.classCode], record[keyFields.itemId])
                    items.add(item)
            self.items[classCode] = sorted(items)
            self.project.logMessage('Offline Item Keys ' + classCode + ' = ' + str(len(self.items[classCode])))
            if len(self.items[classCode]) > 0:
                self._indexLoaded = True
                return True
        return False

    def _loadOnlineClassIndex(self, classCode):
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
            lst = response.data[classCode]
            items = set()
            for record in lst:
                item = Item(record['ste_cd'], classCode, record[classCode + '_no'])
                if item.isValid():
                    items.add(item)
            self.items[classCode] = sorted(items)
            self.project.logMessage('ARK Items ' + classCode + ' = ' + str(len(self.items[classCode])))
            if (len(self.items[classCode]) > 0):
                self._indexLoaded = True
                return True
        return False

    def haveItem(self, item):
        try:
            return item in self.project.data.items[item.classCode()]
        except KeyError:
            return False

    def firstItem(self, classCode):
        try:
            return self.items[classCode][0]
        except KeyError:
            return Item()

    def lastItem(self, classCode):
        try:
            return self.items[classCode][-1]
        except KeyError:
            return Item()

    def prevItem(self, item):
        idx = -1
        try:
            if item.isValid():
                idx = bisect.bisect_left(self.items[item.classCode()], item) - 1
            if idx >= 0 and idx < len(self.items[item.classCode()]) - 1:
                return self.items[item.classCode()][idx]
        except Exception:
            pass
        return Item()

    def nextItem(self, item):
        idx = -1
        if item.isValid():
            idx = bisect.bisect(self.items[item.classCode()], item)
        if idx >= 0 and idx < len(self.items[item.classCode()]) - 1:
            return self.items[item.classCode()][idx]
        return Item()

    def openItem(self, item):
        if not self.project.arkUrl():
            self.project.showWarningMessage('ARK link not configured, please set the ARK URL in Settings.')
        elif not self.haveItem(item):
            self.project.showWarningMessage('Item not in ARK.')
        else:
            mod_cd = item.classCode() + '_cd'
            item_cd = item.siteCode() + '_' + item.itemId()
            url = self.project.arkUrl() + '/micro_view.php?item_key=' + mod_cd + '&' + mod_cd + '=' + item_cd
            try:
                webbrowser.get().open_new_tab(url)
            except Exception:
                QApplication.clipboard().setText(url)
                self.project.showWarningMessage('Unable to open browser, ARK link has been copied to the clipboard')

    def _getOnlineLinks(self, item, linkClassCode):
        if not self.project.arkUrl():
            return []
        xmi = unicode('conf_field_' + item.classCode() + linkClassCode + 'xmi')
        data = self.getItemFields(item, [xmi])
        items = []
        try:
            for link in data[xmi]:
                itemkey = link[u'xmi_itemkey']
                itemvalue = link[u'xmi_itemvalue'].split(u'_')
                item = Item(itemvalue[0], itemkey[:3], itemvalue[1])
                items.append(item)
        except Exception:
            return []
        return items

    def getItemData(self, item):
        try:
            return self._classDataModels[item.classCode()].getItem(item)
        except KeyError:
            return {}

    def childItems(self, item):
        if not item or item.isInvalid() or not Config.fields[item.classCode()]['group']:
            return []
        children = []
        for item in item.toList():
            children.extend(self._linkModel.getChildren(item))
        if len(children) > 0:
            return children
        for item in item.toList():
            children.extend(self._getOnlineLinks(item, Config.fields[item.classCode()]['child']))
        return children

    def nodesItem(self, parentItem):
        if (not self._indexLoaded
                or not parentItem
                or parentItem.isInvalid()
                or not Config.fields[parentItem.classCode()]['group']):
            return parentItem
        else:
            return self.nodesItem(self.childrenItem(parentItem))

    def childrenItem(self, parentItem):
        if not parentItem or parentItem.isInvalid() or not Config.fields[parentItem.classCode()]['group']:
            return Item()
        childIdSet = set()
        for parent in parentItem.toList():
            children = self.childItems(parent)
            for child in children:
                childIdSet.add(child.itemId())
        return Item(parentItem.siteCode(), Config.fields[parentItem.classCode()]['child'], childIdSet)

    def parentItem(self, item):
        # TODO Get from ARK
        return self._linkModel.getParent(item)

    def getFilters(self):
        if self._ark is None:
            return {}
        response = self._ark.describeFilters()
        if response.error:
            utils.logMessage(response.url)
            utils.logMessage(response.message)
            utils.logMessage(response.raw)
        return response.data

    def getFilterItems(self, filterId):
        items = []
        if self._ark is None:
            return items
        response = self._ark.getFilterSet(filterId)
        if response.error:
            utils.logMessage(response.url)
            utils.logMessage(response.message)
            utils.logMessage(response.raw)
        else:
            for item in response.data:
                res = response.data[item]
                item = Item()
                item.fromArkKey(res['itemkey'], res['itemval'])
                utils.logMessage(item.debug())
                if item.isValid():
                    items.append(item)
        return sorted(items)

    def getItemFields(self, item, fields):
        if self._ark is None or item is None or item.isInvalid():
            return {}
        response = self._ark.getFields(item.classCode() + '_cd', item.itemValue(), fields)
        if response.error:
            utils.logMessage(response.url)
            utils.logMessage(response.message)
            utils.logMessage(response.raw)
        return response.data

    def getItemSubform(self, item, subform):
        if self._ark is None or item is None or item.isInvalid():
            return {}
        response = self._ark.get()
        if response.error:
            utils.logMessage(response.url)
            utils.logMessage(response.message)
            utils.logMessage(response.raw)
        return response.url

    def showItemData(self,
                     item,
                     mapAction=MapAction.NoMapAction,
                     filterAction=FilterAction.NoFilterAction,
                     drawingAction=DrawingAction.NoDrawingAction
                     ):
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
        if not self.project.arkUrl():
            return
        self._prevItem = item
        url = ''
        if item.isValid() and self.haveItem(item):
            url = self._ark.transcludeSubformUrl(
                item.classCode() + '_cd', item.itemValue(), item.classCode() + '_apisum')
        self.dock.setItemUrl(url)

    def _value(self, value):
        if value is False:
            return ''
        if isinstance(value, list):
            return self._value(value[-1])
        if isinstance(value, dict):
            try:
                return value[u'current']
            except Exception:
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
        if 'download.php' in url.toString():
            # web = QWebView()
            # web.load(url)
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
            if len(parts) >= 2:
                item_key = parts[-2]
                item_value = parts[-1].split('_')
        if item_key and len(item_value) == 2:
            item = Item(item_value[0], item_key[:3], item_value[1])
            if self.haveItem(item):
                self.dock.setItem(item)
                self._itemChanged()

    def _mapActionChanged(self, mapAction):
        self._mapAction = mapAction

    def _filterActionChanged(self, filterAction):
        self._filterAction = filterAction

    def _drawingActionChanged(self, drawingAction):
        self._drawingAction = drawingAction
