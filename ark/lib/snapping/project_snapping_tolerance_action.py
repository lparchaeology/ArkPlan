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

from qgis.core import QgsProject

import .AbstractSnappingToleranceAction
import .Snapping


class ProjectSnappingToleranceAction(AbstractSnappingToleranceAction):

    """Action to change Project Snapping Tolerance."""

    snappingToleranceChanged = pyqtSignal(float)

    _iface = None

    def __init__(self, parent=None):
        super(ProjectSnappingToleranceAction, self).__init__(parent)

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
        if (unit == Snapping.Pixels):
            self._toleranceSpin.setSuffix(' px')
        elif self._iface is None:
            self._toleranceSpin.setSuffix('')
        elif unit == Snapping.LayerUnits:  # == MapUnits
            layerUnits = None
            mode = Snapping.snappingMode()
            if mode == Snapping.CurrentLayer:
                layerUnits = self._iface.mapCanvas().currentLayer().crs().mapUnits()
            else:
                # TODO Find out the correct option here for all_layers!
                layerUnits = self._iface.mapCanvas().mapUnits()
            suffix = _unitToSuffix(layerUnits)
            self._toleranceSpin.setSuffix(suffix)
        elif unit == Snapping.ProjectUnits:
            projectUnits = self._iface.mapCanvas().mapUnits()
            suffix = _unitToSuffix(projectUnits)
            self._toleranceSpin.setSuffix(suffix)
        self.setEnabled(Snapping.snappingMode() != Snapping.SelectedLayers)
        self._toleranceSpin.blockSignals(False)
        self.blockSignals(False)
