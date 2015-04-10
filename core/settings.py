# -*- coding: utf-8 -*-
"""
/***************************************************************************
                                      Ark
                                 A QGIS plugin
             QGIS Plugin for ARK, the Archaeological Recording Kit
                              -------------------
        begin                : 2015-03-02
        git sha              : $Format:%H$
        copyright            : (C) 2015 by L - P: Heritage LLP
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

from PyQt4 import uic
from PyQt4.QtCore import Qt, QSettings, QDir, QObject, QVariant, pyqtSignal
from PyQt4.QtGui import QDialog, QFileDialog, QIcon, QAction

from qgis.core import QgsProject, QgsSnapper, QgsMessageLog, QgsField, QgsFields
from qgis.gui import QgsMessageBar

from settings_dialog_base import *

class Settings(QObject):

    # Signal when the project changes so modules can reload
    projectChanged = pyqtSignal()

    iface = None # QgsInteface()
    project = None # QgsProject()
    pluginName = 'Ark'
    pluginPath = ''
    pluginIconPath = ':/plugins/Ark/icon.png'

    menuName = ''
    toolbar = None  # QToolBar()
    settingsAction = None  # QAction()

    projectGroupName = 'Ark'
    projectGroupIndex = -1
    planGroupName = 'Context Plans'
    planGroupIndex = -1

    bufferSuffix = '_mem'

    # Grid
    gridGroupNameDefault = 'Grid'
    gridGroupIndex = -1
    gridPointsBaseNameDefault = 'grid_pt'
    gridLinesBaseNameDefault = 'grid_pl'
    gridPolygonsBaseNameDefault = 'grid_pg'
    gridPointsFieldX = 'x'
    gridPointsFieldY = 'y'

    # Contexts
    contextsGroupNameDefault = 'Context Data'
    contextsGroupIndex = -1
    contextsBufferGroupNameDefault = 'Edit Context Data'
    contextsBufferGroupIndex = -1
    contextsPointsBaseNameDefault = 'context_pt'
    contextsLinesBaseNameDefault = 'context_pl'
    contextsPolygonsBaseNameDefault = 'context_pg'
    contextsScopeBaseNameDefault = 'context_mpg'


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

    fieldDefinitions = { 'site'      : QgsField('site',       QVariant.String, '',  10, 0, 'Site Code'),
                         'id'        : QgsField('id',         QVariant.String, '',  10, 0, 'ID'),
                         'context'   : QgsField('context',    QVariant.Int,    '',   5, 0, 'Context'),
                         'category'  : QgsField('category',   QVariant.String, '',  10, 0, 'Category'),
                         'elevation' : QgsField('elevation',  QVariant.Double, '',   3, 3, 'Elevation'),
                         'source'    : QgsField('source',     QVariant.String, '',  50, 0, 'Source'),
                         'file'      : QgsField('file',       QVariant.String, '',  30, 0, 'File'),
                         'local_x'   : QgsField('local_x',    QVariant.Double, '',   4, 3, 'Local Grid X'),
                         'local_y'   : QgsField('local_y',    QVariant.Double, '',   4, 3, 'Local Grid Y'),
                         'crs_x'     : QgsField('crs_x',      QVariant.Double, '',   6, 3, 'CRS X'),
                         'crs_y'     : QgsField('crs_y',      QVariant.Double, '',   6, 3, 'CRS y'),
                         'comment'   : QgsField('comment',    QVariant.String, '', 100, 0, 'Comment'),
                         'created_on': QgsField('created_on', QVariant.String, '',  20, 0, 'Created On'),  # '2012-01-01T23:59:59Z'
                         'created_by': QgsField('created_by', QVariant.String, '',  20, 0, 'Created By') }

    contextPointFields = ['context', 'category', 'elevation', 'source', 'file', 'comment', 'created_on', 'created_by']
    contextLinesFields = ['context', 'category', 'source', 'file', 'comment', 'created_on', 'created_by']
    contextPolygonsFields = contextLinesFields
    contextSchematicFields = contextLinesFields
    baselinePointFields = ['id', 'category', 'elevation', 'source', 'file', 'comment', 'created_on', 'created_by']
    gridPointFields = ['id', 'category', 'local_x', 'local_y', 'elevation', 'source', 'file', 'comment', 'created_on', 'created_by']

    def __init__(self, iface, pluginPath):
        super(Settings, self).__init__()
        self.iface = iface

        self.pluginName = self.tr(u'Ark')
        self.pluginPath = pluginPath

        # Declare instance attributes
        self.menuName = self.tr(u'&Ark')
        self.toolbar = self.iface.addToolBar(self.pluginName)
        self.toolbar.setObjectName(self.pluginName)

    # Load the module when plugin is loaded
    def load(self):
        self.settingsAction = self.createMenuAction(self.tr(u'Ark Settings'), self.pluginIconPath, False)
        self.settingsAction.triggered.connect(self.showSettingsDialog)

    # Unload the module when plugin is unloaded
    def unload(self):
        self.iface.removePluginMenu(self.menuName, self.settingsAction)
        self.iface.removeToolBarIcon(self.settingsAction)

    # Initialise settings for the project the first time they are needed
    def initialise(self):
        if not self.isConfigured():
            self.configure()
        if self.isConfigured():
            self.settings.iface.projectRead.connect(self.projectLoad)
            self.settings.iface.newProjectCreated.connect(self.projectLoad)
        else:
            self.showCriticalMessage('ARK Project not configured, unable to continue!')

    def projectLoad(self):
        self.projectChanged.emit()

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
        return QgsProject.instance().readBoolEntry(self.pluginName, 'configured', False)[0]

    def _setIsConfigured(self, configured):
        QgsProject.instance().writeEntry(self.pluginName, 'configured', configured)

    def configure(self):
        ret = self.showSettingsDialog()
        # TODO more validation, check if files exist, etc
        if (self.siteDir().exists() and self.planDir().exists()):
            self._setIsConfigured(True)
        else:
            self._setIsConfigured(False)

    # Convenience logging functions

    def logMessage(self, text, level=QgsMessageLog.INFO):
        QgsMessageLog.logMessage(text, self.pluginName, level)

    def showCriticalMessage(self, text, duration=0):
        self.iface.messageBar().pushMessage(text, QgsMessageBar.CRITICAL, duration)

    def showMessage(self, text, level=QgsMessageBar.INFO, duration=0):
        self.iface.messageBar().pushMessage(text, level, duration)

    def showStatusMessage(self, text):
        self.iface.mainWindow().statusBar().showMessage(text)


    # Settings utilities

    def _setProjectEntry(self, key, value, default):
        if (value == None or value == '' or value == default):
            QgsProject.instance().removeEntry(self.pluginName, key)
        else:
            QgsProject.instance().writeEntry(self.pluginName, key, value)

    def _layerName(self, baseName):
        if (self.prependSiteCode() and self.siteCode()):
            return self.siteCode() + '_' + baseName
        return baseName


    # Site settings

    def siteDir(self):
        return QDir(self.sitePath())

    def sitePath(self):
        return QgsProject.instance().readEntry(self.pluginName, 'sitePath', '')[0]

    def setSitePath(self, absolutePath):
        QgsProject.instance().writeEntry(self.pluginName, 'sitePath', absolutePath)

    def siteCode(self):
        return QgsProject.instance().readEntry(self.pluginName, 'siteCode', '')[0]

    def setSiteCode(self, siteCode):
        QgsProject.instance().writeEntry(self.pluginName, 'siteCode', siteCode)

    def prependSiteCode(self):
        return QgsProject.instance().readBoolEntry(self.pluginName, 'prependSiteCode', True)[0]

    def setPrependSiteCode(self, prepend):
        QgsProject.instance().writeEntry(self.pluginName, 'prependSiteCode', prepend)

    def useCustomStyles(self):
        return QgsProject.instance().readBoolEntry(self.pluginName, 'useCustomStyles', False)[0]

    def setUseCustomStyles(self, useCustomStyles):
        QgsProject.instance().writeEntry(self.pluginName, 'useCustomStyles', useCustomStyles)

    def styleDir(self):
        return QDir(self.stylePath())

    def stylePath(self):
        path =  QgsProject.instance().readEntry(self.pluginName, 'stylePath', '')[0]
        if (not path):
            return self.pluginPath + '/styles'
        return path

    def setStylePath(self, absolutePath):
        QgsProject.instance().writeEntry(self.pluginName, 'stylePath', absolutePath)


    # Grid Settings

    def gridDir(self):
        return QDir(self.gridPath())

    def gridPath(self):
        path =  QgsProject.instance().readEntry(self.pluginName, 'gridPath', '')[0]
        if (not path):
            return self.sitePath()
        return path

    def setGridPath(self, absolutePath):
        QgsProject.instance().writeEntry(self.pluginName, 'gridPath', absolutePath)

    def gridGroupName(self):
        return QgsProject.instance().readEntry(self.pluginName, 'gridGroupName', self.gridGroupNameDefault)[0]

    def setGridGroupName(self, gridGroupName):
        self._setProjectEntry('gridGroupName', gridGroupName, self.gridGroupNameDefault)

    def gridPointsBaseName(self):
        return QgsProject.instance().readEntry(self.pluginName, 'gridPointsBaseName', self.gridPointsBaseNameDefault)[0]

    def setGridPointsBaseName(self, gridPointsBaseName):
        self._setProjectEntry('gridPointsBaseName', gridPointsBaseName, self.gridPolygonsBaseNameDefault)

    def gridPointsLayerName(self):
        return self._layerName(self.gridPointsBaseName())

    def gridLinesBaseName(self):
        return QgsProject.instance().readEntry(self.pluginName, 'gridLinesBaseName', self.gridLinesBaseNameDefault)[0]

    def setGridLinesBaseName(self, gridLinesBaseName):
        self._setProjectEntry('gridLinesBaseName', gridLinesBaseName, self.gridPolygonsBaseNameDefault)

    def gridLinesLayerName(self):
        return self._layerName(self.gridLinesBaseName())

    def gridPolygonsBaseName(self):
        return QgsProject.instance().readEntry(self.pluginName, 'gridPolygonsBaseName', self.gridPolygonsBaseNameDefault)[0]

    def setGridPolygonsBaseName(self, gridPolygonsBaseName):
        self._setProjectEntry('gridPolygonsBaseName', gridPolygonsBaseName, self.gridPolygonsBaseNameDefault)

    def gridPolygonsLayerName(self):
        return self._layerName(self.gridPolygonsBaseName())


    # Contexts settings

    def contextsDir(self):
        return QDir(self.contextsPath())

    def contextsPath(self):
        path =  QgsProject.instance().readEntry(self.pluginName, 'contextsPath', '')[0]
        if (not path):
            return self.sitePath()
        return path

    def setContextsPath(self, absolutePath):
        QgsProject.instance().writeEntry(self.pluginName, 'contextsPath', absolutePath)

    def contextsGroupName(self):
        return QgsProject.instance().readEntry(self.pluginName, 'contextsGroupName', self.contextsGroupNameDefault)[0]

    def setContextsGroupName(self, contextsGroupName):
        self._setProjectEntry('contextsGroupName', contextsGroupName, self.contextsGroupNameDefault)

    def contextsBufferGroupName(self):
        return QgsProject.instance().readEntry(self.pluginName, 'contextsBufferGroupName', self.contextsBufferGroupNameDefault)[0]

    def setContextsBufferGroupName(self, contextsBufferGroupName):
        self._setProjectEntry('contextsBufferGroupName', contextsBufferGroupName, self.contextsBufferGroupNameDefault)

    def contextsPointsBaseName(self):
        return QgsProject.instance().readEntry(self.pluginName, 'contextsPointsBaseName', self.contextsPointsBaseNameDefault)[0]

    def setContextsPointsBaseName(self, contextsPointsBaseName):
        self._setProjectEntry('contextsPointsBaseName', contextsPointsBaseName, self.contextsPolygonsBaseNameDefault)

    def contextsPointsLayerName(self):
        return self._layerName(self.contextsPointsBaseName())

    def contextsLinesBaseName(self):
        return QgsProject.instance().readEntry(self.pluginName, 'contextsLinesBaseName', self.contextsLinesBaseNameDefault)[0]

    def setContextsLinesBaseName(self, contextsLinesBaseName):
        self._setProjectEntry('contextsLinesBaseName', contextsLinesBaseName, self.contextsPolygonsBaseNameDefault)

    def contextsLinesLayerName(self):
        return self._layerName(self.contextsLinesBaseName())

    def contextsPolygonsBaseName(self):
        return QgsProject.instance().readEntry(self.pluginName, 'contextsPolygonsBaseName', self.contextsPolygonsBaseNameDefault)[0]

    def setContextsPolygonsBaseName(self, contextsPolygonsBaseName):
        self._setProjectEntry('contextsPolygonsBaseName', contextsPolygonsBaseName, self.contextsPolygonsBaseNameDefault)

    def contextsPolygonsLayerName(self):
        return self._layerName(self.contextsPolygonsBaseName())

    def contextsScopeBaseName(self):
        return QgsProject.instance().readEntry(self.pluginName, 'contextsScopeBaseName', self.contextsScopeBaseNameDefault)[0]

    def setContextsScopeBaseName(self, contextsScopeBaseName):
        self._setProjectEntry('contextsScopeBaseName', contextsScopeBaseName, self.contextsScopeBaseNameDefault)

    def contextsScopeLayerName(self):
        return self._layerName(self.contextsScopeBaseName())


    # Plan settings

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
        return QgsProject.instance().readEntry(self.pluginName, 'planPath', '')[0]

    def setPlanPath(self, absolutePath):
        QgsProject.instance().writeEntry(self.pluginName, 'planPath', absolutePath)

    def separatePlanFolders(self):
        return QgsProject.instance().readBoolEntry(self.pluginName, 'separatePlanFolders', True)[0]

    def setSeparatePlanFolders(self, separatePlans):
        QgsProject.instance().writeEntry(self.pluginName, 'separatePlanFolders', separatePlans)

    def planTransparency(self):
        return QgsProject.instance().readNumEntry(self.pluginName, 'planTransparency', 50)[0]

    def setPlanTransparency(self, transparency):
        QgsProject.instance().writeEntry(self.pluginName, 'planTransparency', transparency)


    def projectCrs(self):
        return u'EPSG:27700'
        # TODO Find why this doesn't work!
        # return unicode(QgsProject.instance().readEntry('SpatialRefSys', '/ProjectCRSProj4String', u'')[0])

    def showSettingsDialog(self):
        settingsDialog = SettingsDialog(self, self.iface.mainWindow())
        return settingsDialog.exec_()

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

        # Site tab settings
        self.siteFolderEdit.setText(settings.sitePath())
        self.siteFolderButton.clicked.connect(self._selectSiteFolder)
        self.siteCodeEdit.setText(settings.siteCode())
        self.prependSiteCodeCheck.setChecked(settings.prependSiteCode())
        if settings.useCustomStyles():
            self.defaultStylesCheck.setChecked(False)
            self.styleFolderEdit.setText(settings.stylePath())
            self.styleFolderEdit.setEnabled(True)
            self.styleFolderButton.setEnabled(True)

        # Grid tab settings
        self.gridFolderEdit.setText(settings.gridPath())
        self.gridFolderButton.clicked.connect(self._selectGridFolder)
        self.gridGroupNameEdit.setText(settings.gridGroupName())
        self.gridPointsNameEdit.setText(settings.gridPointsBaseName())
        self.gridLinesNameEdit.setText(settings.gridLinesBaseName())
        self.gridPolygonsNameEdit.setText(settings.gridPolygonsBaseName())

        # Context tab settings
        self.contextsFolderEdit.setText(settings.contextsPath())
        self.contextsFolderButton.clicked.connect(self._selectContextsFolder)
        self.contextsGroupNameEdit.setText(settings.contextsGroupName())
        self.contextsBufferGroupNameEdit.setText(settings.contextsBufferGroupName())
        self.contextsPointsNameEdit.setText(settings.contextsPointsBaseName())
        self.contextsLinesNameEdit.setText(settings.contextsLinesBaseName())
        self.contextsPolygonsNameEdit.setText(settings.contextsPolygonsBaseName())
        self.contextsScopeNameEdit.setText(settings.contextsScopeBaseName())

        # Plan tab settings
        self.planFolderEdit.setText(settings.planPath())
        self.separatePlansCheck.setChecked(settings.separatePlanFolders())
        self.planTransparencySpin.setValue(settings.planTransparency())

        self.defaultStylesCheck.toggled.connect(self._toggleDefaultStyle)
        self.styleFolderButton.clicked.connect(self._selectStyleFolder)
        self.planFolderButton.clicked.connect(self._selectPlanFolder)

    def accept(self):
        # Site tab settings
        self._settings.setSitePath(self.siteFolderEdit.text())
        self._settings.setSiteCode(self.siteCodeEdit.text())
        self._settings.setPrependSiteCode(self.prependSiteCodeCheck.isChecked())
        self._settings.setUseCustomStyles(self.styleFolderEdit.text() != '')
        self._settings.setStylePath(self.styleFolderEdit.text())

        # Grid tab settings
        self._settings.setGridPath(self.gridFolderEdit.text())
        self._settings.setGridGroupName(self.gridGroupNameEdit.text())
        self._settings.setGridPointsBaseName(self.gridPointsNameEdit.text())
        self._settings.setGridLinesBaseName(self.gridLinesNameEdit.text())
        self._settings.setGridPolygonsBaseName(self.gridPolygonsNameEdit.text())

        # Contexts tab settings
        self._settings.setContextsPath(self.contextsFolderEdit.text())
        self._settings.setContextsGroupName(self.contextsGroupNameEdit.text())
        self._settings.setContextsBufferGroupName(self.contextsBufferGroupNameEdit.text())
        self._settings.setContextsPointsBaseName(self.contextsPointsNameEdit.text())
        self._settings.setContextsLinesBaseName(self.contextsLinesNameEdit.text())
        self._settings.setContextsPolygonsBaseName(self.contextsPolygonsNameEdit.text())
        self._settings.setContextsScopeBaseName(self.contextsScopeNameEdit.text())

        # Plan tab settings
        self._settings.setPlanPath(self.planFolderEdit.text())
        self._settings.setSeparatePlanFolders(self.separatePlansCheck.isChecked())
        self._settings.setPlanTransparency(self.planTransparencySpin.value())

        return super(SettingsDialog, self).accept()

    def _selectSiteFolder(self):
        folderName = unicode(QFileDialog.getExistingDirectory(self, self.tr('Site Folder'), self.siteFolderEdit.text()))
        if folderName:
            self.siteFolderEdit.setText(folderName)

    def _selectGridFolder(self):
        folderName = unicode(QFileDialog.getExistingDirectory(self, self.tr('Grid Folder'), self.gridFolderEdit.text()))
        if folderName:
            self.gridFolderEdit.setText(folderName)

    def _toggleDefaultStyle(self, useDefault):
        if useDefault:
            self.styleFolderEdit.setText('')
        self.styleFolderEdit.setEnabled(not useDefault)
        self.styleFolderButton.setEnabled(not useDefault)

    def _selectStyleFolder(self):
        folderName = unicode(QFileDialog.getExistingDirectory(self, self.tr('Style Folder'), self.styleFolderEdit.text()))
        if folderName:
            self.styleFolderEdit.setText(folderName)

    def _selectContextsFolder(self):
        folderName = unicode(QFileDialog.getExistingDirectory(self, self.tr('Contexts Folder'), self.contextsFolderEdit.text()))
        if folderName:
            self.contextsFolderEdit.setText(folderName)

    def _selectPlanFolder(self):
        folderName = unicode(QFileDialog.getExistingDirectory(self, self.tr('Plan Folder'), self.planFolderEdit.text()))
        if folderName:
            self.planFolderEdit.setText(folderName)

