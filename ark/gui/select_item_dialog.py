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

from PyQt4 import uic
from PyQt4.QtGui import QDialog

from ark.core import Config

from select_item_dialog_base import Ui_SelectItemDialog


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

    def setItem(self, item):
        return self.itemWidget.setItem(item)

    def loadDrawings(self):
        return self.loadDrawingCheck.isChecked()

    def zoomToItem(self):
        return self.zoomItemCheck.isChecked()
