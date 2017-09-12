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

from PyQt4.QtCore import QFile, QVariant

from qgis.core import NULL, QgsField, QgsMapLayerRegistry, QgsProject, QgsSnapper, QgsTolerance, QgsVectorLayer

from . import layers
from .. import utils


class CollectionLayer:

    projectPath = ''
    settings = None  # CollectionLayerSettings()

    layer = None
    layerId = ''

    bufferLayer = None
    bufferLayerId = ''

    logLayer = None
    logLayerId = ''

    # Internal variables

    _iface = None  # QgsInterface()
    _highlights = []  # [QgsHighlight]

    def __init__(self, iface, projectPath, settings):
        self._iface = iface
        self.projectPath = projectPath
        self.settings = settings
        # If the layers are removed we need to remove them too
        QgsMapLayerRegistry.instance().layersRemoved.connect(self._layersRemoved)

    def initialise(self):
        self.loadLayer()

    def unload(self):
        pass

    def isCollectionLayer(self, layerId):
        return (layerId == self.layerId or layerId == self.bufferLayerId or layerId == self.logLayerId)

    # Load the collection layers if not already loaded
    def loadLayer(self):
        # Load the main layer
        self._loadLayer()

        # Load the edit buffer if required
        if self.settings.bufferLayer:
            self._loadBufferLayer()

        # Load the log buffer if required
        if self.settings.logLayer:
            self._loadLogLayer(self.layer, self.settings.logPath, self.settings.logName)

    # Load the main layer, must alreay exist
    def _loadLayer(self):
        layer = None
        layerList = QgsMapLayerRegistry.instance().mapLayersByName(self.settings.layerName)
        if (len(layerList) > 0):
            layer = layerList[0]
        else:
            fullLayerPath = self.projectPath + '/' + self.settings.layerPath
            layer = QgsVectorLayer(fullLayerPath, self.settings.layerName, 'ogr')
            layer = layers.addLayerToLegend(self._iface, layer)
        if layer and layer.isValid():
            self._setDefaultSnapping(layer)
            layer.loadNamedStyle(self.settings.stylePath)
            self.layer = layer
            self.layerId = layer.id()
        else:
            self.layer = None
            self.layerId = ''

    # Load the buffer layer, create it if it doesn't alreay exist
    def _loadBufferLayer(self):
        layer = None
        layerList = QgsMapLayerRegistry.instance().mapLayersByName(self.settings.bufferName)
        if (len(layerList) > 0):
            layer = layerList[0]
        else:
            fullLayerPath = self.projectPath + '/' + self.settings.bufferPath
            if (self.settings.bufferName and self.settings.bufferPath and self.layer and self.layer.isValid()):
                if not QFile.exists(fullLayerPath):
                    # If the layer doesn't exist, clone from the source layer
                    layer = layers.cloneAsShapefile(self.layer, fullLayerPath, self.settings.bufferName)
                else:
                    # If the layer does exist, then load it and copy the style
                    layer = QgsVectorLayer(fullLayerPath, self.settings.bufferName, 'ogr')
                layer = layers.addLayerToLegend(self._iface, layer)
        if layer and layer.isValid():
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
    def _loadLogLayer(self, sourceLayer, layerPath, layerName):
        layer = None
        layerList = QgsMapLayerRegistry.instance().mapLayersByName(layerName)
        if (len(layerList) > 0):
            layer = layerList[0]
        else:
            fullLayerPath = self.projectPath + '/' + layerPath
            if (layerName and layerPath and sourceLayer and sourceLayer.isValid()):
                if not QFile.exists(fullLayerPath):
                    # If the layer doesn't exist, clone from the source layer
                    layer = layers.cloneAsShapefile(sourceLayer, fullLayerPath, layerName)
                    if layer and layer.isValid():
                        layer.dataProvider().addAttributes(
                            [QgsField('timestamp', QVariant.String, '', 10, 0, 'timestamp')])
                        layer.dataProvider().addAttributes([QgsField('event', QVariant.String, '', 6, 0, 'event')])
                else:
                    # If the layer does exist, then load it and copy the style
                    layer = QgsVectorLayer(fullLayerPath, layerName, 'ogr')
                    if layer and layer.isValid():
                        layers.loadStyle(layer, fromLayer=sourceLayer)
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
        if timestamp is None and self.settings.log:
            timestamp = utils.timestamp()
        merge = True
        if layers.copyAllFeatures(self.bufferLayer,
                                  self.layer,
                                  undoMessage + ' - copy ' + self.settings.layer,
                                  self.settings.logLayer,
                                  self.logLayer,
                                  timestamp):
            self._clearBuffer(self.buffer, undoMessage + ' - delete ' + self.settings.layer)
        else:
            merge = False
        return merge

    def resetBuffer(self, undoMessage='Reset Buffers'):
        undoMessage += ' - ' + self.settings.layer
        return self.bufferLayer.rollBack() and self.bufferLayer.startEditing()

    def clearBuffer(self, undoMessage='Clear Buffers'):
        undoMessage += ' - ' + self.settings.layer
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
        if timestamp is None and self.settings.logLayer:
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
