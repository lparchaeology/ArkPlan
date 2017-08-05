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
from qgis.core import QgsMapLayerRegistry, QgsProject, QgsVectorLayer
from qgis.gui import QgisInterface

import .AbstractSnappingToleranceAction
import .Snapping


class LayerSnappingToleranceAction(AbstractSnappingToleranceAction):

    """Action to change Layer Snapping Tolerance."""

    snappingToleranceChanged = pyqtSignal(str, float)

    _layerId = ''
    _iface = None  # QgisInteface

    def __init__(self, snapLayer, parent=None):
        super(LayerSnappingToleranceAction, self).__init__(parent)

        if isinstance(snapLayer, QgisInterface):
            self._iface = snapLayer
        elif isinstance(snapLayer, QgsVectorLayer):
            self._layerId = snapLayer.id()
        elif isinstance(snapLayer, str) or isinstance(snapLayer, unicode):
            self._layerId = snapLayer

        self._refresh()

        # Make sure we catch changes in the main snapping dialog
        QgsProject.instance().snapSettingsChanged.connect(self._refresh)
        # If using current layer, make sure we update when it changes
        if self._iface and self._layerId == '':
            self._iface.legendInterface().currentLayerChanged.connect(self._refresh)
        # If the layer is removed then disable the button
        QgsMapLayerRegistry.instance().layerRemoved.connect(self._layerRemoved)
        # If we change the settings, make such others are told
        self.snappingToleranceChanged.connect(QgsProject.instance().snapSettingsChanged)

    def unload(self):
        QgsProject.instance().snapSettingsChanged.disconnect(self._refresh)
        if self._iface and self._layerId == '':
            self._iface.legendInterface().currentLayerChanged.disconnect(self._refresh)
        QgsMapLayerRegistry.instance().layerRemoved.disconnect(self._layerRemoved)
        self.snappingToleranceChanged.disconnect(QgsProject.instance().snapSettingsChanged)

    def layerId(self):
        if self._iface and self._layerId == '' and self._iface.legendInterface().currentLayer():
            return self._iface.legendInterface().currentLayer().id()
        return self._layerId

    def setInterface(self, iface):
        self._iface = iface
        self._refresh()

    # Private API

    def _layerRemoved(self, layerId):
        if layerId == self._layerId:
            self._layerId = ''
            self.setEnabled(False)
            QgsProject.instance().snapSettingsChanged.disconnect(self._refresh)
            QgsMapLayerRegistry.instance().layerRemoved.disconnect(self._layerRemoved)
            self.snappingToleranceChanged.disconnect(QgsProject.instance().snapSettingsChanged)

    def _changed(self, tolerance):
        layerId = self.layerId()
        if layerId:
            Snapping.setLayerSnappingTolerance(layerId, tolerance)
            self.snappingToleranceChanged.emit(layerId, tolerance)

    def _refresh(self):
        self.blockSignals(True)
        self._toleranceSpin.blockSignals(True)
        layerId = self.layerId()
        if layerId:
            self._toleranceSpin.setValue(Snapping.layerSnappingTolerance(layerId))
            unit = Snapping.layerSnappingUnit(layerId)
            if (unit == Snapping.Pixels):
                self._toleranceSpin.setSuffix(' px')
            elif self._iface == None:
                self._toleranceSpin.setSuffix('')
            elif unit == Snapping.LayerUnits:
                layerUnits = QgsMapLayerRegistry.instance().mapLayer(layerId).crs().mapUnits()
                suffix = _unitToSuffix(layerUnits)
                self._toleranceSpin.setSuffix(suffix)
            elif unit == Snapping.ProjectUnits:
                projectUnits = self._iface.mapCanvas().mapUnits()
                suffix = _unitToSuffix(projectUnits)
                self._toleranceSpin.setSuffix(suffix)
            self.setEnabled(Snapping.snappingMode() == Snapping.SelectedLayers)
        else:
            self._toleranceSpin.setValue(0.0)
            self._toleranceSpin.setSuffix('')
            self.setEnabled(False)
        self._toleranceSpin.blockSignals(False)
        self.blockSignals(False)
