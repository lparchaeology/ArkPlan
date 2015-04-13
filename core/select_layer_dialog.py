# -*- coding: utf-8 -*-
"""
/***************************************************************************
                                      Ark
                                 A QGIS plugin
             QGIS Plugin for ARK, the Archaeological Recording Kit
                              -------------------
        begin                : 2015-04-13
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

from PyQt4 import uic
from PyQt4.QtGui import QDialog

from qgis.core import QgsMapLayer, QgsMapLayerRegistry

from select_layer_dialog_base import *

class SelectLayerDialog(QDialog, Ui_SelectLayerDialog):

    _layerName = ''
    _layerId = -1
    _layerType = None
    _geometryType = None
    _iface = None

    def __init__(self, iface, layerType=None, geometryType=None, parent=None):
        super(SelectLayerDialog, self).__init__(parent)
        self.setupUi(self)
        self._iface = iface
        self._layerType = layerType
        self._geometryType = geometryType
        self._loadLayers()

    def accept(self):
        self._layerName = self.layerComboBox.currentText()
        self._layerId = self.layerComboBox.itemData(self.layerComboBox.currentIndex())
        return super(SelectLayerDialog, self).accept()

    def layer(self):
        return QgsMapLayerRegistry.instance().mapLayer(self.layerId())

    def layerName(self):
        return self._layerName

    def layerId(self):
        return self._layerId

    def _loadLayers(self):
        self.layerComboBox.clear()
        for layer in self._iface.legendInterface().layers():
            if self._layerType is None and self._geometryType is None:
                self._addLayer(layer)
            elif self._layerType == QgsMapLayer.RasterLayer:
                if layer.type() == QgsMapLayer.RasterLayer:
                    self._addLayer(layer)
            elif layer.type() == QgsMapLayer.VectorLayer:
                if (self._geometryType == None or layer.geometryType() == self._geometryType):
                    self._addLayer(layer)

    def _addLayer(self, layer):
        self.layerComboBox.addItem(layer.name(), layer.id())
