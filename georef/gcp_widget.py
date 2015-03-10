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

from PyQt4.QtCore import Qt, pyqtSignal
from PyQt4.QtGui import QWidget, uic

import gcp_widget_base

class GcpWidget(QWidget, gcp_widget_base.Ui_GcpWidgetBase):

    # Internal variables
    gridPoint = QPoint()
    geoPoint = QgsPoint()
    rawPoint = QPointF()

    def __init__(self, parent=None):
        super(GcpWidget, self).__init__(parent)
        self.setupUi(self)
