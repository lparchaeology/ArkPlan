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

import copy
import os

from PyQt4.QtCore import QDir, QFile, QFileInfo, QObject, Qt
from PyQt4.QtGui import QAction, QFileDialog, QIcon, QInputDialog

from qgis.core import (NULL, QgsFeatureRequest, QgsGeometry, QgsLayerTreeModel, QgsMapLayer, QgsMapLayerRegistry,
                       QgsProject, QgsRasterLayer)
from qgis.gui import QgsLayerTreeView

from ArkSpatial.ark.lib import Plugin, Project, utils
from ArkSpatial.ark.lib.core import Collection, CollectionSettings, layers
from ArkSpatial.ark.lib.snapping import LayerSnappingAction

from ArkSpatial.ark.core import Config, Drawing, Item, ItemFeature, ItemFeatureError, Settings, Source
from ArkSpatial.ark.core.enum import DrawingAction, FilterAction, MapAction
from ArkSpatial.ark.gui import (ItemFeatureErrorDialog, LayerTreeMenu, ProjectDialog, ProjectDock, ProjectWizard,
                                SelectDrawingDialog, SelectItemDialog)
from ArkSpatial.ark.map import MapToolIndentifyItems


class ProjectModule(QObject):

    def __init__(self, plugin):
        super(ProjectModule, self).__init__(plugin)

        # Project settings
        self._plugin = plugin  # Plugin()
        # self.projectLayerView = None  # QgsLayerTreeView()
        self.dock = None  # ProjectDock()
        self.initialised = False
        self.metadata = None  # Metadata()

        self.projectGroupIndex = -1
        self.drawingsGroupIndex = -1
        self.drawingsGroupName = ''

        self.geoLayer = None  # QgsRasterLayer()
        self.plan = None  # Collection()
        self.section = None  # Collection()
        self.grid = None  # Collection()
        self.site = None  # Collection()
        self._collections = {}  # {Collection()}

        # Tools
        self.identifyMapTool = None  # MapToolIndentifyItems()

        # Internal variables
        self._mapAction = MapAction.MoveMap
        self._filterAction = FilterAction.ExclusiveHighlightFilter
        self._drawingAction = DrawingAction.NoDrawingAction
        self._layerSnappingAction = None  # LayerSnappingAction()
        self._itemLogPath = ''

    # Create the gui when the plugin is first created
    def initGui(self):
        self.dock = ProjectDock(self._plugin.iface.mainWindow())
        self.dock.initGui(self._plugin.iface, Qt.LeftDockWidgetArea, self._plugin.pluginAction)
        # self.projectLayerView = QgsLayerTreeView()
        # self._layerSnappingAction = LayerSnappingAction(self._plugin.iface, self.projectLayerView)
        # self._plugin.iface.legendInterface().addLegendLayerAction(
        #    self._layerSnappingAction, '', 'arksnap', QgsMapLayer.VectorLayer, True)

        """
        # Create the Layer Model and View
        # TODO Should only show our subgroup but crashes!
        # self.projectLayerModel
        # = QgsLayerTreeModel(QgsProject.instance().layerTreeRoot().findGroup(Config.projectGroupName), self);
        self.projectLayerModel = QgsLayerTreeModel(QgsProject.instance().layerTreeRoot(), self)
        self.projectLayerModel.setFlag(QgsLayerTreeModel.ShowLegend)
        self.projectLayerModel.setFlag(QgsLayerTreeModel.ShowLegendAsTree)
        self.projectLayerModel.setFlag(QgsLayerTreeModel.AllowNodeReorder, True)
        self.projectLayerModel.setFlag(QgsLayerTreeModel.AllowNodeRename, False)
        self.projectLayerModel.setFlag(QgsLayerTreeModel.AllowNodeChangeVisibility)
        self.projectLayerModel.setFlag(QgsLayerTreeModel.AllowLegendChangeState)
        self.projectLayerModel.setFlag(QgsLayerTreeModel.AllowSymbologyChangeState)
        self.projectLayerModel.setAutoCollapseLegendNodes(-1)
        self.projectLayerView.setModel(self.projectLayerModel)
        menuProvider = LayerTreeMenu(self, self.projectLayerView)
        self.projectLayerView.setMenuProvider(menuProvider)
        self.projectLayerView.setCurrentLayer(self._plugin.iface.activeLayer())
        self.projectLayerView.doubleClicked.connect(self._plugin.iface.actionOpenTable().trigger)
        self.projectLayerView.currentLayerChanged.connect(self.mapCanvas().setCurrentLayer)
        self.projectLayerView.currentLayerChanged.connect(self._plugin.iface.setActiveLayer)
        self._plugin.iface.currentLayerChanged.connect(self.projectLayerView.setCurrentLayer)
        self.layerViewAction = self.addDockAction(
            ':/plugins/ark/tree.svg', self.tr(u'Toggle Layer View'), callback=self._toggleLayerView, checkable=True)
        self.layerViewAction.setChecked(True)
        """

        # Add Settings to the toolbar TODO move to end of dock?
        self.addDockSeparator()
        self.addDockAction(':/plugins/ark/settings.svg',
                           self._plugin.tr(u'Project Settings'), self._triggerSettingsDialog)

        # Init the identify tool and add to the toolbar
        self.identifyAction = self.addDockAction(
            ':/plugins/ark/filter/identify.png',
            self._plugin.tr(u'Identify Items'),
            callback=self.triggerIdentifyAction,
            checkable=True
        )
        self.identifyMapTool = MapToolIndentifyItems(self._plugin)
        self.identifyMapTool.setAction(self.identifyAction)

        # Init the Load Item tool and add to the toolbar
        self.showItemAction = self.addDockAction(
            ':/plugins/ark/filter/showContext.png',
            self._plugin.tr(u'Show Item'),
            callback=self._showItem
        )

        # If the project or layers or legend indexes change make sure we stay updated
        self._plugin.legendInterface().groupIndexChanged.connect(self._groupIndexChanged)

    # Load the project settings when project is loaded
    def loadProject(self):
        if Settings.isProjectConfigured():
            self.projectGroupIndex = layers.createLayerGroup(self._plugin.iface, Config.projectGroupName)

            # Load the layer collections
            self._addCollection('grid')
            self._addCollection('plan')
            self._addCollection('section')
            self._addCollection('site')
            self.drawingsGroupName = Config.drawings['context']['layersGroupName']
            if (self.collection('grid').loadCollection()
                    and self.collection('plan').loadCollection()
                    and self.collection('section').loadCollection()
                    and self.collection('site').loadCollection()):

                self.dock.loadProject(self._plugin)

                if self.collection('plan').isLogged():
                    self._itemLogPath = os.path.join(self.collection('plan').projectPath,
                                                     self.collection('plan').settings.collectionPath,
                                                     'log/itemLog.csv')
                    if not QFile.exists(self._itemLogPath):
                        fd = open(self._itemLogPath, 'a')
                        fd.write('timestamp,action,siteCode,classCode,itemId\n')
                        fd.close()

                    # TODO Think of a better way...
                    # self.metadata = Metadata(self.dock.widget.sourceWidget)
                    # self.metadata.metadataChanged.connect(self.updateMapToolAttributes)
            self.initialised = True
            return True
        return False

    # Save the project
    def writeProject(self):
        pass

    # Close the project
    def closeProject(self):
        if self.identifyMapTool.action() and self.identifyMapTool.action().isChecked():
            self._plugin.iface.actionPan().trigger()
        # TODO Unload the drawing tools!
        self.dock.closeProject()
        # self.metadata.metadataChanged.disconnect(self.updateMapToolAttributes)
        # Unload the layers
        for collection in self._collections:
            self._collections[collection].unload()
        del self._collections
        self._collections = {}
        self._plugin.iface.legendInterface().removeLegendLayerAction(self._layerSnappingAction)
        self.initialised = False

    # Unload the module when plugin is unloaded
    def unloadGui(self):
        # Unload the dock
        self.dock.unloadGui()
        del self.dock
        # Reset the initialisation
        self.initialised = False

    def run(self, checked):
        if checked and self.initialised:
            pass
        else:
            self.dock.menuAction().setChecked(False)

    # Project

    def crs(self):
        return self._plugin.iface.mapCanvas().mapSettings().destinationCrs()

    def crsId(self):
        return self.crs().authid()

    def projectFolder(self):
        proj = Project.dir()
        proj.cdUp()
        return proj.absolutePath()

    def configure(self):
        wizard = ProjectWizard(self._plugin.iface.mainWindow())

        ok = wizard.exec_()

        if ok:

            if wizard.newProject():
                if Project.exists():
                    Project.write()
                Project.clear()
                projectFolderPath = os.path.join(wizard.projectFolder(), 'project')
                if not QDir(projectFolderPath).mkpath('.'):
                    return False
                projectFilePath = os.path.join(projectFolderPath, wizard.projectFilename() + '.qgs')
                Project.setFileName(projectFilePath)
                Project.setTitle(wizard.project().projectName())

            Settings.setProjectCode(wizard.project().projectCode())
            Settings.setSiteCode(wizard.project().siteCode())

            self._initialised = Project.write()
            if self._initialised:

                # We always want the site collection
                self._addCollection('site')
                self.collection('site').loadCollection()

                # Temp load of other collection, later do on demand
                self._addCollection('plan')
                self.collection('plan').loadCollection()
                self._addCollection('section')
                self.collection('section').loadCollection()
                self._addCollection('grid')
                self.collection('grid').loadCollection()

                # self._configureDrawing('context')
                # self._configureDrawing('plan')
                # self._configureDrawing('section')

                Settings.setProjectConfigured()

        return ok

    def _triggerSettingsDialog(self):
        if Settings.isProjectConfigured():
            self.showSettingsDialog()
        else:
            self.configure()

    def _configureDrawing(self, grp):
        self.rawDrawingDir(grp).mkpath('.')
        self.georefDrawingDir(grp).mkpath('.')

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

    def _groupIndexChanged(self, oldIndex, newIndex):
        if (oldIndex == self.projectGroupIndex):
            self.projectGroupIndex = newIndex

    def loadGeoLayer(self, geoFile, zoomToLayer=True):
        # TODO Check if already loaded, remove old one?
        self.geoLayer = QgsRasterLayer(geoFile.absoluteFilePath(), geoFile.completeBaseName())
        self.geoLayer.renderer().setOpacity(self.drawingTransparency() / 100.0)
        QgsMapLayerRegistry.instance().addMapLayer(self.geoLayer)
        if (self.drawingsGroupIndex < 0):
            self.drawingsGroupIndex = layers.createLayerGroup(
                self._plugin.iface, self.drawingsGroupName, Config.projectGroupName)
        self._plugin.legendInterface().moveLayer(self.geoLayer, self.drawingsGroupIndex)
        if zoomToLayer:
            self.mapCanvas().setExtent(self.geoLayer.extent())

    def clearDrawings(self):
        if (self.drawingsGroupIndex >= 0):
            self.drawingsLayerTreeGroup().removeAllChildren()

    def drawingsLayerTreeGroup(self):
        if (self.drawingsGroupIndex >= 0):
            return QgsProject.instance().layerTreeRoot().findGroup(self.drawingsGroupName)
        else:
            return None

    def isArkGroup(self, name):
        for collection in self._collections:
            if self._collections[collection].isCollectionGroup(name):
                return True
        return name == Config.projectGroupName or name == self.drawingsGroupName

    def isArkLayer(self, layerId):
        for collection in self._collections:
            if self._collections[collection].isCollectionLayer(layerId):
                return True
        return False

    def _pluginStylesPath(self):
        return os.path.join(self._plugin.pluginPath, 'ark', 'styles')

    def _styleFile(self, layerPath, layerName):
        # First see if the layer itself has a default style saved
        filePath = layerPath + '/' + layerName + '.qml'
        if QFile.exists(filePath):
            return filePath
        # Next see if the layer name has a style in the styles folder (which may
        # be a special folder, the site folder or the plugin folder)
        filePath = Settings.stylePath() + '/' + layerName + '.qml'
        if QFile.exists(filePath):
            return filePath
        # Finally, check the plugin folder for the default style
        filePath = self._pluginStylesPath() + '/' + layerName + '.qml'
        if QFile.exists(filePath):
            return filePath
        # If we didn't find that then something is wrong!
        return ''

    def _addCollection(self, collection):
        config = Config.collections[collection]
        path = config['path']
        bufferPath = path + '/buffer'
        logPath = path + '/log'

        config['collection'] = collection
        config['crs'] = self.crs()
        config['parentGroupName'] = Config.projectGroupName

        for layer in config['layers']:
            name = layer['name']
            layer['fields'] = config['fields']
            layer['multi'] = config['multi']
            layer['crs'] = self.crs()
            layer['path'] = layers.shapeFilePath(path, name)
            layer['stylePath'] = layers.styleFilePath(self._pluginStylesPath(), name)
            layer['buffer'] = config['buffer']
            if config['buffer']:
                bufferName = name + Config.bufferSuffix
                layer['bufferName'] = bufferName
                layer['bufferName'] = bufferName
                layer['bufferPath'] = layers.shapeFilePath(bufferPath, bufferName)
            else:
                layer['bufferName'] = ''
                layer['bufferPath'] = ''
            layer['log'] = config['log']
            if config['log']:
                logName = name + Config.logSuffix
                layer['logName'] = logName
                layer['logPath'] = layers.shapeFilePath(logPath, logName)
            else:
                layer['logName'] = ''
                layer['logPath'] = ''

        settings = CollectionSettings.fromArray(config)
        self._collections[collection] = Collection(self._plugin.iface, self.projectFolder(), settings)

    def addDockSeparator(self):
        self.dock.toolbar.addSeparator()

    def addDockAction(self, iconPath, text, callback=None, enabled=True, checkable=False, tip=None, whatsThis=None):
        action = QAction(QIcon(iconPath), text, self.dock)
        if callback is not None:
            action.triggered.connect(callback)
        action.setEnabled(enabled)
        action.setCheckable(checkable)
        if tip is not None:
            action.setStatusTip(tip)
        if whatsThis is not None:
            action.setWhatsThis(whatsThis)
        self.dock.toolbar.addAction(action)
        # self.actions.append(action)
        return action

    def collection(self, collection):
        if collection in self._collections:
            return self._collections[collection]
        return None

    # Identify Tool

    def triggerIdentifyAction(self, checked):
        if checked:
            self.mapCanvas().setMapTool(self.identifyMapTool)
        else:
            self.mapCanvas().unsetMapTool(self.identifyMapTool)

    # Show Items Tool

    def _showItem(self):
        classCodes = sorted(set(self.collection('plan').uniqueValues('class')))
        dialog = SelectItemDialog(Settings.siteCodes(), Settings.siteCode(),
                                  classCodes, self._plugin.iface.mainWindow())
        if dialog.exec_():
            self.drawingModule.showItem(dialog.item(), dialog.loadDrawings(), dialog.zoomToItem())

    # Plan Tools

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
                self._plugin.loadGeoLayer(geoFile)

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
            self._plugin.loadGeoLayer(drawing, zoomToDrawing)

    def loadSourceDrawings(self, item, clearDrawings=False):
        if item.isInvalid():
            return
        sourceKeys = set()
        sourceKeys.add(item)
        itemRequest = item.featureRequest()
        for feature in self.collection('plan').layer('polygons').getFeatures(itemRequest):
            source = Source(feature)
            if source.item().isValid():
                sourceKeys.add(source.item())
        for feature in self.collection('plan').layer('lines').getFeatures(itemRequest):
            source = Source(feature)
            if source.item.isValid():
                sourceKeys.add(source.item())
        for feature in self.collection('plan').layer('points').getFeatures(itemRequest):
            source = Source(feature)
            if source.item().isValid():
                sourceKeys.add(source.item())
        if clearDrawings and len(sourceKeys) > 0:
            self._plugin.clearDrawings()
        for sourceKey in sorted(sourceKeys):
            self.loadDrawing(sourceKey)

    def _featureNameChanged(self, featureName):
        self.metadata.setName(featureName)
        self.updateMapToolAttributes()

    # Layer Methods

    def mergeBuffers(self):
        self._mergeBuffers(self.collection('plan'))
        self._mergeBuffers(self.collection('section'))
        self._mergeBuffers(self.collection('site'))

    def _mergeBuffers(self, collection):
        # Check the layers are writable
        name = collection.settings.collectionGroupName
        if not collection.isWritable():
            self._plugin.showCriticalMessage(
                name + ' layers are not writable! Please correct the permissions and log out.', 0)
            return

        # Check the buffers contain valid data
        errors = self._preMergeBufferCheck(collection.buffer('points'))
        errors.extend(self._preMergeBufferCheck(collection.buffer('lines')))
        errors.extend(self._preMergeBufferCheck(collection.buffer('polygons')))
        if len(errors) > 0:
            dialog = ItemFeatureErrorDialog()
            dialog.loadErrors(errors)
            dialog.exec_()
            if not dialog.ignoreErrors():
                return

        # Update the audit attributes
        timestamp = utils.timestamp()
        user = Settings.userFullName()
        self._preMergeBufferUpdate(collection.buffer('points'), timestamp, user)
        self._preMergeBufferUpdate(collection.buffer('lines'), timestamp, user)
        self._preMergeBufferUpdate(collection.buffer('polygons'), timestamp, user)

        # Finally actually merge the data
        if collection.mergeBuffers('Merge data', timestamp):
            self._plugin.showInfoMessage(name + ' data successfully merged.')
            # TODO pass current Item...
            self._logItemAction(Item(), 'Merge Buffers', timestamp)
            # TODO Signal out layers merged for schematic dock to catch
            # if self._editSchematic:
            #     self._editSchematic = False
            #     self.dock.activateSchematicCheck()
            #     self._findContext()
        else:
            self._plugin.showCriticalMessage(
                name + ' data merge failed! Some data has not been saved, please check your data.', 5)

    def _preMergeBufferCheck(self, layer):
        errors = []
        row = 0
        for feature in layer.getFeatures():
            # Set up the error template
            error = ItemFeatureError()
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
        self.collection('plan').resetBuffers('Clear Buffers')
        self.collection('section').resetBuffers('Clear Buffers')
        self.collection('site').resetBuffers('Clear Buffers')
        # TODO Signal out layers reset for schematic dock to catch
        # if self._editSchematic:
        #     self._editSchematic = False
        #     self.dock.activateSchematicCheck()

    def _confirmDelete(self, itemId, title='Confirm Delete Item', label=None):
        if not label:
            label = 'This action ***DELETES*** item ' + \
                str(itemId) + ' from the saved data.\n\nPlease enter the item ID to confirm.'
        confirm, ok = QInputDialog.getText(None, title, label, text='')
        return ok and confirm == str(itemId)

    def _logItemAction(self, item, action, timestamp=None):
        if self.collection('plan').settings.log:
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
        if self.collection('plan').moveFeatureRequestToBuffers(request, action, timestamp):
            self._logItemAction(item, action, timestamp)
            self._metadataFromBuffers(item)

    def deleteItem(self, item):
        if self._confirmDelete(item.itemId(), 'Confirm Delete Item'):
            request = item.featureRequest()
            timestamp = utils.timestamp()
            action = 'Delete Item'
            if self.collection('plan').deleteFeatureRequest(request, action, timestamp):
                self._logItemAction(item, action, timestamp)

    def applyItemActions(self,
                         item,
                         mapAction=MapAction.NoMapAction,
                         filterAction=FilterAction.NoFilterAction,
                         drawingAction=DrawingAction.NoDrawingAction):
        if drawingAction != DrawingAction.NoDrawingAction:
            self.loadSourceDrawings(item, drawingAction == DrawingAction.LoadDrawings)

        if filterAction != FilterAction.NoFilterAction:
            self._plugin.filter().applyItemAction(item, filterAction)

        if mapAction == MapAction.ZoomMap:
            self._zoomToItem(item)
        elif mapAction == MapAction.PanMap:
            self._panToItem(item)
        elif mapAction == MapAction.MoveMap:
            self._moveToItem(item)
        self._plugin.mapCanvas().refresh()

    def showItem(self, item, loadDrawings=True, zoom=True):
        self._plugin.showMessage('Loading ' + item.itemLabel())
        self._plugin.filter().filterItem(item)
        if loadDrawings:
            self.loadSourceDrawings(item, True)
        if zoom:
            self._zoomToItem(item)

    def panToItem(self, item, highlight=False):
        if highlight:
            self._plugin.filter().highlightItem(item)
        self._panToItem(item)
        self._plugin.mapCanvas().refresh()

    def zoomToItem(self, item, highlight=False):
        if highlight:
            self._plugin.filter().highlightItem(item)
        self._zoomToItem(item)
        self._plugin.mapCanvas().refresh()

    def moveToItem(self, item, highlight=False):
        ret = -1
        if highlight:
            ret = self._plugin.filter().highlightItem(item)
        self._moveToItem(item)
        self._plugin.mapCanvas().refresh()
        return ret

    def _moveToItem(self, item):
        self._moveToExtent(self.itemExtent(item))

    def _moveToExtent(self, extent):
        if extent is None or extent.isNull() or extent.isEmpty():
            return
        mapExtent = self._plugin.mapCanvas().extent()
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
        self._plugin.mapCanvas().setCenter(extent.center())

    def _zoomToItem(self, item):
        self._zoomToExtent(self.itemExtent(item))

    def _zoomToExtent(self, extent):
        if extent is None or extent.isNull() or extent.isEmpty():
            return
        extent.scale(1.05)
        self._plugin.mapCanvas().setExtent(extent)

    def filterItem(self, item):
        self._plugin.filter().filterItem(item)
        self._plugin.mapCanvas().refresh()

    def excludeFilterItem(self, item):
        self._plugin.filter().excludeItem(item)
        self._plugin.mapCanvas().refresh()

    def highlightItem(self, item):
        self._plugin.filter().highlightItem(item)
        self._plugin.mapCanvas().refresh()

    def addHighlightItem(self, item):
        self._plugin.filter().addHighlightItem(item)
        self._plugin.mapCanvas().refresh()

    def itemExtent(self, item):
        requestKey = self._plugin.data().nodesItem(item)
        request = requestKey.featureRequest()
        points = self._requestAsLayer(request, self.collection('plan').layer('points'), 'points')
        lines = self._requestAsLayer(request, self.collection('plan').layer('lines'), 'lines')
        polygons = self._requestAsLayer(request, self.collection('plan').layer('polygons'), 'polygons')
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
        features = layers.getAllFeaturesRequest(request, self.collection('plan').layer('lines'))
        lst = []
        for feature in features:
            lst.append(ItemFeature(feature))
        lst.sort()
        return lst

    def _sectionLineGeometry(self, item):
        if item and item.isValid():
            request = self._categoryRequest(item, 'sln')
            features = layers.getAllFeaturesRequest(request, self.collection('plan').layer('lines'))
            for feature in features:
                return QgsGeometry(feature.geometry())
        return QgsGeometry()

    def _metadataFromBuffers(self, item):
        feature = self._getFeature(self.collection('plan').buffer('polygons'), item, 'sch')
        if feature:
            self.metadata.fromFeature(feature)
            return
        feature = self._getFeature(self.collection('plan').buffer('polygons'), item, 'scs')
        if feature:
            self.metadata.fromFeature(feature)
            return
        feature = self._getFeature(self.collection('plan').buffer('polygons'), item)
        if feature:
            self.metadata.fromFeature(feature)
            return
        feature = self._getFeature(self.collection('plan').buffer('lines'), item)
        if feature:
            self.metadata.fromFeature(feature)
            return
        feature = self._getFeature(self.collection('plan').buffer('points'), item)
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
