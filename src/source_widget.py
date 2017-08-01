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
from PyQt4.QtCore import pyqtSignal
from PyQt4.QtGui import QGroupBox

from qgis.core import NULL

from config import Config
from plan_item import *

import source_widget_base

class SourceWidget(QGroupBox, source_widget_base.Ui_SourceWidget):

    siteCodeChanged = pyqtSignal(str)
    sourceClassChanged = pyqtSignal(str)
    sourceIdChanged = pyqtSignal(str)
    sourceCodeChanged = pyqtSignal(str)
    sourceFileChanged = pyqtSignal(str)
    editorChanged = pyqtSignal(str)
    commentChanged = pyqtSignal(str)
    validateMetadata = pyqtSignal()

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

    def sourceItem(self):
        return ItemKey(self.siteCode(), self.sourceClass(), self.sourceId())

    def source(self):
        return ItemSource(self.sourceCode(), self.sourceItem(), self.sourceFile())

    def feature(self):
        return ItemFeature(key=self.item(), source=self.source(), comment=self.comment(), creator=self.editor())

    def setSiteCode(self, siteCode):
        idx = self.siteCodeCombo.findData(siteCode)
        if idx >= 0:
            self.siteCodeCombo.setCurrentIndex(idx)

    def siteCode(self):
        return self.siteCodeCombo.itemData(self.classCombo.currentIndex())

    def _siteCodeChanged(self, idx):
        self.siteCodeChanged.emit(self.siteCodeCombo.itemData(idx))

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
        if (isinstance(sourceId, int) and sourceId >=0) or (isinstance(sourceId, str) and sourceId.isdigit() and int(sourceId) >= 0):
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
