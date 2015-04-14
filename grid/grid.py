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
from ..core.settings import Settings
from ..core.layers import LayerManager

from ..core.select_layer_dialog import SelectLayerDialog
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

    settings = None # Settings()
    layers = None  # LayerManager()

    # Internal variables
    mapTool = None  # QgsMapToolEmitPoint()
    initialised = False

    def __init__(self, settings, layers):
        super(GridModule, self).__init__()
        self.settings = settings
        self.layers = layers


    # Standard Dock methods

    # Load the module when plugin is loaded
    def load(self):
        self.createGridAction = self.settings.createMenuAction(self.tr(u'Create New Grid'), ':/plugins/Ark/grid/get-hot-new-stuff.png', False)
        self.createGridAction.triggered.connect(self.showCreateGridDialog)

        self.identifyGridAction = self.settings.createMenuAction(self.tr(u'Identify Grid Coordinates'), ':/plugins/Ark/grid/snap-orthogonal.png', True)
        self.identifyGridAction.toggled.connect(self.enableMapTool)

        self.addLocalAction = self.settings.createMenuAction(self.tr(u'Add Local Coords To Layer'), ':/images/themes/default/mActionNewAttribute.png', False)
        self.addLocalAction.triggered.connect(self.selectLayerForLocal)

        self.dock = GridDock()
        self.dock.load(self.settings.iface, Qt.LeftDockWidgetArea, self.settings.createMenuAction(self.tr(u'Local Grid'), ':/plugins/Ark/grid/view-grid.png', True))
        self.dock.toggled.connect(self.run)
        self.dock.convertCrsSelected.connect(self.convertCrs)
        self.dock.convertLocalSelected.connect(self.convertLocal)


    # Unload the module when plugin is unloaded
    def unload(self):
        self.settings.iface.removeToolBarIcon(self.addLocalAction)
        self.settings.iface.removeToolBarIcon(self.createGridAction)
        self.settings.iface.removeToolBarIcon(self.identifyGridAction)
        self.dock.unload()


    def run(self, checked):
        if checked:
            self.initialise()


    def initialise(self):
        if self.initialised:
            return

        if (not self.settings.isConfigured()):
            self.settings.configure()
        if (not self.settings.isConfigured()):
            return
        self.layers.initialise()
        if self.layers.grid.pointsLayer is None:
            return

        features = []
        for feature in self.layers.grid.pointsLayer.getFeatures():
            features.append(feature)
        if len(features) < 2:
            return
        self.layers.grid.pointsLayer.removeSelection()
        crs1, local1 = self.transformPoints(features[0])
        crs2, local2 = self.transformPoints(features[1])
        self.crsTransformer = LinearTransformer(crs1, local1, crs2, local2)
        self.localTransformer = LinearTransformer(local1, crs1, local2, crs2)

        self.mapTool = QgsMapToolEmitPoint(self.settings.iface.mapCanvas())
        self.mapTool.canvasClicked.connect(self.pointSelected)

        self.dock.setReadOnly(False)
        self.initialised = True


    def transformPoints(self, feature):
        crsPoint = feature.geometry().asPoint()
        localX = feature.attribute(self.settings.gridPointsFieldX)
        localY = feature.attribute(self.settings.gridPointsFieldY)
        localPoint = QgsPoint(localX, localY)
        return crsPoint, localPoint


    # Grid methods

    def showCreateGridDialog(self):
        dialog = CreateGridDialog(self, self.settings.iface.mainWindow())
        if dialog.exec_():
            crsOrigin = QgsPoint(dialog.crsOriginEastingSpin.value(), dialog.crsOriginNorthingSpin.value())
            crsTerminus = QgsPoint(dialog.crsTerminusEastingSpin.value(), dialog.crsTerminusNorthingSpin.value())
            localOrigin = QPoint(dialog.localOriginEastingSpin.value(), dialog.localOriginNorthingSpin.value())
            localTerminus = QPoint(dialog.localTerminusEastingSpin.value(), dialog.localTerminusNorthingSpin.value())
            if self.createGrid(crsOrigin, crsTerminus, localOrigin, localTerminus, dialog.localIntervalSpin.value()):
                self.settings.showMessage('Grid files successfully created')


    def createGrid(self, crsOrigin, crsTerminus, localOrigin, localTerminus, localInterval):
        localTransformer = LinearTransformer(localOrigin, crsOrigin, localTerminus, crsTerminus)
        fields = QgsFields()
        fields.append(self.settings.fieldDefinitions['local_x'])
        fields.append(self.settings.fieldDefinitions['local_y'])
        local_x = self.settings.fieldDefinitions['local_x'].name()
        local_y = self.settings.fieldDefinitions['local_y'].name()

        pointsPath = self.settings.gridPath() + '/' + self.settings.gridPointsLayerName() + '.shp'
        points = QgsVectorFileWriter(pointsPath, 'System', fields, QGis.WKBPoint, self.settings.projectCrs(), 'ESRI Shapefile')
        if points.hasError() != QgsVectorFileWriter.NoError:
            self.settings.showCriticalMessage('Create grid points file failed!!!')
            return
        for localX in range(localOrigin.x(), localTerminus.x() + 1, localInterval):
            for localY in range(localOrigin.y(), localTerminus.y() + 1, localInterval):
                localPoint = QgsPoint(localX, localY)
                crsPoint = localTransformer.map(localPoint)
                feature = QgsFeature(fields)
                feature.setGeometry(QgsGeometry.fromPoint(crsPoint))
                feature.setAttribute(local_x, localX)
                feature.setAttribute(local_y, localY)
                points.addFeature(feature)
        del points

        if self.settings.gridLinesLayerName():
            linesPath = self.settings.gridPath() + '/' + self.settings.gridLinesLayerName() + '.shp'
            lines = QgsVectorFileWriter(linesPath, 'System', fields, QGis.WKBLineString, self.settings.projectCrs(), 'ESRI Shapefile')
            if lines.hasError() != QgsVectorFileWriter.NoError:
                self.settings.showCriticalMessage('Create grid lines file failed!!!')
                return
            for localX in range(localOrigin.x(), localTerminus.x() + 1, localInterval):
                localStartPoint = QgsPoint(localX, localOrigin.y())
                localEndPoint = QgsPoint(localX, localTerminus.y())
                crsStartPoint = localTransformer.map(localStartPoint)
                crsEndPoint = localTransformer.map(localEndPoint)
                feature = QgsFeature(fields)
                feature.setGeometry(QgsGeometry.fromPolyline([crsStartPoint, crsEndPoint]))
                feature.setAttribute(local_x, localX)
                lines.addFeature(feature)
            for localY in range(localOrigin.y(), localTerminus.y() + 1, localInterval):
                localStartPoint = QgsPoint(localOrigin.x(), localY)
                localEndPoint = QgsPoint(localTerminus.x(), localY)
                crsStartPoint = localTransformer.map(localStartPoint)
                crsEndPoint = localTransformer.map(localEndPoint)
                feature = QgsFeature(fields)
                feature.setGeometry(QgsGeometry.fromPolyline([crsStartPoint, crsEndPoint]))
                feature.setAttribute(local_y, localY)
                lines.addFeature(feature)
            del lines

        if self.settings.gridPolygonsLayerName():
            polygonsPath = self.settings.gridPath() + '/' + self.settings.gridPolygonsLayerName() + '.shp'
            polygons = QgsVectorFileWriter(polygonsPath, 'System', fields, QGis.WKBPolygon, self.settings.projectCrs(), 'ESRI Shapefile')
            if polygons.hasError() != QgsVectorFileWriter.NoError:
                self.settings.showCriticalMessage('Create grid polygons file failed!!!')
                return
            for localX in range(localOrigin.x(), localTerminus.x(), localInterval):
                for localY in range(localOrigin.y(), localTerminus.y(), localInterval):
                    localPoint = QgsPoint(localX, localY)
                    points = []
                    points.append(localTransformer.map(QgsPoint(localPoint.x(), localPoint.y())))
                    points.append(localTransformer.map(QgsPoint(localPoint.x(), localPoint.y() + localInterval)))
                    points.append(localTransformer.map(QgsPoint(localPoint.x() + localInterval, localPoint.y() + localInterval)))
                    points.append(localTransformer.map(QgsPoint(localPoint.x() + localInterval, localPoint.y())))
                    feature = QgsFeature(fields)
                    feature.setGeometry(QgsGeometry.fromPolygon([points]))
                    feature.setAttribute(local_x, localX)
                    feature.setAttribute(local_y, localY)
                    polygons.addFeature(feature)
            del polygons

    def enableMapTool(self, status):
        if not self.initialised:
            self.initialise()
        if self.initialised:
            if status:
                self.settings.iface.mapCanvas().setMapTool(self.mapTool)
            else:
                self.settings.iface.mapCanvas().unsetMapTool(self.mapTool)
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


    def selectLayerForLocal(self):
        if not self.initialised:
            self.initialise()
        if self.initialised:
            dialog = SelectLayerDialog(self.settings.iface, QgsMapLayer.VectorLayer, QGis.Point)
            if dialog.exec_():
                self.addLocalToLayer(dialog.layer())


    def addLocalToLayer(self, layer):
        if not self.initialised:
            return
        local_x = self.settings.fieldDefinitions['local_x'].name()
        local_y = self.settings.fieldDefinitions['local_y'].name()
        layer.dataProvider().addAttributes([self.settings.fieldDefinitions['local_x'], self.settings.fieldDefinitions['local_y']])
        if layer.startEditing():
            local_x_idx = layer.fieldNameIndex(local_x)
            local_y_idx = layer.fieldNameIndex(local_y)
            for feature in layer.getFeatures():
                geom = feature.geometry()
                if geom.type() == QGis.Point:
                    localPoint = self.crsTransformer.map(geom.asPoint())
                    layer.changeAttributeValue(feature.id(), local_x_idx, localPoint.x())
                    layer.changeAttributeValue(feature.id(), local_y_idx, localPoint.y())
            ok = layer.commitChanges()
            return ok
        return False
