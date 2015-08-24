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
        self.projectFolderEdit.setText(project.projectPath())
        self.projectFolderButton.clicked.connect(self._selectProjectFolder)
        self.multiSiteCheck.setChecked(project.multiSiteProject())
        self.siteCodeEdit.setText(project.siteCode())
        self.prependSiteCodeCheck.setChecked(project.prependSiteCode())
        if project.useCustomStyles():
            self.defaultStylesCheck.setChecked(False)
            self.styleFolderEdit.setText(project.stylePath())
            self.styleFolderEdit.setEnabled(True)
            self.styleFolderButton.setEnabled(True)
        self.defaultStylesCheck.toggled.connect(self._toggleDefaultStyle)
        self.styleFolderButton.clicked.connect(self._selectStyleFolder)
        self.useArkCheck.setChecked(project.useArkDB())
        if project.isConfigured():
            self.useArkCheck.setEnabled(False)

        # Grid tab settings
        self.gridFolderEdit.setText(project.modulePath('grid'))
        self.gridFolderButton.clicked.connect(self._selectGridFolder)
        self.gridGroupNameEdit.setText(project.layersGroupName('grid'))
        self.gridPointsNameEdit.setText(project.pointsBaseName('grid'))
        self.gridLinesNameEdit.setText(project.linesBaseName('grid'))
        self.gridPolygonsNameEdit.setText(project.polygonsBaseName('grid'))

        # Base tab settings
        self.baseFolderEdit.setText(project.modulePath('base'))
        self.baseFolderButton.clicked.connect(self._selectBaseFolder)
        self.baseGroupNameEdit.setText(project.layersGroupName('base'))
        self.basePointsNameEdit.setText(project.pointsBaseName('base'))
        self.baseLinesNameEdit.setText(project.linesBaseName('base'))
        self.basePolygonsNameEdit.setText(project.polygonsBaseName('base'))

        # Plan tab settings
        self.planVectorFolderEdit.setText(project.modulePath('plan'))
        self.planVectorFolderButton.clicked.connect(self._selectPlanFolder)
        self.planGroupNameEdit.setText(project.layersGroupName('plan'))
        self.planBufferGroupNameEdit.setText(project.buffersGroupName('plan'))
        self.planPointsNameEdit.setText(project.pointsBaseName('plan'))
        self.planLinesNameEdit.setText(project.linesBaseName('plan'))
        self.planPolygonsNameEdit.setText(project.polygonsBaseName('plan'))
        self.planRasterFolderEdit.setText(project.planRasterPath())
        self.planRasterFolderButton.clicked.connect(self._selectPlanRasterFolder)
        self.separateGeorefFolderCheck.setChecked(project.separateProcessedPlanFolder())
        self.planTransparencySpin.setValue(project.planTransparency())

    def accept(self):
        # Project tab settings
        self._project.setProjectPath(self.projectFolderEdit.text())
        self._project.setMultiSiteProject(self.multiSiteCheck.isChecked())
        self._project.setSiteCode(self.siteCodeEdit.text())
        self._project.setPrependSiteCode(self.prependSiteCodeCheck.isChecked())
        self._project.setUseCustomStyles(self.styleFolderEdit.text() != '')
        self._project.setStylePath(self.styleFolderEdit.text())
        self._project.setUseArkDB(self.useArkCheck.isChecked())

        # Grid tab settings
        self._project.setModulePath('grid', self.gridFolderEdit.text())
        self._project.setLayersGroupName('grid', self.gridGroupNameEdit.text())
        self._project.setPointsBaseName('grid', self.gridPointsNameEdit.text())
        self._project.setLinesBaseName('grid', self.gridLinesNameEdit.text())
        self._project.setPolygonsBaseName('grid', self.gridPolygonsNameEdit.text())

        # Base tab settings
        self._project.setModulePath('base', self.baseFolderEdit.text())
        self._project.setLayersGroupName('base', self.baseGroupNameEdit.text())
        self._project.setPointsBaseName('base', self.basePointsNameEdit.text())
        self._project.setLinesBaseName('base', self.baseLinesNameEdit.text())
        self._project.setPolygonsBaseName('base', self.basePolygonsNameEdit.text())

        # Plan tab settings
        self._project.setModulePath('plan', self.planVectorFolderEdit.text())
        self._project.setLayersGroupName('plan', self.planGroupNameEdit.text())
        self._project.setBuffersGroupName('plan', self.planBufferGroupNameEdit.text())
        self._project.setPointsBaseName('plan', self.planPointsNameEdit.text())
        self._project.setLinesBaseName('plan', self.planLinesNameEdit.text())
        self._project.setPolygonsBaseName('plan', self.planPolygonsNameEdit.text())
        self._project.setPlanRasterPath(self.planRasterFolderEdit.text())
        self._project.setSeparateProcessedPlanFolder(self.separateGeorefFolderCheck.isChecked())
        self._project.setPlanTransparency(self.planTransparencySpin.value())

        return super(SettingsDialog, self).accept()

    def _selectProjectFolder(self):
        folderName = unicode(QFileDialog.getExistingDirectory(self, self.tr('Project Folder'), self.projectFolderEdit.text()))
        if folderName:
            self.projectFolderEdit.setText(folderName)

    def _selectGridFolder(self):
        folderName = unicode(QFileDialog.getExistingDirectory(self, self.tr('Grid Folder'), self.gridFolderEdit.text()))
        if folderName:
            self.gridFolderEdit.setText(folderName)

    def _selectBaseFolder(self):
        folderName = unicode(QFileDialog.getExistingDirectory(self, self.tr('Base Folder'), self.baseFolderEdit.text()))
        if folderName:
            self.baseFolderEdit.setText(folderName)

    def _toggleDefaultStyle(self, useDefault):
        if useDefault:
            self.styleFolderEdit.setText('')
        self.styleFolderEdit.setEnabled(not useDefault)
        self.styleFolderButton.setEnabled(not useDefault)

    def _selectStyleFolder(self):
        folderName = unicode(QFileDialog.getExistingDirectory(self, self.tr('Style Folder'), self.styleFolderEdit.text()))
        if folderName:
            self.styleFolderEdit.setText(folderName)

    def _selectPlanFolder(self):
        folderName = unicode(QFileDialog.getExistingDirectory(self, self.tr('Plan Data Folder'), self.planVectorFolderEdit.text()))
        if folderName:
            self.planVectorFolderEdit.setText(folderName)

    def _selectPlanRasterFolder(self):
        folderName = unicode(QFileDialog.getExistingDirectory(self, self.tr('Plan Image Folder'), self.planRasterFolderEdit.text()))
        if folderName:
            self.planRasterFolderEdit.setText(folderName)

