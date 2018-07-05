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

from qgis.PyQt.QtWidgets import QGroupBox

from qgis.core import QgsProject

from ArkSpatial.ark.lib import utils
from ArkSpatial.ark.lib.snapping import LayerSnappingAction, Snapping

from .ui.snapping_widget_base import Ui_SnappingWidget


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
        del self.snapSitePointsTool
        # self.snapSiteLinesTool.defaultAction().unload()
        del self.snapSiteLinesTool
        # self.snapSitePolygonsTool.defaultAction().unload()
        del self.snapSitePolygonsTool

    # Load the project settings when project is loaded
    def loadProject(self, plugin):
        plan = plugin.project().collection('plan')
        site = plugin.project().collection('site')
        grid = plugin.project().collection('grid')
        self._setLayer(plugin.iface, plan.buffer('points'), self.snapBufferPointsTool)
        self._setLayer(plugin.iface, plan.buffer('lines'), self.snapBufferLinesTool)
        self._setLayer(plugin.iface, plan.buffer('polygons'), self.snapBufferPolygonsTool)
        self._setLayer(plugin.iface, plan.layer('points'), self.snapPlanPointsTool)
        self._setLayer(plugin.iface, plan.layer('lines'), self.snapPlanLinesTool)
        self._setLayer(plugin.iface, plan.layer('polygons'), self.snapPlanPolygonsTool)
        self._setLayer(plugin.iface, site.layer('points'), self.snapSitePointsTool)
        self._setLayer(plugin.iface, site.layer('lines'), self.snapSiteLinesTool)
        self._setLayer(plugin.iface, site.layer('polygons'), self.snapSitePolygonsTool)
        Snapping.setSnappingMode(Snapping.SelectedLayers)
        Snapping.setIntersectionSnapping(True)
        Snapping.setTopologicalEditing(True)
        Snapping.setLayerSnappingEnabled(plan.buffer('lines').id(), True)
        Snapping.setLayerSnappingEnabled(plan.buffer('polygons').id(), True)
        Snapping.setLayerSnappingEnabled(grid.layer('points').id(), False)
        Snapping.setLayerSnappingEnabled(grid.layer('lines').id(), False)
        Snapping.setLayerSnappingEnabled(grid.layer('polygons').id(), False)
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
        self.snapSiteLinesTool.defaultAction().unload()
        self.snapSitePolygonsTool.defaultAction().unload()
        QgsProject.instance().snapSettingsChanged.disconnect(self._refresh)

    def _setLayer(self, iface, layer, tool):
        if layer and layer.isValid():
            Snapping.setLayerSnappingEnabled(layer.id(), False)
            action = LayerSnappingAction(layer, tool)
            action.setInterface(iface)
            tool.setDefaultAction(action)

    def _refresh(self):
        self.setEnabled(Snapping.snappingMode() == Snapping.SelectedLayers)
