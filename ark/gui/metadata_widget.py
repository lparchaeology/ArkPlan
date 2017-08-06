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
from PyQt4.QtCore import pyqtSignal
from PyQt4.QtGui import QGroupBox

from ark.core import Config, Feature, Item, Source

from metadata_widget_base import Ui_MetadataWidget


class MetadataWidget(QGroupBox, Ui_MetadataWidget):

    siteCodeChanged = pyqtSignal(str)
    classCodeChanged = pyqtSignal(str)
    itemIdChanged = pyqtSignal(str)
    sourceCodeChanged = pyqtSignal(str)
    sourceClassChanged = pyqtSignal(str)
    sourceIdChanged = pyqtSignal(str)
    sourceFileChanged = pyqtSignal(str)
    commentChanged = pyqtSignal(str)
    editorChanged = pyqtSignal(str)
    validateMetadata = pyqtSignal()

    def __init__(self, parent=None):
        super(MetadataWidget, self).__init__(parent)
        self.setupUi(self)

    def initGui(self):
        for key in sorted(Config.classCodes.keys()):
            classCode = Config.classCodes[key]
            if classCode['plan']:
                self.classCombo.addItem(classCode['label'], classCode['code'])
            if classCode['source']:
                self.sourceClassCombo.addItem(classCode['label'], classCode['code'])

        for key in Config.sourceCodesOrder:
            sourceCode = Config.sourceCodes[key]
            self.sourceCodeCombo.addItem(sourceCode['label'], sourceCode['code'])

        self.siteCodeCombo.currentIndexChanged.connect(self._classCodeChanged)
        self.classCombo.currentIndexChanged.connect(self._classCodeChanged)
        self.idSpin.valueChanged.connect(self._itemIdChanged)
        self.sourceCodeCombo.currentIndexChanged.connect(self._sourceCodeChanged)
        self.sourceClassCombo.currentIndexChanged.connect(self._sourceClassChanged)
        self.sourceIdSpin.valueChanged.connect(self._sourceIdChanged)
        self.sourceFileEdit.editingFinished.connect(self._sourceFileChanged)
        self.commentEdit.editingFinished.connect(self._commentChanged)
        self.editorEdit.editingFinished.connect(self._editorChanged)

    def unloadGui(self):
        pass

    def loadProject(self, project):
        self.siteCodeCombo.clear()
        for siteCode in sorted(set(project.siteCodes())):
            self.siteCodeCombo.addItem(siteCode, siteCode)
        self.setSiteCode(project.siteCode())

    def closeProject(self):
        pass

    def item(self):
        return Item(self.siteCode(), self.classCode(), self.itemId())

    def sourceItem(self):
        return Item(self.siteCode(), self.sourceClass(), self.sourceId())

    def source(self):
        return Source(self.sourceCode(), self.sourceItem(), self.sourceFile())

    def feature(self):
        return Feature(item=self.item(), source=self.source(), comment=self.comment(), creator=self.editor())

    def setSiteCode(self, siteCode):
        idx = self.siteCodeCombo.findData(siteCode)
        if idx >= 0:
            self.siteCodeCombo.setCurrentIndex(idx)

    def siteCode(self):
        return self.siteCodeCombo.itemData(self.classCombo.currentIndex())

    def _siteCodeChanged(self, idx):
        self.siteCodeChanged.emit(self.siteCodeCombo.itemData(idx))

    def setClassCode(self, classCode):
        self.classCombo.setCurrentIndex(self.classCombo.findData(classCode))

    def classCode(self):
        return self.classCombo.itemData(self.classCombo.currentIndex())

    def _classCodeChanged(self, idx):
        self.classCodeChanged.emit(self.classCombo.itemData(idx))

    def setItemId(self, itemId):
        self.blockSignals(True)
        if (isinstance(itemId, int) and itemId >= 0) or (isinstance(itemId, str) and itemId.isdigit() and int(itemId) >= 0):
            self.idSpin.setValue(int(itemId))
        else:
            self.idSpin.setValue(0)
        self.blockSignals(False)

    def itemId(self):
        return str(self.idSpin.value())

    def _itemIdChanged(self, itemId):
        self.itemIdChanged.emit(self.itemId())

    def setSourceCode(self, sourceCode):
        self.sourceCodeCombo.setCurrentIndex(self.sourceCodeCombo.findData(sourceCode))

    def sourceCode(self):
        return self.sourceCodeCombo.itemData(self.sourceCodeCombo.currentIndex())

    def _sourceCodeChanged(self, idx):
        self.sourceCodeChanged.emit(self.sourceCodeCombo.itemData(idx))

    def setSourceClass(self, sourceClass):
        self.sourceClassCombo.setCurrentIndex(self.sourceClassCombo.findData(sourceClass))

    def sourceClass(self):
        return self.sourceClassCombo.itemData(self.sourceClassCombo.currentIndex())

    def _sourceClassChanged(self, idx):
        self.sourceClassChanged.emit(self.sourceClassCombo.itemData(idx))

    def setSourceId(self, sourceId):
        self.blockSignals(True)
        if (isinstance(sourceId, int) and sourceId >= 0) or (isinstance(sourceId, str) and sourceId.isdigit() and int(sourceId) >= 0):
            self.sourceIdSpin.setValue(int(sourceId))
        else:
            self.sourceIdSpin.setValue(0)
        self.blockSignals(False)

    def sourceId(self):
        return str(self.sourceIdSpin.value())

    def _sourceIdChanged(self, sourceId):
        self.sourceIdChanged.emit(self.sourceId())

    def setSourceFile(self, sourceFile):
        self.sourceFileEdit.setText(sourceFile)

    def sourceFile(self):
        return self.sourceFileEdit.text()

    def _sourceFileChanged(self):
        self.sourceFileChanged.emit(self.sourceFile())

    def setComment(self, comment):
        self.commentEdit.setText(comment)

    def comment(self):
        return self.commentEdit.text()

    def _commentChanged(self):
        self.commentChanged.emit(self.comment())

    def setEditor(self, editor):
        self.editorEdit.setText(editor)

    def editor(self):
        return self.editorEdit.text()

    def _editorChanged(self):
        self.editorChanged.emit(self.editor())

    def validate(self):
        self.validateMetadata().emit()
