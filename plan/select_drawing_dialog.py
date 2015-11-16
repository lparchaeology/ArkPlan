# -*- coding: utf-8 -*-
"""
/***************************************************************************
                                      Ark
                                 A QGIS plugin
             QGIS Plugin for ARK, the Archaeological Recording Kit
                              -------------------
        begin                : 2015-11-13
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

import os.path

from PyQt4 import uic
from PyQt4.QtCore import Qt, QDir
from PyQt4.QtGui import QDialog, QDialogButtonBox, QAbstractItemView

from select_drawing_dialog_base import *
from schematic_dock import ReturnPressedFilter

from ..config import Config

class SelectDrawingDialog(QDialog, Ui_SelectDrawingDialog):

    _dir = None # QDir
    _fileList = []

    def __init__(self, project, drawingType, siteCode='', georef=False, parent=None):
        super(SelectDrawingDialog, self).__init__(parent)
        self.setupUi(self)
        self._project = project
        self._georef = georef

        for drawType in Config.drawingTypes:
            self.drawingTypeCombo.addItem(Config.groupDefaults[drawType]['label'], drawType)
        self.drawingTypeCombo.setCurrentIndex(self.drawingTypeCombo.findData(drawingType))
        self.drawingTypeCombo.currentIndexChanged.connect(self._findFiles)
        self.findFilter = ReturnPressedFilter(self)
        self.findFilter.returnPressed.connect(self._findFiles)
        self.siteCodeEdit.installEventFilter(self.findFilter)
        self.idSpin.installEventFilter(self.findFilter)
        self.eastingSpin.installEventFilter(self.findFilter)
        self.northingSpin.installEventFilter(self.findFilter)
        self.idSpin.lineEdit().selectAll()
        self.fileList.setSelectionMode(QAbstractItemView.ExtendedSelection)
        self.buttonBox.button(QDialogButtonBox.Open).setDefault(True)

        if georef:
            self._dir = QDir(project.georefDrawingPath(drawingType))
        else:
            self._dir = QDir(project.rawDrawingPath(drawingType))
        self._dir.setFilter(QDir.Files | QDir.NoDotAndDotDot)
        self.siteCodeEdit.setText(siteCode)
        self.findButton.clicked.connect(self._findFiles)
        self._findFiles()

    def accept(self):
        self._fileList = []
        selectedItems = self.fileList.selectedItems()
        for item in selectedItems:
            self._fileList.append(self._dir.absoluteFilePath(item.text()))
        return super(SelectDrawingDialog, self).accept()

    def selectedFiles(self):
        return self._fileList

    def _findFiles(self):
        drawingType = self.drawingTypeCombo.itemData(self.drawingTypeCombo.currentIndex())
        if self._georef:
            self._dir.setPath(self._project.georefDrawingPath(drawingType))
        else:
            self._dir.setPath(self._project.rawDrawingPath(drawingType))
        name = drawingType + '_' + self._str(self.siteCodeEdit.text()) + '_' + self._str(self.idSpin.value())
        if self.eastingSpin.value() > 0 or self.northingSpin.value() > 0:
            name = name + '_' + self._str(self.eastingSpin.value()) + 'e' + self._str(self.northingSpin.value()) + 'n'

        nameList = []
        nameList.append(name + '.png')
        nameList.append(name + '.tif')
        nameList.append(name + '.tiff')
        nameList.append(name + '_*.png')
        nameList.append(name + '_*.tif')
        nameList.append(name + '_*.tiff')

        self._dir.setNameFilters(nameList)
        files = self._dir.entryInfoList()
        self.fileList.clear()
        for fileInfo in files:
            self.fileList.addItem(fileInfo.fileName())
        self.fileList.setCurrentRow(0)
        self.buttonBox.button(QDialogButtonBox.Open).setEnabled(len(files) > 0)

    def _str(self, val):
        if val == '' or val == 0:
            return '*'
        return str(val)
