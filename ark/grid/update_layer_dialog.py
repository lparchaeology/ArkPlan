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

from qgis.PyQt.QtWidgets import QDialog

from qgis.core import QgsMapLayer, QgsMapLayerRegistry, QgsVectorDataProvider, QgsWkbTypes

from .ui.update_layer_dialog_base import Ui_UpdateLayerDialog


class UpdateLayerDialog(QDialog, Ui_UpdateLayerDialog):

    def __init__(self, iface, parent=None):
        super().__init__(parent)
        self.setupUi(self)
        for layer in iface.legendInterface().layers():
            if (layer.type() == QgsMapLayer.VectorLayer
                    and (layer.dataProvider().capabilities() & QgsVectorDataProvider.ChangeAttributeValues)):
                if (layer.geometryType() == QgsWkbTypes.PointGeometry or layer.geometryType() == QgsWkbTypes.NullGeometry):
                    self.layerComboBox.addItem(layer.name(), layer.id())

    def layer(self):
        return QgsMapLayerRegistry.instance().mapLayer(self.layerId())

    def layerName(self):
        return self.layerComboBox.currentText()

    def layerId(self):
        return self.layerComboBox.itemData(self.layerComboBox.currentIndex())

    def updateGeometry(self):
        return self.updateGeometryButton.isChecked()

    def updateFields(self):
        return self.updateFieldsButton.isChecked()

    def createLocalFields(self):
        return self.createLocalFieldsCheck.isChecked()

    def createMapFields(self):
        return self.createMapFieldsCheck.isChecked()
