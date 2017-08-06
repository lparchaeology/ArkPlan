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
from PyQt4.QtGui import QComboBox

from qgis.core import QgsProject

import .Snapping


class SnappingModeCombo(QComboBox):

    snappingModeChanged = pyqtSignal(int)

    _snapMode = ''
    _snapType = ''

    def __init__(self, parent=None):

        super(SnappingModeCombo, self).__init__(parent)

        self.addItem('Off', Snapping.Off)
        self.addItem('Current Layer', Snapping.CurrentLayer)
        self.addItem('All Layers', Snapping.AllLayers)
        self.addItem('Selected Layers', Snapping.SelectedLayers)
        self.setCurrentIndex(0)

        self._refresh()
        self.currentIndexChanged.connect(self._changed)

        # Make sure we catch changes in the main snapping dialog
        QgsProject.instance().snapSettingsChanged.connect(self._refresh)
        # If a new project is read, update to that project's setting
        QgsProject.instance().readProject.connect(self._refresh)
        self.snappingModeChanged.connect(QgsProject.instance().snapSettingsChanged)

    def currentMode(self):
        return self.itemData(self.currentIndex())

    # Private API

    def _changed(self, idx):
        mode = self.currentMode()
        if mode == Snapping.Off:
            Snapping.setProjectSnappingType(Snapping.Off)
            Snapping.setSnappingMode(Snapping.CurrentLayer)
        else:
            if self._snapMode == Snapping.Off and mode != Snapping.Off:
                Snapping.setProjectSnappingType(self._snapType)
            Snapping.setSnappingMode(mode)
        self._snapMode = mode
        self.snappingModeChanged.emit(mode)

    def _refresh(self):
        mode = Snapping.snappingMode()
        if self._snapMode == Snapping.Off and mode == Snapping.CurrentLayer:
            return
        self._snapType = Snapping.projectSnappingType()
        self._snapMode = mode
        idx = self.findData(self._snapMode)
        self.setCurrentIndex(idx)
