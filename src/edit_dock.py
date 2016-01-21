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
from PyQt4.QtGui import QWidget, QAction

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

        self.widget.setEnabled(False)

    def unloadGui(self):
        super(EditDock, self).unloadGui()

    # Load the project settings when project is loaded
    def loadProject(self, project):
        self._setLayer(project.plan.pointsBuffer, self.widget.snapBufferPointsTool)
        self._setLayer(project.plan.linesBuffer, self.widget.snapBufferLinesTool)
        self._setLayer(project.plan.polygonsBuffer, self.widget.snapBufferPolygonsTool)
        self._setLayer(project.plan.pointsLayer, self.widget.snapPlanPointsTool)
        self._setLayer(project.plan.linesLayer, self.widget.snapPlanLinesTool)
        self._setLayer(project.plan.polygonsLayer, self.widget.snapPlanPolygonsTool)
        self._setLayer(project.base.pointsLayer, self.widget.snapBasePointsTool)
        self._setLayer(project.base.linesLayer, self.widget.snapBaseLinesTool)
        self._setLayer(project.base.polygonsLayer, self.widget.snapBasePolygonsTool)
        Snapping.setSnappingMode(Snapping.SelectedLayers)
        Snapping.setIntersectionSnapping(True)
        Snapping.setTopologicalEditing(True)
        Snapping.setLayerSnappingEnabled(project.plan.linesBuffer.id(), True)
        Snapping.setLayerSnappingEnabled(project.plan.polygonsBuffer.id(), True)
        Snapping.setLayerSnappingEnabled(project.grid.pointsLayer.id(), False)
        Snapping.setLayerSnappingEnabled(project.grid.linesLayer.id(), False)
        Snapping.setLayerSnappingEnabled(project.grid.polygonsLayer.id(), False)
        QgsProject.instance().snapSettingsChanged.connect(self._refresh)
        QgsProject.instance().snapSettingsChanged.emit()

    # Close the project
    def closeProject(self):
        QgsProject.instance().snapSettingsChanged.disconnect(self._refresh)

    def _setLayer(self, layer, tool):
        Snapping.setLayerSnappingEnabled(layer.id(), False)
        action = LayerSnappingAction(layer, tool)
        action.setInterface(self._iface)
        tool.setDefaultAction(action)

    def _refresh(self):
        self.widget.setEnabled(Snapping.snappingMode() == Snapping.SelectedLayers)
