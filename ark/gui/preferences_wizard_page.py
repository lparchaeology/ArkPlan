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

from qgis.PyQt.QtWidgets import QWizardPage


class PreferencesWizardPage(QWizardPage):

    def initializePage(self):
        self.registerField("projectsFolder*", self.wizard().preferences().projectsFolderEdit)
        self.registerField("userFullName*", self.wizard().preferences().userFullNameEdit)
        self.registerField("userInitials*", self.wizard().preferences().userInitialsEdit)
        self.registerField("organisation", self.wizard().preferences().organisationEdit)
        self.wizard().preferences().load()
