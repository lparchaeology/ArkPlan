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
from ark_map_tools import *
from ark_plan_util import *

import os.path
import string

class ArkPlan:
    """QGIS Plugin Implementation."""

    # User settings
    #TODO get from QSettings
    crs = 'EPSG:27700'
    rawDir = QDir('/filebin/1120L - 100 Minories/GIS/plans/incoming/raw')
    geoDir = QDir('/filebin/1120L - 100 Minories/GIS/plans/incoming/processed')
    geoLayerOpacity = 0.5

    contextLayerDir = QDir('/filebin/1120L - 100 Minories/GIS/vector/context_data')
    contextLayerGroupName = 'Context Data'
    levelsLayerName = 'MNO12_cxt_levels_pt'
    linesLayerName = 'MNO12_cxt_pl'
    polygonsLayerName = 'MNO12_cxt_pg'
    schematicLayerName = 'MNO12_cxt_schm_pg'
    gridPointsLayerName = 'MNO12_grid_pt'
    gridPointsLayerX = 'x'
    gridPointsLayerY = 'y'

    bufferGroupName = 'ArkPlan Contexts'
    levelsBufferName = levelsLayerName + '_mem'
    linesBufferName = linesLayerName + '_mem'
    polygonsBufferName = polygonsLayerName + '_mem'
    schematicBufferName = schematicLayerName + '_mem'

    stylesDir = contextLayerDir
    levelsStyleName = 'cxt_levels_type_style'
    linesStyleName = 'cxt_line_type_style'
    polygonsStyleName = 'cxt_poly_type_style'
    schematicStyleName = 'cxt_schm_type_style'
    gridStyleName = 'grid_point_type_style'

    contextAttributeName = 'cxt_no'
    contextAttributeSize = 5
    sourceAttributeName = 'source'
    sourceAttributeSize = 20
    typeAttributeName = 'type'
    typeAttributeSize = 10
    commentAttributeName = 'comment'
    commentAttributeSize = 100
    elevationAttributeName = 'elevation'
    elevationAttributeSize = 5
    elevationAttributePrecision = 5

    # Internal variables
    initialised = False
    siteCode = ''
    context = 0
    source = '0'
    comment = ''
    geoLayer = QgsRasterLayer()

    layerGroupIndex = -1
    levelsLayer = None
    linesLayer = None
    polygonsLayer = None
    schematicLayer = None
    gridPointsLayer = None

    bufferGroupIndex = -1
    levelsBuffer = None
    linesBuffer = None
    polygonsBuffer = None
    schematicBuffer = None

    levelsMapTool = None
    lineSegmentMapTool = None
    lineMapTool = None
    polygonMapTool = None
    schematicMapTool = None

    def __init__(self, iface):
        """Constructor.

        :param iface: An interface instance that will be passed to this class
            which provides the hook by which you can manipulate the QGIS
            application at run time.
        :type iface: QgsInterface
        """
        # Save reference to the QGIS interface
        self.iface = iface
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
        self.toolbar = self.iface.addToolBar(u'ArkPlan')
        self.toolbar.setObjectName(u'ArkPlan')

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

        if status_tip is not None:
            action.setStatusTip(status_tip)

        if whats_this is not None:
            action.setWhatsThis(whats_this)

        if add_to_toolbar:
            self.toolbar.addAction(action)

        if add_to_menu:
            self.iface.addPluginToMenu(
                self.menu,
                action)

        self.actions.append(action)

        return action

    def initGui(self):
        """Create the menu entries and toolbar icons inside the QGIS GUI."""

        icon_path = ':/plugins/ArkPlan/icon.png'
        self.add_action(
            icon_path,
            text=self.tr(u'ArkPlan'),
            callback=self.run,
            parent=self.iface.mainWindow())

        self.dock = ArkPlanDock(self.iface)

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
        if (self.levelsBuffer is not None and self.levelsBuffer.isValid()):
            QgsMapLayerRegistry.instance().removeMapLayer(self.levelsBuffer.id())
        if self.linesBuffer is not None:
            QgsMapLayerRegistry.instance().removeMapLayer(self.linesBuffer.id())
        if self.polygonsBuffer is not None:
            QgsMapLayerRegistry.instance().removeMapLayer(self.polygonsBuffer.id())
        if self.schematicBuffer is not None:
            QgsMapLayerRegistry.instance().removeMapLayer(self.schematicBuffer.id())
        if (self.bufferGroupIndex >= 0):
            self.iface.legendInterface().removeGroup(self.bufferGroupIndex)

        """Removes the plugin menu item and icon from QGIS GUI."""
        for action in self.actions:
            self.iface.removePluginMenu(
                self.tr(u'&ArkPlan'),
                action)
            self.iface.removeToolBarIcon(action)

        # Unload the dock
        self.iface.removeDockWidget(self.dock)
        self.dock.deleteLater()

    def run(self):
        if not self.initialised:
            self.initialise()
        self.iface.addDockWidget(Qt.RightDockWidgetArea, self.dock)

    def groupIndexChanged(self, oldIndex, newIndex):
        if (oldIndex == self.layerGroupIndex):
            self.layerGroupIndex = newIndex
        elif (oldIndex == self.bufferGroupIndex):
            self.bufferGroupIndex = newIndex

    def loadLayerByName(self, dir, name, styleDir, styleName, groupIndex):
        # If the layer is already loaded, use it and return
        layerList = QgsMapLayerRegistry.instance().mapLayersByName(name)
        if (len(layerList) > 0):
            self.iface.legendInterface().moveLayer(layerList[0], groupIndex)
            return layerList[0]
        #TODO Check if exists, if not then create!
        # Otherwise load the layer and add it to the legend
        layer = QgsVectorLayer(dir.absolutePath() + '/' + name + '.shp', name, "ogr")
        if (layer.isValid()):
            layer.loadNamedStyle(styleDir.absolutePath() + '/' + styleName + '.qml')
            QgsMapLayerRegistry.instance().addMapLayer(layer)
            self.iface.legendInterface().moveLayer(layer, groupIndex)
            self.iface.legendInterface().refreshLayerSymbology(layer)
            return layer
        return None

    def initialise(self):

        # TODO Find why this doesn't work!
        projectCRS = unicode(QgsProject.instance().readEntry("SpatialRefSys", "/ProjectCRSProj4String"))

        # If the legend indexes change make sure we stay updated
        self.iface.legendInterface().groupIndexChanged.connect(self.groupIndexChanged)

        self.initMapTools()
        self.createBufferLayers()
        self.loadContextLayers()

    # Setup the map tools
    def initMapTools(self):
        if self.levelsMapTool is None:
            self.levelsMapTool = LevelsMapTool(self.iface.mapCanvas())
            self.levelsMapTool.levelAdded.connect(self.addLevel)
        if self.lineSegmentMapTool is None:
            self.lineSegmentMapTool = LineSegmentMapTool(self.iface.mapCanvas())
            self.lineSegmentMapTool.lineSegmentAdded.connect(self.addLine)
        if self.lineMapTool is None:
            self.lineMapTool = LineMapTool(self.iface.mapCanvas())
            self.lineMapTool.lineAdded.connect(self.addLine)
        if self.polygonMapTool is None:
            self.polygonMapTool = PolygonMapTool(self.iface.mapCanvas())
            self.polygonMapTool.polygonAdded.connect(self.addPolygon)
        if self.schematicMapTool is None:
            self.schematicMapTool = PolygonMapTool(self.iface.mapCanvas())
            self.schematicMapTool.polygonAdded.connect(self.addSchematic)
        self.initialised = True

    # Load the context layers if not already loaded
    def loadContextLayers(self):
        haveLayerGroup = False
        i = 0
        for groupName in self.iface.legendInterface().groups():
            if (not haveLayerGroup and groupName == self.contextLayerGroupName):
                haveLayerGroup = True
                self.layerGroupIndex = i
            i += 1
        if (not haveLayerGroup):
            self.layerGroupIndex = self.iface.legendInterface().addGroup(self.contextLayerGroupName)
        if (self.schematicLayer is None):
            self.schematicLayer = self.loadLayerByName(self.contextLayerDir, self.schematicLayerName, self.stylesDir, self.schematicStyleName, self.layerGroupIndex)
            self.dock.setSchematicsLayer(self.schematicLayer)
        if (self.polygonsLayer is None):
            self.polygonsLayer = self.loadLayerByName(self.contextLayerDir, self.polygonsLayerName, self.stylesDir, self.polygonsStyleName, self.layerGroupIndex)
            self.dock.setPolygonsLayer(self.polygonsLayer)
        if (self.linesLayer is None):
            self.linesLayer = self.loadLayerByName(self.contextLayerDir, self.linesLayerName, self.stylesDir, self.linesStyleName, self.layerGroupIndex)
            self.dock.setLinesLayer(self.linesLayer)
        if (self.levelsLayer is None):
            self.levelsLayer = self.loadLayerByName(self.contextLayerDir, self.levelsLayerName, self.stylesDir, self.levelsStyleName, self.layerGroupIndex)
        if (self.gridPointsLayer is None):
            self.gridPointsLayer = self.loadLayerByName(self.contextLayerDir, self.gridPointsLayerName, self.stylesDir, self.gridStyleName, self.layerGroupIndex)

    # Setup the in-memory buffer layers
    def createBufferLayers(self):

        self.bufferGroupIndex = self.iface.legendInterface().addGroup(self.bufferGroupName)

        if self.schematicBuffer is None:
            self.schematicBuffer = self.createStandardLayer('Polygon', self.schematicBufferName, 'memory')
            QgsMapLayerRegistry.instance().addMapLayer(self.schematicBuffer)
            self.dock.setSchematicsBuffer(self.schematicBuffer)
        self.schematicBuffer.startEditing()
        self.schematicBuffer.loadNamedStyle(self.stylesDir.absolutePath() + '/' + self.schematicStyleName + '.qml')
        self.iface.legendInterface().moveLayer(self.schematicBuffer, self.bufferGroupIndex)
        self.iface.legendInterface().refreshLayerSymbology(self.schematicBuffer)

        if self.polygonsBuffer is None:
            self.polygonsBuffer = self.createStandardLayer('Polygon', self.polygonsBufferName, 'memory')
            QgsMapLayerRegistry.instance().addMapLayer(self.polygonsBuffer)
            self.dock.setPolygonsBuffer(self.polygonsBuffer)
        self.polygonsBuffer.startEditing()
        self.polygonsBuffer.loadNamedStyle(self.stylesDir.absolutePath() + '/' + self.polygonsStyleName + '.qml')
        self.iface.legendInterface().moveLayer(self.polygonsBuffer, self.bufferGroupIndex)
        self.iface.legendInterface().refreshLayerSymbology(self.polygonsBuffer)

        if (self.linesBuffer is None or not self.linesBuffer.isValid()):
            self.linesBuffer = self.createStandardLayer('LineString', self.linesBufferName, 'memory')
        if self.linesBuffer.isValid():
            QgsMapLayerRegistry.instance().addMapLayer(self.linesBuffer)
            self.dock.setLinesBuffer(self.linesBuffer)
            self.linesBuffer.loadNamedStyle(self.stylesDir.absolutePath() + '/' + self.linesStyleName + '.qml')
            self.iface.legendInterface().moveLayer(self.linesBuffer, self.bufferGroupIndex)
            self.iface.legendInterface().refreshLayerSymbology(self.linesBuffer)
            self.linesBuffer.startEditing()

        if self.levelsBuffer is None:
            self.levelsBuffer = self.createLevelsLayer(self.levelsBufferName, 'memory')
            QgsMapLayerRegistry.instance().addMapLayer(self.levelsBuffer)
        self.levelsBuffer.startEditing()
        self.levelsBuffer.loadNamedStyle(self.stylesDir.absolutePath() + '/' + self.levelsStyleName + '.qml')
        self.iface.legendInterface().moveLayer(self.levelsBuffer, self.bufferGroupIndex)
        self.iface.legendInterface().refreshLayerSymbology(self.levelsBuffer)

    def createLevelsLayer(self, name, provider):
        vl = QgsVectorLayer("Point?crs=" + self.crs + "&index=yes", name, provider)
        pr = vl.dataProvider()
        pr.addAttributes([QgsField(self.contextAttributeName, QVariant.Int, '', self.contextAttributeSize),
                          QgsField(self.sourceAttributeName,  QVariant.String, '', self.sourceAttributeSize),
                          QgsField(self.typeAttributeName, QVariant.String, '', self.typeAttributeSize),
                          QgsField(self.commentAttributeName, QVariant.String, '', self.commentAttributeSize),
                          QgsField(self.elevationAttributeName, QVariant.Double, '', self.elevationAttributeSize, self.elevationAttributePrecision)])
        #TODO set symbols
        return vl

    def createStandardLayer(self, type, name, provider):
        vl = QgsVectorLayer(type + "?crs=" + self.crs + "&index=yes", name, provider)
        if (vl.isValid()):
            pr = vl.dataProvider()
            pr.addAttributes([QgsField(self.contextAttributeName, QVariant.Int, '', self.contextAttributeSize),
                              QgsField(self.sourceAttributeName,  QVariant.String, '', self.sourceAttributeSize),
                              QgsField(self.typeAttributeName, QVariant.String, '', self.typeAttributeSize),
                              QgsField(self.commentAttributeName, QVariant.String, '', self.commentAttributeSize)])
        #TODO set symbols
        return vl

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
        self.copyBuffer('levels', self.levelsBuffer, self.levelsLayer)
        self.copyBuffer('lines', self.linesBuffer, self.linesLayer)
        self.copyBuffer('polygons', self.polygonsBuffer, self.polygonsLayer)
        self.copyBuffer('schematic', self.schematicBuffer, self.schematicLayer)
        self.clearBuffers()

    def clearBuffers(self):
        self.clearBuffer('levels', self.levelsBuffer)
        self.clearBuffer('lines', self.linesBuffer)
        self.clearBuffer('polygons', self.polygonsBuffer)
        self.clearBuffer('schematic', self.schematicBuffer)

    # Plan Tools

    def setMetadata(self, siteCode, type, number, suffix, easting, northing):
        self.dock.setSite(siteCode)
        self.dock.setContext(number)
        self.dock.setSource(str(number))

    def loadRawPlan(self):
        fileName = unicode(QFileDialog.getOpenFileName(None, self.tr('Load Raw Plan'), self.rawDir.absolutePath(),
                                                       self.tr('Image Files (*.png *.tif *.tiff)')))
        if fileName:
            self.georeferencePlan(QFileInfo(fileName))

    def loadGeoPlan(self):
        fileName = unicode(QFileDialog.getOpenFileName(None, self.tr('Load Georeferenced Plan'), self.geoDir.absolutePath(),
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
        georefDialog = ArkGeorefDialog(rawFile, self.geoDir, self.crs, self.gridPointsLayerName, self.gridPointsLayerX, self.gridPointsLayerY)
        if (georefDialog.exec_()):
            md = georefDialog.metadata()
            self.setMetadata(md[0], md[1], md[2], md[3], md[4], md[5])
            self.loadGeoLayer(georefDialog.geoRefFile())

    def loadGeoLayer(self, geoFile):
        #TODO Check if already loaded, remove old one?
        self.geoLayer = QgsRasterLayer(geoFile.absoluteFilePath(), geoFile.completeBaseName())
        self.geoLayer.renderer().setOpacity(self.geoLayerOpacity)
        QgsMapLayerRegistry.instance().addMapLayer(self.geoLayer)
        #TODO Add to own group?
        self.iface.legendInterface().moveLayer(self.geoLayer, self.bufferGroupIndex)
        self.iface.mapCanvas().setExtent(self.geoLayer.extent())

    # Layers Management Methods

    def showLevels(self, status):
        self.iface.legendInterface().setLayerVisible(self.levelsLayer, status)

    def showLines(self, status):
        self.iface.legendInterface().setLayerVisible(self.linesLayer, status)

    def showPolygons(self, status):
        self.iface.legendInterface().setLayerVisible(self.polygonsLayer, status)

    def showSchematics(self, status):
        self.iface.legendInterface().setLayerVisible(self.schematicLayer, status)

    def applyContextFilter(self, contextList):
        clause = '"cxt_no" = %d'
        filter = ''
        if (len(contextList) > 0):
            filter += clause % contextList[0]
            for context in contextList[1:]:
                filter += ' or '
                filter += clause % context
        self.applyLayerFilter(self.levelsLayer, filter)
        self.applyLayerFilter(self.linesLayer, filter)
        self.applyLayerFilter(self.polygonsLayer, filter)
        self.applyLayerFilter(self.schematicLayer, filter)

    def applyLayerFilter(self, layer, filter):
        if (self.iface.mapCanvas().isDrawing()):
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
        self.iface.mapCanvas().refresh()
        self.iface.legendInterface().refreshLayerSymbology(layer)

    # Levels Tool Methods

    def enableLevelsMode(self, type):
        #TODO disable all snapping
        self.iface.mapCanvas().setCurrentLayer(self.levelsBuffer)
        self.iface.legendInterface().setCurrentLayer(self.levelsBuffer)
        self.levelsMapTool.setType(type)
        self.iface.mapCanvas().setMapTool(self.levelsMapTool)

    def addLevel(self, point, type, elevation):
        feature = QgsFeature()
        feature.setGeometry(QgsGeometry.fromPoint(point))
        feature.setAttributes([self.context, self.source, type, self.comment, elevation])
        self.levelsBuffer.beginEditCommand('Buffer level ' + str(self.context) + ' ' + type + ' ' + str(elevation))
        self.levelsBuffer.addFeature(feature, True)
        self.levelsBuffer.endEditCommand()
        self.iface.mapCanvas().refresh()

    # Line Segment Tool Methods

    def enableLineSegmentMode(self, type):
        #TODO configure snapping
        self.iface.mapCanvas().setCurrentLayer(self.linesBuffer)
        self.iface.legendInterface().setCurrentLayer(self.linesBuffer)
        self.lineSegmentMapTool.setType(type)
        self.iface.mapCanvas().setMapTool(self.lineSegmentMapTool)

    # Line Tool Methods

    def enableLineMode(self, type):
        #TODO configure snapping
        self.iface.mapCanvas().setCurrentLayer(self.linesBuffer)
        self.iface.legendInterface().setCurrentLayer(self.linesBuffer)
        self.lineMapTool.setType(type)
        self.iface.mapCanvas().setMapTool(self.lineMapTool)

    def addLine(self, points, type):
        feature = QgsFeature()
        feature.setGeometry(QgsGeometry.fromPolyline(points))
        feature.setAttributes([self.context, self.source, type, self.comment])
        self.linesBuffer.beginEditCommand('Buffer line ' + str(self.context) + type)
        self.linesBuffer.addFeature(feature, True)
        self.linesBuffer.endEditCommand()
        self.iface.mapCanvas().refresh()

    # Polygon Tool Methods

    def enablePolygonMode(self, type):
        #TODO configure snapping
        self.iface.mapCanvas().setCurrentLayer(self.polygonsBuffer)
        self.iface.legendInterface().setCurrentLayer(self.polygonsBuffer)
        self.polygonMapTool.setType(type)
        self.iface.mapCanvas().setMapTool(self.polygonMapTool)

    def addPolygon(self, points, type):
        feature = QgsFeature()
        feature.setGeometry(QgsGeometry.fromPolygon([points]))
        feature.setAttributes([self.context, self.source, type, self.comment])
        self.polygonsBuffer.beginEditCommand('Buffer polygon ' + str(self.context) + type)
        self.polygonsBuffer.addFeature(feature, True)
        self.polygonsBuffer.endEditCommand()
        self.iface.mapCanvas().refresh()

    # Schematic Tool Methods

    def enableSchematicMode(self, type):
        #TODO configure snapping
        self.iface.mapCanvas().setCurrentLayer(self.schematicBuffer)
        self.iface.legendInterface().setCurrentLayer(self.schematicBuffer)
        self.schematicMapTool.setType(type)
        self.iface.mapCanvas().setMapTool(self.schematicMapTool)

    def addSchematic(self, points, type):
        feature = QgsFeature()
        feature.setGeometry(QgsGeometry.fromPolygon([points]))
        feature.setAttributes([self.context, self.source, type, self.comment])
        self.schematicBuffer.beginEditCommand('Buffer schematic ' + str(self.context) + type)
        self.schematicBuffer.addFeature(feature, True)
        self.schematicBuffer.endEditCommand()
        self.iface.mapCanvas().refresh()
