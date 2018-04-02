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

from qgis.core import QgsFeatureRequest

import layers
from .. import utils

from collection_layer import CollectionLayer


class Collection:

    def __init__(self, iface, projectPath, settings):
        self.projectPath = projectPath
        self.settings = settings  # CollectionSettings()
        self.filter = ''
        self.selection = ''
        self.highlight = ''

        # Internal variables
        self._iface = iface  # QgsInterface()
        self._collectionGroupIndex = -1
        self._bufferGroupIndex = -1
        self._layers = {}  # CollectionLayer()

        # If the legend indexes change make sure we stay updated
        self._iface.legendInterface().groupIndexChanged.connect(self._groupIndexChanged)

    def initialise(self):
        return self.loadCollection()

    def unload(self):
        pass

    def isCollectionGroup(self, name):
        return (name == self.settings.collectionGroupName or name == self.settings.bufferGroupName)

    def isCollectionLayer(self, layerId):
        for layer in self._layers:
            if self._layers[layer].isCollectionLayer(layerId):
                return True
        return False

    def _groupIndexChanged(self, oldIndex, newIndex):
        if (oldIndex == self._collectionGroupIndex):
            self._collectionGroupIndex = newIndex
        elif (oldIndex == self._bufferGroupIndex):
            self._bufferGroupIndex = newIndex

    # Load the collection layers if not already loaded
    def loadCollection(self):
        if len(self._layers) == len(self.settings.layers):
            return True

        for settings in self.settings.layers:
            layer = CollectionLayer(self._iface, self.projectPath, settings)
            if layer != None and layer.initialise():
                self._layers[settings.layer] = layer

        # Load the main layers
        self._collectionGroupIndex = layers.createLayerGroup(
            self._iface, self.settings.collectionGroupName, self.settings.parentGroupName)
        for layer in reversed(self.settings.layers):
            self._layers[layer.layer].moveLayer(self._collectionGroupIndex)

        # Load the edit buffers if required
        if self.settings.bufferGroupName:
            self._bufferGroupIndex = layers.createLayerGroup(
                self._iface, self.settings.bufferGroupName, self.settings.collectionGroupName)
            layers.moveChildGroup(self.settings.collectionGroupName, self.settings.bufferGroupName, 0)
            self._bufferGroupIndex = layers.getGroupIndex(self._iface, self.settings.bufferGroupName)
            for layer in reversed(self.settings.layers):
                self._layers[layer.layer].moveBufferLayer(self._bufferGroupIndex)

        return len(self._layers) == len(self.settings.layers)

    def hasLayer(self, name):
        return name in self._layers and self._layers[name].layer != None

    def layer(self, name):
        if name in self._layers:
            return self._layers[name].layer
        return None

    def hasBuffer(self, name):
        return name in self._layers and self._layers[name].buffer != None

    def buffer(self, name):
        if name in self._layers:
            return self._layers[name].buffer
        return None

    def isWritable(self):
        for layerKey in self._layers:
            if not self._layers[layerKey].isWritable():
                return False
        return True

    def mergeBuffers(self, undoMessage='Merge Buffers', timestamp=None):
        if timestamp is None:
            timestamp = utils.timestamp()
        for layerKey in self._layers:
            if not self._layers[layerKey].mergeBuffer(undoMessage, timestamp):
                return False
        return True

    def resetBuffers(self, undoMessage='Reset Buffers'):
        for layerKey in self._layers:
            self._layers[layerKey].resetBuffer(undoMessage)

    def clearBuffers(self, undoMessage='Clear Buffers'):
        for layerKey in self._layers:
            self._layers[layerKey].clearBuffer(undoMessage)

    def moveFeatureRequestToBuffers(self, featureRequest, logMessage='Move Features', timestamp=None):
        if timestamp is None:
            timestamp = utils.timestamp()
        for layerKey in self._layers:
            if not self._layers[layerKey].moveFeatureRequestToBuffer(featureRequest, logMessage, timestamp):
                return False
        return True

    def copyFeatureRequestToBuffers(self, featureRequest, logMessage='Copy Features to Buffer', timestamp=None):
        if timestamp is None:
            timestamp = utils.timestamp()
        for layerKey in self._layers:
            if not self._layers[layerKey].copyFeatureRequestToBuffer(featureRequest, logMessage, timestamp):
                return False
        return True

    def deleteFeatureRequest(self, featureRequest, logMessage='Delete Features', timestamp=None):
        if timestamp is None:
            timestamp = utils.timestamp()
        for layerKey in self._layers:
            if not self._layers[layerKey].deleteFeatureRequest(featureRequest, logMessage, timestamp):
                return False
        return True

    def setVisible(self, status):
        for layerKey in self._layers:
            self._layers[layerKey].setVisible(status)

    def applyFilter(self, expression):
        self.filter = expression
        for layerKey in self._layers:
            self._layers[layerKey].applyFilter(expression)

    def clearFilter(self):
        for layerKey in self._layers:
            self._layers[layerKey].clearFilter()

    def applySelection(self, expression):
        self.selection = expression
        request = QgsFeatureRequest().setFilterExpression(expression)
        for layerKey in self._layers:
            self._layers[layerKey].applySelectionRequest(request)

    def clearSelection(self):
        self.selection = ''
        for layerKey in self._layers:
            self._layers[layerKey].removeSelection()

    def zoomToExtent(self):
        extent = self.extent()
        layers.zoomToExtent(self._iface.mapCanvas(), extent)

    def extent(self):
        extent = None
        for layerKey in self._layers:
            extent = layers.extendExtent(extent, self._layers[layerKey].extent())
        return extent

    def uniqueValues(self, fieldName):
        vals = set()
        for layerKey in self._layers:
            vals.update(self._layers[layerKey].uniqueValues())
        return sorted(vals)

    def updateAttribute(self, attribute, value, expression=None):
        for layerKey in self._layers:
            self._layers[layerKey].updateAttribute(attribute, value, expression)

    def updateBufferAttribute(self, attribute, value, expression=None):
        for layerKey in self._layers:
            self._layers[layerKey].updateBufferAttribute(attribute, value, expression)

    def clearHighlight(self):
        for layerKey in self._layers:
            self._layers[layerKey].clearHighlight()

    def applyHighlight(self, requestOrExpr, lineColor=None, fillColor=None, buff=None, minWidth=None):
        request = None
        if isinstance(requestOrExpr, QgsFeatureRequest):
            request = requestOrExpr
            self.highlight = request.filterExpression()
        else:
            request = QgsFeatureRequest()
            request.setFilterExpression(requestOrExpr)
            self.highlight = requestOrExpr
        for layerKey in self._layers:
            self._layers[layerKey].applyHighlight(request, lineColor, fillColor, buff, minWidth)

    def addHighlight(self, requestOrExpr, lineColor=None, fillColor=None, buff=None, minWidth=None):
        request = None
        if isinstance(requestOrExpr, QgsFeatureRequest):
            request = requestOrExpr
            self.highlight = request.filterExpression()
        else:
            request = QgsFeatureRequest()
            request.setFilterExpression(requestOrExpr)
            self.highlight = requestOrExpr
        for layerKey in self._layers:
            self._layers[layerKey].addHighlight(request, lineColor, fillColor, buff, minWidth)
