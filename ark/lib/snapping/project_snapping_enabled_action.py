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


class ProjectSnappingEnabledAction(QAction):

    """Action to enable snapping."""

    snappingEnabledChanged = pyqtSignal()

    _selectedLayers = []
    _prevType = Snapping.Off

    def __init__(self, parent=None):
        super(ProjectSnappingEnabledAction, self).__init__(parent)

        self.setText('Toggle Snapping')
        self.setStatusTip('Enbale/disable snapping')
        self.setIcon(QIcon(':/plugins/ark/snapEnable.png'))
        self.setCheckable(True)
        self._refresh()
        self.triggered.connect(self._triggered)

        # Make sure we catch changes in the main snapping dialog
        QgsProject.instance().snapSettingsChanged.connect(self._refresh)
        # If a new project is read, update to that project's setting
        QgsProject.instance().readProject.connect(self._refresh)
        self.snappingEnabledChanged.connect(QgsProject.instance().snapSettingsChanged)

    def setInterface(self, iface):
        self._toleranceAction.setInterface(iface)

    def unload(self):
        QgsProject.instance().snapSettingsChanged.disconnect(self._refresh)
        QgsProject.instance().readProject.disconnect(self._refresh)
        self.snappingEnabledChanged.disconnect(QgsProject.instance().snapSettingsChanged)

    # Private API

    def _triggered(self, checked):
        if checked:
            if Snapping.snappingMode() == Snapping.SelectedLayers:
                Snapping.setLayerSnappingEnabledLayers(self._selectedLayers)
            else:
                Snapping.setProjectSnappingType(self._prevType)
        else:
            if Snapping.snappingMode() == Snapping.SelectedLayers:
                self._selectedLayers = Snapping.layerSnappingEnabledLayers()
                Snapping.setLayerSnappingEnabledLayers([])
            else:
                self._prevType = Snapping.projectSnappingType()
                Snapping.setProjectSnappingType(Snapping.Off)
        self.snappingEnabledChanged.emit()

    def _refresh(self):
        self.blockSignals(True)
        snapMode = Snapping.snappingMode()
        snapType = Snapping.projectSnappingType()
        if snapType != Snapping.Off:
            self._prevType = snapType
        selectedLayers = Snapping.layerSnappingEnabledLayers()
        if len(selectedLayers) > 0:
            self._selectedLayers = selectedLayers
        if snapMode == Snapping.SelectedLayers:
            self.setChecked(len(selectedLayers) > 0)
        else:
            self.setChecked(snapType != Snapping.Off)
        self.blockSignals(False)
