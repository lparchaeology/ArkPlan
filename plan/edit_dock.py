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
from PyQt4.QtGui import QWidget, QVBoxLayout, QToolBar, QSpacerItem, QSizePolicy

from ..libarkqgis.dock import ArkDockWidget
from ..libarkqgis.snapping import *

import edit_widget_base

class EditWidget(QWidget, edit_widget_base.Ui_EditWidget):

    def __init__(self, parent=None):
        super(EditWidget, self).__init__(parent)
        self.setupUi(self)

class EditDock(ArkDockWidget):

    def __init__(self, iface, parent=None):
        super(EditDock, self).__init__(parent)

        self.setWindowTitle(u'Editing Tools')
        self.setObjectName(u'EditDock')

        self.editToolbar = QToolBar()
        self.editToolbar.setObjectName(u'editToolbar')
        self.editToolbar.setIconSize(QSize(22, 22))
        self.editToolbar.addAction(iface.actionPan())
        self.editToolbar.addAction(iface.actionZoomIn())
        self.editToolbar.addAction(iface.actionZoomOut())
        self.editToolbar.addAction(iface.actionZoomLast())
        self.editToolbar.addAction(iface.actionZoomNext())

        self.editWidget = EditWidget()
        self.editWidget.setObjectName(u'editWidget')

        self.editSpacer = QSpacerItem(20, 40, QSizePolicy.Minimum, QSizePolicy.Expanding)

        self.verticalLayout = QVBoxLayout()
        self.verticalLayout.setObjectName(u'verticalLayout')
        self.verticalLayout.addWidget(self.editToolbar)
        self.verticalLayout.addWidget(self.editWidget)
        self.verticalLayout.addSpacerItem(self.editSpacer)

        self.editDockContents = QWidget()
        self.editDockContents.setObjectName(u'editDockContents')
        self.editDockContents.setLayout(self.verticalLayout)
        self.setWidget(self.editDockContents)

    def addAction(self, action):
        self.editToolbar.addAction(action)

    # Snapping Tools

    def setBufferPoints(self, layer):
        self.editWidget.snapBufferPointsTool.setLayer(layer)

    def setBufferLines(self, layer):
        self.editWidget.snapBufferLinesTool.setLayer(layer)

    def setBufferPolygons(self, layer):
        self.editWidget.snapBufferPolygonsTool.setLayer(layer)

    def setPlanPoints(self, layer):
        self.editWidget.snapPlanPointsTool.setLayer(layer)

    def setPlanLines(self, layer):
        self.editWidget.snapPlanLinesTool.setLayer(layer)

    def setPlanPolygons(self, layer):
        self.editWidget.snapPlanPolygonsTool.setLayer(layer)

    def setBasePoints(self, layer):
        self.editWidget.snapBasePointsTool.setLayer(layer)

    def setBaseLines(self, layer):
        self.editWidget.snapBaseLinesTool.setLayer(layer)

    def setBasePolygons(self, layer):
        self.editWidget.snapBasePolygonsTool.setLayer(layer)
