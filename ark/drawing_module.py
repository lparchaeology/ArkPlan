# -*- coding: utf-8 -*-
"""
/***************************************************************************
                                ARKspatial
                    A QGIS plugin for Archaeological Recording.
        Part of the Archaeological Recording Kit by L - P : Archaeology
                        http://ark.lparchaeology.com
                              -------------------
        copyright            : 2017 by L - P : Heritage LLP
        email                : ark@lparchaeology.com
        copyright            : 2017 by John Layt
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

import bisect
import copy
import os

from PyQt4.QtCore import QDir, QFile, QFileInfo, QObject, Qt
from PyQt4.QtGui import QFileDialog, QInputDialog

from qgis.core import NULL, QgsFeatureRequest, QgsGeometry

from ArkSpatial.ark.lib import utils
from ArkSpatial.ark.lib.core import layers
from ArkSpatial.ark.lib.gui import TableDialog

from ArkSpatial.ark.core import Config, Drawing, Feature, FeatureError, Item, Source, Settings
from ArkSpatial.ark.core.enum import DrawingAction, FilterAction, MapAction, SearchStatus
from ArkSpatial.ark.georef import GeorefDialog
from ArkSpatial.ark.gui import FeatureErrorDialog, DrawingDock, SnappingDock, SelectDrawingDialog


class DrawingModule(QObject):

    def __init__(self, plugin):
        super(DrawingModule, self).__init__(plugin)

        # Project settings
        self.plugin = plugin  # Plugin()
        self.dock = None  # DrawingDock()
        self.initialised = False
        self.metadata = None  # Metadata()

        # Internal variables
        self._mapAction = MapAction.MoveMap
        self._filterAction = FilterAction.ExclusiveHighlightFilter
        self._drawingAction = DrawingAction.NoDrawingAction
        self._itemLogPath = ''

    # Create the gui when the plugin is first created
    def initGui(self):
        self.dock = DrawingDock(self.plugin.iface.mainWindow())
        action = self.plugin.addDockAction(
            ':/plugins/ark/plan/drawPlans.png',
            self.tr(u'Drawing Tools'),
            callback=self.run,
            checkable=True
        )
        self.dock.initGui(self.plugin.iface, Qt.RightDockWidgetArea, action)

        self.dock.loadAnyFileSelected.connect(self._loadAnyPlan)
        self.dock.loadRawFileSelected.connect(self._loadRawPlan)
        self.dock.loadGeoFileSelected.connect(self._loadGeoPlan)

        self.dock.resetSelected.connect(self.resetBuffers)
        self.dock.mergeSelected.connect(self.mergeBuffers)

        self.snapDock = SnappingDock(self.plugin.iface.mainWindow())
        action = self.plugin.addDockAction(
            ':/plugins/ark/snapIntersections.png',
            self.tr(u'Snapping Tools'),
            callback=self.runSnapping,
            checkable=True
        )
        self.snapDock.initGui(self.plugin.iface, Qt.LeftDockWidgetArea, action)

    # Load the project settings when project is loaded
    def loadProject(self):
        # Assume layers are loaded and filters cleared
        self.dock.loadProject(self.plugin)
        self.snapDock.loadProject(self.plugin)

        if self.collection().isLogged():
            self._itemLogPath = os.path.join(self.collection().projectPath,
                                             self.collection().settings.collectionPath,
                                             'log/itemLog.csv')
            if not QFile.exists(self._itemLogPath):
                fd = open(self._itemLogPath, 'a')
                fd.write('timestamp,action,siteCode,classCode,itemId\n')
                fd.close()

        # TODO Think of a better way...
        # self.metadata = Metadata(self.dock.widget.sourceWidget)
        # self.metadata.metadataChanged.connect(self.updateMapToolAttributes)

        self.initialised = True

    # Save the project
    def writeProject(self):
        pass

    # Close the project
    def closeProject(self):
        # TODO Unload the drawing tools!
        self.snapDock.closeProject()
        self.dock.closeProject()
        # self.metadata.metadataChanged.disconnect(self.updateMapToolAttributes)
        self.initialised = False

    # Unload the module when plugin is unloaded
    def unloadGui(self):
        # Unload the dock
        self.snapDock.unloadGui()
        del self.snapDock
        self.dock.unloadGui()
        del self.dock
        # Reset the initialisation
        self.initialised = False

    def run(self, checked):
        if checked and self.initialised:
            self.plugin.filterModule.showDock()
        else:
            self.dock.menuAction().setChecked(False)

    def runSnapping(self, checked):
        if checked and self.initialised:
            pass
        else:
            self.snapDock.menuAction().setChecked(False)

    # Plan Tools

    def collection(self):
        return self.plugin.collection('plan')

    def _setDrawing(self, pmd):
        self.metadata.setSiteCode(pmd.siteCode)
        self.metadata.setClassCode(pmd.sourceClass)
        if pmd.sourceId > 0:
            self.metadata.setItemId(pmd.sourceId)
            self.metadata.setSourceId(pmd.sourceId)
        self.metadata.setSourceCode('drawing')
        self.metadata.setSourceClass(pmd.sourceClass)
        self.metadata.setSourceFile(pmd.filename)
        self.metadata.setEditor(Settings.userFullName())

    def _loadAnyPlan(self):
        filePaths = QFileDialog.getOpenFileNames(
            self.dock, caption='Georeference Any File', filter='Images (*.png *.xpm *.jpg)')
        for filePath in filePaths:
            self.georeferencePlan(QFileInfo(filePath), 'free')

    def _loadRawPlan(self):
        dialog = SelectDrawingDialog('context', Settings.siteCode())
        if (dialog.exec_()):
            for filePath in dialog.selectedFiles():
                self.georeferencePlan(QFileInfo(filePath))

    def _loadGeoPlan(self):
        dialog = SelectDrawingDialog('context', Settings.siteCode(), True)
        if (dialog.exec_()):
            for filePath in dialog.selectedFiles():
                geoFile = QFileInfo(filePath)
                self._setDrawing(Drawing(geoFile))
                self.plugin.loadGeoLayer(geoFile)

    def loadDrawing(self, item, zoomToDrawing=True):
        if not Config.classCodes[item.classCode()]['drawing']:
            return
        drawingDir = Settings.georefDrawingDir(item.classCode())
        drawingDir.setFilter(QDir.Files | QDir.NoDotAndDotDot)
        name = item.name()
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
            self._setDrawing(Drawing(drawing))
            self.plugin.loadGeoLayer(drawing, zoomToDrawing)

    def loadSourceDrawings(self, item, clearDrawings=False):
        if item.isInvalid():
            return
        sourceKeys = set()
        sourceKeys.add(item)
        itemRequest = item.featureRequest()
        for feature in self.collection().layer('polygons').getFeatures(itemRequest):
            source = Source(feature)
            if source.item().isValid():
                sourceKeys.add(source.item())
        for feature in self.collection().layer('lines').getFeatures(itemRequest):
            source = Source(feature)
            if source.item.isValid():
                sourceKeys.add(source.item())
        for feature in self.collection().layer('points').getFeatures(itemRequest):
            source = Source(feature)
            if source.item().isValid():
                sourceKeys.add(source.item())
        if clearDrawings and len(sourceKeys) > 0:
            self.plugin.clearDrawings()
        for sourceKey in sorted(sourceKeys):
            self.loadDrawing(sourceKey)

    def _featureNameChanged(self, featureName):
        self.metadata.setName(featureName)
        self.updateMapToolAttributes()

    # Georeference Tools

    def georeferencePlan(self, sourceFile, mode='name'):
        drawings = Config.drawings
        for drawing in drawings:
            drawings[drawing]['raw'] = Settings.rawDrawingDir(drawing)
            drawings[drawing]['geo'] = Settings.georefDrawingDir(drawing)
            drawings[drawing]['suffix'] = '_r'
            drawings[drawing]['crs'] = self.plugin.projectCrs().authid()
            drawings[drawing]['grid'] = self.plugin.grid.layer('points')
            drawings[drawing]['local_x'] = 'local_x'
            drawings[drawing]['local_y'] = 'local_y'
        georefDialog = GeorefDialog(drawings)
        if georefDialog.loadImage(sourceFile) and georefDialog.exec_():
            geoFile = georefDialog.geoFile()
            md = georefDialog.metadata()
            md.filename = geoFile.fileName()
            self._setDrawing(md)
            self.plugin.loadGeoLayer(geoFile)

    # Layer Methods

    def mergeBuffers(self):
        self._mergeBuffers(self.plugin.plan)
        self._mergeBuffers(self.plugin.section)
        self._mergeBuffers(self.plugin.site)

    def _mergeBuffers(self, collection):
        # Check the layers are writable
        name = collection.settings.collectionGroupName
        if not collection.isWritable():
            self.plugin.showCriticalMessage(
                name + ' layers are not writable! Please correct the permissions and log out.', 0)
            return

        # Check the buffers contain valid data
        errors = self._preMergeBufferCheck(collection.buffer('points'))
        errors.extend(self._preMergeBufferCheck(collection.buffer('lines')))
        errors.extend(self._preMergeBufferCheck(collection.buffer('polygons')))
        if len(errors) > 0:
            dialog = FeatureErrorDialog()
            dialog.loadErrors(errors)
            dialog.exec_()
            if not dialog.ignoreErrors():
                return

        # Update the audit attributes
        timestamp = utils.timestamp()
        user = self.metadata.editor()
        self._preMergeBufferUpdate(collection.buffer('points'), timestamp, user)
        self._preMergeBufferUpdate(collection.buffer('lines'), timestamp, user)
        self._preMergeBufferUpdate(collection.buffer('polygons'), timestamp, user)

        # Finally actually merge the data
        if collection.mergeBuffers('Merge data', Settings.logUpdates(), timestamp):
            self.plugin.showInfoMessage(name + ' data successfully merged.')
            self._logItemAction(self.metadata.feature().item(), 'Merge Buffers', timestamp)
            if self._editSchematic:
                self._editSchematic = False
                self.dock.activateSchematicCheck()
                self._findContext()
        else:
            self.plugin.showCriticalMessage(
                name + ' data merge failed! Some data has not been saved, please check your data.', 5)

    def _preMergeBufferCheck(self, layer):
        errors = []
        row = 0
        for feature in layer.getFeatures():
            # Set up the error template
            error = FeatureError()
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
                # Ignore the last error, it is just a total
                for err in geomErrs[:-1]:
                    error.message = err.what()
                    errors.append(copy.deepcopy(error))
            # Key attributes that must always be populated
            if self._isEmpty(feature.attribute('site')):
                error.field = 'site'
                error.message = 'Site Code is required'
                errors.append(copy.deepcopy(error))
            if self._isEmpty(feature.attribute('class')):
                error.field = 'class'
                error.message = 'Class Code is required'
                errors.append(copy.deepcopy(error))
            if self._isEmpty(feature.attribute('id')):
                error.field = 'id'
                error.message = 'ID is required'
                errors.append(copy.deepcopy(error))
            if self._isEmpty(feature.attribute('category')):
                error.field = 'category'
                error.message = 'Category is required'
                errors.append(copy.deepcopy(error))
            if self._isEmpty(feature.attribute('source_cd')):
                error.field = 'source_cd'
                error.message = 'Source Code is required'
                error.ignore = True
                # errors.append(copy.deepcopy(error))
            # Source attributes required depend on the source type
            if feature.attribute('source_cd') == 'creator' or feature.attribute('source_cd') == 'other':
                if self._isEmpty(feature.attribute('comment')):
                    error.field = 'source_cd'
                    error.message = 'Comment is required for Source type of Creator or Other'
                    error.ignore = True
                    # errors.append(copy.deepcopy(error))
            elif feature.attribute('source_cd') == 'survey':
                if self._isEmpty(feature.attribute('file')):
                    error.field = 'source_cd'
                    error.message = 'Filename is required for Source type of Survey'
                    error.ignore = True
                    # errors.append(copy.deepcopy(error))
            else:  # 'drw', 'unc', 'skt', 'cln', 'mod', 'inf'
                if ((feature.attribute('source_cd') == 'drawing' or feature.attribute('source_cd') == 'unchecked')
                        and self._isEmpty(feature.attribute('file'))):
                    error.field = 'source_cd'
                    error.message = 'Filename is required for Source type of Drawing'
                    error.ignore = True
                    # errors.append(copy.deepcopy(error))
                if (self._isEmpty(feature.attribute('source_cl')) or self._isEmpty(feature.attribute('source_id'))):
                    error.field = 'source_cd'
                    error.message = 'Source Class and ID is required'
                    error.ignore = True
                    # errors.append(copy.deepcopy(error))
        return errors

    def _isEmpty(self, val):
        if val is None or val == NULL:
            return True
        if isinstance(val, str) and (val == '' or val.strip() == ''):
            return True
        return False

    def _preMergeBufferUpdate(self, layer, timestamp, user):
        createdIdx = layer.fieldNameIndex('created')
        creatorIdx = layer.fieldNameIndex('creator')
        modifiedIdx = layer.fieldNameIndex('modified')
        modifierIdx = layer.fieldNameIndex('modifier')
        for feature in layer.getFeatures():
            if self._isEmpty(feature.attribute('created')):
                layer.changeAttributeValue(feature.id(), createdIdx, timestamp)
                layer.changeAttributeValue(feature.id(), creatorIdx, user)
            else:
                layer.changeAttributeValue(feature.id(), modifiedIdx, timestamp)
                layer.changeAttributeValue(feature.id(), modifierIdx, user)

    def resetBuffers(self):
        self.collection().resetBuffers('Clear Buffers')
        if self._editSchematic:
            self._editSchematic = False
            self.dock.activateSchematicCheck()

    # Drawing tools

    def _confirmDelete(self, itemId, title='Confirm Delete Item', label=None):
        if not label:
            label = 'This action ***DELETES*** item ' + \
                str(itemId) + ' from the saved data.\n\nPlease enter the item ID to confirm.'
        confirm, ok = QInputDialog.getText(None, title, label, text='')
        return ok and confirm == str(itemId)

    def _logItemAction(self, item, action, timestamp=None):
        if self.collection().settings.log:
            if not timestamp:
                timestamp = utils.timestamp()
            fd = open(self._itemLogPath, 'a')
            fd.write(utils.doublequote(timestamp) + ',' + utils.doublequote(action) + ',' + item.toCsv() + '\n')
            fd.close()

    def editInBuffers(self, item):
        # if self._confirmDelete(item.itemId(), 'Confirm Move Item'):
        request = item.featureRequest()
        timestamp = utils.timestamp()
        action = 'Edit Item'
        if self.collection().moveFeatureRequestToBuffers(request, action, Settings.logUpdates(), timestamp):
            self._logItemAction(item, action, timestamp)
            self._metadataFromBuffers(item)

    def deleteItem(self, item):
        if self._confirmDelete(item.itemId(), 'Confirm Delete Item'):
            request = item.featureRequest()
            timestamp = utils.timestamp()
            action = 'Delete Item'
            if self.collection().deleteFeatureRequest(request, action, Settings.logUpdates(), timestamp):
                self._logItemAction(item, action, timestamp)

    def applyItemActions(self,
                         item,
                         mapAction=MapAction.NoMapAction,
                         filterAction=FilterAction.NoFilterAction,
                         drawingAction=DrawingAction.NoDrawingAction):
        if drawingAction != DrawingAction.NoDrawingAction:
            self.loadSourceDrawings(item, drawingAction == DrawingAction.LoadDrawings)

        if filterAction != FilterAction.NoFilterAction:
            self.plugin.filterModule.applyItemAction(item, filterAction)

        if mapAction == MapAction.ZoomMap:
            self._zoomToItem(item)
        elif mapAction == MapAction.PanMap:
            self._panToItem(item)
        elif mapAction == MapAction.MoveMap:
            self._moveToItem(item)
        self.plugin.mapCanvas().refresh()

    def showItem(self, item, loadDrawings=True, zoom=True):
        self.plugin.showMessage('Loading ' + item.itemLabel())
        self.plugin.filterModule.filterItem(item)
        if loadDrawings:
            self.loadSourceDrawings(item, True)
        if zoom:
            self._zoomToItem(item)

    def panToItem(self, item, highlight=False):
        if highlight:
            self.plugin.filterModule.highlightItem(item)
        self._panToItem(item)
        self.plugin.mapCanvas().refresh()

    def zoomToItem(self, item, highlight=False):
        if highlight:
            self.plugin.filterModule.highlightItem(item)
        self._zoomToItem(item)
        self.plugin.mapCanvas().refresh()

    def moveToItem(self, item, highlight=False):
        ret = -1
        if highlight:
            ret = self.plugin.filterModule.highlightItem(item)
        self._moveToItem(item)
        self.plugin.mapCanvas().refresh()
        return ret

    def _moveToItem(self, item):
        self._moveToExtent(self.itemExtent(item))

    def _moveToExtent(self, extent):
        if extent is None or extent.isNull() or extent.isEmpty():
            return
        mapExtent = self.plugin.mapCanvas().extent()
        if (extent.width() > mapExtent.width() or extent.height() > mapExtent.height()
                or extent.width() * extent.height() > mapExtent.width() * mapExtent.height()):
            self._zoomToExtent(extent)
        else:
            self._panToExtent(extent)

    def _panToItem(self, item):
        self._panToExtent(self.itemExtent(item))

    def _panToExtent(self, extent):
        if extent is None or extent.isNull() or extent.isEmpty():
            return
        self.plugin.mapCanvas().setCenter(extent.center())

    def _zoomToItem(self, item):
        self._zoomToExtent(self.itemExtent(item))

    def _zoomToExtent(self, extent):
        if extent is None or extent.isNull() or extent.isEmpty():
            return
        extent.scale(1.05)
        self.plugin.mapCanvas().setExtent(extent)

    def filterItem(self, item):
        self.plugin.filterModule.filterItem(item)
        self.plugin.mapCanvas().refresh()

    def excludeFilterItem(self, item):
        self.plugin.filterModule.excludeItem(item)
        self.plugin.mapCanvas().refresh()

    def highlightItem(self, item):
        self.plugin.filterModule.highlightItem(item)
        self.plugin.mapCanvas().refresh()

    def addHighlightItem(self, item):
        self.plugin.filterModule.addHighlightItem(item)
        self.plugin.mapCanvas().refresh()

    def itemExtent(self, item):
        requestKey = self.plugin.data.nodesItem(item)
        request = requestKey.featureRequest()
        points = self._requestAsLayer(request, self.collection().layer('points'), 'points')
        lines = self._requestAsLayer(request, self.collection().layer('lines'), 'lines')
        polygons = self._requestAsLayer(request, self.collection().layer('polygons'), 'polygons')
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
            if extent is None:
                extent = layerExtent
            else:
                extent.combineExtentWith(layerExtent)
        return extent

    def _sectionItemList(self, siteCode):
        # TODO in 2.14 use addOrderBy()
        request = self._classItemsRequest(siteCode, 'sec')
        features = layers.getAllFeaturesRequest(request, self.collection().layer('lines'))
        lst = []
        for feature in features:
            lst.append(Feature(feature))
        lst.sort()
        return lst

    def _sectionLineGeometry(self, item):
        if item and item.isValid():
            request = self._categoryRequest(item, 'sln')
            features = layers.getAllFeaturesRequest(request, self.collection().layer('lines'))
            for feature in features:
                return QgsGeometry(feature.geometry())
        return QgsGeometry()

    def _sectionChanged(self, item):
        try:
            self.mapTools['scs'].setSectionGeometry(self._sectionLineGeometry(item))
        except Exception:
            pass

    def _metadataFromBuffers(self, item):
        feature = self._getFeature(self.collection().buffer('polygons'), item, 'sch')
        if feature:
            self.metadata.fromFeature(feature)
            return
        feature = self._getFeature(self.collection().buffer('polygons'), item, 'scs')
        if feature:
            self.metadata.fromFeature(feature)
            return
        feature = self._getFeature(self.collection().buffer('polygons'), item)
        if feature:
            self.metadata.fromFeature(feature)
            return
        feature = self._getFeature(self.collection().buffer('lines'), item)
        if feature:
            self.metadata.fromFeature(feature)
            return
        feature = self._getFeature(self.collection().buffer('points'), item)
        if feature:
            self.metadata.fromFeature(feature)

    def _getFeature(self, layer, item, category=''):
        req = None
        if category:
            req = self._categoryRequest(item, 'sch')
        else:
            req = self._itemRequest(item)
        try:
            return layer.getFeatures(req).next()
        except StopIteration:
            return None
        return None

    # Feature Request Methods

    def _eqClause(self, field, value):
        return utils.eqClause(field, value)

    def _neClause(self, field, value):
        return utils.neClause(field, value)

    def _categoryClause(self, category):
        return self._eqClause('category', category)

    def _notCategoryClause(self, category):
        return self._neClause('category', category)

    def _featureRequest(self, expr):
        request = QgsFeatureRequest()
        request.setFilterExpression(expr)
        return request

    def _itemRequest(self, item):
        return self._featureRequest(item.filterClause())

    def _categoryRequest(self, item, category):
        return self._featureRequest(item.filterClause() + ' and ' + self._categoryClause(category))

    def _notCategoryRequest(self, item, category):
        return self._featureRequest(item.filterClause() + ' and ' + self._notCategoryClause(category))

    def _classItemsRequest(self, siteCode, classCode):
        return self._featureRequest(self._eqClause('site', siteCode) + ' and ' + self._eqClause('class', classCode))
