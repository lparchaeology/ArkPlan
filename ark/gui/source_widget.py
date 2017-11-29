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

from PyQt4.QtCore import pyqtSignal
from PyQt4.QtGui import QWidget

from ArkSpatial.ark.core import Config, Item, Source

from .ui.source_widget_base import Ui_SourceWidget


class SourceWidget(QWidget, Ui_SourceWidget):

    sourceChanged = pyqtSignal()

    def __init__(self, parent=None):
        super(SourceWidget, self).__init__(parent)
        self.setupUi(self)

    def initGui(self):
        for key in sorted(Config.classCodes.keys()):
            classCode = Config.classCodes[key]
            if classCode['source']:
                self.sourceClassCombo.addItem(classCode['label'], classCode['code'])

        for key in Config.sourceCodesOrder:
            sourceCode = Config.sourceCodes[key]
            self.sourceCodeCombo.addItem(sourceCode['label'], sourceCode['code'])

        self.siteCodeCombo.currentIndexChanged.connect(self.sourceChanged)
        self.sourceCodeCombo.currentIndexChanged.connect(self.sourceChanged)
        self.sourceClassCombo.currentIndexChanged.connect(self.sourceChanged)
        self.sourceIdEdit.editingFinished.connect(self.sourceChanged)
        self.sourceFileEdit.editingFinished.connect(self.sourceChanged)

    def unloadGui(self):
        pass

    def loadProject(self, project):
        self.siteCodeCombo.clear()
        for siteCode in sorted(set(project.siteCodes())):
            self.siteCodeCombo.addItem(siteCode, siteCode)
        self._setSiteCode(project.siteCode())

    def closeProject(self):
        pass

    def source(self):
        return Source(self._sourceCode(), self._sourceItem(), self._sourceFile())

    def setSource(self, source):
        self.blockSignals(True)

        self.sourceCodeCombo.setCurrentIndex(self.sourceCodeCombo.findData(source.sourceCode()))
        self.sourceFileEdit.setText(source.sourceFile())

        self._setSiteCode(source.item().siteCode())
        self.sourceClassCombo.setCurrentIndex(self.sourceClassCombo.findData(source.item().classCode()))
        self.sourceIdEdit.setText(source.item().itemId())

        self.blockSignals(False)
        self.sourceChanged.emit()

    def _setSiteCode(self, siteCode):
        idx = self.siteCodeCombo.findData(siteCode)
        if idx >= 0:
            self.siteCodeCombo.setCurrentIndex(idx)

    def _sourceCode(self):
        return self.sourceCodeCombo.itemData(self.sourceCodeCombo.currentIndex())

    def _siteCode(self):
        return self.siteCodeCombo.itemData(self.siteCodeCombo.currentIndex())

    def _sourceItem(self):
        return Item(self._siteCode(), self._sourceClass(), self._sourceId())

    def _sourceClass(self):
        return self.sourceClassCombo.itemData(self.sourceClassCombo.currentIndex())

    def _sourceId(self):
        return self.sourceIdEdit.text().strip()

    def _sourceFile(self):
        return self.sourceFileEdit.text().strip()
