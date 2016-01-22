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

import select_item_widget_base

class SelectItemWidget(QWidget, metadata_widget_base.Ui_SelectItemWidget):

    siteCodeChanged = pyqtSignal(str)
    classCodeChanged = pyqtSignal(str)
    itemIdChanged = pyqtSignal(str)

    def __init__(self, parent=None):
        super(SelectItemWidget, self).__init__(parent)
        self.setupUi(self)

    def initGui(self, project):

        self.siteCodeCombo.currentIndexChanged.connect(self._siteCodeIndexChanged)
        self.classCodeCombo.currentIndexChanged.connect(self._classCodeIndexChanged)
        self.itemIdEdit.editingFinished.connect(self.itemIdChanged)

    def siteCode(self):
        return self.siteCodeCombo.itemData(self.siteCodeCombo.currentIndex())

    def classCode(self):
        return self.classCodeChanged.itemData(self.classCodeChanged.currentIndex())

    def itemId(self):
        return self.itemIdEdit.text()

    def _siteCodeIndexChanged(self, idx):
        emit self.siteCodeChanged(self.siteCodeCombo.itemData(idx))

    def _classCodeIndexChanged(self, idx):
        emit self.classCodeChanged(self.classCodeCombo.itemData(idx))
