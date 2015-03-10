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

import os

from PyQt4.QtCore import Qt, pyqtSignal, QPoint, QPointF
from PyQt4.QtGui import QWidget, QPen
from PyQt4 import uic

from qgis.core import QgsPoint

import gcp_widget_base

class GcpWidget(QWidget, gcp_widget_base.Ui_GcpWidget):

    rawPointChanged = pyqtSignal(QPointF)

    # Internal variables
    _localPoint = QPoint()
    _crsPoint = QgsPoint()
    _rawPoint = QPointF()

    _gridEditable = False
    _crsEditable = False
    _rawEditable = True

    _gcpItem = None  # QGraphicsItem

    def __init__(self, parent=None):
        super(GcpWidget, self).__init__(parent)
        self.setupUi(self)

    def setScene(self, scene, centerX=0, centerY=0, scale=1):
        self.gcpView.setScene(scene)
        self.gcpView.centerOn(centerX, centerY)
        self.gcpView.scale(scale, scale)
        self._gcpItem = self.gcpView.scene().addEllipse(-1.5, -1.5, 3.0, 3.0, QPen(Qt.red))
        self._gcpItem.setVisible(False)
        self.gcpView.pointSelected.connect(self.setRawPoint)
        self.rawXSpin.valueChanged.connect(self.setRawX)
        self.rawYSpin.valueChanged.connect(self.setRawY)

    def localPoint(self):
        return self._localPoint

    def setLocalPoint(self, localPoint):
        self._localPoint = localPoint
        self.localXSpin.setValue(localPoint.x())
        self.localYSpin.setValue(localPoint.y())

    def crsPoint(self):
        return self._crsPoint

    def setCrsPoint(self, crsPoint):
        self._crsPoint = crsPoint
        self.crsXSpin.setValue(crsPoint.x())
        self.crsYSpin.setValue(crsPoint.y())

    def rawPoint(self):
        return self._rawPoint

    def setRawPoint(self, rawPoint):
        self._rawPoint = rawPoint
        self.rawXSpin.setValue(rawPoint.x())
        self.rawYSpin.setValue(rawPoint.y())
        self._updateGcpItem()

    def setRawX(self, x):
        if (x != self._rawPoint.x()):
            self._rawPoint.setX(x)
            self.rawXSpin.setValue(x)
            self._updateGcpItem()

    def setRawY(self, y):
        if (y != self._rawPoint.y()):
            self._rawPoint.setY(y)
            self.rawYSpin.setValue(y)
            self._updateGcpItem()

    def _updateGcpItem(self):
        if (not self._rawPoint.isNull()):
            self._gcpItem.setPos(self._rawPoint)
            self._gcpItem.setVisible(True)
        else:
            self._gcpItem.setVisible(False)
        # TODO if outside view then center on point
