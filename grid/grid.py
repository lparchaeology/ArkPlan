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

from PyQt4.QtCore import Qt, QObject
from PyQt4.QtGui import QAction, QIcon, QFileDialog

from qgis.core import *
from qgis.gui import QgsMapToolEmitPoint

from ..core.settings import Settings
from ..core.layers import LayerManager

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

        self.dock = GridDock()
        self.dock.load(self.settings.iface, Qt.LeftDockWidgetArea, self.settings.createMenuAction(self.tr(u'Local Grid'), ':/plugins/Ark/grid/view-grid.png', True))
        self.dock.toggled.connect(self.run)
        self.dock.convertCrsSelected.connect(self.convertCrs)
        self.dock.convertLocalSelected.connect(self.convertLocal)


    # Unload the module when plugin is unloaded
    def unload(self):
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
            localOrigin = QgsPoint(dialog.localOriginEastingSpin.value(), dialog.localOriginNorthingSpin.value())
            localTerminus = QgsPoint(dialog.localTerminusEastingSpin.value(), dialog.localTerminusNorthingSpin.value())
            self.createGrid(crsOrigin, crsTerminus, localOrigin, localTerminus, dialog.localIntervalSpin.value()

    def createGrid(self, crsOrigin, crsTerminus, localOrigin, localTerminus, localInterval):
        localTransformer = LinearTransformer(localOrigin, crsOrigin, localTerminus, crsTerminus)
        fields = [QgsField(self.settings.gridPointsFieldX, QVariant.Int), QgsField((self.settings.gridPointsFieldY, QVariant.Int)]
        writer = QgsVectorFileWriter("my_shapes.shp", "CP1250", fields, QGis.WKBPoint, None, "ESRI Shapefile")
        if writer.hasError() != QgsVectorFileWriter.NoError:
            self.settings.showCriticalMessage('Create grid_pt failed!!!')
            return
        fet = QgsFeature()
        fet.setGeometry(QgsGeometry.fromPoint(QgsPoint(10,10)))
        fet.setAttribute(self.settings.gridPointsFieldX, x)
        fet.setAttribute(self.settings.gridPointsFieldY, y)
        writer.addFeature(fet)
        del writer

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
