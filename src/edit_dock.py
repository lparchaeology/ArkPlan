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
from PyQt4.QtCore import Qt, pyqtSignal, QSize
from PyQt4.QtGui import QWidget, QVBoxLayout, QToolBar, QSpacerItem, QSizePolicy

from qgis.core import QgsProject

from ..libarkqgis.dock import ArkDockWidget
from ..libarkqgis.snapping import TopologicalEditingAction, IntersectionSnappingAction, SnappingModeTool, Snapping

import edit_widget_base

class EditWidget(QWidget, edit_widget_base.Ui_EditWidget):

    def __init__(self, parent=None):
        super(EditWidget, self).__init__(parent)
        self.setupUi(self)

class EditDock(ArkDockWidget):

    _project = None # QgsProject()
    _modeTool = None # SnappingModeTool()

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
        self.editToolbar.addSeparator()
        self._modeTool = SnappingModeTool(self)
        self._modeTool.setToolButtonStyle(self.editToolbar.toolButtonStyle())
        self.editToolbar.addWidget(self._modeTool)
        self.editToolbar.addAction(IntersectionSnappingAction(self))
        self.editToolbar.addAction(TopologicalEditingAction(self))

        self.editWidget = EditWidget()
        self.editWidget.setObjectName(u'editWidget')
        self.editWidget.snapToleranceSpin.setIface(iface)

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

        self._refresh()
        self._project = QgsProject.instance()
        self._project.snapSettingsChanged.connect(self._refresh)

    def unloadGui(self):
        self.setBufferPoints(None)
        self.setBufferLines(None)
        self.setBufferPolygons(None)
        self.setPlanPoints(None)
        self.setPlanLines(None)
        self.setPlanPolygons(None)
        self.setBasePoints(None)
        self.setBaseLines(None)
        self.setBasePolygons(None)
        super(EditDock, self).unloadGui()

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

    def _refresh(self):
        advanced = (Snapping.snappingMode() == Snapping.SelectedLayers)
        self.editWidget.snapTypeCombo.setDisabled(advanced)
        self.editWidget.snapUnitCombo.setDisabled(advanced)
        self.editWidget.snapToleranceSpin.setDisabled(advanced)
        self.editWidget.snapBufferPointsTool.setEnabled(advanced)
        self.editWidget.snapBufferLinesTool.setEnabled(advanced)
        self.editWidget.snapBufferPolygonsTool.setEnabled(advanced)
        self.editWidget.snapPlanPointsTool.setEnabled(advanced)
        self.editWidget.snapPlanLinesTool.setEnabled(advanced)
        self.editWidget.snapPlanPolygonsTool.setEnabled(advanced)
        self.editWidget.snapBasePointsTool.setEnabled(advanced)
        self.editWidget.snapBaseLinesTool.setEnabled(advanced)
        self.editWidget.snapBasePolygonsTool.setEnabled(advanced)
