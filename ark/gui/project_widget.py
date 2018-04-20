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

from PyQt4.QtGui import QComboBox, QWidget

from ArkSpatial.ark.lib import utils

from ArkSpatial.ark.core import Settings
from ArkSpatial.ark.pyARK import Ark

from .ui.project_widget_base import Ui_ProjectWidget


class ProjectWidget(QWidget, Ui_ProjectWidget):

    def __init__(self, parent=None):
        super(ProjectWidget, self).__init__(parent)
        self.setupUi(self)
        self._ark = None
        if Settings.useProjectServer():
            self.projectNameEdit.setEnabled(False)
            self.siteCodeEdit.setEnabled(False)
            self.locationEastingEdit.setEnabled(False)
            self.locationNorthingEdit.setEnabled(False)
            self.projectCodeCombo.setMaxVisibleItems(10)
            self.projectCodeCombo.setInsertPolicy(QComboBox.NoInsert)
            self.projectCodeCombo.currentIndexChanged.connect(self._selectProject)

    def load(self):
        if Settings.useProjectServer():
            self._ark = Ark(Settings.serverUrl(), Settings.serverUser(), Settings.serverPassword())
            projects = self._ark.getProjectList()
            self.projectCodeCombo.setMaxCount(len(projects))
            for key in utils.natsorted(projects.keys()):
                self.projectCodeCombo.addItem(projects[key], key)
        self.setProjectCode(Settings.projectCode())
        self.setProjectName(Settings.projectName())
        self.setSiteCode(Settings.siteCode())
        self.setLocation(Settings.locationEasting(), Settings.locationNorthing)

    def projectCode(self):
        return self.projectCodeCombo.lineEdit().text()

    def setProjectCode(self, code):
        if code is None:
            code = ''
        return self.projectCodeCombo.lineEdit().setText(code)

    def projectName(self):
        return self.projectNameEdit.text()

    def setProjectName(self, name):
        if name is None:
            name = ''
        self.projectNameEdit.setText(name)

    def siteCode(self):
        return self.siteCodeEdit.text()

    def setSiteCode(self, siteCode):
        if siteCode is None:
            siteCode = ''
        self.siteCodeEdit.setText(siteCode)

    def locationEasting(self):
        return self.locationEastingEdit.text()

    def locationNorthing(self):
        return self.locationNorthingEdit.text()

    def setLocation(self, easting, northing):
        if easting is None or northing is None or easting == '' or northing == '':
            easting = ''
            northing = ''
        self.locationEastingEdit.setText(str(easting))
        self.locationNorthingEdit.setText(str(northing))

    def _selectProject(self, index):
        project = self.projectCodeCombo.itemData(index)
        data = self._ark.getProjectDetails(project)
        self.setProjectName(utils.safeFilename(data['projectName']))
        self.setSiteCode(data['siteCode'])
        self.setLocation(data['locationEasting'], data['locationNorthing'])
