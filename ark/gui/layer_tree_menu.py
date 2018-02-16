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

from PyQt4.QtGui import QAction, QMenu

from qgis.core import QgsLayerTreeNode, QgsMapLayer, QgsProject
from qgis.gui import QgsLayerTreeViewMenuProvider

from ArkSpatial.ark.lib import Application


class LayerTreeMenu(QgsLayerTreeViewMenuProvider):

    _iface = None
    _view = None
    _plugin = None

    def __init__(self, plugin, view):
        QgsLayerTreeViewMenuProvider.__init__(self)
        self._plugin = plugin
        self._view = view

        # Default actions
        self._zoomGroup = self._view.defaultActions().actionZoomToGroup(self._plugin.mapCanvas())
        self._zoomLayer = self._view.defaultActions().actionZoomToLayer(self._plugin.mapCanvas())
        self._featureCount = self._view.defaultActions().actionShowFeatureCount(self._plugin.mapCanvas())
        self._remove = self._view.defaultActions().actionRemoveGroupOrLayer(self._plugin.mapCanvas())
        self._rename = self._view.defaultActions().actionRenameGroupOrLayer(self._plugin.mapCanvas())

        # Custom actions
        self._removeDrawings = QAction('Remove All Drawings', view)
        self._removeDrawings.triggered.connect(self._plugin.clearDrawings)

        self._openAttributes = QAction(
            Application.getThemeIcon('mActionOpenTable.svg'), plugin.tr('&Open Attribute Table'), view)
        self._openAttributes.triggered.connect(self._showAttributeTable)

        self._openProperties = QAction(plugin.tr('&Properties'), view)
        self._openProperties.triggered.connect(self._showLayerProperties)

    def createContextMenu(self):
        if not self._view.currentNode():
            return None
        menu = QMenu()
        node = self._view.currentNode()
        if node.nodeType() == QgsLayerTreeNode.NodeGroup:
            menu.addAction(self._zoomGroup)
            if not self._plugin.isArkGroup(node.name()):
                menu.addAction(self._rename)
                menu.addAction(self._remove)
            if node.name() == self._plugin.drawingsGroupName:
                menu.addAction(self._removeDrawings)
        elif node.nodeType() == QgsLayerTreeNode.NodeLayer:
            menu.addAction(self._zoomLayer)
            if node.layer().type() == QgsMapLayer.VectorLayer:
                menu.addAction(self._featureCount)
                menu.addAction(self._openAttributes)
            layerId = node.layerId()
            parent = node.parent()
            if parent.nodeType() == QgsLayerTreeNode.NodeGroup and parent.name() == self._plugin.drawingsGroupName:
                menu.addAction(self._removeDrawings)
            if not self._plugin.isArkLayer(layerId):
                menu.addSeparator()
                menu.addAction(self._rename)
                menu.addAction(self._remove)
                if not QgsProject.instance().layerIsEmbedded(layerId):
                    menu.addAction(self._openProperties)
        return menu

    def _showAttributeTable(self):
        node = self._view.currentNode()
        if node.nodeType() == QgsLayerTreeNode.NodeLayer and node.layer().type() == QgsMapLayer.VectorLayer:
            self._plugin.iface.showAttributeTable(node.layer())

    def _showLayerProperties(self):
        node = self._view.currentNode()
        if node.nodeType() == QgsLayerTreeNode.NodeLayer:
            self._plugin.iface.showLayerProperties(node.layer())
