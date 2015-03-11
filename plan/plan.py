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
        self.layers = layers

    def initGui(self):
        self.dock = PlanDock()
        self.dock.load(self.settings, Qt.RightDockWidgetArea, self.tr(u'Draw Archaeological Plans'), ':/plugins/Ark/plan/draw-freehand.png')
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

        if (not self.settings.isConfigured()):
            self.settings.configure()
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
        georefDialog = GeorefDialog(rawFile, self.settings.planDir(), self.settings.separatePlanFolders(), self.settings.projectCrs(), self.settings.gridPointsLayerName(), self.settings.gridPointsFieldX, self.settings.gridPointsFieldY)
        if (georefDialog.exec_()):
            md = georefDialog.metadata()
            self.setMetadata(md[0], md[1], md[2], md[3], md[4], md[5])
            self.layers.loadGeoLayer(georefDialog.geoRefFile())

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
        self.currentMapTool.setShowSnappableVertices(True)
        self.settings.iface.mapCanvas().setMapTool(self.currentMapTool)

    def mapToolChanged(self, newMapTool):
        if (newMapTool != self.currentMapTool):
            self.dock.clearCheckedToolButton()
            self.deleteMapTool()

    def deleteMapTool(self):
        if self.currentMapTool is not None:
            self.currentMapTool.deactivate()
            del self.currentMapTool
            self.currentMapTool = None
