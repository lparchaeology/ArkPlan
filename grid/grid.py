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
from qgis.gui import QgsMapToolEmitPoint

from ..core.utils import *
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
    mapTool = None  # QgsMapToolEmitPoint()
    initialised = False

    def __init__(self, project):
        super(GridModule, self).__init__()
        self.project = project


    # Standard Dock methods

    # Load the module when plugin is loaded
    def load(self):
        self.createGridAction = self.project.createMenuAction(self.tr(u'Create New Grid'), ':/plugins/Ark/grid/get-hot-new-stuff.png', False)
        self.createGridAction.triggered.connect(self.showCreateGridDialog)

        self.identifyGridAction = self.project.createMenuAction(self.tr(u'Identify Grid Coordinates'), ':/plugins/Ark/grid/snap-orthogonal.png', True)
        self.identifyGridAction.toggled.connect(self.enableMapTool)

        self.updateLayerAction = self.project.createMenuAction(self.tr(u'Update Layer Coordinates'), ':/images/themes/default/mActionNewAttribute.png', False)
        self.updateLayerAction.triggered.connect(self.showUpdateLayerDialog)

        self.dock = GridDock()
        self.dock.load(self.project.iface, Qt.LeftDockWidgetArea, self.project.createMenuAction(self.tr(u'Local Grid'), ':/plugins/Ark/grid/view-grid.png', True))
        self.dock.toggled.connect(self.run)
        self.dock.convertCrsSelected.connect(self.convertCrs)
        self.dock.convertLocalSelected.connect(self.convertLocal)


    # Unload the module when plugin is unloaded
    def unload(self):
        self.project.iface.removeToolBarIcon(self.updateLayerAction)
        self.project.iface.removeToolBarIcon(self.createGridAction)
        self.project.iface.removeToolBarIcon(self.identifyGridAction)
        self.dock.unload()


    def run(self, checked):
        if checked:
            self.initialise()


    def initialise(self):
        if self.initialised:
            return

        if (not self.project.initialise()):
            return

        # Check if files exist or need creating
        # Run create if needed

        if self.project.grid.pointsLayer is None:
            return

        features = []
        for feature in self.project.grid.pointsLayer.getFeatures():
            features.append(feature)
        if len(features) < 2:
            return
        crs1, local1 = self.transformPoints(features[0])
        crs2, local2 = self.transformPoints(features[1])
        self.crsTransformer = LinearTransformer(crs1, local1, crs2, local2)
        self.localTransformer = LinearTransformer(local1, crs1, local2, crs2)

        self.mapTool = QgsMapToolEmitPoint(self.project.iface.mapCanvas())
        self.mapTool.canvasClicked.connect(self.pointSelected)

        self.dock.setReadOnly(False)
        self.initialised = True


    def transformPoints(self, feature):
        crsPoint = feature.geometry().asPoint()
        localX = feature.attribute(self.project.fieldName('local_x'))
        localY = feature.attribute(self.project.fieldName('local_y'))
        localPoint = QgsPoint(localX, localY)
        return crsPoint, localPoint


    # Grid methods

    def showCreateGridDialog(self):
        self.initialise()
        dialog = CreateGridDialog(self, self.project.iface.mainWindow())
        if dialog.exec_():
            crsOrigin = QgsPoint(dialog.crsOriginEastingSpin.value(), dialog.crsOriginNorthingSpin.value())
            crsTerminus = QgsPoint(dialog.crsTerminusEastingSpin.value(), dialog.crsTerminusNorthingSpin.value())
            localOrigin = QPoint(dialog.localOriginEastingSpin.value(), dialog.localOriginNorthingSpin.value())
            localTerminus = QPoint(dialog.localTerminusEastingSpin.value(), dialog.localTerminusNorthingSpin.value())
            if self.createGrid(crsOrigin, crsTerminus, localOrigin, localTerminus, dialog.localIntervalSpin.value()):
                self.project.showMessage('Grid files successfully created')


    def createGrid(self, crsOrigin, crsTerminus, localOrigin, localTerminus, localInterval):
        localTransformer = LinearTransformer(localOrigin, crsOrigin, localTerminus, crsTerminus)
        local_x = self.project.fieldName('local_x')
        local_y = self.project.fieldName('local_y')
        crs_x = self.project.fieldName('crs_x')
        crs_y = self.project.fieldName('crs_y')

        points = self.project.grid.pointsLayer
        if (points is None or not points.isValid()):
            self.project.showCriticalMessage('Invalid grid points file, cannot create grid!')
            return
        self._addGridPointsToLayer(points, localTransformer,
                                   localOrigin.x(), localInterval, (localTerminus.x() - localOrigin.x()) / localInterval,
                                   localOrigin.y(), localInterval, (localTerminus.y() - localOrigin.y()) / localInterval,
                                   self._attributes(points, 'gpt'), local_x, local_y, crs_x, crs_y)

        if self.project.linesLayerName('grid'):
            lines = self.project.grid.linesLayer
            if lines is None or not lines.isValid():
                self.project.showCriticalMessage('Invalid grid lines file!')
            else:
                self._addGridLinesToLayer(lines, localTransformer,
                                          localOrigin.x(), localInterval, (localTerminus.x() - localOrigin.x()) / localInterval,
                                          localOrigin.y(), localInterval, (localTerminus.y() - localOrigin.y()) / localInterval,
                                          self._attributes(lines, 'gln'), local_x, local_y, crs_x, crs_y)

        if self.project.polygonsLayerName('grid'):
            polygons = self.project.grid.polygonsLayer
            if lines is None or not lines.isValid():
                self.project.showCriticalMessage('Invalid grid polygons file!')
            else:
                self._addGridPolygonsToLayer(polygons, localTransformer,
                                             localOrigin.x(), localInterval, (localTerminus.x() - localOrigin.x()) / localInterval,
                                             localOrigin.y(), localInterval, (localTerminus.y() - localOrigin.y()) / localInterval,
                                             self._attributes(polygons, 'gpg'), local_x, local_y, crs_x, crs_y)


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


    def _addGridPointsToLayer(self, layer, transformer, originX, intervalX, repeatX, originY, intervalY, repeatY, attributes, localFieldX='local_x', localFieldY='local_x', crsFieldX='crs_x', crsFieldY='crs_y'):
        if (layer is None or not layer.isValid() or layer.geometryType() != QGis.Point):
            return
        features = []
        for localX in range(originX, originX + (intervalX * repeatX) + 1, intervalX):
            for localY in range(originY, originY + (intervalY * repeatY) + 1, intervalY):
                localPoint = QgsPoint(localX, localY)
                crsPoint = transformer.map(localPoint)
                feature = QgsFeature(layer.dataProvider().fields())
                feature.setGeometry(QgsGeometry.fromPoint(crsPoint))
                self._setAttributes(feature, attributes)
                feature.setAttribute(localFieldX, localX)
                feature.setAttribute(localFieldY, localY)
                feature.setAttribute(crsFieldX, crsPoint.x())
                feature.setAttribute(crsFieldY, crsPoint.y())
                features.append(feature)
        layer.dataProvider().addFeatures(features)


    def _addGridLinesToLayer(self, layer, transformer, originX, intervalX, repeatX, originY, intervalY, repeatY, attributes, localFieldX='local_x', localFieldY='local_x', crsFieldX='crs_x', crsFieldY='crs_y'):
        if (layer is None or not layer.isValid() or layer.geometryType() != QGis.Line):
            return
        features = []
        terminusX = originX + (intervalX * repeatX)
        terminusY = originY + (intervalY * repeatY)
        for localX in range(originX, originX + (intervalX * repeatX) + 1, intervalX):
            localStartPoint = QgsPoint(localX, originY)
            localEndPoint = QgsPoint(localX, terminusY)
            crsStartPoint = transformer.map(localStartPoint)
            crsEndPoint = transformer.map(localEndPoint)
            feature = QgsFeature(layer.dataProvider().fields())
            feature.setGeometry(QgsGeometry.fromPolyline([crsStartPoint, crsEndPoint]))
            self._setAttributes(feature, attributes)
            feature.setAttribute(localFieldX, localX)
            feature.setAttribute(crsFieldX, crsStartPoint.x())
            features.append(feature)
        for localY in range(originY, originY + (intervalY * repeatY) + 1, intervalY):
            localStartPoint = QgsPoint(originX, localY)
            localEndPoint = QgsPoint(terminusX, localY)
            crsStartPoint = transformer.map(localStartPoint)
            crsEndPoint = transformer.map(localEndPoint)
            feature = QgsFeature(layer.dataProvider().fields())
            feature.setGeometry(QgsGeometry.fromPolyline([crsStartPoint, crsEndPoint]))
            self._setAttributes(feature, attributes)
            feature.setAttribute(localFieldY, localY)
            feature.setAttribute(crsFieldY, crsStartPoint.y())
            features.append(feature)
        layer.dataProvider().addFeatures(features)


    def _addGridPolygonsToLayer(self, layer, transformer, originX, intervalX, repeatX, originY, intervalY, repeatY, attributes, localFieldX='local_x', localFieldY='local_x', crsFieldX='crs_x', crsFieldY='crs_y'):
        if (layer is None or not layer.isValid() or layer.geometryType() != QGis.Polygon):
            return
        features = []
        for localX in range(originX, originX + intervalX * repeatX, intervalX):
            for localY in range(originY, originY + intervalY * repeatY, intervalY):
                localPoint = QgsPoint(localX, localY)
                crsPoint = transformer.map(localPoint)
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
                feature.setAttribute(crsFieldX, crsPoint.x())
                feature.setAttribute(crsFieldY, crsPoint.y())
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
            self.identifyGridAction.setChecked(False)


    def pointSelected(self, point, button):
        if not self.initialised:
            return
        if (button == Qt.LeftButton):
            if not self.dock.menuAction().isChecked():
                self.dock.menuAction().toggle()
            self.dock.setCrsPoint(point)
            self.convertCrs()


    def convertCrs(self):
        if not self.initialised:
            return
        localPoint = self.crsTransformer.map(self.dock.crsPoint())
        self.dock.setLocalPoint(localPoint)


    def convertLocal(self):
        if not self.initialised:
            return
        crsPoint = self.localTransformer.map(self.dock.localPoint())
        self.dock.setCrsPoint(crsPoint)


    def showUpdateLayerDialog(self):
        if not self.initialised:
            self.initialise()
        if self.initialised:
            dialog = UpdateLayerDialog(self.project.iface)
            if dialog.exec_():
                self.updateLayerCoordinates(dialog.layer())


    def updateLayerCoordinates(self, layer):
        if not self.initialised:
            return
        local_x = self.project.fieldName('local_x')
        local_y = self.project.fieldName('local_y')
        crs_x = self.project.fieldName('crs_x')
        crs_y = self.project.fieldName('crs_y')
        if layer.startEditing():
            if layer.fieldNameIndex(local_x) < 0:
                layer.dataProvider().addAttributes([self.project.field('local_x')])
            if layer.fieldNameIndex(local_y) < 0:
                layer.dataProvider().addAttributes([self.project.field('local_y')])
            local_x_idx = layer.fieldNameIndex(local_x)
            local_y_idx = layer.fieldNameIndex(local_y)
            crs_x_idx = layer.fieldNameIndex(crs_x)
            crs_y_idx = layer.fieldNameIndex(crs_y)
            for feature in layer.getFeatures():
                geom = feature.geometry()
                if geom.type() == QGis.Point:
                    crsPoint = geom.asPoint()
                    localPoint = self.crsTransformer.map(crsPoint)
                    layer.changeAttributeValue(feature.id(), local_x_idx, localPoint.x())
                    layer.changeAttributeValue(feature.id(), local_y_idx, localPoint.y())
                    layer.changeAttributeValue(feature.id(), crs_x_idx, crsPoint.x())
                    layer.changeAttributeValue(feature.id(), crs_y_idx, crsPoint.y())
            return layer.commitChanges()
        return False
