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

from .grid.grid import GridModule
from .plan.plan import Plan
from .filter.filter import Filter

class Ark:
    """QGIS Plugin Implementation."""

    # Common plugin objects
    project = None # Project()

    # Modules
    gridModule = None  # Grid()
    planModule = None  # Plan()
    filterModule = None  # Filter()

    def __init__(self, iface):
        self.project = Project(iface, os.path.dirname(__file__))
        self.gridModule = GridModule(self.project)
        self.planModule = Plan(self.project)
        self.filterModule = Filter(self.project)

    # Load the plugin
    def initGui(self):
        self.project.load()
        self.gridModule.load()
        self.planModule.load()
        self.filterModule.load()

    # Unload the plugin
    def unload(self):

        # Unload the modules
        self.gridModule.unload()
        self.planModule.unload()
        self.filterModule.unload()

        # Removes the plugin menu item and icon from QGIS GUI.
        self.project.unload()
