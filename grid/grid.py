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

from vectorbender.vectorbendertransformers import *

from ..core.settings import Settings
from ..core.layers import LayerManager

from create_grid_dialog import CreateGridDialog
from grid_dock import GridDock

class GridModule(QObject):

    settings = None # Settings()
    layers = None  # LayerManager()

    # Internal variables
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

        self.initialised = True


    # Grid methods

    def showCreateGridDialog(self):
        dialog = CreateGridDialog(self, self.settings.iface.mainWindow())
        return dialog.exec_()


    def transformPoint(self):
        self.transformer = LinearTransformer(pairsLayer, False)
        # Uses QgsPoint
        newPoint = self.transformer.map(oldPoint)
