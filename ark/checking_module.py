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

from qgis.PyQt.QtCore import QObject, Qt

from ArkSpatial.ark.lib import utils
from ArkSpatial.ark.lib.core import layers
from ArkSpatial.ark.lib.gui import TableDialog

from ArkSpatial.ark.core import Drawing, Item, Module, Settings, Source
from ArkSpatial.ark.core.enum import DrawingAction, FilterAction, MapAction, SearchStatus
from ArkSpatial.ark.gui import CheckingDock


class CheckingModule(Module):

    def __init__(self, plugin):
        super(CheckingModule, self).__init__(plugin)

        # Internal variables
        self._editSchematic = False
        self._mapAction = MapAction.MoveMap
        self._filterAction = FilterAction.ExclusiveHighlightFilter
        self._drawingAction = DrawingAction.NoDrawingAction
        self._itemLogPath = ''

    # Create the gui when the plugin is first created
    def initGui(self):
        dock = CheckingDock(self._plugin.iface.mainWindow())
        action = self._plugin.project().addDockAction(
            ':/plugins/ark/plan/schematicReport.svg',
            self.tr(u'Checking Tools'),
            callback=self.run,
            checkable=True
        )
        self._initDockGui(dock, Qt.RightDockWidgetArea, action)

        self._dock.loadArkData.connect(self._loadArkData)
        self._dock.mapActionChanged.connect(self._mapActionChanged)
        self._dock.filterActionChanged.connect(self._filterActionChanged)
        self._dock.drawingActionChanged.connect(self._drawingActionChanged)
        self._dock.openContextData.connect(self._openContextData)
        self._dock.openSourceContextData.connect(self._openSourceContextData)
        self._dock.findContextSelected.connect(self._findContext)
        self._dock.firstContextSelected.connect(self._firstContext)
        self._dock.lastContextSelected.connect(self._lastContext)
        self._dock.prevContextSelected.connect(self._prevContext)
        self._dock.nextContextSelected.connect(self._nextContext)
        self._dock.prevMissingSelected.connect(self._prevMissing)
        self._dock.nextMissingSelected.connect(self._nextMissing)
        self._dock.schematicReportSelected.connect(self._showSchematicReport)
        self._dock.editContextSelected.connect(self._editSchematicContext)
        self._dock.deleteSectionSchematicSelected.connect(self._deleteSectionSchematic)
        self._dock.findSourceSelected.connect(self._findSource)
        self._dock.copySourceSelected.connect(self._editSourceSchematic)
        self._dock.cloneSourceSelected.connect(self._cloneSourceSchematic)
        self._dock.editSourceSelected.connect(self._editSource)
        self._dock.contextChanged.connect(self._clearSchematicFilters)
        self._dock.resetSchematicSelected.connect(self._resetSchematic)

        self._plugin.filter().filterSetCleared.connect(self._clearSchematic)

    # Load the project settings when project is loaded
    def loadProject(self):
        # Assume layers are loaded and filters cleared
        self._dock.loadProject(self._plugin)
        self._plugin.data().dataLoaded.connect(self._dock.activateArkData)
        self._initialised = True

    # Save the project
    def writeProject(self):
        # We don't want to save the schematic search or filters
        self._clearSchematic()

    # Close the project
    def closeProject(self):
        self._clearSchematicFilters()
        # TODO Unload the drawing tools!
        self._dock.closeProject()
        # self._plugin.data().dataLoaded.disconnect(self._dock.activateArkData)
        self._initialised = False

    def run(self, checked):
        if checked and self._initialised:
            self._plugin.drawing().showDock(False)
        else:
            self.showDock(False)

    # Plan Tools

    def collection(self):
        return self._plugin.project().collection('plan')

    # SchematicDock methods

    def _loadArkData(self):
        self._plugin.data().loadData()

    def _mapActionChanged(self, mapAction):
        self._mapAction = mapAction

    def _filterActionChanged(self, filterAction):
        self._filterAction = filterAction

    def _drawingActionChanged(self, drawingAction):
        self._drawingAction = drawingAction

    def _openContextData(self):
        self.openItemInArk(self._dock.contextItem())

    def _openSourceContextData(self):
        self.openItemInArk(self._dock.sourceItem())

    def openItemInArk(self, item):
        self._plugin.data().openItem(item)

    def _resetSchematic(self):
        self._clearSchematic()
        self._dock.activateSchematicCheck()

    def _clearSchematic(self):
        self._clearSchematicFilters()
        self._dock.resetContext()

    def _mergeSchematic(self):
        self.mergeBuffers()
        self._findContext()

    def _clearSchematicFilters(self):
        self._plugin.filter().clearSchematicFilter()

    def _firstContext(self):
        self._findContext(self._plugin.data().firstItem('context'))

    def _lastContext(self):
        self._findContext(self._plugin.data().lastItem('context'))

    def _prevContext(self):
        self._findContext(self._plugin.data().prevItem(self._dock.contextItem()))

    def _nextContext(self):
        self._findContext(self._plugin.data().nextItem(self._dock.contextItem()))

    def _prevMissing(self):
        context = self._dock.contextItem()
        idx = 0
        if context.isValid():
            idx = bisect.bisect_left(self._plugin.data().items['context'], context)
        schematics = self._getAllSchematicItems()
        for prv in reversed(list(range(idx))):
            item = self._plugin.data().items['context'][prv]
            if item not in schematics:
                self._findContext(item)
                return

    def _nextMissing(self):
        context = self._dock.contextItem()
        idx = 0
        if context.isValid():
            idx = bisect.bisect(self._plugin.data().items['context'], context)
        schematics = self._getAllSchematicItems()
        for item in self._plugin.data().items['context'][idx:]:
            if item not in schematics:
                self._findContext(item)
                return

    def _getAllSchematicItems(self):
        features = self._getAllSchematicFeatures()
        items = set()
        for feature in features:
            item = Item(feature)
            items.add(item)
        return sorted(items)

    def _getAllSchematicFeatures(self):
        req = self._featureRequest(self._categoryClause('sch'))
        return layers.getAllFeaturesRequest(req, self.collection().layer('polygons'))

    def _editSchematicContext(self):
        self._editSchematic = True
        self.editInBuffers(self._dock.contextItem())
        self._dock.widget.setCurrentIndex(0)

    def _deleteSectionSchematic(self):
        item = self._dock.contextItem()
        label = 'This action ***DELETES*** ***ALL*** Section Schematics from item ' + \
            str(item.itemId()) + '\n\nPlease enter the item ID to confirm.'
        if self._confirmDelete(item.itemId(), 'Confirm Delete Section Schematic', label):
            request = self._categoryRequest(item, 'scs')
            timestamp = utils.timestamp()
            action = 'Delete Section Schematic'
            if self.collection().deleteFeatureRequest(request, action, timestamp):
                self._logItemAction(item, action, timestamp)
            self._findContext(item)

    def _arkStatus(self, item):
        haveArk = SearchStatus.NotFound
        contextType = 'None'
        contextDescription = ''
        try:
            if item in self._plugin.data().items['context']:
                haveArk = SearchStatus.Found
                vals = self._plugin.data().getItemFields(item, ['conf_field_cxttype', 'conf_field_short_desc'])
                if (u'conf_field_cxttype' in vals and vals[u'conf_field_cxttype']):
                    contextType = str(vals[u'conf_field_cxttype'])
                if u'conf_field_short_desc' in vals:
                    contextDescription = str(vals[u'conf_field_short_desc'][0][u'current'])
            else:
                contextDescription = 'Context not in ARK'
        except Exception:
            haveArk = SearchStatus.Unknown
        return haveArk, contextType, contextDescription

    def _featureStatus(self, item, copyMetadata=False):
        itemRequest = item.featureRequest()
        try:
            feature = next(self.collection().layer('lines').getFeatures(itemRequest))
            if copyMetadata:
                self._copyFeatureMetadata(feature)
        except StopIteration:
            return SearchStatus.NotFound
        return SearchStatus.Found

    def _schematicStatus(self, item):
        schRequest = self._categoryRequest(item, 'sch')
        try:
            next(self.collection().layer('polygons').getFeatures(schRequest))
        except StopIteration:
            return SearchStatus.NotFound
        return SearchStatus.Found

    def _findContext(self, context=Item()):
        self._clearSchematicFilters()

        if not context.isValid():
            context = self._dock.contextItem()

        self._plugin.filter().applySchematicFilter(context, self._filterAction)
        self.applyItemActions(context, self._mapAction, FilterAction.NoFilterAction, self._drawingAction)

        haveArk, contextType, contextDescription = self._arkStatus(context)
        haveFeature = self._featureStatus(context, True)

        if haveFeature == SearchStatus.NotFound:
            polyRequest = self._notCategoryRequest(context, 'sch')
            haveFeature = SearchStatus.Found
            try:
                next(self.collection().layer('polygons').getFeatures(polyRequest))
            except StopIteration:
                haveFeature = SearchStatus.NotFound

        haveSchematic = self._schematicStatus(context)

        scsRequest = self._categoryRequest(context, 'scs')
        haveSectionSchematic = SearchStatus.Found
        try:
            next(self.collection().layer('polygons').getFeatures(scsRequest))
        except StopIteration:
            haveSectionSchematic = SearchStatus.NotFound

        self._dock.setContext(context, haveArk, contextType, contextDescription,
                              haveFeature, haveSchematic, haveSectionSchematic)
        self.metadata.setItemId(context.itemId())

    def _editSource(self):
        self.editInBuffers(self._dock.sourceItem())
        self._dock.widget.setCurrentIndex(0)

    def _findSource(self, source=Item()):
        if not source.isValid():
            source = self._dock.sourceItem()

        self._plugin.filter().applySchematicFilter(source, self._filterAction)
        self.applyItemActions(source, self._mapAction, FilterAction.NoFilterAction, self._drawingAction)

        haveArk, contextType, contextDescription = self._arkStatus(source)
        haveFeature = self._featureStatus(source)
        haveSchematic = self._schematicStatus(source)

        self._dock.setSourceContext(source, haveArk, contextType, contextDescription, haveFeature, haveSchematic)

    def _attribute(self, feature, attribute):
        val = feature.attribute(attribute)
        if val == NULL:
            return None
        else:
            return val

    def _copyFeatureMetadata(self, feature):
        self.metadata.setSiteCode(self._attribute(feature, 'site'))
        self.metadata.setComment(self._attribute(feature, 'comment'))
        self.metadata.setClassCode('context')
        self.metadata.setItemId(self._dock.context())
        self.metadata.setSourceCode('cloned')
        self.metadata.setSourceClass('context')
        self.metadata.setSourceId(self._dock.sourceContext())
        self.metadata.setSourceFile('')

    def _copySourceSchematic(self):
        self.metadata.validate()
        request = self._categoryRequest(self._dock.sourceItem(), 'sch')
        features = layers.getAllFeaturesRequest(request, self.collection().layer('polygons'))
        for feature in features:
            feature.setAttribute('site', self.metadata.siteCode())
            feature.setAttribute('class', 'context')
            feature.setAttribute('id', self._dock.context())
            feature.setAttribute('label', None)
            feature.setAttribute('category', 'sch')
            feature.setAttribute('source_cd', self.metadata.sourceCode())
            feature.setAttribute('source_cl', self.metadata.sourceClass())
            feature.setAttribute('source_id', self.metadata.sourceId())
            feature.setAttribute('file', self.metadata.sourceFile())
            feature.setAttribute('comment', self.metadata.comment())
            feature.setAttribute('created', self.metadata.editor())
            feature.setAttribute('creator', None)
            self.collection().buffer('polygons').addFeature(feature)

    def _editSourceSchematic(self):
        self._clearSchematicFilters()
        self._copySourceSchematic()
        self._editSchematic = True
        self._dock.widget.setCurrentIndex(0)
        self._plugin.iface.setActiveLayer(self.collection().buffer('polygons'))
        self._plugin.iface.actionZoomToLayer().trigger()
        self.collection().buffer('polygons').selectAll()
        self._plugin.iface.actionNodeTool().trigger()

    def _cloneSourceSchematic(self):
        self._clearSchematicFilters()
        self._copySourceSchematic()
        self._mergeSchematic()

    def _showSchematicReport(self):
        features = set()
        for feature in self.collection().layer('points').getFeatures():
            features.add(Item(feature))
        for feature in self.collection().layer('lines').getFeatures():
            features.add(Item(feature))
        for feature in self.collection().layer('polygons').getFeatures():
            features.add(Item(feature))
        schRequest = self._featureRequest(self._categoryClause('sch'))
        scsRequest = self._featureRequest(self._categoryClause('scs'))
        schematics = set()
        for feature in self.collection().layer('polygons').getFeatures(schRequest):
            schematics.add(Item(feature))
        for feature in self.collection().layer('polygons').getFeatures(scsRequest):
            schematics.add(Item(feature))
        missing = []
        contexts = self._plugin.data().items['context']
        for context in contexts:
            if context not in schematics:
                row = {}
                row['Site Code'] = context.siteCode()
                row['Context'] = context.itemId()
                itemData = self._plugin.data().getItemData(context)
                try:
                    row['Type'] = itemData['context_type']
                except Exception:
                    row['Type'] = ''
                    try:
                        vals = self._plugin.data().getItemFields(context, ['conf_field_cxttype'])
                        row['Type'] = vals[u'conf_field_cxttype']
                    except Exception:
                        row['Type'] = ''
                if context in features:
                    row['GIS'] = 'Y'
                else:
                    row['GIS'] = 'N'
                missing.append(row)
        text = '<html><head/><body><p><span style=" font-weight:600;">Missing Schematics:</span></p><p>There are ' + \
            str(len(contexts)) + ' Contexts in ARK, of which ' + \
            str(len(missing)) + ' are missing schematics.<br/></p></body></html>'
        dialog = TableDialog('Missing Schematics', text, ['Site Code', 'Context', 'Type', 'GIS'], {
                             'Site Code': '', 'Context': '', 'Type': '', 'GIS': ''}, self._dock)
        dialog.addRows(missing)
        dialog.exec_()
