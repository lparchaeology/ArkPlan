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
from PyQt4.QtCore import Qt, pyqtSignal
from PyQt4.QtGui import QDockWidget

FORM_CLASS, _ = uic.loadUiType(os.path.join(os.path.dirname(__file__), 'ui_dock.ui'))

class ArkPlanDock(QDockWidget, FORM_CLASS):

    loadRawFileSelected = pyqtSignal()
    loadGeoFileSelected = pyqtSignal()

    siteChanged = pyqtSignal('QString')
    contextChanged = pyqtSignal(int)
    sourceChanged = pyqtSignal('QString')
    commentChanged = pyqtSignal('QString')

    selectedLineMode = pyqtSignal('QString')
    selectedPolygonMode = pyqtSignal('QString')
    selectedHachureMode = pyqtSignal('QString')
    selectedSchematicMode = pyqtSignal('QString')
    selectedLevelsMode = pyqtSignal()

    clearSelected = pyqtSignal()
    mergeSelected = pyqtSignal()

    def __init__(self, iface):
        QDockWidget.__init__(self)
        self.setupUi(self)
        self.iface = iface

        self.m_loadRawButton.clicked.connect(self.loadRawFileSelected)
        self.m_loadGeoButton.clicked.connect(self.loadGeoFileSelected)

        self.m_siteEdit.textChanged.connect(self.siteChanged)
        self.m_contextSpin.valueChanged.connect(self.contextChanged)
        self.m_sourceEdit.textChanged.connect(self.sourceChanged)
        self.m_commentEdit.textChanged.connect(self.commentChanged)

        self.m_extentTool.clicked.connect(self.extentSelected)
        self.m_breakOfSlopeTool.clicked.connect(self.breakOfSlopeSelected)
        self.m_limitOfExcavationTool.clicked.connect(self.limitOfExcavationSelected)
        self.m_truncationTool.clicked.connect(self.truncationSelected)
        self.m_uncertainEdgeTool.clicked.connect(self.uncertainEdgeSelected)
        self.m_verticalBreakOfSlopeTool.clicked.connect(self.verticalBreakOfSlopeSelected)
        self.m_verticalEdgeTool.clicked.connect(self.verticalEdgeSelected)
        self.m_verticalTruncationTool.clicked.connect(self.verticalTruncationSelected)

        self.m_brickTool.clicked.connect(self.brickSelected)
        self.m_cbmTool.clicked.connect(self.cbmSelected)
        self.m_charcoalTool.clicked.connect(self.charcoalSelected)
        self.m_flintTool.clicked.connect(self.flintSelected)
        self.m_mortarTool.clicked.connect(self.mortarSelected)
        self.m_potTool.clicked.connect(self.potSelected)
        self.m_tileTool.clicked.connect(self.tileSelected)
        self.m_stoneTool.clicked.connect(self.stoneSelected)

        self.m_hachureTool.clicked.connect(self.hachureSelected)
        self.m_undercutTool.clicked.connect(self.undercutSelected)
        self.m_returnOfSlopeTool.clicked.connect(self.returnOfSlopeSelected)

        self.m_levelTool.clicked.connect(self.selectedLevelsMode)

        self.m_schematicTool.clicked.connect(self.schematicSelected)

        self.m_clearButton.clicked.connect(self.clearSelected)
        self.m_mergeButton.clicked.connect(self.mergeSelected)

    # Plan Tools

    def setSite(self, name):
        self.m_siteEdit.setText(name)

    def setContext(self, context):
        self.m_contextSpin.setValue(context)

    def setSource(self, source):
        self.m_sourceEdit.setText(source)

    def setComment(self, comment):
        self.m_commentEdit.setText(comment)

    # Drawing Tools

    def extentSelected(self):
        self.selectedLineMode("ext")

    def breakOfSlopeSelected(self):
        self.selectedLineMode("bos")

    def limitOfExcavationSelected(self):
        self.selectedLineMode("loe")

    def truncationSelected(self):
        self.selectedLineMode("trn")

    def uncertainEdgeSelected(self):
        self.selectedLineMode("ueg")

    def verticalBreakOfSlopeSelected(self):
        self.selectedLineMode("vbs")

    def verticalEdgeSelected(self):
        self.selectedLineMode("veg")

    def verticalTruncationSelected(self):
        self.selectedLineMode("vtr")

    def brickSelected(self):
        self.selectedPolygonMode("brk")

    def cbmSelected(self):
        self.selectedPolygonMode("cbm")

    def charcoalSelected(self):
        self.selectedPolygonMode("cha")

    def flintSelected(self):
        self.selectedPolygonMode("fli")

    def mortarSelected(self):
        self.selectedPolygonMode("mtr")

    def potSelected(self):
        self.selectedPolygonMode("pot")

    def stoneSelected(self):
        self.selectedPolygonMode("sto")

    def tileSelected(self):
        self.selectedPolygonMode("til")

    def hachureSelected(self):
        self.selectedHachureMode("hch")

    def undercutSelected(self):
        self.selectedHachureMode("unc")

    def returnOfSlopeSelected(self):
        self.selectedHachureMode("ros")

    def schematicSelected(self):
        self.selectedSchematicMode("sch")

