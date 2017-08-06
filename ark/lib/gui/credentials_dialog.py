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

from PyQt4 import uic
from PyQt4.QtGui import QDialog

from credentials_dialog_base import Ui_CredentialsDialog


class CredentialsDialog(QDialog, Ui_CredentialsDialog):

    def __init__(self, parent=None):
        super(CredentialsDialog, self).__init__(parent)
        self.setupUi(self)
        self.passwordEdit.setText('anon')
        self.passwordEdit.selectAll()
        self.usernameEdit.setText('anon')
        self.usernameEdit.selectAll()

    def username(self):
        return self.usernameEdit.text()

    def password(self):
        return self.passwordEdit.text()
