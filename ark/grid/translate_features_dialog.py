# -*- coding: utf-8 -*-
"""
/***************************************************************************
                                ARK Spatial
                    A QGIS plugin for Archaeological Recording.
        Part of the Archaeological Recording Kit by L-P : Archaeology
                        http://ark.lparchaeology.com
                              -------------------
        begin                : 2014-12-07
        git sha              : $Format:%H$
        copyright            : 2014, 2015 by L-P : Heritage LLP
        email                : ark@lparchaeology.com
        copyright            : 2014, 2015 by John Layt
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

from translate_features_dialog_base import *

class TranslateFeaturesDialog(QDialog, Ui_TranslateFeaturesDialog):

    def __init__(self, iface, parent=None):
        super(TranslateFeaturesDialog, self).__init__(parent)
        self.setupUi(self)
        for layer in iface.legendInterface().layers():
            if (layer.type() == QgsMapLayer.VectorLayer and (layer.dataProvider().capabilities() & QgsVectorDataProvider.ChangeAttributeValues)):
                self.layerComboBox.addItem(layer.name(), layer.id())

    def layer(self):
        return QgsMapLayerRegistry.instance().mapLayer(self.layerId())

    def layerName(self):
        return self.layerComboBox.currentText()

    def layerId(self):
        return self.layerComboBox.itemData(self.layerComboBox.currentIndex())

    def translateEast(self):
        return self.translateEastSpin.value()

    def translateNorth(self):
        return self.translateNorthSpin.value()

    def selectedFeatures(self):
        return self.selectedFeaturesButton.isChecked()

    def allFeatures(self):
        return self.allFeaturesButton.isChecked()
