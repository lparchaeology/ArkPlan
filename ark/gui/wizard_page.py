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

from PyQt4.QtGui import QComboBox, QFileDialog, QWizardPage

from qgis.gui import QgsProjectionSelectionWidget

from ArkSpatial.ark.lib import Application, Project, utils

from ArkSpatial.ark.core import Settings
from ArkSpatial.ark.pyARK import Ark


class PreferencesPage(QWizardPage):

    def initializePage(self):
        self.registerField("projectsFolder*", self.wizard().projectsFolderEdit)
        self.registerField("userFullName*", self.wizard().userFullNameEdit)
        self.registerField("userInitials*", self.wizard().userInitialsEdit)
        self.registerField("organisation", self.wizard().organisationEdit)
        self.setField('userFullName', Settings.userFullName())
        self.setField('userInitials', Settings.userInitials())
        self.wizard().projectsFolderButton.clicked.connect(self._selectProjectsFolder)

    def _selectProjectsFolder(self):
        folderName = unicode(
            QFileDialog.getExistingDirectory(self, self.tr('Project Folder'), self.field("projectFolder"))
        )
        if folderName:
            self.setField("projectFolder", folderName)


class GlobalPage(QWizardPage):

    crs = None

    def initializePage(self):
        self.crs = Application.projectDefaultCrs()
        self.wizard().crsWidget.setCrs(self.crs)
        self.wizard().crsWidget.setOptionVisible(QgsProjectionSelectionWidget.LayerCrs, False)
        self.wizard().crsWidget.setOptionVisible(QgsProjectionSelectionWidget.ProjectCrs, True)
        self.wizard().crsWidget.setOptionVisible(QgsProjectionSelectionWidget.CurrentCrs, False)
        self.wizard().crsWidget.setOptionVisible(QgsProjectionSelectionWidget.DefaultCrs, False)
        self.wizard().crsWidget.setOptionVisible(QgsProjectionSelectionWidget.RecentCrs, True)
        self.wizard().crsWidget.crsChanged.connect(self._crsChanged)

    def _crsChanged(self, crs):
        self.crs = crs


class ProjectPage(QWizardPage):

    ark = None
    crs = None

    def initializePage(self):
        self.registerField("projectName*", self.wizard().projectNameEdit)
        self.registerField("siteCode", self.wizard().siteCodeEdit)
        self.registerField("locationEasting", self.wizard().locationEastingEdit)
        self.registerField("locationNorthing", self.wizard().locationNorthingEdit)
        self.registerField("siteRadius", self.wizard().siteRadiusSpin)

        self.crs = Application.projectDefaultCrs()
        self.wizard().crsWidget.setCrs(self.crs)
        self.wizard().crsWidget.setOptionVisible(QgsProjectionSelectionWidget.LayerCrs, False)
        self.wizard().crsWidget.setOptionVisible(QgsProjectionSelectionWidget.ProjectCrs, True)
        self.wizard().crsWidget.setOptionVisible(QgsProjectionSelectionWidget.CurrentCrs, False)
        self.wizard().crsWidget.setOptionVisible(QgsProjectionSelectionWidget.DefaultCrs, False)
        self.wizard().crsWidget.setOptionVisible(QgsProjectionSelectionWidget.RecentCrs, True)
        self.wizard().crsWidget.crsChanged.connect(self._crsChanged)

        url = self.field("arkUrl")
        if url is None or url == "":
            self.registerField("projectCode*", self.wizard().projectCodeCombo.lineEdit())
            return

        self.registerField("projectCode*", self.wizard().projectCodeCombo)
        self.wizard().projectCodeCombo.setMaxVisibleItems(10)
        self.wizard().projectCodeCombo.setInsertPolicy(QComboBox.NoInsert)
        self.wizard().projectNameEdit.setEnabled(False)
        self.wizard().siteCodeEdit.setEnabled(False)
        self.wizard().locationEastingEdit.setEnabled(False)
        self.wizard().locationNorthingEdit.setEnabled(False)
        self.wizard().projectCodeCombo.currentIndexChanged.connect(self._updateArkProject)

        user = self.field("arkUser")
        password = self.field("arkPassword")
        self.ark = Ark(url, user, password)
        projects = self.ark.getProjectList()
        self.wizard().projectCodeCombo.setMaxCount(len(projects))
        for key in utils.natsorted(projects.keys()):
            self.wizard().projectCodeCombo.addItem(projects[key], key)

    def validatePage(self):
        siteCode = self.field("siteCode")
        if siteCode is None or siteCode == "":
            self.setField("siteCode", self.wizard().projectCode())
        return True

    def _updateArkProject(self):
        utils.debug(self.field("projectCode"))
        project = self.wizard().projectCodeCombo.itemData(self.field("projectCode"))
        data = self.ark.getProjectDetails(project)
        self._setField('projectName', data)
        self._setField('siteCode', data)
        self._setField('locationEasting', data)
        self._setField('locationNorthing', data)

    def _setField(self, fieldName, data):
        value = None
        if fieldName in data:
            value = data[fieldName]
        self.setField(fieldName, value)

    def _crsChanged(self, crs):
        self.crs = crs


class UserPage(QWizardPage):

    def initializePage(self):
        self.registerField("userFullName*", self.wizard().userFullNameEdit)
        self.registerField("userInitials*", self.wizard().userInitialsEdit)
        self.setField('userFullName', Settings.userFullName())
        self.setField('userInitials', Settings.userInitials())


class ConfirmPage(QWizardPage):

    def initializePage(self):
        self.registerField("projectFolder*", self.wizard().projectFolderEdit)
        self.registerField("projectFile*", self.wizard().projectFileEdit)
        self.registerField("clearProject", self.wizard().clearProjectCheck)
        if Project.exists():
            self.setField('projectFolder', Project.filePath())
            self.setField('projectFile', Project.fileName())
            self._updateFilePath()
        else:
            self.setField('projectFile', self.field("siteCode"))
        self.wizard().projectFolderButton.clicked.connect(self._selectProjectFolder)

    def _updateFilePath(self):
        self.wizard().projectFullPath.setText(self.fullFilePath())

    def fullFilePath(self):
        return os.path.join(self.field('projectFolder'), self.field('projectFile')) + '.qgs'

    def _selectProjectFolder(self):
        folderName = unicode(
            QFileDialog.getExistingDirectory(self, self.tr('Project Folder'), self.field("projectFolder"))
        )
        if folderName:
            self.setField("projectFolder", folderName)
            self._updateFilePath()
