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

from PyQt4.QtGui import QFileDialog, QWizardPage

from ArkSpatial.ark.core import Settings


class PreferencesWizardPage(QWizardPage):

    def initializePage(self):
        self.registerField("projectsFolder*", self.wizard().preferencesWidget.projectsFolderEdit)
        self.registerField("userFullName*", self.wizard().preferencesWidget.userFullNameEdit)
        self.registerField("userInitials*", self.wizard().preferencesWidget.userInitialsEdit)
        self.registerField("organisation", self.wizard().preferencesWidget.organisationEdit)
        self.setField('userFullName', Settings.userFullName())
        self.setField('userInitials', Settings.userInitials())
        self.wizard().projectsFolderButton.clicked.connect(self._selectProjectsFolder)

    def _selectProjectsFolder(self):
        folderName = unicode(
            QFileDialog.getExistingDirectory(self, self.tr('Project Folder'), self.field("projectFolder"))
        )
        if folderName:
            self.setField("projectFolder", folderName)
