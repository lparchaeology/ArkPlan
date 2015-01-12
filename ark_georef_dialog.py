# -*- coding: utf-8 -*-
"""
/***************************************************************************
 ArkPlanDialog
                                 A QGIS plugin
 Plugin to assist in digitising of Archaeological plans.
                             -------------------
        begin                : 2015-01-10
        git sha              : $Format:%H$
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

import os

from PyQt4.QtCore import Qt, QFileInfo, QPoint, QPointF, QObject, SIGNAL, qDebug
from PyQt4 import QtGui, uic
from qgis.core import QgsPoint, QgsMapLayerRegistry
import osgeo
import ark_georef_dialog_base
import ark_georef_graphics_view

class ArkGeorefDialog(QtGui.QDialog, ark_georef_dialog_base.Ui_ArkGeorefDialogBase):

    gridPoint1 = QPoint()
    gridPoint2 = QPoint()
    gridPoint3 = QPoint()

    geo1 = QgsPoint()
    geo2 = QgsPoint()
    geo3 = QgsPoint()

    gcp1 = QPointF()
    gcp2 = QPointF()
    gcp3 = QPointF()

    def __init__(self, rawFile, gridReference, gridLayerId, gridX, gridY, parent=None):
        super(ArkGeorefDialog, self).__init__(parent)
        self.setupUi(self)
        self.rawFile = rawFile
        self.gridReference = gridReference
        self.rawPixmap = QtGui.QPixmap(self.rawFile.absoluteFilePath())
        self.scene = QtGui.QGraphicsScene(self)
        self.rawItem = self.scene.addPixmap(self.rawPixmap)
        QObject.connect(self.m_runButton,  SIGNAL("clicked()"),  self.runGeoreference)

        self.gridPoint1 = QPoint(self.gridReference.x(), self.gridReference.y() + 5)
        self.m_gridLabel1.setText('%d / %d' % (self.gridPoint1.x(), self.gridPoint1.y()))
        self.m_gridView1.setScene(self.scene)
        self.m_gridView1.centerOn(250, 100)
        self.m_gridView1.scale(2, 2)
        self.gridItem1 = self.scene.addEllipse(-1.5, -1.5, 3.0, 3.0, QtGui.QPen(Qt.red))
        self.gridItem1.setVisible(False)
        QObject.connect(self.m_gridView1,  SIGNAL("pointSelected(QPointF)"),  self.setGcp1)

        self.gridPoint2 = QPoint(self.gridReference.x(), self.gridReference.y())
        self.m_gridLabel2.setText('%d / %d' % (self.gridPoint2.x(), self.gridPoint2.y()))
        self.m_gridView2.setScene(self.scene)
        self.m_gridView2.centerOn(250, 3050)
        self.m_gridView2.scale(2, 2)
        self.gridItem2 = self.scene.addEllipse(-1.5, -1.5, 3.0, 3.0, QtGui.QPen(Qt.red))
        self.gridItem2.setVisible(False)
        QObject.connect(self.m_gridView2,  SIGNAL("pointSelected(QPointF)"),  self.setGcp2)

        self.gridPoint3 = QPoint(self.gridReference.x() + 5, self.gridReference.y())
        self.m_gridLabel3.setText('%d / %d' % (self.gridPoint3.x(), self.gridPoint3.y()))
        self.m_gridView3.setScene(self.scene)
        self.m_gridView3.centerOn(3200, 3050)
        self.m_gridView3.scale(2, 2)
        self.gridItem3 = self.scene.addEllipse(-1.5, -1.5, 3.0, 3.0, QtGui.QPen(Qt.red))
        self.gridItem3.setVisible(False)
        QObject.connect(self.m_gridView3,  SIGNAL("pointSelected(QPointF)"),  self.setGcp3)

        # Find the geo points for the grid points
        gridLayer = QgsMapLayerRegistry.instance().mapLayersByName(gridLayerId)[0]
        #gridLayer = QgsMapLayerRegistry.instance().mapLayer(gridLayerId)
        iX = gridLayer.fieldNameIndex(gridX)
        iY = gridLayer.fieldNameIndex(gridY)
        features = gridLayer.getFeatures()
        for feature in features:
            if feature.attributes()[iX] == self.gridPoint1.x() and feature.attributes()[iY] == self.gridPoint1.y():
                   self.geo1 = feature.geometry().asPoint()
            if feature.attributes()[iX] == self.gridPoint2.x() and feature.attributes()[iY] == self.gridPoint2.y():
                   self.geo2 = feature.geometry().asPoint()
            if feature.attributes()[iX] == self.gridPoint3.x() and feature.attributes()[iY] == self.gridPoint3.y():
                   self.geo3 = feature.geometry().asPoint()

        self.m_gcpTable.item(0, 2).setText(str(self.gridPoint1.x()))
        self.m_gcpTable.item(0, 3).setText(str(self.gridPoint1.y()))
        self.m_gcpTable.item(0, 4).setText(str(self.geo1.x()))
        self.m_gcpTable.item(0, 5).setText(str(self.geo1.y()))

        self.m_gcpTable.item(1, 2).setText(str(self.gridPoint2.x()))
        self.m_gcpTable.item(1, 3).setText(str(self.gridPoint2.y()))
        self.m_gcpTable.item(1, 4).setText(str(self.geo2.x()))
        self.m_gcpTable.item(1, 5).setText(str(self.geo2.y()))

        self.m_gcpTable.item(2, 2).setText(str(self.gridPoint3.x()))
        self.m_gcpTable.item(2, 3).setText(str(self.gridPoint3.y()))
        self.m_gcpTable.item(2, 4).setText(str(self.geo3.x()))
        self.m_gcpTable.item(2, 5).setText(str(self.geo3.y()))

    def setGcp1(self, point):
        self.gcp1 = point
        self.gridItem1.setPos(point)
        self.gridItem1.setVisible(True)
        self.m_gcpTable.item(0, 0).setText(str(point.x()))
        self.m_gcpTable.item(0, 1).setText(str(point.y()))

    def setGcp2(self, point):
        self.gcp2 = point
        self.gridItem2.setPos(point)
        self.gridItem2.setVisible(True)
        self.m_gcpTable.item(1, 0).setText(str(point.x()))
        self.m_gcpTable.item(1, 1).setText(str(point.y()))

    def setGcp3(self, point):
        self.gcp3 = point
        self.gridItem3.setPos(point)
        self.gridItem3.setVisible(True)
        self.m_gcpTable.item(2, 0).setText(str(point.x()))
        self.m_gcpTable.item(2, 1).setText(str(point.y()))

    def runGeoreference(self):
        osgeo.gdal.ContourGenerate()
