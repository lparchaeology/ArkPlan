# -*- coding: utf-8 -*-
"""
/***************************************************************************
                                ARK Spatial
                    A QGIS plugin for Archaeological Recording.
        Part of the Archaeological Recording Kit by L-P : Archaeology
                        http://ark.lparchaeology.com
                              -------------------
        begin                : 2014-12-07
        git sha              : $Format:%H$
        copyright            : 2014, 2015 by L-P : Heritage LLP
        email                : ark@lparchaeology.com
        copyright            : 2014, 2015 by John Layt
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
from PyQt4.QtGui import QDialog, QFileDialog

from settings_dialog_base import *

class SettingsDialog(QDialog, Ui_SettingsDialogBase):

    _project = None # Project()

    def __init__(self, project, parent=None):
        super(SettingsDialog, self).__init__(parent)
        self._project = project

        self.setupUi(self)

        # Project tab settings
        self.projectFolderEdit.setText(project.projectPath())
        self.projectFolderButton.clicked.connect(self._selectProjectFolder)
        self.multiSiteCheck.setChecked(project.multiSiteProject())
        self.siteCodeEdit.setText(project.siteCode())
        self.styleFolderCheck.setChecked(project.useCustomStyles())
        if project.useCustomStyles():
            self.styleFolderEdit.setEnabled(True)
            self.styleFolderButton.setEnabled(True)
        self.styleFolderButton.clicked.connect(self._selectStyleFolder)
        self.useArkCheck.setChecked(project.useArkDB())
        self.arkUrlEdit.setText(project.arkUrl())
        if project.isConfigured():
            self.useArkCheck.setEnabled(False)

        # Grid tab settings
        self.gridFolderCheck.setChecked(project.useCustomPath('grid'))
        if project.useCustomPath('grid'):
            self.gridFolderEdit.setEnabled(True)
            self.gridFolderButton.setEnabled(True)
        self.gridFolderEdit.setText(project.groupPath('grid'))
        self.gridFolderButton.clicked.connect(self._selectGridFolder)
        self.gridGroupNameEdit.setText(project.layersGroupName('grid'))
        self.gridPointsNameEdit.setText(project.pointsBaseName('grid'))
        self.gridLinesNameEdit.setText(project.linesBaseName('grid'))
        self.gridPolygonsNameEdit.setText(project.polygonsBaseName('grid'))

        # Base tab settings
        self.baseFolderCheck.setChecked(project.useCustomPath('base'))
        if project.useCustomPath('base'):
            self.baseFolderEdit.setEnabled(True)
            self.baseFolderButton.setEnabled(True)
        self.baseFolderEdit.setText(project.groupPath('base'))
        self.baseFolderButton.clicked.connect(self._selectBaseFolder)
        self.baseGroupNameEdit.setText(project.layersGroupName('base'))
        self.basePointsNameEdit.setText(project.pointsBaseName('base'))
        self.baseLinesNameEdit.setText(project.linesBaseName('base'))
        self.basePolygonsNameEdit.setText(project.polygonsBaseName('base'))

        # Plan tab settings
        self.planDataFolderCheck.setChecked(project.useCustomPath('plan'))
        if project.useCustomPath('plan'):
            self.planFolderEdit.setEnabled(True)
            self.planFolderButton.setEnabled(True)
        self.planDataFolderEdit.setText(project.groupPath('plan'))
        self.planDataFolderButton.clicked.connect(self._selectPlanFolder)
        self.planDataGroupNameEdit.setText(project.layersGroupName('plan'))
        self.planBufferGroupNameEdit.setText(project.buffersGroupName('plan'))
        self.planPointsNameEdit.setText(project.pointsBaseName('plan'))
        self.planLinesNameEdit.setText(project.linesBaseName('plan'))
        self.planPolygonsNameEdit.setText(project.polygonsBaseName('plan'))

        # Drawings tab settings
        self.drawingGroupNameEdit.setText(project.layersGroupName('cxt'))
        self.drawingTransparencySpin.setValue(project.drawingTransparency())
        self.georefFolderCheck.setChecked(project.useGeorefFolder())
        self.contextDrawingFolderCheck.setChecked(project.useCustomPath('cxt'))
        if project.useCustomPath('cxt'):
            self.contextDrawingFolderEdit.setEnabled(True)
            self.contextDrawingFolderButton.setEnabled(True)
        self.contextDrawingFolderEdit.setText(project.groupPath('cxt'))
        self.contextDrawingFolderButton.clicked.connect(self._selectContextDrawingFolder)
        if project.useCustomPath('pln'):
            self.planDrawingFolderEdit.setEnabled(True)
            self.planDrawingFolderButton.setEnabled(True)
        self.planDrawingFolderEdit.setText(project.groupPath('pln'))
        self.planDrawingFolderButton.clicked.connect(self._selectPlanDrawingFolder)

    def accept(self):
        # Project tab settings
        self._project.setProjectPath(self.projectFolderEdit.text())
        self._project.setMultiSiteProject(self.multiSiteCheck.isChecked())
        self._project.setSiteCode(self.siteCodeEdit.text())
        self._project.setStylePath(self.styleFolderCheck.isChecked(), self.styleFolderEdit.text())
        self._project.setUseArkDB(self.useArkCheck.isChecked())
        self._project.setArkUrl(self.arkUrlEdit.text())

        # Grid tab settings
        self._project.setGroupPath('grid', self.gridFolderCheck.isChecked(), self.gridFolderEdit.text())
        self._project.setLayersGroupName('grid', self.gridGroupNameEdit.text())
        self._project.setPointsBaseName('grid', self.gridPointsNameEdit.text())
        self._project.setLinesBaseName('grid', self.gridLinesNameEdit.text())
        self._project.setPolygonsBaseName('grid', self.gridPolygonsNameEdit.text())

        # Base tab settings
        self._project.setGroupPath('base', self.baseFolderCheck.isChecked(), self.baseFolderEdit.text())
        self._project.setLayersGroupName('base', self.baseGroupNameEdit.text())
        self._project.setPointsBaseName('base', self.basePointsNameEdit.text())
        self._project.setLinesBaseName('base', self.baseLinesNameEdit.text())
        self._project.setPolygonsBaseName('base', self.basePolygonsNameEdit.text())

        # Plan tab settings
        self._project.setGroupPath('plan', self.planDataFolderCheck.isChecked(), self.planDataFolderEdit.text())
        self._project.setLayersGroupName('plan', self.planDataGroupNameEdit.text())
        self._project.setBuffersGroupName('plan', self.planBufferGroupNameEdit.text())
        self._project.setPointsBaseName('plan', self.planPointsNameEdit.text())
        self._project.setLinesBaseName('plan', self.planLinesNameEdit.text())
        self._project.setPolygonsBaseName('plan', self.planPolygonsNameEdit.text())

        # Drawings tab settings
        self._project.setGroupPath('cxt', self.contextDrawingFolderCheck.isChecked(), self.contextDrawingFolderEdit.text())
        self._project.setLayersGroupName('cxt', self.drawingGroupNameEdit.text())
        self._project.setGroupPath('pln', self.planDrawingFolderCheck.isChecked(), self.planDrawingFolderEdit.text())
        self._project.setLayersGroupName('pln', self.drawingGroupNameEdit.text())
        self._project.setUseGeorefFolder(self.georefFolderCheck.isChecked())
        self._project.setDrawingTransparency(self.drawingTransparencySpin.value())

        return super(SettingsDialog, self).accept()

    def _selectProjectFolder(self):
        folderName = unicode(QFileDialog.getExistingDirectory(self, self.tr('Project Folder'), self.projectFolderEdit.text()))
        if folderName:
            self.projectFolderEdit.setText(folderName)

    def _selectGridFolder(self):
        folderName = unicode(QFileDialog.getExistingDirectory(self, self.tr('Grid Folder'), self.gridFolderEdit.text()))
        if folderName:
            self.gridFolderEdit.setText(folderName)

    def _selectBaseFolder(self):
        folderName = unicode(QFileDialog.getExistingDirectory(self, self.tr('Base Folder'), self.baseFolderEdit.text()))
        if folderName:
            self.baseFolderEdit.setText(folderName)

    def _toggleDefaultStyle(self, useDefault):
        if useDefault:
            self.styleFolderEdit.setText('')
        self.styleFolderEdit.setEnabled(not useDefault)
        self.styleFolderButton.setEnabled(not useDefault)

    def _selectStyleFolder(self):
        folderName = unicode(QFileDialog.getExistingDirectory(self, self.tr('Style Folder'), self.styleFolderEdit.text()))
        if folderName:
            self.styleFolderEdit.setText(folderName)

    def _selectPlanFolder(self):
        folderName = unicode(QFileDialog.getExistingDirectory(self, self.tr('Plan Data Folder'), self.planDataFolderEdit.text()))
        if folderName:
            self.planDataFolderEdit.setText(folderName)

    def _selectContextDrawingFolder(self):
        folderName = unicode(QFileDialog.getExistingDirectory(self, self.tr('Context Drawing Folder'), self.contextDrawingFolderEdit.text()))
        if folderName:
            self.contextDrawingFolderEdit.setText(folderName)

    def _selectPlanDrawingFolder(self):
        folderName = unicode(QFileDialog.getExistingDirectory(self, self.tr('Plan Drawing Folder'), self.planDrawingFolderEdit.text()))
        if folderName:
            self.planDrawingFolderEdit.setText(folderName)

