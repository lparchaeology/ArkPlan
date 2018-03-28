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

import os

from PyQt4.QtCore import QFile, QVariant

from qgis.core import NULL, QgsField, QgsFields, QgsMapLayerRegistry, QgsProject, QgsSnapper, QgsTolerance, QgsVectorLayer

from . import layers
from .. import utils


class CollectionLayer:

    layer = None
    layerId = ''

    bufferLayer = None
    bufferLayerId = ''

    logLayer = None
    logLayerId = ''

    fields = QgsFields()

    # Internal variables

    _iface = None  # QgsInterface()
    _projectPath = ''
    _settings = None  # CollectionLayerSettings()

    _highlights = []  # [QgsHighlight]

    def __init__(self, iface, projectPath, settings):
        self._iface = iface
        self._projectPath = projectPath
        self._settings = settings
        for fieldKey in self._settings['fields']:
            field = self._settings['fields'][fieldKey].toField()
            self.fields.append(field)
        # If the layers are removed we need to remove them too
        QgsMapLayerRegistry.instance().layersRemoved.connect(self._layersRemoved)

    def isValid(self):
        self.layer !== None && self.layer.isValid()

    def initialise(self):
        self.loadLayer()
        return self.isValid()

    def unload(self):
        QgsMapLayerRegistry.instance().layersRemoved.disconnect(self._layersRemoved)

    def isCollectionLayer(self, layerId):
        return (self.layerId == layerId or self.bufferLayerId == layerId or self.logLayerId == layerId)

    # Load the collection layers if not already loaded
    def loadLayer(self):
        # Load the main layer
        self._loadLayer()

        # Load the edit buffer if required
        if self._settings.bufferLayer:
            self._loadBufferLayer()

        # Load the log buffer if required
        if self._settings.logLayer:
            self._loadLogLayer()

    # Load the main layer, must alreay exist
    def _loadLayer(self):
        fullLayerPath = os.path.join(self._projectPath, self._settings.path)
        layer = layers.loadShapefileLayer(fullLayerPath, self._settings.name)
        if layer is None:
            wkbType = layers.geometryToWkbType(self._settings.geometry, self._settings.multi)
            layer = layers.createShapefile(fullLayerPath,
                                           self._settings.name,
                                           wkbType,
                                           self._settings.crs,
                                           self.fields)
        if layer and layer.isValid():
            layer = layers.addLayerToLegend(self._iface, layer)
            self._setDefaultSnapping(layer)
            layer.loadNamedStyle(self._settings.stylePath)
            self.layer = layer
            self.layerId = layer.id()
        else:
            self.layer = None
            self.layerId = ''

    # Load the buffer layer, create it if it doesn't alreay exist
    def _loadBufferLayer(self):
        fullLayerPath = os.path.join(self._projectPath, self._settings.bufferPath)
        layer = layers.loadShapefileLayer(fullLayerPath, self._settings.bufferName)
        if layer is None:
            layer = layers.cloneAsShapefile(self.layer, fullLayerPath, self._settings.bufferName)
        if layer and layer.isValid():
            layer = layers.addLayerToLegend(self._iface, layer)
            layers.loadStyle(layer, fromLayer=self.layer)
                self._setDefaultSnapping(layer)
            layer.startEditing()
            layer.setFeatureFormSuppress(QgsVectorLayer.SuppressOn)
            self.bufferLayer = layer
            self.bufferLayerId = layer.id()
        else:
            self.bufferLayer = None
            self.bufferLayerId = ''

    # Load the log layer, create it if it doesn't alreay exist
    def _loadLogLayer(self):
        fullLayerPath = os.path.join(self._projectPath, self._settings.logPath)
        layer = layers.loadShapefileLayer(fullLayerPath, self._settings.logName)
        if layer is None:
            fields = [
                QgsField('timestamp', QVariant.String, '', 10, 0, 'timestamp'),
                QgsField('event', QVariant.String, '', 6, 0, 'event')
            ]
            fields = fields + self.fields
            layer = layers.createShapefile(fullLayerPath,
                                           self._settings.logName,
                                           self.layer.wkbType(),
                                           self._settings.crs,
                                           fields)
        if layer and layer.isValid():
            layer.setFeatureFormSuppress(QgsVectorLayer.SuppressOn)
            self.logLayer = layer
            self.logLayerId = layer.id()
        else:
            self.logLayer = None
            self.logLayerId = ''

    def _setDefaultSnapping(self, layer):
        res = QgsProject.instance().snapSettingsForLayer(layer.id())
        if not res[0]:
            QgsProject.instance().setSnapSettingsForLayer(
                layer.id(), True, QgsSnapper.SnapToVertex, QgsTolerance.Pixels, 10.0, False)

    def moveLayer(self, groupIndex, expanded=False):
        self._moveLayer(self.layer, groupIndex, expanded)

    def moveBufferLayer(self, groupIndex, expanded=False):
        self._moveLayer(self.bufferLayer, groupIndex, expanded)

    def _moveLayer(self, layer, groupIndex, expanded):
        self._iface.legendInterface().moveLayer(layer, groupIndex)
        self._iface.legendInterface().setLayerExpanded(layer, False)

    # If a layer is removed from the registry, (i.e. closed), we can't use it anymore
    def _layersRemoved(self, layerList):
        for layerId in layerList:
            if layerId == '':
                pass
            elif layerId == self.layerId:
                self.layer = None
                self.layerId = ''
            elif layerId == self.bufferLayerId:
                self.bufferLayer = None
                self.bufferLayerId = ''
            elif layerId == self.logLayerId:
                self.logLayer = None
                self.logLayerId = ''

    def _removeLayers(self):
        if self.layerId:
            QgsMapLayerRegistry.instance().removeMapLayer(self.layerId)
        if self.bufferLayerId:
            QgsMapLayerRegistry.instance().removeMapLayer(self.bufferLayerId)
        if self.logLayerId:
            QgsMapLayerRegistry.instance().removeMapLayer(self.logLayerId)

    def isWritable(self):
        return ((self.layer is None or layers.isWritable(self.layer))
                and (self.bufferLayer is None or layers.isWritable(self.bufferLayeruffer))
                and (self.logLayer is None or layers.isWritable(self.logLayer)))

    def mergeBuffer(self, undoMessage='Merge Buffers', timestamp=None):
        if timestamp is None and self._settings.log:
            timestamp = utils.timestamp()
        merge = True
        if layers.copyAllFeatures(self.bufferLayer,
                                  self.layer,
                                  undoMessage + ' - copy ' + self._settings.layer,
                                  self._settings.logLayer,
                                  self.logLayer,
                                  timestamp):
            self._clearBuffer(self.buffer, undoMessage + ' - delete ' + self._settings.layer)
        else:
            merge = False
        return merge

    def resetBuffer(self, undoMessage='Reset Buffers'):
        undoMessage += ' - ' + self._settings.layer
        return self.bufferLayer.rollBack() and self.bufferLayer.startEditing()

    def clearBuffer(self, undoMessage='Clear Buffers'):
        undoMessage += ' - ' + self._settings.layer
        return (layers.deleteAllFeatures(self.bufferLayer, undoMessage)
                and self.bufferLayer.commitChanges()
                and self.bufferLayer.startEditing())

    def moveFeatureRequestToBuffer(self, featureRequest, logMessage='Move Features', timestamp=None):
        ret = False
        if self.bufferLayer.isEditable():
            self.bufferLayer.commitChanges()
        if self.copyFeatureRequestToBuffers(featureRequest, logMessage):
            ret = self.deleteFeatureRequest(featureRequest, logMessage, timestamp)
        self.bufferLayer.startEditing()
        return ret

    def copyFeatureRequestToBuffer(self, featureRequest, logMessage='Copy Features to Buffer'):
        return layers.copyFeatureRequest(featureRequest, self.layer, self.bufferLayer, logMessage)

    def deleteFeatureRequest(self, featureRequest, logMessage='Delete Features', timestamp=None):
        if timestamp is None and self._settings.logLayer:
            timestamp = utils.timestamp()
        return layers.deleteFeatureRequest(featureRequest, self.layer, logMessage, self.logLayer, timestamp)

    def setVisible(self, status):
        self._iface.legendInterface().setLayerVisible(self.layer, status)

    def setBufferVisible(self, status):
        self._iface.legendInterface().setLayerVisible(self.bufferLayer, status)

    def applyFilter(self, expression):
        layers.applyFilter(self._iface, self.layer, expression)

    def clearFilter(self):
        self.applyFilter('')

    def applySelectionRequest(self, request):
        layers.applySelectionRequest(self.layer, request)

    def clearSelection(self):
        if self.layer:
            self.layer.removeSelection()

    def zoomToExtent(self):
        layers.zoomToExtent(self._iface.mapCanvas(), self.extent())

    def extent(self):
        extent = None
        if (self.layer is not None and self._iface.legendInterface().isLayerVisible(self.layer)):
            extent = layers.extendExtent(extent, self.layer)
        if (self.bufferLayer is not None and self._iface.legendInterface().isLayerVisible(self.bufferLayer)):
            extent = layers.extendExtent(extent, self.bufferLayer)
        return extent

    def uniqueValues(self, fieldName):
        vals = set()
        vals.update(layers.uniqueValues(self.layer, fieldName))
        vals.discard(None)
        vals.discard(NULL)
        vals.discard('')
        return sorted(vals)

    def updateAttribute(self, attribute, value, expression=None):
        layers.updateAttribute(self.layer, attribute, value, expression)

    def updateBufferAttribute(self, attribute, value, expression=None):
        layers.updateAttribute(self.buffer, attribute, value, expression)

    def clearHighlight(self):
        for hl in self._highlights:
            hl.remove()
        del self._highlights[:]

    def applyHighlight(self, request, lineColor=None, fillColor=None, buff=None, minWidth=None):
        self.clearHighlight()
        self.addHighlight(request, lineColor, fillColor, buff, minWidth)

    def addHighlight(self, request, lineColor=None, fillColor=None, buff=None, minWidth=None):
        for feature in self.layer.getFeatures(request):
            hl = layers.addHighlight(self._iface.mapCanvas(), feature, self.layer, lineColor, fillColor, buff, minWidth)
            self._highlights.append(hl)
