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

        for classCode in Config.classCodes:
            if classCode['plan']:
                self.classCombo.addItem(classCode['label'], classCode['code'])
            if classCode['source']:
                self.sourceClassCombo.addItem(classCode['label'], classCode['code'])
        self._md.setClass(self.sourceClassCombo.itemData(0))
        self._md.setSourceClass(self.sourceClassCombo.itemData(0))

        for sourceCode in Config.sourceCodes:
            self.sourceCodeCombo.addItem(sourceCode['label'], sourceCode['code'])
        self._md.setSourceCode(self.sourceCodeCombo.itemData(0))

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
