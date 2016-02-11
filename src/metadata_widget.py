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

import metadata_widget_base

class MetadataWidget(QGroupBox, metadata_widget_base.Ui_MetadataWidget):

    siteCodeChanged = pyqtSignal(str)
    classCodeChanged = pyqtSignal(str)
    itemIdChanged = pyqtSignal(str)
    sourceCodeChanged = pyqtSignal(str)
    sourceClassChanged = pyqtSignal(str)
    sourceIdChanged = pyqtSignal(str)
    sourceFileChanged = pyqtSignal(str)
    commentChanged = pyqtSignal(str)
    createdByChanged = pyqtSignal(str)
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

        self.siteEdit.editingFinished.connect(self._siteCodeChanged)
        self.classCombo.currentIndexChanged.connect(self._classCodeChanged)
        self.idSpin.valueChanged.connect(self._itemIdChanged)
        self.sourceCodeCombo.currentIndexChanged.connect(self._sourceCodeChanged)
        self.sourceClassCombo.currentIndexChanged.connect(self._sourceClassChanged)
        self.sourceIdSpin.valueChanged.connect(self._sourceIdChanged)
        self.sourceFileEdit.editingFinished.connect(self._sourceFileChanged)
        self.commentEdit.editingFinished.connect(self._commentChanged)
        self.createdByEdit.editingFinished.connect(self._createdByChanged)

    def unloadGui(self):
        pass

    def loadProject(self, project):
        pass

    def closeProject(self):
        pass

    def setSiteCode(self, siteCode):
        self.siteEdit.setText(siteCode)

    def siteCode(self):
        return self.siteEdit.text()

    def _siteCodeChanged(self):
        self.siteCodeChanged.emit(self.siteCode())

    def setClassCode(self, classCode):
        self.classCombo.setCurrentIndex(self.classCombo.findData(classCode))

    def classCode(self):
        self.classCombo.itemData(self.classCombo.currentIndex())

    def _classCodeChanged(self, idx):
        self.classCodeChanged.emit(self.classCombo.itemData(idx))

    def setItemId(self, itemId):
        self.blockSignals(True)
        if itemId is None or itemId ==  NULL or itemId == '':
            self.idSpin.setValue(0)
        else:
            self.idSpin.setValue(int(itemId))
        self.blockSignals(False)

    def itemId(self):
        if self.idSpin.value() > 0:
            return str(self.idSpin.value())
        else:
            return ''

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
        if sourceId is None or sourceId ==  NULL or sourceId == '':
            self.sourceIdSpin.setValue(0)
        else:
            self.sourceIdSpin.setValue(int(sourceId))
        self.blockSignals(False)

    def sourceId(self):
        if self.sourceIdSpin.value() > 0:
            return str(self.sourceIdSpin.value())
        else:
            return ''

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

    def setCreatedBy(self, createdBy):
        self.createdByEdit.setText(createdBy)

    def createdBy(self):
        return self.createdByEdit.text()

    def _createdByChanged(self):
        self.createdByChanged.emit(self.createdBy())

    def validate(self):
        self.validateMetadata().emit()
