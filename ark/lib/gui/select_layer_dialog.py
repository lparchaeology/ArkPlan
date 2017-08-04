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

from PyQt4.QtGui import QDialog, QDialogButtonBox

from qgis.core import QgsMapLayerRegistry

# Layer Widgets

class SelectLayerDialog(QDialog):

    def __init__(self, iface, text='', label='', layerType=None, geometryType=None, parent=None):

        self.setWindowTitle(self.tr("Select Layer"))

        self._dialogLayout = QtGui.QVBoxLayout(self)

        if text:
            self._textLabel = QtGui.QLabel(self)
            self._textLabel.setText(text)
            self._dialogLayout.addWidget(self._textLabel)

        if (label or not text):
            self._comboLabel = QtGui.QLabel(self)
            if label:
                self._comboLabel.setText(label)
            elif not text:
                self._comboLabel.setText(self.tr('Layer:'))
            self._comboBox = ArkLayerComboBox(iface, layerType, geometryType, self)
            self._comboLayout = QtGui.QHBoxLayout()
            self._comboLayout.addWidget(self._comboLabel)
            self._comboLayout.addWidget(self._comboBox)
            self._dialogLayout.addLayout(self._comboLayout)
        else:
            self._comboBox = ArkLayerComboBox(iface, layerType, geometryType, self)
            self._dialogLayout.addWidget(self._comboBox)

        self._buttonBox = QDialogButtonBox(QDialogButtonBox.Ok | QDialogButtonBox.Cancel, Qt.Horizontal, self)
        self._buttonBox.accepted.connect(self.accept)
        self._buttonBox.rejected.connect(self.reject)
        self._comboLayout.addWidget(self._buttonBox)

    def layer(self):
        return QgsMapLayerRegistry.instance().mapLayer(self.layerId())

    def layerName(self):
        return self.layerComboBox.currentText()

    def layerId(self):
        return self.layerComboBox.itemData(self.layerComboBox.currentIndex())
