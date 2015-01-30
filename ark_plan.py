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
from PyQt4.QtCore import Qt, QSettings, QTranslator, qVersion, QCoreApplication, QVariant, QObject, SIGNAL, pyqtSignal, QFileInfo, QPoint, QDir
from PyQt4.QtGui import QAction, QIcon, QDockWidget, QInputDialog, QColor, QFileDialog, QMessageBox

from qgis.core import *
from qgis.gui import QgsMapToolEmitPoint, QgsRubberBand

# Initialize Qt resources from file resources.py
import resources_rc

# Import the code for the dialog
from ark_plan_dock import ArkPlanDock
from ark_georef_dialog import ArkGeorefDialog

import os.path
import string

class ArkPlan:
    """QGIS Plugin Implementation."""

    # User settings
    #TODO get from QSettings
    crs = 'EPSG:27700'
    geoSuffix = '_r'
    rawDir = QDir('/filebin/1120L - 100 Minories/GIS/plans/incoming/raw')
    geoDir = QDir('/filebin/1120L - 100 Minories/GIS/plans/incoming/processed')
    geoLayerOpacity = 0.5

    contextLayerGroupName = 'Context Data'
    levelsLayerName = 'MNO12_cxt_levels_pt'
    linesLayerName = 'MNO12_cxt_pl'
    polygonsLayerName = 'MNO12_cxt_pg'
    schematicLayerName = 'MNO12_cxt_schm_pg'
    gridLayerName = 'MNO12_grid_pt'
    gridLayerX = 'x'
    gridLayerY = 'y'

    contextLayerDir = QDir('/filebin/1120L - 100 Minories/GIS/vector/context_data')
    layerGroupName = 'Context Data'
    levelsLayerName = 'MNO12_cxt_levels_pt'
    linesLayerName = 'MNO12_cxt_pl'
    polygonsLayerName = 'MNO12_cxt_pg'
    schematicLayerName = 'MNO12_cxt_schm_pg'

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
    context = 0
    gridReference = QPoint(0, 0)
    source = 'No Source'
    rawFile = QFileInfo()
    geoFile = QFileInfo()
    geoLayer = QgsRasterLayer()

    layerGroupIndex = -1
    levelsLayer = None
    linesLayer = None
    polygonsLayer = None
    schematicLayer = None

    bufferGroupIndex = -1
    levelsBuffer = None
    linesBuffer = None
    polygonsBuffer = None
    schematicBuffer = None

    levelsMapTool = None
    hachureMapTool = None
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

    def unload(self):

        # Remove the levels form the legend
        if self.initialised:
            QgsMapLayerRegistry.instance().removeMapLayer(self.levelsBuffer.id())
            QgsMapLayerRegistry.instance().removeMapLayer(self.linesBuffer.id())
            QgsMapLayerRegistry.instance().removeMapLayer(self.polygonsBuffer.id())
            QgsMapLayerRegistry.instance().removeMapLayer(self.schematicBuffer.id())
            self.iface.legendInterface().removeGroup(self.bufferLegendGroup)

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
        self.populatePlanMetadata()

    def groupIndexChanged(self, oldIndex, newIndex):
        if (oldIndex == self.layerGroupIndex):
            self.layerGroupIndex = newIndex
        elif (oldIndex == self.bufferGroupIndex):
            self.bufferGroupIndex = newIndex

    def getLayerByName(self, dir, name, styleName, groupIndex):
        # If the layer is already loaded, use it and return
        layerList = QgsMapLayerRegistry.instance().mapLayersByName(name)
        if (len(layerList) > 0):
            return layerList[0]
        #TODO Check if exists, if not then create!
        # Otherwise load the layer and add it to the legend
        layer = QgsVectorLayer(dir + '/' + name + '.shp', name, "ogr")
        if (layer.isValid()):
            layer.loadNamedStyle(self.stylesDir + '/' + styleName + '.qml')
            QgsMapLayerRegistry.instance().addMapLayer(layer)
            self.iface.legendInterface().moveLayer(layer, groupIndex)
            self.iface.legendInterface().refreshLayerSymbology(layer)
            return layer
        return None

    def initialise(self):

        # Init gui stuff
        self.dock.loadRawFileSelected.connect(self.loadRawPlan)
        self.dock.georefSelected.connect(self.georeferencePlan)
        self.dock.loadGeoFileSelected.connect(self.loadGeoPlan)
        self.dock.contextChanged.connect(self.setContext)
        self.dock.gridReferenceChanged.connect(self.setGridReference)
        self.dock.sourceChanged.connect(self.setSource)

        self.dock.selectedLevelsMode.connect(self.enableLevelsMode)
        self.dock.selectedLineMode.connect(self.enableLineMode)
        self.dock.selectedHachureMode.connect(self.enableHachureMode)
        self.dock.selectedPolygonMode.connect(self.enablePolygonMode)
        self.dock.selectedSchematicMode.connect(self.enableSchematicMode)

        # If the legend indexes change make sure we stay updated
        self.iface.legendInterface().groupIndexChanged.connect(self.groupIndexChanged)

        # TODO Find why this doesn't work!
        projectCRS = unicode(QgsProject.instance().readEntry("SpatialRefSys", "/ProjectCRSProj4String"))

        # Load the context layers if not already loaded
        haveLayerGroup = False
        index = 0
        for groupName in self.iface.legendInterface().groups():
            if (groupName == self.layerGroupName)
                haveLayerGroup = True
                self.layerGroupIndex = index
        if (not haveLayerGroup
        if (self.gridLayer is None):
            self.gridLayer = getLayerByName(self.contextLayerDir, self.gridLayerName, self.stylesDir, self.gridStyleName, self.layerGroupIndex)
        if (self.schematicLayer is None):
            self.schematicLayer = getLayerByName(self.contextLayerDir, self.schematicLayerName, self.stylesDir, self.schematicStyleName, self.layerGroupIndex)
        if (self.polygonsLayer is None):
            self.polygonsLayer = getLayerByName(self.contextLayerDir, self.polygonsLayerName, self.stylesDir, self.polygonsStyleName, self.layerGroupIndex)
        if (self.linesLayer is None):
            self.linesLayer = getLayerByName(self.contextLayerDir, self.polygonsLayerName, self.stylesDir, self.linesStyleName, self.layerGroupIndex)
        if (self.levelsLayer is None):
            self.levelsLayer = getLayerByName(self.contextLayerDir, self.levelsLayerName, self.stylesDir, self.levelsStyleName, self.layerGroupIndex)

        # Setup the in-memory buffer layers
        self.bufferLegendGroup = self.iface.legendInterface().addGroup(self.contextBufferGroupName)
        if self.schematicBuffer is None:
            self.schematicBuffer = self.createPolygonLayer(self.schematicBufferName, 'memory')
            self.schematicBuffer.startEditing()
            self.schematicBuffer.loadNamedStyle(self.stylesDir + '/' + self.schematicStyleName + '.qml')
            QgsMapLayerRegistry.instance().addMapLayer(self.schematicBuffer)
            self.iface.legendInterface().moveLayer(self.schematicBuffer, self.bufferLegendGroup)
            self.iface.legendInterface().refreshLayerSymbology(self.schematicBuffer)
        if self.polygonsBuffer is None:
            self.polygonsBuffer = self.createPolygonLayer(self.polygonsBufferName, 'memory')
            self.polygonsBuffer.startEditing()
            self.polygonsBuffer.loadNamedStyle(self.stylesDir + '/' + self.polygonsStyleName + '.qml')
            QgsMapLayerRegistry.instance().addMapLayer(self.polygonsBuffer)
            self.iface.legendInterface().moveLayer(self.polygonsBuffer, self.bufferLegendGroup)
            self.iface.legendInterface().refreshLayerSymbology(self.polygonsBuffer)
        if self.linesBuffer is None:
            self.linesBuffer = self.createLinesLayer(self.linesBufferName, 'memory')
            self.linesBuffer.startEditing()
            self.linesBuffer.loadNamedStyle(self.stylesDir + '/' + self.linesStyleName + '.qml')
            QgsMapLayerRegistry.instance().addMapLayer(self.linesBuffer)
            self.iface.legendInterface().moveLayer(self.linesBuffer, self.bufferLegendGroup)
            self.iface.legendInterface().refreshLayerSymbology(self.linesBuffer)
        if self.levelsBuffer is None:
            self.levelsBuffer = self.createLevelsLayer(self.levelsBufferName, 'memory')
            self.levelsBuffer.startEditing()
            self.levelsBuffer.loadNamedStyle(self.stylesDir + '/' + self.levelsStyleName + '.qml')
            QgsMapLayerRegistry.instance().addMapLayer(self.levelsBuffer)
            self.iface.legendInterface().moveLayer(self.levelsBuffer, self.bufferLegendGroup)
            self.iface.legendInterface().refreshLayerSymbology(self.levelsBuffer)

        # Setup the map tools
        if self.levelsMapTool is None:
            self.levelsMapTool = LevelsMapTool(self.iface.mapCanvas())
            self.levelsMapTool.levelAdded.connect(self.addLevel)
        if self.hachureMapTool is None:
            self.hachureMapTool = HacureMapTool(self.iface.mapCanvas())
            self.hachureMapTool.hachureAdded.connect(self.addHachure)
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

    def createLinesLayer(self, name, provider):
        vl = QgsVectorLayer("Line?crs=" + self.crs + "&index=yes", name, provider)
        pr = vl.dataProvider()
        pr.addAttributes([QgsField(self.contextAttributeName, QVariant.Int, '', self.contextAttributeSize),
                          QgsField(self.sourceAttributeName,  QVariant.String, '', self.sourceAttributeSize),
                          QgsField(self.typeAttributeName, QVariant.String, '', self.typeAttributeSize),
                          QgsField(self.commentAttributeName, QVariant.String, '', self.commentAttributeSize)])
        #TODO set symbols
        return vl

    def createPolygonLayer(self, name, provider):
        vl = QgsVectorLayer("Polygon?crs=" + self.crs + "&index=yes", name, provider)
        pr = vl.dataProvider()
        pr.addAttributes([QgsField(self.contextAttributeName, QVariant.Int, '', self.contextAttributeSize),
                          QgsField(self.sourceAttributeName,  QVariant.String, '', self.sourceAttributeSize),
                          QgsField(self.typeAttributeName, QVariant.String, '', self.typeAttributeSize),
                          QgsField(self.commentAttributeName, QVariant.String, '', self.commentAttributeSize)])
        #TODO set symbols
        return vl

    def mergeBuffers(self):
        #TODO copy from buffers to master
        self.clearBuffers()

    def clearBuffers(self):
        self.levelsBuffer.rollback()
        self.linesBuffer.rollback()
        self.polygonsBuffer.rollback()
        self.schematicBuffer.rollback()

    # Plan Tools

    def populatePlanMetadata(self):
        filename = self.rawFile.baseName()
        if not filename:
            filename = self.geoFile.baseName()
        if filename:
            elements = string.split(filename, '_')
            self.dock.setFile(filename)
            self.dock.setSite(elements[0])
            self.dock.setContext(int(elements[1][1:]))
            self.dock.setGridReference(int(elements[2][1:]), int(elements[3][1:]))
            self.dock.setSource(elements[1][1:])
        else:
            self.dock.setFile(self.tr('No file loaded'))
            self.dock.setSite('')
            self.dock.setContext(0)
            self.dock.setGridReference(0, 0)
            self.dock.setSource(self.tr('No source selected'))

    def loadRawPlan(self):
        fileName = unicode(QFileDialog.getOpenFileName(None, self.tr('Load Raw Plan'), self.rawDir.absolutePath(),
                                                       self.tr('Image Files (*.png *.tif *.tiff)')))
        if fileName:
            self.rawFile = QFileInfo(fileName)
            self.geoFile = QFileInfo(self.geoDir, self.rawFile.completeBaseName() + self.geoSuffix + '.tif')
            #TODO check if geo file already exists?
            self.populatePlanMetadata()
            self.georeferencePlan()

    def loadGeoPlan(self):
        fileName = unicode(QFileDialog.getOpenFileName(None, self.tr('Load Georeferenced Plan'), self.geoDir.absolutePath(),
                                                       self.tr('GeoTiff Files (*.tif *.tiff)')))
        if fileName:
            self.geoFile = QFileInfo(fileName)
            #TODO set raw file
            self.rawFile = QFileInfo()
            self.populatePlanMetadata()
            self.loadGeoLayer()

    def setContext(self, context):
        self.context = context

    def setGridReference(self, easting, northing):
        self.gridReference = QPoint(easting, northing)

    def setSource(self, source):
        self.source = source

    # Georeference Tools

    def georeferencePlan(self):
        georefDialog = ArkGeorefDialog(self.rawFile, self.geoFile, self.crs, self.gridReference, self.gridLayerName, self.gridLayerX, self.gridLayerY)
        if (georefDialog.exec_()):
            self.loadGeoLayer()

    def loadGeoLayer(self):
        #TODO Check if already loaded, remove old one?
        self.geoLayer = QgsRasterLayer(self.geoFile.absoluteFilePath(), self.geoFile.completeBaseName())
        self.geoLayer.renderer().setOpacity(self.geoLayerOpacity)
        QgsMapLayerRegistry.instance().addMapLayer(self.geoLayer)
        #TODO Add to own group?
        self.iface.legendInterface().moveLayer(self.geoLayer, self.bufferLegendGroup)
        self.iface.mapCanvas().setExtent(self.geoLayer.extent())

    # Levels Tool Methods

    def addLevel(self, point, elevation):
        feature = QgsFeature()
        feature.setGeometry(QgsGeometry.fromPoint(point))
        feature.setAttributes([self.context, self.source, elevation])
        self.levelsBuffer.addFeature(feature, True)
        self.iface.mapCanvas().refresh()

    def enableLevelsMode(self):
        #TODO disable all snapping
        self.iface.mapCanvas().setCurrentLayer(self.levelsBuffer)
        self.iface.legendInterface().setCurrentLayer(self.levelsBuffer)
        self.iface.mapCanvas().setMapTool(self.levelsMapTool)

    # Hachure Tool Methods

    def enableHachureMode(self, type):
        #TODO configure snapping
        self.iface.mapCanvas().setCurrentLayer(self.linesBuffer)
        self.iface.legendInterface().setCurrentLayer(self.linesBuffer)
        self.hachureMapTool.setType(type)
        self.iface.mapCanvas().setMapTool(self.hachureMapTool)

    def addHachure(self, point1, point2, type):
        feature = QgsFeature()
        feature.setGeometry(QgsGeometry.fromPolyline([point1, point2]))
        feature.setAttributes([self.context, self.source, type])
        self.linesBuffer.addFeature(feature, True)
        self.iface.mapCanvas().refresh()

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
        feature.setAttributes([self.context, self.source, type])
        self.linesBuffer.addFeature(feature, True)
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
        feature.setAttributes([self.context, self.source, type])
        self.polygonsBuffer.addFeature(feature, True)
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
        feature.setAttributes([self.context, self.source, type])
        self.schematicBuffer.addFeature(feature, True)
        self.iface.mapCanvas().refresh()

class LevelsMapTool(QgsMapToolEmitPoint):

    levelAdded = pyqtSignal(QgsPoint, float)

    def __init__(self, canvas):
        self.canvas = canvas
        QgsMapToolEmitPoint.__init__(self, canvas)

    def canvasPressEvent(self, e):
        if e.button() != Qt.LeftButton:
            return
        elevation, ok = QInputDialog.getDouble(None, 'Add Level', 'Please enter the elevation in meters (m):',
                                               0, -100, 100, 2)
        if ok:
            point = self.toMapCoordinates(e.pos())
            self.levelAdded.emit(point, elevation)

# Map Tool to take two points and draw a hachure
class HacureMapTool(QgsMapToolEmitPoint):

    hachureAdded = pyqtSignal(QgsPoint, QgsPoint, 'QString')
    startPoint = None
    endPoint = None
    rubberBand = None
    hachureType = 'hch'

    def __init__(self, canvas, type='hch'):
        self.canvas = canvas
        self.hachureType = type
        QgsMapToolEmitPoint.__init__(self, canvas)

    def canvasMoveEvent(self, e):
        if self.startPoint:
            toPoint = self.toMapCoordinates(e.pos())
            if self.rubberBand:
                self.rubberBand.reset()
            else:
                self.rubberBand = QgsRubberBand(self.canvas, False)
                self.rubberBand.setColor(QColor(Qt.red))
            points  = [self.startPoint, toPoint]
            self.rubberBand.setToGeometry(QgsGeometry.fromPolyline(points), None)

    def canvasPressEvent(self, e):
        if e.button() != Qt.LeftButton:
            self.rubberBand.reset()
            self.startPoint = None
            self.endPoint = None
            return
        if self.startPoint is None:
            self.startPoint = self.toMapCoordinates(e.pos())
        else:
            self.endPoint = self.toMapCoordinates(e.pos())
            self.rubberBand.reset()
            self.hachureAdded.emit(self.startPoint, self.endPoint, self.hachureType)
            self.startPoint = None
            self.endPoint = None

    def type(self):
        return self.hachureType

    def setType(self, type):
        self.hachureType = type

# Map Tool to take mulitple points and draw a line
class LineMapTool(QgsMapToolEmitPoint):

    lineAdded = pyqtSignal(list, 'QString')
    points = []
    rubberBand = None
    lineType = 'ext'

    def __init__(self, canvas, type='ext'):
        self.canvas = canvas
        self.lineType = type
        QgsMapToolEmitPoint.__init__(self, canvas)

    def canvasMoveEvent(self, e):
        if len(self.points) > 0:
            rbPoints = list(self.points)
            toPoint = self.toMapCoordinates(e.pos())
            rbPoints.append(toPoint)
            if self.rubberBand:
                self.rubberBand.reset()
            else:
                self.rubberBand = QgsRubberBand(self.canvas, False)
                self.rubberBand.setColor(QColor(Qt.red))
            self.rubberBand.setToGeometry(QgsGeometry.fromPolyline(rbPoints), None)

    def canvasPressEvent(self, e):
        if e.button() == Qt.LeftButton:
            point = self.toMapCoordinates(e.pos())
            self.points.append(point)
        elif e.button() == Qt.RightButton:
            self.rubberBand.reset()
            self.lineAdded.emit(self.points, self.lineType)
            self.points = []
        else:
            self.rubberBand.reset()
            self.points = []

    def type(self):
        return self.lineType

    def setType(self, type):
        self.lineType = type

# Map Tool to take mulitple points and draw a line
class PolygonMapTool(QgsMapToolEmitPoint):

    polygonAdded = pyqtSignal(list, 'QString')
    points = []
    rubberBand = None
    polygonType = 'ext'

    def __init__(self, canvas, type='ext'):
        self.canvas = canvas
        self.lineType = type
        QgsMapToolEmitPoint.__init__(self, canvas)

    def canvasMoveEvent(self, e):
        if len(self.points) > 0:
            rbPoints = list(self.points)
            toPoint = self.toMapCoordinates(e.pos())
            rbPoints.append(toPoint)
            if self.rubberBand:
                self.rubberBand.reset()
            else:
                self.rubberBand = QgsRubberBand(self.canvas, False)
                self.rubberBand.setColor(QColor(Qt.red))
            if len(self.points) == 1:
                self.rubberBand.setToGeometry(QgsGeometry.fromPolyline(rbPoints), None)
            else:
                self.rubberBand.setToGeometry(QgsGeometry.fromPolygon([rbPoints]), None)

    def canvasPressEvent(self, e):
        if e.button() == Qt.LeftButton:
            point = self.toMapCoordinates(e.pos())
            self.points.append(point)
        elif e.button() == Qt.RightButton:
            self.rubberBand.reset()
            self.polygonAdded.emit(self.points, self.polygonType)
            self.points = []
        else:
            self.rubberBand.reset()
            self.points = []

    def type(self):
        return self.polygonType

    def setType(self, type):
        self.polygonType = type
