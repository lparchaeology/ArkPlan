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

from qgis.PyQt.QtCore import pyqtSignal

from qgis.core import QgsProject

from .. import utils
from .abstract_snapping_tolerance_action import AbstractSnappingToleranceAction
from .snapping_ import Snapping, SnappingMode, SnappingUnit


class ProjectSnappingToleranceAction(AbstractSnappingToleranceAction):

    """Action to change Project Snapping Tolerance."""

    snappingToleranceChanged = pyqtSignal(float)

    def __init__(self, parent=None):
        super().__init__(parent)

        self._iface = None

        # Make sure we catch changes in the main snapping dialog
        QgsProject.instance().snapSettingsChanged.connect(self._refresh)
        # If a new project is read, update to that project's setting
        QgsProject.instance().readProject.connect(self._refresh)
        # If we change the settings, make such others are told
        self.snappingToleranceChanged.connect(QgsProject.instance().snapSettingsChanged)

    def unload(self):
        QgsProject.instance().snapSettingsChanged.disconnect(self._refresh)
        QgsProject.instance().readProject.disconnect(self._refresh)
        self.snappingToleranceChanged.disconnect(QgsProject.instance().snapSettingsChanged)

    def setInterface(self, iface):
        self._iface = iface
        self._refresh()

    # Private API

    def _changed(self, tolerance):
        Snapping.setProjectSnappingTolerance(tolerance)
        self.snappingToleranceChanged.emit(tolerance)

    def _refresh(self):
        self.blockSignals(True)
        self._toleranceSpin.blockSignals(True)
        self._toleranceSpin.setValue(Snapping.projectSnappingTolerance())
        unit = Snapping.projectSnappingUnit()
        if (unit == SnappingUnit.Pixels):
            self._toleranceSpin.setSuffix(' px')
        elif self._iface is None:
            self._toleranceSpin.setSuffix('')
        elif unit == SnappingUnit.LayerUnits:  # == MapUnits
            layerUnits = None
            mode = Snapping.snappingMode()
            if mode == SnappingMode.CurrentLayer:
                layerUnits = self._iface.mapCanvas().currentLayer().crs().mapUnits()
            else:
                # TODO Find out the correct option here for all_layers!
                layerUnits = self._iface.mapCanvas().mapUnits()
            suffix = utils.unitToSuffix(layerUnits)
            self._toleranceSpin.setSuffix(suffix)
        elif unit == SnappingUnit.ProjectUnits:
            projectUnits = self._iface.mapCanvas().mapUnits()
            suffix = utils.unitToSuffix(projectUnits)
            self._toleranceSpin.setSuffix(suffix)
        self.setEnabled(Snapping.snappingMode() != SnappingMode.SelectedLayers)
        self._toleranceSpin.blockSignals(False)
        self.blockSignals(False)
