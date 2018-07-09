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

from qgis.PyQt.QtWidgets import QDialog

from .ui.preferences_dialog_base import Ui_PreferencesDialogBase


class PreferencesDialog(QDialog, Ui_PreferencesDialogBase):

    def __init__(self, parent=None):
        super().__init__(parent)
        self.setupUi(self)
        self.load()

    def accept(self):
        return super().accept()

    def load(self):
        self.preferences().load()
        self.server().load()

    def preferences(self):
        return self.preferencesWidget

    def server(self):
        return self.serverWidget
