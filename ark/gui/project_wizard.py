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

from qgis.PyQt.QtCore import QDir, QFileInfo
from qgis.PyQt.QtWidgets import QWizard

from qgis.core import QgsPointV2

from .ui.project_wizard_base import Ui_ProjectWizard


class ProjectWizard(QWizard, Ui_ProjectWizard):

    def __init__(self, parent=None):
        super().__init__(parent)
        self.setupUi(self)

    def project(self):
        return self.projectWidget

    def newProject(self):
        return self.field('newProject')

    def projectFolder(self):
        return self.field('projectFolder')

    def projectFilename(self):
        return self.field('projectFilename')

    def projectLocation(self):
        if self.field('locationEasting') and self.field('locationNorthing'):
            return QgsPointV2(float(self.field('locationEasting')), float(self.field('locationNorthing')))
        return QgsPointV2()
