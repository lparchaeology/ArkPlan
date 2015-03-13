# -*- coding: utf-8 -*-
"""
/***************************************************************************
                                      Ark
                                 A QGIS plugin
             QGIS Plugin for ARK, the Archaeological Recording Kit
                              -------------------
        begin                : 2015-03-02
        git sha              : $Format:%H$
        copyright            : (C) 2015 by L - P: Heritage LLP
        copyright            : (C) 2015 by John Layt
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
from PyQt4.QtCore import QVariant
from PyQt4.QtGui import QMessageBox

from qgis.core import *

from settings import *

class LayerManager:

    settings = None # Settings()

    # Internal variables

    geoLayer = QgsRasterLayer()

    pointsLayer = None
    linesLayer = None
    polygonsLayer = None
    schematicLayer = None
    gridPointsLayer = None

    pointsBuffer = None
    linesBuffer = None
    polygonsBuffer = None
    schematicBuffer = None

    filter = ''

    def __init__(self, settings):
        self.settings = settings
        # If the legend indexes change make sure we stay updated
        self.settings.iface.legendInterface().groupIndexChanged.connect(self.groupIndexChanged)

    def initialise(self):
        self.loadContextLayers()
        self.createBufferLayers()

    def unload(self):
        # Remove the buffers from the legend
        if (self.pointsBuffer is not None and self.pointsBuffer.isValid()):
            QgsMapLayerRegistry.instance().removeMapLayer(self.pointsBuffer.id())
        if self.linesBuffer is not None:
            QgsMapLayerRegistry.instance().removeMapLayer(self.linesBuffer.id())
        if self.polygonsBuffer is not None:
            QgsMapLayerRegistry.instance().removeMapLayer(self.polygonsBuffer.id())
        if self.schematicBuffer is not None:
            QgsMapLayerRegistry.instance().removeMapLayer(self.schematicBuffer.id())
        if (self.settings.bufferGroupIndex >= 0):
            self.settings.iface.legendInterface().removeGroup(self.settings.bufferGroupIndex)

    def groupIndexChanged(self, oldIndex, newIndex):
        if (oldIndex == self.settings.dataGroupIndex):
            self.settings.dataGroupIndex = newIndex
        elif (oldIndex == self.settings.bufferGroupIndex):
            self.settings.bufferGroupIndex = newIndex
        elif (oldIndex == self.settings.planGroupIndex):
            self.settings.planGroupIndex = newIndex

    def loadLayerByName(self, dir, name, groupIndex):
        # If the layer is already loaded, use it and return
        layerList = QgsMapLayerRegistry.instance().mapLayersByName(name)
        if (len(layerList) > 0):
            self.settings.iface.legendInterface().moveLayer(layerList[0], groupIndex)
            return layerList[0]
        #TODO Check if exists, if not then create!
        # Otherwise load the layer and add it to the legend
        layer = QgsVectorLayer(dir.absolutePath() + '/' + name + '.shp', name, "ogr")
        if (layer.isValid()):
            self._setDefaultSnapping(layer)
            # TODO Check for other locations of style file
            layer.loadNamedStyle(dir.absolutePath() + '/' + name + '.qml')
            QgsMapLayerRegistry.instance().addMapLayer(layer)
            self.settings.iface.legendInterface().moveLayer(layer, groupIndex)
            self.settings.iface.legendInterface().refreshLayerSymbology(layer)
            return layer
        return None

    # Load the context layers if not already loaded
    def loadContextLayers(self):
        if (self.settings.dataGroupIndex < 0):
            self.settings.dataGroupIndex = self.getGroupIndex(self.settings.dataGroupName)
        if (self.schematicLayer is None):
            self.schematicLayer = self.loadLayerByName(self.settings.dataDir(), self.settings.schematicLayerName(), self.settings.dataGroupIndex)
        if (self.polygonsLayer is None):
            self.polygonsLayer = self.loadLayerByName(self.settings.dataDir(), self.settings.polygonsLayerName(), self.settings.dataGroupIndex)
        if (self.linesLayer is None):
            self.linesLayer = self.loadLayerByName(self.settings.dataDir(), self.settings.linesLayerName(), self.settings.dataGroupIndex)
        if (self.pointsLayer is None):
            self.pointsLayer = self.loadLayerByName(self.settings.dataDir(), self.settings.pointsLayerName(), self.settings.dataGroupIndex)
        if (self.gridPointsLayer is None):
            self.gridPointsLayer = self.loadLayerByName(self.settings.gridDir(), self.settings.gridPointsLayerName(), self.settings.dataGroupIndex)

    def _setDefaultSnapping(self, layer):
        # TODO Check if layer id already in settings, only set defaults if it isn't
        QgsProject.instance().setSnapSettingsForLayer(layer.id(), True, self.settings.defaultSnappingMode(), self.settings.defaultSnappingUnit(), self.settings.defaultSnappingTolerance(), False)

    # Setup the in-memory buffer layers
    def createBufferLayers(self):

        if (self.settings.bufferGroupIndex < 0):
            self.settings.bufferGroupIndex = self.getGroupIndex(self.settings.bufferGroupName)

        if (self.schematicBuffer is None or not self.schematicBuffer.isValid()):
            self.schematicBuffer = self.createMemoryLayer(self.schematicLayer)
            self.addBufferToLegend(self.schematicBuffer)

        if (self.polygonsBuffer is None or not self.polygonsBuffer.isValid()):
            self.polygonsBuffer = self.createMemoryLayer(self.polygonsLayer)
            self.addBufferToLegend(self.polygonsBuffer)

        if (self.linesBuffer is None or not self.linesBuffer.isValid()):
            self.linesBuffer = self.createMemoryLayer(self.linesLayer)
            self.addBufferToLegend(self.linesBuffer)

        if (self.pointsBuffer is None or not self.pointsBuffer.isValid()):
            self.pointsBuffer = self.createMemoryLayer(self.pointsLayer)
            self.addBufferToLegend(self.pointsBuffer)

    def addBufferToLegend(self, buffer):
        if buffer.isValid():
            self.addLayerToLegend(buffer, self.settings.bufferGroupIndex)
            buffer.startEditing()

    def addLayerToLegend(self, layer, group):
        if layer.isValid():
            QgsMapLayerRegistry.instance().addMapLayer(layer)
            self.settings.iface.legendInterface().moveLayer(layer, group)
            self.settings.iface.legendInterface().refreshLayerSymbology(layer)

    def createLayer(self, type, name, style, provider):
        layer = QgsVectorLayer(type + "?crs=" + self.settings.projectCrs() + "&index=yes", name, provider)
        if (layer.isValid()):
            attributes = [QgsField(self.settings.contextAttributeName, QVariant.Int, '', self.settings.contextAttributeSize),
                          QgsField(self.settings.sourceAttributeName,  QVariant.String, '', self.settings.sourceAttributeSize),
                          QgsField(self.settings.typeAttributeName, QVariant.String, '', self.settings.typeAttributeSize),
                          QgsField(self.settings.commentAttributeName, QVariant.String, '', self.settings.commentAttributeSize)]
            if (type.lower() == 'point'):
                attributes.append(QgsField(self.settings.elevationAttributeName, QVariant.Double, '', self.settings.elevationAttributeSize, self.settings.elevationAttributePrecision))
            layer.dataProvider().addAttributes(attributes)
            layer.loadNamedStyle(self.settings.dataDir().absolutePath() + '/' + style + '.qml')
            self._setDefaultSnapping(layer)
        #TODO set symbols?
        return layer

    def createMemoryLayer(self, layer):
        if layer.isValid():
            uri = self.wkbToMemoryType(layer.wkbType()) + "?crs=" + layer.crs().authid() + "&index=yes"
            buffer = QgsVectorLayer(uri, layer.name() + self.settings.bufferSuffix, 'memory')
            if (buffer is not None and buffer.isValid()):
                buffer.dataProvider().addAttributes(layer.dataProvider().fields().toList())
                buffer.loadNamedStyle(layer.styleURI())
            return buffer
        return None

    def wkbToMemoryType(self, wkbType):
        if (wkbType == QGis.WKBPoint):
            return 'point'
        elif (wkbType == QGis.WKBLineString):
            return 'linestring'
        elif (wkbType == QGis.WKBPolygon):
            return 'polygon'
        elif (wkbType == QGis.WKBMultiPoint):
            return 'multipoint'
        elif (wkbType == QGis.WKBMultiLineString):
            return 'multilinestring'
        elif (wkbType == QGis.WKBMultiPolygon):
            return 'multipolygon'
        elif (wkbType == QGis.WKBPoint25D):
            return 'point'
        elif (wkbType == QGis.WKBLineString25D):
            return 'linestring'
        elif (wkbType == QGis.WKBPolygon25D):
            return 'polygon'
        elif (wkbType == QGis.WKBMultiPoint25D):
            return 'multipoint'
        elif (wkbType == QGis.WKBMultiLineString25D):
            return 'multilinestring'
        elif (wkbType == QGis.WKBMultiPolygon25D):
            return 'multipolygon'
        return 'unknown'

    def okToMergeBuffers(self):
        return self.areLayersEditable()

    def areLayersEditable(self):
        return self.isLayerEditable(self.pointsLayer) and self.isLayerEditable(self.linesLayer) and self.isLayerEditable(self.polygonsLayer) and self.isLayerEditable(self.schematicLayer)

    def isLayerEditable(self, layer):
        if (layer.type() != QgsMapLayer.VectorLayer):
            self.settings.showCriticalMessage('Cannot edit layer ' + layer.name() + ' - Not a vector layer')
            return False
        if (layer.isModified()):
            self.settings.showCriticalMessage('Cannot edit layer ' + layer.name() + ' - Has pending modifications')
            return False
        # We don't check here as can turn filter off temporarily
        #if (layer.subsetString()):
        #    self.settings.showCriticalMessage('Cannot edit layer ' + layer.name() + ' - Filter is applied')
        #    return False
        if (len(layer.vectorJoins()) > 0):
            self.settings.showCriticalMessage('Cannot edit layer ' + layer.name() + ' - Layer has joins')
            return False
        return True

    def clearBuffer(self, type, buffer, undoMessage=''):
        message = undoMessage
        if (not undoMessage):
            message = 'Clear buffer'
        message = message + ' - ' + type
        buffer.selectAll()
        if (buffer.selectedFeatureCount() > 0):
            if not buffer.isEditable():
                buffer.startEditing()
            buffer.beginEditCommand(message)
            buffer.deleteSelectedFeatures()
            buffer.endEditCommand()
            buffer.commitChanges()
            buffer.startEditing()
        buffer.removeSelection()

    def copyBuffer(self, type, buffer, layer, undoMessage=''):
        ok = False
        message = undoMessage
        if (not undoMessage):
            message = 'Merge data'
        message = message + ' - ' + type
        filter = layer.subsetString()
        if filter:
            layer.setSubsetString('')
        buffer.selectAll()
        if (buffer.selectedFeatureCount() > 0):
            if layer.startEditing():
                layer.beginEditCommand(message)
                ok = layer.addFeatures(buffer.selectedFeatures(), False)
                layer.endEditCommand()
                if ok:
                    ok = layer.commitChanges()
        else:
            ok = True
        buffer.removeSelection()
        if filter:
            layer.setSubsetString(filter)
        return ok

    def mergeBuffers(self, undoMessage):
        if self.copyBuffer('levels', self.pointsBuffer, self.pointsLayer, undoMessage):
            self.clearBuffer('levels', self.pointsBuffer, undoMessage)
        if self.copyBuffer('lines', self.linesBuffer, self.linesLayer, undoMessage):
            self.clearBuffer('lines', self.linesBuffer, undoMessage)
        if self.copyBuffer('polygons', self.polygonsBuffer, self.polygonsLayer, undoMessage):
            self.clearBuffer('polygons', self.polygonsBuffer, undoMessage)
        if self.copyBuffer('schematic', self.schematicBuffer, self.schematicLayer, undoMessage):
            self.clearBuffer('schematic', self.schematicBuffer, undoMessage)

    def clearBuffers(self, undoMessage):
        self.clearBuffer('levels', self.pointsBuffer, undoMessage)
        self.clearBuffer('lines', self.linesBuffer, undoMessage)
        self.clearBuffer('polygons', self.polygonsBuffer, undoMessage)
        self.clearBuffer('schematic', self.schematicBuffer, undoMessage)

    def loadGeoLayer(self, geoFile):
        #TODO Check if already loaded, remove old one?
        self.geoLayer = QgsRasterLayer(geoFile.absoluteFilePath(), geoFile.completeBaseName())
        self.geoLayer.renderer().setOpacity(self.settings.planTransparency()/100.0)
        QgsMapLayerRegistry.instance().addMapLayer(self.geoLayer)
        if (self.settings.planGroupIndex < 0):
            self.settings.planGroupIndex = self.getGroupIndex(self.settings.planGroupName)
        self.settings.iface.legendInterface().moveLayer(self.geoLayer, self.settings.planGroupIndex)
        self.settings.iface.mapCanvas().setExtent(self.geoLayer.extent())

    def getGroupIndex(self, groupName):
        groupIndex = -1
        i = 0
        for name in self.settings.iface.legendInterface().groups():
            if (groupIndex < 0 and name == groupName):
                groupIndex = i
            i += 1
        if (groupIndex < 0):
            groupIndex = self.settings.iface.legendInterface().addGroup(groupName)
        return groupIndex

    def showPoints(self, status):
        self.settings.iface.legendInterface().setLayerVisible(self.pointsLayer, status)

    def showLines(self, status):
        self.settings.iface.legendInterface().setLayerVisible(self.linesLayer, status)

    def showPolygons(self, status):
        self.settings.iface.legendInterface().setLayerVisible(self.polygonsLayer, status)

    def showSchematics(self, status):
        self.settings.iface.legendInterface().setLayerVisible(self.schematicLayer, status)


    def applyContextFilter(self, contextList):
        clause = '"' + self.settings.contextAttributeName + '" = %d'
        filter = ''
        if (len(contextList) > 0):
            filter += clause % contextList[0]
            for context in contextList[1:]:
                filter += ' or '
                filter += clause % context
        self.applyFilter(filter)


    def applyFilter(self, filter):
        self.filter = filter
        self.applyLayerFilter(self.pointsLayer, self.filter)
        self.applyLayerFilter(self.linesLayer, self.filter)
        self.applyLayerFilter(self.polygonsLayer, self.filter)
        self.applyLayerFilter(self.schematicLayer, self.filter)


    def applyLayerFilter(self, layer, filter):
        if (self.settings.iface.mapCanvas().isDrawing()):
            self.settings.showMessage('Cannot apply filter: Canvas is drawing')
            return
        if (layer.type() != QgsMapLayer.VectorLayer):
            self.settings.showMessage('Cannot apply filter: Not a vector layer')
            return
        if (layer.isEditable()):
            self.settings.showMessage('Cannot apply filter: Layer is in editing mode')
            return
        if (not layer.dataProvider().supportsSubsetString()):
            self.settings.showMessage('Cannot apply filter: Subsets not supported by layer')
            return
        if (len(layer.vectorJoins()) > 0):
            self.settings.showMessage('Cannot apply filter: Layer has joins')
            return
        layer.setSubsetString(filter)
        self.settings.iface.mapCanvas().refresh()
        self.settings.iface.legendInterface().refreshLayerSymbology(layer)


    def zoomToLayers(self, includeBuffers):
        self.pointsLayer.updateExtents()
        self.linesLayer.updateExtents()
        self.polygonsLayer.updateExtents()
        self.schematicLayer.updateExtents()
        extent = QgsRectangle()
        extent = self.extendExtent(extent, self.pointsLayer)
        extent = self.extendExtent(extent, self.linesLayer)
        extent = self.extendExtent(extent, self.polygonsLayer)
        extent = self.extendExtent(extent, self.schematicLayer)
        if includeBuffers:
            self.pointsBuffer.updateExtents()
            self.linesBuffer.updateExtents()
            self.polygonsBuffer.updateExtents()
            self.schematicBuffer.updateExtents()
            extent = self.extendExtent(extent, self.pointsBuffer)
            extent = self.extendExtent(extent, self.linesBuffer)
            extent = self.extendExtent(extent, self.polygonsBuffer)
            extent = self.extendExtent(extent, self.schematicBuffer)
        if (extent is not None and not extent.isNull()):
            extent.scale(1.05)
            self.settings.iface.mapCanvas().setExtent(extent)
            self.settings.iface.mapCanvas().refresh()


    def extendExtent(self, extent, layer):
        layerExtent = QgsRectangle()
        if (layer is not None and layer.isValid() and layer.featureCount() > 0 and self.settings.iface.legendInterface().isLayerVisible(layer)):
            layerExtent = layer.extent()
        if (extent is None and layerExtent is None):
            return QgsRectangle()
        elif (extent is None or extent.isNull()):
            return layerExtent
        elif (layerExtent is None or layerExtent.isNull()):
            return extent
        return extent.combineExtentWith(layerExtent)
