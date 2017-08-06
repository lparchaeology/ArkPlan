# -*- coding: utf-8 -*-
"""
/***************************************************************************
                                ARK Spatial
                    A QGIS plugin for Archaeological Recording.
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

from PyQt4 import uic
from PyQt4.QtGui import QGroupBox

from qgis.core import QgsProject

from ark.lib import Snapping

from snapping_widget_base import Ui_SnappingWidget


class SnappingWidget(QGroupBox, Ui_SnappingWidget):

    def __init__(self, parent=None):
        super(SnappingWidget, self).__init__(parent)
        self.setupUi(self)
        self.setEnabled(False)

    def initGui(self):
        pass

    def unloadGui(self):
        # self.snapBufferPointsTool.defaultAction().unload()
        del self.snapBufferPointsTool
        # self.snapBufferLinesTool.defaultAction().unload()
        del self.snapBufferLinesTool
        # self.snapBufferPolygonsTool.defaultAction().unload()
        del self.snapBufferPolygonsTool
        # self.snapPlanPointsTool.defaultAction().unload()
        del self.snapPlanPointsTool
        # self.snapPlanLinesTool.defaultAction().unload()
        del self.snapPlanPolygonsTool
        # self.snapPlanPolygonsTool.defaultAction().unload()
        del self.snapBasePointsTool
        # self.snapBaseLinesTool.defaultAction().unload()
        del self.snapBaseLinesTool
        # self.snapBasePolygonsTool.defaultAction().unload()
        del self.snapBasePolygonsTool

    # Load the project settings when project is loaded
    def loadProject(self, project):
        self._setLayer(project.iface, project.plan.pointsBuffer, self.snapBufferPointsTool)
        self._setLayer(project.iface, project.plan.linesBuffer, self.snapBufferLinesTool)
        self._setLayer(project.iface, project.plan.polygonsBuffer, self.snapBufferPolygonsTool)
        self._setLayer(project.iface, project.plan.pointsLayer, self.snapPlanPointsTool)
        self._setLayer(project.iface, project.plan.linesLayer, self.snapPlanLinesTool)
        self._setLayer(project.iface, project.plan.polygonsLayer, self.snapPlanPolygonsTool)
        self._setLayer(project.iface, project.base.pointsLayer, self.snapBasePointsTool)
        self._setLayer(project.iface, project.base.linesLayer, self.snapBaseLinesTool)
        self._setLayer(project.iface, project.base.polygonsLayer, self.snapBasePolygonsTool)
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
        self.snapBufferPointsTool.defaultAction().unload()
        self.snapBufferLinesTool.defaultAction().unload()
        self.snapBufferPolygonsTool.defaultAction().unload()
        self.snapPlanPointsTool.defaultAction().unload()
        self.snapPlanLinesTool.defaultAction().unload()
        self.snapPlanPolygonsTool.defaultAction().unload()
        self.snapBaseLinesTool.defaultAction().unload()
        self.snapBasePolygonsTool.defaultAction().unload()
        QgsProject.instance().snapSettingsChanged.disconnect(self._refresh)

    def _setLayer(self, iface, layer, tool):
        if layer and layer.isValid():
            Snapping.setLayerSnappingEnabled(layer.id(), False)
            action = LayerSnappingAction(layer, tool)
            action.setInterface(iface)
            tool.setDefaultAction(action)

    def _refresh(self):
        self.setEnabled(Snapping.snappingMode() == Snapping.SelectedLayers)
