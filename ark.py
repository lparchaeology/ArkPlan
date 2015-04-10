# -*- coding: utf-8 -*-
"""
/***************************************************************************
 Ark
                                 A QGIS plugin
 Plugin to assist in digitising of Archaeological plans.
                              -------------------
        begin                : 2014-12-07
        git sha              : $Format:%H$
        copyright            : (C) 2014 by John Layt
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

import os.path

import resources_rc

from .core.settings import Settings
from .core.layers import LayerManager

from .grid.grid import GridModule
from .plan.plan import Plan
from .filter.filter import Filter

class Ark:
    """QGIS Plugin Implementation."""

    # Common plugin objects
    iface = None  # QgisInterface()
    settings = None # Settings()
    layers = None  # LayerManager()

    # Modules
    gridModule = None  # Plan()
    planModule = None  # Plan()
    filterModule = None  # Filter()

    def __init__(self, iface):
        self.iface = iface
        self.iface.initializationCompleted.connect(self.projectLoad)
        self.iface.projectRead.connect(self.projectLoad)
        self.iface.newProjectCreated.connect(self.projectLoad)

        self.settings = Settings(iface, os.path.dirname(__file__))
        self.layers = LayerManager(self.settings)
        self.gridModule = GridModule(self.settings, self.layers)
        self.planModule = Plan(self.settings, self.layers)
        self.filterModule = Filter(self.settings, self.layers)

    def initGui(self):
        self.settings.load()
        self.gridModule.load()
        self.planModule.load()
        self.filterModule.load()

    def unload(self):

        # Remove the layers from the legend
        self.layers.unload()

        # Unload the modules
        self.gridModule.unload()
        self.planModule.unload()
        self.filterModule.unload()

        # Removes the plugin menu item and icon from QGIS GUI.
        self.settings.unload()
