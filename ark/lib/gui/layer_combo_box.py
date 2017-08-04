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

from PyQt4.QtCore import pyqtSignal, QFileInfo, QFile, QSettings
from PyQt4.QtGui import QDialog, QComboBox, QDialogButtonBox, QColor
from PyQt4.QtXml import QDomImplementation, QDomDocument

from qgis.core import QGis, QgsMapLayer, QgsMapLayerRegistry, QgsVectorLayer, QgsVectorFileWriter, QgsProject, QgsLayerTreeGroup, NULL, QgsFeature, QgsFeatureRequest
from qgis.gui import QgsHighlight

import utils
from project import Project
from canvas_items import GeometryHighlight, FeatureHighlight

# Layer Widgets

class LayerComboBox(QComboBox):

    layerChanged = pyqtSignal()

    _layerType = None
    _geometryType = None
    _iface = None

    def __init__(self, iface, layerType=None, geometryType=None, parent=None):
        super(ArkLayerComboBox, self).__init__(parent)
        self._iface = iface
        self._layerType = layerType
        self._geometryType = geometryType
        self._loadLayers()

    def _addLayer(self, layer):
        self.addItem(layer.name(), layer.id())

    def _loadLayers(self):
        self.clear()
        for layer in self._iface.legendInterface().layers():
            if self._layerType is None and self._geometryType is None:
                self._addLayer(layer)
            elif (self._layerType == QgsMapLayer.RasterLayer and layer.type() == QgsMapLayer.RasterLayer):
                self._addLayer(layer)
            elif layer.type() == QgsMapLayer.VectorLayer:
                if (self._geometryType == None or layer.geometryType() == self._geometryType):
                    self._addLayer(layer)
