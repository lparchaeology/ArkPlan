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

from qgis.PyQt.QtCore import QObject, pyqtSignal
from qgis.PyQt.QtWidgets import QInputDialog

from ArkSpatial.ark.core import ItemFeature


class Metadata(QObject):

    metadataChanged = pyqtSignal()

    def __init__(self, planWidget, parent=None):
        super().__init__(parent)
        self.feature = planWidget.feature()
        self._planWidget = planWidget  # MetadataWidget
        self._connectWidget(self._planWidget)

    def _connectWidget(self, widget):
        widget.siteCodeChanged.connect(self._setSiteCode)
        widget.classCodeChanged.connect(self._setClassCode)
        widget.itemIdChanged.connect(self._setItemId)
        widget.sourceCodeChanged.connect(self._setSourceCode)
        widget.sourceClassChanged.connect(self._setSourceClass)
        widget.sourceIdChanged.connect(self._setSourceId)
        widget.sourceFileChanged.connect(self._setSourceFile)
        widget.commentChanged.connect(self._setComment)
        widget.editorChanged.connect(self._setEditor)
        widget.validateMetadata.connect(self.validate)

    def siteCode(self):
        return self.feature.item().siteCode()

    def setSiteCode(self, siteCode):
        self.feature.item().setSiteCode(siteCode)
        self.feature.source().item().setSiteCode(siteCode)
        self._planWidget.setSiteCode(self.siteCode())

    def _setSiteCode(self, siteCode):
        self.setSiteCode(siteCode)
        self.metadataChanged.emit()

    def classCode(self):
        return self.feature.item().classCode()

    def setClassCode(self, classCode):
        self.feature.item().setClassCode(classCode)
        self._planWidget.setClassCode(self.classCode())

    def _setClassCode(self, classCode):
        self.setClassCode(classCode)
        self.metadataChanged.emit()

    def itemId(self):
        return self.feature.item().itemId()

    def setItemId(self, itemId):
        self.feature.item().setItemId(itemId)
        self._planWidget.setItemId(self.itemId())

    def _setItemId(self, itemId):
        self.setItemId(itemId)
        self.metadataChanged.emit()

    def category(self):
        return self.feature.category()

    def setCategory(self, category):
        self.feature.setCategory(category)

    def label(self):
        return self.feature.label()

    def setName(self, name):
        self.feature.setName(name)

    def sourceCode(self):
        return self.feature.source().sourceCode()

    def setSourceCode(self, sourceCode):
        self.feature.source().setSourceCode(sourceCode)
        self._planWidget.setSourceCode(self.sourceCode())

    def _setSourceCode(self, sourceCode):
        self.setSourceCode(sourceCode)
        self.metadataChanged.emit()

    def sourceClass(self):
        return self.feature.source().item().classCode()

    def setSourceClass(self, sourceClass):
        self.feature.source().setSourceClass(sourceClass)
        self._planWidget.setSourceClass(self.sourceClass())

    def _setSourceClass(self, sourceClass):
        self.setSourceClass(sourceClass)
        self.metadataChanged.emit()

    def sourceId(self):
        return self.feature.source().item().itemId()

    def setSourceId(self, sourceId):
        self.feature.source().setSourceId(sourceId)
        self._planWidget.setSourceId(self.sourceId())

    def _setSourceId(self, sourceId):
        self.setSourceId(sourceId)
        self.metadataChanged.emit()

    def sourceFile(self):
        return self.feature.source().filename()

    def setSourceFile(self, sourceFile):
        self.feature.source().setFilename(sourceFile)
        self._planWidget.setSourceFile(self.sourceFile())

    def _setSourceFile(self, sourceFile):
        self.setSourceFile(sourceFile)
        self.metadataChanged.emit()

    def comment(self):
        return self.feature.comment()

    def setComment(self, comment):
        self.feature.setComment(comment)
        self._planWidget.setComment(self.comment())

    def _setComment(self, comment):
        self.setComment(comment)
        self.metadataChanged.emit()

    def editor(self):
        return self.feature.creator()

    def setEditor(self, editor):
        self.feature.setCreator(editor)
        self._planWidget.setEditor(self.editor())

    def _setEditor(self, editor):
        self.setEditor(editor)
        self.metadataChanged.emit()

    def created(self):
        return self.feature.created()

    def setCreated(self, created):
        self.feature.setCreated(created)

    def fromFeature(self, feature):
        self.fromItemFeature(ItemFeature(feature))

    def fromItemFeature(self, feature):
        self.setSiteCode(feature.item().siteCode())
        self.setClassCode(feature.item().classCode())
        self.setItemId(feature.item().itemId())
        self.setComment(feature.comment())
        self.setSourceCode(feature.source().sourceCode())
        self.setSourceClass(feature.source().item.classCode())
        self.setSourceId(feature.source().item().itemId())
        self.setSourceFile(feature.source().filename())

    def validate(self):
        signalChanged = False
        if self.siteCode() == '':
            value, ok = QInputDialog.getText(None, 'Site Code', 'Please enter a valid Site Code')
            if ok and value.strip():
                self.setSiteCode(value)
                signalChanged = True
        if self.classCode() == '':
            self.setClassCode(self._planWidget.classCode())
        if self.itemId() == '':
            value = 0
            ok = False
            value, ok = QInputDialog.getInt(None, 'Item ID', 'Please enter a valid Item ID', 1, 1, 99999)
            if ok and value > 0:
                self.setItemId(str(value))
                signalChanged = True
        if self.sourceCode() == '':
            self.setSourceCode(self._planWidget.sourceCode())
        if self.sourceClass() == '':
            self.setSourceClass(self._planWidget.sourceClass())
        if self.sourceCode() != 'svy' and self.sourceId() == '':
            value, ok = QInputDialog.getInt(None, 'Source ID', 'Please enter a valid Source ID Number', 1, 1, 99999)
            if ok and value > 0:
                self.setSourceId(str(value))
                signalChanged = True
        if (self.sourceCode() == 'svy' and self.sourceFile() == ''):
            value, ok = QInputDialog.getText(None, 'Source File', "Please enter the source file name")
            if ok and value.strip():
                self.setSourceFile(value)
                signalChanged = True
        if self.editor() == '':
            value, ok = QInputDialog.getText(None, 'Editor', "Please enter your full name (e.g. 'Dorothy Garrod')")
            if ok and value.strip():
                self.setEditor(value)
                signalChanged = True
        if signalChanged:
            self.metadataChanged.emit()
