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

from PyQt4.QtCore import pyqtSignal
from PyQt4.QtGui import QAction, QIcon

from qgis.core import QgsMapLayerRegistry, QgsProject, QgsVectorLayer
from qgis.gui import QgisInterface

import .Snapping


class LayerSnappingEnabledAction(QAction):

    """Action for Layer Snapping Enabled."""

    _layerId = ''
    _iface = None  # QgisInteface

    snappingEnabledChanged = pyqtSignal(str, bool)

    def __init__(self, snapLayer, parent=None):
        super(LayerSnappingEnabledAction, self).__init__(parent)

        if isinstance(snapLayer, QgisInterface):
            self._iface = snapLayer
        elif isinstance(snapLayer, QgsVectorLayer):
            self._layerId = snapLayer.id()
        elif isinstance(snapLayer, str) or isinstance(snapLayer, unicode):
            self._layerId = snapLayer

        self.setCheckable(True)
        self.setText('Toggle Layer Snapping')
        self.setStatusTip('Toggle snapping on this layer')
        self.setIcon(QIcon(':/plugins/ark/snapEnable.png'))

        self._refresh()
        self.triggered.connect(self._triggered)

        # Make sure we catch changes in the main snapping dialog
        QgsProject.instance().snapSettingsChanged.connect(self._refresh)
        # If using current layer, make sure we update when it changes
        if self._iface:
            self._iface.legendInterface().currentLayerChanged.connect(self._refresh)
        # If the layer is removed then disable the button
        QgsMapLayerRegistry.instance().layerRemoved.connect(self._layerRemoved)
        # If we change the settings, make such others are told
        self.snappingEnabledChanged.connect(QgsProject.instance().snapSettingsChanged)

    def unload(self):
        self._layerRemoved(self._layerId)
        if self._iface:
            self._iface.legendInterface().currentLayerChanged.disconnect(self._refresh)

    def layerId(self):
        if self._iface and self._iface.legendInterface().currentLayer():
            return self._iface.legendInterface().currentLayer().id()
        return self._layerId

    # Private API

    def _layerRemoved(self, layerId):
        if self._layerId and layerId == self._layerId:
            self._layerId = ''
            self.setEnabled(False)
            QgsProject.instance().snapSettingsChanged.disconnect(self._refresh)
            QgsMapLayerRegistry.instance().layerRemoved.disconnect(self._layerRemoved)
            self.snappingEnabledChanged.disconnect(QgsProject.instance().snapSettingsChanged)

    def _triggered(self, status):
        layerId = self.layerId()
        if layerId:
            Snapping.setLayerSnappingEnabled(layerId, status)
            self.snappingEnabledChanged.emit(layerId, status)

    def _refresh(self):
        self.blockSignals(True)
        if self._layerId or self._iface:
            self.setChecked(Snapping.layerSnappingEnabled(self.layerId()))
            self.setEnabled(Snapping.snappingMode() == Snapping.SelectedLayers)
        else:
            self.setChecked(False)
            self.setEnabled(False)
        self.blockSignals(False)
