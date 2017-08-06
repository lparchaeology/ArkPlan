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
from PyQt4.QtGui import QActionGroup

from qgis.core import QgsProject

import .ProjectSnappingEnabledAction
import .Snapping


class ProjectSnappingAction(ProjectSnappingEnabledAction):

    """Action to configure snapping."""

    snapSettingsChanged = pyqtSignal()

    def __init__(self, parent=None):
        super(ProjectSnappingAction, self).__init__(parent)
        self.setCheckable(True)

        self._currentAction = SnappingModeAction(Snapping.CurrentLayer, self)
        self._allAction = SnappingModeAction(Snapping.AllLayers, self)
        self._selectedAction = SnappingModeAction(Snapping.SelectedLayers, self)

        self._snappingModeActionGroup = QActionGroup(self)
        self._snappingModeActionGroup.addAction(self._currentAction)
        self._snappingModeActionGroup.addAction(self._allAction)
        self._snappingModeActionGroup.addAction(self._selectedAction)

        self._vertexAction = ProjectSnappingTypeAction(Snapping.Vertex, self)
        self._segmentAction = ProjectSnappingTypeAction(Snapping.Segment, self)
        self._vertexSegmentAction = ProjectSnappingTypeAction(Snapping.VertexAndSegment, self)

        self._snappingTypeActionGroup = QActionGroup(self)
        self._snappingTypeActionGroup.addAction(self._vertexAction)
        self._snappingTypeActionGroup.addAction(self._segmentAction)
        self._snappingTypeActionGroup.addAction(self._vertexSegmentAction)

        self._pixelUnitsAction = ProjectSnappingUnitAction(Snapping.Pixels, self)
        self._layerUnitsAction = ProjectSnappingUnitAction(Snapping.LayerUnits, self)
        self._projectUnitsAction = ProjectSnappingUnitAction(Snapping.ProjectUnits, self)

        self._unitTypeActionGroup = QActionGroup(self)
        self._unitTypeActionGroup.addAction(self._pixelUnitsAction)
        self._unitTypeActionGroup.addAction(self._layerUnitsAction)
        self._unitTypeActionGroup.addAction(self._projectUnitsAction)

        self._toleranceAction = ProjectSnappingToleranceAction(parent)

        menu = ControlMenu(parent)
        menu.addActions(self._snappingModeActionGroup.actions())
        menu.addSeparator()
        menu.addActions(self._snappingTypeActionGroup.actions())
        menu.addSeparator()
        menu.addAction(self._toleranceAction)
        menu.addActions(self._unitTypeActionGroup.actions())
        self.setMenu(menu)

        self._refreshAction()

        # Make sure we catch changes in the main snapping dialog
        QgsProject.instance().snapSettingsChanged.connect(self._refreshAction)

    def setInterface(self, iface):
        self._toleranceAction.setInterface(iface)

    def unload(self):
        super(ProjectSnappingAction, self).unload()
        self._currentAction.unload()
        self._allAction.unload()
        self._selectedAction.unload()
        self._vertexAction.unload()
        self._segmentAction.unload()
        self._vertexSegmentAction.unload()
        self._pixelUnitsAction.unload()
        self._layerUnitsAction.unload()
        self._projectUnitsAction.unload()
        self._toleranceAction.unload()
        QgsProject.instance().snapSettingsChanged.disconnect(self._refreshAction)

    # Private API

    def _refreshAction(self):
        snapMode = Snapping.snappingMode()
        if snapMode == Snapping.SelectedLayers:
            self.setIcon(self._selectedAction.icon())
        elif snapMode == Snapping.CurrentLayer:
            self.setIcon(self._currentAction.icon())
        elif snapMode == Snapping.AllLayers:
            self.setIcon(self._allAction.icon())
