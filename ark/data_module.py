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

from ArkSpatial.ark.core import Config, Item, ItemModel, Settings
from ArkSpatial.ark.core.enum import DrawingAction, FilterAction, MapAction
from ArkSpatial.ark.gui import DataDock
from ArkSpatial.ark.pyARK import Ark


class DataModule(QObject):

    dataLoaded = pyqtSignal()

    def __init__(self, plugin):
        super(DataModule, self).__init__(plugin)

        self.plugin = plugin  # Plugin()
        self.items = {}  # {classCode: [Item]}

        # Internal variables
        self.dock = None  # DataDock()
        self._classDataModels = {}  # {classCode: ItemModel()}
        self._classDataProxyModels = {}  # {classCode: QSortFilterProxyModel()}
        self._linkModel = ParentChildModel()
        self._ark = None
        self._indexLoaded = False
        self._dataMode = ''
        self._prevItem = Item()
        self._mapAction = MapAction.MoveMap
        self._filterAction = FilterAction.ExclusiveHighlightFilter
        self._drawingAction = DrawingAction.NoDrawingAction

    # Standard Dock methods

    # Create the gui when the plugin is first created
    def initGui(self):
        self.dock = DataDock(self.plugin.iface.mainWindow())
        action = self.plugin.addDockAction(
            ':/plugins/ark/data/data.svg', self.tr(u'Query Item Data'), callback=self.run, checkable=True)
        self.dock.initGui(self.plugin.iface, Qt.LeftDockWidgetArea, action)

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
        self.dock.initSiteCodes([Settings.siteCode()])
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
        if self._indexLoaded:
            self.dataLoaded.emit()

    def hasClassData(self, classCode):
        try:
            return (len(self.items[classCode]) > 0)
        except Exception:
            return False

    def _createArkSession(self):
        dialog = CredentialsDialog()
        if dialog.exec_():
            self._ark = Ark(Settings.siteServerUrl(), dialog.siteServerUser(), dialog.siteServerPassword())

    def _loadIndex(self):
        self._indexLoaded = False
        self.items = {}
        for classCode in Config.classCodes.keys():
            self.items[classCode] = []
            self._loadOnlineClassIndex(classCode)
        self.dock.setItemNavEnabled(self._indexLoaded)

    def _loadOnlineClassIndex(self, classCode):
        if not Settings.siteServerUrl():
            return False
        if self._ark is None:
            self._createArkSession()
        if self._ark is None:
            return False
        response = self._ark.getItems(classCode + '_cd')
        if response.error:
            self.plugin.logMessage(response.url)
            self.plugin.logMessage(response.message)
            self.plugin.logMessage(response.raw)
        else:
            lst = response.data[classCode]
            items = set()
            for record in lst:
                item = Item(record['ste_cd'], classCode, record[classCode + '_no'])
                if item.isValid():
                    items.add(item)
            self.items[classCode] = sorted(items)
            self.plugin.logMessage('ARK Items ' + classCode + ' = ' + str(len(self.items[classCode])))
            if (len(self.items[classCode]) > 0):
                self._indexLoaded = True
                return True
        return False

    def haveItem(self, item):
        try:
            return item in self.plugin.data.items[item.classCode()]
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
        if not Settings.siteServerUrl():
            self.plugin.showWarningMessage('ARK link not configured, please set the ARK URL in Settings.')
        elif not self.haveItem(item):
            self.plugin.showWarningMessage('Item not in ARK.')
        else:
            mod_cd = item.classCode() + '_cd'
            item_cd = item.siteCode() + '_' + item.itemId()
            url = Settings.siteServerUrl() + '/micro_view.php?item_key=' + mod_cd + '&' + mod_cd + '=' + item_cd
            try:
                webbrowser.get().open_new_tab(url)
            except Exception:
                QApplication.clipboard().setText(url)
                self.plugin.showWarningMessage('Unable to open browser, ARK link has been copied to the clipboard')

    def _getOnlineLinks(self, item, linkClassCode):
        if not Settings.siteServerUrl():
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
        self.plugin.drawingModule.applyItemActions(item, mapAction, filterAction, drawingAction)

    def _itemChanged(self):
        item = self.dock.item()
        if self._prevItem == item:
            return
        self._showItem(item)
        self.plugin.drawingModule.applyItemActions(item, self._mapAction, self._filterAction, self._drawingAction)

    def _showItem(self, item):
        if not Settings.siteServerUrl():
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
        self.plugin.drawingModule.openItemInArk(self.dock.item())

    def _nextItemSelected(self):
        self.dock.setItem(self.nextItem(self.dock.item()))
        self._itemChanged()

    def _lastItemSelected(self):
        self.dock.setItem(self.lastItem(self.dock.classCode()))
        self._itemChanged()

    def _showItemSelected(self):
        self.plugin.drawingModule.showItem(self.dock.item())

    def _zoomItemSelected(self):
        self.plugin.drawingModule.zoomToItem(self.dock.item())

    def _filterItemSelected(self):
        self.plugin.drawingModule.filterItem(self.dock.item())

    def _editItemSelected(self):
        self.plugin.drawingModule.editInBuffers(self.dock.item())

    def _loadDrawingsSelected(self):
        self.plugin.drawingModule.loadSourceDrawings(self.dock.item())

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
