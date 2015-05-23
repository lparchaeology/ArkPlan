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

import os.path

from PyQt4 import uic
from PyQt4.QtCore import Qt, QPoint
from PyQt4.QtGui import QDialog

from qgis.core import QgsPoint

from ..core.map_tools import ArkMapToolEmitPoint

from create_grid_dialog_base import *

class CreateGridDialog(QDialog, Ui_CreateGridDialog):

    PointOnXAxis = 0
    PointOnYAxis = 1

    _project = None # PluginSettings()
    _mapTool = None # ArkMapToolEmitPoint

    def __init__(self, project, parent=None):
        super(CreateGridDialog, self).__init__(parent)
        self._project = project

        self.setupUi(self)
        self.crsOriginFromMapButton.clicked.connect(self.getOriginFromMap)
        self.crsAxisFromMapButton.clicked.connect(self.getAxisFromMap)
        self.createGridButton.clicked.connect(self.accept)
        self.cancelButton.clicked.connect(self.reject)

        self._mapTool = ArkMapToolEmitPoint(self._project.iface.mapCanvas())
        self._mapTool.setSnappingEnabled(True)
        self._mapTool.canvasClicked.connect(self.pointSelected)
        self._mapTool.deactivated.connect(self.cancelGetPoint)

    def crsOriginPoint(self):
        return QgsPoint(self.crsOriginEastingSpin.value(), self.crsOriginNorthingSpin.value())

    def crsAxisPoint(self):
        return QgsPoint(self.crsAxisEastingSpin.value(), self.crsAxisNorthingSpin.value())

    def crsAxisPointType(self):
        if self.crsOnAxisYButton.isChecked():
            return CreateGridDialog.PointOnYAxis
        else:
            return CreateGridDialog.PointOnXAxis

    def localOriginPoint(self):
        return QPoint(self.localOriginEastingSpin.value(), self.localOriginNorthingSpin.value())

    def localTerminusPoint(self):
        return QPoint(self.localTerminusEastingSpin.value(), self.localTerminusNorthingSpin.value())

    def localEastingInterval(self):
        return self.localEastingIntervalSpin.value()

    def localNorthingInterval(self):
        return self.localNorthingIntervalSpin.value()

    def getOriginFromMap(self):
        self.getPoint = 'origin'
        self.getPointFromMap()

    def getAxisFromMap(self):
        self.getPoint = 'axis'
        self.getPointFromMap()

    def getPointFromMap(self):
        self._project.iface.mapCanvas().setMapTool(self._mapTool)
        self._showMainWindow()

    def cancelGetPoint(self):
        self._showDialog()

    def pointSelected(self, point, button):
        if (button == Qt.LeftButton):
            if self.getPoint == 'origin':
                self.crsOriginEastingSpin.setValue(point.x())
                self.crsOriginNorthingSpin.setValue(point.y())
            elif self.getPoint == 'axis':
                self.crsAxisEastingSpin.setValue(point.x())
                self.crsAxisNorthingSpin.setValue(point.y())
        self._project.iface.mapCanvas().unsetMapTool(self._mapTool)
        self._showDialog()

    def _showMainWindow(self):
        if self.parentWidget() is not None:
            self.showMinimized()
            self.parentWidget().activateWindow()
            self.parentWidget().raise_()

    def _showDialog(self):
        self.showNormal()
        self.activateWindow()
        self.raise_()
