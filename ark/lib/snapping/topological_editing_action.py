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
from qgis.core import QgsProject

import .Snapping
import .resources


class TopologicalEditingAction(QAction):

    """Action to toggle Topological Editing for a project."""

    topologicalEditingChanged = pyqtSignal(bool)

    def __init__(self, parent=None):
        super(TopologicalEditingAction, self).__init__(parent)

        self.setCheckable(True)
        self._icon = QIcon(':/plugins/ark/topologicalEditing.png')
        self.setIcon(self._icon)
        self.setText('Topological Editing')

        self._refresh()
        self.triggered.connect(self._triggered)

        # Make sure we catch changes in the main snapping dialog
        QgsProject.instance().snapSettingsChanged.connect(self._refresh)
        # If a new project is read, update to that project's setting
        QgsProject.instance().readProject.connect(self._refresh)
        # If we change the settings, make such others are told
        self.topologicalEditingChanged.connect(QgsProject.instance().snapSettingsChanged)

    def unload(self):
        QgsProject.instance().snapSettingsChanged.disconnect(self._refresh)
        QgsProject.instance().readProject.disconnect(self._refresh)
        self.topologicalEditingChanged.disconnect(QgsProject.instance().snapSettingsChanged)

    # Private API

    def _triggered(self, status):
        Snapping.setTopologicalEditing(status)
        self.topologicalEditingChanged.emit(status)

    def _refresh(self):
        self.blockSignals(True)
        self.setChecked(Snapping.topologicalEditing())
        self.blockSignals(False)
