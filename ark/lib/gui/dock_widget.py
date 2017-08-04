# -*- coding: utf-8 -*-
"""
/***************************************************************************
                                ARK QGIS
                        A QGIS utilities library.
        Part of the Archaeological Recording Kit by L-P : Archaeology
                        http://ark.lparchaeology.com
                              -------------------
        copyright            : 2017 by L-P : Heritage LLP
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

from PyQt4.QtGui import QDockWidget

class DockWidget(QDockWidget):

    _iface = None  # QgisInterface
    _dockLocation = None  # Qt.DockWidgetArea
    _action = None  # QAction

    def __init__(self, parent=None):
        super(ArkDockWidget, self).__init__(parent)
        # HACK Work around a crash when dragging!
        self.setFeatures(QDockWidget.DockWidgetClosable)

    def initGui(self, iface, location, menuAction):
        self._iface = iface
        self._dockLocation = location
        self._action = menuAction

        self._action.toggled.connect(self._toggle)
        self.visibilityChanged.connect(self._action.setChecked)
        self.dockLocationChanged.connect(self._updateDockLocation)

    def unloadGui(self):
        self._iface.removeDockWidget(self)

    def menuAction(self):
        return self._action

    def dockLocation(self):
        return self._dockLocation

    def _updateDockLocation(self, location):
        self._dockLocation = location

    def _toggle(self, checked):
        if checked:
            self._iface.addDockWidget(self._dockLocation, self)
        else:
            self._iface.removeDockWidget(self)
