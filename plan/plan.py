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
from PyQt4.QtCore import Qt, QVariant, QFileInfo, QObject, QDir
from PyQt4.QtGui import QAction, QIcon, QFileDialog, QInputDialog

from qgis.core import *

from ..arklib.map_tools import *

from ..core.project import Project
from ..georef.georef_dialog import GeorefDialog

from plan_dock import PlanDock
from plan_util import *

class Plan(QObject):

    # Project settings
    project = None # Project()

    # Internal variables
    initialised = False
    module = ''
    siteCode = ''
    contextNumber = 0
    baseNumber = 0
    category = ''
    source = '0'
    sourceFile = ''
    comment = ''
    createdBy = ''

    levelsMapTool = None
    currentMapTool = None

    def __init__(self, project):
        super(Plan, self).__init__()
        self.project = project
        # If the project gets changed, make sure we update too
        self.project.projectChanged.connect(self.loadProject)
        # If the map tool changes make sure we stay updated
        self.project.iface.mapCanvas().mapToolSet.connect(self.mapToolChanged)

    # Load the module when plugin is loaded
    def load(self):
        self.dock = PlanDock()
        self.dock.load(self.project.iface, Qt.RightDockWidgetArea, self.project.createMenuAction(self.tr(u'Draw Archaeological Plans'), ':/plugins/Ark/plan/draw-freehand.png', True))
        self.dock.toggled.connect(self.run)

        self.dock.loadRawFileSelected.connect(self.loadRawPlan)
        self.dock.loadGeoFileSelected.connect(self.loadGeoPlan)
        self.dock.loadContextSelected.connect(self.loadContextPlans)
        self.dock.siteChanged.connect(self.setSite)
        self.dock.siteChanged.connect(self.updateDefaultAttributes)
        self.dock.contextNumberChanged.connect(self.setContextNumber)
        self.dock.contextNumberChanged.connect(self.updateDefaultAttributes)
        self.dock.baseNumberChanged.connect(self.setBaseNumber)
        self.dock.baseNumberChanged.connect(self.updateDefaultAttributes)
        self.dock.sourceChanged.connect(self.setSource)
        self.dock.sourceChanged.connect(self.updateDefaultAttributes)
        self.dock.sourceFileChanged.connect(self.setSourceFile)
        self.dock.sourceFileChanged.connect(self.updateDefaultAttributes)
        self.dock.commentChanged.connect(self.setComment)
        self.dock.commentChanged.connect(self.updateDefaultAttributes)
        self.dock.createdByChanged.connect(self.setCreatedBy)
        self.dock.createdByChanged.connect(self.updateDefaultAttributes)

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

        self.project.initialise()
        if (not self.project.isInitialised()):
            return

        self.dock.setSite(self.project.siteCode())
        self.initialiseBuffers()
        self.initialised = True

    def initialiseBuffers(self):
        self.project.contexts.createBuffers()
        self.project.base.createBuffers()
        self.dock.setSchematicsBuffer(self.project.contexts.schemaBuffer)
        self.dock.setPolygonsBuffer(self.project.contexts.polygonsBuffer)
        self.dock.setLinesBuffer(self.project.contexts.linesBuffer)
        self.dock.setSchematicsLayer(self.project.contexts.schemaLayer)
        self.dock.setPolygonsLayer(self.project.contexts.polygonsLayer)
        self.dock.setLinesLayer(self.project.contexts.linesLayer)

    def loadProject(self):
        if not self.initialised:
            return
        self.initialised = False

    # Plan Tools

    def setMetadata(self, siteCode, type, number, file, easting, northing, suffix):
        self.dock.setSite(siteCode)
        self.dock.setContextNumber(number)
        self.dock.setSource(str(number))
        self.dock.setSourceFile(file)

    def loadRawPlan(self):
        fileName = unicode(QFileDialog.getOpenFileName(None, self.tr('Load Raw Plan'), self.project.rawPlanPath(),
                                                       self.tr('Image Files (*.png *.tif *.tiff)')))
        if fileName:
            self.georeferencePlan(QFileInfo(fileName))

    def loadGeoPlan(self):
        fileName = unicode(QFileDialog.getOpenFileName(None, self.tr('Load Georeferenced Plan'), self.project.processedPlanPath(),
                                                       self.tr('GeoTiff Files (*.tif *.tiff)')))
        if fileName:
            geoFile = QFileInfo(fileName)
            md = planMetadata(geoFile.completeBaseName())
            self.setMetadata(md[0], md[1], md[2], geoFile.completeBaseName(), md[3], md[4], md[5])
            self.project.loadGeoLayer(geoFile)

    def loadContextPlans(self):
        context, ok = QInputDialog.getInt(None, 'Load Context Plans', 'Please enter the Context number to load all plans for:', 0, 0, 99999)
        if (not ok or context == 0):
            return
        planDir = self.project.processedPlanDir()
        planDir.setFilter(QDir.Files | QDir.NoDotAndDotDot)
        geoName = self.project.siteCode() + '*' + str(context) + '*_r.tif'
        planDir.setNameFilters([geoName])
        plans = planDir.entryInfoList()
        for plan in plans:
            md = planMetadata(plan.completeBaseName())
            self.setMetadata(md[0], md[1], md[2], plan.completeBaseName(), md[3], md[4], md[5])
            self.project.loadGeoLayer(plan)

    def setSite(self, siteCode):
        self.siteCode = siteCode

    def setContextNumber(self, context):
        self.contextNumber = context

    def setBaseNumber(self, number):
        self.baseNumber = number

    def setSource(self, source):
        self.source = source

    def setSourceFile(self, sourceFile):
        self.sourceFile = sourceFile

    def setComment(self, comment):
        self.comment = comment

    def setCreatedBy(self, creator):
        self.createdBy = creator

    # Georeference Tools

    def georeferencePlan(self, rawFile):
        georefDialog = GeorefDialog(rawFile, self.project.planDir(), self.project.separatePlanFolders(), self.project.projectCrs().authid(), self.project.pointsLayerName('grid'), self.project.fieldName('local_x'), self.project.fieldName('local_y'))
        if (georefDialog.exec_()):
            geoFile = georefDialog.geoRefFile()
            md = georefDialog.metadata()
            self.setMetadata(md[0], md[1], md[2], geoFile.completeBaseName(), md[3], md[4], md[5])
            self.project.loadGeoLayer(geoFile)

    # Layer Methods

    def mergeBuffers(self):
        if self.project.contexts.okToMergeBuffers():
            self.project.contexts.mergeBuffers('Merge context data ' + str(self.contextNumber))
        if self.project.base.okToMergeBuffers():
            self.project.base.mergeBuffers('Merge base data ' + str(self.baseNumber))

    def clearBuffers(self):
        self.project.contexts.clearBuffers('Clear contexts buffer data ' + str(self.contextNumber))
        self.project.base.clearBuffers('Clear base buffer data ' + str(self.baseNumber))

    def enableLevelsMode(self, module, category):
        mapTool = ArkMapToolAddFeature(self.project.iface, self.project.collection(module).pointsBuffer, ArkMapToolAddFeature.Point, self.tr('Add level'))
        mapTool.setAttributeQuery('elevation', QVariant.Double, 0.0, 'Add Level', 'Please enter the elevation in meters (m):', -1000, 1000, 2)
        self.enableMapTool(module, category, mapTool, True)
        #TODO configure snapping

    def enableLineSegmentMode(self, module, category):
        mapTool = ArkMapToolAddFeature(self.project.iface, self.project.collection(module).linesBuffer, ArkMapToolAddFeature.Segment, self.tr('Add line segment'))
        self.enableMapTool(module, category, mapTool, True)
        #TODO configure snapping

    def enableLineMode(self, module, category):
        mapTool = ArkMapToolAddFeature(self.project.iface, self.project.collection(module).linesBuffer, ArkMapToolAddFeature.Line, self.tr('Add line'))
        self.enableMapTool(module, category, mapTool, True)
        #TODO configure snapping

    def enablePolygonMode(self, module, category):
        mapTool = ArkMapToolAddFeature(self.project.iface, self.project.collection(module).polygonsBuffer, ArkMapToolAddFeature.Polygon, self.tr('Add polygon'))
        self.enableMapTool(module, category, mapTool, True)
        #TODO configure snapping

    def enableSchematicMode(self, module, category):
        mapTool = ArkMapToolAddFeature(self.project.iface, self.project.collection(module).schemaBuffer, ArkMapToolAddFeature.Polygon, self.tr('Add schema'))
        self.enableMapTool(module, category, mapTool, True)
        #TODO configure snapping

    def enableSectionMode(self, module, category):
        mapTool = ArkMapToolAddBaseline(self.project.iface, self.project.collection(module).linesBuffer, ArkMapToolAddFeature.Line, self.tr('Add section'))
        mapTool.setAttributeQuery('id', QVariant.String, '', 'Section ID', 'Please enter the Section ID (e.g. S45):')
        mapTool.setPointQuery('elevation', QVariant.Double, 0.0, 'Add Level', 'Please enter the pin or string height in meters (m):', -100, 100, 2)
        self.enableMapTool(module, category, mapTool, True)
        #TODO configure snapping

    def enableMapTool(self, module, category, mapTool, snappingEnabled):
        self.deleteMapTool()
        self.module = module
        self.category = category
        self.currentMapTool = mapTool
        self.updateDefaultAttributes()
        self.currentMapTool.setPanningEnabled(True)
        self.currentMapTool.setZoomingEnabled(True)
        if snappingEnabled:
            self.currentMapTool.setSnappingEnabled(True)
            self.currentMapTool.setShowSnappableVertices(True)
        self.project.iface.mapCanvas().setMapTool(self.currentMapTool)
        self.project.iface.mapCanvas().setCurrentLayer(self.currentMapTool.layer())
        self.project.iface.legendInterface().setCurrentLayer(self.currentMapTool.layer())

    def mapToolChanged(self, newMapTool):
        if (newMapTool != self.currentMapTool):
            self.deleteMapTool()

    def deleteMapTool(self):
        if self.currentMapTool is not None:
            self.project.iface.mapCanvas().unsetMapTool(self.currentMapTool)
            del self.currentMapTool
            self.currentMapTool = None
            self.category = ''

    def updateDefaultAttributes(self):
        if self.currentMapTool is not None:
            layer = self.currentMapTool.layer()
            if (layer is None or not layer.isValid()):
                return
            defaults = {}
            defaults[layer.fieldNameIndex(self.project.fieldName('site'))] = self.siteCode
            if self.module == 'contexts':
                defaults[layer.fieldNameIndex(self.project.fieldName('context'))] = self.contextNumber
            elif self.module == 'base':
                bid = ''
                if (self.category == 'sec' or self.category == 'sln'):
                    bid = 'S' + str(self.baseNumber)
                elif (self.category == 'bpt' or self.category == 'bln'):
                    bid = 'B' + str(self.baseNumber)
                defaults[layer.fieldNameIndex(self.project.fieldName('id'))] = bid
            defaults[layer.fieldNameIndex(self.project.fieldName('source'))] = self.source
            defaults[layer.fieldNameIndex(self.project.fieldName('file'))] = self.sourceFile
            defaults[layer.fieldNameIndex(self.project.fieldName('category'))] = self.category
            defaults[layer.fieldNameIndex(self.project.fieldName('comment'))] = self.comment
            defaults[layer.fieldNameIndex(self.project.fieldName('created_by'))] = self.createdBy
            self.currentMapTool.setDefaultAttributes(defaults)
