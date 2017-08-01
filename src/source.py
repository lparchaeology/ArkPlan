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

import string

from PyQt4.QtCore import QObject, pyqtSignal, QPyNullVariant
from PyQt4.QtGui import QInputDialog

from plan_item import ItemFeature

class Source(QObject):

    def __init__(self, planWidget, parent=None):
        super(Metadata, self).__init__(parent)

    def siteCode(self):
        return self.itemFeature.key.siteCode

    def setSiteCode(self, siteCode):
        self.itemFeature.key.setSiteCode(siteCode)
        self.itemFeature.source.key.setSiteCode(siteCode)
        self._planWidget.setSiteCode(self.siteCode())

    def _setSiteCode(self, siteCode):
        self.setSiteCode(siteCode)
        self.metadataChanged.emit()

    def sourceCode(self):
        return self.itemFeature.source.sourceCode

    def setSourceCode(self, sourceCode):
        self.itemFeature.source.setSourceCode(sourceCode)
        self._planWidget.setSourceCode(self.sourceCode())

    def _setSourceCode(self, sourceCode):
        self.setSourceCode(sourceCode)
        self.metadataChanged.emit()

    def sourceClass(self):
        return self.itemFeature.source.key.classCode

    def setSourceClass(self, sourceClass):
        self.itemFeature.source.setSourceClass(sourceClass)
        self._planWidget.setSourceClass(self.sourceClass())

    def _setSourceClass(self, sourceClass):
        self.setSourceClass(sourceClass)
        self.metadataChanged.emit()

    def sourceId(self):
        return self.itemFeature.source.key.itemId

    def setSourceId(self, sourceId):
        self.itemFeature.source.setSourceId(sourceId)
        self._planWidget.setSourceId(self.sourceId())

    def _setSourceId(self, sourceId):
        self.setSourceId(sourceId)
        self.metadataChanged.emit()

    def sourceFile(self):
        return self.itemFeature.source.filename

    def setSourceFile(self, sourceFile):
        self.itemFeature.source.setFilename(sourceFile)
        self._planWidget.setSourceFile(self.sourceFile())

    def _setSourceFile(self, sourceFile):
        self.setSourceFile(sourceFile)
        self.metadataChanged.emit()

    def comment(self):
        return self.itemFeature.comment

    def setComment(self, comment):
        self.itemFeature.setComment(comment)
        self._planWidget.setComment(self.comment())

    def _setComment(self, comment):
        self.setComment(comment)
        self.metadataChanged.emit()

    def editor(self):
        return self.itemFeature.creator

    def setEditor(self, editor):
        self.itemFeature.setCreator(editor)
        self._planWidget.setEditor(self.editor())

    def _setEditor(self, editor):
        self.setEditor(editor)
        self.metadataChanged.emit()

    def fromFeature(self, feature):
        self.fromItemFeature(ItemFeature(feature))

    def fromItemFeature(self, feature):
        self.setSiteCode(feature.key.siteCode)
        self.setClassCode(feature.key.classCode)
        self.setItemId(feature.key.itemId)
        self.setComment(feature.comment)
        self.setSourceCode(feature.source.sourceCode)
        self.setSourceClass(feature.source.key.classCode)
        self.setSourceId(feature.source.key.itemId)
        self.setSourceFile(feature.source.filename)

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
