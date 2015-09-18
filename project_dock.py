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
from PyQt4.QtCore import Qt, pyqtSignal, QSize
from PyQt4.QtGui import QWidget, QVBoxLayout, QToolBar

from qgis.gui import QgsLayerTreeView

from .libarkqgis.dock import ArkDockWidget

class ProjectDock(ArkDockWidget):

    def __init__(self, parent=None):
        super(ProjectDock, self).__init__(parent)

        self.setWindowTitle(u'ARK Project Layers')
        self.setObjectName(u'ProjectDock')

        self.projectToolbar = QToolBar()
        self.projectToolbar.setObjectName(u'projectToolbar')
        self.projectToolbar.setIconSize(QSize(24, 24))

        self.projectLayerView = QgsLayerTreeView()
        self.projectLayerView.setObjectName(u'projectLayerView')

        self.verticalLayout = QVBoxLayout()
        self.verticalLayout.setObjectName(u'verticalLayout')
        self.verticalLayout.addWidget(self.projectToolbar)
        self.verticalLayout.addWidget(self.projectLayerView)

        self.projectDockContents = QWidget()
        self.projectDockContents.setObjectName(u'projectDockContents')
        self.projectDockContents.setLayout(self.verticalLayout)
        self.setWidget(self.projectDockContents)

    def addAction(self, action):
        self.projectToolbar.addAction(action)
