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

from . import layers
from .. import utils


class Collection:

    projectPath = ''
    settings = None  # CollectionSettings()

    # Internal variables

    _iface = None  # QgsInterface()
    _collectionGroupIndex = -1
    _bufferGroupIndex = -1
    _fields = {}  # QgsField()
    _layers = {}  # CollectionLayer()

    filter = ''
    selection = ''
    highlight = ''

    def __init__(self, iface, projectPath, settings):
        self._iface = iface
        self.projectPath = projectPath
        self.settings = settings
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
        for layer in self._layers:
            if self._layers[layer].isCollectionLayer(layerId):
                return True
        return False

    def _layers(self):
        if self._layers.length != self.settings.layers.length:
            self.loadCollection
        return self._layers

    def _layer(self, layer):
        layers = self._layers()
        if layer in layers:
            return layers[layer]
        return None

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
        for layer in self._layers():
            if not self._layers[layer].isWritable():
                return False
        return True

    def mergeBuffers(self, undoMessage='Merge Buffers', timestamp=None):
        if timestamp is None:
            timestamp = utils.timestamp()
        for layer in self._layers():
            if not self._layers[layer].mergeBuffer(undoMessage, timestamp):
                return False
        return True

    def resetBuffers(self, undoMessage='Reset Buffers'):
        for layer in self._layers():
            self._layers[layer].resetBuffer(undoMessage)

    def clearBuffers(self, undoMessage='Clear Buffers'):
        for layer in self._layers():
            self._layers[layer].clearBuffer(undoMessage)

    def moveFeatureRequestToBuffers(self, featureRequest, logMessage='Move Features', timestamp=None):
        if timestamp is None:
            timestamp = utils.timestamp()
        for layer in self._layers():
            if not self._layers[layer].moveFeatureRequestToBuffer(featureRequest, logMessage, timestamp):
                return False
        return True

    def copyFeatureRequestToBuffers(self, featureRequest, logMessage='Copy Features to Buffer', timestamp=None):
        if timestamp is None:
            timestamp = utils.timestamp()
        for layer in self._layers():
            if not self._layers[layer].copyFeatureRequestToBuffer(featureRequest, logMessage, timestamp):
                return False
        return True

    def deleteFeatureRequest(self, featureRequest, logMessage='Delete Features', timestamp=None):
        if timestamp is None:
            timestamp = utils.timestamp()
        for layer in self._layers():
            if not self._layers[layer].deleteFeatureRequest(featureRequest, logMessage, timestamp):
                return False
        return True

    def setVisible(self, status):
        for layer in self._layers():
            self._layers[layer].setVisible(status)

    def applyFilter(self, expression):
        self.filter = expression
        for layer in self._layers():
            self._layers[layer].applyFilter(expression)

    def clearFilter(self):
        for layer in self._layers():
            self._layers[layer].clearFilter()

    def applySelection(self, expression):
        self.selection = expression
        request = QgsFeatureRequest().setFilterExpression(expression)
        for layer in self._layers():
            self._layers[layer].applySelectionRequest(request)

    def clearSelection(self):
        self.selection = ''
        for layer in self._layers():
            self._layers[layer].removeSelection()

    def zoomToExtent(self):
        extent = self.extent()
        layers.zoomToExtent(self._iface.mapCanvas(), extent)

    def extent(self):
        extent = None
        for layer in self._layers():
            extent = layers.extendExtent(extent, self._layers[layer].extent())
        return extent

    def uniqueValues(self, fieldName):
        vals = set()
        for layer in self._layers():
            vals.update(self._layers[layer].uniqueValues())
        return sorted(vals)

    def updateAttribute(self, attribute, value, expression=None):
        for layer in self._layers():
            self._layers[layer].updateAttribute(attribute, value, expression)

    def updateBufferAttribute(self, attribute, value, expression=None):
        for layer in self._layers():
            self._layers[layer].updateBufferAttribute(attribute, value, expression)

    def clearHighlight(self):
        for layer in self._layers():
            self._layers[layer].clearHighlight()

    def applyHighlight(self, requestOrExpr, lineColor=None, fillColor=None, buff=None, minWidth=None):
        request = None
        if isinstance(requestOrExpr, QgsFeatureRequest):
            request = requestOrExpr
            self.highlight = request.filterExpression()
        else:
            request = QgsFeatureRequest()
            request.setFilterExpression(requestOrExpr)
            self.highlight = requestOrExpr
        for layer in self._layers():
            self._layers[layer].applyHighlight(request, lineColor, fillColor, buff, minWidth)

    def addHighlight(self, requestOrExpr, lineColor=None, fillColor=None, buff=None, minWidth=None):
        request = None
        if isinstance(requestOrExpr, QgsFeatureRequest):
            request = requestOrExpr
            self.highlight = request.filterExpression()
        else:
            request = QgsFeatureRequest()
            request.setFilterExpression(requestOrExpr)
            self.highlight = requestOrExpr
        for layer in self._layers():
            self._layers[layer].addHighlight(request, lineColor, fillColor, buff, minWidth)
