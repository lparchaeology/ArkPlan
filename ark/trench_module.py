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

from PyQt4.QtCore import QObject, Qt

from ArkSpatial.ark.gui import TrenchDock


class TrenchModule(QObject):

    def __init__(self, plugin):
        super(TrenchModule, self).__init__(plugin)

        self._plugin = plugin  # Plugin()

        # Internal variables
        self.dock = None  # FilterDock()
        self._initialised = False

    # Standard Dock methods

    # Create the gui when the plugin is first created
    def initGui(self):
        self.dock = TrenchDock(self._plugin.iface.mainWindow())
        action = self._plugin.project().addDockAction(
            ':/plugins/ark/filter/filter.png',
            self.tr(u'Trench Tools'),
            callback=self.run,
            checkable=True
        )
        self.dock.initGui(self._plugin.iface, Qt.RightDockWidgetArea, action)

    # Load the project settings when project is loaded
    def loadProject(self):
        return self._initialised

    # Save the project
    def writeProject(self):
        pass

    # Close the project
    def closeProject(self):
        # Reset the initialisation
        self._initialised = False

    # Unload the gui when the plugin is unloaded
    def unloadGui(self):
        self.dock.unloadGui()

    def run(self, checked):
        if checked and not self._initialised:
            self.dock.menuAction().setChecked(False)

    def showDock(self, show=True):
        self.dock.menuAction().setChecked(show)
