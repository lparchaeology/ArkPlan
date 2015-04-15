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
from PyQt4.QtCore import QVariant, QFile
from PyQt4.QtGui import QMessageBox

from qgis.core import *

from project import *
from layercollection import *

class LayerManager:

    geoLayer = None  #QgsRasterLayer()
    contexts = None  # LayerCollection()
    grid = None  # LayerCollection()

    # Internal variables

    _project = None # Project()


    def __init__(self, project):
        self._project = project
        # If the legend indexes change make sure we stay updated
        self._project.iface.legendInterface().groupIndexChanged.connect(self._groupIndexChanged)


    def initialise(self):
        self.contexts = self._createCollection('contexts')
        self.contexts.initialise()
        self.grid = self._createCollection('grid')
        self.grid.initialise()


    def unload(self):
        if self.contexts is not None:
            self.contexts.unload()
        if self.grid is not None:
            self.grid.unload()


    def _groupIndexChanged(self, oldIndex, newIndex):
        if (oldIndex == self._project.projectGroupIndex):
            self._project.projectGroupIndex = newIndex


    def loadGeoLayer(self, geoFile):
        #TODO Check if already loaded, remove old one?
        self.geoLayer = QgsRasterLayer(geoFile.absoluteFilePath(), geoFile.completeBaseName())
        self.geoLayer.renderer().setOpacity(self._project.planTransparency()/100.0)
        QgsMapLayerRegistry.instance().addMapLayer(self.geoLayer)
        if (self._project.planGroupIndex < 0):
            self._project.planGroupIndex = self.getGroupIndex(self._project.planGroupName)
        self._project.iface.legendInterface().moveLayer(self.geoLayer, self._project.planGroupIndex)
        self._project.iface.mapCanvas().setExtent(self.geoLayer.extent())


    def applyContextFilter(self, contextList):
        self.contexts.applyFieldFilter(self._project.contextAttributeName, contextList)


    def _shapeFile(self, layerPath, layerName):
        return layerPath + '/' + layerName + '.shp'


    def _styleFile(self, layerPath, layerName, baseName, defaultName):
        # First see if the layer itself has a default style saved
        filePath = layerPath + '/' + layerName + '.qml'
        if QFile.exists(filePath):
            return filePath
        # Next see if the base name has a style in the styles folder (which may be a special folder, the site folder or the plugin folder)
        filePath = self._project.stylePath() + '/' + baseName + '.qml'
        if QFile.exists(filePath):
            return filePath
        # Next see if the default name has a style in the style folder
        filePath = self._project.stylePath() + '/' + defaultName + '.qml'
        if QFile.exists(filePath):
            return filePath
        # Finally, check the plugin folder for the default style
        filePath = self._project.stylePath() + '/' + defaultName + '.qml'
        if QFile.exists(filePath):
            return filePath
        # If we didn't find that then something is wrong!
        return ''


    def _createCollection(self, module):
        path = self._project.modulePath(module)
        lcs = LayerCollectionSettings()
        lcs.collectionGroupName = self._project.layersGroupName(module)
        lcs.buffersGroupName = self._project.buffersGroupName(module)
        lcs.bufferSuffix = self._project.bufferSuffix
        lcs.pointsLayerProvider = 'ogr'
        lcs.pointsLayerName = self._project.pointsLayerName(module)
        lcs.pointsLayerPath = self._shapeFile(path, lcs.pointsLayerName)
        lcs.pointsStylePath = self._styleFile(path, lcs.pointsLayerName, self._project.pointsBaseName(module), self._project.pointsBaseNameDefault(module))
        lcs.linesLayerProvider = 'ogr'
        lcs.linesLayerName = self._project.linesLayerName(module)
        lcs.linesLayerPath = self._shapeFile(path, lcs.linesLayerName)
        lcs.linesStylePath = self._styleFile(path, lcs.linesLayerName, self._project.linesBaseName(module), self._project.linesBaseNameDefault(module))
        lcs.polygonsLayerProvider = 'ogr'
        lcs.polygonsLayerName = self._project.polygonsLayerName(module)
        lcs.polygonsLayerPath = self._shapeFile(path, lcs.polygonsLayerName)
        lcs.polygonsStylePath = self._styleFile(path, lcs.polygonsLayerName, self._project.polygonsBaseName(module), self._project.polygonsBaseNameDefault(module))
        lcs.schemaLayerProvider = 'ogr'
        lcs.schemaLayerName = self._project.schemaLayerName(module)
        lcs.schemaLayerPath = self._shapeFile(self._project.modulePath(module), lcs.schemaLayerName)
        lcs.schemaStylePath = self._styleFile(self._project.modulePath(module), lcs.schemaLayerName, self._project.schemaBaseName(module), self._project.schemaBaseNameDefault(module))
        return LayerCollection(self._project.iface, lcs)

