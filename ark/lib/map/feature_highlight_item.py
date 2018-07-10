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

from qgis.PyQt.QtCore import Qt
from qgis.PyQt.QtGui import QBrush, QPen

from qgis.core import (QgsFeature, QgsRectangle, QgsRenderContext, QgsSimpleMarkerSymbolLayer, QgsSymbol,
                       QgsSymbolLayerUtils)
from qgis.gui import QgsMapCanvasItem

from ..application import Application


class FeatureHighlightItem(QgsMapCanvasItem):
    # Code ported from QGIS QgsHighlight

    def __init__(self, mapCanvas, feature, layer):
        super().__init__(mapCanvas)

        self._mapCanvas = None  # QgsMapCanvas
        self._brush = QBrush()
        self._pen = QPen()
        self._feature = None  # QgsFeature()
        self._layer = None  # QgsMapLayer()
        self._buffer = 0.0
        self._minWidth = 0.0

        self._mapCanvas = mapCanvas
        if (not layer
                or not feature
                or not isinstance(feature, QgsFeature)
                or not feature.hasGeometry()
                or feature.geometry().isEmpty()
                or not feature.geometry().isGeosValid()):
            return
        self._feature = QgsFeature(feature)  # Force deep copy
        self._layer = layer
        self.setLineColor(Application.highlightLineColor())
        self.setFillColor(Application.highlightFillColor())
        self._minWidth = Application.highlightMinimumWidth()
        self._buffer = Application.highlightBuffer()
        if self._mapCanvas.mapSettings().hasCrsTransformEnabled():
            ct = self._mapCanvas.mapSettings().layerTransform(self._layer)
            if ct:
                self._feature.geometry().transform(ct)
        self.updateRect()
        self.update()

    def remove(self):
        self._mapCanvas.scene().removeItem(self)

    def setLineWidth(self, width):
        self._pen.setWidth(width)

    def setLineColor(self, color):
        self._pen.setColor(color)

    def setFillColor(self, fillColor):
        self._brush.setColor(fillColor)
        self._brush.setStyle(Qt.SolidPattern)

    def setBuffer(self, buff):
        self._buffer = buff

    def setMinWidth(self, width):
        self._minWidth = width

    def layer(self):
        return self._layer

    def updatePosition(self):
        pass

    # protected:
    def paint(self, painter, option=None, widget=None):  # Override
        if not self._feature:
            return

        mapSettings = self._mapCanvas.mapSettings()
        context = QgsRenderContext.fromMapSettings(mapSettings)
        renderer = self._getRenderer(context, self._pen.color(), self._brush.color())

        if renderer:
            context.setPainter(painter)
            renderer.startRender(context, self._layer.fields())
            renderer.renderFeature(self._feature, context)
            renderer.stopRender(context)

    def updateRect(self):
        if self._feature and self._feature.hasGeometry():
            m2p = self._mapCanvas.mapSettings().mapToPixel()
            topLeft = m2p.toMapPoint(0, 0)
            res = m2p.mapUnitsPerPixel()
            imageSize = self._mapCanvas.mapSettings().outputSize()
            rect = QgsRectangle(topLeft.x(), topLeft.y(), topLeft.x() + imageSize.width()
                                * res, topLeft.y() - imageSize.height() * res)
            self.setRect(rect)
            self.setVisible(True)
        else:
            self.setRect(QgsRectangle())

    # private:
    def _setSymbol(self, symbol, context, color, fillColor):
        if not symbol:
            return

        for symbolLayer in reversed(symbol.symbolLayers()):
            if symbolLayer:
                if symbolLayer.subSymbol():
                    self._setSymbol(symbolLayer.subSymbol(), context, color, fillColor)
                else:
                    symbolLayer.setColor(color)
                    symbolLayer.setOutlineColor(color)
                    symbolLayer.setFillColor(fillColor)
                    if isinstance(symbolLayer, QgsSimpleMarkerSymbolLayer):
                        symbolLayer.setOutlineWidth(
                            self._getSymbolWidth(context, symbolLayer.strokeWidth(), symbolLayer.strokeWidthUnit()))
                    if symbolLayer.type() == QgsSymbol.Line:
                        symbolLayer.setWidth(
                            self._getSymbolWidth(context, symbolLayer.width(), symbolLayer.widthUnit()))
                    if symbolLayer.type() == QgsSymbol.Fill:
                        symbolLayer.setBorderWidth(
                            self._getSymbolWidth(context, symbolLayer.strokeWidth(), symbolLayer.outputUnit()))
                    symbolLayer.removeDataDefinedProperty('color')
                    symbolLayer.removeDataDefinedProperty('color_border')

    def _getSymbolWidth(self, context, width, unit):
        scale = 1.0
        if unit == QgsSymbol.MapUnit:
            scale = QgsSymbolLayerUtils.lineWidthScaleFactor(
                context, QgsSymbol.MM) / QgsSymbolLayerUtils.lineWidthScaleFactor(context, QgsSymbol.MapUnit)
        width = max(width + 2 * self._buffer * scale, self._minWidth * scale)
        return width

    def _getRenderer(self, context, color, fillColor):
        renderer = None
        if self._layer and self._layer.rendererV2():
            renderer = self._layer.rendererV2().clone()
        if renderer:
            for symbol in renderer.symbols2(context):
                self._setSymbol(symbol, context, color, fillColor)
        return renderer
