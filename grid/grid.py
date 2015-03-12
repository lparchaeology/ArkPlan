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

from PyQt4.QtCore import Qt, QObject
from PyQt4.QtGui import QAction, QIcon, QFileDialog

from qgis.core import *
from qgis.gui import QgsMapToolEmitPoint

from VectorBender.vectorbendertransformers import LinearTransformer

from ..core.settings import Settings
from ..core.layers import LayerManager

from create_grid_dialog import CreateGridDialog
from grid_dock import GridDock

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

    def initGui(self):
        self.createGridAction = self.settings.createMenuAction(self.tr(u'Create New Grid'), ':/plugins/Ark/grid/get-hot-new-stuff.png', False)
        self.createGridAction.triggered.connect(self.showCreateGridDialog)

        self.identifyGridAction = self.settings.createMenuAction(self.tr(u'Identify Grid Coordinates'), ':/plugins/Ark/grid/snap-orthogonal.png', True)
        self.identifyGridAction.toggled.connect(self.enableMapTool)

        self.dock = GridDock()
        self.dock.load(self.settings, Qt.LeftDockWidgetArea, self.tr(u'Local Grid'), ':/plugins/Ark/grid/view-grid.png')
        self.dock.toggled.connect(self.run)
        self.dock.mapGridTool.setDefaultAction(self.identifyGridAction)
        self.dock.newGridTool.setDefaultAction(self.createGridAction)
        self.dock.convertCrsSelected.connect(self.convertCrs)
        self.dock.convertLocalSelected.connect(self.convertLocal)


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
        self.layers.initialise()

        self.mapTool = QgsMapToolEmitPoint(self.settings.iface.mapCanvas())
        self.mapTool.canvasClicked.connect(self.pointSelected)

        self.crsLayer = QgsVectorLayer(self.settings.gridPath() + '/grid_bender_osgb_to_local.shp', 'grid_bender_osgb_to_local', "ogr")
        if (self.crsLayer is None or not self.crsLayer.isValid()):
            self.settings.showMessage('Unable to load grid bender conversion file!')
            return
        self.crsTransformer = LinearTransformer(self.crsLayer, False)

        self.localLayer = QgsVectorLayer(self.settings.gridPath() + '/grid_bender_local_to_osgb.shp', 'grid_bender_local_to_osgb', "ogr")
        if (self.localLayer is None or not self.localLayer.isValid()):
            self.settings.showMessage('Unable to load grid bender conversion file!')
            return
        self.localTransformer = LinearTransformer(self.localLayer, False)

        self.dock.setReadOnly(False)

        self.initialised = True


    # Grid methods

    def showCreateGridDialog(self):
        dialog = CreateGridDialog(self, self.settings.iface.mainWindow())
        return dialog.exec_()


    def enableMapTool(self, status):
        if status:
            self.settings.iface.mapCanvas().setMapTool(self.mapTool)
        else:
            self.settings.iface.mapCanvas().unsetMapTool(self.mapTool)
        self.dock.setReadOnly(status)


    def pointSelected(self, point, button):
        if (button == Qt.LeftButton):
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
