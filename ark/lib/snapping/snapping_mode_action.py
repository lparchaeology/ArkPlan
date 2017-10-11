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

from .snapping_ import Snapping


class SnappingModeAction(QAction):

    """Action to change Snapping Mode for a project."""

    snappingModeChanged = pyqtSignal(int)

    def __init__(self, snapMode, parent=None):
        super(SnappingModeAction, self).__init__(parent)

        self._snapMode = snapMode
        if snapMode == Snapping.CurrentLayer:
            self.setText('Current Layer')
            self.setStatusTip('Snap to current layer')
            self._icon = QIcon(':/plugins/ark/snapLayerCurrent.png')
        elif snapMode == Snapping.AllLayers:
            self.setText('All Layers')
            self.setStatusTip('Snap to all layers')
            self._icon = QIcon(':/plugins/ark/snapLayerAll.png')
        elif snapMode == Snapping.SelectedLayers:
            self.setText('Selected Layers')
            self.setStatusTip('Snap to selected layers')
            self._icon = QIcon(':/plugins/ark/snapLayerSelected.png')

        self.setIcon(self._icon)
        self.setCheckable(True)

        self._refresh()
        self.triggered.connect(self._triggered)

        # Make sure we catch changes in the main snapping dialog
        QgsProject.instance().snapSettingsChanged.connect(self._refresh)
        # If a new project is read, update to that project's setting
        QgsProject.instance().readProject.connect(self._refresh)
        # If we change the settings, make such others are told
        self.snappingModeChanged.connect(QgsProject.instance().snapSettingsChanged)

    def unload(self):
        self.triggered.disconnect(self._triggered)
        QgsProject.instance().snapSettingsChanged.disconnect(self._refresh)
        QgsProject.instance().readProject.disconnect(self._refresh)
        self.snappingModeChanged.disconnect(QgsProject.instance().snapSettingsChanged)

    # Private API

    def _triggered(self, checked):
        if checked:
            Snapping.setSnappingMode(self._snapMode)
            self.snappingModeChanged.emit(self._snapMode)

    def _refresh(self):
        self.blockSignals(True)
        self.setChecked(self._snapMode == Snapping.snappingMode())
        self.blockSignals(False)
