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

from qgis.core import QGis, QgsMapLayer, QgsMapLayerRegistry, QgsVectorDataProvider
from qgis.gui import QgsMapLayerComboBox

from update_layer_dialog_base import *

class UpdateLayerDialog(QDialog, Ui_UpdateLayerDialog):

    def __init__(self, iface, parent=None):
        super(UpdateLayerDialog, self).__init__(parent)
        self.setupUi(self)
        for layer in iface.legendInterface().layers():
            if (layer.type() == QgsMapLayer.VectorLayer and (layer.dataProvider().capabilities() & QgsVectorDataProvider.ChangeAttributeValues)):
                if (layer.geometryType() == QGis.Point or layer.geometryType() == QGis.NoGeometry):
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

    def createCrsFields(self):
        return self.createCrsFieldsCheck.isChecked()
