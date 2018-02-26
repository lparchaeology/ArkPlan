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

from PyQt4.QtGui import QWidget

from ArkSpatial.ark.core import Settings

from .ui.server_widget_base import Ui_ServerWidget


class ServerWidget(QWidget, Ui_ServerWidget):

    def __init__(self, parent=None):
        super(ServerWidget, self).__init__(parent)
        self.setupUi(self)

    def load(self):
        self.setUrl(Settings.serverUrl())
        self.setUser(Settings.serverUser())
        self.setPassword(Settings.serverPassword())

    def loadSite(self):
        self.setUrl(Settings.siteServerUrl())
        self.setUser(Settings.siteServerUser())
        self.setPassword(Settings.siteServerPassword())

    def url(self):
        return self.urlEdit.text()

    def setUrl(self, url):
        if url is not None:
            self.urlEdit.setText(url)

    def user(self):
        return self.userEdit.text()

    def setUser(self, user):
        if user is not None:
            self.userEdit.setText(user)

    def password(self):
        return self.passwordEdit.text()

    def setPassword(self, password):
        if password is not None:
            self.passwordEdit.setText(password)
