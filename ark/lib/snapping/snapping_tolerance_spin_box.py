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
from PyQt4.QtGui import QDoubleSpinBox

from qgis.core import QgsProject

from .. import utils
from .snapping_ import Snapping


class SnappingToleranceSpinBox(QDoubleSpinBox):

    snappingToleranceChanged = pyqtSignal(float)

    _iface = None

    def __init__(self, parent=None):

        super(SnappingToleranceSpinBox, self).__init__(parent)

        self.setDecimals(5)
        self.setRange(0.0, 100000000.0)

        self._refresh()
        self.valueChanged.connect(self._changed)

        # Make sure we catch changes in the main snapping dialog
        QgsProject.instance().snapSettingsChanged.connect(self._refresh)
        # If a new project is read, update to that project's setting
        QgsProject.instance().readProject.connect(self._refresh)
        self.snappingToleranceChanged.connect(QgsProject.instance().snapSettingsChanged)

    def setIface(self, iface):
        self._iface = iface
        self._refresh()

    # Private API

    def _changed(self, idx):
        Snapping.setProjectSnappingTolerance(self.value())
        self.snappingToleranceChanged.emit(self.value())

    def _refresh(self):
        self.setValue(Snapping.projectSnappingTolerance())
        unit = Snapping.projectSnappingUnit()
        if (unit == Snapping.Pixels):
            self.setSuffix(' px')
        elif self._iface is None:
            self.setSuffix('')
        elif unit == Snapping.LayerUnits:  # == MapUnits
            layerUnits = None
            mode = Snapping.snappingMode()
            if mode == Snapping.CurrentLayer:
                layerUnits = self._iface.mapCanvas().currentLayer().crs().mapUnits()
            else:
                # TODO Find out the correct option here for all_layers!
                layerUnits = self._iface.mapCanvas().mapUnits()
            suffix = utils.unitToSuffix(layerUnits)
            self.setSuffix(suffix)
        elif unit == Snapping.ProjectUnits:
            projectUnits = self._iface.mapCanvas().mapUnits()
            suffix = utils.unitToSuffix(projectUnits)
            self.setSuffix(suffix)
