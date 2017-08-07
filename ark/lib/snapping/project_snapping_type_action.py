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

from .abstract_snapping_type_action import AbstractSnappingTypeAction
from .snapping_ import Snapping


class ProjectSnappingTypeAction(AbstractSnappingTypeAction):

    """Action to change Project Snapping Type for a project."""

    snappingTypeChanged = pyqtSignal(int)

    def __init__(self, snapType, parent=None):
        super(ProjectSnappingTypeAction, self).__init__(snapType, parent)

        # Make sure we catch changes in the main snapping dialog
        QgsProject.instance().snapSettingsChanged.connect(self._refresh)
        # If a new project is read, update to that project's setting
        QgsProject.instance().readProject.connect(self._refresh)
        # If we change the settings, make such others are told
        self.snappingTypeChanged.connect(QgsProject.instance().snapSettingsChanged)

    def unload(self):
        QgsProject.instance().snapSettingsChanged.disconnect(self._refresh)
        QgsProject.instance().readProject.disconnect(self._refresh)
        self.snappingTypeChanged.disconnect(QgsProject.instance().snapSettingsChanged)

    # Private API

    def _triggered(self, checked):
        if checked:
            Snapping.setProjectSnappingType(self._snapType)
            self.snappingTypeChanged.emit(self._snapType)

    def _refresh(self):
        self.blockSignals(True)
        self.setChecked(Snapping.projectSnappingType() == self._snapType)
        self.setEnabled(Snapping.snappingMode() != Snapping.SelectedLayers)
        self.blockSignals(False)
