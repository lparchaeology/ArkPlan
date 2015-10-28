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
from ..libarkqgis import utils

from ..project import Project
from ..georef.georef_dialog import GeorefDialog

from plan_dock import PlanDock
from edit_dock import EditDock
from schematic_dock import SchematicDock, SearchStatus
from ..filter.filter import FilterType
from plan_util import *
from metadata import Metadata

class Plan(QObject):

    # Project settings
    project = None # Project()

    # Internal variables
    initialised = False
    _buffersInitialised = False
    module = None
    contextNumber = None
    featureId = None
    featureName = None
    category = ''

    actions = {}
    mapTools = {}
    currentMapTool = None

    _schematicContextIncludeFilter = -1
    _schematicContextHighlightFilter = -1
    _schematicSourceIncludeFilter = -1
    _schematicSourceHighlightFilter = -1

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

        self.dock.loadRawFileSelected.connect(self._loadRawPlan)
        self.dock.loadGeoFileSelected.connect(self._loadGeoPlan)
        self.dock.loadContextSelected.connect(self._loadContextPlans)
        self.dock.loadPlanSelected.connect(self._loadPlans)
        self.metadata().metadataChanged.connect(self.updateDefaultAttributes)
        self.dock.contextNumberChanged.connect(self._setContextNumber)
        self.dock.featureIdChanged.connect(self._setFeatureId)
        self.dock.featureNameChanged.connect(self._setFeatureName)

        self.dock.clearSelected.connect(self.clearBuffers)
        self.dock.mergeSelected.connect(self.mergeBuffers)

        self.editDock = EditDock(self.project.plugin.iface)
        action = self.project.addAction(':/plugins/ArkPlan/plan/document-edit.png', self.tr(u'Editing Tools'), checkable=True)
        self.editDock.load(self.project.plugin.iface, Qt.RightDockWidgetArea, action)
        self.editDock.toggled.connect(self.runEdit)

        self.schematicDock = SchematicDock()
        action = self.project.addAction(':/plugins/ArkPlan/plan/task-delegate.png', self.tr(u'Check Context Schematics'), checkable=True)
        self.schematicDock.load(self.project.plugin.iface, Qt.RightDockWidgetArea, action)
        self.schematicDock.toggled.connect(self.runSchematic)
        self.schematicDock.findContextSelected.connect(self._findContext)
        self.schematicDock.findSourceSelected.connect(self._findSource)
        self.schematicDock.copySourceSelected.connect(self._copySource)
        self.schematicDock.cloneSourceSelected.connect(self._cloneSource)
        self.metadata().metadataChanged.connect(self.updateDefaultAttributes)
        self.schematicDock.clearSelected.connect(self.clearBuffers)
        self.schematicDock.mergeSelected.connect(self.mergeBuffers)

    # Unload the module when plugin is unloaded
    def unload(self):

        for action in self.actions.values():
            if action.isChecked():
                action.setChecked(False)

        # Unload the dock
        self.schematicDock.unload()
        self.editDock.unload()
        self.dock.unload()

    def run(self, checked):
        if checked:
            self.initialise()

    def runEdit(self, checked):
        if checked:
            self.project.initialise()
            if (not self.project.isInitialised()):
                return
            self.initialiseBuffers()

    def runSchematic(self, checked):
        if checked:
            self.initialise()

    def initialise(self):
        if self.initialised:
            return

        self.project.initialise()
        if (not self.project.isInitialised()):
            return

        self.initialiseBuffers()
        self.dock.init(self.project)
        self.schematicDock.init(self.project)

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
        self.addDrawingTool('plan', 'cxt', 'tim', self.tr('Timber'), QIcon(), ArkMapToolAddFeature.Polygon)
        self.addDrawingTool('plan', 'cxt', 'clk', self.tr('Chalk'), QIcon(), ArkMapToolAddFeature.Polygon)
        self.dock.newDrawingToolRow('plan')
        self.addLevelTool('plan', 'cxt', 'lvl', self.tr('Level'), QIcon())
        self.addSchemaTool('plan', 'cxt', 'sch', self.tr('Schema'), QIcon())

        self.addDrawingTool('plan', 'sec', 'sec', self.tr('Section Pin'), QIcon(), ArkMapToolAddFeature.Point)
        self.addDrawingTool('plan', 'sec', 'sln', self.tr('Section Line'), QIcon(), ArkMapToolAddFeature.Line)
        self.addDrawingTool('plan', 'rgf', 'spf', self.tr('Special Find'), QIcon(), ArkMapToolAddFeature.Point)
        self.addDrawingTool('plan', 'smp', 'spl', self.tr('Sample'), QIcon(), ArkMapToolAddFeature.Point)

        self.initialised = True

    def initialiseBuffers(self):
        if self._buffersInitialised:
            return
        self.project.plan.createBuffers()
        self._buffersInitialised = True
        self.editDock.setBufferPoints(self.project.plan.pointsBuffer)
        self.editDock.setBufferLines(self.project.plan.linesBuffer)
        self.editDock.setBufferPolygons(self.project.plan.polygonsBuffer)
        self.editDock.setPlanPoints(self.project.plan.pointsLayer)
        self.editDock.setPlanLines(self.project.plan.linesLayer)
        self.editDock.setPlanPolygons(self.project.plan.polygonsLayer)
        self.editDock.setBasePoints(self.project.base.pointsLayer)
        self.editDock.setBaseLines(self.project.base.linesLayer)
        self.editDock.setBasePolygons(self.project.base.polygonsLayer)

    def loadProject(self):
        if not self.initialised:
            return
        self.initialised = False

    def metadata(self):
        return self.dock.metadata()

    # Plan Tools

    def _setPlanMetadata(self, pmd):
        self.metadata().setSiteCode(pmd.siteCode)
        self.metadata().setSourceCode('drw')
        self.metadata().setSourceClass(pmd.sourceClass)
        self.metadata().setSourceId(pmd.sourceId)
        self.metadata().setSourceFile(pmd.filename)
        if pmd.sourceClass == 'cxt':
            self.setContextNumber(pmd.sourceId)
            self.setFeatureId(0)
        else:
            self.setContextNumber(0)
            self.setFeatureId(pmd.sourceId)

    def _loadRawPlan(self):
        fileName = unicode(QFileDialog.getOpenFileName(None, self.tr('Load Raw Drawing'), self.project.rawPlanPath(),
                                                       self.tr('Image Files (*.png *.tif *.tiff)')))
        if fileName:
            self.georeferencePlan(QFileInfo(fileName))

    def _loadGeoPlan(self):
        fileName = unicode(QFileDialog.getOpenFileName(None, self.tr('Load Georeferenced Drawing'), self.project.processedPlanPath(),
                                                       self.tr('GeoTiff Files (*.tif *.tiff)')))
        if fileName:
            geoFile = QFileInfo(fileName)
            self._setPlanMetadata(Metadata(geoFile))
            self.project.loadGeoLayer(geoFile)
        self._setSourceCode('drw')
        self._setSourceId(self.contextNumber)

    def _loadContextPlans(self):
        context, ok = QInputDialog.getInt(None, 'Load Context Plans', 'Please enter the Context number to load all drawings for:', 1, 1, 99999)
        if (not ok or context <= 0):
            return
        self.loadContextPlans(context)

    def loadContextPlans(self, context):
        planDir = self.project.processedPlanDir()
        planDir.setFilter(QDir.Files | QDir.NoDotAndDotDot)
        geoName = 'cxt_' + self.project.siteCode() + '_' + str(context) + '_*r.tif'
        planDir.setNameFilters([geoName])
        plans = planDir.entryInfoList()
        for plan in plans:
            self._setPlanMetadata(PlanMetadata(plan))
            self.project.loadGeoLayer(plan)

    def _loadPlans(self):
        plan, ok = QInputDialog.getInt(None, 'Load Plans', 'Please enter the Plan number to load all drawings for:', 1, 1, 99999)
        if (not ok or plan <= 0):
            return
        self.loadPlans(plan)

    def loadPlans(self, plan):
        planDir = self.project.processedPlanDir()
        planDir.setFilter(QDir.Files | QDir.NoDotAndDotDot)
        geoName = 'pln_' + self.project.siteCode() + '_' + str(plan) + '_*r.tif'
        planDir.setNameFilters([geoName])
        plans = planDir.entryInfoList()
        for plan in plans:
            self._setPlanMetadata(PlanMetadata(plan))
            self.project.loadGeoLayer(plan)

    def setContextNumber(self, context):
        self.dock.setContextNumber(context)

    def _setContextNumber(self, context):
        if context is None or context <= 0:
            self.contextNumber = None
        else:
            self.contextNumber = context
        self.updateDefaultAttributes()

    def setFeatureId(self, featureId):
        self.dock.setFeatureId(featureId)

    def _setFeatureId(self, featureId):
        if featureId is None or featureId <= 0:
            self.featureId = None
        else:
            self.featureId = featureId
        self.updateDefaultAttributes()

    def setFeatureName(self, featureName):
        self.dock.setFeatureName(featureName)

    def _setFeatureName(self, featureName):
        if featureName is None or featureName.strip() == '':
            self.featureName = None
        else:
            self.featureName = featureName
        self.updateDefaultAttributes()

    # Georeference Tools

    def georeferencePlan(self, rawFile):
        georefDialog = GeorefDialog(rawFile, self.project.planRasterDir(), self.project.separateProcessedPlanFolder(), self.project.plugin.projectCrs().authid(), self.project.pointsLayerName('grid'), self.project.fieldName('local_x'), self.project.fieldName('local_y'))
        if (georefDialog.exec_()):
            geoFile = georefDialog.geoRefFile()
            md = georefDialog.metadata()
            md.filename = geoFile.fileName()
            self._setPlanMetadata(md)
            self.project.loadGeoLayer(geoFile)

    # Layer Methods

    def mergeBuffers(self):
        self.project.plan.updateBufferAttribute(self.project.fieldName('created_on'), utils.timestamp())
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
        if classCode == 'cxt':
            action.triggered.connect(self.validateContext)
        else:
            action.triggered.connect(self.validateFeature)
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
        md = self.metadata()
        defaults = {}
        defaults[layer.fieldNameIndex(self.project.fieldName('site'))] = self._string(md.siteCode())
        defaults[layer.fieldNameIndex(self.project.fieldName('class'))] = self._string(data['class'])
        id = ''
        if data['class'] == 'cxt':
            id = self.contextNumber
        else:
            id = self.featureId
        defaults[layer.fieldNameIndex(self.project.fieldName('id'))] = self._number(id)
        defaults[layer.fieldNameIndex(self.project.fieldName('name'))] = self._string(self.featureName)
        defaults[layer.fieldNameIndex(self.project.fieldName('source_cd'))] = self._string(md.sourceCode())
        if md.sourceCode() != 'svy':
            defaults[layer.fieldNameIndex(self.project.fieldName('source_cl'))] = self._string(md.sourceClass())
            defaults[layer.fieldNameIndex(self.project.fieldName('source_id'))] = self._number(md.sourceId())
        defaults[layer.fieldNameIndex(self.project.fieldName('file'))] = self._string(md.sourceFile())
        defaults[layer.fieldNameIndex(self.project.fieldName('category'))] = self._string(data['category'])
        defaults[layer.fieldNameIndex(self.project.fieldName('comment'))] = self._string(md.comment())
        defaults[layer.fieldNameIndex(self.project.fieldName('created_by'))] = self._string(md.createdBy())
        mapTool.setDefaultAttributes(defaults)

    def _string(self, value):
        if value is None or value.strip() == '':
            return None
        else:
            return value

    def _number(self, value):
        if value is None or value <= 0:
            return None
        else:
            return value

    def validateContext(self):
        if self.contextNumber <= 0:
            num, ok = QInputDialog.getInt(None, 'Context Number', 'Please enter a valid Context Number', 1, 1, 99999)
            if ok:
                self.setContextNumber(num)
                if self.metadata().sourceClass() == 'cxt' and self.metadata().sourceId() <= 0:
                    self.metadata().setSourceId(num)
        self.metadata().validate()

    def validateFeature(self):
        if self.featureId <= 0:
            num, ok = QInputDialog.getInt(None, 'Feature ID', 'Please enter a valid Feature ID', 1, 1, 99999)
            if ok:
                self.setFeatureId(num)
        self.metadata().validate()

    # SchematicDock methods

    def _clearSchematicFilters(self):
        self.project.plugin.filterModule.removeFilter(self._schematicContextIncludeFilter)
        self._schematicContextIncludeFilter = -1
        self.project.plugin.filterModule.removeFilter(self._schematicContextHighlightFilter)
        self._schematicContextHighlightFilter = -1
        self._clearSchematicSourceFilters()

    def _clearSchematicSourceFilters(self):
        self.project.plugin.filterModule.removeFilter(self._schematicSourceIncludeFilter)
        self._schematicSourceIncludeFilter = -1
        self.project.plugin.filterModule.removeFilter(self._schematicSourceHighlightFilter)
        self._schematicSourceHighlightFilter = -1

    def _findContext(self):
        self._clearSchematicFilters()

        filterModule = self.project.plugin.filterModule
        if filterModule.hasFilterType(FilterType.IncludeFilter) or filterModule.hasFilterType(FilterType.IncludeFilter):
            self._schematicContextFilter = filterModule.addFilter(FilterType.IncludeFilter, 'cxt', str(self.schematicDock.context()))
        self._schematicContextHighlightFilter = filterModule.addFilter(FilterType.HighlightFilter, 'cxt', str(self.schematicDock.context()))

        classExpr = '"' + self.project.fieldName('class') + '" = \'' + 'cxt' + '\''
        idExpr = '"' + self.project.fieldName('id') + '" = \'' + str(self.schematicDock.context()) + '\''
        schmExpr = '"' + self.project.fieldName('category') + '" = \'sch\''

        request = QgsFeatureRequest()
        request.setFilterExpression(classExpr + ' and ' + idExpr)
        haveFeature = SearchStatus.Found
        try:
            self.project.plan.linesLayer.getFeatures(request).next()
        except StopIteration:
            haveFeature = SearchStatus.NotFound

        request.setFilterExpression(classExpr + ' and ' + idExpr + ' and ' + schmExpr)
        haveSchematic = SearchStatus.Found
        try:
            self.project.plan.polygonsLayer.getFeatures(request).next()
        except StopIteration:
            haveSchematic = SearchStatus.NotFound

        self.schematicDock.setContext(self.schematicDock.context(), haveFeature, haveSchematic)

    def _findSource(self):
        self._clearSchematicSourceFilters()

        filterModule = self.project.plugin.filterModule
        if filterModule.hasFilterType(FilterType.IncludeFilter) or filterModule.hasFilterType(FilterType.IncludeFilter):
            self._schematicContextFilter = filterModule.addFilter(FilterType.IncludeFilter, 'cxt', str(self.schematicDock.sourceContext()))
        self._schematicContextHighlightFilter = filterModule.addFilter(FilterType.HighlightFilter, 'cxt', str(self.schematicDock.sourceContext()))

        classExpr = '"' + self.project.fieldName('class') + '" = \'' + 'cxt' + '\''
        idExpr = '"' + self.project.fieldName('id') + '" = \'' + str(self.schematicDock.sourceContext()) + '\''
        schmExpr = '"' + self.project.fieldName('category') + '" = \'sch\''

        request = QgsFeatureRequest()
        request.setFilterExpression(classExpr + ' and ' + idExpr)
        haveFeature = SearchStatus.Found
        try:
            self.project.plan.linesLayer.getFeatures(request).next()
        except StopIteration:
            haveFeature = SearchStatus.NotFound

        request.setFilterExpression(classExpr + ' and ' + idExpr + ' and ' + schmExpr)
        haveSchematic = SearchStatus.Found
        try:
            self.project.plan.polygonsLayer.getFeatures(request).next()
        except StopIteration:
            haveSchematic = SearchStatus.NotFound

        self.schematicDock.setSourceContext(self.schematicDock.sourceContext(), haveFeature, haveSchematic)

    def _copySource(self):
        return

    def _cloneSource(self):
        return
