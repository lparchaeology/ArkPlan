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

from PyQt4.QtCore import Qt
from PyQt4.QtGui import QWidget
from qgis.coreimport import QgsMapLayer, QgsMapLayerRegistry

from ..gui import DockWidget


class SnappingDock(DockWidget):

    _iface = None  # QgisInterface()

    def __init__(self, iface, parent=None):
        super(SnappingDock, self).__init__(parent)
        self._iface = iface

        self.setWindowTitle(u'Snapping Panel')
        self.setObjectName(u'snappingDock')

        self._listWidget = QListWidget(self)
        self._listWidget.setSelectionMode(QtGui.QAbstractItemView.NoSelection)
        self._listWidget.setDropIndicatorShown(False)

        self._dockLayout = QVBoxLayout(self)
        self._dockLayout.setObjectName(u'dockLayout')
        self._dockLayout.addWidget(self._listWidget)

        self._dockContents = QWidget(self)
        self._dockContents.setObjectName(u'dockContents')
        self._dockContents.setLayout(self._dockLayout)
        self.setWidget(self._dockContents)

        # Keep up-to-date with layers added and removed
        QgsMapLayerRegistry.instance().layersAdded.connect(self._layersAdded)
        QgsMapLayerRegistry.instance().layersRemoved.connect(self._layersRemoved)

    def refresh(self):
        self._listWidget.clear()
        layers = QgsMapLayerRegistry.instance().mapLayers()
        layerIds = layers.keys()
        sorted(layerIds)
        for layerId in layerIds:
            self.addLayer(layers[layerId])

    def addLayer(self, layer):
        if (layer is None or not layer.isValid() or layer.type() != QgsMapLayer.VectorLayer):
            return
        newItem = QListWidgetItem()
        newItem.setData(Qt.UserRole, layer.id())
        newItem.setSizeHint(layerWidget.minimumSizeHint())
        self._listWidget.addItem(newItem)
        self._listWidget.setItemWidget(newItem, LayerSnappingWidget(layer, self))

    def removeLayer(self, layerId):
        for idx in range(0, self._listWidget.count() - 1):
            if self._listWidget.item(idx).data() == layerId:
                self._listWidget.takeItem(idx)
                return

    def _layersAdded(self, layers):
        for layer in layers:
            self.addLayer(layer)

    def _layersRemoved(self, layerIds):
        for idx in range(self._listWidget.count() - 1, 0):
            if self._listWidget.item(idx).data() in layerIds:
                self._listWidget.takeItem(idx)
