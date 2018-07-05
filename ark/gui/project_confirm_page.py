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

import os

from qgis.PyQt.QtWidgets import QFileDialog, QWizardPage

from ArkSpatial.ark.lib import Project, utils

from ArkSpatial.ark.core import Settings


class ProjectConfirmPage(QWizardPage):

    def initializePage(self):
        self.registerField("newProject", self.wizard().newProjectCheck)
        self.registerField("projectFolder", self.wizard().projectFolderEdit)
        self.registerField("projectFilename", self.wizard().projectFilenameEdit)
        if Project.exists() and not Settings.isProjectConfigured():
            self.wizard().newProjectCheck.setChecked(False)
            self.wizard().newProjectCheck.setEnabled(True)
        else:
            self.wizard().newProjectCheck.setChecked(True)
            self.wizard().newProjectCheck.setEnabled(False)
        self._newProjectChanged()
        self.wizard().newProjectCheck.stateChanged.connect(self._newProjectChanged)
        self.wizard().projectFolderButton.clicked.connect(self._selectProjectFolder)

    def validatePage(self):
        if self.field("newProject"):
            return self.field("projectFolder") != '' and self.field("projectFilename") != ''
        return True

    def _newProjectChanged(self):
        checked = self.wizard().newProjectCheck.isChecked()
        self.wizard().projectFolderEdit.setEnabled(checked)
        self.wizard().projectFolderButton.setEnabled(checked)
        self.wizard().projectFilenameEdit.setEnabled(checked)
        if checked:
            self.setField('projectFolder', self._defaultProjectFolder())
            self.setField('projectFilename', self._defaultFileName())
        else:
            self.setField('projectFolder', Settings.projectPath())
            self.setField('projectFilename', Project.fileInfo().baseName())

    def _selectProjectFolder(self):
        defaultPath = self.field("projectFolder")
        if defaultPath == '':
            defaultPath = Settings.projectsFolder()
        folderName = str(
            QFileDialog.getExistingDirectory(self, self.tr('Project Folder'), defaultPath)
        )
        if folderName:
            self.setField("projectFolder", folderName)

    def _defaultProjectFolder(self):
        projectFolderName = self.field("projectCode") + ' - ' + self.field("projectName")
        return os.path.join(Settings.projectsFolder(), projectFolderName, 'GIS')

    def _defaultFileName(self):
        if (self.field("siteCode") != ''):
            return str(self.field("siteCode")) + '_' + str(Settings.userInitials())
        else:
            return str(self.field("projectCode")) + '_' + str(Settings.userInitials())
