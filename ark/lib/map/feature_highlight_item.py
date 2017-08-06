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
        copyright            : 2011 by Jürgen E. Fischer
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

from PyQt4.QtCore import Qt
from PyQt4.QtGui import QBrush, QPen

from qgis.core import QgsFeature, QgsRectangle, QgsRenderContext, QgsSimpleMarkerSymbolLayerV2, QgsSymbolV2
from qgis.gui import QgsMapCanvasItem

from ..project import Project


class FeatureHighlightItem(QgsMapCanvasItem):
    # Code ported from QGIS QgsHighlight

    _mapCanvas = None  # QgsMapCanvas
    _brush = QBrush()
    _pen = QPen()
    _feature = None  # QgsFeature()
    _layer = None  # QgsMapLayer()
    _buffer = 0.0
    _minWidth = 0.0

    def __init__(self, mapCanvas, feature, layer):
        super(FeatureHighlight, self).__init__(mapCanvas)
        self._mapCanvas = mapCanvas
        if (not layer
            or not feature
            or not isinstance(feature, QgsFeature)
            or not feature.geometry()
            or feature.geometry().isEmpty()
            or not feature.geometry().isGeosValid()
            ):
            return
        self._feature = QgsFeature(feature)  # Force deep copy
        self._layer = layer
        self.setLineColor(Project.highlightLineColor())
        self.setFillColor(Project.highlightFillColor())
        self._minWidth = Project.highlightMinimumWidth()
        self._buffer = Project.highlightBuffer()
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
        if self._feature and self._feature.constGeometry():
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
                    if isinstance(symbolLayer, QgsSimpleMarkerSymbolLayerV2):
                        symbolLayer.setOutlineWidth(
                            self._getSymbolWidth(context, symbolLayer.outlineWidth(), symbolLayer.outlineWidthUnit()))
                    if symbolLayer.type() == QgsSymbolV2.Line:
                        symbolLayer.setWidth(
                            self._getSymbolWidth(context, symbolLayer.width(), symbolLayer.widthUnit()))
                    if symbolLayer.type() == QgsSymbolV2.Fill:
                        symbolLayer.setBorderWidth(
                            self._getSymbolWidth(context, symbolLayer.borderWidth(), symbolLayer.outputUnit()))
                    symbolLayer.removeDataDefinedProperty('color')
                    symbolLayer.removeDataDefinedProperty('color_border')

    def _getSymbolWidth(self, context, width, unit):
        scale = 1.0
        if unit == QgsSymbolV2.MapUnit:
            scale = QgsSymbolLayerV2Utils.lineWidthScaleFactor(
                context, QgsSymbolV2.MM) / QgsSymbolLayerV2Utils.lineWidthScaleFactor(context, QgsSymbolV2.MapUnit)
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
