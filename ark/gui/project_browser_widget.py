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

from qgis.PyQt.QtWidgets import QWidget

from ArkSpatial.ark.core import Settings

from .ui.project_browser_widget_base import Ui_ProjectBrowserWidget


class ProjectBrowserWidget(QWidget, Ui_ProjectBrowserWidget):

    def __init__(self, parent=None):
        super(ProjectBrowserWidget, self).__init__(parent)
        self.setupUi(self)

    def loadProject(self, plugin):
        self.projectCodeEdit.setText(Settings.projectCode())
        self.siteCodeEdit.setText(Settings.siteCode())
        self.projectNameEdit.setText(Settings.projectName())

    def closeProject(self):
        self.projectCodeEdit.setText('')
        self.siteCodeEdit.setText('')
        self.projectNameEdit.setText('')
