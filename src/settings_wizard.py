# -*- coding: utf-8 -*-
"""
/***************************************************************************
                                      Ark
                                 A QGIS plugin
             QGIS Plugin for ARK, the Archaeological Recording Kit
                              -------------------
        begin                : 2015-11-17
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
from PyQt4.QtCore import Qt
from PyQt4.QtGui import QWizard, QFileDialog

from settings_wizard_base import *

class SettingsWizard(QWizard, Ui_SettingsWizard):

    _advanced = False

    def __init__(self, parent=None):
        super(SettingsWizard, self).__init__(parent)
        self.setupUi(self)
        self.advancedButton.clicked.connect(self._advancedSettings)
        self.projectFolderButton.clicked.connect(self._selectProjectFolder)

    def advancedMode(self):
        return self._advanced

    def projectPath(self):
        return self.projectFolderEdit.text()

    def multiSiteProject(self):
        return self.multiSiteCheck.isChecked()

    def siteCode(self):
        return self.siteCodeEdit.text()

    def useArkDB(self):
        return self.useArkCheck.isChecked()

    def arkUrl(self):
        return self.arkUrlEdit.text()

    def _advancedSettings(self):
        self._advanced = True
        self.accept()

    def _selectProjectFolder(self):
        folderName = unicode(QFileDialog.getExistingDirectory(self, self.tr('Project Folder'), self.projectFolderEdit.text()))
        if folderName:
            self.projectFolderEdit.setText(folderName)
