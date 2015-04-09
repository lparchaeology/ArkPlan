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
from layercollection import *

class LayerManager:

    geoLayer = QgsRasterLayer()
    contexts = None  # LayerCollection()
    grid = None  # LayerCollection()

    # Internal variables

    _settings = None # Settings()

    def __init__(self, settings):
        self._settings = settings
        # If the legend indexes change make sure we stay updated
        self._settings.iface.legendInterface().groupIndexChanged.connect(self._groupIndexChanged)

        # Configure the context layers settings
        cs = LayerCollectionSettings()
        collectionDir = settings.contextsDir()
        collectionCrs = settings.projectCrs()
        collectionGroupName = settings.contextsGroupName()
        bufferGroupName = settings.contextsBufferGroupName()
        bufferSuffix = settings.bufferSuffix
        pointsLayerName = settings.contextPointsLayerName()
        pointsLayerPath = ''
        pointsStylePath = ''
        pointsLayerFields = QgsFields()
        linesLayerName = ''
        linesLayerPath = ''
        linesStylePath = ''
        linesLayerFields = QgsFields()

        polygonsLayerName = ''
        polygonsLayerPath = ''
        polygonsStylePath = ''
        polygonsLayerFields = QgsFields()

        # Scope, Boundary, Reach, Dimension, Schematic???
        scopeLayerName = ''
        scopeLayerPath = ''
        scopeStylePath = ''
        scopeLayerFields = QgsFields()


    def initialise(self):
        self.grid.initialise()
        self.contexts.initialise()

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
        clause = '"' + self._settings.contextAttributeName + '" = %d'
        filter = ''
        if (len(contextList) > 0):
            filter += clause % contextList[0]
            for context in contextList[1:]:
                filter += ' or '
                filter += clause % context
        self.contexts.applyFilter(filter)
