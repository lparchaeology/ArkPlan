# -*- coding: utf-8 -*-
"""
/***************************************************************************
                                ARKspatial
                    A QGIS plugin for Archaeological Recording.
        Part of the Archaeological Recording Kit by L - P : Archaeology
                        http://ark.lparchaeology.com
                              -------------------
        copyright            : 2018 by L - P : Heritage LLP
        email                : ark@lparchaeology.com
        copyright            : 2018 by John Layt
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

from .project_browser_widget import ProjectBrowserWidget


class ProjectDock(ToolDockWidget):

    def __init__(self, parent=None):
        super().__init__(ProjectBrowserWidget(), parent)

        self.setWindowTitle('ARK Project Browser')
        self.setObjectName('ProjectDock')

    # Load the project settings when project is loaded
    def loadProject(self, plugin):
        self.widget.loadProject(plugin)

    # Save the project
    def writeProject(self):
        pass

    # Close the project
    def closeProject(self):
        self.widget.closeProject()
