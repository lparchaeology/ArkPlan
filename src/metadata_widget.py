# -*- coding: utf-8 -*-
"""
/***************************************************************************
                                      Ark
                                 A QGIS plugin
             QGIS Plugin for ARK, the Archaeological Recording Kit
                              -------------------
        begin                : 2015-10-21
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

from PyQt4 import uic
from PyQt4.QtCore import Qt, pyqtSignal
from PyQt4.QtGui import QWidget

import metadata_widget_base
from metadata import Metadata

class MetadataWidget(QWidget, metadata_widget_base.Ui_MetadataWidget):

    _md = Metadata()

    def __init__(self, parent=None):
        super(MetadataWidget, self).__init__(parent)
        self.setupUi(self)

    def initGui(self):

        self._md.siteCodeChanged.connect(self._setSiteCode)
        self._md.sourceCodeChanged.connect(self._setSourceCode)
        self._md.sourceClassChanged.connect(self._setSourceClass)
        self._md.sourceIdChanged.connect(self._setSourceId)
        self._md.sourceFileChanged.connect(self._setSourceFile)
        self._md.commentChanged.connect(self._setComment)
        self._md.createdByChanged.connect(self._setCreatedBy)

        self.siteEdit.textChanged.connect(self._md.setSiteCode)
        self.sourceCodeCombo.currentIndexChanged.connect(self._sourceCodeIndexChanged)
        self.sourceClassCombo.currentIndexChanged.connect(self._sourceClassIndexChanged)
        self.sourceIdSpin.valueChanged.connect(self._md.setSourceId)
        self.sourceFileEdit.textChanged.connect(self._md.setSourceFile)
        self.commentEdit.textChanged.connect(self._md.setComment)
        self.createdByEdit.textChanged.connect(self._md.setCreatedBy)

    def metadata(self):
        return self._md

    def initSourceCodes(self, sourceCodes):
        self.sourceCodeCombo.clear()
        for sourceCode in sourceCodes:
            self.sourceCodeCombo.addItem(sourceCode[0], sourceCode[1])
        self._md.setSourceCode(self.sourceCodeCombo.itemData(0))

    def initSourceClasses(self, sourceClasses):
        self.sourceClassCombo.clear()
        for sourceClass in sourceClasses:
            self.sourceClassCombo.addItem(sourceClass[0], sourceClass[1])
        self._md.setSourceClass(self.sourceClassCombo.itemData(0))

    def _setSiteCode(self, siteCode):
        self.siteEdit.setText(siteCode)

    def _setComment(self, comment):
        self.commentEdit.setText(comment)

    def _sourceCodeIndexChanged(self, idx):
        self._md.setSourceCode(self.sourceCodeCombo.itemData(idx))

    def _setSourceCode(self, sourceCode):
        self.sourceCodeCombo.setCurrentIndex(self.sourceCodeCombo.findData(sourceCode))

    def _sourceClassIndexChanged(self, idx):
        self._md.setSourceClass(self.sourceClassCombo.itemData(idx))

    def _setSourceClass(self, sourceClass):
        self.sourceClassCombo.setCurrentIndex(self.sourceClassCombo.findData(sourceClass))

    def _setSourceId(self, sourceId):
        if sourceId is None:
            self.sourceIdSpin.setValue(0)
        else:
            self.sourceIdSpin.setValue(sourceId)

    def _setSourceFile(self, sourceFile):
        self.sourceFileEdit.setText(sourceFile)

    def _setCreatedBy(self, createdBy):
        self.createdByEdit.setText(createdBy)
