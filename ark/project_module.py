# -*- coding: utf-8 -*-
"""
/***************************************************************************
                                ARK Spatial
                    A QGIS plugin for Archaeological Recording.
        Part of the Archaeological Recording Kit by L-P : Archaeology
                        http://ark.lparchaeology.com
                              -------------------
        copyright            : 2017 by L-P : Heritage LLP
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
import webbrowser

from PyQt4.QtCore import QObject, Qt
from PyQt4.QtGui import QApplication

from ArkSpatial.ark.lib import utils
from ArkSpatial.ark.lib.gui import ProjectDialog

from ArkSpatial.ark.core import Config, Item
from ArkSpatial.ark.pyARK import Ark


class ProjectModule(QObject):

    _ark = None
    _dialog = None

    def __init__(self):
        super(ProjectModule, self).__init__()

    # Create the gui when the plugin is first created
    def initGui(self):
        self._dialog = ProjectDialog(self)
        self._dialog.initGui(self.project.iface, action)
        self.__dict__dialog.projectChanged.connect(self._projectChanged)

    def run(self, checked):
        pass

    # Data methods

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

    def showItemData(self, item):
        self.dock.setItem(item)
        self._showItem(item)

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
