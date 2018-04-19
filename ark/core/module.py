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

from PyQt4.QtCore import QObject


class Module(QObject):

    def __init__(self, plugin):
        super(Module, self).__init__(plugin)

        # Internal variables
        self._plugin = plugin  # Plugin()
        self._dock = None  # ToolDockWidget()
        self._initialised = False

    # Standard Dock methods

    # Create the gui when the plugin is first created
    def initGui(self):
        pass

    def _initDockGui(self, dock, location, menuAction):
        self._dock = dock
        self._dock.initGui(self._plugin.iface, location, menuAction)

    # Unload the gui when the plugin is unloaded
    def unloadGui(self):
        # Unload the dock
        self._dock.unloadGui()
        del self._dock
        # Reset the initialisation
        self._initialised = False

    # Load the project settings when project is loaded
    def loadProject(self):
        self._dock.loadProject(self._plugin)
        self._initialised = True

    # Save the project
    def writeProject(self):
        self._dock.writeProject()

    # Close the project
    def closeProject(self):
        self._dock.closeProject()
        # Reset the initialisation
        self._initialised = False

    def run(self, checked):
        if checked and self._initialised:
            pass
        else:
            self.showDock(False)

    def showDock(self, show=True):
        self._dock.menuAction().setChecked(show)
