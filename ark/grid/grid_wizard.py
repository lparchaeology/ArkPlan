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

import os.path

from PyQt4 import uic
from PyQt4.QtCore import Qt, QPoint
from PyQt4.QtGui import QWizard

from qgis.core import QgsPoint

from ..libarkqgis.map_tools import ArkMapToolEmitPoint

from grid_wizard_base import *

class GridWizard(QWizard, Ui_GridWizard):

    TwoKnownPoints = 0
    PointOnXAxis = 1
    PointOnYAxis = 2

    _iface = None # QgisInterface()
    _mapTool = None # ArkMapToolEmitPoint

    def __init__(self, iface, project, parent=None):
        super(GridWizard, self).__init__(parent)
        self._iface = iface

        self.setupUi(self)
        self.gridFolderEdit.setText(project.grid.settings.collectionPath)
        self.gridGroupNameEdit.setText(project.grid.settings.collectionGroupName)
        self.gridPointsNameEdit.setText(project.grid.settings.pointsLayerName)
        self.gridLinesNameEdit.setText(project.grid.settings.linesLayerName)
        self.gridPolygonsNameEdit.setText(project.grid.settings.polygonsLayerName)
        self.siteCodeEdit.setText(project.siteCode())
        self.mapPoint1FromMapButton.clicked.connect(self.getPoint1FromMap)
        self.mapPoint2FromMapButton.clicked.connect(self.getPoint2FromMap)
        self.methodCombo.currentIndexChanged.connect(self.setMethodType)

        self._mapTool = ArkMapToolEmitPoint(self._iface.mapCanvas())
        self._mapTool.setSnappingEnabled(True)
        self._mapTool.canvasClicked.connect(self.pointSelected)
        self._mapTool.deactivated.connect(self.cancelGetPoint)

    def mapPoint1(self):
        return QgsPoint(self.mapPoint1EastingSpin.value(), self.mapPoint1NorthingSpin.value())

    def mapPoint2(self):
        return QgsPoint(self.mapPoint2EastingSpin.value(), self.mapPoint2NorthingSpin.value())

    def localPoint1(self):
        if self.methodType() == GridWizard.TwoKnownPoints:
            return QgsPoint(self.localPoint1EastingSpin.value(), self.localPoint1NorthingSpin.value())
        return QgsPoint(self.localOriginEastingSpin.value(), self.localOriginNorthingSpin.value())

    def localPoint2(self):
        if self.methodType() == GridWizard.TwoKnownPoints:
            return QgsPoint(self.localPoint2EastingSpin.value(), self.localPoint2NorthingSpin.value())
        return QgsPoint()

    def methodType(self):
        return self.methodCombo.currentIndex()

    def setMethodType(self, method):
        if method == GridWizard.TwoKnownPoints:
            self.mapPoint1Label.setText('Map Point 1')
            self.localPoint1Label.setEnabled(True)
            self.localPoint1EastingSpin.setEnabled(True)
            self.localPoint1NorthingSpin.setEnabled(True)
            self.mapPoint2Label.setText('Map Point 2')
            self.localPoint2Label.setEnabled(True)
            self.localPoint2EastingSpin.setEnabled(True)
            self.localPoint2NorthingSpin.setEnabled(True)
        else:
            self.mapPoint1Label.setText('Map Origin Point')
            self.localPoint1Label.setEnabled(False)
            self.localPoint1EastingSpin.setEnabled(False)
            self.localPoint1NorthingSpin.setEnabled(False)
            self.mapPoint2Label.setText('Map Axis Point')
            self.localPoint2Label.setEnabled(False)
            self.localPoint2EastingSpin.setEnabled(False)
            self.localPoint2NorthingSpin.setEnabled(False)

    def localOriginPoint(self):
        return QPoint(self.localOriginEastingSpin.value(), self.localOriginNorthingSpin.value())

    def localTerminusPoint(self):
        return QPoint(self.localTerminusEastingSpin.value(), self.localTerminusNorthingSpin.value())

    def localEastingInterval(self):
        return self.localEastingIntervalSpin.value()

    def localNorthingInterval(self):
        return self.localNorthingIntervalSpin.value()

    def siteCode(self):
        return self.siteCodeEdit.text()

    def gridName(self):
        return self.gridNameEdit.text()

    def getPoint1FromMap(self):
        self.getPoint = 'origin'
        self.getPointFromMap()

    def getPoint2FromMap(self):
        self.getPoint = 'axis'
        self.getPointFromMap()

    def getPointFromMap(self):
        self._iface.mapCanvas().setMapTool(self._mapTool)
        self._showMainWindow()

    def cancelGetPoint(self):
        self._showDialog()

    def pointSelected(self, point, button):
        if (button == Qt.LeftButton):
            if self.getPoint == 'origin':
                self.mapPoint1EastingSpin.setValue(point.x())
                self.mapPoint1NorthingSpin.setValue(point.y())
            elif self.getPoint == 'axis':
                self.mapPoint2EastingSpin.setValue(point.x())
                self.mapPoint2NorthingSpin.setValue(point.y())
        self._iface.mapCanvas().unsetMapTool(self._mapTool)
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
