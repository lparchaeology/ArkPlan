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


class ServerWizardPage(QWizardPage):

    def initializePage(self):
        self.registerField("url", self.wizard().server().urlEdit)
        self.registerField("user", self.wizard().server().userEdit)
        self.registerField("password", self.wizard().server().passwordEdit)
        self.wizard().server().load()

    def validatePage(self):
        url = self.field("url")
        if url is None or url == "":
            return True
        user = self.field("user")
        password = self.field("password")
        if user is None or user == "" or password is None or password == "":
            return False
        return True
