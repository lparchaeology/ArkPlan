# -*- coding: utf-8 -*-
"""
/***************************************************************************
                                      Ark
                                 A QGIS plugin
             QGIS Plugin for ARK, the Archaeological Recording Kit
                              -------------------
        begin                : 2015-03-02
        git sha              : $Format:%H$
        copyright            : (C) 2015 by L - P: Heritage LLP
        copyright            : (C) 2015 by John Layt
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

import math

from PyQt4.QtCore import Qt, QObject, QVariant, QPoint
from PyQt4.QtGui import QAction, QIcon, QFileDialog

from qgis.core import *

from ..core.utils import *
from ..core.map_tools import ArkMapToolEmitPoint
from ..core.project import Project

from update_layer_dialog import UpdateLayerDialog
from create_grid_dialog import CreateGridDialog
from grid_dock import GridDock

# Based on LinearTransformer code from VectorBender plugin
# (C) 2014 by Olivier Dalang
class LinearTransformer():

    def __init__(self, a1, b1, a2, b2):
        #scale
        self.ds = math.sqrt((b2.x() - b1.x()) ** 2.0 + (b2.y() - b1.y()) ** 2.0) / math.sqrt((a2.x() - a1.x()) ** 2.0 + (a2.y() - a1.y()) ** 2.0)
        #rotation
        self.da =  math.atan2(b2.y() - b1.y(), b2.x() - b1.x()) - math.atan2(a2.y() - a1.y(), a2.x() - a1.x() )
        #translation
        self.dx1 = a1.x()
        self.dy1 = a1.y()
        self.dx2 = b1.x()
        self.dy2 = b1.y()

    def map(self, p):
        #move to origin (translation part 1)
        p = QgsPoint( p.x()-self.dx1, p.y()-self.dy1 )
        #scale
        p = QgsPoint( self.ds*p.x(), self.ds*p.y() )
        #rotation
        p = QgsPoint(math.cos(self.da) * p.x() - math.sin(self.da) * p.y(), math.sin(self.da) * p.x() + math.cos(self.da) * p.y())
        #remove to right spot (translation part 2)
        p = QgsPoint(p.x() + self.dx2, p.y() + self.dy2)

        return p


class GridModule(QObject):

    project = None # Project()

    # Internal variables
    mapTool = None  #ArkMapToolEmitPoint()
    initialised = False
    createDialog = None  # QDialog

    def __init__(self, project):
        super(GridModule, self).__init__()
        self.project = project

    # Standard Dock methods

    # Load the module when plugin is loaded
    def load(self):
        self.dock = GridDock()
        self.dock.load(self.project.iface, Qt.LeftDockWidgetArea, self.project.createMenuAction(self.tr(u'Local Grid'), ':/plugins/Ark/grid/view-grid.png', True))
        self.dock.toggled.connect(self.run)
        self.dock.createGridSelected.connect(self.showCreateGridDialog)
        self.dock.identifyGridSelected.connect(self.enableMapTool)
        self.dock.updateLayerSelected.connect(self.showUpdateLayerDialog)
        self.dock.convertMapSelected.connect(self.convertMapPoint)
        self.dock.convertLocalSelected.connect(self.convertLocalPoint)
        self.dock.setReadOnly(True)
        self.dock.createGridTool.setEnabled(False)

    # Unload the module when plugin is unloaded
    def unload(self):
        self.dock.unload()

    def run(self, checked):
        if checked:
            self.initialise()

    def initialise(self):
        if self.initialised:
            return

        if (not self.project.initialise()):
            self.dock.setReadOnly(True)
            self.dock.createGridTool.setEnabled(False)
            return
        self.dock.createGridTool.setEnabled(True)

        # Check if files exist or need creating
        # Run create if needed

        if self.project.grid.pointsLayer is None:
            return

        features = []
        for feature in self.project.grid.pointsLayer.getFeatures():
            features.append(feature)
        if len(features) < 2:
            return
        map1, local1 = self.transformPoints(features[0])
        map2, local2 = self.transformPoints(features[1])
        self.mapTransformer = LinearTransformer(map1, local1, map2, local2)
        self.localTransformer = LinearTransformer(local1, map1, local2, map2)

        self.mapTool = ArkMapToolEmitPoint(self.project.iface.mapCanvas())
        self.mapTool.setAction(self.dock.identifyGridAction)
        self.mapTool.canvasClicked.connect(self.pointSelected)

        self.dock.setReadOnly(False)
        self.initialised = True

    def transformPoints(self, feature):
        mapPoint = feature.geometry().asPoint()
        localX = feature.attribute(self.project.fieldName('local_x'))
        localY = feature.attribute(self.project.fieldName('local_y'))
        localPoint = QgsPoint(localX, localY)
        return mapPoint, localPoint

    # Grid methods

    def showCreateGridDialog(self):
        self.initialise()
        if self.createDialog is None:
            self.createDialog = CreateGridDialog(self.project, self.project.iface.mainWindow())
            self.createDialog.accepted.connect(self.createGridDialogAccepted)
        self.createDialog.show()
        self.createDialog._showDialog()

    def createGridDialogAccepted(self):
        if self.createGrid(self.createDialog.mapOriginPoint(), self.createDialog.mapAxisPoint(),
                           self.createDialog.mapAxisPointType(),
                           self.createDialog.localOriginPoint(), self.createDialog.localTerminusPoint(),
                           self.createDialog.localEastingInterval(), self.createDialog.localEastingInterval()):
            self.project.iface.mapCanvas().refresh()
            self.dock.setReadOnly(False)
            self.project.showMessage('Grid successfully created')

    def createGrid(self, mapOrigin, mapAxis, mapAxisType, localOrigin, localTerminus, xInterval, yInterval):
        axisGeometry = QgsGeometry.fromPolyline([mapOrigin, mapAxis])
        mapAxisPoint = None
        localAxisPoint = None
        if mapAxisType == CreateGridDialog.PointOnYAxis:
            if axisGeometry.length() < yInterval:
                self.project.showCriticalMessage('Cannot create grid: Input axis must be longer than local interval')
                return False
            mapAxisPoint = axisGeometry.interpolate(yInterval).asPoint()
            localAxisPoint = QgsPoint(localOrigin.x(), localOrigin.y() + yInterval)
        else:
            if axisGeometry.length() < xInterval:
                self.project.showCriticalMessage('Cannot create grid: Input axis must be longer than local interval')
                return False
            mapAxisPoint = axisGeometry.interpolate(xInterval).asPoint()
            localAxisPoint = QgsPoint(localOrigin.x() + xInterval, localOrigin.y())
        localTransformer = LinearTransformer(localOrigin, mapOrigin, localAxisPoint, mapAxisPoint)
        local_x = self.project.fieldName('local_x')
        local_y = self.project.fieldName('local_y')
        map_x = self.project.fieldName('map_x')
        map_y = self.project.fieldName('map_y')

        points = self.project.grid.pointsLayer
        if (points is None or not points.isValid()):
            self.project.showCriticalMessage('Invalid grid points file, cannot create grid!')
            return False
        self._addGridPointsToLayer(points, localTransformer,
                                   localOrigin.x(), xInterval, (localTerminus.x() - localOrigin.x()) / xInterval,
                                   localOrigin.y(), yInterval, (localTerminus.y() - localOrigin.y()) / yInterval,
                                   self._attributes(points, 'gpt'), local_x, local_y, map_x, map_y)

        if self.project.linesLayerName('grid'):
            lines = self.project.grid.linesLayer
            if lines is None or not lines.isValid():
                self.project.showCriticalMessage('Invalid grid lines file!')
            else:
                self._addGridLinesToLayer(lines, localTransformer,
                                          localOrigin.x(), xInterval, (localTerminus.x() - localOrigin.x()) / xInterval,
                                          localOrigin.y(), yInterval, (localTerminus.y() - localOrigin.y()) / yInterval,
                                          self._attributes(lines, 'gln'), local_x, local_y, map_x, map_y)

        if self.project.polygonsLayerName('grid'):
            polygons = self.project.grid.polygonsLayer
            if lines is None or not lines.isValid():
                self.project.showCriticalMessage('Invalid grid polygons file!')
            else:
                self._addGridPolygonsToLayer(polygons, localTransformer,
                                             localOrigin.x(), xInterval, (localTerminus.x() - localOrigin.x()) / xInterval,
                                             localOrigin.y(), yInterval, (localTerminus.y() - localOrigin.y()) / yInterval,
                                             self._attributes(polygons, 'gpg'), local_x, local_y, map_x, map_y)
        return True

    def _attributes(self, layer, category):
        attributes = {}
        attributes[layer.fieldNameIndex(self.project.fieldName('site'))] = self.project.siteCode()
        attributes[layer.fieldNameIndex(self.project.fieldName('category'))] = category
        attributes[layer.fieldNameIndex(self.project.fieldName('source'))] = 'ARK'
        attributes[layer.fieldNameIndex(self.project.fieldName('created_on'))] = self.project.timestamp()
        attributes[layer.fieldNameIndex(self.project.fieldName('created_by'))] = 'Grid Tool'
        return attributes

    def _setAttributes(self, feature, attributes):
        for key in attributes.keys():
            feature.setAttribute(key, attributes[key])

    def _addGridPointsToLayer(self, layer, transformer, originX, intervalX, repeatX, originY, intervalY, repeatY, attributes, localFieldX='local_x', localFieldY='local_x', mapFieldX='map_x', mapFieldY='map_y'):
        if (layer is None or not layer.isValid() or layer.geometryType() != QGis.Point):
            return
        features = []
        for localX in range(originX, originX + (intervalX * repeatX) + 1, intervalX):
            for localY in range(originY, originY + (intervalY * repeatY) + 1, intervalY):
                localPoint = QgsPoint(localX, localY)
                mapPoint = transformer.map(localPoint)
                feature = QgsFeature(layer.dataProvider().fields())
                feature.setGeometry(QgsGeometry.fromPoint(mapPoint))
                self._setAttributes(feature, attributes)
                feature.setAttribute(localFieldX, localX)
                feature.setAttribute(localFieldY, localY)
                feature.setAttribute(mapFieldX, mapPoint.x())
                feature.setAttribute(mapFieldY, mapPoint.y())
                features.append(feature)
        layer.dataProvider().addFeatures(features)

    def _addGridLinesToLayer(self, layer, transformer, originX, intervalX, repeatX, originY, intervalY, repeatY, attributes, localFieldX='local_x', localFieldY='local_x', mapFieldX='map_x', mapFieldY='map_y'):
        if (layer is None or not layer.isValid() or layer.geometryType() != QGis.Line):
            return
        features = []
        terminusX = originX + (intervalX * repeatX)
        terminusY = originY + (intervalY * repeatY)
        for localX in range(originX, originX + (intervalX * repeatX) + 1, intervalX):
            localStartPoint = QgsPoint(localX, originY)
            localEndPoint = QgsPoint(localX, terminusY)
            mapStartPoint = transformer.map(localStartPoint)
            mapEndPoint = transformer.map(localEndPoint)
            feature = QgsFeature(layer.dataProvider().fields())
            feature.setGeometry(QgsGeometry.fromPolyline([mapStartPoint, mapEndPoint]))
            self._setAttributes(feature, attributes)
            feature.setAttribute(localFieldX, localX)
            feature.setAttribute(mapFieldX, mapStartPoint.x())
            features.append(feature)
        for localY in range(originY, originY + (intervalY * repeatY) + 1, intervalY):
            localStartPoint = QgsPoint(originX, localY)
            localEndPoint = QgsPoint(terminusX, localY)
            mapStartPoint = transformer.map(localStartPoint)
            mapEndPoint = transformer.map(localEndPoint)
            feature = QgsFeature(layer.dataProvider().fields())
            feature.setGeometry(QgsGeometry.fromPolyline([mapStartPoint, mapEndPoint]))
            self._setAttributes(feature, attributes)
            feature.setAttribute(localFieldY, localY)
            feature.setAttribute(mapFieldY, mapStartPoint.y())
            features.append(feature)
        layer.dataProvider().addFeatures(features)

    def _addGridPolygonsToLayer(self, layer, transformer, originX, intervalX, repeatX, originY, intervalY, repeatY, attributes, localFieldX='local_x', localFieldY='local_x', mapFieldX='map_x', mapFieldY='map_y'):
        if (layer is None or not layer.isValid() or layer.geometryType() != QGis.Polygon):
            return
        features = []
        for localX in range(originX, originX + intervalX * repeatX, intervalX):
            for localY in range(originY, originY + intervalY * repeatY, intervalY):
                localPoint = QgsPoint(localX, localY)
                mapPoint = transformer.map(localPoint)
                points = []
                points.append(transformer.map(localPoint))
                points.append(transformer.map(QgsPoint(localX, localY + intervalY)))
                points.append(transformer.map(QgsPoint(localX + intervalX, localY + intervalY)))
                points.append(transformer.map(QgsPoint(localX + intervalX, localY)))
                feature = QgsFeature(layer.dataProvider().fields())
                feature.setGeometry(QgsGeometry.fromPolygon([points]))
                self._setAttributes(feature, attributes)
                feature.setAttribute(localFieldX, localX)
                feature.setAttribute(localFieldY, localY)
                feature.setAttribute(mapFieldX, mapPoint.x())
                feature.setAttribute(mapFieldY, mapPoint.y())
                features.append(feature)
        layer.dataProvider().addFeatures(features)

    def enableMapTool(self, status):
        if not self.initialised:
            self.initialise()
        if self.initialised:
            if status:
                self.project.iface.mapCanvas().setMapTool(self.mapTool)
            else:
                self.project.iface.mapCanvas().unsetMapTool(self.mapTool)
        elif status:
            self.dock.identifyGridAction.setChecked(False)

    def pointSelected(self, point, button):
        if not self.initialised:
            return
        if (button == Qt.LeftButton):
            if not self.dock.menuAction().isChecked():
                self.dock.menuAction().toggle()
            self.dock.setMapPoint(point)
            self.convertMapPoint()

    def convertMapPoint(self):
        if not self.initialised:
            return
        localPoint = self.mapTransformer.map(self.dock.mapPoint())
        self.dock.setLocalPoint(localPoint)

    def convertLocalPoint(self):
        if not self.initialised:
            return
        mapPoint = self.localTransformer.map(self.dock.localPoint())
        self.dock.setMapPoint(mapPoint)

    def showUpdateLayerDialog(self):
        if not self.initialised:
            self.initialise()
        if self.initialised:
            dialog = UpdateLayerDialog(self.project.iface)
            if dialog.exec_():
                self.updateLayerCoordinates(dialog.layer(), dialog.updateGeometry(), dialog.createMapFields())

    def updateLayerCoordinates(self, layer, updateGeometry, createMapFields):
        if (not self.initialised or layer is None or not layer.isValid() or layer.geometryType() != QGis.Point):
            return False
        local_x = self.project.fieldName('local_x')
        local_y = self.project.fieldName('local_y')
        map_x = self.project.fieldName('map_x')
        map_y = self.project.fieldName('map_y')
        if layer.startEditing():
            if layer.fieldNameIndex(local_x) < 0:
                layer.dataProvider().addAttributes([self.project.field('local_x')])
            if layer.fieldNameIndex(local_y) < 0:
                layer.dataProvider().addAttributes([self.project.field('local_y')])
            if (createMapFields and layer.fieldNameIndex(map_x) < 0):
                layer.dataProvider().addAttributes([self.project.field('map_x')])
            if (createMapFields and layer.fieldNameIndex(map_y) < 0):
                layer.dataProvider().addAttributes([self.project.field('map_y')])
            local_x_idx = layer.fieldNameIndex(local_x)
            local_y_idx = layer.fieldNameIndex(local_y)
            map_x_idx = layer.fieldNameIndex(map_x)
            map_y_idx = layer.fieldNameIndex(map_y)
            if updateGeometry:
                for feature in layer.getFeatures():
                    localPoint = QgsPoint(feature.attribute(local_x), feature.attribute(local_y))
                    mapPoint = self.localTransformer.map(localPoint)
                    layer.changeGeometry(feature.id(), QgsGeometry.fromPoint(mapPoint))
            for feature in layer.getFeatures():
                mapPoint = feature.geometry().asPoint()
                localPoint = self.mapTransformer.map(mapPoint)
                layer.changeAttributeValue(feature.id(), local_x_idx, localPoint.x())
                layer.changeAttributeValue(feature.id(), local_y_idx, localPoint.y())
                layer.changeAttributeValue(feature.id(), map_x_idx, mapPoint.x())
                layer.changeAttributeValue(feature.id(), map_y_idx, mapPoint.y())
            return layer.commitChanges()
        return False
