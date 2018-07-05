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

from qgis.PyQt.QtCore import pyqtSignal
from qgis.PyQt.QtGui import QIcon

from ArkSpatial.ark.lib import utils
from ArkSpatial.ark.lib.gui import ToolDockWidget

from .digitising_widget import DigitisingWidget


class DrawingDock(ToolDockWidget):

    # Toolbar Signals
    loadAnyFileSelected = pyqtSignal()
    loadRawFileSelected = pyqtSignal()
    loadGeoFileSelected = pyqtSignal()

    # Drawing Signals
    resetSelected = pyqtSignal()
    mergeSelected = pyqtSignal()

    def __init__(self, parent=None):
        super(DrawingDock, self).__init__(DigitisingWidget(), parent)

        self.setWindowTitle('ARK Drawing')
        self.setObjectName('DrawingDock')

    def initGui(self, iface, location, menuAction):
        super(DrawingDock, self).initGui(iface, location, menuAction)

        # Init the toolbar
        self.toolbar.addAction(iface.actionPan())
        self.toolbar.addAction(iface.actionZoomIn())
        self.toolbar.addAction(iface.actionZoomOut())
        self.toolbar.addAction(iface.actionZoomLast())
        self.toolbar.addAction(iface.actionZoomNext())

        self.toolbar.addSeparator()

        self.toolbar.addAction(
            QIcon(':/plugins/ark/plan/georef.png'), self.tr('Georeference Any Drawing'), self.loadAnyFileSelected)
        self.toolbar.addAction(
            QIcon(':/plugins/ark/grid/grid.png'), self.tr('Georeference Raw Drawings'), self.loadRawFileSelected)
        self.toolbar.addAction(QIcon(':/plugins/ark/plan/loadDrawings.svg'),
                               self.tr('Load Georeferenced Drawings'), self.loadGeoFileSelected)

        # Init the main widgets
        self.widget.initGui(iface)

        # Cascade the child widget signals
        self.widget.resetButton.clicked.connect(self.resetSelected)
        self.widget.mergeButton.clicked.connect(self.mergeSelected)

    def unloadGui(self):
        self.widget.unloadGui()
        super(DrawingDock, self).unloadGui()

    # Load the project settings when project is loaded
    def loadProject(self, plugin):
        self.widget.loadProject(plugin)

    # Save the project
    def writeProject(self):
        pass

    # Close the project
    def closeProject(self):
        self.widget.closeProject()

    # Drawing methods pass-through

    def source(self):
        return self.widget.source()

    def setSource(self, source):
        self.widget.setSource(source)
