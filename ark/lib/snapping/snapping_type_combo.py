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

from PyQt4.QtCore import pyqtSignal
from PyQt4.QtGui import QComboBox

from qgis.core import QgsProject

from .snapping_ import Snapping


class SnappingTypeCombo(QComboBox):

    snappingTypeChanged = pyqtSignal(int)

    def __init__(self, parent=None):

        super(SnappingTypeCombo, self).__init__(parent)

        self.addItem('Off', Snapping.Off)
        self.addItem('Vertex', Snapping.Vertex)
        self.addItem('Segment', Snapping.Segment)
        self.addItem('Vertex and Segment', Snapping.VertexAndSegment)
        self.setCurrentIndex(0)

        self._refresh()
        self.currentIndexChanged.connect(self._changed)

        # Make sure we catch changes in the main snapping dialog
        QgsProject.instance().snapSettingsChanged.connect(self._refresh)
        # If a new project is read, update to that project's setting
        QgsProject.instance().readProject.connect(self._refresh)
        self.snappingTypeChanged.connect(QgsProject.instance().snapSettingsChanged)

    # Private API

    def _changed(self, idx):
        snapType = self.itemData(self.currentIndex())
        Snapping.setProjectSnappingType(snapType)
        self.snappingTypeChanged.emit(snapType)

    def _refresh(self):
        snapType = Snapping.projectSnappingType()
        idx = self.findData(snapType)
        self.setCurrentIndex(idx)
