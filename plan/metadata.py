# -*- coding: utf-8 -*-
"""
/***************************************************************************
                                      Ark
                                 A QGIS plugin
             QGIS Plugin for ARK, the Archaeological Recording Kit
                              -------------------
        begin                : 2015-03-02
        git sha              : $Format:%H$
        copyright            : (C) 2015 by L - P: Heritage LLP
        copyright            : (C) 2015 by John Layt
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

from PyQt4.QtCore import QObject, pyqtSignal
from PyQt4.QtGui import QInputDialog

class Metadata(QObject):

    metadataChanged = pyqtSignal()

    siteCodeChanged = pyqtSignal(str)
    sourceCodeChanged = pyqtSignal(str)
    sourceClassChanged = pyqtSignal(str)
    sourceIdChanged = pyqtSignal(int)
    sourceFileChanged = pyqtSignal(str)
    commentChanged = pyqtSignal(str)
    createdByChanged = pyqtSignal(str)

    _siteCode = ''
    _comment = ''
    _sourceCode = ''
    _sourceClass = ''
    _sourceId = 0
    _sourceFile = ''
    _createdBy = ''
    _createdOn = ''

    def __init__(self, parent=None):
        super(Metadata, self).__init__(parent)

    def siteCode(self):
        return self._siteCode

    def setSiteCode(self, siteCode):
        if self._siteCode == siteCode:
            return False
        self._setSiteCode(siteCode)
        self.metadataChanged.emit()

    def _setSiteCode(self, siteCode):
        self._siteCode = siteCode
        self.siteCodeChanged.emit(siteCode)

    def comment(self):
        return self._comment

    def setComment(self, comment):
        if self._comment == comment:
            return
        self._setComment(comment)
        self.metadataChanged.emit()

    def _setComment(self, comment):
        self._comment = comment
        self.commentChanged.emit(comment)

    def sourceCode(self):
        return self._sourceCode

    def setSourceCode(self, sourceCode):
        if self._sourceCode == sourceCode:
            return
        self._setSourceCode(sourceCode)
        self.metadataChanged.emit()

    def _setSourceCode(self, sourceCode):
        self._sourceCode = sourceCode
        self.sourceCodeChanged.emit(sourceCode)

    def sourceClass(self):
        return self._sourceClass

    def setSourceClass(self, sourceClass):
        if self._sourceClass == sourceClass:
            return
        self._setSourceClass(sourceClass)
        self.metadataChanged.emit()

    def _setSourceClass(self, sourceClass):
        self._sourceClass = sourceClass
        self.sourceClassChanged.emit(sourceClass)

    def sourceId(self):
        return self._sourceId

    def setSourceId(self, sourceId):
        if self._sourceId == sourceId:
            return
        self._setSourceId(sourceId)
        self.metadataChanged.emit()

    def _setSourceId(self, sourceId):
        self._sourceId = sourceId
        self.sourceIdChanged.emit(sourceId)

    def sourceFile(self):
        return self._sourceFile

    def setSourceFile(self, sourceFile):
        if self._sourceFile == sourceFile:
            return
        self._setSourceFile(sourceFile)
        self.metadataChanged.emit()

    def _setSourceFile(self, sourceFile):
        self._sourceFile = sourceFile
        self.sourceFileChanged.emit(sourceFile)

    def createdBy(self):
        return self._createdBy

    def setCreatedBy(self, createdBy):
        if self._createdBy == createdBy:
            return
        self._setCreatedBy(createdBy)
        self.metadataChanged.emit()

    def _setCreatedBy(self, createdBy):
        self._createdBy = createdBy
        self.createdByChanged.emit(createdBy)

    def validate(self):
        signalMetadata = False
        if self._siteCode is None or self._siteCode == '':
            value, ok = QInputDialog.getText(None, 'Site Code', 'Please enter a valid Site Code')
            if ok and value != self._siteCode:
                self._setSiteCode(value)
                signalMetadata = True
        if (self._sourceCode != 'svy') and (self._sourceId is None or self._sourceId <= 0):
            value, ok = QInputDialog.getInt(None, 'Source ID', 'Please enter a valid Source ID Number', 1, 1, 99999)
            if ok and value != self._sourceId:
                self._setSourceId(value)
                signalMetadata = True
        if (self._sourceCode == 'drw' or self._sourceCode == 'unc' or self._sourceCode == 'svy') and (self._sourceFile is None or self._sourceFile == ''):
            value, ok = QInputDialog.getText(None, 'Source File', "Please enter the source file name")
            if ok and value != self._sourceFile:
                self._setSourceFile(value)
                signalMetadata = True
        if self._createdBy is None or self._createdBy == '':
            value, ok = QInputDialog.getText(None, 'Created By', "Please enter your full name (e.g. 'Mortimer Wheeler')")
            if ok and value != self._siteCode:
                self._setCreatedBy(value)
                signalMetadata = True
        if signalMetadata:
            self.metadataChanged.emit()
