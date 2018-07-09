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

from qgis.PyQt.QtCore import QDir
from qgis.PyQt.QtWidgets import QAbstractItemView, QDialog, QDialogButtonBox

from ArkSpatial.ark.lib import utils
from ArkSpatial.ark.lib.core import ReturnPressedFilter

from ArkSpatial.ark.core import Config, Settings

from .ui.select_drawing_dialog_base import Ui_SelectDrawingDialog


class SelectDrawingDialog(QDialog, Ui_SelectDrawingDialog):

    def __init__(self, drawingType, siteCode='', georef=False, parent=None):
        super().__init__(parent)
        self.setupUi(self)

        self._dir = None  # QDir
        self._fileList = []
        self._georef = georef

        keys = sorted(Config.classCodes.keys())
        for key in keys:
            classCode = Config.classCodes[key]
            if classCode['drawing']:
                self.drawingTypeCombo.addItem(classCode['label'], classCode['class'])
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
            self._dir = Settings.georefDrawingDir(drawingType)
        else:
            self._dir = Settings.drawingDir(drawingType)
        self._dir.setFilter(QDir.Files | QDir.NoDotAndDotDot)
        self.siteCodeEdit.setText(siteCode)
        self.findButton.clicked.connect(self._findFiles)
        self._findFiles()

    def accept(self):
        self._fileList = []
        selectedItems = self.fileList.selectedItems()
        for item in selectedItems:
            self._fileList.append(self._dir.absoluteFilePath(item.text()))
        return super().accept()

    def selectedFiles(self):
        return self._fileList

    def _findFiles(self):
        drawingType = self.drawingTypeCombo.itemData(self.drawingTypeCombo.currentIndex())
        drawingCode = Config.drawings[drawingType]['code']
        if self._georef:
            self._dir.setPath(Settings.georefDrawingPath(drawingType))
        else:
            self._dir.setPath(Settings.drawingPath(drawingType))
        name = drawingCode + '_' + self._str(self.siteCodeEdit.text()) + '_' + self._str(self.idSpin.value())
        if self.eastingSpin.value() > 0 or self.northingSpin.value() > 0:
            name = name + '_' + self._str(self.eastingSpin.value()) + 'e' + self._str(self.northingSpin.value()) + 'n'
        nameList = []
        if self._georef:
            nameList.append(name + '_r.tif')
            nameList.append(name + '_modified.tif')
            nameList.append(name + '_*_r.tif')
            nameList.append(name + '_*_modified.tif')
        else:
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
