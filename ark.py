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

import resources_rc

from .core.settings import Settings
from .core.layers import LayerManager

from .grid.grid import GridModule
from .plan.plan import Plan
from .filter.filter import Filter

class Ark:
    """QGIS Plugin Implementation."""

    # Common plugin objects
    settings = None # Settings()
    layers = None  # LayerManager()

    # Modules
    planDock = None  # Plan()
    filterDock = None  # Filter()

    def __init__(self, iface):
        self.settings = Settings(iface)
        self.layers = LayerManager(self.settings)
        self.gridDock = GridModule(self.settings, self.layers)
        self.planDock = Plan(self.settings, self.layers)
        self.filterDock = Filter(self.settings, self.layers)

    def initGui(self):
        self.settings.initGui()
        self.gridDock.initGui()
        self.planDock.initGui()
        self.filterDock.initGui()

    def unload(self):

        # Remove the layers from the legend
        self.layers.unload()

        # Unload the modules
        self.gridDock.unload()
        self.planDock.unload()
        self.filterDock.unload()

        # Removes the plugin menu item and icon from QGIS GUI.
        self.settings.unload()
