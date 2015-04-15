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
from PyQt4.QtCore import Qt, QVariant, QFileInfo, QObject
from PyQt4.QtGui import QAction, QIcon, QFileDialog

from qgis.core import *

from ..core.settings import Settings
from ..core.layers import LayerManager
from ..core.map_tools import *

from ..georef.georef_dialog import GeorefDialog

from plan_dock import PlanDock
from plan_util import *

class Plan(QObject):

    # Project settings
    settings = None # Settings()

    # Internal variables
    initialised = False
    siteCode = ''
    context = 0
    source = '0'
    comment = ''

    layers = None  # LayerManager

    levelsMapTool = None
    currentMapTool = None

    def __init__(self, settings, layers):
        super(Plan, self).__init__()
        self.settings = settings
        # If the project gets changed, make sure we update too
        self.settings.projectChanged.connect(self.loadProject)
        # If the map tool changes make sure we stay updated
        self.settings.iface.mapCanvas().mapToolSet.connect(self.mapToolChanged)
        self.layers = layers

    # Load the module when plugin is loaded
    def load(self):
        self.dock = PlanDock()
        self.dock.load(self.settings.iface, Qt.RightDockWidgetArea, self.settings.createMenuAction(self.tr(u'Draw Archaeological Plans'), ':/plugins/Ark/plan/draw-freehand.png', True))
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

    # Unload the module when plugin is unloaded
    def unload(self):

        self.deleteMapTool()

        # Unload the dock
        self.dock.unload()

    def run(self, checked):
        if checked:
            self.initialise()

    def initialise(self):
        if self.initialised:
            return

        self.settings.initialise()
        if (not self.settings.isConfigured()):
            return
        self.layers.initialise()

        self.initialiseBuffers()
        self.initialised = True

    def initialiseBuffers(self):
        self.layers.contexts.createBuffers()
        self.dock.setSchematicsBuffer(self.layers.contexts.schemaBuffer)
        self.dock.setPolygonsBuffer(self.layers.contexts.polygonsBuffer)
        self.dock.setLinesBuffer(self.layers.contexts.linesBuffer)
        self.dock.setSchematicsLayer(self.layers.contexts.schemaLayer)
        self.dock.setPolygonsLayer(self.layers.contexts.polygonsLayer)
        self.dock.setLinesLayer(self.layers.contexts.linesLayer)

    def loadProject(self):
        if not self.initialised:
            return
        self.initialised = False

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
        georefDialog = GeorefDialog(rawFile, self.settings.planDir(), self.settings.separatePlanFolders(), self.settings.projectCrs().authid(), self.settings.gridPointsLayerName(), self.settings.gridPointsFieldX, self.settings.gridPointsFieldY)
        if (georefDialog.exec_()):
            md = georefDialog.metadata()
            self.setMetadata(md[0], md[1], md[2], md[3], md[4], md[5])
            self.layers.loadGeoLayer(georefDialog.geoRefFile())

    # Layer Methods

    def mergeBuffers(self):
        if self.layers.contexts.okToMergeBuffers():
            self.layers.contexts.mergeBuffers('Merge context ' + str(self.context))

    def clearBuffers(self):
        self.layers.contexts.clearBuffers('Clear buffer data ' + str(self.context))

    def enableLevelsMode(self, typeAttribute):
        #TODO disable all snapping
        self.createMapTool(typeAttribute, self.layers.contexts.pointsBuffer, QgsMapToolAddFeature.Point, False, self.tr('Add level'))
        self.currentMapTool.setAttributeQuery('elevation', QVariant.Double, 0.0, 'Add Level', 'Please enter the elevation in meters (m):', -100, 100, 2)
        self.settings.iface.mapCanvas().setMapTool(self.currentMapTool)

    def enableLineSegmentMode(self, typeAttribute):
        #TODO configure snapping
        self.createMapTool(typeAttribute, self.layers.contexts.linesBuffer, QgsMapToolAddFeature.Segment, True, self.tr('Add line segment feature'))
        self.settings.iface.mapCanvas().setMapTool(self.currentMapTool)

    def enableLineMode(self, typeAttribute):
        #TODO configure snapping
        self.createMapTool(typeAttribute, self.layers.contexts.linesBuffer, QgsMapToolAddFeature.Line, True, self.tr('Add line feature'))
        self.settings.iface.mapCanvas().setMapTool(self.currentMapTool)

    def enablePolygonMode(self, typeAttribute):
        #TODO configure snapping
        self.createMapTool(typeAttribute, self.layers.contexts.polygonsBuffer, QgsMapToolAddFeature.Polygon, True, self.tr('Add polygon feature'))
        self.settings.iface.mapCanvas().setMapTool(self.currentMapTool)

    def enableSchematicMode(self, typeAttribute):
        #TODO configure snapping
        self.createMapTool(typeAttribute, self.layers.contexts.schemaBuffer, QgsMapToolAddFeature.Polygon, True, self.tr('Add schematic feature'))
        self.settings.iface.mapCanvas().setMapTool(self.currentMapTool)

    def createMapTool(self, typeAttribute, layer, featureType, snappingEnabled, toolName):
        #TODO configure snapping
        self.settings.iface.mapCanvas().setCurrentLayer(layer)
        self.settings.iface.legendInterface().setCurrentLayer(layer)
        self.deleteMapTool()
        self.currentMapTool = QgsMapToolAddFeature(self.settings.iface.mapCanvas(), self.settings.iface, featureType, toolName)
        self.currentMapTool.setDefaultAttributes({0 : self.context, 1 : self.source, 2 : typeAttribute, 3 : self.comment})
        if snappingEnabled:
            self.currentMapTool.setSnappingEnabled(True)
            self.currentMapTool.setShowSnappableVertices(True)

    def mapToolChanged(self, newMapTool):
        if (newMapTool != self.currentMapTool):
            self.dock.clearCheckedToolButton()
            self.deleteMapTool()

    def deleteMapTool(self):
        if self.currentMapTool is not None:
            self.settings.iface.mapCanvas().unsetMapTool(self.currentMapTool)
            del self.currentMapTool
            self.currentMapTool = None
