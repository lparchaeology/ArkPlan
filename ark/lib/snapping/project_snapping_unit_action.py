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

from .abstract_snapping_unit_action import AbstractSnappingUnitAction
from .snapping_ import Snapping


class ProjectSnappingUnitAction(AbstractSnappingUnitAction):

    """Action to change Snapping Unit for a project."""

    snappingUnitChanged = pyqtSignal(int)

    def __init__(self, snapUnit, parent=None):
        super(ProjectSnappingUnitAction, self).__init__(snapUnit, parent)

        # Make sure we catch changes in the main snapping dialog
        QgsProject.instance().snapSettingsChanged.connect(self._refresh)
        # If a new project is read, update to that project's setting
        QgsProject.instance().readProject.connect(self._refresh)
        # If we change the settings, make such others are told
        self.snappingUnitChanged.connect(QgsProject.instance().snapSettingsChanged)

    def unload(self):
        QgsProject.instance().snapSettingsChanged.disconnect(self._refresh)
        QgsProject.instance().readProject.disconnect(self._refresh)
        self.snappingUnitChanged.disconnect(QgsProject.instance().snapSettingsChanged)

    # Private API

    def _triggered(self, checked):
        if checked:
            Snapping.setProjectSnappingUnit(self._snapUnit)
            self.snappingUnitChanged.emit(self._snapUnit)

    def _refresh(self):
        self.blockSignals(True)
        self.setChecked(Snapping.projectSnappingUnit() == self._snapUnit)
        self.setEnabled(Snapping.snappingMode() != Snapping.SelectedLayers)
        self.blockSignals(False)
