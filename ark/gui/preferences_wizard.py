# -*- coding: utf-8 -*-
"""
/***************************************************************************
                                ARKspatial
                    A QGIS plugin for Archaeological Recording.
        Part of the Archaeological Recording Kit by L - P : Archaeology
                        http://ark.lparchaeology.com
                              -------------------
        copyright            : 2018 by L - P : Heritage LLP
        email                : ark@lparchaeology.com
        copyright            : 2018 by John Layt
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

from .ui.preferences_wizard_base import Ui_PreferencesWizard


class PreferencesWizard(QWizard, Ui_PreferencesWizard):

    def __init__(self, parent=None):
        super(PreferencesWizard, self).__init__(parent)
        self.setupUi(self)

    def preferences(self):
        return self.preferencesWidget

    def server(self):
        return self.serverWidget

    def globals(self):
        return self.globalPage
