# -*- coding: utf-8 -*-
"""
/***************************************************************************
                                ARK Spatial
                    A QGIS plugin for Archaeological Recording.
        Part of the Archaeological Recording Kit by L-P : Archaeology
                        http://ark.lparchaeology.com
                              -------------------
        begin                : 2016-02-10
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

import os.path

from PyQt4 import uic
from PyQt4.QtCore import Qt, QDir
from PyQt4.QtGui import QDialog, QDialogButtonBox, QAbstractItemView

from config import Config

from select_item_dialog_base import *

class SelectItemDialog(QDialog, Ui_SelectItemDialog):

    def __init__(self, siteCodes, defaultSiteCode=None, classCodes=None, parent=None):
        super(SelectItemDialog, self).__init__(parent)
        self.setupUi(self)

        self.itemWidget.setSiteCodes(siteCodes, defaultSiteCode)

        if classCodes == None:
            classCodes = sorted(Config.classCodes.keys())
        self.itemWidget.setClassCodes(classCodes)

        loadDrawings = False
        for classCode in classCodes:
            if Config.classCodes[classCode]['drawing']:
                loadDrawings = True

        self.itemWidget.itemIdEntered.connect(self.accept)

    def accept(self):
        return super(SelectItemDialog, self).accept()

    def item(self):
        return self.itemWidget.item()

    def setItem(self, itemKey):
        return self.itemWidget.setItem(itemKey)

    def loadDrawings(self):
        return self.loadDrawingCheck.isChecked()

    def zoomToItem(self):
        return self.zoomItemCheck.isChecked()