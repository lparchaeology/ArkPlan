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

import os

from PyQt4 import uic
from PyQt4.QtCore import Qt, pyqtSignal
from PyQt4.QtGui import QTabWidget, QToolButton

import drawing_widget_base

class DrawingWidget(QTabWidget, drawing_widget_base.Ui_DrawingWidget):

    autoSchematicSelected = pyqtSignal()
    featureNameChanged = pyqtSignal(str)
    sectionChanged = pyqtSignal(object)

    _cgColMax = 4
    _cgCol = 0
    _cgRow = 0
    _fgColMax = 4
    _fgCol = 0
    _fgRow = 0
    _sgColMax = 4
    _sgCol = 0
    _sgRow = 0

    def __init__(self, parent=None):
        super(DrawingWidget, self).__init__(parent)
        self.setupUi(self)

    def initGui(self):
        self.autoSchematicTool.clicked.connect(self.autoSchematicSelected)
        self.featureNameEdit.textChanged.connect(self.featureNameChanged)
        self.sectionCombo.currentIndexChanged.connect(self._sectionChanged)

    def unloadGui(self):
        pass

    def loadProject(self, project):
        pass

    def closeProject(self):
        pass

    def initSections(self, itemList):
        self.sectionCombo.clear()
        for section in sorted(itemList):
            if section.name:
                self.sectionCombo.addItem(section.name, section.key)
            else:
                self.sectionCombo.addItem('S' + section.key.itemId, section.key)

    def featureName(self):
        return self.featureNameEdit.text()

    def setFeatureName(self, name):
        self.featureNameEdit.setText(name)

    def sectionKey(self):
        return self.sectionCombo.itemData(self.sectionCombo.currentIndex())

    def setSection(self, itemKey):
        #TODO Doesn't work when it should...
        #idx = self.sectionCombo.findData(itemKey)
        for i in range(0, self.sectionCombo.count()):
            if self.sectionCombo.itemData(i) == itemKey:
                self.sectionCombo.setCurrentIndex(i)
                return

    # Drawing Tools

    def addDrawingTool(self, dockTab, action):
        toolButton = QToolButton(self)
        toolButton.setFixedWidth(40)
        toolButton.setDefaultAction(action)
        if dockTab == 'cxt':
            self.contextToolsLayout.addWidget(toolButton, self._cgRow, self._cgCol, Qt.AlignCenter)
            if self._cgCol == self._cgColMax:
                self._cgRow += 1
                self._cgCol = 0
            else:
                self._cgCol += 1
        elif dockTab == 'sec':
            self.sectionToolsLayout.addWidget(toolButton, self._sgRow, self._sgCol, Qt.AlignCenter)
            if self._sgCol == self._sgColMax:
                self._sgRow += 1
                self._sgCol = 0
            else:
                self._sgCol += 1
        else:
            self.featureToolsLayout.addWidget(toolButton, self._fgRow, self._fgCol, Qt.AlignCenter)
            if self._fgCol == self._fgColMax:
                self._fgRow += 1
                self._fgCol = 0
            else:
                self._fgCol += 1

    def _sectionChanged(self, idx):
        self.sectionChanged.emit(self.sectionCombo.itemData(idx))
