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

from PyQt4.QtCore import Qt, QObject, QVariant, QPoint
from PyQt4.QtGui import QApplication, QAction, QIcon, QFileDialog

from qgis.core import *
from qgis.gui import QgsVertexMarker

from ..libarkqgis.maths import LinearTransformer
from ..libarkqgis import utils
from ..libarkqgis.map_tools import ArkMapToolEmitPoint

from ..core.project import Project

from translate_features_dialog import TranslateFeaturesDialog
from update_layer_dialog import UpdateLayerDialog
from grid_wizard import GridWizard
from grid_dock import GridDock

class GridModule(QObject):

    project = None # Project()

    # Internal variables
    mapTool = None  #ArkMapToolEmitPoint()
    initialised = False
    gridWizard = None  # QWizard

    def __init__(self, project):
        super(GridModule, self).__init__()
        self.project = project

    # Standard Dock methods

    # Load the module when plugin is loaded
    def load(self):
        self.dock = GridDock()
        action = self.project.plugin.addAction(':/plugins/ArkPlan/grid/view-grid.png', self.tr(u'Local Grid'), checkable=True)
        self.dock.load(self.project.plugin.iface, Qt.LeftDockWidgetArea, action)
        self.dock.toggled.connect(self.run)
        self.dock.createGridSelected.connect(self.showGridWizard)
        self.dock.identifyGridSelected.connect(self.enableMapTool)
        self.dock.updateLayerSelected.connect(self.showUpdateLayerDialog)
        self.dock.translateFeaturesSelected.connect(self.showTranslateFeaturesDialog)
        self.dock.panMapSelected.connect(self.panMapToPoint)
        self.dock.copyMapPointSelected.connect(self.copyMapPointToClipboard)
        self.dock.copyLocalPointSelected.connect(self.copyLocalPointToClipboard)
        self.dock.pasteMapPointSelected.connect(self.pasteMapPointFromClipboard)
        self.dock.addMapPointSelected.connect(self.addMapPointToLayer)
        self.dock.gridSelectionChanged.connect(self.changeGrid)
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

        self.loadGridNames()
        if not self.initialiseGrid(self.dock.siteCode(), self.dock.gridName()):
            return

        self.mapTool = ArkMapToolEmitPoint(self.project.plugin.mapCanvas())
        self.mapTool.setVertexIcon(QgsVertexMarker.ICON_CROSS)
        self.mapTool.setAction(self.dock.identifyGridAction)
        self.mapTool.canvasClicked.connect(self.pointSelected)

        self.dock.setReadOnly(False)
        self.initialised = True

    def loadGridNames(self):
        names = set()
        for feature in self.project.grid.pointsLayer.getFeatures():
            name = (feature.attribute(self.project.fieldName('site')),
                    feature.attribute(self.project.fieldName('name')))
            names.add(name)
        self.dock.setGridNames(list(names))

    def initialiseGrid(self, siteCode, gridName):
        features = []
        for feature in self.project.grid.pointsLayer.getFeatures():
            if (feature.attribute(self.project.fieldName('site')) == siteCode
                and feature.attribute(self.project.fieldName('name')) == gridName):
                features.append(feature)
        if len(features) < 2:
            return False
        map1, local1 = self.transformPoints(features[0])
        map2, local2 = self.transformPoints(features[1])
        self.mapTransformer = LinearTransformer(map1, local1, map2, local2)
        self.localTransformer = LinearTransformer(local1, map1, local2, map2)
        return True

    def changeGrid(self, siteCode, gridName):
        self.initialiseGrid(siteCode, gridName)
        self.dock.setMapPoint(QgsPoint(0, 0))
        self.dock.setLocalPoint(QgsPoint(0, 0))

    def transformPoints(self, feature):
        mapPoint = feature.geometry().asPoint()
        localX = feature.attribute(self.project.fieldName('local_x'))
        localY = feature.attribute(self.project.fieldName('local_y'))
        localPoint = QgsPoint(localX, localY)
        return mapPoint, localPoint

    # Grid methods

    def showGridWizard(self):
        self.initialise()
        if self.gridWizard is None:
            self.gridWizard = GridWizard(self.project.plugin.iface, self.project.siteCode(), self.project.plugin.iface.mainWindow())
            self.gridWizard.accepted.connect(self.createGridDialogAccepted)
        else:
            self.gridWizard.restart()
        self.gridWizard.show()
        self.gridWizard._showDialog()

    def createGridDialogAccepted(self):
        mp1 = self.gridWizard.mapPoint1()
        lp1 = self.gridWizard.localPoint1()
        mp2 = self.gridWizard.mapPoint2()
        lp2 = self.gridWizard.localPoint2()
        xInterval = self.gridWizard.localEastingInterval()
        yInterval = self.gridWizard.localNorthingInterval()
        if self.gridWizard.methodType() != GridWizard.TwoKnownPoints:
            axisGeometry = QgsGeometry.fromPolyline([mp1, mp2])
            mapAxisPoint = None
            localAxisPoint = None
            if self.gridWizard.methodType() == GridWizard.PointOnYAxis:
                if axisGeometry.length() < yInterval:
                    self.project.plugin.showCriticalMessage('Cannot create grid: Input axis must be longer than local interval')
                    return False
                mp2 = axisGeometry.interpolate(yInterval).asPoint()
                lp2 = QgsPoint(lp1.x(), lp1.y() + yInterval)
            else:
                if axisGeometry.length() < xInterval:
                    self.project.plugin.showCriticalMessage('Cannot create grid: Input axis must be longer than local interval')
                    return False
                mp2 = axisGeometry.interpolate(xInterval).asPoint()
                lp2 = QgsPoint(lp1.x() + xInterval, lp1.y())
        if self.createGrid(self.gridWizard.siteCode(), self.gridWizard.gridName(),
                           mp1, lp1, mp2, lp2,
                           self.gridWizard.localOriginPoint(), self.gridWizard.localTerminusPoint(),
                           xInterval, yInterval):
            self.project.plugin.mapCanvas().refresh()
            self.loadGridNames()
            self.dock.setReadOnly(False)
            self.project.plugin.showInfoMessage('Grid successfully created', 10)

    def createGrid(self, siteCode, gridName, mapPoint1, localPoint1, mapPoint2, localPoint2, localOrigin, localTerminus, xInterval, yInterval):
        localTransformer = LinearTransformer(localPoint1, mapPoint1, localPoint2, mapPoint2)
        local_x = self.project.fieldName('local_x')
        local_y = self.project.fieldName('local_y')
        map_x = self.project.fieldName('map_x')
        map_y = self.project.fieldName('map_y')

        points = self.project.grid.pointsLayer
        if (points is None or not points.isValid()):
            self.project.plugin.showCriticalMessage('Invalid grid points file, cannot create grid!')
            return False
        self._addGridPointsToLayer(points, localTransformer,
                                   localOrigin.x(), xInterval, (localTerminus.x() - localOrigin.x()) / xInterval,
                                   localOrigin.y(), yInterval, (localTerminus.y() - localOrigin.y()) / yInterval,
                                   self._attributes(points, siteCode, gridName), local_x, local_y, map_x, map_y)

        if self.project.linesLayerName('grid'):
            lines = self.project.grid.linesLayer
            if lines is None or not lines.isValid():
                self.project.plugin.showCriticalMessage('Invalid grid lines file!')
            else:
                self._addGridLinesToLayer(lines, localTransformer,
                                          localOrigin.x(), xInterval, (localTerminus.x() - localOrigin.x()) / xInterval,
                                          localOrigin.y(), yInterval, (localTerminus.y() - localOrigin.y()) / yInterval,
                                          self._attributes(lines, siteCode, gridName), local_x, local_y, map_x, map_y)

        if self.project.polygonsLayerName('grid'):
            polygons = self.project.grid.polygonsLayer
            if lines is None or not lines.isValid():
                self.project.plugin.showCriticalMessage('Invalid grid polygons file!')
            else:
                self._addGridPolygonsToLayer(polygons, localTransformer,
                                             localOrigin.x(), xInterval, (localTerminus.x() - localOrigin.x()) / xInterval,
                                             localOrigin.y(), yInterval, (localTerminus.y() - localOrigin.y()) / yInterval,
                                             self._attributes(polygons, siteCode, gridName), local_x, local_y, map_x, map_y)
        return True

    def _attributes(self, layer, site, name):
        attributes = {}
        attributes[layer.fieldNameIndex(self.project.fieldName('site'))] = site
        attributes[layer.fieldNameIndex(self.project.fieldName('name'))] = name
        attributes[layer.fieldNameIndex(self.project.fieldName('created_on'))] = utils.timestamp()
        attributes[layer.fieldNameIndex(self.project.fieldName('created_by'))] = 'Grid Tool'
        return attributes

    def _setAttributes(self, feature, attributes):
        self.project.plugin.logMessage(str(attributes))
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
                self.project.plugin.mapCanvas().setMapTool(self.mapTool)
            else:
                self.project.plugin.iface.mapCanvas().unsetMapTool(self.mapTool)
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
            dialog = UpdateLayerDialog(self.project.plugin.iface)
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

    def showTranslateFeaturesDialog(self):
        if not self.initialised:
            self.initialise()
        if self.initialised:
            dialog = TranslateFeaturesDialog(self.project.plugin.iface)
            if dialog.exec_():
                self.translateFeatures(dialog.layer(), dialog.translateEast(), dialog.translateNorth(), dialog.allFeatures())

    def translateFeatures(self, layer, xInterval, yInterval, allFeatures):
        localOriginPoint = QgsPoint(0, 0)
        localTranslatedPoint = QgsPoint(xInterval, yInterval)
        mapOriginPoint = self.localTransformer.map(localOriginPoint)
        mapTranslatedPoint = self.localTransformer.map(localTranslatedPoint)
        dx = mapTranslatedPoint.x() - mapOriginPoint.x()
        dy = mapTranslatedPoint.y() - mapOriginPoint.y()
        if layer.startEditing():
            featureIds = None
            if allFeatures:
                featureIds = layer.allFeatureIds()
            else:
                featureIds = layer.selectedFeaturesIds()
            for featureId in featureIds:
                layer.translateFeature(featureId, dx, dy)
            if layer.commitChanges():
                return self.updateLayerCoordinates(layer, False, False)
        return False

    def panMapToPoint(self):
        self.project.plugin.mapCanvas().zoomByFactor(1.0, self.mapPoint())

    def copyMapPointToClipboard(self):
        #TODO Use QgsClipboard when it becomes public
        QApplication.clipboard().setText(self.mapPointAsWkt())

    def copyLocalPointToClipboard(self):
        #TODO Use QgsClipboard when it becomes public
        QApplication.clipboard().setText(self.localPointAsWkt())

    def pasteMapPointFromClipboard(self):
        #TODO Use QgsClipboard when it becomes public
        text = QApplication.clipboard().text().strip().upper()
        idx = text.find('POINT(')
        if idx >= 0:
            idx_l = idx + 5
            idx_r = text.find(')', idx_l) + 1
            text = text[idx_l:idx_r]
        if (text[0] == '(' and text[len(text) - 1] == ')'):
            coords = text[1:len(text) - 2].split()
            point = QgsPoint(float(coords[0]), float(coords[1]))
            self.setMapPoint(point)

    def addMapPointToLayer(self):
        layer = self.project.plugin.mapCanvas().currentLayer()
        if (layer.geometryType() == QGis.Point and layer.isEditable()):
            layer.addFeature(self.mapPointAsFeature(layer.pendingFields()))
        self.project.plugin.mapCanvas().refresh()

    def setMapPoint(self, mapPoint):
        self.dock.setMapPoint(mapPoint)
        self.convertMapPoint()

    def setMapPointFromGeometry(self, geom):
        if (geom is not None and geom.type() == QGis.Point and geom.isGeosValid()):
            self.setMapPoint(geom.asPoint())

    def setMapPointFromWkt(self, wkt):
        self.setMapPointFromGeometry(QgsGeometry.fromWkt(wkt))

    def mapPoint(self):
        return self.dock.mapPoint()

    def mapPointAsGeometry(self):
        return QgsGeometry.fromPoint(self.mapPoint())

    def mapPointAsFeature(self, fields):
        feature = QgsFeature(fields)
        feature.setGeometry(self.mapPointAsGeometry())
        return feature

    def mapPointAsLayer(self):
        mem = QgsVectorLayer("point?crs=" + self.project.plugin.projectCrs().authid() + "&index=yes", 'point', 'memory')
        if (mem is not None and mem.isValid()):
            mem.dataProvider().addAttributes([QgsField('id', QVariant.String, '', 10, 0, 'ID')])
            feature = self.mapPointAsFeature(mem.dataProvider().fields())
            mem.dataProvider().addFeatures([feature])
        return mem

    def mapPointAsWkt(self):
        # Return the text so we don't have insignificant double values
        return 'POINT(' + self.dock.mapEastingSpin.text() + ' ' + self.dock.mapNorthingSpin.text() + ')'

    def setLocalPoint(self, localPoint):
        self.dock.setLocalPoint(mapPoint)
        self.convertLocalPoint()

    def setLocalPointFromGeometry(self, geom):
        if (geom is not None and geom.type() == QGis.Point and geom.isGeosValid()):
            self.setLocalPoint(geom.asPoint())

    def setLocalPointFromWkt(self, wkt):
        self.setLocalPointFromGeometry(QgsGeometry.fromWkt(wkt))

    def localPoint(self):
        return self.dock.localPoint()

    def localPointAsGeometry(self):
        return QgsGeometry.fromPoint(self.localPoint())

    def localPointAsWkt(self):
        # Return the text so we don't have insignificant double values
        return 'POINT(' + self.dock.localEastingSpin.text() + ' ' + self.dock.localNorthingSpin.text() + ')'
