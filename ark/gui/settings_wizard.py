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

from PyQt4.QtGui import QWizard

from .ui.settings_wizard_base import Ui_SettingsWizard


class SettingsWizard(QWizard, Ui_SettingsWizard):

    def __init__(self, parent=None):
        super(SettingsWizard, self).__init__(parent)
        self.setupUi(self)

    def arkUrl(self):
        return self.field('arkUrl')

    def arkUser(self):
        return self.field('arkUser')

    def arkPassword(self):
        return self.field('arkPassword')

    def projectCode(self):
        return self.projectCodeCombo.lineEdit().text()

    def projectName(self):
        return self.field('projectName')

    def siteCode(self):
        return self.field('siteCode')

    def locationEasting(self):
        return self.field('locationEasting')

    def locationNorthing(self):
        return self.field('locationNorthing')

    def crs(self):
        return self.field('crs')

    def userFullName(self):
        return self.field('userFullName')

    def userInitials(self):
        return self.field('userInitials')

    def projectPath(self):
        return self.field('projectFolder')

    def projectFile(self):
        return self.field('projectFile')
