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
import bisect, copy

from PyQt4.QtCore import Qt, QVariant, QFileInfo, QObject, QDir, QFile
from PyQt4.QtGui import QAction, QIcon, QFileDialog, QInputDialog

from qgis.core import *

from ..libarkqgis.map_tools import *
from ..libarkqgis import utils, layers, geometry

from ..georef.georef_dialog import GeorefDialog

from plan_dock import PlanDock
from plan_error import ErrorDialog, PlanError
from select_drawing_dialog import SelectDrawingDialog

from filter import FilterType, FilterAction
from plan_util import *
from plan_item import *
from plan_map_tools import *
from config import Config
from metadata import Metadata
from schematic_widget import SearchStatus

import resources

def _quote(string):
    return "'" + string + "'"

def _doublequote(string):
    return '"' + string + '"'

class Plan(QObject):

    # Project settings
    project = None # Project()

    dock = None # PlanDock()

    # Internal variables
    initialised = False

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

    _editSchematic = False

    _itemLogPath = ''

    def __init__(self, project):
        super(Plan, self).__init__(project)
        self.project = project

    # Create the gui when the plugin is first created
    def initGui(self):
        self.dock = PlanDock(self.project.layerDock)
        action = self.project.addDockAction(':/plugins/ark/plan/drawPlans.png', self.tr(u'Drawing Tools'), callback=self.run, checkable=True)
        self.dock.initGui(self.project.iface, Qt.RightDockWidgetArea, action)

        self.dock.loadRawFileSelected.connect(self._loadRawPlan)
        self.dock.loadGeoFileSelected.connect(self._loadGeoPlan)

        self.dock.autoSchematicSelected.connect(self._autoSchematicSelected)
        self.dock.editPointsSelected.connect(self._editPointsLayer)
        self.dock.editLinesSelected.connect(self._editLinesLayer)
        self.dock.editPolygonsSelected.connect(self._editPolygonsLayer)
        self.dock.featureNameChanged.connect(self._featureNameChanged)
        self.dock.sectionChanged.connect(self._sectionChanged)
        self.dock.clearSelected.connect(self.clearBuffers)
        self.dock.mergeSelected.connect(self.mergeBuffers)

        self.dock.loadArkData.connect(self._loadArkData)
        self.dock.findContextSelected.connect(self._findMoveContext)
        self.dock.firstContextSelected.connect(self._firstContext)
        self.dock.lastContextSelected.connect(self._lastContext)
        self.dock.prevContextSelected.connect(self._prevContext)
        self.dock.nextContextSelected.connect(self._nextContext)
        self.dock.prevMissingSelected.connect(self._prevMissing)
        self.dock.nextMissingSelected.connect(self._nextMissing)
        self.dock.editContextSelected.connect(self._editSchematicContext)
        self.dock.findSourceSelected.connect(self._findPanSource)
        self.dock.copySourceSelected.connect(self._editSourceSchematic)
        self.dock.cloneSourceSelected.connect(self._cloneSourceSchematic)
        self.dock.editSourceSelected.connect(self._editSource)
        self.dock.contextChanged.connect(self._clearSchematicFilters)
        self.dock.resetSelected.connect(self._resetSchematic)

        self.project.filterModule.filterSetCleared.connect(self._clearSchematic)

        # TODO Think of a better way...
        self.metadata = Metadata(self.dock.widget.metadataWidget)
        self.metadata.metadataChanged.connect(self.updateMapToolAttributes)

    # Load the project settings when project is loaded
    def loadProject(self):
        # Assume layers are loaded and filters cleared
        self.siteCodes = set(self.project.siteCodes())
        self.classCodes = set(self.project.plan.uniqueValues(self.project.fieldName('class')))

        self.dock.loadProject(self.project)
        # TODO Move these into widgets???
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

        if self.project.plan.settings.log:
            self._itemLogPath = self.project.projectPath() + '/' + self.project.plan.settings.collectionPath + '/log/itemLog.csv'
            if not QFile.exists(self._itemLogPath):
                fd = open(self._itemLogPath, 'a')
                fd.write('timestamp,action,siteCode,classCode,itemId\n')
                fd.close()

        self.project.plan.pointsBuffer.setFeatureFormSuppress(QgsVectorLayer.SuppressOn)
        self.project.plan.linesBuffer.setFeatureFormSuppress(QgsVectorLayer.SuppressOn)
        self.project.plan.polygonsBuffer.setFeatureFormSuppress(QgsVectorLayer.SuppressOn)

        self.initialised = True

    # Save the project
    def writeProject(self):
        # We don't want to save the schematic serach or filters
        self._clearSchematic()

    # Close the project
    def closeProject(self):
        self._clearSchematicFilters()
        # TODO Unload the drawing tools!
        self.dock.closeProject()
        self.initialised = False

    # Unload the module when plugin is unloaded
    def unloadGui(self):
        for action in self.actions.values():
            if action.isChecked():
                action.setChecked(False)

        # Reset the initialisation
        self.initialised = False

        # Unload the dock
        self.dock.unloadGui()
        del self.dock

    def run(self, checked):
        if checked and self.initialised:
            self.project.filterModule.showDock()
        else:
            self.dock.menuAction().setChecked(False)

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

    def loadDrawing(self, itemKey, zoomToDrawing=True):
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
            self.project.loadGeoLayer(drawing, zoomToDrawing)

    def loadSourceDrawings(self, itemKey):
        sourceKeys = set()
        sourceKeys.add(itemKey)
        itemRequest = itemKey.featureRequest()
        for feature in self.project.plan.polygonsLayer.getFeatures(itemRequest):
            itemSource = ItemSource(feature)
            if itemSource.key.isValid():
                sourceKeys.add(itemSource.key)
        for feature in self.project.plan.linesLayer.getFeatures(itemRequest):
            itemSource = ItemSource(feature)
            if itemSource.key.isValid():
                sourceKeys.add(itemSource.key)
        for feature in self.project.plan.pointsLayer.getFeatures(itemRequest):
            itemSource = ItemSource(feature)
            if itemSource.key.isValid():
                sourceKeys.add(itemSource.key)
        for sourceKey in sorted(sourceKeys):
            self.loadDrawing(sourceKey)

    def _featureNameChanged(self, featureName):
        self.metadata.setName(featureName)
        self.updateMapToolAttributes()

    # Georeference Tools

    def georeferencePlan(self, rawFile):
        pmd = PlanMetadata(rawFile)
        georefDialog = GeorefDialog(rawFile, self.project.georefDrawingDir(pmd.sourceClass), self.project.projectCrs().authid(), self.project.grid.settings.pointsLayerName, self.project.fieldName('local_x'), self.project.fieldName('local_y'))
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
        errors = self._preMergeBufferCheck(self.project.plan.pointsBuffer)
        errors.extend(self._preMergeBufferCheck(self.project.plan.linesBuffer))
        errors.extend(self._preMergeBufferCheck(self.project.plan.polygonsBuffer))
        if len(errors) > 0:
            dialog = ErrorDialog()
            dialog.loadErrors(errors)
            dialog.exec_()
            return

        # Update the audit attributes
        timestamp = utils.timestamp()
        user = self.metadata.createdBy()
        self._preMergeBufferUpdate(self.project.plan.pointsBuffer, timestamp, user)
        self._preMergeBufferUpdate(self.project.plan.linesBuffer, timestamp, user)
        self._preMergeBufferUpdate(self.project.plan.polygonsBuffer, timestamp, user)

        # Finally actually merge the data
        if self.project.plan.mergeBuffers('Merge plan data', timestamp):
            self.project.showInfoMessage('Plan data successfully merged.')
            self._logItemAction(self.metadata.itemFeature.key, 'Merge Buffers', timestamp)
            if self._editSchematic:
                self._editSchematic = False
                self.dock.activateSchematicCheck()
                self._findContext()
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
        errors = []
        row = 0
        for feature in layer.getFeatures():
            # Set up the error template
            error = PlanError()
            error.layer = layer.name()
            error.row = row
            row = row + 1
            error.fid = feature.id()
            error.feature.fromFeature(feature)
            # Feature must be valid
            if not feature.isValid():
                error.field = 'feature'
                error.message = 'Invalid Feature'
                errors.append(copy.deepcopy(error))
            # Geometry must be valid
            error.field = 'geometry'
            if feature.geometry() is None:
                error.message = 'No Geometry'
                errors.append(copy.deepcopy(error))
            elif feature.geometry().isEmpty():
                error.message = 'Empty Geometry'
                errors.append(copy.deepcopy(error))
            else:
                error.message = 'Invalid Geometry'
                geomErrs = feature.geometry().validateGeometry()
                for err in geomErrs:
                    error.message = err.what()
                    errors.append(copy.deepcopy(error))
            # Key attributes that must always be populated
            if self._isEmpty(feature.attribute(siteField)):
                error.field = siteField
                error.message = 'Site Code is required'
                errors.append(copy.deepcopy(error))
            if self._isEmpty(feature.attribute(classField)):
                error.field = classField
                error.message = 'Class Code is required'
                errors.append(copy.deepcopy(error))
            if self._isEmpty(feature.attribute(idField)):
                error.field = idField
                error.message = 'ID is required'
                errors.append(copy.deepcopy(error))
            if self._isEmpty(feature.attribute(categoryField)):
                error.field = categoryField
                error.message = 'Category is required'
                errors.append(copy.deepcopy(error))
            if self._isEmpty(feature.attribute(sourceCodeField)):
                error.field = sourceCodeField
                error.message = 'Source Code is required'
                errors.append(copy.deepcopy(error))
            # Source attributes required depend on the source type
            if feature.attribute(sourceCodeField) == 'cre' or feature.attribute(sourceCodeField) == 'oth':
                if self._isEmpty(feature.attribute(commentField)):
                    error.field = sourceCodeField
                    error.message = 'Comment is required for Source type of Creator or Other'
                    errors.append(copy.deepcopy(error))
            elif feature.attribute(sourceCodeField) == 'svy':
                if self._isEmpty(feature.attribute(fileField)):
                    error.field = sourceCodeField
                    error.message = 'Filename is required for Source type of Survey'
                    errors.append(copy.deepcopy(error))
            else: # 'drw', 'unc', 'skt', 'cln', 'mod', 'inf'
                if (feature.attribute(sourceCodeField) == 'drw' or feature.attribute(sourceCodeField) == 'unc') and self._isEmpty(feature.attribute(fileField)):
                    error.field = sourceCodeField
                    error.message = 'Filename is required for Source type of Drawing'
                    errors.append(copy.deepcopy(error))
                if (self._isEmpty(feature.attribute(sourceClassField)) or self._isEmpty(feature.attribute(sourceIdField))):
                    error.field = sourceCodeField
                    error.message = 'Source Class and ID is required'
                    errors.append(copy.deepcopy(error))
        return errors

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
        self.project.plan.clearBuffers('Clear Buffers')
        if self._editSchematic:
            self._editSchematic = False
            self.dock.activateSchematicCheck()

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

    def _autoSchematicSelected(self):
        self.actions['sch'].trigger()
        self._autoSchematic(self.metadata, self.project.plan.linesBuffer, self.project.plan.polygonsBuffer)

    def _autoSchematic(self, md, inLayer, outLayer):
        definitiveFeatures = []
        if inLayer.selectedFeatureCount() > 0:
            definitiveFeatures = inLayer.selectedFeatures()
        else:
            featureIter = inLayer.getFeatures()
            for feature in featureIter:
                if str(feature.attribute(self.project.fieldName('id'))) == str(md.itemId()) and feature.attribute(self.project.fieldName('category')) in self._definitiveCategories:
                    definitiveFeatures.append(feature)
        if len(definitiveFeatures) <= 0:
            return
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

    def _logItemAction(self, key, action, timestamp=None):
        if self.project.plan.settings.log:
            if not timestamp:
                timestamp = utils.timestamp()
            fd = open(self._itemLogPath, 'a')
            fd.write(utils.doublequote(timestamp) + ',' + utils.doublequote(action) + ',' + key.toCsv() + '\n')
            fd.close()

    def editInBuffers(self, itemKey):
        if self._confirmDelete(itemKey.itemId, 'Confirm Move Item'):
            request = itemKey.featureRequest()
            timestamp = utils.timestamp()
            action = 'Edit Item'
            if self.project.plan.moveFeatureRequestToBuffers(request, action, timestamp):
                self._logItemAction(itemKey, action, timestamp)
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
            timestamp = utils.timestamp()
            action = 'Delete Item'
            if self.project.plan.deleteFeatureRequest(request, action, timestamp):
                self._logItemAction(itemKey, action, timestamp)

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

    def moveToItem(self, itemKey, highlight=False):
        extent = self.itemExtent(itemKey)
        if extent == None or extent.isNull() or extent.isEmpty():
            return
        mapExtent = self.project.mapCanvas().extent()
        if (extent.width() > mapExtent.width() or extent.height() > mapExtent.height()
            or extent.width() * extent.height() > mapExtent.width() * mapExtent.height()):
            extent.scale(1.05)
            self.project.mapCanvas().setExtent(extent)
        else:
            self.project.mapCanvas().setCenter(extent.center())
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

    def _loadArkData(self):
        self.project.data.loadAllItems(self.project)
        if self.project.data.itemKeys['cxt'] and len(self.project.data.itemKeys['cxt']) > 0:
            self.dock.activateArkData()

    def _resetSchematic(self):
        self._clearSchematic()
        self.dock.activateSchematicCheck()

    def _clearSchematic(self):
        self._clearSchematicFilters()
        self.dock.resetContext()

    def _mergeSchematic(self):
        self.mergeBuffers()
        self._findMoveContext()

    def _clearSchematicFilters(self):
        self._clearSchematicContextIncludeFilter()
        self._clearSchematicContextHighlightFilter()
        self._clearSchematicSourceFilters()

    def _clearSchematicContextIncludeFilter(self):
        if self._schematicContextIncludeFilter >= 0:
            self.project.filterModule.removeFilterClause(self._schematicContextIncludeFilter)
            self._schematicContextIncludeFilter = -1

    def _clearSchematicContextHighlightFilter(self):
        if self._schematicContextHighlightFilter >= 0:
            self.project.filterModule.removeFilterClause(self._schematicContextHighlightFilter)
            self._schematicContextHighlightFilter = -1

    def _clearSchematicSourceFilters(self):
        if self._schematicSourceIncludeFilter >= 0:
            self.project.filterModule.removeFilterClause(self._schematicSourceIncludeFilter)
            self._schematicSourceIncludeFilter = -1
        if self._schematicSourceHighlightFilter >= 0:
            self.project.filterModule.removeFilterClause(self._schematicSourceHighlightFilter)
            self._schematicSourceHighlightFilter = -1

    def _findMoveContext(self, context=ItemKey()):
        self._findContext(context)
        if self.dock.contextStatus() == SearchStatus.Found:
            self.moveToItem(self.dock.contextItemKey())

    def _firstContext(self):
        self._findMoveContext(self.project.data.itemKeys['cxt'][0])

    def _lastContext(self):
        self._findMoveContext(self.project.data.itemKeys['cxt'][-1])

    def _prevContext(self):
        context = self.dock.contextItemKey()
        idx = 0
        if context.isValid():
            idx = bisect.bisect_left(self.project.data.itemKeys['cxt'], context) - 1
        if idx >= 0 and idx < len(self.project.data.itemKeys['cxt']) - 1:
            self._findMoveContext(self.project.data.itemKeys['cxt'][idx])

    def _nextContext(self):
        context = self.dock.contextItemKey()
        idx = 0
        if context.isValid():
            idx = bisect.bisect(self.project.data.itemKeys['cxt'], context)
        if idx >= 0 and idx < len(self.project.data.itemKeys['cxt']) - 1:
            self._findMoveContext(self.project.data.itemKeys['cxt'][idx])

    def _prevMissing(self):
        context = self.dock.contextItemKey()
        idx = 0
        if context.isValid():
            idx = bisect.bisect_left(self.project.data.itemKeys['cxt'], context)
        for prv in reversed(range(idx)):
            item = self.project.data.itemKeys['cxt'][prv]
            status = self._schematicStatus(item)
            if status == SearchStatus.NotFound:
                self._findContext(item)
                return

    def _nextMissing(self):
        context = self.dock.contextItemKey()
        idx = 0
        if context.isValid():
            idx = bisect.bisect(self.project.data.itemKeys['cxt'], context)
        for item in self.project.data.itemKeys['cxt'][idx:]:
            status = self._schematicStatus(item)
            if status == SearchStatus.NotFound:
                self._findContext(item)
                return

    def _editSchematicContext(self):
        self._editSchematic = True
        self.editInBuffers(self.dock.contextItemKey())
        self.dock.widget.setCurrentIndex(0)

    def _arkStatus(self, item):
        try:
            if item in self.project.data.itemKeys[item.classCode]:
                return SearchStatus.Found
        except:
            return SearchStatus.Unknown
        return SearchStatus.NotFound

    def _featureStatus(self, item, copyMetadata=False):
        itemRequest = item.featureRequest()
        try:
            feature = self.project.plan.linesLayer.getFeatures(itemRequest).next()
            if copyMetadata:
                self._copyFeatureMetadata(feature)
        except StopIteration:
            return SearchStatus.NotFound
        return SearchStatus.Found

    def _schematicStatus(self, item):
        schRequest = self._categoryRequest(item, 'sch')
        try:
            self.project.plan.polygonsLayer.getFeatures(schRequest).next()
        except StopIteration:
            return SearchStatus.NotFound
        return SearchStatus.Found

    def _findContext(self, context=ItemKey()):
        self._clearSchematicFilters()

        if not context.isValid():
            context = self.dock.contextItemKey()

        filterModule = self.project.filterModule
        self.metadata.setSiteCode(context.siteCode)
        if filterModule.hasFilterType(FilterType.IncludeFilter) or filterModule.hasFilterType(FilterType.ExcludeFilter):
            self._schematicContextIncludeFilter = filterModule.addFilterClause(FilterType.IncludeFilter, context, FilterAction.LockFilter)
        self._schematicContextHighlightFilter = filterModule.addFilterClause(FilterType.HighlightFilter, context, FilterAction.LockFilter)

        haveArk = SearchStatus.NotFound
        try:
            if context in self.project.data.itemKeys['cxt']:
                haveArk = SearchStatus.Found
        except:
            haveArk = SearchStatus.Unknown

        haveArk = self._arkStatus(context)
        haveFeature = self._featureStatus(context, True)

        if haveFeature == SearchStatus.NotFound:
            polyRequest = self._notCategoryRequest(context, 'sch')
            haveFeature = SearchStatus.Found
            try:
                self.project.plan.polygonsLayer.getFeatures(polyRequest).next()
            except StopIteration:
                haveFeature = SearchStatus.NotFound

        haveSchematic = self._schematicStatus(context)

        scsRequest = self._categoryRequest(context, 'scs')
        haveSectionSchematic = SearchStatus.Found
        try:
            self.project.plan.polygonsLayer.getFeatures(scsRequest).next()
        except StopIteration:
            haveSectionSchematic = SearchStatus.NotFound

        self.dock.setContext(context, haveArk, haveFeature, haveSchematic, haveSectionSchematic)
        self.metadata.setItemId(context.itemId)

    def _findPanSource(self):
        if self.dock.sourceStatus() == SearchStatus.Unknown:
            self._findSource()
        if self.dock.sourceStatus() == SearchStatus.Found:
            self.moveToItem(self.dock.sourceItemKey())

    def _editSource(self):
        self.editInBuffers(self.dock.sourceItemKey())
        self.dock.widget.setCurrentIndex(0)

    def _findSource(self, source=ItemKey()):
        self._clearSchematicSourceFilters()

        if not source.isValid():
            source = self.dock.sourceItemKey()

        filterModule = self.project.filterModule
        if self.metadata.siteCode() == '':
            self.metadata.setSiteCode(self.project.siteCode())
        if filterModule.hasFilterType(FilterType.IncludeFilter) or filterModule.hasFilterType(FilterType.IncludeFilter):
            self._schematicSourceIncludeFilter = filterModule.addFilterClause(FilterType.IncludeFilter, source, FilterAction.LockFilter)
        self._clearSchematicContextHighlightFilter()
        self._schematicSourceHighlightFilter = filterModule.addFilterClause(FilterType.HighlightFilter, source, FilterAction.LockFilter)

        haveArk = self._arkStatus(source)
        haveFeature = self._featureStatus(source)
        haveSchematic = self._schematicStatus(source)

        self.dock.setSourceContext(source, haveArk, haveFeature, haveSchematic)

    def _attribute(self, feature, fieldName):
        val = feature.attribute(self.project.fieldName(fieldName))
        if val == NULL:
            return None
        else:
            return val

    def _copyFeatureMetadata(self, feature):
        self.metadata.setSiteCode(self._attribute(feature, 'site'))
        self.metadata.setComment(self._attribute(feature, 'comment'))
        self.metadata.setClassCode('cxt')
        self.metadata.setItemId(self.dock.context())
        self.metadata.setSourceCode('cln')
        self.metadata.setSourceClass('cxt')
        self.metadata.setSourceId(self.dock.sourceContext())
        self.metadata.setSourceFile('')

    def _copySourceSchematic(self):
        self.metadata.validate()
        request = self._categoryRequest(self.dock.sourceItemKey(), 'sch')
        fi = self.project.plan.polygonsLayer.getFeatures(request)
        for feature in fi:
            feature.setAttribute(self.project.fieldName('site'), self.metadata.siteCode())
            feature.setAttribute(self.project.fieldName('class'), 'cxt')
            feature.setAttribute(self.project.fieldName('id'), self.dock.context())
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
        self._editSchematic = True
        self.dock.widget.setCurrentIndex(0)
        self.project.iface.setActiveLayer(self.project.plan.polygonsBuffer)
        self.project.iface.actionZoomToLayer().trigger()
        self.project.plan.polygonsBuffer.selectAll()
        self.project.iface.actionNodeTool().trigger()

    def _cloneSourceSchematic(self):
        self._clearSchematicSourceFilters()
        self._copySourceSchematic()
        self._mergeSchematic()
