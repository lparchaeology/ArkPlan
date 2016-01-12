# -*- coding: utf-8 -*-
"""
/***************************************************************************
                                ARK Spatial
                    A QGIS plugin for Archaeological Recording.
        Part of the Archaeological Recording Kit by L-P : Archaeology
                        http://ark.lparchaeology.com
                              -------------------
        begin                : 2014-12-07
        git sha              : $Format:%H$
        copyright            : 2014, 2015 by L-P : Heritage LLP
        email                : ark@lparchaeology.com
        copyright            : 2014, 2015 by John Layt
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

from PyQt4 import uic
from PyQt4.QtCore import Qt, pyqtSignal
from PyQt4.QtGui import QWidget

from qgis.core import QgsProject

from ..libarkqgis.dock import ToolDockWidget
from ..libarkqgis.snapping import *

import edit_widget_base

class EditWidget(QWidget, edit_widget_base.Ui_EditWidget):

    def __init__(self, parent=None):
        super(EditWidget, self).__init__(parent)
        self.setupUi(self)

class EditDock(ToolDockWidget):

    _iface = None # QgsisInterface()
    _snappingAction = None  # ProjectSnappingAction()
    _interAction = None  # IntersectionSnappingAction()
    _topoAction = None  # TopologicalEditingAction()

    def __init__(self, iface, parent=None):
        super(EditDock, self).__init__(EditWidget(), parent)
        self._iface = iface

        self.setWindowTitle(u'Editing Tools')
        self.setObjectName(u'EditDock')

    def initGui(self, iface, location, menuAction):
        super(EditDock, self).initGui(iface, location, menuAction)

        self.toolbar.addAction(iface.actionPan())
        self.toolbar.addAction(iface.actionZoomIn())
        self.toolbar.addAction(iface.actionZoomOut())
        self.toolbar.addAction(iface.actionZoomLast())
        self.toolbar.addAction(iface.actionZoomNext())
        self.toolbar.addSeparator()
        self._snappingAction = ProjectSnappingAction(self)
        self._snappingAction.setInterface(iface)
        self.toolbar.addAction(self._snappingAction)
        self._interAction = IntersectionSnappingAction(self)
        self.toolbar.addAction(self._interAction)
        self._topoAction = TopologicalEditingAction(self)
        self.toolbar.addAction(self._topoAction)

        self._refresh()
        QgsProject.instance().snapSettingsChanged.connect(self._refresh)

    def unloadGui(self):
        super(EditDock, self).unloadGui()

    # Snapping Tools

    def setBufferPoints(self, layer):
        action = LayerSnappingAction(layer, self.widget.snapBufferPointsTool)
        action.setInterface(self._iface)
        self.widget.snapBufferPointsTool.setDefaultAction(action)

    def setBufferLines(self, layer):
        action = LayerSnappingAction(layer, self.widget.snapBufferLinesTool)
        action.setInterface(self._iface)
        self.widget.snapBufferLinesTool.setDefaultAction(action)

    def setBufferPolygons(self, layer):
        action = LayerSnappingAction(layer, self.widget.snapBufferPolygonsTool)
        action.setInterface(self._iface)
        self.widget.snapBufferPolygonsTool.setDefaultAction(action)

    def setPlanPoints(self, layer):
        action = LayerSnappingAction(layer, self.widget.snapPlanPointsTool)
        action.setInterface(self._iface)
        self.widget.snapPlanPointsTool.setDefaultAction(action)

    def setPlanLines(self, layer):
        action = LayerSnappingAction(layer, self.widget.snapPlanLinesTool)
        action.setInterface(self._iface)
        self.widget.snapPlanLinesTool.setDefaultAction(action)

    def setPlanPolygons(self, layer):
        action = LayerSnappingAction(layer, self.widget.snapPlanPolygonsTool)
        action.setInterface(self._iface)
        self.widget.snapPlanPolygonsTool.setDefaultAction(action)

    def setBasePoints(self, layer):
        action = LayerSnappingAction(layer, self.widget.snapBasePointsTool)
        action.setInterface(self._iface)
        self.widget.snapBasePointsTool.setDefaultAction(action)

    def setBaseLines(self, layer):
        action = LayerSnappingAction(layer, self.widget.snapBaseLinesTool)
        action.setInterface(self._iface)
        self.widget.snapBaseLinesTool.setDefaultAction(action)

    def setBasePolygons(self, layer):
        action = LayerSnappingAction(layer, self.widget.snapBasePolygonsTool)
        action.setInterface(self._iface)
        self.widget.snapBasePolygonsTool.setDefaultAction(action)

    def _refresh(self):
        advanced = (Snapping.snappingMode() == Snapping.SelectedLayers)
        self.widget.snapBufferPointsTool.setEnabled(advanced)
        self.widget.snapBufferLinesTool.setEnabled(advanced)
        self.widget.snapBufferPolygonsTool.setEnabled(advanced)
        self.widget.snapPlanPointsTool.setEnabled(advanced)
        self.widget.snapPlanLinesTool.setEnabled(advanced)
        self.widget.snapPlanPolygonsTool.setEnabled(advanced)
        self.widget.snapBasePointsTool.setEnabled(advanced)
        self.widget.snapBaseLinesTool.setEnabled(advanced)
        self.widget.snapBasePolygonsTool.setEnabled(advanced)
