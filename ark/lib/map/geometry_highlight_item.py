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
        copyright            : 2011 by Jürgen E. Fischer
 ***************************************************************************/
"""

from PyQt4.QtCore import Qt
from PyQt4.QtGui import QBrush, QColor, QPainterPath, QPen, QPolygonF

from qgis.core import QGis, QgsGeometry, QgsRectangle
from qgis.gui import QgsMapCanvasItem

from ..application import Application


class GeometryHighlightItem(QgsMapCanvasItem):
    # Code ported from QGIS QgsHighlight

    _mapCanvas = None  # QgsMapCanvas
    _geometry = None  # QgsGeometry()
    _brush = QBrush()
    _pen = QPen()

    def __init__(self, mapCanvas, geometry, layer):
        super(GeometryHighlightItem, self).__init__(mapCanvas)
        self._mapCanvas = mapCanvas
        if not geometry or not isinstance(geometry, QgsGeometry) or geometry.isEmpty() or not geometry.isGeosValid():
            return
        self._geometry = QgsGeometry(geometry)  # Force deep copy
        self.setLineColor(Application.highlightLineColor())
        self.setFillColor(Application.highlightFillColor())
        if (layer and self._mapCanvas.mapSettings().hasCrsTransformEnabled()):
            ct = self._mapCanvas.mapSettings().layerTransform(layer)
            if ct:
                self._geometry.transform(ct)
        self.updateRect()
        self.update()

    def remove(self):
        self._mapCanvas.scene().removeItem(self)

    def setLineWidth(self, width):
        self._pen.setWidth(width)

    def setLineColor(self, color):
        lineColor = QColor(color)
        lineColor.setAlpha(255)
        self._pen.setColor(lineColor)

    def setFillColor(self, fillColor):
        self._brush.setColor(fillColor)
        self._brush.setStyle(Qt.SolidPattern)

    def updatePosition(self):
        pass

    # protected:
    def paint(self, painter, option=None, widget=None):  # Override
        if not self._geometry:
            return

        painter.setPen(self._pen)
        painter.setBrush(self._brush)

        wkbType = self._geometry.wkbType()
        if wkbType == QGis.WKBPoint or wkbType == QGis.WKBPoint25D:
            self._paintPoint(painter, self._geometry.geometry())
        elif wkbType == QGis.WKBMultiPoint or wkbType == QGis.WKBMultiPoint25D:
            for point in self._geometry.geometry():
                self._paintPoint(painter, point)
        elif wkbType == QGis.WKBLineString or wkbType == QGis.WKBLineString25D:
            self._paintLine(painter, self._geometry.geometry())
        elif wkbType == QGis.WKBMultiLineString or wkbType == QGis.WKBMultiLineString25D:
            for line in self._geometry.geometry():
                self._paintLine(painter, line)
        elif wkbType == QGis.WKBPolygon or wkbType == QGis.WKBPolygon25D:
            self._paintPolygon(painter, self._geometry.geometry())
        elif wkbType == QGis.WKBMultiPolygon or wkbType == QGis.WKBMultiPolygon25D:
            for polygon in self._geometry.geometry():
                self._paintPolygon(painter, polygon)

    def updateRect(self):
        if self._geometry:
            r = self._geometry.boundingBox()
            if r.isEmpty():
                d = self._mapCanvas.extent().width() * 0.005
                r.setXMinimum(r.xMinimum() - d)
                r.setYMinimum(r.yMinimum() - d)
                r.setXMaximum(r.xMaximum() + d)
                r.setYMaximum(r.yMaximum() + d)
            self.setRect(r)
            self.setVisible(True)
        else:
            self.setRect(QgsRectangle())

    # private:

    def _paintPoint(self, painter, point):
        painter.drawEllipse(self.toCanvasCoordinates(point) - self.pos(), 2, 2)

    def _paintLine(self, painter, line):
        polyline = QPolygonF()
        for point in line:
            polyline.append(self.toCanvasCoordinates(point) - self.pos())
        painter.drawPolyline(polyline)

    def _paintPolygon(self, painter, polygon):
        path = QPainterPath()
        for line in polygon:
            ring = QPolygonF()
            for point in line:
                cur = self.toCanvasCoordinates(point) - self.pos()
                ring.append(cur)
            ring.append(ring[0])
            path.addPolygon(ring)
        painter.drawPath(path)
