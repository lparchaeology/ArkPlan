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
from ..libarkqgis import utils, layers, geometry

from ..georef.georef_dialog import GeorefDialog

from plan_dock import PlanDock
from edit_dock import EditDock
from schematic_dock import SchematicDock, SearchStatus
from select_drawing_dialog import SelectDrawingDialog

from filter import FilterType, FilterAction
from plan_util import *
from plan_item import *
from plan_map_tools import *
from config import Config
from metadata import Metadata

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

    actions = {}
    mapTools = {}
    currentMapTool = None

    siteCodes = {}
    classCodes = {}
    metadata = None  # Metadata()

    _definitiveCategories = set()
    _schematicContextIncludeFilter = -1
    _schematicContextHighlightFilter = -1
    _schematicSourceIncludeFilter = -1
    _schematicSourceHighlightFilter = -1

    def __init__(self, project):
        super(Plan, self).__init__(project)
        self.project = project

    # Create the gui when the plugin is first created
    def initGui(self):
        self.dock = PlanDock(self.project.layerDock)
        action = self.project.addDockAction(':/plugins/ark/plan/drawPlans.png', self.tr(u'Draw Archaeological Plans'), callback=self.run, checkable=True)
        self.dock.initGui(self.project.iface, Qt.RightDockWidgetArea, action)

        self.dock.loadRawFileSelected.connect(self._loadRawPlan)
        self.dock.loadGeoFileSelected.connect(self._loadGeoPlan)
        self.dock.loadContextSelected.connect(self._loadContextPlans)
        self.dock.loadPlanSelected.connect(self._loadPlans)
        self.dock.featureNameChanged.connect(self._featureNameChanged)
        self.dock.autoSchematicSelected.connect(self._autoSchematicSelected)
        self.dock.editPointsSelected.connect(self._editPointsLayer)
        self.dock.editLinesSelected.connect(self._editLinesLayer)
        self.dock.editPolygonsSelected.connect(self._editPolygonsLayer)
        self.dock.sectionChanged.connect(self._sectionChanged)

        self.dock.clearSelected.connect(self.clearBuffers)
        self.dock.mergeSelected.connect(self.mergeBuffers)

        self.schematicDock = SchematicDock(self.project.layerDock)
        action = self.project.addDockAction(':/plugins/ark/plan/checkSchematic.png', self.tr(u'Check Context Schematics'), callback=self.runSchematic, checkable=True)

        self.schematicDock.initGui(self.project.iface, Qt.RightDockWidgetArea, action)
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
        self.schematicDock.clearSelected.connect(self._clearSchematic)
        self.schematicDock.mergeSelected.connect(self._mergeSchematic)
        self.project.filterModule.filterSetCleared.connect(self._resetSchematic)

        self.editDock = EditDock(self.project.iface, self.project.layerDock)
        action = self.project.addDockAction(':/plugins/ark/plan/editingTools.png', self.tr(u'Editing Tools'), callback=self.runEdit, checkable=True)
        self.editDock.initGui(self.project.iface, Qt.RightDockWidgetArea, action)

        self.metadata = Metadata(self.dock.metadataWidget, self.schematicDock.widget.metadataWidget)
        self.metadata.metadataChanged.connect(self.updateMapToolAttributes)

    # Load the project settings when project is loaded
    def loadProject(self):
        self.initialiseBuffers()

        # Assume layers are loaded and filters cleared
        self.siteCodes = set(self.project.plan.uniqueValues(self.project.fieldName('site')))
        self.siteCodes.add(self.project.siteCode())
        self.classCodes = set(self.project.plan.uniqueValues(self.project.fieldName('class')))

        self.dock.initSections(self._sectionItemList(self.project.siteCode()))

        for category in Config.featureCategories:
            #TODO Select by map tool type enum
            if category[2] == 'lvl' or category[2] == 'llv':
                self.addLevelTool(category[0], category[1], category[2], category[3], QIcon(category[4]), category[7])
            elif category[2] == 'scs':
                self.addSectionSchematicTool(category[0], category[1], category[2], category[3], QIcon(category[4]), category[5], category[7])
            else:
                self.addDrawingTool(category[0], category[1], category[2], category[3], QIcon(category[4]), category[5], category[7])
            if category[6] == True:
                self._definitiveCategories.add(category[2])

        self.schematicDock.setContext(0, SearchStatus.Unknown, SearchStatus.Unknown, SearchStatus.Unknown)
        self.schematicDock.addDrawingTool('sch', self.actions['sch'])
        self.schematicDock.addDrawingTool('lvl', self.actions['lvl'])

        self.editDock.loadProject(self.project)

        self.initialised = True

    # Save the project
    def writeProject(self):
        pass

    # Close the project
    def closeProject(self):
        self._clearSchematicFilters()
        # TODO Unload the drawing tools!
        self.editDock.closeProject()
        self.initialised = False

    # Unload the module when plugin is unloaded
    def unloadGui(self):
        for action in self.actions.values():
            if action.isChecked():
                action.setChecked(False)

        # Reset the initialisation
        self.initialised = False
        self._buffersInitialised = False

        # Unload the docks
        self.schematicDock.unloadGui()
        self.editDock.unloadGui()
        del self.editDock
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
            self.project.filterModule.showDock()
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

    # Plan Tools

    def _setPlanMetadata(self, pmd):
        self.metadata.setSiteCode(pmd.siteCode)
        self.metadata.setClassCode(pmd.sourceClass)
        if pmd.sourceId > 0:
            self.metadata.setItemId(pmd.sourceId)
            self.metadata.setSourceId(pmd.sourceId)
        self.metadata.setSourceCode('drw')
        self.metadata.setSourceClass(pmd.sourceClass)
        self.metadata.setSourceFile(pmd.filename)
        if self.metadata.classCode() == 'sec':
            self.dock.setSection(self.metadata.itemFeature.key)

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
            self.loadDrawing(ItemKey(self.project.siteCode(), 'cxt', context))

    def _loadPlans(self):
        plan, ok = QInputDialog.getInt(None, 'Load Plans', 'Please enter the Plan number to load all drawings for:', 1, 1, 99999)
        if (ok and plan > 0):
            self.loadDrawing(ItemKey(self.project.siteCode(), 'pln', plan))

    def loadDrawing(self, itemKey):
        drawingDir = self.project.georefDrawingDir(itemKey.classCode)
        drawingDir.setFilter(QDir.Files | QDir.NoDotAndDotDot)
        name = itemKey.name()
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

    def _featureNameChanged(self, featureName):
        self.metadata.setName(featureName)
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
        # Check the layers are writable
        if not self.project.plan.isWritable():
            self.project.showCriticalMessage('Plan layers are not writable! Please correct the permissions and log out.', 0)
            return

        # Check the buffers contain valid data
        if (not self._preMergeBufferCheck(self.project.plan.pointsBuffer)
            or not self._preMergeBufferCheck(self.project.plan.linesBuffer)
            or not self._preMergeBufferCheck(self.project.plan.polygonsBuffer)):
            return

        # Update the audit attributes
        timestamp = utils.timestamp()
        user = self.metadata.createdBy()
        self._preMergeBufferUpdate(self.project.plan.pointsBuffer, timestamp, user)
        self._preMergeBufferUpdate(self.project.plan.linesBuffer, timestamp, user)
        self._preMergeBufferUpdate(self.project.plan.polygonsBuffer, timestamp, user)

        # Finally actually merge the data
        if self.project.plan.mergeBuffers('Merge plan data'):
            self.project.showInfoMessage('Plan data successfully merged.')
        else:
            self.project.showCriticalMessage('Plan data merge failed! Some data has not been saved, please check your data.', 5)

    def _preMergeBufferCheck(self, layer):
        siteField = self.project.fieldName('site')
        classField = self.project.fieldName('class')
        idField = self.project.fieldName('id')
        categoryField = self.project.fieldName('category')
        sourceCodeField = self.project.fieldName('source_cd')
        sourceClassField = self.project.fieldName('source_cl')
        sourceIdField = self.project.fieldName('source_id')
        fileField = self.project.fieldName('file')
        commentField = self.project.fieldName('comment')
        for feature in layer.getFeatures():
            valid = True
            # Key attributes that must always be populated
            if (self._isEmpty(feature.attribute(siteField))
                or self._isEmpty(feature.attribute(classField))
                or self._isEmpty(feature.attribute(idField))
                or self._isEmpty(feature.attribute(categoryField))
                or self._isEmpty(feature.attribute(sourceCodeField))):
                valid = False
            # Source attributes required depend on the source type
            if feature.attribute(sourceCodeField) == 'cre' or feature.attribute(sourceCodeField) == 'oth':
                if self._isEmpty(feature.attribute(commentField)):
                    valid = False
            elif feature.attribute(sourceCodeField) == 'svy':
                if self._isEmpty(feature.attribute(fileField)):
                    valid = False
            elif (self._isEmpty(feature.attribute(sourceClassField)) or self._isEmpty(feature.attribute(sourceIdField))):
                    valid = False
            if not valid:
                self.project.showCriticalMessage('Plan data merge failed! Some key attributes are not populated, please check the attribute table and complete the missing data.', 5)
                return False
        return True

    def _isEmpty(self, val):
        if val is None or val == NULL:
            return True
        if type(val) == str and (val == '' or val.strip() == ''):
            return True
        return False

    def _preMergeBufferUpdate(self, layer, timestamp, user):
        siteField = self.project.fieldName('site')
        classField = self.project.fieldName('class')
        createdOnField = self.project.fieldName('created_on')
        createdOnIdx = layer.fieldNameIndex(createdOnField)
        createdByIdx = layer.fieldNameIndex(self.project.fieldName('created_by'))
        updatedOnIdx = layer.fieldNameIndex(self.project.fieldName('updated_on'))
        updatedByIdx = layer.fieldNameIndex(self.project.fieldName('updated_by'))
        for feature in layer.getFeatures():
            if self._isEmpty(feature.attribute(createdOnField)):
                layer.changeAttributeValue(feature.id(), createdOnIdx, timestamp)
                layer.changeAttributeValue(feature.id(), createdByIdx, user)
            else:
                layer.changeAttributeValue(feature.id(), updatedOnIdx, timestamp)
                layer.changeAttributeValue(feature.id(), updatedByIdx, user)
            self.siteCodes.add(feature.attribute(siteField))
            self.classCodes.add(feature.attribute(classField))

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

    def _addMapTool(self, dockTab, category, mapTool, action):
        action.triggered.connect(self.validateFeature)
        self.dock.addDrawingTool(dockTab, action)
        self.actions[category] = action
        self.mapTools[category] = mapTool

    def addDrawingTool(self, collection, classCode, category, toolName, icon, featureType, dockTab):
        action = self._newMapToolAction(classCode, category, toolName, icon)
        layer = None
        if (featureType == FeatureType.Line or featureType == FeatureType.Segment):
            layer = self.project.collection(collection).linesBuffer
        elif featureType == FeatureType.Polygon:
            layer = self.project.collection(collection).polygonsBuffer
        else:
            layer = self.project.collection(collection).pointsBuffer
        mapTool = self._newMapTool(toolName, featureType, layer, action)
        self._addMapTool(dockTab, category, mapTool, action)

    def addSectionSchematicTool(self, collection, classCode, category, toolName, icon, featureType, dockTab):
        action = self._newMapToolAction(classCode, category, toolName, icon)
        geom = self._sectionLineGeometry(self.dock.sectionKey())
        mapTool = ArkMapToolSectionSchematic(self.project.iface, geom, self.project.collection(collection).polygonsBuffer, toolName)
        mapTool.setAction(action)
        mapTool.setPanningEnabled(True)
        mapTool.setZoomingEnabled(True)
        mapTool.setAttributeQuery(Config.fieldName('id'), QVariant.Int, 0, 'Context Number', 'Please enter the Context Number:', 0, 99999)
        mapTool.activated.connect(self.mapToolActivated)
        self._addMapTool(dockTab, category, mapTool, action)

    def addLevelTool(self, collection, classCode, category, toolName, icon, dockTab):
        action = self._newMapToolAction(classCode, category, toolName, icon)
        mapTool = self._newMapTool(toolName, FeatureType.Point, self.project.collection(collection).pointsBuffer, action)
        mapTool.setAttributeQuery('elevation', QVariant.Double, 0.0, 'Add Level', 'Please enter the elevation in meters (m):', -1000, 1000, 2)
        self._addMapTool(dockTab, category, mapTool, action)

    def addSectionTool(self, collection, classCode, category, toolName, icon, dockTab):
        action = self._newMapToolAction(classCode, category, toolName, icon)
        mapTool = ArkMapToolAddBaseline(self.project.iface, self.project.collection(collection).linesBuffer, FeatureType.Line, self.tr('Add section'))
        mapTool.setAttributeQuery('id', QVariant.String, '', 'Section ID', 'Please enter the Section ID (e.g. S45):')
        mapTool.setPointQuery('elevation', QVariant.Double, 0.0, 'Add Level', 'Please enter the pin or string height in meters (m):', -100, 100, 2)
        self._addMapTool(dockTab, category, mapTool, action)

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
        if toolData['class'] != self.metadata.classCode():
            self.metadata.setItemId('')
        self.metadata.setClassCode(toolData['class'])
        self.metadata.setCategory(toolData['category'])
        mapTool.setDefaultAttributes(self.metadata.itemFeature.toAttributes())

    def validateFeature(self):
        if self.metadata.sourceClass() == self.metadata.classCode() and int(self.metadata.sourceId()) <= 0:
            self.metadata.setSourceId(self.metadata.itemId())
        self.metadata.validate()
        if self.metadata.sourceClass() == self.metadata.classCode() and int(self.metadata.sourceId()) <= 0:
            self.metadata.setSourceId(self.metadata.itemId())
        self.dock.setFeatureName(self.metadata.name())

    def _autoSchematicSelected(self, sourceId):
        self.actions['sch'].trigger()
        self._autoSchematic(sourceId, self.metadata, self.project.plan.linesBuffer, self.project.plan.polygonsBuffer)

    def _autoSchematic(self, sourceId, md, inLayer, outLayer):
        definitiveFeatures = []
        if inLayer.selectedFeatureCount() > 0:
            definitiveFeatures = inLayer.selectedFeatures()
        else:
            featureIter = inLayer.getFeatures()
            for feature in featureIter:
                if feature.attribute(self.project.fieldName('id')) == sourceId and feature.attribute(self.project.fieldName('category')) in self._definitiveCategories:
                    definitiveFeatures.append(feature)
        schematicFeatures = geometry.polygonizeFeatures(definitiveFeatures, outLayer.pendingFields())
        if len(schematicFeatures) <= 0:
            return
        schematic = geometry.dissolveFeatures(schematicFeatures, outLayer.pendingFields())
        attrs = md.itemFeature.toAttributes()
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

    def editInBuffers(self, itemKey):
        if self._confirmDelete(itemKey.itemId, 'Confirm Move Item'):
            self._editInBuffers(itemKey)

    def _editInBuffers(self, itemKey):
        request = itemKey.featureRequest()
        self.project.plan.moveFeatureRequestToBuffers(request)
        self.metadata.setSiteCode(itemKey.siteCode)
        self.metadata.setClassCode(itemKey.classCode)
        self.metadata.setItemId(itemKey.itemId)
        self.metadata.setComment('')
        self.metadata.setSourceCode('drw')
        self.metadata.setSourceClass(itemKey.classCode)
        self.metadata.setSourceId(itemKey.itemId)
        self.metadata.setSourceFile('')

    def deleteItem(self, itemKey):
        if self._confirmDelete(itemKey.itemId, 'Confirm Delete Item'):
            request = itemKey.featureRequest()
            self.project.plan.deleteFeatureRequest(request)

    def panToItem(self, itemKey, highlight=False):
        extent = self.itemExtent(itemKey)
        if extent == None or extent.isNull() or extent.isEmpty():
            return
        self.project.mapCanvas().setCenter(extent.center())
        if highlight:
            self.project.filterModule.removeHighlightFilters()
            self.project.filterModule.addFilterClause(FilterType.HighlightFilter, itemKey)
        self.project.mapCanvas().refresh()

    def zoomToItem(self, itemKey, highlight=False):
        extent = self.itemExtent(itemKey)
        if extent == None or extent.isNull() or extent.isEmpty():
            return
        extent.scale(1.05)
        self.project.mapCanvas().setExtent(extent)
        if highlight:
            self.project.filterModule.removeHighlightFilters()
            self.project.filterModule.addFilterClause(FilterType.HighlightFilter, itemKey)
        self.project.mapCanvas().refresh()

    def filterItem(self, itemKey):
        self.project.filterModule.removeFilters()
        self.project.filterModule.addFilterClause(FilterType.IncludeFilter, itemKey)
        self.project.mapCanvas().refresh()

    def excludeFilterItem(self, itemKey):
        self.project.filterModule.addFilterClause(FilterType.ExcludeFilter, itemKey)
        self.project.mapCanvas().refresh()

    def highlightItem(self, itemKey):
        self.project.filterModule.removeHighlightFilters()
        self.project.filterModule.addFilterClause(FilterType.HighlightFilter, itemKey)
        self.project.mapCanvas().refresh()

    def addHighlightItem(self, itemKey):
        self.project.filterModule.addFilterClause(FilterType.HighlightFilter, itemKey)
        self.project.mapCanvas().refresh()

    def itemExtent(self, itemKey):
        request = itemKey.featureRequest()
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

    def _sectionItemList(self, siteCode):
        # TODO in 2.14 use addOrderBy()
        request = self._classItemsRequest(siteCode, 'sec')
        fi = self.project.plan.linesLayer.getFeatures(request)
        lst = []
        for feature in fi:
            lst.append(ItemFeature(feature))
        lst.sort()
        return lst

    def _sectionLineGeometry(self, itemKey):
        if itemKey and itemKey.isValid():
            request = self._categoryRequest(itemKey, 'sln')
            fi = self.project.plan.linesLayer.getFeatures(request)
            for feature in fi:
                return QgsGeometry(feature.geometry())
        return QgsGeometry()

    def _sectionChanged(self, itemKey):
        try:
            self.mapTools['scs'].setSectionGeometry(self._sectionLineGeometry(itemKey))
        except:
            pass

    # Feature Request Methods

    def _eqClause(self, field, value):
        return _doublequote(self.project.fieldName(field)) + ' = ' + _quote(str(value))

    def _neClause(self, field, value):
        return _doublequote(self.project.fieldName(field)) + ' != ' + _quote(str(value))

    def _categoryClause(self, category):
        return self._eqClause('category', category)

    def _notCategoryClause(self, category):
        return self._neClause('category', category)

    def _featureRequest(self, expr):
        request = QgsFeatureRequest()
        request.setFilterExpression(expr)
        return request

    def _categoryRequest(self, itemKey, category):
        return self._featureRequest(itemKey.filterClause() + ' and ' + self._categoryClause(category))

    def _notCategoryRequest(self, itemKey, category):
        return self._featureRequest(itemKey.filterClause() + ' and ' + self._notCategoryClause(category))

    def _classItemsRequest(self, siteCode, classCode):
        return self._featureRequest(self._eqClause('site', siteCode)+ ' and ' + self._eqClause('class', classCode))

    # SchematicDock methods

    def _resetSchematic(self):
        self._clearSchematicFilters()
        self.schematicDock.setContext(0, SearchStatus.Unknown, SearchStatus.Unknown, SearchStatus.Unknown)

    def _clearSchematic(self):
        self.clearBuffers()
        self._findPanContext()

    def _mergeSchematic(self):
        self.mergeBuffers()
        self._findPanContext()

    def _clearSchematicFilters(self):
        self._clearSchematicContextIncludeFilter()
        self._clearSchematicContextHighlightFilter()
        self._clearSchematicSourceFilters()

    def _clearSchematicContextIncludeFilter(self):
        self.project.filterModule.removeFilterClause(self._schematicContextIncludeFilter)
        self._schematicContextIncludeFilter = -1

    def _clearSchematicContextHighlightFilter(self):
        self.project.filterModule.removeFilterClause(self._schematicContextHighlightFilter)
        self._schematicContextHighlightFilter = -1

    def _clearSchematicSourceFilters(self):
        self.project.filterModule.removeFilterClause(self._schematicSourceIncludeFilter)
        self._schematicSourceIncludeFilter = -1
        self.project.filterModule.removeFilterClause(self._schematicSourceHighlightFilter)
        self._schematicSourceHighlightFilter = -1

    def _findPanContext(self):
        self._findContext()
        if self.schematicDock.contextStatus() == SearchStatus.Found:
            self.panToItem(self.schematicDock.contextItemKey())

    def _findZoomContext(self):
        self._findContext()
        if self.schematicDock.contextStatus() == SearchStatus.Found:
            self.zoomToItem(self.schematicDock.contextItemKey())

    def _editSchematicContext(self):
        self.editInBuffers(self.schematicDock.contextItemKey())

    def _findContext(self):
        self._clearSchematicFilters()

        filterModule = self.project.filterModule
        if self.metadata.siteCode() == '':
            self.metadata.setSiteCode(self.project.siteCode())
        if filterModule.hasFilterType(FilterType.IncludeFilter) or filterModule.hasFilterType(FilterType.IncludeFilter):
            self._schematicContextFilter = filterModule.addFilterClause(FilterType.IncludeFilter, self.schematicDock.contextItemKey(), FilterAction.LockFilter)
        self._schematicContextHighlightFilter = filterModule.addFilterClause(FilterType.HighlightFilter, self.schematicDock.contextItemKey(), FilterAction.LockFilter)

        itemRequest = self.schematicDock.contextItemKey().featureRequest()
        haveFeature = SearchStatus.Found
        try:
            feature = self.project.plan.linesLayer.getFeatures(itemRequest).next()
            self._copyFeatureMetadata(feature)
        except StopIteration:
            haveFeature = SearchStatus.NotFound

        if haveFeature == SearchStatus.NotFound:
            polyRequest = self._notCategoryRequest(self.schematicDock.contextItemKey(), 'sch')
            haveFeature = SearchStatus.Found
            try:
                self.project.plan.polygonsLayer.getFeatures(polyRequest).next()
            except StopIteration:
                haveFeature = SearchStatus.NotFound

        schRequest = self._categoryRequest(self.schematicDock.contextItemKey(), 'sch')
        haveSchematic = SearchStatus.Found
        try:
            self.project.plan.polygonsLayer.getFeatures(schRequest).next()
        except StopIteration:
            haveSchematic = SearchStatus.NotFound

        scsRequest = self._categoryRequest(self.schematicDock.contextItemKey(), 'scs')
        haveSectionSchematic = SearchStatus.Found
        try:
            self.project.plan.polygonsLayer.getFeatures(scsRequest).next()
        except StopIteration:
            haveSectionSchematic = SearchStatus.NotFound

        self.schematicDock.setContext(self.schematicDock.context(), haveFeature, haveSchematic, haveSectionSchematic)
        self.metadata.setItemId(self.schematicDock.context())

    def _findPanSource(self):
        if self.schematicDock.sourceStatus() == SearchStatus.Unknown:
            self._findSource()
        if self.schematicDock.sourceStatus() == SearchStatus.Found:
            self.panToItem(self.schematicDock.sourceItemKey())

    def _findZoomSource(self):
        if self.schematicDock.sourceStatus() == SearchStatus.Unknown:
            self._findSource()
        if self.schematicDock.sourceStatus() == SearchStatus.Found:
            self.zoomToItem(self.schematicDock.sourceItemKey())

    def _editSource(self):
        self.editInBuffers(self.schematicDock.sourceItemKey())

    def _findSource(self):
        self._clearSchematicSourceFilters()

        filterModule = self.project.filterModule
        if self.metadata.siteCode() == '':
            self.metadata.setSiteCode(self.project.siteCode())
        if filterModule.hasFilterType(FilterType.IncludeFilter) or filterModule.hasFilterType(FilterType.IncludeFilter):
            self._schematicSourceIncludeFilter = filterModule.addFilterClause(FilterType.IncludeFilter, self.schematicDock.sourceItemKey(), FilterAction.LockFilter)
        self._clearSchematicContextHighlightFilter()
        self._schematicSourceHighlightFilter = filterModule.addFilterClause(FilterType.HighlightFilter, self.schematicDock.sourceItemKey(), FilterAction.LockFilter)

        itemRequest = self.schematicDock.sourceItemKey().featureRequest()
        haveFeature = SearchStatus.Found
        try:
            self.project.plan.linesLayer.getFeatures(itemRequest).next()
        except StopIteration:
            haveFeature = SearchStatus.NotFound

        schRequest = self._categoryRequest(self.schematicDock.sourceItemKey(), 'sch')
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
        self.metadata.setSiteCode(self._attribute(feature, 'site'))
        self.metadata.setComment(self._attribute(feature, 'comment'))
        self.metadata.setSourceCode('cln')
        self.metadata.setSourceClass('cxt')
        self.metadata.setSourceId(self.schematicDock.sourceContext())
        self.metadata.setSourceFile('')

    def _copySourceSchematic(self):
        request = self._categoryRequest(self.schematicDock.sourceItemKey(), 'sch')
        fi = self.project.plan.polygonsLayer.getFeatures(request)
        for feature in fi:
            feature.setAttribute(self.project.fieldName('site'), self.metadata.siteCode())
            feature.setAttribute(self.project.fieldName('class'), 'cxt')
            feature.setAttribute(self.project.fieldName('id'), self.schematicDock.context())
            feature.setAttribute(self.project.fieldName('name'), None)
            feature.setAttribute(self.project.fieldName('category'), 'sch')
            feature.setAttribute(self.project.fieldName('source_cd'), self.metadata.sourceCode())
            feature.setAttribute(self.project.fieldName('source_cl'), self.metadata.sourceClass())
            feature.setAttribute(self.project.fieldName('source_id'), self.metadata.sourceId())
            feature.setAttribute(self.project.fieldName('file'), self.metadata.sourceFile())
            feature.setAttribute(self.project.fieldName('comment'), self.metadata.comment())
            feature.setAttribute(self.project.fieldName('created_by'), self.metadata.createdBy())
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
        self._mergeSchematic()
