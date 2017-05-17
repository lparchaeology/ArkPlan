# -*- coding: utf-8 -*-
"""
/***************************************************************************
                                ARK Spatial
                    A QGIS plugin for Archaeological Recording.
        Part of the Archaeological Recording Kit by L-P : Archaeology
                        http://ark.lparchaeology.com
                              -------------------
        begin                : 2014-12-07
        git sha              : $Format:%H$
        copyright            : 2014, 2015 by L-P : Heritage LLP
        email                : ark@lparchaeology.com
        copyright            : 2014, 2015 by John Layt
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

from PyQt4.QtCore import Qt
from PyQt4.QtGui import QWizardPage

class FolderPage(QWizardPage):

    def initializePage(self):
        self.registerField("projectFolder*", self.wizard().projectFolderEdit)

class ProjectPage(QWizardPage):

    def initializePage(self):
        self.registerField("projectCode*", self.wizard().projectCodeEdit)
        self.registerField("projectName*", self.wizard().projectNameEdit)
        self.registerField("siteCodes", self.wizard().siteCodesEdit)
        self.registerField("arkUrl", self.wizard().arkUrlEdit)

class UserPage(QWizardPage):

    def initializePage(self):
        self.registerField("userFullname*", self.wizard().userFullnameEdit)
        self.registerField("userInitials*", self.wizard().userInitialsEdit)
        self.registerField("arkUserId", self.wizard().arkUserIdEdit)

class ConfirmPage(QWizardPage):

    def initializePage(self):
        self.registerField("projectFile*", self.wizard().projectFileEdit)
        projectFile = self.field("projectCode") + '_' + self.field("userInitials")
        self.setField('projectFile', projectFile)
