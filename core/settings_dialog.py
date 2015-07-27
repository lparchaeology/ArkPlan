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

        # Features tab settings
        self.featuresFolderEdit.setText(project.modulePath('features'))
        self.featuresFolderButton.clicked.connect(self._selectFeaturesFolder)
        self.featuresGroupNameEdit.setText(project.layersGroupName('features'))
        self.featuresBufferGroupNameEdit.setText(project.buffersGroupName('features'))
        self.featuresPointsNameEdit.setText(project.pointsBaseName('features'))
        self.featuresLinesNameEdit.setText(project.linesBaseName('features'))
        self.featuresPolygonsNameEdit.setText(project.polygonsBaseName('features'))

        # Context tab settings
        self.contextsFolderEdit.setText(project.modulePath('contexts'))
        self.contextsFolderButton.clicked.connect(self._selectContextsFolder)
        self.contextsGroupNameEdit.setText(project.layersGroupName('contexts'))
        self.contextsBufferGroupNameEdit.setText(project.buffersGroupName('contexts'))
        self.contextsPointsNameEdit.setText(project.pointsBaseName('contexts'))
        self.contextsLinesNameEdit.setText(project.linesBaseName('contexts'))
        self.contextsPolygonsNameEdit.setText(project.polygonsBaseName('contexts'))
        self.contextsSchemaNameEdit.setText(project.schemaBaseName('contexts'))

        # Plan tab settings
        self.planFolderEdit.setText(project.planPath())
        self.planFolderButton.clicked.connect(self._selectPlanFolder)
        self.separatePlansCheck.setChecked(project.separatePlanFolders())
        self.planTransparencySpin.setValue(project.planTransparency())

    def accept(self):
        # Project tab settings
        self._project.setProjectPath(self.projectFolderEdit.text())
        self._project.setMultiSiteProject(self.multiSiteCheck.isChecked())
        self._project.setSiteCode(self.siteCodeEdit.text())
        self._project.setPrependSiteCode(self.prependSiteCodeCheck.isChecked())
        self._project.setUseCustomStyles(self.styleFolderEdit.text() != '')
        self._project.setStylePath(self.styleFolderEdit.text())

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

        # Features tab settings
        self._project.setModulePath('features', self.featuresFolderEdit.text())
        self._project.setLayersGroupName('features', self.featuresGroupNameEdit.text())
        self._project.setBuffersGroupName('features', self.featuresBufferGroupNameEdit.text())
        self._project.setPointsBaseName('features', self.featuresPointsNameEdit.text())
        self._project.setLinesBaseName('features', self.featuresLinesNameEdit.text())
        self._project.setPolygonsBaseName('features', self.featuresPolygonsNameEdit.text())

        # Contexts tab settings
        self._project.setModulePath('contexts', self.contextsFolderEdit.text())
        self._project.setLayersGroupName('contexts', self.contextsGroupNameEdit.text())
        self._project.setBuffersGroupName('contexts', self.contextsBufferGroupNameEdit.text())
        self._project.setPointsBaseName('contexts', self.contextsPointsNameEdit.text())
        self._project.setLinesBaseName('contexts', self.contextsLinesNameEdit.text())
        self._project.setPolygonsBaseName('contexts', self.contextsPolygonsNameEdit.text())
        self._project.setSchemaBaseName('contexts', self.contextsSchemaNameEdit.text())

        # Plan tab settings
        self._project.setPlanPath(self.planFolderEdit.text())
        self._project.setSeparatePlanFolders(self.separatePlansCheck.isChecked())
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

    def _selectFeaturesFolder(self):
        folderName = unicode(QFileDialog.getExistingDirectory(self, self.tr('Features Folder'), self.featuresFolderEdit.text()))
        if folderName:
            self.featuresFolderEdit.setText(folderName)

    def _selectContextsFolder(self):
        folderName = unicode(QFileDialog.getExistingDirectory(self, self.tr('Contexts Folder'), self.contextsFolderEdit.text()))
        if folderName:
            self.contextsFolderEdit.setText(folderName)

    def _selectPlanFolder(self):
        folderName = unicode(QFileDialog.getExistingDirectory(self, self.tr('Plan Folder'), self.planFolderEdit.text()))
        if folderName:
            self.planFolderEdit.setText(folderName)

