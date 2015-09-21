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

from ..libarkqgis.map_tools import *

from ..project import Project
from ..georef.georef_dialog import GeorefDialog

from plan_dock import PlanDock
from plan_util import *

class Plan(QObject):

    # Project settings
    project = None # Project()

    # Internal variables
    initialised = False
    module = None
    siteCode = None
    classCode = None
    contextNumber = None
    featureId = None
    featureName = None
    category = ''
    sourceCode = None
    sourceId = None
    sourceFile = None
    comment = None
    createdBy = None

    actions = {}
    mapTools = {}
    currentMapTool = None

    def __init__(self, project):
        super(Plan, self).__init__()
        self.project = project
        # If the project gets changed, make sure we update too
        self.project.projectChanged.connect(self.loadProject)

    # Load the module when plugin is loaded
    def load(self):
        self.dock = PlanDock()
        action = self.project.addAction(':/plugins/ArkPlan/plan/draw-freehand.png', self.tr(u'Draw Archaeological Plans'), checkable=True)
        self.dock.load(self.project.plugin.iface, Qt.RightDockWidgetArea, action)
        self.dock.toggled.connect(self.run)

        self.dock.loadRawFileSelected.connect(self.loadRawPlan)
        self.dock.loadGeoFileSelected.connect(self.loadGeoPlan)
        self.dock.loadContextSelected.connect(self.loadContextPlans)
        self.dock.siteChanged.connect(self.setSite)
        self.dock.siteChanged.connect(self.updateDefaultAttributes)
        self.dock.contextNumberChanged.connect(self.setContextNumber)
        self.dock.contextNumberChanged.connect(self.updateDefaultAttributes)
        self.dock.featureIdChanged.connect(self.setFeatureId)
        self.dock.featureIdChanged.connect(self.updateDefaultAttributes)
        self.dock.featureNameChanged.connect(self.setFeatureName)
        self.dock.featureNameChanged.connect(self.updateDefaultAttributes)
        self.dock.sourceCodeChanged.connect(self.setSourceCode)
        self.dock.sourceCodeChanged.connect(self.updateDefaultAttributes)
        self.dock.sourceIdChanged.connect(self.setSourceId)
        self.dock.sourceIdChanged.connect(self.updateDefaultAttributes)
        self.dock.sourceFileChanged.connect(self.setSourceFile)
        self.dock.sourceFileChanged.connect(self.updateDefaultAttributes)
        self.dock.commentChanged.connect(self.setComment)
        self.dock.commentChanged.connect(self.updateDefaultAttributes)
        self.dock.createdByChanged.connect(self.setCreatedBy)
        self.dock.createdByChanged.connect(self.updateDefaultAttributes)

        self.dock.clearSelected.connect(self.clearBuffers)
        self.dock.mergeSelected.connect(self.mergeBuffers)

    # Unload the module when plugin is unloaded
    def unload(self):

        for action in self.actions.values():
            if action.isChecked():
                action.setChecked(False)

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

        self.dock.addSourceCode('Plan', 'pln')
        self.dock.addSourceCode('Cloned', 'cln')
        self.dock.addSourceCode('Modified', 'mod')
        self.dock.addSourceCode('Inferred', 'inf')
        self.dock.addSourceCode('Survey', 'svy')

        self.addDrawingTool('plan', 'cxt', 'ext', self.tr('Extent'), QIcon(), ArkMapToolAddFeature.Line)
        self.addDrawingTool('plan', 'cxt', 'veg', self.tr('Vertical Edge'), QIcon(), ArkMapToolAddFeature.Line)
        self.addDrawingTool('plan', 'cxt', 'ueg', self.tr('Uncertain Edge'), QIcon(), ArkMapToolAddFeature.Line)
        self.addDrawingTool('plan', 'cxt', 'loe', self.tr('Limit of Excavation'), QIcon(), ArkMapToolAddFeature.Line)
        self.addDrawingTool('plan', 'cxt', 'trn', self.tr('Truncation'), QIcon(), ArkMapToolAddFeature.Line)
        self.addDrawingTool('plan', 'cxt', 'vtr', self.tr('Vertical Truncation'), QIcon(), ArkMapToolAddFeature.Line)
        self.dock.newDrawingToolRow('plan')
        self.addDrawingTool('plan', 'cxt', 'bos', self.tr('Break of Slope'), QIcon(), ArkMapToolAddFeature.Line)
        self.addDrawingTool('plan', 'cxt', 'hch', self.tr('Hachure'), QIcon(), ArkMapToolAddFeature.Segment)
        self.addDrawingTool('plan', 'cxt', 'unc', self.tr('Undercut'), QIcon(), ArkMapToolAddFeature.Segment)
        self.addDrawingTool('plan', 'cxt', 'ros', self.tr('Return of Slope'), QIcon(), ArkMapToolAddFeature.Segment)
        self.dock.newDrawingToolRow('plan')
        self.addDrawingTool('plan', 'cxt', 'cbm', self.tr('CBM'), QIcon(), ArkMapToolAddFeature.Polygon)
        self.addDrawingTool('plan', 'cxt', 'brk', self.tr('Brick'), QIcon(), ArkMapToolAddFeature.Polygon)
        self.addDrawingTool('plan', 'cxt', 'til', self.tr('Tile'), QIcon(), ArkMapToolAddFeature.Polygon)
        self.addDrawingTool('plan', 'cxt', 'pot', self.tr('Pot'), QIcon(), ArkMapToolAddFeature.Polygon)
        self.addDrawingTool('plan', 'cxt', 'sto', self.tr('Stone'), QIcon(), ArkMapToolAddFeature.Polygon)
        self.addDrawingTool('plan', 'cxt', 'fli', self.tr('Flint'), QIcon(), ArkMapToolAddFeature.Polygon)
        self.addDrawingTool('plan', 'cxt', 'cha', self.tr('Charcol'), QIcon(), ArkMapToolAddFeature.Polygon)
        self.dock.newDrawingToolRow('plan')
        self.addLevelTool('plan', 'cxt', 'lvl', self.tr('Level'), QIcon())
        self.addSchemaTool('plan', 'cxt', 'sch', self.tr('Schema'), QIcon())

        self.addDrawingTool('plan', 'sec', 'sec', self.tr('Section Pin'), QIcon(), ArkMapToolAddFeature.Point)
        self.addDrawingTool('plan', 'sec', 'sln', self.tr('Section Line'), QIcon(), ArkMapToolAddFeature.Line)
        self.addDrawingTool('plan', 'rgf', 'spf', self.tr('Special Find'), QIcon(), ArkMapToolAddFeature.Point)
        self.addDrawingTool('plan', 'smp', 'spl', self.tr('Sample'), QIcon(), ArkMapToolAddFeature.Point)

        self.initialised = True

    def initialiseBuffers(self):
        self.project.plan.createBuffers()
        self.dock.setPolygonsBuffer(self.project.plan.polygonsBuffer)
        self.dock.setLinesBuffer(self.project.plan.linesBuffer)
        self.dock.setPolygonsLayer(self.project.plan.polygonsLayer)
        self.dock.setLinesLayer(self.project.plan.linesLayer)

    def loadProject(self):
        if not self.initialised:
            return
        self.initialised = False

    # Plan Tools

    def setMetadata(self, siteCode, type, number, file, easting, northing, suffix):
        self.dock.setSite(siteCode)
        self.dock.setContextNumber(number)
        self.dock.setSourceCode('pln')
        self.dock.setSourceId(number)
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
            self.setMetadata(md[0], md[1], md[2], geoFile.fileName(), md[3], md[4], md[5])
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
            self.setMetadata(md[0], md[1], md[2], plan.fileName(), md[3], md[4], md[5])
            self.project.loadGeoLayer(plan)

    def setSite(self, siteCode):
        if siteCode is None or siteCode.strip() == '':
            self.siteCode = None
        else:
            self.siteCode = siteCode

    def setContextNumber(self, context):
        if context is None or context <= 0:
            self.contextNumber = None
        else:
            self.contextNumber = context

    def setFeatureId(self, featureId):
        if featureId is None or featureId <= 0:
            self.featureId = None
        else:
            self.featureId = featureId

    def setFeatureName(self, featureName):
        if featureName is None or featureName.strip() == '':
            self.featureName = None
        else:
            self.featureName = featureName

    def setSourceCode(self, sourceCode):
        if sourceCode is None or sourceCode.strip() == '':
            self.sourceCode = None
        else:
            self.sourceCode = sourceCode

    def setSourceId(self, sourceId):
        if sourceId is None or sourceId <= 0:
            self.sourceId = None
        else:
            self.sourceId = sourceId

    def setSourceFile(self, sourceFile):
        if sourceFile is None or sourceFile.strip() == '':
            self.sourceFile = None
        else:
            self.sourceFile = sourceFile

    def setComment(self, comment):
        if comment is None or comment.strip() == '':
            self.comment = None
        else:
            self.comment = comment

    def setCreatedBy(self, creator):
        if creator is None or creator.strip() == '':
            self.createdBy = None
        else:
            self.createdBy = creator

    # Georeference Tools

    def georeferencePlan(self, rawFile):
        georefDialog = GeorefDialog(rawFile, self.project.planRasterDir(), self.project.separateProcessedPlanFolder(), self.project.plugin.projectCrs().authid(), self.project.pointsLayerName('grid'), self.project.fieldName('local_x'), self.project.fieldName('local_y'))
        if (georefDialog.exec_()):
            geoFile = georefDialog.geoRefFile()
            md = georefDialog.metadata()
            self.setMetadata(md[0], md[1], md[2], geoFile.fileName(), md[3], md[4], md[5])
            self.project.loadGeoLayer(geoFile)

    # Layer Methods

    def mergeBuffers(self):
        if self.project.plan.okToMergeBuffers():
            self.project.plan.mergeBuffers('Merge plan data')

    def clearBuffers(self):
        self.project.plan.clearBuffers('Clear plan buffer data')

    # Drawing tools

    def _newMapToolAction(self, module, classCode, category, name, icon):
        data = {}
        data['module'] = module
        data['class'] = classCode
        data['category'] = category
        data['name'] = name
        action = QAction(icon, category, self.dock)
        action.setData(data)
        action.setToolTip(name)
        action.setCheckable(True)
        return action

    def _newMapTool(self, name, featureType, buffer, action):
        mapTool = ArkMapToolAddFeature(self.project.plugin.iface, buffer, featureType, name)
        mapTool.setAction(action)
        mapTool.setPanningEnabled(True)
        mapTool.setZoomingEnabled(True)
        mapTool.setSnappingEnabled(True)
        mapTool.setShowSnappableVertices(True)
        mapTool.activated.connect(self.updateDefaultAttributes)
        return mapTool

    def _addMapTool(self, classCode, category, mapTool, action):
        self.dock.addDrawingTool(classCode, action)
        self.actions[category] = action
        self.mapTools[category] = mapTool

    def addDrawingTool(self, module, classCode, category, name, icon, featureType):
        action = self._newMapToolAction(module, classCode, category, name, icon)
        layer = None
        if (featureType == ArkMapToolAddFeature.Line or featureType == ArkMapToolAddFeature.Segment):
            layer = self.project.collection(module).linesBuffer
        elif featureType == ArkMapToolAddFeature.Polygon:
            layer = self.project.collection(module).polygonsBuffer
        else:
            layer = self.project.collection(module).pointsBuffer
        mapTool = self._newMapTool(name, featureType, layer, action)
        self._addMapTool(classCode, category, mapTool, action)

    def addLevelTool(self, module, classCode, category, name, icon):
        action = self._newMapToolAction(module, classCode, category, name, icon)
        mapTool = self._newMapTool(name, ArkMapToolAddFeature.Point, self.project.collection(module).pointsBuffer, action)
        mapTool.setAttributeQuery('elevation', QVariant.Double, 0.0, 'Add Level', 'Please enter the elevation in meters (m):', -1000, 1000, 2)
        self._addMapTool(classCode, category, mapTool, action)

    def addSchemaTool(self, module, classCode, category, name, icon):
        action = self._newMapToolAction(module, classCode, category, name, icon)
        mapTool = self._newMapTool(name, ArkMapToolAddFeature.Polygon, self.project.collection(module).polygonsBuffer, action)
        self._addMapTool(classCode, category, mapTool, action)

    def addSectionTool(self, module, classCode, category, name, icon):
        action = self._newMapToolAction(module, classCode, category, name, icon)
        mapTool = ArkMapToolAddBaseline(self.project.plugin.iface, self.project.collection(module).linesBuffer, ArkMapToolAddFeature.Line, self.tr('Add section'))
        mapTool.setAttributeQuery('id', QVariant.String, '', 'Section ID', 'Please enter the Section ID (e.g. S45):')
        mapTool.setPointQuery('elevation', QVariant.Double, 0.0, 'Add Level', 'Please enter the pin or string height in meters (m):', -100, 100, 2)
        self._addMapTool(classCode, category, mapTool, action)

    def updateDefaultAttributes(self):
        for mapTool in self.mapTools.values():
            if mapTool.action().isChecked():
                self.setDefaultAttributes(mapTool.action().data(), mapTool)

    def setDefaultAttributes(self, data, mapTool):
        if mapTool is None:
            return
        layer = mapTool.layer()
        if (layer is None or not layer.isValid()):
            return
        defaults = {}
        defaults[layer.fieldNameIndex(self.project.fieldName('site'))] = self.siteCode
        defaults[layer.fieldNameIndex(self.project.fieldName('class'))] = data['class']
        id = ''
        if data['class'] == 'cxt':
            id = self.contextNumber
        else:
            id = self.featureId
        defaults[layer.fieldNameIndex(self.project.fieldName('id'))] = id
        defaults[layer.fieldNameIndex(self.project.fieldName('name'))] = self.featureName
        defaults[layer.fieldNameIndex(self.project.fieldName('source_cd'))] = self.sourceCode
        defaults[layer.fieldNameIndex(self.project.fieldName('source_id'))] = self.sourceId
        defaults[layer.fieldNameIndex(self.project.fieldName('file'))] = self.sourceFile
        defaults[layer.fieldNameIndex(self.project.fieldName('category'))] = data['category']
        defaults[layer.fieldNameIndex(self.project.fieldName('comment'))] = self.comment
        defaults[layer.fieldNameIndex(self.project.fieldName('created_by'))] = self.createdBy
        mapTool.setDefaultAttributes(defaults)
