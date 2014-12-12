# -*- coding: utf-8 -*-
"""
/***************************************************************************
 ArkPlanDialog
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

import os
from PyQt4.QtCore import *
from PyQt4.QtGui import *
from PyQt4 import uic
from qgis.core import *

class ArkPlanDock(QObject):
    """This class controls all plugin-related GUI elements."""

    def __init__ (self,iface):
        """initialize the GUI control"""
        QObject.__init__(self)
        self.iface = iface

        # load the form
        path = os.path.dirname(os.path.abspath( __file__ ))
        self.dock = uic.loadUi(os.path.join( path, "ui_dock.ui" ))
        self.iface.addDockWidget(Qt.RightDockWidgetArea, self.dock)

        # connect to gui signals
        #QObject.connect(self.dock,
