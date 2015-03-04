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
        self.createGridAction = self.settings.createMenuAction(self.tr(u'Create Grid'), ':/plugins/Ark/grid/view-grid.png', False)
        self.createGridAction.triggered.connect(self.showCreateGridDialog)

        self.dock = GridDock()
        self.dock.load(self.settings, Qt.LeftDockWidgetArea, self.tr(u'Local Grid'), ':/plugins/Ark/grid/view-grid.png')
        self.dock.toggled.connect(self.run)
        self.dock.mapToolToggled.connect(self.enableMapTool)
        self.dock.convertCrsSelected.connect(self.convertCrs)
        self.dock.convertLocalSelected.connect(self.convertLocal)


    def unload(self):
        self.settings.iface.removeToolBarIcon(self.createGridAction)
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
        self.crsTransformer = LinearTransformer(self.crsLayer, False)

        self.localLayer = QgsVectorLayer(self.settings.gridPath() + '/grid_bender_local_to_osgb.shp', 'grid_bender_local_to_osgb', "ogr")
        self.localTransformer = LinearTransformer(self.localLayer, False)

        self.initialised = True


    # Grid methods

    def showCreateGridDialog(self):
        dialog = CreateGridDialog(self, self.settings.iface.mainWindow())
        return dialog.exec_()


    def enableMapTool(self, status):
        if status:
            self.settings.iface.mapCanvas().setMapTool(self.mapTool)
        elif (self.settings.iface.mapCanvas().mapTool() == self.mapTool):
            self.settings.iface.mapCanvas().setMapTool(None)

    def pointSelected(self, point, button):
        if (button == Qt.LeftButton):
            self.dock.setCrsPoint(point)
            self.convertCrs()

    def convertCrs(self):
        localPoint = self.crsTransformer.map(self.dock.crsPoint())
        self.dock.setLocalPoint(localPoint)


    def convertLocal(self):
        crsPoint = self.localTransformer.map(self.dock.localPoint())
        self.dock.setCrsPoint(crsPoint)
