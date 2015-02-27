# -*- coding: utf-8 -*-
"""
/***************************************************************************
 ArkPlanDialog
                                 A QGIS plugin
 Plugin to assist in digitising of Archaeological plans.
                             -------------------
        begin                : 2015-01-10
        git sha              : $Format:%H$
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
from PyQt4.QtCore import Qt, QSettings
from PyQt4.QtGui import QDialog, QFileDialog

from qgis.core import QgsProject

from project_settings_dialog_base import *

class ProjectSettingsDialog(QDialog, Ui_ProjectSettingsDialogBase):

    _pluginName = ''

    def __init__(self, pluginName, parent=None):
        super(ProjectSettingsDialog, self).__init__(parent)
        self.setupUi(self)
        self._pluginName = pluginName
        self._loadProjectSettings()
        self.dataFolderButton.clicked.connect(self.selectDataFolder)
        self.planFolderButton.clicked.connect(self.selectPlanFolder)

    def selectDataFolder(self):
        folderName = unicode(QFileDialog.getExistingDirectory(self, self.tr('Data Folder'), self.dataFolderEdit.text()))
        if folderName:
            self.dataFolderEdit.setText(folderName)

    def selectPlanFolder(self):
        folderName = unicode(QFileDialog.getExistingDirectory(self, self.tr('Plan Folder'), self.planFolderEdit.text()))
        if folderName:
            self.planFolderEdit.setText(folderName)

    def projectDataFolder(self):
        return self.dataFolderEdit.text()

    def projectSiteCode(self):
        return self.siteCodeEdit.text()

    def prependSiteCode(self):
        return self.prependSiteCodeCheck.isChecked()

    def projectPlanFolder(self):
        return self.planFolderEdit.text()

    def useRawProcessedFolders(self):
        return self.separatePlansCheck.isChecked()

    def planOpacity(self):
        return self.planOpacitySpin.value()

    def _loadProjectSettings(self):
        project = QgsProject.instance()
        self.dataFolderEdit.setText(project.readEntry(self._pluginName, 'projectDataFolder', '')[0])
        self.siteCodeEdit.setText(project.readEntry(self._pluginName, 'projectSiteCode', '')[0])
        self.prependSiteCodeCheck.setChecked(project.readBoolEntry(self._pluginName, 'prependSiteCode', True)[0])
        self.planFolderEdit.setText(project.readEntry(self._pluginName, 'projectPlanFolder', '')[0])
        self.separatePlansCheck.setChecked(project.readBoolEntry(self._pluginName, 'useRawProcessedFolders', True)[0])
        self.planOpacitySpin.setValue(project.readNumEntry(self._pluginName, 'planOpacity', 50)[0])
