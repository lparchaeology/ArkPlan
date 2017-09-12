# -*- coding: utf-8 -*-
"""
/***************************************************************************
                                ARK QGIS
                        A QGIS utilities library.
        Part of the Archaeological Recording Kit by L-P : Archaeology
                        http://ark.lparchaeology.com
                              -------------------
        copyright            : 2017 by L-P : Heritage LLP
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

from qgis.core import QgsFeatureRequest

from . import layers
from .. import utils
from collection_layer import CollectionLayer


class Collection:

    projectPath = ''
    settings = None  # CollectionSettings()

    points = None  # CollectionLayer()
    lines = None  # CollectionLayer()
    polygons = None  # CollectionLayer()

    # Internal variables

    _iface = None  # QgsInterface()
    _collectionGroupIndex = -1
    _bufferGroupIndex = -1

    filter = ''
    selection = ''
    highlight = ''

    def __init__(self, iface, projectPath, settings):
        self._iface = iface
        self.projectPath = projectPath
        self.settings = settings
        self.points = CollectionLayer(iface, projectPath, settings.points)
        self.lines = CollectionLayer(iface, projectPath, settings.lines)
        self.polygons = CollectionLayer(iface, projectPath, settings.polygons)
        # If the legend indexes change make sure we stay updated
        self._iface.legendInterface().groupIndexChanged.connect(self._groupIndexChanged)

    def initialise(self):
        return self.loadCollection()

    def unload(self):
        pass

    def isCollectionGroup(self, name):
        return (name == self.plan.settings.collectionGroupName
                or name == self.plan.settings.bufferGroupName)

    def isCollectionLayer(self, layerId):
        return (self.points.isCollectionLayer(layerId)
                or self.lines.isCollectionLayer(layerId)
                or self.polygons.isCollectionLayer(layerId))

    def _groupIndexChanged(self, oldIndex, newIndex):
        if (oldIndex == self._collectionGroupIndex):
            self._collectionGroupIndex = newIndex
        elif (oldIndex == self._bufferGroupIndex):
            self._bufferGroupIndex = newIndex

    # Load the collection layers if not already loaded
    def loadCollection(self):
        self.points.loadLayer()
        self.lines.loadLayer()
        self.polygons.loadLayer()

        # Load the main layers
        self._collectionGroupIndex = layers.createLayerGroup(
            self._iface, self.settings.collectionGroupName, self.settings.parentGroupName)
        self.points.moveLayer(self._collectionGroupIndex)
        self.lines.moveLayer(self._collectionGroupIndex)
        self.polygons.moveLayer(self._collectionGroupIndex)

        # Load the edit buffers if required
        if self.settings.bufferGroupName:
            self._bufferGroupIndex = layers.createLayerGroup(
                self._iface, self.settings.bufferGroupName, self.settings.collectionGroupName)
            layers.moveChildGroup(self.settings.collectionGroupName, self.settings.bufferGroupName, 0)
            self._bufferGroupIndex = layers.getGroupIndex(self._iface, self.settings.bufferGroupName)
            self.points.moveBufferLayer(self._bufferGroupIndex)
            self.lines.moveBufferLayer(self._bufferGroupIndex)
            self.polygons.moveBufferLayer(self._bufferGroupIndex)

        # TODO actually check if is OK
        return True

    def isWritable(self):
        return (self.points.isWritable() and self.lines.isWritable() and self.polygons.isWritable())

    def mergeBuffers(self, undoMessage='Merge Buffers', timestamp=None):
        if timestamp is None:
            timestamp = utils.timestamp()
        return (self.points.mergeBuffer(undoMessage, timestamp)
                and self.lines.mergeBuffer(undoMessage, timestamp)
                and self.polygons.mergeBuffer(undoMessage, timestamp))

    def resetBuffers(self, undoMessage='Reset Buffers'):
        self.points.resetBuffer(undoMessage)
        self.lines.resetBuffer(undoMessage)
        self.polygons.resetBuffer(undoMessage)

    def clearBuffers(self, undoMessage='Clear Buffers'):
        self.points.clearBuffer(undoMessage)
        self.lines.clearBuffer(undoMessage)
        self.polygons.clearBuffer(undoMessage)

    def moveFeatureRequestToBuffers(self, featureRequest, logMessage='Move Features', timestamp=None):
        if timestamp is None:
            timestamp = utils.timestamp()
        return (self.points.moveFeatureRequestToBuffer(featureRequest, logMessage, timestamp)
                and self.lines.moveFeatureRequestToBuffer(featureRequest, logMessage, timestamp)
                and self.polygons.moveFeatureRequestToBuffer(featureRequest, logMessage, timestamp))

    def copyFeatureRequestToBuffers(self, featureRequest, logMessage='Copy Features to Buffer', timestamp=None):
        if timestamp is None:
            timestamp = utils.timestamp()
        return (self.points.copyFeatureRequestToBuffer(featureRequest, logMessage, timestamp)
                and self.lines.copyFeatureRequestToBuffer(featureRequest, logMessage, timestamp)
                and self.polygons.copyFeatureRequestToBuffer(featureRequest, logMessage, timestamp))

    def deleteFeatureRequest(self, featureRequest, logMessage='Delete Features', timestamp=None):
        if timestamp is None:
            timestamp = utils.timestamp()
        return (self.points.deleteFeatureRequest(featureRequest, logMessage, timestamp)
                and self.lines.deleteFeatureRequest(featureRequest, logMessage, timestamp)
                and self.polygons.deleteFeatureRequest(featureRequest, logMessage, timestamp))

    def setVisible(self, status):
        self.points.setVisible(status)
        self.lines.setVisible(status)
        self.polygons.setVisible(status)

    def applyFilter(self, expression):
        self.filter = expression
        self.points.applyFilter(expression)
        self.lines.applyFilter(expression)
        self.polygons.applyFilter(expression)

    def clearFilter(self):
        self.points.clearFilter()
        self.lines.clearFilter()
        self.polygons.clearFilter()

    def applySelection(self, expression):
        self.selection = expression
        request = QgsFeatureRequest().setFilterExpression(expression)
        self.points.applySelectionRequest(request)
        self.lines.applySelectionRequest(request)
        self.polygons.applySelectionRequest(request)

    def clearSelection(self):
        self.selection = ''
        self.points.removeSelection()
        self.lines.removeSelection()
        self.polygons.removeSelection()

    def zoomToExtent(self):
        extent = self.extent()
        layers.zoomToExtent(self._iface.mapCanvas(), extent)

    def extent(self):
        extent = None
        extent = layers.extendExtent(extent, self.points.extent())
        extent = layers.extendExtent(extent, self.lines.extent())
        extent = layers.extendExtent(extent, self.polygons.extent())
        return extent

    def uniqueValues(self, fieldName):
        vals = set()
        vals.update(self.points.uniqueValues())
        vals.update(self.lines.uniqueValues())
        vals.update(self.polygons.uniqueValues())
        return sorted(vals)

    def updateAttribute(self, attribute, value, expression=None):
        self.points.updateAttribute(attribute, value, expression)
        self.lines.updateAttribute(attribute, value, expression)
        self.polygons.updateAttribute(attribute, value, expression)

    def updateBufferAttribute(self, attribute, value, expression=None):
        self.points.updateBufferAttribute(attribute, value, expression)
        self.lines.updateBufferAttribute(attribute, value, expression)
        self.polygons.updateBufferAttribute(attribute, value, expression)

    def clearHighlight(self):
        self.points.clearHighlight()
        self.lines.clearHighlight()
        self.polygons.clearHighlight()

    def applyHighlight(self, requestOrExpr, lineColor=None, fillColor=None, buff=None, minWidth=None):
        request = None
        if isinstance(requestOrExpr, QgsFeatureRequest):
            request = requestOrExpr
            self.highlight = request.filterExpression()
        else:
            request = QgsFeatureRequest()
            request.setFilterExpression(requestOrExpr)
            self.highlight = requestOrExpr
        self.points.applyHighlight(request, lineColor, fillColor, buff, minWidth)
        self.lines.applyHighlight(request, lineColor, fillColor, buff, minWidth)
        self.polygons.applyHighlight(request, lineColor, fillColor, buff, minWidth)

    def addHighlight(self, requestOrExpr, lineColor=None, fillColor=None, buff=None, minWidth=None):
        request = None
        if isinstance(requestOrExpr, QgsFeatureRequest):
            request = requestOrExpr
            self.highlight = request.filterExpression()
        else:
            request = QgsFeatureRequest()
            request.setFilterExpression(requestOrExpr)
            self.highlight = requestOrExpr
        self.points.addHighlight(request, lineColor, fillColor, buff, minWidth)
        self.lines.addHighlight(request, lineColor, fillColor, buff, minWidth)
        self.polygons.addHighlight(request, lineColor, fillColor, buff, minWidth)
