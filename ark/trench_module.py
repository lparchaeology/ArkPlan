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

from qgis.PyQt.QtCore import QObject, Qt

from ArkSpatial.ark.core import Module
from ArkSpatial.ark.gui import TrenchDock


class TrenchModule(Module):

    def __init__(self, plugin):
        super().__init__(plugin)

    # Create the gui when the plugin is first created
    def initGui(self):
        dock = TrenchDock(self._plugin.iface.mainWindow())
        action = self._plugin.project().addDockAction(
            ':/plugins/ark/trench/trench.svg',
            self.tr('Trench Tools'),
            callback=self.run,
            checkable=True
        )
        self._initDockGui(dock, Qt.LeftDockWidgetArea, action)
