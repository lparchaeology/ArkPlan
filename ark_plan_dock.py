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

        QObject.connect(self.m_loadRawButton,  SIGNAL("clicked()"), self, SIGNAL("loadRawFileSelected()"))
        QObject.connect(self.m_georefButton,  SIGNAL("clicked()"), self, SIGNAL("georefSelected()"))
        QObject.connect(self.m_loadGeoButton,  SIGNAL("clicked()"), self, SIGNAL("loadGeoFileSelected()"))
        QObject.connect(self.m_contextSpin,  SIGNAL("valueChanged(int)"), self, SIGNAL("contextChanged(int)"))
        QObject.connect(self.m_eastSpin,  SIGNAL("valueChanged(int)"), self.changedGridReference)
        QObject.connect(self.m_northSpin,  SIGNAL("valueChanged(int)"), self.changedGridReference)
        QObject.connect(self.m_sourceEdit,  SIGNAL("textChanged(QString)"), self, SIGNAL("sourceChanged(QString)"))

        QObject.connect(self.m_extentTool,  SIGNAL("clicked()"), self.extentSelected)
        QObject.connect(self.m_breakOfSlopeTool,  SIGNAL("clicked()"), self.breakOfSlopeSelected)
        QObject.connect(self.m_limitOfExcavationTool,  SIGNAL("clicked()"), self.limitOfExcavationSelected)
        QObject.connect(self.m_truncationTool,  SIGNAL("clicked()"), self.truncationSelected)
        QObject.connect(self.m_uncertainEdgeTool,  SIGNAL("clicked()"), self.uncertainEdgeSelected)
        QObject.connect(self.m_verticalBreakOfSlopeTool,  SIGNAL("clicked()"), self.verticalBreakOfSlopeSelected)
        QObject.connect(self.m_verticalEdgeTool,  SIGNAL("clicked()"), self.verticalEdgeSelected)
        QObject.connect(self.m_verticalTruncationTool,  SIGNAL("clicked()"), self.verticalTruncationSelected)

        QObject.connect(self.m_brickTool,  SIGNAL("clicked()"), self.brickSelected)
        QObject.connect(self.m_cbmTool,  SIGNAL("clicked()"), self.cbmSelected)
        QObject.connect(self.m_charcoalTool,  SIGNAL("clicked()"), self.charcoalSelected)
        QObject.connect(self.m_flintTool,  SIGNAL("clicked()"), self.flintSelected)
        QObject.connect(self.m_mortarTool,  SIGNAL("clicked()"), self.mortarSelected)
        QObject.connect(self.m_potTool,  SIGNAL("clicked()"), self.potSelected)
        QObject.connect(self.m_tileTool,  SIGNAL("clicked()"), self.tileSelected)
        QObject.connect(self.m_stoneTool,  SIGNAL("clicked()"), self.stoneSelected)

        QObject.connect(self.m_hachureTool,  SIGNAL("clicked()"), self.hachureSelected)
        QObject.connect(self.m_undercutTool,  SIGNAL("clicked()"), self.undercutSelected)
        QObject.connect(self.m_returnOfSlopeTool,  SIGNAL("clicked()"), self.returnOfSlopeSelected)

        QObject.connect(self.m_levelTool,  SIGNAL("clicked()"), self, SIGNAL("selectedLevelsMode()"))

        QObject.connect(self.m_schematicTool,  SIGNAL("clicked()"), self.schematicSelected)

    # Plan Tools

    def setFile(self, name):
        self.m_fileEdit.setText(name)

    def setSite(self, name):
        self.m_siteEdit.setText(name)

    def setContext(self, context):
        self.m_contextSpin.setValue(context)

    def setGridReference(self, easting, northing):
        self.m_eastSpin.setValue(easting)
        self.m_northSpin.setValue(northing)

    def changedGridReference(self):
        self.emit(SIGNAL("gridReferenceChanged(int, int)"), self.m_eastSpin.value(), self.m_northSpin.value())

    def setSource(self, source):
        self.m_sourceEdit.setText(source)

    # Drawing Tools

    def extentSelected(self):
        self.emit(SIGNAL("selectedLineMode(QString)"), "ext")

    def breakOfSlopeSelected(self):
        self.emit(SIGNAL("selectedLineMode(QString)"), "bos")

    def limitOfExcavationSelected(self):
        self.emit(SIGNAL("selectedLineMode(QString)"), "loe")

    def truncationSelected(self):
        self.emit(SIGNAL("selectedLineMode(QString)"), "trn")

    def uncertainEdgeSelected(self):
        self.emit(SIGNAL("selectedLineMode(QString)"), "ueg")

    def verticalBreakOfSlopeSelected(self):
        self.emit(SIGNAL("selectedLineMode(QString)"), "vbs")

    def verticalEdgeSelected(self):
        self.emit(SIGNAL("selectedLineMode(QString)"), "veg")

    def verticalTruncationSelected(self):
        self.emit(SIGNAL("selectedLineMode(QString)"), "vtr")

    def brickSelected(self):
        self.emit(SIGNAL("selectedPolygonMode(QString)"), "brk")

    def cbmSelected(self):
        self.emit(SIGNAL("selectedPolygonMode(QString)"), "cbm")

    def charcoalSelected(self):
        self.emit(SIGNAL("selectedPolygonMode(QString)"), "cha")

    def flintSelected(self):
        self.emit(SIGNAL("selectedPolygonMode(QString)"), "fli")

    def mortarSelected(self):
        self.emit(SIGNAL("selectedPolygonMode(QString)"), "mtr")

    def potSelected(self):
        self.emit(SIGNAL("selectedPolygonMode(QString)"), "pot")

    def stoneSelected(self):
        self.emit(SIGNAL("selectedPolygonMode(QString)"), "sto")

    def tileSelected(self):
        self.emit(SIGNAL("selectedPolygonMode(QString)"), "til")

    def hachureSelected(self):
        self.emit(SIGNAL("selectedHachureMode(QString)"), "hch")

    def undercutSelected(self):
        self.emit(SIGNAL("selectedHachureMode(QString)"), "unc")

    def returnOfSlopeSelected(self):
        self.emit(SIGNAL("selectedHachureMode(QString)"), "ros")

    def schematicSelected(self):
        self.emit(SIGNAL("selectedSchematicMode(QString)"), "sch")

