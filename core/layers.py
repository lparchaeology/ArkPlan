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

from settings import *
from layercollection import *

class LayerManager:

    geoLayer = None  #QgsRasterLayer()
    contexts = None  # LayerCollection()
    grid = None  # LayerCollection()

    # Internal variables

    _settings = None # Settings()


    def __init__(self, settings):
        self._settings = settings
        # If the legend indexes change make sure we stay updated
        self._settings.iface.legendInterface().groupIndexChanged.connect(self._groupIndexChanged)


    def initialise(self):
        self.contexts = self._createContextsCollection()
        self.contexts.initialise()
        self.grid = self._createGridCollection()
        self.grid.initialise()


    def unload(self):
        self.contexts.unload()
        self.grid.unload()


    def _groupIndexChanged(self, oldIndex, newIndex):
        if (oldIndex == self._settings.projectGroupIndex):
            self._settings.projectGroupIndex = newIndex


    def loadGeoLayer(self, geoFile):
        #TODO Check if already loaded, remove old one?
        self.geoLayer = QgsRasterLayer(geoFile.absoluteFilePath(), geoFile.completeBaseName())
        self.geoLayer.renderer().setOpacity(self._settings.planTransparency()/100.0)
        QgsMapLayerRegistry.instance().addMapLayer(self.geoLayer)
        if (self._settings.planGroupIndex < 0):
            self._settings.planGroupIndex = self.getGroupIndex(self._settings.planGroupName)
        self._settings.iface.legendInterface().moveLayer(self.geoLayer, self._settings.planGroupIndex)
        self._settings.iface.mapCanvas().setExtent(self.geoLayer.extent())


    def applyContextFilter(self, contextList):
        self.contexts.applyFilter(self._settings.contextAttributeName, contextList)


    def _shapeFile(self, layerPath, layerName):
        return layerPath + '/' + layerName + '.shp'


    def _styleFile(self, layerPath, layerName, baseName, defaultName):
        # First see if the layer itself has a default style saved
        filePath = layerPath + '/' + layerName + '.qml'
        if QFile.exists(filePath):
            return filePath
        # Next see if the base name has a style in the styles folder (which may be a special folder, the site folder or the plugin folder)
        filePath = self._settings.stylePath() + '/' + baseName + '.qml'
        if QFile.exists(filePath):
            return filePath
        # Next see if the default name has a style in the style folder
        filePath = self._settings.stylePath() + '/' + defaultName + '.qml'
        if QFile.exists(filePath):
            return filePath
        # Finally, check the plugin folder for the default style
        filePath = self._settings.stylePath() + '/' + defaultName + '.qml'
        if QFile.exists(filePath):
            return filePath
        # If we didn't find that then something is wrong!
        return ''


    def _createContextsCollection(self):
        cs = LayerCollectionSettings()
        cs.collectionDir = self._settings.contextsDir()
        cs.collectionCrs = self._settings.projectCrs()
        cs.collectionGroupName = self._settings.contextsGroupName()
        cs.bufferGroupName = self._settings.contextsBufferGroupName()
        cs.bufferSuffix = self._settings.bufferSuffix
        cs.pointsLayerName = self._settings.contextsPointsLayerName()
        cs.pointsLayerPath = self._shapeFile(self._settings.contextsPath(), cs.pointsLayerName)
        cs.pointsStylePath = self._styleFile(self._settings.contextsPath(), cs.pointsLayerName, self._settings.contextsPointsBaseName(), self._settings.contextsPointsBaseNameDefault)
        cs.pointsLayerFields = QgsFields()
        cs.linesLayerName = self._settings.contextsLinesLayerName()
        cs.linesLayerPath = self._shapeFile(self._settings.contextsPath(), cs.linesLayerName)
        cs.linesStylePath = self._styleFile(self._settings.contextsPath(), cs.linesLayerName, self._settings.contextsLinesBaseName(), self._settings.contextsLinesBaseNameDefault)
        cs.linesLayerFields = QgsFields()
        cs.polygonsLayerName = self._settings.contextsPolygonsLayerName()
        cs.polygonsLayerPath = self._shapeFile(self._settings.contextsPath(), cs.polygonsLayerName)
        cs.polygonsStylePath = self._styleFile(self._settings.contextsPath(), cs.polygonsLayerName, self._settings.contextsPolygonsBaseName(), self._settings.contextsPolygonsBaseNameDefault)
        cs.polygonsLayerFields = QgsFields()
        cs.scopeLayerName = self._settings.contextsScopeLayerName()
        cs.scopeLayerPath = self._shapeFile(self._settings.contextsPath(), cs.scopeLayerName)
        cs.scopeStylePath = self._styleFile(self._settings.contextsPath(), cs.scopeLayerName, self._settings.contextsScopeBaseName(), self._settings.contextsScopeBaseNameDefault)
        cs.scopeLayerFields = QgsFields()
        cc = LayerCollection(self._settings.iface, cs)
        return cc


    def _createGridCollection(self):
        gs = LayerCollectionSettings()
        gs.collectionDir = self._settings.gridDir()
        gs.collectionCrs = self._settings.projectCrs()
        gs.collectionGroupName = self._settings.gridGroupName()
        gs.bufferGroupName = self._settings.gridGroupName()
        gs.bufferSuffix = self._settings.bufferSuffix
        gs.pointsLayerName = self._settings.gridPointsLayerName()
        gs.pointsLayerPath = self._shapeFile(self._settings.gridPath(), gs.pointsLayerName)
        gs.pointsStylePath = self._styleFile(self._settings.gridPath(), gs.pointsLayerName, self._settings.gridPointsBaseName(), self._settings.gridPointsBaseNameDefault)
        gs.pointsLayerFields = QgsFields()
        gs.linesLayerName = self._settings.gridLinesLayerName()
        gs.linesLayerPath = self._shapeFile(self._settings.gridPath(), gs.linesLayerName)
        gs.linesStylePath = self._styleFile(self._settings.gridPath(), gs.linesLayerName, self._settings.gridLinesBaseName(), self._settings.gridLinesBaseNameDefault)
        gs.linesLayerFields = QgsFields()
        gs.polygonsLayerName = self._settings.gridPolygonsLayerName()
        gs.polygonsLayerPath = self._shapeFile(self._settings.gridPath(), gs.polygonsLayerName)
        gs.polygonsStylePath = self._styleFile(self._settings.gridPath(), gs.polygonsLayerName, self._settings.gridPolygonsBaseName(), self._settings.gridPolygonsBaseNameDefault)
        gs.polygonsLayerFields = QgsFields()
        gc = LayerCollection(self._settings.iface, gs)
        return gc
