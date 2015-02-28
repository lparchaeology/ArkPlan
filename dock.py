# -*- coding: utf-8 -*-
"""
/***************************************************************************
 ArkPlanDialog
                                 A QGIS plugin
 Plugin to assist in digitising of Archaeological plans.
                             -------------------
        begin                : 2015-02-28
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

import os
from PyQt4 import uic
from PyQt4.QtCore import Qt, pyqtSignal
from PyQt4.QtGui import QDockWidget, QAction, QIcon

class QgsDockWidget(QDockWidget):

    toggled = pyqtSignal(bool)

    _iface = None  # QgsInterface()
    _menuAction = None  # QAction()
    _dockLocation = None  # Qt::DockWidgetArea

    def __init__(self, iface, parent=None):
        super(QgsDockWidget, self).__init__(parent)

    def load(self, iface, location, menu, toolbar, iconPath, actionText, tip='', whatsThis=''):
        self._iface = iface
        self._dockLocation = location
        icon = QIcon(iconPath)
        self._menuAction = QAction(icon, actionText, self._iface.mainWindow())
        self._menuAction.toggled.connect(self._toggle)
        self._menuAction.toggled.connect(self.toggled)
        self._menuAction.setCheckable(True)
        self._menuAction.setStatusTip(tip)
        self._menuAction.setWhatsThis(whatsThis)
        toolbar.addAction(self._menuAction)

        self._iface.addPluginToMenu(menu, self._menuAction)

        self.visibilityChanged.connect(self._menuAction.setChecked)
        self.dockLocationChanged.connect(self._updateDockLocation)

    def unload(self):
        self._iface.removeToolBarIcon(self._menuAction)
        self._iface.removeDockWidget(self)
        self.deleteLater()

    def menuAction(self):
        return self._menuAction

    def dockLocation(self):
        return self._dockLocation

    def _updateDockLocation(self, location):
        self._dockLocation = location

    def _toggle(self, checked):
        if checked:
            self._iface.addDockWidget(self._dockLocation, self)
        else:
            self._iface.removeDockWidget(self)
