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

from .core.project import Project
from .core.layers import LayerManager

from .grid.grid import GridModule
from .plan.plan import Plan
from .filter.filter import Filter

class Ark:
    """QGIS Plugin Implementation."""

    # Common plugin objects
    project = None # Project()
    layers = None  # LayerManager()

    # Modules
    gridModule = None  # Plan()
    planModule = None  # Plan()
    filterModule = None  # Filter()

    def __init__(self, iface):
        self.project = Project(iface, os.path.dirname(__file__))
        self.layers = LayerManager(self.project)
        self.gridModule = GridModule(self.project, self.layers)
        self.planModule = Plan(self.project, self.layers)
        self.filterModule = Filter(self.project, self.layers)

    # Load the plugin
    def initGui(self):
        self.project.load()
        self.gridModule.load()
        self.planModule.load()
        self.filterModule.load()

    # Unload the plugin
    def unload(self):

        # Remove the layers from the legend
        self.layers.unload()

        # Unload the modules
        self.gridModule.unload()
        self.planModule.unload()
        self.filterModule.unload()

        # Removes the plugin menu item and icon from QGIS GUI.
        self.project.unload()

