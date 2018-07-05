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

from qgis.PyQt.QtWidgets import QDialog, QFileDialog

from ArkSpatial.ark.core import Settings

from .ui.settings_dialog_base import Ui_SettingsDialogBase


class SettingsDialog(QDialog, Ui_SettingsDialogBase):

    def __init__(self, parent=None):
        super(SettingsDialog, self).__init__(parent)
        self.setupUi(self)

        # Settings tab settings
        self.siteCodeEdit.setText(Settings.siteCode())
        self.styleFolderCheck.setChecked(Settings.useCustomStyles())
        if Settings.useCustomStyles():
            self.styleFolderEdit.setEnabled(True)
            self.styleFolderButton.setEnabled(True)
        self.styleFolderButton.clicked.connect(self._selectStyleFolder)
        self.arkUrlEdit.setText(Settings.arkUrl())
        if Settings.isSettingsConfigured():
            self.useArkCheck.setEnabled(False)
        self.logUpdatesCheck.setChecked(Settings.logUpdates())

        # Drawings tab settings
        self.drawingTransparencySpin.setValue(Settings.drawingTransparency())
        self.georefFolderCheck.setChecked(Settings.useGeorefFolder())
        self.contextDrawingFolderCheck.setChecked(Settings.useCustomDrawingPath('context'))
        if Settings.useCustomDrawingPath('context'):
            self.contextDrawingFolderEdit.setEnabled(True)
            self.contextDrawingFolderButton.setEnabled(True)
        self.contextDrawingFolderEdit.setText(Settings.drawingPath('context'))
        self.contextDrawingFolderButton.clicked.connect(self._selectContextDrawingFolder)
        if Settings.useCustomDrawingPath('plan'):
            self.planDrawingFolderEdit.setEnabled(True)
            self.planDrawingFolderButton.setEnabled(True)
        self.planDrawingFolderEdit.setText(Settings.drawingPath('plan'))
        self.planDrawingFolderButton.clicked.connect(self._selectPlanDrawingFolder)
        if Settings.useCustomDrawingPath('section'):
            self.sectionDrawingFolderEdit.setEnabled(True)
            self.sectionDrawingFolderButton.setEnabled(True)
        self.sectionDrawingFolderEdit.setText(Settings.drawingPath('section'))
        self.sectionDrawingFolderButton.clicked.connect(self._selectSectionDrawingFolder)

    def accept(self):
        # Settings tab settings
        Settings.setSiteCode(self.siteCodeEdit.text())
        Settings.setStylePath(self.styleFolderCheck.isChecked(), self.styleFolderEdit.text())
        Settings.setArkUrl(self.arkUrlEdit.text())
        Settings.setLogUpdates(self.logUpdatesCheck.isChecked())

        # Drawings tab settings
        Settings.setDrawingPath(
            'context', self.contextDrawingFolderCheck.isChecked(), self.contextDrawingFolderEdit.text())
        Settings.setDrawingPath('plan', self.planDrawingFolderCheck.isChecked(), self.planDrawingFolderEdit.text())
        Settings.setDrawingPath(
            'section', self.sectionDrawingFolderCheck.isChecked(), self.sectionDrawingFolderEdit.text())
        Settings.setUseGeorefFolder(self.georefFolderCheck.isChecked())
        Settings.setDrawingTransparency(self.drawingTransparencySpin.value())

        return super(SettingsDialog, self).accept()

    def _toggleDefaultStyle(self, useDefault):
        if useDefault:
            self.styleFolderEdit.setText('')
        self.styleFolderEdit.setEnabled(not useDefault)
        self.styleFolderButton.setEnabled(not useDefault)

    def _selectStyleFolder(self):
        folderName = str(QFileDialog.getExistingDirectory(
            self, self.tr('Style Folder'), self.styleFolderEdit.text()))
        if folderName:
            self.styleFolderEdit.setText(folderName)

    def _selectContextDrawingFolder(self):
        folderName = str(QFileDialog.getExistingDirectory(
            self, self.tr('Context Drawing Folder'), self.contextDrawingFolderEdit.text()))
        if folderName:
            self.contextDrawingFolderEdit.setText(folderName)

    def _selectPlanDrawingFolder(self):
        folderName = str(QFileDialog.getExistingDirectory(
            self, self.tr('Plan Drawing Folder'), self.planDrawingFolderEdit.text()))
        if folderName:
            self.planDrawingFolderEdit.setText(folderName)

    def _selectSectionDrawingFolder(self):
        folderName = str(QFileDialog.getExistingDirectory(
            self, self.tr('Section Drawing Folder'), self.sectionDrawingFolderEdit.text()))
        if folderName:
            self.sectionDrawingFolderEdit.setText(folderName)
