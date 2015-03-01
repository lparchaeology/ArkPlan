# -*- coding: utf-8 -*-
"""
/***************************************************************************
 ArkPlanDialog
                                 A QGIS plugin
 Plugin to assist in digitising of Archaeological plans.
                             -------------------
        begin                : 2015-01-10
        git sha              : $Format:%H$
        copyright            : (C) 2015 by John Layt
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

import os.path

from PyQt4 import uic
from PyQt4.QtCore import Qt, QSettings, QDir, QObject
from PyQt4.QtGui import QDialog, QFileDialog, QIcon, QAction

from qgis.core import QgsProject, QgsSnapper

from settings_dialog_base import *

import resources_rc

class Settings(QObject):

    iface = None # QgsInteface()
    project = None # QgsProject()
    pluginName = 'Ark'
    pluginPath = ''
    pluginIconPath = ':/plugins/ArkPlan/icon.png'

    menuName = ''
    toolbar = None  # QToolBar()
    settingsAction = None  # QAction()

    projectGroupName = 'Ark'
    projectGroupIndex = -1
    dataGroupName = 'Context Data'
    dataGroupIndex = -1
    bufferGroupName = 'Edit Buffers'
    bufferGroupIndex = -1
    planGroupName = 'Context Plans'
    planGroupIndex = -1

    pointsBaseName = 'context_pt'
    linesBaseName = 'context_pl'
    polygonsBaseName = 'context_pg'
    schematicBaseName = 'schematic_pg'

    gridPointsBaseName = 'grid_pt'
    gridPointsFieldX = 'x'
    gridPointsFieldY = 'y'

    bufferSuffix = '_mem'

    contextAttributeName = 'context'
    contextAttributeSize = 5
    sourceAttributeName = 'source'
    sourceAttributeSize = 30
    typeAttributeName = 'type'
    typeAttributeSize = 10
    commentAttributeName = 'comment'
    commentAttributeSize = 100
    elevationAttributeName = 'elevation'
    elevationAttributeSize = 5
    elevationAttributePrecision = 2

    def __init__(self, iface):
        super(Settings, self).__init__()
        self.iface = iface
        self.project = QgsProject.instance()

        self.pluginName = self.tr(u'Ark')
        self.pluginPath = os.path.dirname(__file__)

        # Declare instance attributes
        self.menuName = self.tr(u'&Ark')
        self.toolbar = self.iface.addToolBar(self.pluginName)
        self.toolbar.setObjectName(self.pluginName)

    def initGui(self):
        self.settingsAction = self.createMenuAction(self.tr(u'ArkPlan Settings'), self.pluginIconPath, False)
        self.settingsAction.toggled.connect(self.showSettingsDialog)

    def unload(self):
        self.iface.removePluginMenu(self.tr(u'&ArkPlan'), action)
        self.iface.removeToolBarIcon(action)

    def createMenuAction(self, actionText, iconPath, checkable, tip='', whatsThis=''):
        icon = QIcon(iconPath)
        action = QAction(icon, actionText, self.iface.mainWindow())
        action.setCheckable(checkable)
        action.setStatusTip(tip)
        action.setWhatsThis(whatsThis)
        self.toolbar.addAction(action)
        self.iface.addPluginToMenu(self.menuName, action)
        return action

    def isConfigured(self):
        return self.project.readBoolEntry(self.pluginName, 'configured', False)[0]

    def _setIsConfigured(self, configured):
        self.project.writeEntry(self.pluginName, 'configured', configured)

    def configure(self):
        ret = self.showSettingsDialog()
        # TODO more validation, check if files exist, etc
        if (self.dataDir().exists() and self.planDir().exists()):
            self._setIsConfigured(True)
        else:
            self._setIsConfigured(False)

    def dataDir(self):
        return QDir(self.dataPath())

    def dataPath(self):
        return self.project.readEntry(self.pluginName, 'dataPath', '')[0]

    def setDataPath(self, absolutePath):
        self.project.writeEntry(self.pluginName, 'dataPath', absolutePath)

    def siteCode(self):
        return self.project.readEntry(self.pluginName, 'siteCode', '')[0]

    def setSiteCode(self, siteCode):
        self.project.writeEntry(self.pluginName, 'siteCode', siteCode)

    def prependSiteCode(self):
        return self.project.readBoolEntry(self.pluginName, 'prependSiteCode', True)[0]

    def setPrependSiteCode(self, prepend):
        self.project.writeEntry(self.pluginName, 'prependSiteCode', prepend)

    def planDir(self):
        return QDir(self.planPath())

    def rawPlanPath(self):
        if self.separatePlanFolders():
            dir = QDir(self.planPath() + '/raw')
            if dir.exists():
                return dir.absolutePath()
        return self.planPath()

    def processedPlanPath(self):
        if self.separatePlanFolders():
            dir = QDir(self.planPath() + '/processed')
            if (not dir.exists()):
                self.planDir().mkdir('processed')
            return dir.absolutePath()
        return self.planPath()

    def planPath(self):
        return self.project.readEntry(self.pluginName, 'planPath', '')[0]

    def setPlanPath(self, absolutePath):
        self.project.writeEntry(self.pluginName, 'planPath', absolutePath)

    def separatePlanFolders(self):
        return self.project.readBoolEntry(self.pluginName, 'separatePlanFolders', True)[0]

    def setSeparatePlanFolders(self, separatePlans):
        self.project.writeEntry(self.pluginName, 'separatePlanFolders', separatePlans)

    def planTransparency(self):
        return self.project.readNumEntry(self.pluginName, 'planTransparency', 50)[0]

    def setPlanTransparency(self, transparency):
        self.project.writeEntry(self.pluginName, 'planTransparency', transparency)

    def projectCrs(self):
        return u'EPSG:27700'
        # TODO Find why this doesn't work!
        # return unicode(QgsProject.instance().readEntry('SpatialRefSys', '/ProjectCRSProj4String', u'')[0])

    def showSettingsDialog(self):
        settingsDialog = SettingsDialog(self, self.iface.mainWindow())
        return settingsDialog.exec_()

    def pointsLayerName(self):
        return self._layerName(self.pointsBaseName)

    def linesLayerName(self):
        return self._layerName(self.linesBaseName)

    def polygonsLayerName(self):
        return self._layerName(self.polygonsBaseName)

    def schematicLayerName(self):
        return self._layerName(self.schematicBaseName)

    def gridPointsLayerName(self):
        return self._layerName(self.gridPointsBaseName)

    def pointsBufferName(self):
        return self._bufferName(self.pointsBaseName)

    def linesBufferName(self):
        return self._bufferName(self.linesBaseName)

    def polygonsBufferName(self):
        return self._bufferName(self.polygonsBaseName)

    def schematicBufferName(self):
        return self._bufferName(self.schematicBaseName)

    def _layerName(self, baseName):
        if (self.prependSiteCode() and self.siteCode()):
            return self.siteCode() + '_' + baseName
        return baseName

    def _bufferName(self, baseName):
        return self._layerName(baseName) + self.bufferSuffix

    def defaultSnappingMode(self):
        defaultSnappingModeString = QSettings().value('/qgis/digitizing/default_snap_mode', 'to vertex')
        defaultSnappingMode = QgsSnapper.SnapToVertex
        if (defaultSnappingModeString == "to vertex and segment" ):
            return QgsSnapper.SnapToVertexAndSegment
        elif (defaultSnappingModeString == 'to segment'):
            return QgsSnapper.SnapToSegment
        return QgsSnapper.SnapToVertex

    def defaultSnappingUnit(self):
        unit = QSettings().value('/qgis/digitizing/default_snapping_tolerance_unit', 0, int)
        # Huh???
        if unit is None:
            return 0
        return unit

    def defaultSnappingTolerance(self):
        tolerance = QSettings().value('/qgis/digitizing/default_snapping_tolerance', 10.0, float)
        # Huh???
        if tolerance is None:
            return 0.0
        return tolerance


class SettingsDialog(QDialog, Ui_SettingsDialogBase):

    _settings = None # PluginSettings()

    def __init__(self, settings, parent=None):
        super(SettingsDialog, self).__init__(parent)
        self._settings = settings

        self.setupUi(self)

        self.dataFolderEdit.setText(settings.dataPath())
        self.siteCodeEdit.setText(settings.siteCode())
        self.prependSiteCodeCheck.setChecked(settings.prependSiteCode())
        self.planFolderEdit.setText(settings.planPath())
        self.separatePlansCheck.setChecked(settings.separatePlanFolders())
        self.planTransparencySpin.setValue(settings.planTransparency())

        self.dataFolderButton.clicked.connect(self._selectDataFolder)
        self.planFolderButton.clicked.connect(self._selectPlanFolder)

    def accept(self):
        self._settings.setDataPath(self.dataFolderEdit.text())
        self._settings.setSiteCode(self.siteCodeEdit.text())
        self._settings.setPrependSiteCode(self.prependSiteCodeCheck.isChecked())
        self._settings.setPlanPath(self.planFolderEdit.text())
        self._settings.setSeparatePlanFolders(self.separatePlansCheck.isChecked())
        self._settings.setPlanTransparency(self.planTransparencySpin.value())
        return super(SettingsDialog, self).accept()

    def _selectDataFolder(self):
        folderName = unicode(QFileDialog.getExistingDirectory(self, self.tr('Data Folder'), self.dataFolderEdit.text()))
        if folderName:
            self.dataFolderEdit.setText(folderName)

    def _selectPlanFolder(self):
        folderName = unicode(QFileDialog.getExistingDirectory(self, self.tr('Plan Folder'), self.planFolderEdit.text()))
        if folderName:
            self.planFolderEdit.setText(folderName)

