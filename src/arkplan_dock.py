# -*- coding: utf-8 -*-
"""
/***************************************************************************
                                      Ark
                                 A QGIS plugin
             QGIS Plugin for ARK, the Archaeological Recording Kit
                              -------------------
        begin                : 2015-03-02
        git sha              : $Format:%H$
        copyright            : (C) 2015 by L - P: Heritage LLP
        copyright            : (C) 2015 by John Layt
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

from PyQt4 import uic
from PyQt4.QtCore import QSize
from PyQt4.QtGui import QWidget, QVBoxLayout, QToolBar

from qgis.gui import QgsLayerTreeView

from ..libarkqgis.dock import ArkDockWidget

class ArkPlanDock(ArkDockWidget):

    def __init__(self, parent=None):
        super(ArkPlanDock, self).__init__(parent)

        self.setWindowTitle(u'ARK Project Layers')
        self.setObjectName(u'ArkPlanDock')

        self.dockToolbar = QToolBar(self)
        self.dockToolbar.setObjectName(u'dockToolbar')
        self.dockToolbar.setIconSize(QSize(24, 24))

        self.projectLayerView = QgsLayerTreeView(self)
        self.projectLayerView.setObjectName(u'projectLayerView')

        self.verticalLayout = QVBoxLayout(self)
        self.verticalLayout.setObjectName(u'verticalLayout')
        self.verticalLayout.addWidget(self.dockToolbar)
        self.verticalLayout.addWidget(self.projectLayerView)

        self.dockContents = QWidget(self)
        self.dockContents.setObjectName(u'dockContents')
        self.dockContents.setLayout(self.verticalLayout)
        self.setWidget(self.dockContents)

    def addAction(self, action):
        self.dockToolbar.addAction(action)

    def unload(self):
        del self.projectLayerView
        self.projectLayerView = None
        super(ArkPlanDock, self).unload()
