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

    crs = 'EPSG:27700'
    initialised = False
    dockLocation = Qt.RightDockWidgetArea
    siteCode = ''
    context = 0
    source = '0'
    comment = ''
    geoLayer = QgsRasterLayer()

    pointsLayer = None
    linesLayer = None
    polygonsLayer = None
    schematicLayer = None
    gridPointsLayer = None

    pointsBuffer = None
    linesBuffer = None
    polygonsBuffer = None
    schematicBuffer = None

    levelsMapTool = None
    currentMapTool = None

    def __init__(self, iface):

        self.settings = Settings('ArkPlan', iface)

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

        self.dock.showLevelsChanged.connect(self.showLevels)
        self.dock.showLinesChanged.connect(self.showLines)
        self.dock.showPolygonsChanged.connect(self.showPolygons)
        self.dock.showSchematicsChanged.connect(self.showSchematics)

        self.dock.contextFilterChanged.connect(self.applyContextFilter)

    def unload(self):

        # Remove the levels form the legend
        if (self.pointsBuffer is not None and self.pointsBuffer.isValid()):
            QgsMapLayerRegistry.instance().removeMapLayer(self.pointsBuffer.id())
        if self.linesBuffer is not None:
            QgsMapLayerRegistry.instance().removeMapLayer(self.linesBuffer.id())
        if self.polygonsBuffer is not None:
            QgsMapLayerRegistry.instance().removeMapLayer(self.polygonsBuffer.id())
        if self.schematicBuffer is not None:
            QgsMapLayerRegistry.instance().removeMapLayer(self.schematicBuffer.id())
        if (self.settings.bufferGroupIndex >= 0):
            self.settings.iface.legendInterface().removeGroup(self.settings.bufferGroupIndex)

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

    def groupIndexChanged(self, oldIndex, newIndex):
        if (oldIndex == self.settings.dataGroupIndex):
            self.settings.dataGroupIndex = newIndex
        elif (oldIndex == self.settings.bufferGroupIndex):
            self.settings.bufferGroupIndex = newIndex
        elif (oldIndex == self.settings.planGroupIndex):
            self.settings.planGroupIndex = newIndex

    def loadLayerByName(self, dir, name, groupIndex):
        # If the layer is already loaded, use it and return
        layerList = QgsMapLayerRegistry.instance().mapLayersByName(name)
        if (len(layerList) > 0):
            self.settings.iface.legendInterface().moveLayer(layerList[0], groupIndex)
            return layerList[0]
        #TODO Check if exists, if not then create!
        # Otherwise load the layer and add it to the legend
        layer = QgsVectorLayer(dir.absolutePath() + '/' + name + '.shp', name, "ogr")
        if (layer.isValid()):
            self._setDefaultSnapping(layer)
            # TODO Check for other locations of style file
            layer.loadNamedStyle(dir.absolutePath() + '/' + name + '.qml')
            QgsMapLayerRegistry.instance().addMapLayer(layer)
            self.settings.iface.legendInterface().moveLayer(layer, groupIndex)
            self.settings.iface.legendInterface().refreshLayerSymbology(layer)
            return layer
        return None

    def initialise(self):

        if (not self.settings.isConfigured()):
            self.configureProject()

        # If the legend indexes change make sure we stay updated
        self.settings.iface.legendInterface().groupIndexChanged.connect(self.groupIndexChanged)

        # If the map tool changes make sure we stay updated
        self.settings.iface.mapCanvas().mapToolSet.connect(self.mapToolChanged)

        self.createBufferLayers()
        self.loadContextLayers()
        self.initialised = True

    # Load the context layers if not already loaded
    def loadContextLayers(self):
        if (self.settings.dataGroupIndex < 0):
            self.settings.dataGroupIndex = self.getGroupIndex(self.settings.dataGroupName)
        if (self.schematicLayer is None):
            self.schematicLayer = self.loadLayerByName(self.settings.dataDir(), self.settings.schematicLayerName(), self.settings.dataGroupIndex)
            self.dock.setSchematicsLayer(self.schematicLayer)
        if (self.polygonsLayer is None):
            self.polygonsLayer = self.loadLayerByName(self.settings.dataDir(), self.settings.polygonsLayerName(), self.settings.dataGroupIndex)
            self.dock.setPolygonsLayer(self.polygonsLayer)
        if (self.linesLayer is None):
            self.linesLayer = self.loadLayerByName(self.settings.dataDir(), self.settings.linesLayerName(), self.settings.dataGroupIndex)
            self.dock.setLinesLayer(self.linesLayer)
        if (self.pointsLayer is None):
            self.pointsLayer = self.loadLayerByName(self.settings.dataDir(), self.settings.pointsLayerName(), self.settings.dataGroupIndex)
        if (self.gridPointsLayer is None):
            self.gridPointsLayer = self.loadLayerByName(self.settings.dataDir(), self.settings.gridPointsLayerName(), self.settings.dataGroupIndex)

    def _setDefaultSnapping(self, layer):
        # TODO Check if layer id already in settings, only set defaults if it isn't
        QgsProject.instance().setSnapSettingsForLayer(layer.id(), True, self.settings.defaultSnappingMode(), self.settings.defaultSnappingUnit(), self.settings.defaultSnappingTolerance(), False)

    # Setup the in-memory buffer layers
    def createBufferLayers(self):

        if (self.settings.bufferGroupIndex < 0):
            self.settings.bufferGroupIndex = self.getGroupIndex(self.settings.bufferGroupName)

        if (self.schematicBuffer is None or not self.schematicBuffer.isValid()):
            self.schematicBuffer = self.createLayer('Polygon', self.settings.schematicBufferName(), self.settings.schematicLayerName(), 'memory')
            if (self.schematicBuffer.isValid()):
                self.addLayerToLegend(self.schematicBuffer, self.settings.bufferGroupIndex)
                self.schematicBuffer.startEditing()
                self.dock.setSchematicsBuffer(self.schematicBuffer)

        if (self.polygonsBuffer is None or not self.polygonsBuffer.isValid()):
            self.polygonsBuffer = self.createLayer('Polygon', self.settings.polygonsBufferName(), self.settings.polygonsLayerName(), 'memory')
            if (self.polygonsBuffer.isValid()):
                self.addLayerToLegend(self.polygonsBuffer, self.settings.bufferGroupIndex)
                self.polygonsBuffer.startEditing()
                self.dock.setPolygonsBuffer(self.polygonsBuffer)

        if (self.linesBuffer is None or not self.linesBuffer.isValid()):
            self.linesBuffer = self.createLayer('LineString', self.settings.linesBufferName(), self.settings.linesLayerName(), 'memory')
            if (self.linesBuffer.isValid()):
                self.addLayerToLegend(self.linesBuffer, self.settings.bufferGroupIndex)
                self.linesBuffer.startEditing()
                self.dock.setLinesBuffer(self.linesBuffer)

        if (self.pointsBuffer is None or not self.pointsBuffer.isValid()):
            self.pointsBuffer = self.createLayer('Point', self.settings.pointsBufferName(), self.settings.pointsLayerName(), 'memory')
            if (self.pointsBuffer.isValid()):
                self.addLayerToLegend(self.pointsBuffer, self.settings.bufferGroupIndex)
                self.pointsBuffer.startEditing()
                self.dock.setLinesBuffer(self.pointsBuffer)

    def addLayerToLegend(self, layer, group):
        if layer.isValid():
            QgsMapLayerRegistry.instance().addMapLayer(layer)
            self.settings.iface.legendInterface().moveLayer(layer, group)
            self.settings.iface.legendInterface().refreshLayerSymbology(layer)

    def createLayer(self, type, name, style, provider):
        layer = QgsVectorLayer(type + "?crs=" + self.crs + "&index=yes", name, provider)
        if (layer.isValid()):
            attributes = [QgsField(self.settings.contextAttributeName, QVariant.Int, '', self.settings.contextAttributeSize),
                          QgsField(self.settings.sourceAttributeName,  QVariant.String, '', self.settings.sourceAttributeSize),
                          QgsField(self.settings.typeAttributeName, QVariant.String, '', self.settings.typeAttributeSize),
                          QgsField(self.settings.commentAttributeName, QVariant.String, '', self.settings.commentAttributeSize)]
            if (type.lower() == 'point'):
                attributes.append(QgsField(self.settings.elevationAttributeName, QVariant.Double, '', self.settings.elevationAttributeSize, self.settings.elevationAttributePrecision))
            layer.dataProvider().addAttributes(attributes)
            layer.loadNamedStyle(self.settings.dataDir().absolutePath() + '/' + style + '.qml')
            self._setDefaultSnapping(layer)
        #TODO set symbols?
        return layer

    def clearBuffer(self, type, buffer):
        buffer.selectAll()
        if (buffer.selectedFeatureCount() > 0):
            buffer.beginEditCommand('Clear buffer ' + type + ' data ' + str(self.context))
            buffer.deleteSelectedFeatures()
            buffer.endEditCommand()
            buffer.commitChanges()
            buffer.startEditing()
        buffer.removeSelection()

    def copyBuffer(self, type, buffer, layer):
        buffer.selectAll()
        if (buffer.selectedFeatureCount() > 0):
            layer.startEditing()
            layer.beginEditCommand('Merge context ' + type + ' data ' + str(self.context))
            layer.addFeatures(buffer.selectedFeatures(), False)
            layer.endEditCommand()
            layer.commitChanges()
        buffer.removeSelection()

    def mergeBuffers(self):
        self.copyBuffer('levels', self.pointsBuffer, self.pointsLayer)
        self.copyBuffer('lines', self.linesBuffer, self.linesLayer)
        self.copyBuffer('polygons', self.polygonsBuffer, self.polygonsLayer)
        self.copyBuffer('schematic', self.schematicBuffer, self.schematicLayer)
        self.clearBuffers()

    def clearBuffers(self):
        self.clearBuffer('levels', self.pointsBuffer)
        self.clearBuffer('lines', self.linesBuffer)
        self.clearBuffer('polygons', self.polygonsBuffer)
        self.clearBuffer('schematic', self.schematicBuffer)

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
            self.loadGeoLayer(geoFile)

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
        georefDialog = ArkGeorefDialog(rawFile, self.settings.planDir(), self.settings.separatePlanFolders(), self.crs, self.settings.gridPointsLayerName(), self.settings.gridPointsFieldX, self.settings.gridPointsFieldY)
        if (georefDialog.exec_()):
            md = georefDialog.metadata()
            self.setMetadata(md[0], md[1], md[2], md[3], md[4], md[5])
            self.loadGeoLayer(georefDialog.geoRefFile())

    def loadGeoLayer(self, geoFile):
        #TODO Check if already loaded, remove old one?
        self.geoLayer = QgsRasterLayer(geoFile.absoluteFilePath(), geoFile.completeBaseName())
        self.geoLayer.renderer().setOpacity(self.settings.planTransparency()/100.0)
        QgsMapLayerRegistry.instance().addMapLayer(self.geoLayer)
        if (self.settings.planGroupIndex < 0):
            self.settings.planGroupIndex = self.getGroupIndex(self.settings.planGroupName)
        self.settings.iface.legendInterface().moveLayer(self.geoLayer, self.settings.planGroupIndex)
        self.settings.iface.mapCanvas().setExtent(self.geoLayer.extent())

    def getGroupIndex(self, groupName):
        groupIndex = -1
        i = 0
        for name in self.settings.iface.legendInterface().groups():
            if (groupIndex < 0 and name == groupName):
                groupIndex = i
            i += 1
        if (groupIndex < 0):
            groupIndex = self.settings.iface.legendInterface().addGroup(groupName)
        return groupIndex

    # Layers Management Methods

    def showLevels(self, status):
        self.settings.iface.legendInterface().setLayerVisible(self.pointsLayer, status)

    def showLines(self, status):
        self.settings.iface.legendInterface().setLayerVisible(self.linesLayer, status)

    def showPolygons(self, status):
        self.settings.iface.legendInterface().setLayerVisible(self.polygonsLayer, status)

    def showSchematics(self, status):
        self.settings.iface.legendInterface().setLayerVisible(self.schematicLayer, status)

    def applyContextFilter(self, contextList):
        clause = '"context" = %d'
        filter = ''
        if (len(contextList) > 0):
            filter += clause % contextList[0]
            for context in contextList[1:]:
                filter += ' or '
                filter += clause % context
        self.applyLayerFilter(self.pointsLayer, filter)
        self.applyLayerFilter(self.linesLayer, filter)
        self.applyLayerFilter(self.polygonsLayer, filter)
        self.applyLayerFilter(self.schematicLayer, filter)

    def applyLayerFilter(self, layer, filter):
        if (self.settings.iface.mapCanvas().isDrawing()):
            QMessageBox.information(self.dock, 'applyLayerFilter', 'Cannot apply filter: Canvas is drawing')
            return
        if (layer.type() != QgsMapLayer.VectorLayer):
            QMessageBox.information(self.dock, 'applyLayerFilter', 'Cannot apply filter: Not a vector layer')
            return
        if (layer.isEditable()):
            QMessageBox.information(self.dock, 'applyLayerFilter', 'Cannot apply filter: Layer is in editing mode')
            return
        if (not layer.dataProvider().supportsSubsetString()):
            QMessageBox.information(self.dock, 'applyLayerFilter', 'Cannot apply filter: Subsets not supported by layer')
            return
        if (len(layer.vectorJoins()) > 0):
            QMessageBox.information(self.dock, 'applyLayerFilter', 'Cannot apply filter: Layer has joins')
            return
        layer.setSubsetString(filter)
        self.settings.iface.mapCanvas().refresh()
        self.settings.iface.legendInterface().refreshLayerSymbology(layer)

    # Levels Tool Methods

    def enableLevelsMode(self, type):
        #TODO disable all snapping
        self.settings.iface.mapCanvas().setCurrentLayer(self.pointsBuffer)
        self.settings.iface.legendInterface().setCurrentLayer(self.pointsBuffer)
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
        self.pointsBuffer.beginEditCommand('Buffer level ' + str(self.context) + ' ' + type + ' ' + str(elevation))
        self.pointsBuffer.addFeature(feature, True)
        self.pointsBuffer.endEditCommand()
        self.settings.iface.mapCanvas().refresh()

    # Map Tool Methods

    def enableLineSegmentMode(self, typeAttribute):
        #TODO configure snapping
        self.enableMapTool(typeAttribute, self.linesBuffer, QgsMapToolAddFeature.Segment, self.tr('Add line segment feature'))

    def enableLineMode(self, typeAttribute):
        #TODO configure snapping
        self.enableMapTool(typeAttribute, self.linesBuffer, QgsMapToolAddFeature.Line, self.tr('Add line feature'))

    def enablePolygonMode(self, typeAttribute):
        #TODO configure snapping
        self.enableMapTool(typeAttribute, self.polygonsBuffer, QgsMapToolAddFeature.Polygon, self.tr('Add polygon feature'))

    def enableSchematicMode(self, typeAttribute):
        #TODO configure snapping
        self.enableMapTool(typeAttribute, self.schematicBuffer, QgsMapToolAddFeature.Polygon, self.tr('Add schematic feature'))

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
