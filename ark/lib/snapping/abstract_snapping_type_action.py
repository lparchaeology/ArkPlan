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

from PyQt4.QtGui import QAction, QIcon

from .snapping_ import Snapping


class AbstractSnappingTypeAction(QAction):

    """Abstract action for Snapping Type."""

    def __init__(self, snapType, parent=None):
        super(AbstractSnappingTypeAction, self).__init__(parent)

        self._snapType = snapType
        if snapType == Snapping.CurrentLayer:
            self.setText('Vertex')
            self.setStatusTip('Snap to vertex')
            self._icon = QIcon(':/plugins/ark/snapVertex.png')
        elif snapType == Snapping.AllLayers:
            self.setText('Segment')
            self.setStatusTip('Snap to segment')
            self._icon = QIcon(':/plugins/ark/snapSegment.png')
        elif snapType == Snapping.SelectedLayers:
            self.setText('Vertex and Segment')
            self.setStatusTip('Snap to vertex and segment')
            self._icon = QIcon(':/plugins/ark/snapVertexSegment.png')
        self.setIcon(self._icon)
        self.setCheckable(True)

        self._refresh()
        self.triggered.connect(self._triggered)

    # Private API

    def _triggered(self, checked):
        pass

    def _refresh(self):
        pass
