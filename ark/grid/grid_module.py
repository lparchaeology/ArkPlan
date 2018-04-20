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

from PyQt4.QtCore import QObject, Qt, QVariant
from PyQt4.QtGui import QApplication, QIcon

from qgis.core import (QGis, QgsFeature, QgsField, QgsGeometry, QgsLineStringV2, QgsPoint, QgsPointV2, QgsPolygonV2,
                       QgsVectorLayer)
from qgis.gui import QgsVertexMarker

from ArkSpatial.ark.lib import utils
from ArkSpatial.ark.lib.core import LinearTransformer, geometry, layers
from ArkSpatial.ark.lib.map import MapToolEmitPoint

# Move to lib???
from ArkSpatial.ark.core import Module

from .grid_dock import GridDock
from .grid_wizard import GridWizard
from .translate_features_dialog import TranslateFeaturesDialog
from .update_layer_dialog import UpdateLayerDialog


class GridModule(Module):

    def __init__(self, plugin):
        super(GridModule, self).__init__(plugin)

        # Internal variables
        self.mapTool = None  # MapToolEmitPoint()
        self.gridWizard = None  # QWizard
        self._vertexMarker = None  # QgsVertexMarker
        self.mapTransformer = None  # LinearTransformer()
        self.localTransformer = None  # LinearTransformer()

    # Standard Dock methods

    # Load the module when plugin is loaded
    def initGui(self):
        dock = GridDock(self._plugin.iface.mainWindow())
        action = self._plugin.project().addDockAction(
            ':/plugins/ark/grid/grid.png', self.tr(u'Grid Tools'), callback=self.run, checkable=True)
        self._initDockGui(dock, Qt.LeftDockWidgetArea, action)

        self._createGridAction = self._dock.toolbar.addAction(
            QIcon(':/plugins/ark/grid/newGrid.png'), self.tr(u'Create New Grid'), self.showGridWizard)
        self._identifyGridAction = self._dock.toolbar.addAction(
            QIcon(':/plugins/ark/grid/identifyCoordinates.png'), self.tr(u'Identify Grid Coordinates'), self._triggerMapTool)
        self._identifyGridAction.setCheckable(True)
        self._panToAction = self._dock.toolbar.addAction(
            QIcon(':/plugins/ark/grid/panToSelected.svg'), self.tr(u'Pan to map point'), self.panMapToPoint)
        self._pasteMapPointAction = self._dock.toolbar.addAction(
            QIcon(':/plugins/ark/grid/pastePoint.png'), self.tr(u'Paste Map Point'), self.pasteMapPointFromClipboard)
        self._addMapPointAction = self._dock.toolbar.addAction(
            QIcon(':/plugins/ark/grid/addPoint.png'), self.tr(u'Add point to current layer'), self.addMapPointToLayer)
        self._updateLayerAction = self._dock.toolbar.addAction(
            QIcon(':/plugins/ark/grid/updateLayer.png'), self.tr(u'Update Layer Coordinates'), self.showUpdateLayerDialog)
        self._translateFeaturesAction = self._dock.toolbar.addAction(
            QIcon(':/plugins/ark/grid/translateFeature.png'), self.tr(u'Translate features'), self.showTranslateFeaturesDialog)

        self._dock.widget.gridSelectionChanged.connect(self.changeGrid)
        self._dock.widget.mapPointChanged.connect(self.convertMapPoint)
        self._dock.widget.copyMapPointSelected.connect(self.copyMapPointToClipboard)
        self._dock.widget.localPointChanged.connect(self.convertLocalPoint)
        self._dock.widget.copyLocalPointSelected.connect(self.copyLocalPointToClipboard)

        self._setReadOnly(True)
        self._createGridAction.setEnabled(False)

        self.mapTool = MapToolEmitPoint(self._plugin.mapCanvas())
        self.mapTool.setAction(self._identifyGridAction)
        self.mapTool.canvasClicked.connect(self.pointSelected)

        self._vertexMarker = QgsVertexMarker(self._plugin.mapCanvas())
        self._vertexMarker.setIconType(QgsVertexMarker.ICON_CROSS)

    def loadProject(self):
        self._createGridAction.setEnabled(True)

        # Check if files exist or need creating
        # Run create if needed

        if not self.collection().hasLayer('points'):
            return

        if self.loadGridNames():
            self._setReadOnly(False)
            self._initialised = True
            return True
        return False

    # Close the project
    def closeProject(self):
        self._vertexMarker.setCenter(QgsPoint())
        self.collection().clearFilter()
        self._initialised = False

    # Unload the module when plugin is unloaded
    def unloadGui(self):
        # Reset the initialisation
        del self._vertexMarker
        self._vertexMarker = None
        self._initialised = False
        self._dock.unloadGui()

    def _setReadOnly(self, readOnly):
        enabled = not readOnly
        self._identifyGridAction.setEnabled(enabled)
        self._updateLayerAction.setEnabled(enabled)
        self._translateFeaturesAction.setEnabled(enabled)
        self._panToAction.setEnabled(enabled)
        self._pasteMapPointAction.setEnabled(enabled)
        self._addMapPointAction.setEnabled(enabled)
        self._dock.widget.setEnabled(enabled)

    def run(self, checked):
        if checked:
            if not self._initialised:
                self.loadProject()
            self._vertexMarker.setCenter(geometry.toPoint(self.mapPoint()))
        else:
            self._vertexMarker.setCenter(QgsPoint())

    def collection(self):
        return self._plugin.project().collection('grid')

    def loadGridNames(self):
        self.collection().clearFilter()
        names = set()
        default = None
        for feature in self.collection().layer('points').getFeatures():
            name = (feature.attribute('site'),
                    feature.attribute('id'))
            names.add(name)
            if not default:
                default = name
        if default:
            self.setGridNames(sorted(names))
            self.setGrid(default[0], default[1])
            return True
        return False

    def initialiseGrid(self, siteCode, gridName):
        prevFilter = self.collection().filter
        expr = utils.eqClause('site', siteCode) + ' and ' + utils.eqClause('id', gridName)
        self.collection().applyFilter(expr)
        if self.collection().layer('points').featureCount() < 2:
            self.collection().applyFilter(prevFilter)
            return False
        features = []
        for feature in self.collection().layer('points').getFeatures():
            features.append(feature)
            if len(features) >= 2:
                break
        map1, local1 = self.transformPoints(features[0])
        map2, local2 = self.transformPoints(features[1])
        self.mapTransformer = LinearTransformer(map1, local1, map2, local2)
        self.localTransformer = LinearTransformer(local1, map1, local2, map2)
        return True

    def changeGrid(self, siteCode, gridName):
        self.initialiseGrid(siteCode, gridName)
        self.convertMapPoint()

    def transformPoints(self, feature):
        mapPoint = feature.geometry().geometry()
        localX = feature.attribute('local_x')
        localY = feature.attribute('local_y')
        localPoint = QgsPointV2(localX, localY)
        return mapPoint, localPoint

    # Widget settings methods

    def siteCode(self):
        return self._dock.widget.siteCode()

    def gridName(self):
        return self._dock.widget.gridName()

    def setGrid(self, siteCode, gridName):
        self._dock.widget.setGrid(siteCode, gridName)

    def setGridNames(self, names):
        self._dock.widget.setGridNames(names)

    def mapPoint(self):
        return self._dock.widget.mapPoint()

    def setMapPoint(self, point):
        self._dock.widget.setMapPoint(point)
        self._vertexMarker.setCenter(self.mapPoint())

    def localPoint(self):
        return self._dock.widget.localPoint()

    def setLocalPoint(self, point):
        self._dock.widget.setLocalPoint(point)

    # Grid methods

    def showGridWizard(self):
        if self.gridWizard is None:
            self.gridWizard = GridWizard(self._plugin.iface, self._plugin, self._plugin.iface.mainWindow())
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
            if self.gridWizard.methodType() == GridWizard.PointOnYAxis:
                if axisGeometry.length() < yInterval:
                    self._plugin.showCriticalMessage(
                        'Cannot create grid: Input axis must be longer than local interval')
                    return False
                mp2 = axisGeometry.interpolate(yInterval).geometry()
                lp2 = QgsPointV2(lp1.x(), lp1.y() + yInterval)
            else:
                if axisGeometry.length() < xInterval:
                    self._plugin.showCriticalMessage(
                        'Cannot create grid: Input axis must be longer than local interval')
                    return False
                mp2 = axisGeometry.interpolate(xInterval).geometry()
                lp2 = QgsPointV2(lp1.x() + xInterval, lp1.y())
        if self.createGrid(self.gridWizard.siteCode(), self.gridWizard.gridName(),
                           mp1, lp1, mp2, lp2,
                           self.gridWizard.localOriginPoint(), self.gridWizard.localTerminusPoint(),
                           xInterval, yInterval):
            self._plugin.mapCanvas().refresh()
            self.loadGridNames()
            self.setGrid(self.gridWizard.siteCode(), self.gridWizard.gridName())
            self._setReadOnly(False)
            self._plugin.showInfoMessage('Grid successfully created', 10)

    def createGrid(self, siteCode, gridName, mapPoint1, localPoint1, mapPoint2, localPoint2, localOrigin, localTerminus, xInterval, yInterval):
        localTransformer = LinearTransformer(localPoint1, mapPoint1, localPoint2, mapPoint2)
        local_x = 'local_x'
        local_y = 'local_y'
        map_x = 'map_x'
        map_y = 'map_y'

        points = self.collection().layer('points')
        if (points is None or not points.isValid()):
            self._plugin.showCriticalMessage('Invalid grid points file, cannot create grid!')
            return False
        self._addGridPointsToLayer(points, localTransformer,
                                   localOrigin.x(), xInterval, (localTerminus.x() - localOrigin.x()) / xInterval,
                                   localOrigin.y(), yInterval, (localTerminus.y() - localOrigin.y()) / yInterval,
                                   self._attributes(points, siteCode, gridName), local_x, local_y, map_x, map_y)

        if self.collection().hasLayer('lines'):
            lines = self.collection().layer('lines')
            if lines is None or not lines.isValid():
                self._plugin.showCriticalMessage('Invalid grid lines file!')
            else:
                self._addGridLinesToLayer(lines, localTransformer,
                                          localOrigin.x(), xInterval, (localTerminus.x() - localOrigin.x()) / xInterval,
                                          localOrigin.y(), yInterval, (localTerminus.y() - localOrigin.y()) / yInterval,
                                          self._attributes(lines, siteCode, gridName), local_x, local_y, map_x, map_y)

        if self.collection().hasLayer('polygons'):
            polygons = self.collection().layer('polygons')
            if lines is None or not lines.isValid():
                self._plugin.showCriticalMessage('Invalid grid polygons file!')
            else:
                self._addGridPolygonsToLayer(polygons, localTransformer,
                                             localOrigin.x(), xInterval, (localTerminus.x() - localOrigin.x()) /
                                             xInterval,
                                             localOrigin.y(), yInterval, (localTerminus.y() - localOrigin.y()) /
                                             yInterval,
                                             self._attributes(polygons, siteCode, gridName), local_x, local_y, map_x, map_y)
        return True

    def _attributes(self, layer, site, name):
        attributes = {}
        attributes[layer.fieldNameIndex('site')] = site
        attributes[layer.fieldNameIndex('id')] = name
        attributes[layer.fieldNameIndex('created')] = utils.timestamp()
        attributes[layer.fieldNameIndex('creator')] = 'ARK Grid Tool'
        return attributes

    def _setAttributes(self, feature, attributes):
        utils.debug(attributes)
        for key in attributes:
            feature.setAttribute(key, attributes[key])

    def _addGridPointsToLayer(self, layer, transformer, originX, intervalX, repeatX, originY, intervalY, repeatY, attributes, localFieldX='local_x', localFieldY='local_x', mapFieldX='map_x', mapFieldY='map_y'):
        if (layer is None or not layer.isValid() or layer.geometryType() != QGis.Point):
            return
        features = []
        for localX in range(originX, originX + (intervalX * repeatX) + 1, intervalX):
            for localY in range(originY, originY + (intervalY * repeatY) + 1, intervalY):
                localPoint = QgsPointV2(localX, localY)
                mapPoint = transformer.map(localPoint)
                feature = QgsFeature(layer.dataProvider().fields())
                feature.setGeometry(QgsGeometry(mapPoint))
                self._setAttributes(feature, attributes)
                feature.setAttribute(localFieldX, localX)
                feature.setAttribute(localFieldY, localY)
                feature.setAttribute(mapFieldX, mapPoint.x())
                feature.setAttribute(mapFieldY, mapPoint.y())
                features.append(feature)
        layers.addFeatures(features, layer)

    def _addGridLinesToLayer(self, layer, transformer, originX, intervalX, repeatX, originY, intervalY, repeatY, attributes, localFieldX='local_x', localFieldY='local_x', mapFieldX='map_x', mapFieldY='map_y'):
        if (layer is None or not layer.isValid() or layer.geometryType() != QGis.Line):
            return
        features = []
        terminusX = originX + (intervalX * repeatX)
        terminusY = originY + (intervalY * repeatY)
        for localX in range(originX, originX + (intervalX * repeatX) + 1, intervalX):
            localStartPoint = QgsPointV2(localX, originY)
            localEndPoint = QgsPointV2(localX, terminusY)
            mapStartPoint = transformer.map(localStartPoint)
            mapEndPoint = transformer.map(localEndPoint)
            feature = QgsFeature(layer.dataProvider().fields())
            lineGeometry = QgsLineStringV2()
            lineGeometry.setPoints([mapStartPoint, mapEndPoint])
            feature.setGeometry(QgsGeometry(lineGeometry))
            self._setAttributes(feature, attributes)
            feature.setAttribute(localFieldX, localX)
            feature.setAttribute(mapFieldX, mapStartPoint.x())
            features.append(feature)
        for localY in range(originY, originY + (intervalY * repeatY) + 1, intervalY):
            localStartPoint = QgsPointV2(originX, localY)
            localEndPoint = QgsPointV2(terminusX, localY)
            mapStartPoint = transformer.map(localStartPoint)
            mapEndPoint = transformer.map(localEndPoint)
            feature = QgsFeature(layer.dataProvider().fields())
            lineGeometry = QgsLineStringV2()
            lineGeometry.setPoints([mapStartPoint, mapEndPoint])
            feature.setGeometry(QgsGeometry(lineGeometry))
            self._setAttributes(feature, attributes)
            feature.setAttribute(localFieldY, localY)
            feature.setAttribute(mapFieldY, mapStartPoint.y())
            features.append(feature)
        layers.addFeatures(features, layer)

    def _addGridPolygonsToLayer(self, layer, transformer, originX, intervalX, repeatX, originY, intervalY, repeatY, attributes, localFieldX='local_x', localFieldY='local_x', mapFieldX='map_x', mapFieldY='map_y'):
        if (layer is None or not layer.isValid() or layer.geometryType() != QGis.Polygon):
            return
        features = []
        for localX in range(originX, originX + intervalX * repeatX, intervalX):
            for localY in range(originY, originY + intervalY * repeatY, intervalY):
                localPoint = QgsPointV2(localX, localY)
                mapPoint = transformer.map(localPoint)
                points = []
                points.append(transformer.map(localPoint))
                points.append(transformer.map(QgsPointV2(localX, localY + intervalY)))
                points.append(transformer.map(QgsPointV2(localX + intervalX, localY + intervalY)))
                points.append(transformer.map(QgsPointV2(localX + intervalX, localY)))
                feature = QgsFeature(layer.dataProvider().fields())
                lineGeometry = QgsLineStringV2()
                lineGeometry.setPoints(points)
                polygonGeometry = QgsPolygonV2()
                polygonGeometry.setExteriorRing(lineGeometry)
                feature.setGeometry(QgsGeometry(polygonGeometry))
                self._setAttributes(feature, attributes)
                feature.setAttribute(localFieldX, localX)
                feature.setAttribute(localFieldY, localY)
                feature.setAttribute(mapFieldX, mapPoint.x())
                feature.setAttribute(mapFieldY, mapPoint.y())
                features.append(feature)
        layers.addFeatures(features, layer)

    def _triggerMapTool(self):
        if not self._initialised:
            self.initialise()
        if self._initialised:
            if self._identifyGridAction.isChecked():
                self._plugin.mapCanvas().setMapTool(self.mapTool)
            else:
                self._plugin.mapCanvas().unsetMapTool(self.mapTool)
        elif self._identifyGridAction.isChecked():
            self._identifyGridAction.setChecked(False)

    def pointSelected(self, point, button):
        if not self._initialised:
            return
        if (button == Qt.LeftButton):
            if not self._dock.menuAction().isChecked():
                self._dock.menuAction().toggle()
            self.setMapPoint(point)
            self.convertMapPoint()

    def convertMapPoint(self):
        if not self._initialised:
            return
        localPoint = self.mapTransformer.map(self.mapPoint())
        self.setLocalPoint(localPoint)

    def convertLocalPoint(self):
        if not self._initialised:
            return
        mapPoint = self.localTransformer.map(self.localPoint())
        self.setMapPoint(mapPoint)

    def showUpdateLayerDialog(self):
        if not self._initialised:
            self.initialise()
        if self._initialised:
            dialog = UpdateLayerDialog(self._plugin.iface)
            if dialog.exec_():
                self.updateLayerCoordinates(dialog.layer(), dialog.updateGeometry(), dialog.createMapFields())

    def updateLayerCoordinates(self, layer, updateGeometry, createMapFields):
        if (not self._initialised or layer is None or not layer.isValid() or layer.geometryType() != QGis.Point):
            return False
        local_x = 'local_x'
        local_y = 'local_y'
        map_x = 'map_x'
        map_y = 'map_y'
        if layer.startEditing():
            if layer.fieldNameIndex(local_x) < 0:
                layer.dataProvider().addAttributes([self._plugin.field('local_x')])
            if layer.fieldNameIndex(local_y) < 0:
                layer.dataProvider().addAttributes([self._plugin.field('local_y')])
            if (createMapFields and layer.fieldNameIndex(map_x) < 0):
                layer.dataProvider().addAttributes([self._plugin.field('map_x')])
            if (createMapFields and layer.fieldNameIndex(map_y) < 0):
                layer.dataProvider().addAttributes([self._plugin.field('map_y')])
            local_x_idx = layer.fieldNameIndex(local_x)
            local_y_idx = layer.fieldNameIndex(local_y)
            map_x_idx = layer.fieldNameIndex(map_x)
            map_y_idx = layer.fieldNameIndex(map_y)
            if updateGeometry:
                for feature in layer.getFeatures():
                    localPoint = QgsPointV2(feature.attribute(local_x), feature.attribute(local_y))
                    mapPoint = self.localTransformer.map(localPoint)
                    layer.changeGeometry(feature.id(), QgsGeometry(mapPoint))
            for feature in layer.getFeatures():
                mapPoint = feature.geometry().geometry()
                localPoint = self.mapTransformer.map(mapPoint)
                layer.changeAttributeValue(feature.id(), local_x_idx, localPoint.x())
                layer.changeAttributeValue(feature.id(), local_y_idx, localPoint.y())
                layer.changeAttributeValue(feature.id(), map_x_idx, mapPoint.x())
                layer.changeAttributeValue(feature.id(), map_y_idx, mapPoint.y())
            return layer.commitChanges()
        return False

    def showTranslateFeaturesDialog(self):
        if not self._initialised:
            self.initialise()
        if self._initialised:
            dialog = TranslateFeaturesDialog(self._plugin.iface)
            if dialog.exec_():
                self.translateFeatures(
                    dialog.layer(), dialog.translateEast(), dialog.translateNorth(), dialog.allFeatures())

    def translateFeatures(self, layer, xInterval, yInterval, allFeatures):
        localOriginPoint = QgsPointV2(0, 0)
        localTranslatedPoint = QgsPointV2(xInterval, yInterval)
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
        self._plugin.mapCanvas().zoomByFactor(1.0, self.mapPoint())

    def copyMapPointToClipboard(self):
        # TODO Use QgsClipboard when it becomes public
        QApplication.clipboard().setText(self.mapPointAsWkt())

    def copyLocalPointToClipboard(self):
        # TODO Use QgsClipboard when it becomes public
        QApplication.clipboard().setText(self.localPointAsWkt())

    def pasteMapPointFromClipboard(self):
        # TODO Use QgsClipboard when it becomes public
        text = QApplication.clipboard().text().strip().upper()
        idx = text.find('POINT(')
        if idx >= 0:
            idx_l = idx + 5
            idx_r = text.find(')', idx_l) + 1
            text = text[idx_l:idx_r]
        if (text[0] == '(' and text[len(text) - 1] == ')'):
            coords = text[1:len(text) - 2].split()
            point = QgsPointV2(float(coords[0]), float(coords[1]))
            self.setMapPoint(point)

    def addMapPointToLayer(self):
        layer = self._plugin.mapCanvas().currentLayer()
        if (layer.geometryType() == QGis.Point and layer.isEditable()):
            layer.addFeature(self.mapPointAsFeature(layer.pendingFields()))
        self._plugin.mapCanvas().refresh()

    def setMapPointFromGeometry(self, geom):
        if (geom is not None and geom.type() == QGis.Point and geom.isGeosValid()):
            self.setMapPoint(geom.geometry())

    def setMapPointFromWkt(self, wkt):
        self.setMapPointFromGeometry(QgsGeometry.fromWkt(wkt))

    def mapPointAsGeometry(self):
        return QgsGeometry(self.mapPoint())

    def mapPointAsFeature(self, fields):
        feature = QgsFeature(fields)
        feature.setGeometry(self.mapPointAsGeometry())
        return feature

    def mapPointAsLayer(self):
        mem = QgsVectorLayer("point?crs=" + self._plugin.projectCrs().authid() + "&index=yes", 'point', 'memory')
        if (mem is not None and mem.isValid()):
            mem.dataProvider().addAttributes([QgsField('id', QVariant.String, '', 10, 0, 'ID')])
            feature = self.mapPointAsFeature(mem.dataProvider().fields())
            mem.dataProvider().addFeatures([feature])
        return mem

    def mapPointAsWkt(self):
        # Return the text so we don't have insignificant double values
        return 'POINT(' + self._dock.widget.mapEastingSpin.text() + ' ' + self._dock.widget.mapNorthingSpin.text() + ')'

    def setLocalPointFromGeometry(self, geom):
        if (geom is not None and geom.type() == QGis.Point and geom.isGeosValid()):
            self.setLocalPoint(geom.geometry())

    def setLocalPointFromWkt(self, wkt):
        self.setLocalPointFromGeometry(QgsGeometry.fromWkt(wkt))

    def localPointAsGeometry(self):
        return QgsGeometry(self.localPoint())

    def localPointAsWkt(self):
        # Return the text so we don't have insignificant double values
        return 'POINT(' + self._dock.widget.localEastingSpin.text() + ' ' + self._dock.widget.localNorthingSpin.text() + ')'
