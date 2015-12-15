# -*- coding: utf-8 -*-
"""
/***************************************************************************
                                ARK Spatial
                    A QGIS plugin for Archaeological Recording.
        Part of the Archaeological Recording Kit by L-P : Archaeology
                        http://ark.lparchaeology.com
                              -------------------
        begin                : 2014-12-07
        git sha              : $Format:%H$
        copyright            : 2014, 2015 by L-P : Heritage LLP
        email                : ark@lparchaeology.com
        copyright            : 2014, 2015 by John Layt
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

class LayerDock(ArkDockWidget):

    def __init__(self, parent=None):
        super(LayerDock, self).__init__(parent)

    def initGui(self, iface, location, menuAction):
        super(LayerDock, self).initGui(iface, location, menuAction)
        self.setWindowTitle(u'ARK Spatial Layers')
        self.setObjectName(u'LayerDock')

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

    def addSeparator(self):
        self.dockToolbar.addSeparator()

    def unloadGui(self):
        del self.projectLayerView
        self.projectLayerView = None
        super(LayerDock, self).unloadGui()
