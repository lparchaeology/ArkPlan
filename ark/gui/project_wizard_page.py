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

from PyQt4.QtGui import QWizardPage

from ArkSpatial.ark.core import Settings


class ProjectWizardPage(QWizardPage):

    def initializePage(self):
        if Settings.useProjectServer():
            self.registerField("projectCode*", self.wizard().project().projectCodeCombo)
        else:
            self.registerField("projectCode*", self.wizard().project().projectCodeCombo.lineEdit())
        self.registerField("projectName*", self.wizard().project().projectNameEdit)
        self.registerField("siteCode", self.wizard().project().siteCodeEdit)
        self.registerField("locationEasting", self.wizard().project().locationEastingEdit)
        self.registerField("locationNorthing", self.wizard().project().locationNorthingEdit)
        self.wizard().project().load()
