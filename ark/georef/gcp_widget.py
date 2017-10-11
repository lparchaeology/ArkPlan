# -*- coding: utf-8 -*-
"""
/***************************************************************************
                                ARK Spatial
                    A QGIS plugin for Archaeological Recording.
        Part of the Archaeological Recording Kit by L-P : Archaeology
                        http://ark.lparchaeology.com
                              -------------------
        copyright            : 2017 by L-P : Heritage LLP
        email                : ark@lparchaeology.com
        copyright            : 2017 by John Layt
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

from PyQt4.QtCore import QPointF, Qt, pyqtSignal
from PyQt4.QtGui import QPen, QWidget

from .gcp import GroundControlPoint
from .ui.gcp_widget_base import Ui_GcpWidget


class GcpWidget(QWidget, Ui_GcpWidget):

    rawPointChanged = pyqtSignal(QPointF)

    # Internal variables
    _gcp = None

    _gridEditable = False
    _mapEditable = False
    _rawEditable = True

    _gcpItem = None  # QGraphicsItem

    def __init__(self, parent=None):
        super(GcpWidget, self).__init__(parent)
        self.setupUi(self)
        self._gcp = GroundControlPoint()

    def setScene(self, scene, centerX=0, centerY=0, scale=1):
        self.gcpView.setScene(scene)
        self.gcpView.centerOn(centerX, centerY)
        self.gcpView.scale(scale, scale)
        self._gcpItem = self.gcpView.scene().addEllipse(-1.5, -1.5, 3.0, 3.0, QPen(Qt.red))
        self._gcpItem.setVisible(False)
        self.gcpView.pointSelected.connect(self.setRaw)
        self.rawXSpin.valueChanged.connect(self._setRawX)
        self.rawYSpin.valueChanged.connect(self._setRawY)

    def gcp(self):
        return self._gcp

    def setGcp(self, gcp):
        self._gcp = gcp
        self._update()

    def setGeo(self, local, map):
        self._gcp.setLocal(local)
        self._gcp.setMap(map)
        self._updateGeo()

    def setRaw(self, raw):
        self._gcp.setRaw(raw)
        self._updateRaw()

    def _update(self):
        self._updateGeo()
        self._updateRaw()

    def _updateGeo(self):
        self.localX.setNum(self._gcp.local().x())
        self.localY.setNum(self._gcp.local().y())
        self.mapX.setNum(self._gcp.map().x())
        self.mapY.setNum(self._gcp.map().y())

    def _updateRaw(self):
        self.rawXSpin.setValue(self._gcp.raw().x())
        self.rawYSpin.setValue(self._gcp.raw().y())
        self._updateGcpItem()

    def _setRawX(self, x):
        if (x != self._gcp.raw().x()):
            self._gcp.setRawX(x)
            self._updateGcpItem()

    def _setRawY(self, y):
        if (y != self._gcp.raw().y()):
            self._gcp.setRawY(y)
            self._updateGcpItem()

    def _updateGcpItem(self):
        if (self._gcp.isRawSet()):
            self._gcpItem.setPos(self._gcp.raw())
            self._gcpItem.setVisible(True)
        else:
            self._gcpItem.setVisible(False)
        # TODO if outside view then center on point
