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

from qgis.PyQt.QtCore import QDir
from qgis.PyQt.QtWidgets import QFileDialog, QWidget

from ArkSpatial.ark.core import Settings

from .ui.preferences_widget_base import Ui_PreferencesWidget


class PreferencesWidget(QWidget, Ui_PreferencesWidget):

    def __init__(self, parent=None):
        super().__init__(parent)
        self.setupUi(self)
        self.projectsFolderButton.clicked.connect(self._selectProjectsFolder)

    def load(self):
        self.setProjectsFolder(Settings.projectsFolder())
        self.setUserFullName(Settings.userFullName())
        self.setUserInitials(Settings.userInitials())
        self.setUserOrganisation(Settings.userOrganisation())

    def userFullName(self):
        return self.userFullNameEdit.text()

    def setUserFullName(self, fullName):
        if fullName is not None:
            self.userFullNameEdit.setText(fullName)

    def userInitials(self):
        return self.userInitialsEdit.text()

    def setUserInitials(self, initials):
        if initials is not None:
            self.userInitialsEdit.setText(initials)

    def userOrganisation(self):
        return self.organisationEdit.text()

    def setUserOrganisation(self, organisation):
        if organisation is not None:
            self.organisationEdit.setText(organisation)

    def projectsDir(self):
        return QDir(self.projectsFolder())

    def projectsFolder(self):
        return self.projectsFolderEdit.text()

    def setProjectsFolder(self, path):
        if path is not None:
            self.projectsFolderEdit.setText(path)

    def _selectProjectsFolder(self):
        path = str(
            QFileDialog.getExistingDirectory(self, self.tr('Project Folder'), self.projectsFolder())
        )
        if path:
            self.setProjectsFolder(path)
