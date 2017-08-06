# -*- coding: utf-8 -*-
"""
/***************************************************************************
                                ARK Spatial
                    A QGIS plugin for Archaeological Recording.
        Part of the Archaeological Recording Kit by L-P : Archaeology
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

from PyQt4 import uic
from PyQt4.QtGui import QFileDialog, QWizard

from settings_wizard_base import Ui_SettingsWizard


class SettingsWizard(QWizard, Ui_SettingsWizard):

    def __init__(self, parent=None):
        super(SettingsWizard, self).__init__(parent)
        self.setupUi(self)
        self.projectFolderButton.clicked.connect(self._selectProjectFolder)

    def projectPath(self):
        return self.projectFolderEdit.text()

    def projectCode(self):
        return self.projectCodeEdit.text()

    def projectName(self):
        return self.projectNameEdit.text()

    def siteCodes(self):
        return self.siteCodesEdit.text()

    def arkUrl(self):
        return self.arkUrlEdit.text()

    def arkUserId(self):
        return self.arkUserIdEdit.text()

    def userFullname(self):
        return self.userFullnameEdit.text()

    def userInitials(self):
        return self.userInitialsEdit.text()

    def projectFile(self):
        return self.projectFileEdit.text()

    def _selectProjectFolder(self):
        folderName = unicode(QFileDialog.getExistingDirectory(
            self, self.tr('Project Folder'), self.projectFolderEdit.text()))
        if folderName:
            self.projectFolderEdit.setText(folderName)
