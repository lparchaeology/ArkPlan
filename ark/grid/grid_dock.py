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

from ArkSpatial.ark.lib.gui import ToolDockWidget

from .grid_widget import GridWidget


class GridDock(ToolDockWidget):

    def __init__(self, parent=None):
        super().__init__(GridWidget(), parent)

        self.setWindowTitle(self.tr('ARK Grid'))
        self.setObjectName('GridDock')

    def initGui(self, iface, location, menuAction):
        super().initGui(iface, location, menuAction)
        self.widget.initGui()

    # Load the project settings when project is loaded
    def loadProject(self, plugin):
        self.widget.loadProject(plugin)

    # Save the project
    def writeProject(self):
        pass

    # Close the project
    def closeProject(self):
        self.widget.closeProject()
