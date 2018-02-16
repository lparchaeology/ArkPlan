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

from PyQt4.QtCore import QPoint, QSettings, Qt
from PyQt4.QtGui import QAction, QColor, QMenu

from qgis.core import QGis, QgsPointV2
from qgis.gui import QgsHighlight, QgsMapToolIdentify, QgsVertexMarker

from ArkSpatial.ark.lib.gui import ClipboardAction

from ArkSpatial.ark.core import Item
from ArkSpatial.ark.gui import IdentifyItemAction


class MapToolIndentifyItems(QgsMapToolIdentify):

    _menu = None  # QMenu()
    _actions = []
    _highlights = []
    _plugin = None
    _vertexMarker = None  # QgsVertexMarker

    def __init__(self, plugin):
        super(MapToolIndentifyItems, self).__init__(plugin.mapCanvas())
        mToolName = self.tr('Identify feature')
        self._vertexMarker = QgsVertexMarker(plugin.mapCanvas())
        self._vertexMarker.setIconType(QgsVertexMarker.ICON_CROSS)
        self._plugin = plugin
        self._menu = QMenu(plugin.mapCanvas())
        self._menu.hovered.connect(self._highlight)

    def deactivate(self):
        self._reset()
        super(MapToolIndentifyItems, self).deactivate()

    def canvasPressEvent(self, e):
        self._reset()

    def canvasReleaseEvent(self, e):
        self._reset()
        if e.button() != Qt.LeftButton:
            return
        mapPoint = self.toMapCoordinates(e.pos())
        self._vertexMarker.setCenter(mapPoint)
        layers = [self._plugin.plan.pointsLayer, self._plugin.plan.linesLayer, self._plugin.plan.polygonsLayer]
        results = self.identify(e.x(), e.y(), layers, QgsMapToolIdentify.TopDownAll)
        if (len(results) < 1):
            return
        # Build the set of unique items identified
        items = set()
        for result in results:
            feature = result.mFeature
            siteCode = feature.attribute('site')
            classCode = feature.attribute('class')
            itemId = feature.attribute('id')
            items.add(Item(siteCode, classCode, itemId))
        action = QAction('Plan Items', self._menu)
        action.setData('top')
        self._menu.addAction(action)
        site = ''
        for item in sorted(items):
            if item.siteCode() != site:
                site = item.siteCode()
                self._menu.addSeparator()
                action = QAction('Site ' + site + ':', self._menu)
                action.setData('top')
                self._menu.addAction(action)
            action = IdentifyItemAction(item, self._plugin, self._menu)
            action.setData('top')
            action.zoomToItemSelected.connect(self._zoom)
            action.panToItemSelected.connect(self._pan)
            action.filterItemSelected.connect(self._filterItem)
            action.excludeFilterItemSelected.connect(self._excludeFilterItem)
            action.highlightItemSelected.connect(self._highlightItem)
            action.addHighlightItemSelected.connect(self._addHighlightItem)
            action.editItemSelected.connect(self._editInBuffers)
            action.deleteItemSelected.connect(self._delete)
            action.openDrawingsSelected.connect(self._openDrawings)
            self._actions.append(action)
            self._menu.addAction(action)
        self._menu.addSeparator()
        action = ClipboardAction('Map: ', mapPoint.toString(3), self._menu)
        action.setData('top')
        self._menu.addAction(action)
        if self._plugin.gridModule.mapTransformer is not None:
            localPoint = self._plugin.gridModule.mapTransformer.map(mapPoint)
            self._menu.addAction(ClipboardAction('Local: ', localPoint.toString(3), self._menu))
        menuPos = QPoint(e.globalX() + 100, e.globalY() - 50)
        selected = self._menu.exec_(menuPos)
        self._reset(resetVertex=False)

    def keyPressEvent(self, e):
        if (e.key() == Qt.Key_Escape):
            self._reset()
            self.canvas().unsetMapTool(self)

    def _reset(self, resetVertex=True):
        self._menu.clear()
        del self._highlights[:]
        del self._actions[:]
        if resetVertex and self._vertexMarker:
            self._vertexMarker.setCenter(QgsPointV2())

    def _highlight(self, item):
        if item.data() == 'top':
            del self._highlights[:]
        else:
            return
        if not isinstance(item, IdentifyItemAction):
            return
        request = item.item.featureRequest()
        for feature in self._plugin.plan.polygonsLayer.getFeatures(request):
            self._addHighlight(self._plugin.mapCanvas(), feature.geometry(), self._plugin.plan.polygonsLayer)
        for feature in self._plugin.plan.linesLayer.getFeatures(request):
            self._addHighlight(self._plugin.mapCanvas(), feature.geometry(), self._plugin.plan.linesLayer)
        for feature in self._plugin.plan.pointsLayer.getFeatures(request):
            self._addHighlight(self._plugin.mapCanvas(), feature.geometry(), self._plugin.plan.pointsLayer)

    def _addHighlight(self, canvas, geometry, layer):
        hl = QgsHighlight(canvas, geometry, layer)
        color = QColor(QSettings().value('/Map/highlight/color', QGis.DEFAULT_HIGHLIGHT_COLOR.name(), str))
        alpha = QSettings().value('/Map/highlight/colorAlpha', QGis.DEFAULT_HIGHLIGHT_COLOR.alpha(), int)
        buff = QSettings().value('/Map/highlight/buffer', QGis.DEFAULT_HIGHLIGHT_BUFFER_MM, float)
        minWidth = QSettings().value('/Map/highlight/minWidth', QGis.DEFAULT_HIGHLIGHT_MIN_WIDTH_MM, float)
        hl.setColor(color)
        color.setAlpha(alpha)
        hl.setFillColor(color)
        hl.setBuffer(buff)
        hl.setMinWidth(minWidth)
        self._highlights.append(hl)

    def _zoom(self, item):
        self._plugin.planModule.zoomToItem(item, highlight=True)

    def _pan(self, item):
        self._plugin.planModule.moveToItem(item, highlight=True)

    def _filterItem(self, item):
        self._plugin.planModule.filterItem(item)

    def _excludeFilterItem(self, item):
        self._plugin.planModule.excludeFilterItem(item)

    def _highlightItem(self, item):
        self._plugin.planModule.highlightItem(item)

    def _addHighlightItem(self, item):
        self._plugin.planModule.addHighlightItem(item)

    def _openDrawings(self, item):
        self._plugin.planModule.loadDrawing(item)

    def _editInBuffers(self, item):
        self._plugin.planModule.editInBuffers(item)

    def _delete(self, item):
        self._plugin.planModule.deleteItem(item)
