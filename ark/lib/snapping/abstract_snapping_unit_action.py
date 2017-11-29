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

from PyQt4.QtGui import QAction

from .snapping_ import Snapping


class AbstractSnappingUnitAction(QAction):

    """Abstract action for Snapping Unit."""

    def __init__(self, snapUnit, parent=None):
        super(AbstractSnappingUnitAction, self).__init__(parent)

        self._snapUnit = snapUnit
        if snapUnit == Snapping.Pixels:
            self.setText('Pixels')
            self.setStatusTip('Use pixels')
        elif snapUnit == Snapping.LayerUnits:
            self.setText('Layer Units')
            self.setStatusTip('Use layer units')
        elif snapUnit == Snapping.ProjectUnits:
            self.setText('Project Units')
            self.setStatusTip('Use project units')

        self.setCheckable(True)

        self._refresh()
        self.triggered.connect(self._triggered)

    # Private API

    def _triggered(self, checked):
        pass

    def _refresh(self):
        pass
