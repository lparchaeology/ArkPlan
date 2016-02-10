# -*- coding: utf-8 -*-
"""
/***************************************************************************
                                ARK Spatial
                    A QGIS plugin for Archaeological Recording.
        Part of the Archaeological Recording Kit by L-P : Archaeology
                        http://ark.lparchaeology.com
                              -------------------
        begin                : 2014-12-07
        git sha              : $Format:%H$
        copyright            : 2014, 2015 by L-P : Heritage LLP
        email                : ark@lparchaeology.com
        copyright            : 2014, 2015 by John Layt
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

from PyQt4 import uic
from PyQt4.QtCore import Qt, pyqtSignal
from PyQt4.QtGui import QWidget

from config import Config
from plan_item import ItemKey

from select_item_widget_base import *

class SelectItemWidget(QWidget, Ui_SelectItemWidget):

    siteCodeChanged = pyqtSignal(str)
    classCodeChanged = pyqtSignal(str)
    itemIdChanged = pyqtSignal(str)
    itemIdEntered = pyqtSignal()

    def __init__(self, parent=None):
        super(SelectItemWidget, self).__init__(parent)
        self.setupUi(self)

    def initGui(self, project):

        self.siteCodeCombo.currentIndexChanged.connect(self._siteCodeIndexChanged)
        self.classCodeCombo.currentIndexChanged.connect(self._classCodeIndexChanged)
        self.itemIdEdit.editingFinished.connect(self.itemIdChanged)
        self.itemIdEdit.returnPressed.connect(self.itemIdEntered)

    def siteCode(self):
        return self.siteCodeCombo.itemData(self.siteCodeCombo.currentIndex())

    def setSiteCodes(self, siteCodes, default=None):
        self.siteCodeCombo.clear()
        for siteCode in sorted(set(siteCodes)):
            self.siteCodeCombo.addItem(siteCode, siteCode)
        if default:
            idx = self.siteCodeCombo.findData(default)
            if idx >= 0:
                self.siteCodeCombo.setCurrentIndex(idx)

    def classCode(self):
        return self.classCodeCombo.itemData(self.classCodeCombo.currentIndex())

    def setClassCodes(self, classCodes, default=None):
        self.classCodeCombo.clear()
        for key in classCodes:
            classCode = Config.classCodes[key]
            self.classCodeCombo.addItem(classCode['label'], key)
        if default:
            idx = self.classCodeCombo.findData(default)
            if idx >= 0:
                self.classCodeCombo.setCurrentIndex(idx)

    def itemId(self):
        return self.itemIdEdit.text()

    def item(self):
        return ItemKey(self.siteCode(), self.classCode(), self.itemId())

    def setItem(self, itemKey):
        if type(itemKey) == ItemKey and itemKey.isValid():
            self.siteCodeCombo.setCurrentIndex(self.siteCodeCombo.findData(itemKey.siteCode))
            self.classCodeCombo.setCurrentIndex(self.classCodeCombo.findData(itemKey.classCode))
            self.itemIdEdit.setText(itemKey.itemId)

    def _siteCodeIndexChanged(self, idx):
        self.siteCodeChanged.emit(self.siteCodeCombo.itemData(idx))

    def _classCodeIndexChanged(self, idx):
        self.classCodeChanged.emit(self.classCodeCombo.itemData(idx))
