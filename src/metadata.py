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

def _str(val):
    if val is None or val == QPyNullVariant(str) or val.strip() == '':
        return ''
    else:
        return str(val)

def _int(val):
    if val is None or val == QPyNullVariant(int):
        return 0
    else:
        return int(val)

def _val(val, attrVal=False):
    if attrVal and (val == '' or val <= 0):
        return None
    else:
        return val


class FeatureData(QObject):

    featureDataChanged = pyqtSignal()

    classCodeChanged = pyqtSignal(str)
    featureIdChanged = pyqtSignal(int)
    categoryChanged = pyqtSignal(str)
    nameChanged = pyqtSignal(str)

    _classCode = ''
    _featureId = 0
    _category = ''
    _name = ''

    def __init__(self, parent=None):
        super(FeatureData, self).__init__(parent)

    def classCode(self, attrVal=False):
        return _val(self._classCode, attrVal)

    def setClassCode(self, classCode):
        if self._classCode != _str(classCode):
            self._setClassCode(classCode)
            self.featureDataChanged.emit()

    def _setClassCode(self, classCode):
        self._classCode = _str(classCode)
        self.classCodeChanged.emit(self._classCode)

    def featureId(self, attrVal=False):
        return _val(self._featureId, attrVal)

    def setFeatureId(self, featureId):
        if self._featureId == _int(featureId):
            return
        self._setFeatureId(featureId)
        self.featureDataChanged.emit()

    def _setFeatureId(self, featureId):
        self._featureId = _int(featureId)
        self.featureIdChanged.emit(self._featureId)

    def category(self, attrVal=False):
        return _val(self._category, attrVal)

    def setCategory(self, category):
        if self._category != _str(category):
            self._setCategory(category)
            self.featureDataChanged.emit()

    def _setCategory(self, category):
        self._category = _str(category)
        self.categoryChanged.emit(self._category)

    def name(self, attrVal=False):
        return _val(self._name, attrVal)

    def setName(self, name):
        if self._name != _str(name):
            self._setName(name)
            self.featureDataChanged.emit()

    def _setName(self, name):
        self._name = _str(name)
        self.nameChanged.emit(self._name)

    def validate(self):
        signalChanged = False
        if self._classCode is None or self._classCode == '':
            value, ok = QInputDialog.getText(None, 'Class Code', "Please enter a valid Class Code or Ark Module, e.g. 'cxt'")
            if ok and _str(value) != self._classCode:
                self._setClassCode(value)
                signalChanged = True
        if (self._featureId is None or self._featureId <= 0):
            value = 0
            ok = False
            if (self._classCode == 'cxt'):
                value, ok = QInputDialog.getInt(None, 'Context Number', 'Please enter a valid Context Number', 1, 1, 99999)
            else:
                value, ok = QInputDialog.getInt(None, 'Feature ID', 'Please enter a valid Feature ID Number', 1, 1, 99999)
            if ok and _int(value) != self._featureId:
                self._setFeatureId(value)
                signalChanged = True
        if self._category is None or self._category == '':
            value, ok = QInputDialog.getText(None, 'Category', "Please enter a valid category code, e.g. 'loe'")
            if ok and _str(value) != self._siteCode:
                self._setCategory(value)
                signalChanged = True
        if signalChanged:
            self.featureDataChanged.emit()


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

    def siteCode(self, attrVal=False):
        return _val(self._siteCode, attrVal)

    def setSiteCode(self, siteCode):
        if self._siteCode == _str(siteCode):
            return False
        self._setSiteCode(siteCode)
        self.metadataChanged.emit()

    def _setSiteCode(self, siteCode):
        self._siteCode = _str(siteCode)
        self.siteCodeChanged.emit(self._siteCode)

    def comment(self, attrVal=False):
        return _val(self._comment, attrVal)

    def setComment(self, comment):
        if self._comment == _str(comment):
            return
        self._setComment(comment)
        self.metadataChanged.emit()

    def _setComment(self, comment):
        self._comment = _str(comment)
        self.commentChanged.emit(self._comment)

    def sourceCode(self, attrVal=False):
        return _val(self._sourceCode, attrVal)

    def setSourceCode(self, sourceCode):
        if self._sourceCode == _str(sourceCode):
            return
        self._setSourceCode(sourceCode)
        self.metadataChanged.emit()

    def _setSourceCode(self, sourceCode):
        self._sourceCode = _str(sourceCode)
        self.sourceCodeChanged.emit(self._sourceCode)

    def sourceClass(self, attrVal=False):
        return _val(self._sourceClass, attrVal)

    def setSourceClass(self, sourceClass):
        if self._sourceClass == _str(sourceClass):
            return
        self._setSourceClass(sourceClass)
        self.metadataChanged.emit()

    def _setSourceClass(self, sourceClass):
        self._sourceClass = _str(sourceClass)
        self.sourceClassChanged.emit(self._sourceClass)

    def sourceId(self, attrVal=False):
        return _val(self._sourceId, attrVal)

    def setSourceId(self, sourceId):
        if self._sourceId == _int(sourceId):
            return
        self._setSourceId(sourceId)
        self.metadataChanged.emit()

    def _setSourceId(self, sourceId):
        self._sourceId = _int(sourceId)
        self.sourceIdChanged.emit(self._sourceId)

    def sourceFile(self, attrVal=False):
        return _val(self._sourceFile, attrVal)

    def setSourceFile(self, sourceFile):
        if self._sourceFile == _str(sourceFile):
            return
        self._setSourceFile(sourceFile)
        self.metadataChanged.emit()

    def _setSourceFile(self, sourceFile):
        self._sourceFile = _str(sourceFile)
        self.sourceFileChanged.emit(self._sourceFile)

    def createdBy(self, attrVal=False):
        return _val(self._createdBy, attrVal)

    def setCreatedBy(self, createdBy):
        if self._createdBy == _str(createdBy):
            return
        self._setCreatedBy(createdBy)
        self.metadataChanged.emit()

    def _setCreatedBy(self, createdBy):
        self._createdBy = _str(createdBy)
        self.createdByChanged.emit(self._createdBy)

    def validate(self):
        signalChanged = False
        if self._siteCode is None or self._siteCode == '':
            value, ok = QInputDialog.getText(None, 'Site Code', 'Please enter a valid Site Code')
            if ok and _str(value) != self._siteCode:
                self._setSiteCode(value)
                signalChanged = True
        if (self._sourceCode != 'svy') and (self._sourceId is None or self._sourceId <= 0):
            value, ok = QInputDialog.getInt(None, 'Source ID', 'Please enter a valid Source ID Number', 1, 1, 99999)
            if ok and _int(value) != self._sourceId:
                self._setSourceId(value)
                signalChanged = True
        if (self._sourceCode == 'drw' or self._sourceCode == 'unc' or self._sourceCode == 'svy') and (self._sourceFile is None or self._sourceFile == ''):
            value, ok = QInputDialog.getText(None, 'Source File', "Please enter the source file name")
            if ok and _str(value) != self._sourceFile:
                self._setSourceFile(value)
                signalChanged = True
        if self._createdBy is None or self._createdBy == '':
            value, ok = QInputDialog.getText(None, 'Created By', "Please enter your full name (e.g. 'Mortimer Wheeler')")
            if ok and _str(value) != self._createdBy:
                self._setCreatedBy(value)
                signalChanged = True
        if signalChanged:
            self.metadataChanged.emit()
