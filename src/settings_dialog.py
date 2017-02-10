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
from PyQt4.QtGui import QDialog, QFileDialog

from settings_dialog_base import *

class SettingsDialog(QDialog, Ui_SettingsDialogBase):

    _project = None # Project()

    def __init__(self, project, parent=None):
        super(SettingsDialog, self).__init__(parent)
        self._project = project

        self.setupUi(self)

        # Project tab settings
        self.multiSiteCheck.setChecked(project.multiSiteProject())
        self.siteCodeEdit.setText(project.siteCode())
        self.styleFolderCheck.setChecked(project.useCustomStyles())
        if project.useCustomStyles():
            self.styleFolderEdit.setEnabled(True)
            self.styleFolderButton.setEnabled(True)
        self.styleFolderButton.clicked.connect(self._selectStyleFolder)
        self.useArkCheck.setChecked(project.useArkDB())
        self.arkUrlEdit.setText(project.arkUrl())
        if project.isConfigured():
            self.useArkCheck.setEnabled(False)
        self.logUpdatesCheck.setChecked(project.logUpdates())

        # Drawings tab settings
        self.drawingTransparencySpin.setValue(project.drawingTransparency())
        self.georefFolderCheck.setChecked(project.useGeorefFolder())
        self.contextDrawingFolderCheck.setChecked(project.useCustomPath('cxt'))
        if project.useCustomPath('cxt'):
            self.contextDrawingFolderEdit.setEnabled(True)
            self.contextDrawingFolderButton.setEnabled(True)
        self.contextDrawingFolderEdit.setText(project.rasterGroupPath('cxt'))
        self.contextDrawingFolderButton.clicked.connect(self._selectContextDrawingFolder)
        if project.useCustomPath('pln'):
            self.planDrawingFolderEdit.setEnabled(True)
            self.planDrawingFolderButton.setEnabled(True)
        self.planDrawingFolderEdit.setText(project.rasterGroupPath('pln'))
        self.planDrawingFolderButton.clicked.connect(self._selectPlanDrawingFolder)
        if project.useCustomPath('sec'):
            self.sectionDrawingFolderEdit.setEnabled(True)
            self.sectionDrawingFolderButton.setEnabled(True)
        self.sectionDrawingFolderEdit.setText(project.rasterGroupPath('sec'))
        self.sectionDrawingFolderButton.clicked.connect(self._selectSectionDrawingFolder)

    def accept(self):
        # Project tab settings
        self._project.setMultiSiteProject(self.multiSiteCheck.isChecked())
        self._project.setSiteCode(self.siteCodeEdit.text())
        self._project.setStylePath(self.styleFolderCheck.isChecked(), self.styleFolderEdit.text())
        self._project.setUseArkDB(self.useArkCheck.isChecked())
        self._project.setArkUrl(self.arkUrlEdit.text())
        self._project.setLogUpdates(self.logUpdatesCheck.isChecked())

        # Drawings tab settings
        self._project.setRasterGroupPath('cxt', self.contextDrawingFolderCheck.isChecked(), self.contextDrawingFolderEdit.text())
        self._project.setRasterGroupPath('pln', self.planDrawingFolderCheck.isChecked(), self.planDrawingFolderEdit.text())
        self._project.setRasterGroupPath('sec', self.sectionDrawingFolderCheck.isChecked(), self.sectionDrawingFolderEdit.text())
        self._project.setUseGeorefFolder(self.georefFolderCheck.isChecked())
        self._project.setDrawingTransparency(self.drawingTransparencySpin.value())

        return super(SettingsDialog, self).accept()

    def _toggleDefaultStyle(self, useDefault):
        if useDefault:
            self.styleFolderEdit.setText('')
        self.styleFolderEdit.setEnabled(not useDefault)
        self.styleFolderButton.setEnabled(not useDefault)

    def _selectStyleFolder(self):
        folderName = unicode(QFileDialog.getExistingDirectory(self, self.tr('Style Folder'), self.styleFolderEdit.text()))
        if folderName:
            self.styleFolderEdit.setText(folderName)

    def _selectContextDrawingFolder(self):
        folderName = unicode(QFileDialog.getExistingDirectory(self, self.tr('Context Drawing Folder'), self.contextDrawingFolderEdit.text()))
        if folderName:
            self.contextDrawingFolderEdit.setText(folderName)

    def _selectPlanDrawingFolder(self):
        folderName = unicode(QFileDialog.getExistingDirectory(self, self.tr('Plan Drawing Folder'), self.planDrawingFolderEdit.text()))
        if folderName:
            self.planDrawingFolderEdit.setText(folderName)

    def _selectSectionDrawingFolder(self):
        folderName = unicode(QFileDialog.getExistingDirectory(self, self.tr('Section Drawing Folder'), self.sectionDrawingFolderEdit.text()))
        if folderName:
            self.sectionDrawingFolderEdit.setText(folderName)
