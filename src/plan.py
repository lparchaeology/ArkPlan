# -*- coding: utf-8 -*-
"""
/***************************************************************************
                                ARK Spatial
                    A QGIS plugin for Archaeological Recording.
        Part of the Archaeological Recording Kit by L-P : Archaeology
                        http://ark.lparchaeology.com
                              -------------------
        begin                : 2014-12-07
        git sha              : $Format:%H$
        copyright            : 2014, 2015 by L-P : Heritage LLP
        email                : ark@lparchaeology.com
        copyright            : 2014, 2015 by John Layt
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
from ..libarkqgis import utils, layers, processing

from ..georef.georef_dialog import GeorefDialog

from plan_dock import PlanDock
from edit_dock import EditDock
from schematic_dock import SchematicDock, SearchStatus
from select_drawing_dialog import SelectDrawingDialog

from filter import FilterType, FilterAction
from plan_util import *
from config import Config
from metadata import Metadata, FeatureData

import resources_rc

def _quote(string):
    return "'" + string + "'"

def _doublequote(string):
    return '"' + string + '"'

class Plan(QObject):

    # Project settings
    project = None # Project()

    dock = None # PlanDock()
    editDock = None # EditDock()
    schematicDock = None # SchematicDock()

    # Internal variables
    initialised = False
    _buffersInitialised = False

    _featureData = FeatureData()

    actions = {}
    mapTools = {}
    currentMapTool = None

    _definitiveCategories = set()
    _schematicContextIncludeFilter = -1
    _schematicContextHighlightFilter = -1
    _schematicSourceIncludeFilter = -1
    _schematicSourceHighlightFilter = -1

    def __init__(self, project):
        super(Plan, self).__init__(self.project)
        self.project = project

    # Create the gui when the plugin is first created
    def initGui(self):
        self.dock = PlanDock(self.project.layerDock)
        action = self.project.addDockAction(':/plugins/ark/plan/drawPlans.png', self.tr(u'Draw Archaeological Plans'), checkable=True)
        self.dock.initGui(self.project.iface, Qt.RightDockWidgetArea, action)
        self.dock.toggled.connect(self.run)

        self.dock.loadRawFileSelected.connect(self._loadRawPlan)
        self.dock.loadGeoFileSelected.connect(self._loadGeoPlan)
        self.dock.loadContextSelected.connect(self._loadContextPlans)
        self.dock.loadPlanSelected.connect(self._loadPlans)
        self.dock.contextNumberChanged.connect(self._featureIdChanged)
        self.dock.featureIdChanged.connect(self._featureIdChanged)
        self.dock.featureNameChanged.connect(self._featureNameChanged)
        self.dock.autoSchematicSelected.connect(self._autoSchematicSelected)
        self.dock.editPointsSelected.connect(self._editPointsLayer)
        self.dock.editLinesSelected.connect(self._editLinesLayer)
        self.dock.editPolygonsSelected.connect(self._editPolygonsLayer)

        self.dock.clearSelected.connect(self.clearBuffers)
        self.dock.mergeSelected.connect(self.mergeBuffers)

        self.schematicDock = SchematicDock(self.project.layerDock)
        action = self.project.addDockAction(':/plugins/ark/plan/checkSchematic.png', self.tr(u'Check Context Schematics'), checkable=True)
        self.schematicDock.initGui(self.project.iface, Qt.RightDockWidgetArea, action)
        self.schematicDock.toggled.connect(self.runSchematic)
        self.schematicDock.findContextSelected.connect(self._findPanContext)
        self.schematicDock.zoomContextSelected.connect(self._findZoomContext)
        self.schematicDock.editContextSelected.connect(self._editSchematicContext)
        self.schematicDock.findSourceSelected.connect(self._findPanSource)
        self.schematicDock.zoomSourceSelected.connect(self._findZoomSource)
        self.schematicDock.copySourceSelected.connect(self._editSourceSchematic)
        self.schematicDock.cloneSourceSelected.connect(self._cloneSourceSchematic)
        self.schematicDock.editSourceSelected.connect(self._editSource)
        self.schematicDock.autoSchematicSelected.connect(self._autoSchematicSelected)
        self.schematicDock.editLinesSelected.connect(self._editLinesLayer)
        self.schematicDock.editPolygonsSelected.connect(self._editPolygonsLayer)
        self.schematicDock.resetSelected.connect(self._resetSchematic)
        self.schematicDock.clearSelected.connect(self.clearBuffers)
        self.schematicDock.mergeSelected.connect(self.mergeBuffers)
        self.project.filterModule.filterSetCleared.connect(self._resetSchematic)

        self.editDock = EditDock(self.project.iface, self.project.layerDock)
        action = self.project.addDockAction(':/plugins/ark/plan/editingTools.png', self.tr(u'Editing Tools'), checkable=True)
        self.editDock.initGui(self.project.iface, Qt.RightDockWidgetArea, action)
        self.editDock.toggled.connect(self.runEdit)

        self.metadata().metadataChanged.connect(self.updateMapToolAttributes)

    # Load the project settings when project is loaded
    def loadProject(self):
        self.initialiseBuffers()
        self.dock.initSourceCodes(Config.planSourceCodes)
        self.dock.initSourceClasses(Config.planSourceClasses)
        for category in Config.featureCategories:
            #TODO Select by map tool type enum
            if category[2] == 'lvl' or category[2] == 'llv':
                self.addLevelTool(category[0], category[1], category[2], category[3], QIcon(category[4]))
            else:
                self.addDrawingTool(category[0], category[1], category[2], category[3], QIcon(category[4]), category[5])
            if category[6] == True:
                self._definitiveCategories.add(category[2])

        self.schematicDock.initSourceCodes(Config.planSourceCodes)
        self.schematicDock.initSourceClasses(Config.planSourceClasses)
        self.schematicDock.setContext(0, SearchStatus.Unknown, SearchStatus.Unknown)
        self.schematicDock.addDrawingTool('sch', self.actions['sch'])
        self.schematicDock.addDrawingTool('lvl', self.actions['lvl'])

        self.initialised = True

    # Save the project
    def writeProject(self):
        pass

    # Close the project
    def closeProject(self):
        self._clearSchematicFilters()
        self.writeProject()
        self.initialised = False

    # Unload the module when plugin is unloaded
    def unloadGui(self):

        self.closeProject()

        for action in self.actions.values():
            if action.isChecked():
                action.setChecked(False)

        # Reset the initialisation
        self.initialised = False
        self._buffersInitialised = False

        # Unload the docks
        self.schematicDock.unloadGui()
        self.editDock.unloadGui()
        self.dock.unloadGui()

    def run(self, checked):
        if checked and self.initialised:
            self.schematicDock.menuAction().setChecked(False)
            self.editDock.menuAction().setChecked(False)
        else:
            self.dock.menuAction().setChecked(False)

    def runEdit(self, checked):
        if checked and self.initialised:
            self.schematicDock.menuAction().setChecked(False)
            self.dock.menuAction().setChecked(False)
        else:
            self.editDock.menuAction().setChecked(False)

    def runSchematic(self, checked):
        if checked and self.initialised:
            self.dock.menuAction().setChecked(False)
            self.editDock.menuAction().setChecked(False)
        else:
            self.schematicDock.menuAction().setChecked(False)

    def initialiseBuffers(self):
        if self._buffersInitialised:
            return
        self.project.plan.createBuffers()
        self.project.plan.pointsBuffer.setFeatureFormSuppress(QgsVectorLayer.SuppressOn)
        self.project.plan.linesBuffer.setFeatureFormSuppress(QgsVectorLayer.SuppressOn)
        self.project.plan.polygonsBuffer.setFeatureFormSuppress(QgsVectorLayer.SuppressOn)
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

    def metadata(self):
        if self.schematicDock.menuAction().isChecked():
            return self.schematicDock.metadata()
        return self.dock.metadata()

    # Plan Tools

    def _setPlanMetadata(self, pmd):
        self.metadata().setSiteCode(pmd.siteCode)
        self.metadata().setSourceCode('drw')
        self.metadata().setSourceClass(pmd.sourceClass)
        self.metadata().setSourceId(pmd.sourceId)
        self.metadata().setSourceFile(pmd.filename)
        if pmd.sourceClass == 'cxt':
            self.dock.setContextNumber(pmd.sourceId)
            self.dock.setFeatureId(0)
        else:
            self.dock.setContextNumber(0)
            self.dock.setFeatureId(pmd.sourceId)

    def _loadRawPlan(self):
        dialog = SelectDrawingDialog(self.project, 'cxt', self.project.siteCode())
        if (dialog.exec_()):
            for filePath in dialog.selectedFiles():
                self.georeferencePlan(QFileInfo(filePath))

    def _loadGeoPlan(self):
        dialog = SelectDrawingDialog(self.project, 'cxt', self.project.siteCode(), True)
        if (dialog.exec_()):
            for filePath in dialog.selectedFiles():
                geoFile = QFileInfo(filePath)
                self._setPlanMetadata(PlanMetadata(geoFile))
                self.project.loadGeoLayer(geoFile)

    def _loadContextPlans(self):
        context, ok = QInputDialog.getInt(None, 'Load Context Plans', 'Please enter the Context number to load all drawings for:', 1, 1, 99999)
        if (ok and context > 0):
            self.loadDrawing('cxt', self.project.siteCode(), context)

    def _loadPlans(self):
        plan, ok = QInputDialog.getInt(None, 'Load Plans', 'Please enter the Plan number to load all drawings for:', 1, 1, 99999)
        if (ok and plan > 0):
            self.loadDrawing('pln', self.project.siteCode(), plan)

    def loadDrawing(self, drawingType, siteCode, drawingId):
        drawingDir = self.project.georefDrawingDir(drawingType)
        drawingDir.setFilter(QDir.Files | QDir.NoDotAndDotDot)
        name = drawingType + '_' + siteCode + '_' + str(drawingId)
        nameList = []
        nameList.append(name + '.png')
        nameList.append(name + '.tif')
        nameList.append(name + '.tiff')
        nameList.append(name + '_*.png')
        nameList.append(name + '_*.tif')
        nameList.append(name + '_*.tiff')
        drawingDir.setNameFilters(nameList)
        drawings = drawingDir.entryInfoList()
        for drawing in drawings:
            self._setPlanMetadata(PlanMetadata(drawing))
            self.project.loadGeoLayer(drawing)

    def _featureIdChanged(self, featureId):
        self._featureData.setFeatureId(featureId)
        self.updateMapToolAttributes()

    def _featureNameChanged(self, featureName):
        if featureName is None or featureName.strip() == '':
            self._featureData.setFeatureName('')
        else:
            self._featureData.setFeatureName(featureName)
        self.updateMapToolAttributes()

    # Georeference Tools

    def georeferencePlan(self, rawFile):
        pmd = PlanMetadata(rawFile)
        georefDialog = GeorefDialog(rawFile, self.project.georefDrawingDir(pmd.sourceClass), self.project.projectCrs().authid(), self.project.pointsLayerName('grid'), self.project.fieldName('local_x'), self.project.fieldName('local_y'))
        if (georefDialog.exec_()):
            geoFile = georefDialog.geoRefFile()
            md = georefDialog.metadata()
            md.filename = geoFile.fileName()
            self._setPlanMetadata(md)
            self.project.loadGeoLayer(geoFile)

    # Layer Methods

    def mergeBuffers(self):
        self.project.plan.updateBufferAttribute(self.project.fieldName('created_on'), utils.timestamp())
        if self.project.plan.isEditable():
            self.project.plan.mergeBuffers('Merge plan data')

    def clearBuffers(self):
        self.project.plan.clearBuffers('Clear plan buffer data')

    # Drawing tools

    def _newMapToolAction(self, classCode, category, toolName, icon):
        data = {}
        data['class'] = classCode
        data['category'] = category
        action = QAction(icon, category, self.dock)
        action.setData(data)
        action.setToolTip(toolName)
        action.setCheckable(True)
        return action

    def _newMapTool(self, toolName, featureType, buffer, action):
        mapTool = ArkMapToolAddFeature(self.project.iface, buffer, featureType, toolName)
        mapTool.setAction(action)
        mapTool.setPanningEnabled(True)
        mapTool.setZoomingEnabled(True)
        mapTool.setSnappingEnabled(True)
        mapTool.setShowSnappableVertices(True)
        mapTool.activated.connect(self.mapToolActivated)
        return mapTool

    def _addMapTool(self, classCode, category, mapTool, action):
        action.triggered.connect(self.validateFeature)
        self.dock.addDrawingTool(classCode, action)
        self.actions[category] = action
        self.mapTools[category] = mapTool

    def addDrawingTool(self, collection, classCode, category, toolName, icon, featureType):
        action = self._newMapToolAction(classCode, category, toolName, icon)
        layer = None
        if (featureType == FeatureType.Line or featureType == FeatureType.Segment):
            layer = self.project.collection(collection).linesBuffer
        elif featureType == FeatureType.Polygon:
            layer = self.project.collection(collection).polygonsBuffer
        else:
            layer = self.project.collection(collection).pointsBuffer
        mapTool = self._newMapTool(toolName, featureType, layer, action)
        self._addMapTool(classCode, category, mapTool, action)

    def addLevelTool(self, collection, classCode, category, toolName, icon):
        action = self._newMapToolAction(classCode, category, toolName, icon)
        mapTool = self._newMapTool(toolName, FeatureType.Point, self.project.collection(collection).pointsBuffer, action)
        mapTool.setAttributeQuery('elevation', QVariant.Double, 0.0, 'Add Level', 'Please enter the elevation in meters (m):', -1000, 1000, 2)
        self._addMapTool(classCode, category, mapTool, action)

    def addSectionTool(self, collection, classCode, category, toolName, icon):
        action = self._newMapToolAction(classCode, category, toolName, icon)
        mapTool = ArkMapToolAddBaseline(self.project.iface, self.project.collection(collection).linesBuffer, FeatureType.Line, self.tr('Add section'))
        mapTool.setAttributeQuery('id', QVariant.String, '', 'Section ID', 'Please enter the Section ID (e.g. S45):')
        mapTool.setPointQuery('elevation', QVariant.Double, 0.0, 'Add Level', 'Please enter the pin or string height in meters (m):', -100, 100, 2)
        self._addMapTool(classCode, category, mapTool, action)

    def mapToolActivated(self):
        for mapTool in self.mapTools.values():
            if mapTool.action().isChecked():
                if not mapTool.layer().isEditable():
                    mapTool.layer().startEditing()
                self.setMapToolAttributes(mapTool)

    def updateMapToolAttributes(self):
        for mapTool in self.mapTools.values():
            if mapTool.action().isChecked():
                self.setMapToolAttributes(mapTool)

    def setMapToolAttributes(self, mapTool):
        if mapTool is None:
            return
        toolData = mapTool.action().data()
        self._featureData.setClassCode(toolData['class'])
        self._featureData.setCategory(toolData['category'])
        attrs = self.featureAttributes(self.metadata(), self._featureData, mapTool.layer())
        mapTool.setDefaultAttributes(attrs)

    def featureAttributes(self, md, fd, layer):
        if (layer is None or not layer.isValid()):
            return
        defaults = {}
        defaults[layer.fieldNameIndex(self.project.fieldName('site'))] = md.siteCode(True)
        defaults[layer.fieldNameIndex(self.project.fieldName('class'))] = fd.classCode(True)
        defaults[layer.fieldNameIndex(self.project.fieldName('id'))] = fd.featureId(True)
        defaults[layer.fieldNameIndex(self.project.fieldName('name'))] = fd.name(True)
        defaults[layer.fieldNameIndex(self.project.fieldName('source_cd'))] = md.sourceCode(True)
        if md.sourceCode() != 'svy':
            defaults[layer.fieldNameIndex(self.project.fieldName('source_cl'))] = md.sourceClass(True)
            defaults[layer.fieldNameIndex(self.project.fieldName('source_id'))] = md.sourceId(True)
        defaults[layer.fieldNameIndex(self.project.fieldName('file'))] = md.sourceFile(True)
        defaults[layer.fieldNameIndex(self.project.fieldName('category'))] = fd.category(True)
        defaults[layer.fieldNameIndex(self.project.fieldName('comment'))] = md.comment(True)
        defaults[layer.fieldNameIndex(self.project.fieldName('created_by'))] = md.createdBy(True)
        return defaults

    def validateFeature(self):
        self._featureData.validate()
        if self._featureData.classCode() == 'cxt':
            self.dock.setContextNumber(self._featureData.featureId())
            self.dock.setFeatureId(0)
        else:
            self.dock.setContextNumber(0)
            self.dock.setFeatureId(self._featureData.featureId())
        self.dock.setFeatureName(self._featureData.name())
        if self.metadata().sourceClass() == self._featureData.classCode() and self.metadata().sourceId() <= 0:
            self.metadata().setSourceId(self._featureData.featureId())
        self.metadata().validate()

    def _autoSchematicSelected(self, sourceId):
        self.actions['sch'].trigger()
        self._autoSchematic(sourceId, self._featureData, self.metadata(), self.project.plan.linesBuffer, self.project.plan.polygonsBuffer)

    def _autoSchematic(self, sourceId, fd, md, inLayer, outLayer):
        definitiveFeatures = []
        if inLayer.selectedFeatureCount() > 0:
            definitiveFeatures = inLayer.selectedFeatures()
        else:
            featureIter = inLayer.getFeatures()
            for feature in featureIter:
                if feature.attribute(self.project.fieldName('id')) == sourceId and feature.attribute(self.project.fieldName('category')) in self._definitiveCategories:
                    definitiveFeatures.append(feature)
        schematicFeatures = processing.polygonizeFeatures(definitiveFeatures, outLayer.pendingFields())
        if len(schematicFeatures) <= 0:
            return
        schematic = processing.dissolveFeatures(schematicFeatures, outLayer.pendingFields())
        attrs = self.featureAttributes(md, fd, outLayer)
        for attr in attrs.keys():
            schematic.setAttribute(attr, attrs[attr])
        outLayer.beginEditCommand("Add Auto Schematic")
        outLayer.addFeature(schematic)
        outLayer.endEditCommand()
        self.project.mapCanvas().refresh()

    def _editPointsLayer(self):
        self.project.iface.setActiveLayer(self.project.plan.pointsBuffer)
        self.project.iface.actionNodeTool().trigger()

    def _editLinesLayer(self):
        self.project.iface.setActiveLayer(self.project.plan.linesBuffer)
        self.project.iface.actionNodeTool().trigger()

    def _editPolygonsLayer(self):
        self.project.iface.setActiveLayer(self.project.plan.polygonsBuffer)
        self.project.iface.actionNodeTool().trigger()

    def _confirmDelete(self, itemId, title='Confirm Delete Item'):
        label = 'This action ***DELETES*** item ' + str(itemId) + ' from the saved data.\n\nPlease enter the item ID to confirm.'
        confirm, ok = QInputDialog.getText(None, title, label, text='')
        return ok and confirm == str(itemId)

    def editInBuffers(self, siteCode, classCode, itemId):
        if self._confirmDelete(itemId, 'Confirm Move Item'):
            self._editInBuffers(siteCode, classCode, itemId)

    def _editInBuffers(self, siteCode, classCode, itemId):
        request = self._itemRequest(siteCode, classCode, itemId)
        self.project.plan.moveFeatureRequestToBuffers(request)
        if classCode == 'cxt':
            self.dock.setContextNumber(int(itemId))
            self.dock.setFeatureId(0)
        else:
            self.dock.setContextNumber(0)
            self.dock.setFeatureId(itemId)
        self.metadata().setSiteCode(siteCode)
        self.metadata().setComment('')
        self.metadata().setSourceCode('drw')
        self.metadata().setSourceClass(classCode)
        self.metadata().setSourceId(itemId)
        self.metadata().setSourceFile('')

    def deleteItem(self, siteCode, classCode, itemId):
        if self._confirmDelete(itemId, 'Confirm Delete Item'):
            request = self._itemRequest(siteCode, classCode, itemId)
            self.project.plan.deleteFeatureRequest(request)

    def panToItem(self, siteCode, classCode, itemId):
        extent = self.itemExtent(siteCode, classCode, itemId)
        if extent == None or extent.isNull() or extent.isEmpty():
            return
        self.project.mapCanvas().setCenter(extent.center())
        self.project.mapCanvas().refresh()

    def zoomToItem(self, siteCode, classCode, itemId):
        extent = self.itemExtent(siteCode, classCode, itemId)
        if extent == None or extent.isNull() or extent.isEmpty():
            return
        extent.scale(1.05)
        self.project.mapCanvas().setExtent(extent)
        self.project.mapCanvas().refresh()

    def itemExtent(self, siteCode, classCode, itemId):
        request = self._itemRequest(siteCode, classCode, itemId)
        points = self._requestAsLayer(request, self.project.plan.pointsLayer, 'points')
        lines = self._requestAsLayer(request, self.project.plan.linesLayer, 'lines')
        polygons = self._requestAsLayer(request, self.project.plan.polygonsLayer, 'polygons')
        extent = None
        extent = self._combineExtentWith(extent, polygons)
        extent = self._combineExtentWith(extent, lines)
        extent = self._combineExtentWith(extent, points)
        return extent

    def _requestAsLayer(self, request, fromLayer, toName):
        toLayer = layers.cloneAsMemoryLayer(fromLayer, toName)
        layers.copyFeatureRequest(request, fromLayer, toLayer)
        toLayer.updateExtents()
        return toLayer

    def _combineExtentWith(self, extent, layer):
        if (layer is not None and layer.isValid() and layer.featureCount() > 0):
            layerExtent = layer.extent()
            if layerExtent.isNull() or layerExtent.isEmpty():
                return extent
            if extent == None:
                extent = layerExtent
            else:
                extent.combineExtentWith(layerExtent)
        return extent

    # Feature Request Methods

    def _eqClause(self, field, value):
        return _doublequote(self.project.fieldName(field)) + ' = ' + _quote(str(value))

    def _siteClause(self, siteCode):
        return self._eqClause('site', siteCode)

    def _classClause(self, classCode):
        return self._eqClause('class', classCode)

    def _idClause(self, itemId):
        return self._eqClause('id', itemId)

    def _categoryClause(self, category):
        return self._eqClause('category', category)
        return _doublequote(self.project.fieldName('category')) + ' = ' + _quote(category)

    def _itemExpr(self, siteCode, classCode, itemId):
        return self._siteClause(siteCode) + ' and ' + self._classClause(classCode) + ' and ' + self._idClause(itemId)

    def _featureRequest(self, expr):
        request = QgsFeatureRequest()
        request.setFilterExpression(expr)
        return request

    def _itemRequest(self, siteCode, classCode, itemId):
        expr = self._itemExpr(siteCode, classCode, itemId)
        return self._featureRequest(expr)

    def _categoryRequest(self, siteCode, classCode, itemId, category):
        return self._featureRequest(self._itemExpr(siteCode, classCode, itemId) + ' and ' + self._categoryClause(category))

    # SchematicDock methods

    def _resetSchematic(self):
        self._clearSchematicFilters()
        self.schematicDock.setContext(0, SearchStatus.Unknown, SearchStatus.Unknown)

    def _clearSchematicFilters(self):
        self._clearSchematicContextIncludeFilter()
        self._clearSchematicContextHighlightFilter()
        self._clearSchematicSourceFilters()

    def _clearSchematicContextIncludeFilter(self):
        self.project.filterModule.removeFilter(self._schematicContextIncludeFilter)
        self._schematicContextIncludeFilter = -1

    def _clearSchematicContextHighlightFilter(self):
        self.project.filterModule.removeFilter(self._schematicContextHighlightFilter)
        self._schematicContextHighlightFilter = -1

    def _clearSchematicSourceFilters(self):
        self.project.filterModule.removeFilter(self._schematicSourceIncludeFilter)
        self._schematicSourceIncludeFilter = -1
        self.project.filterModule.removeFilter(self._schematicSourceHighlightFilter)
        self._schematicSourceHighlightFilter = -1

    def _findPanContext(self):
        if self.schematicDock.contextStatus() == SearchStatus.Unknown:
            self._findContext()
        if self.schematicDock.contextStatus() == SearchStatus.Found:
            self.panToItem(self.schematicDock.metadata().siteCode(), 'cxt', self.schematicDock.context())

    def _findZoomContext(self):
        if self.schematicDock.contextStatus() == SearchStatus.Unknown:
            self._findContext()
        if self.schematicDock.contextStatus() == SearchStatus.Found:
            self.zoomToItem(self.schematicDock.metadata().siteCode(), 'cxt', self.schematicDock.context())

    def _editSchematicContext(self):
        self.editInBuffers(self.schematicDock.metadata().siteCode(), 'cxt', self.schematicDock.context())

    def _findContext(self):
        self._clearSchematicFilters()

        filterModule = self.project.filterModule
        siteCode = self.schematicDock.metadata().siteCode()
        if siteCode == '':
            siteCode = self.project.siteCode()
        if filterModule.hasFilterType(FilterType.IncludeFilter) or filterModule.hasFilterType(FilterType.IncludeFilter):
            self._schematicContextFilter = filterModule.addFilter(FilterType.IncludeFilter, siteCode, 'cxt', str(self.schematicDock.context()), FilterAction.LockFilter)
        self._schematicContextHighlightFilter = filterModule.addFilter(FilterType.HighlightFilter, siteCode, 'cxt', str(self.schematicDock.context()), FilterAction.LockFilter)

        itemRequest = self._itemRequest(siteCode, 'cxt', self.schematicDock.context())
        haveFeature = SearchStatus.Found
        try:
            feature = self.project.plan.linesLayer.getFeatures(itemRequest).next()
            self._copyFeatureMetadata(feature)
        except StopIteration:
            haveFeature = SearchStatus.NotFound

        schRequest = self._categoryRequest(siteCode, 'cxt', self.schematicDock.context(), 'sch')
        haveSchematic = SearchStatus.Found
        try:
            self.project.plan.polygonsLayer.getFeatures(schRequest).next()
        except StopIteration:
            haveSchematic = SearchStatus.NotFound

        self.schematicDock.setContext(self.schematicDock.context(), haveFeature, haveSchematic)
        self._featureIdChanged(self.schematicDock.context())

    def _findPanSource(self):
        if self.schematicDock.sourceStatus() == SearchStatus.Unknown:
            self._findSource()
        if self.schematicDock.sourceStatus() == SearchStatus.Found:
            self.panToItem(self.schematicDock.metadata().siteCode(), 'cxt', self.schematicDock.sourceContext())

    def _findZoomSource(self):
        if self.schematicDock.sourceStatus() == SearchStatus.Unknown:
            self._findSource()
        if self.schematicDock.sourceStatus() == SearchStatus.Found:
            self.zoomToItem(self.schematicDock.metadata().siteCode(), 'cxt', self.schematicDock.sourceContext())

    def _editSource(self):
        self.editInBuffers(self.schematicDock.metadata().siteCode(), 'cxt', self.schematicDock.sourceContext())

    def _findSource(self):
        self._clearSchematicSourceFilters()

        filterModule = self.project.filterModule
        siteCode = self.schematicDock.metadata().siteCode()
        if siteCode == '':
            siteCode = self.project.siteCode()
        if filterModule.hasFilterType(FilterType.IncludeFilter) or filterModule.hasFilterType(FilterType.IncludeFilter):
            self._schematicSourceIncludeFilter = filterModule.addFilter(FilterType.IncludeFilter, siteCode, 'cxt', str(self.schematicDock.sourceContext()), FilterAction.LockFilter)
        self._clearSchematicContextHighlightFilter()
        self._schematicSourceHighlightFilter = filterModule.addFilter(FilterType.HighlightFilter, siteCode, 'cxt', str(self.schematicDock.sourceContext()), FilterAction.LockFilter)

        itemRequest = self._itemRequest(siteCode, 'cxt', self.schematicDock.sourceContext())
        haveFeature = SearchStatus.Found
        try:
            self.project.plan.linesLayer.getFeatures(itemRequest).next()
        except StopIteration:
            haveFeature = SearchStatus.NotFound

        schRequest = self._categoryRequest(siteCode, 'cxt', self.schematicDock.sourceContext(), 'sch')
        haveSchematic = SearchStatus.Found
        try:
            feature = self.project.plan.polygonsLayer.getFeatures(schRequest).next()
            self._copyFeatureMetadata(feature)
        except StopIteration:
            haveSchematic = SearchStatus.NotFound

        self.schematicDock.setSourceContext(self.schematicDock.sourceContext(), haveFeature, haveSchematic)

    def _attribute(self, feature, fieldName):
        val = feature.attribute(self.project.fieldName(fieldName))
        if val == NULL:
            return None
        else:
            return val

    def _copyFeatureMetadata(self, feature):
        self.schematicDock.metadata().setSiteCode(self._attribute(feature, 'site'))
        #TODO FIXME WTF???
        self.schematicDock.metadataWidget._setSiteCode(self.schematicDock.metadata().siteCode())
        self.schematicDock.metadata().setComment(self._attribute(feature, 'comment'))
        self.schematicDock.metadata().setSourceCode('cln')
        self.schematicDock.metadata().setSourceClass('cxt')
        self.schematicDock.metadata().setSourceId(self.schematicDock.sourceContext())
        self.schematicDock.metadata().setSourceFile('')

    def _copySourceSchematic(self):
        request = self._categoryRequest(self.schematicDock.metadata().siteCode(), 'cxt', self.schematicDock.sourceContext(), 'sch')
        fi = self.project.plan.polygonsLayer.getFeatures(request)
        for feature in fi:
            md = self.schematicDock.metadata()
            feature.setAttribute(self.project.fieldName('site'), md.siteCode(True))
            feature.setAttribute(self.project.fieldName('class'), 'cxt')
            feature.setAttribute(self.project.fieldName('id'), self.schematicDock.context())
            feature.setAttribute(self.project.fieldName('name'), None)
            feature.setAttribute(self.project.fieldName('category'), 'sch')
            feature.setAttribute(self.project.fieldName('source_cd'), md.sourceCode(True))
            feature.setAttribute(self.project.fieldName('source_cl'), md.sourceClass(True))
            feature.setAttribute(self.project.fieldName('source_id'), md.sourceId(True))
            feature.setAttribute(self.project.fieldName('file'), md.sourceFile(True))
            feature.setAttribute(self.project.fieldName('comment'), md.comment(True))
            feature.setAttribute(self.project.fieldName('created_by'), md.createdBy(True))
            feature.setAttribute(self.project.fieldName('created_on'), None)
            self.project.plan.polygonsBuffer.addFeature(feature)

    def _editSourceSchematic(self):
        self._clearSchematicSourceFilters()
        self._copySourceSchematic()
        self.project.iface.setActiveLayer(self.project.plan.polygonsBuffer)
        self.project.iface.actionZoomToLayer().trigger()
        self.project.plan.polygonsBuffer.selectAll()
        self.project.iface.actionNodeTool().trigger()

    def _cloneSourceSchematic(self):
        self._clearSchematicSourceFilters()
        self._copySourceSchematic()
        self.mergeBuffers()
