# -*- coding: utf-8 -*-
"""
/***************************************************************************
 ArkPlan
                                 A QGIS plugin
 Plugin to assist in digitising of Archaeological plans.
                              -------------------
        begin                : 2014-12-07
        git sha              : $Format:%H$
        copyright            : (C) 2014 by John Layt
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
from PyQt4.QtCore import Qt, QSettings, QTranslator, qVersion, QCoreApplication, QVariant, QObject, SIGNAL, QFileInfo, QPoint, QDir
from PyQt4.QtGui import QAction, QIcon, QDockWidget, QFileDialog, QMessageBox

from qgis.core import *

# Initialize Qt resources from file resources.py
import resources_rc

# Import the code for the dialog
from ark_plan_dock import ArkPlanDock
from ark_georef_dialog import ArkGeorefDialog
from settings import *
from layers import *
from ark_map_tools import *
from snap_map_tools import *
from ark_plan_util import *

import os.path
import string

class ArkPlan:
    """QGIS Plugin Implementation."""

    # Project settings
    settings = None # Settings()

    # Internal variables

    initialised = False
    dockLocation = Qt.RightDockWidgetArea
    siteCode = ''
    context = 0
    source = '0'
    comment = ''

    layers = None  # LayerManager

    levelsMapTool = None
    currentMapTool = None

    def __init__(self, iface):

        self.settings = Settings('ArkPlan', iface)
        self.layers = LayerManager(self.settings)

        # initialize plugin directory
        self.plugin_dir = os.path.dirname(__file__)

        # initialize locale
        locale = QSettings().value('locale/userLocale')[0:2]
        locale_path = os.path.join(
            self.plugin_dir,
            'i18n',
            'ArkPlan_{}.qm'.format(locale))
        if os.path.exists(locale_path):
            self.translator = QTranslator()
            self.translator.load(locale_path)
            if qVersion() > '4.3.3':
                QCoreApplication.installTranslator(self.translator)

        # Declare instance attributes
        self.actions = []
        self.menu = self.tr(u'&ArkPlan')
        # TODO: We are going to let the user set this up in a future iteration
        self.toolbar = self.settings.iface.addToolBar(self.settings.pluginName)
        self.toolbar.setObjectName(self.settings.pluginName)

    # noinspection PyMethodMayBeStatic
    def tr(self, message):
        """Get the translation for a string using Qt translation API.

        We implement this ourselves since we do not inherit QObject.

        :param message: String for translation.
        :type message: str, QString

        :returns: Translated version of message.
        :rtype: QString
        """
        # noinspection PyTypeChecker,PyArgumentList,PyCallByClass
        return QCoreApplication.translate('ArkPlan', message)


    def add_action(
        self,
        icon_path,
        text,
        callback,
        enabled_flag=True,
        checkable=False,
        add_to_menu=True,
        add_to_toolbar=True,
        status_tip=None,
        whats_this=None,
        parent=None):
        """Add a toolbar icon to the toolbar.

        :param icon_path: Path to the icon for this action. Can be a resource
            path (e.g. ':/plugins/foo/bar.png') or a normal file system path.
        :type icon_path: str

        :param text: Text that should be shown in menu items for this action.
        :type text: str

        :param callback: Function to be called when the action is triggered.
        :type callback: function

        :param enabled_flag: A flag indicating if the action should be enabled
            by default. Defaults to True.
        :type enabled_flag: bool

        :param add_to_menu: Flag indicating whether the action should also
            be added to the menu. Defaults to True.
        :type add_to_menu: bool

        :param add_to_toolbar: Flag indicating whether the action should also
            be added to the toolbar. Defaults to True.
        :type add_to_toolbar: bool

        :param status_tip: Optional text to show in a popup when mouse pointer
            hovers over the action.
        :type status_tip: str

        :param parent: Parent widget for the new action. Defaults None.
        :type parent: QWidget

        :param whats_this: Optional text to show in the status bar when the
            mouse pointer hovers over the action.

        :returns: The action that was created. Note that the action is also
            added to self.actions list.
        :rtype: QAction
        """

        icon = QIcon(icon_path)
        action = QAction(icon, text, parent)
        action.triggered.connect(callback)
        action.setEnabled(enabled_flag)
        action.setCheckable(checkable)

        if status_tip is not None:
            action.setStatusTip(status_tip)

        if whats_this is not None:
            action.setWhatsThis(whats_this)

        if add_to_toolbar:
            self.toolbar.addAction(action)

        if add_to_menu:
            self.settings.iface.addPluginToMenu(
                self.menu,
                action)

        self.actions.append(action)

        return action

    def initGui(self):
        """Create the menu entries and toolbar icons inside the QGIS GUI."""

        icon_path = ':/plugins/ArkPlan/icon.png'
        self.projectSettingsAction = self.add_action(icon_path, text=self.tr(u'ArkPlan Settings'), callback=self.settings.showSettingsDialog, checkable=False, parent=self.settings.iface.mainWindow())

        self.dock = ArkPlanDock()
        self.dock.load(self.settings.iface, Qt.RightDockWidgetArea, self.menu, self.toolbar, icon_path, self.tr(u'Draw Archaeological Plans'))
        self.dock.toggled.connect(self.run)

        self.dock.loadRawFileSelected.connect(self.loadRawPlan)
        self.dock.loadGeoFileSelected.connect(self.loadGeoPlan)
        self.dock.siteChanged.connect(self.setSite)
        self.dock.contextChanged.connect(self.setContext)
        self.dock.sourceChanged.connect(self.setSource)
        self.dock.commentChanged.connect(self.setComment)

        self.dock.selectedLevelsMode.connect(self.enableLevelsMode)
        self.dock.selectedLineMode.connect(self.enableLineMode)
        self.dock.selectedLineSegmentMode.connect(self.enableLineSegmentMode)
        self.dock.selectedPolygonMode.connect(self.enablePolygonMode)
        self.dock.selectedSchematicMode.connect(self.enableSchematicMode)

        self.dock.clearSelected.connect(self.clearBuffers)
        self.dock.mergeSelected.connect(self.mergeBuffers)

        self.dock.showPointsChanged.connect(self.layers.showPoints)
        self.dock.showLinesChanged.connect(self.layers.showLines)
        self.dock.showPolygonsChanged.connect(self.layers.showPolygons)
        self.dock.showSchematicsChanged.connect(self.layers.showSchematics)

        self.dock.contextFilterChanged.connect(self.layers.applyContextFilter)

    def unload(self):

        # Remove the layers from the legend
        self.layers.unload()

        """Removes the plugin menu item and icon from QGIS GUI."""
        for action in self.actions:
            self.settings.iface.removePluginMenu(self.tr(u'&ArkPlan'), action)
            self.settings.iface.removeToolBarIcon(action)

        # Unload the dock
        self.dock.unload()

    def configureProject(self):
        if (self.settings.showSettingsDialog() and self.settings.dataDir().exists() and self.settings.planDir().exists()):
            # Do validation, check if files exist, etc
            self.settings.setIsConfigured(True)
        else:
            self.settings.setIsConfigured(False)

    def run(self, checked):
        if checked:
            if not self.initialised:
                self.initialise()

    def initialise(self):

        if (not self.settings.isConfigured()):
            self.configureProject()

        self.layers.initialise()
        self.dock.setSchematicsBuffer(self.layers.schematicBuffer)
        self.dock.setPolygonsBuffer(self.layers.polygonsBuffer)
        self.dock.setLinesBuffer(self.layers.linesBuffer)
        self.dock.setLinesBuffer(self.layers.pointsBuffer)
        self.dock.setSchematicsLayer(self.layers.schematicLayer)
        self.dock.setPolygonsLayer(self.layers.polygonsLayer)
        self.dock.setLinesLayer(self.layers.linesLayer)

        # If the map tool changes make sure we stay updated
        self.settings.iface.mapCanvas().mapToolSet.connect(self.mapToolChanged)

        self.initialised = True

    # Plan Tools

    def setMetadata(self, siteCode, type, number, easting, northing, suffix):
        self.dock.setSite(siteCode)
        self.dock.setContext(number)
        self.dock.setSource(str(number))

    def loadRawPlan(self):
        fileName = unicode(QFileDialog.getOpenFileName(None, self.tr('Load Raw Plan'), self.settings.rawPlanPath(),
                                                       self.tr('Image Files (*.png *.tif *.tiff)')))
        if fileName:
            self.georeferencePlan(QFileInfo(fileName))

    def loadGeoPlan(self):
        fileName = unicode(QFileDialog.getOpenFileName(None, self.tr('Load Georeferenced Plan'), self.settings.processedPlanPath(),
                                                       self.tr('GeoTiff Files (*.tif *.tiff)')))
        if fileName:
            geoFile = QFileInfo(fileName)
            md = planMetadata(geoFile.completeBaseName())
            self.setMetadata(md[0], md[1], md[2], md[3], md[4], md[5])
            self.layers.loadGeoLayer(geoFile)

    def setSite(self, siteCode):
        self.siteCode = siteCode

    def setContext(self, context):
        self.context = context

    def setSource(self, source):
        self.source = source

    def setComment(self, comment):
        self.comment = comment

    # Georeference Tools

    def georeferencePlan(self, rawFile):
        georefDialog = ArkGeorefDialog(rawFile, self.settings.planDir(), self.settings.separatePlanFolders(), self.settings.projectCrs(), self.settings.gridPointsLayerName(), self.settings.gridPointsFieldX, self.settings.gridPointsFieldY)
        if (georefDialog.exec_()):
            md = georefDialog.metadata()
            self.setMetadata(md[0], md[1], md[2], md[3], md[4], md[5])
            self.loadGeoLayer(georefDialog.geoRefFile())

    # Levels Tool Methods

    def enableLevelsMode(self, type):
        #TODO disable all snapping
        self.settings.iface.mapCanvas().setCurrentLayer(self.layers.pointsBuffer)
        self.settings.iface.legendInterface().setCurrentLayer(self.layers.pointsBuffer)
        if self.levelsMapTool is not None:
            del self.levelsMapTool
        self.levelsMapTool = LevelsMapTool(self.settings.iface.mapCanvas())
        self.levelsMapTool.levelAdded.connect(self.addLevel)
        self.levelsMapTool.setType(type)
        self.settings.iface.mapCanvas().setMapTool(self.levelsMapTool)

    def addLevel(self, point, type, elevation):
        feature = QgsFeature()
        feature.setGeometry(QgsGeometry.fromPoint(point))
        feature.setAttributes([self.context, self.source, type, self.comment, elevation])
        self.layers.pointsBuffer.beginEditCommand('Buffer level ' + str(self.context) + ' ' + type + ' ' + str(elevation))
        self.layers.pointsBuffer.addFeature(feature, True)
        self.layers.pointsBuffer.endEditCommand()
        self.settings.iface.mapCanvas().refresh()

    # Layer Methods

    def mergeBuffers(self):
        self.layers.copyBuffers('Merge context data  ' + str(self.context))
        self.clearBuffers()

    def clearBuffers(self):
        self.layers.clearBuffers('Clear buffer data ' + str(self.context))

    def enableLineSegmentMode(self, typeAttribute):
        #TODO configure snapping
        self.enableMapTool(typeAttribute, self.layers.linesBuffer, QgsMapToolAddFeature.Segment, self.tr('Add line segment feature'))

    def enableLineMode(self, typeAttribute):
        #TODO configure snapping
        self.enableMapTool(typeAttribute, self.layers.linesBuffer, QgsMapToolAddFeature.Line, self.tr('Add line feature'))

    def enablePolygonMode(self, typeAttribute):
        #TODO configure snapping
        self.enableMapTool(typeAttribute, self.layers.polygonsBuffer, QgsMapToolAddFeature.Polygon, self.tr('Add polygon feature'))

    def enableSchematicMode(self, typeAttribute):
        #TODO configure snapping
        self.enableMapTool(typeAttribute, self.layers.schematicBuffer, QgsMapToolAddFeature.Polygon, self.tr('Add schematic feature'))

    def enableMapTool(self, typeAttribute, layer, featureType, toolName):
        #TODO configure snapping
        self.settings.iface.mapCanvas().setCurrentLayer(layer)
        self.settings.iface.legendInterface().setCurrentLayer(layer)
        if self.currentMapTool is not None:
            self.currentMapTool.deactivate()
            self.currentMapTool = None
        self.currentMapTool = QgsMapToolAddFeature(self.settings.iface.mapCanvas(), self.settings.iface, featureType, toolName)
        self.currentMapTool.setDefaultAttributes({0 : self.context, 1 : self.source, 2 : typeAttribute, 3 : self.comment})
        self.settings.iface.mapCanvas().setMapTool(self.currentMapTool)

    def mapToolChanged(self, newMapTool):
        if (newMapTool != self.currentMapTool):
            self.dock.clearCheckedToolButton()
            if (self.currentMapTool is not None):
                self.currentMapTool.deactivate()
                self.currentMapTool = None
