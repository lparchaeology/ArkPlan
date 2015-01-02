# -*- coding: utf-8 -*-
"""
/***************************************************************************
 ArkPlanDialog
                                 A QGIS plugin
 Plugin to assist in digitising of Archaeological plans.
                             -------------------
        begin                : 2014-12-07
        git sha              : $Format:%H$
        copyright            : (C) 2014 by John Layt
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
from PyQt4 import uic
from PyQt4.QtCore import Qt, QObject, SIGNAL
from PyQt4.QtGui import QDockWidget, QMessageBox

FORM_CLASS, _ = uic.loadUiType(os.path.join(os.path.dirname(__file__), 'ui_dock.ui'))

class ArkPlanDock(QDockWidget, FORM_CLASS):

    def __init__(self, iface):
        QDockWidget.__init__(self)
        self.setupUi(self)
        self.iface = iface
        QObject.connect(self.m_levelTool,  SIGNAL("clicked()"), self, SIGNAL("selectedLevelsMode()"))
        QObject.connect(self.m_contextSpin,  SIGNAL("valueChanged(int)"), self, SIGNAL("contextChanged(int)"))
        QObject.connect(self.m_sourceEdit,  SIGNAL("textChanged(QString)"), self, SIGNAL("sourceChanged(QString)"))

    def setContext(self, context):
        self.m_contextSpin.setValue(context)

    def setSource(self, source):
        self.m_sourceEdit.setText(source)
