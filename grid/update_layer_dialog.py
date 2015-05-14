# -*- coding: utf-8 -*-
"""
/***************************************************************************
                                      Ark
                                 A QGIS plugin
             QGIS Plugin for ARK, the Archaeological Recording Kit
                              -------------------
        begin                : 2015-05-14
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

from qgis.core import QGis, QgsMapLayer, QgsMapLayerRegistry
from qgis.gui import QgsMapLayerComboBox

from update_layer_dialog_base import *

class UpdateLayerDialog(QDialog, Ui_UpdateLayerDialog):

    _layerName = ''
    _layerId = -1
    _layerType = None
    _geometryType = None
    _iface = None

    def __init__(self, iface, parent=None):
        super(UpdateLayerDialog, self).__init__(parent)
        self.setupUi(self)
        self.layerComboBox.currentIndexChanged.connect(self.layerChanged)
        self._iface = iface
        self.layerComboBox.clear()
        for layer in self._iface.legendInterface().layers():
            if layer.type() == QgsMapLayer.VectorLayer:
                if (layer.geometryType() == QGis.Point or layer.geometryType() == QGis.NoGeometry):
                    self.layerComboBox.addItem(layer.name(), layer.id())
        self.layerChanged(self.layerComboBox.currentIndex())

    def layer(self):
        return QgsMapLayerRegistry.instance().mapLayer(self.layerId())

    def layerName(self):
        return self._layerName

    def layerId(self):
        return self._layerId

    def layerChanged(self, index):
        self._layerName = self.layerComboBox.currentText()
        self._layerId = self.layerComboBox.itemData(self.layerComboBox.currentIndex())
        if self.layer().geometryType() == QGis.Point:
            self._toggleUpdateType(True)
        elif self.layer().geometryType() == QGis.NoGeometry:
            self._toggleUpdateType(True)

    def _toggleUpdateType(self, hasGeometry):
        self.updateFieldsButton.setEnabled(hasGeometry)
        self.updateGeometryFromLocalButton.setEnabled(hasGeometry)
        self.updateGeometryFromCrsButton.setEnabled(hasGeometry)
        self.updateLocalFieldsButton.setDisabled(hasGeometry)
        self.updateCrsFieldsButton.setDisabled(hasGeometry)
