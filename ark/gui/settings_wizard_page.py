# -*- coding: utf-8 -*-
"""
/***************************************************************************
                                ARK Spatial
                    A QGIS plugin for Archaeological Recording.
    Part of the Archaeological Recording Kit by L - P : Archaeology.
                        http://ark.lparchaeology.com
                              -------------------
        copyright            : 2017 by L-P : Heritage LLP
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

from PyQt4.QtGui import QWizardPage, QComboBox

from qgis.core import QgsApplication

from ArkSpatial.ark.lib import Application, Project, utils

from ArkSpatial.ark.pyARK import Ark


class ServerPage(QWizardPage):

    def __init__(self):
        super(ServerPage, self).__init__()

    def initializePage(self):
        self.registerField("arkUrl", self.wizard().arkUrlEdit)
        self.registerField("arkUser", self.wizard().arkUserEdit)
        self.registerField("arkPassword", self.wizard().arkPasswordEdit)
        self.setField('arkUrl', Application.serverUrl())
        self.setField('arkUserId', Application.serverUser())
        self.setField('arkUserId', Application.serverPassword())

    def validatePage(self):
        url = self.field("arkUrl")
        if url is None or url == "":
            return True
        user = self.field("arkUser")
        password = self.field("arkPassword")
        if user is None or user == "" or password is None or password == "":
            return False
        return True


class ProjectPage(QWizardPage):

    ark = None

    def __init__(self):
        super(ProjectPage, self).__init__()

    def initializePage(self):
        url = self.field("arkUrl")
        if url is None or url == "":
            self.registerField("projectCode*", self.wizard().projectCodeCombo.lineEdit())
        else:
            self.registerField("projectCode*", self.wizard().projectCodeCombo)
            self.wizard().projectCodeCombo.setMaxVisibleItems(10)
            self.wizard().projectCodeCombo.setInsertPolicy(QComboBox.NoInsert)
            self.wizard().projectNameEdit.setEnabled(False)
            self.wizard().siteCodesEdit.setEnabled(False)
            self.wizard().locationEastingEdit.setEnabled(False)
            self.wizard().locationNorthingEdit.setEnabled(False)
        self.registerField("projectName*", self.wizard().projectNameEdit)
        self.registerField("siteCodes", self.wizard().siteCodesEdit)
        self.registerField("locationEasting", self.wizard().locationEastingEdit)
        self.registerField("locationNorthing", self.wizard().locationNorthingEdit)
        self.registerField("crs", self.wizard().crsEdit)
        self.setField('crs', Application.projectDefaultCrs().authid())
        if url is None or url == "":
            return
        user = self.field("arkUser")
        password = self.field("arkPassword")
        self.ark = Ark(url, user, password)
        response = self.ark.getItems('job_cd')
        if response.error:
            utils.debug(response.url)
            utils.debug(response.message)
            utils.debug(response.raw)
            return
        self.wizard().projectCodeCombo.setMaxCount(len(response.data['job']))
        for item in response.data['job']:
            self.wizard().projectCodeCombo.addItem(item["job_no"], item["job_cd"])


class UserPage(QWizardPage):

    def __init__(self):
        super(UserPage, self).__init__()

    def initializePage(self):
        self.registerField("userFullname*", self.wizard().userFullnameEdit)
        self.registerField("userInitials*", self.wizard().userInitialsEdit)
        self.setField('userFullname', QgsApplication.userFullName())
        initials = ''
        for name in self.field("userFullname").split(' '):
            initials += name[0]
        self.setField('userInitials', initials)


class ConfirmPage(QWizardPage):

    def __init__(self):
        super(ConfirmPage, self).__init__()

    def initializePage(self):
        self.registerField("projectFolder*", self.wizard().projectFolderEdit)
        self.registerField("projectFile*", self.wizard().projectFileEdit)
        if Project.exists():
            self.setField('projectFolder', Project.filePath())
            self.setField('projectFile', Project.fileName())
        else:
            projectFile = self.field("projectCode") + '_' + self.field("userInitials")
            self.setField('projectFile', projectFile)
