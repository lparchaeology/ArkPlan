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

from PyQt4 import uic
from PyQt4.QtCore import Qt, pyqtSignal
from PyQt4.QtGui import QDockWidget, QMenu, QAction, QIcon

from ..core.dock import *
from ..core.snap_widgets import *

import plan_dock_base

class PlanDock(QgsDockWidget, plan_dock_base.Ui_PlanDockWidget):

    loadRawFileSelected = pyqtSignal()
    loadGeoFileSelected = pyqtSignal()
    loadContextSelected = pyqtSignal()

    siteChanged = pyqtSignal(str)
    contextNumberChanged = pyqtSignal(int)
    baseNumberChanged = pyqtSignal(int)
    sourceChanged = pyqtSignal(str)
    sourceFileChanged = pyqtSignal(str)
    commentChanged = pyqtSignal(str)
    createdByChanged = pyqtSignal(str)

    selectedLineMode = pyqtSignal(str, str)
    selectedPolygonMode = pyqtSignal(str, str)
    selectedLineSegmentMode = pyqtSignal(str, str)
    selectedSchematicMode = pyqtSignal(str, str)
    selectedLevelsMode = pyqtSignal(str, str)

    clearSelected = pyqtSignal()
    mergeSelected = pyqtSignal()

    linesSnappingToggled = pyqtSignal(bool)
    polygonsSnappingToggled = pyqtSignal(bool)
    schematicSnappingToggled = pyqtSignal(bool)

    def __init__(self, parent=None):
        super(PlanDock, self).__init__(parent)
        self.setupUi(self)

        self.m_loadRawButton.clicked.connect(self.loadRawFileSelected)
        self.m_loadGeoButton.clicked.connect(self.loadGeoFileSelected)
        self.m_loadContextButton.clicked.connect(self.loadContextSelected)

        self.m_siteEdit.textChanged.connect(self.siteChanged)
        self.m_contextNumberSpin.valueChanged.connect(self.contextNumberChanged)
        self.m_baseNumberSpin.valueChanged.connect(self.baseNumberChanged)
        self.m_sourceEdit.textChanged.connect(self.sourceChanged)
        self.m_sourceFileEdit.textChanged.connect(self.sourceFileChanged)
        self.m_commentEdit.textChanged.connect(self.commentChanged)
        self.m_createdByEdit.textChanged.connect(self.createdByChanged)

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

        self.m_levelTool.clicked.connect(self.levelsSelected)

        self.m_schematicTool.clicked.connect(self.schematicSelected)

        self.m_sectionPinTool.clicked.connect(self.sectionPinSelected)
        self.m_sectionLineTool.clicked.connect(self.sectionLineSelected)
        self.m_basePointTool.clicked.connect(self.basePointSelected)
        self.m_baseLineTool.clicked.connect(self.baseLineSelected)

        self.m_clearButton.clicked.connect(self.clearSelected)
        self.m_mergeButton.clicked.connect(self.mergeSelected)

        self.m_snapLinesLayerTool.snapSettingsChanged.connect(self.linesLayerSnapSettingsChanged)
        self.m_snapPolygonsLayerTool.snapSettingsChanged.connect(self.polygonsLayerSnapSettingsChanged)
        self.m_snapSchematicsLayerTool.snapSettingsChanged.connect(self.schematicLayerSnapSettingsChanged)

    # Plan Tools

    def setSite(self, name):
        self.m_siteEdit.setText(name)

    def setContextNumber(self, context):
        self.m_contextNumberSpin.setValue(context)

    def setBaseNumber(self, number):
        self.m_baseNumberSpin.setValue(number)

    def setSource(self, source):
        self.m_sourceEdit.setText(source)

    def setSourceFile(self, sourceFile):
        self.m_sourceFileEdit.setText(sourceFile)

    def setComment(self, comment):
        self.m_commentEdit.setText(comment)

    def setCreatedBy(self, creator):
        self.m_createdByEdit.setText(creator)

    # Drawing Tools

    def extentSelected(self):
        self.selectedLineMode.emit('contexts', 'ext')

    def breakOfSlopeSelected(self):
        self.selectedLineMode.emit('contexts', 'bos')

    def limitOfExcavationSelected(self):
        self.selectedLineMode.emit('contexts', 'loe')

    def truncationSelected(self):
        self.selectedLineMode.emit('contexts', 'trn')

    def uncertainEdgeSelected(self):
        self.selectedLineMode.emit('contexts', 'ueg')

    def verticalBreakOfSlopeSelected(self):
        self.selectedLineMode.emit('contexts', 'vbs')

    def verticalEdgeSelected(self):
        self.selectedLineMode.emit('contexts', 'veg')

    def verticalTruncationSelected(self):
        self.selectedLineMode.emit('contexts', 'vtr')

    def brickSelected(self):
        self.selectedPolygonMode.emit('contexts', 'brk')

    def cbmSelected(self):
        self.selectedPolygonMode.emit('contexts', 'cbm')

    def charcoalSelected(self):
        self.selectedPolygonMode.emit('contexts', 'cha')

    def flintSelected(self):
        self.selectedPolygonMode.emit('contexts', 'fli')

    def mortarSelected(self):
        self.selectedPolygonMode.emit('contexts', 'mtr')

    def potSelected(self):
        self.selectedPolygonMode.emit('contexts', 'pot')

    def stoneSelected(self):
        self.selectedPolygonMode.emit('contexts', 'sto')

    def tileSelected(self):
        self.selectedPolygonMode.emit('contexts', 'til')

    def hachureSelected(self):
        self.selectedLineSegmentMode.emit('contexts', 'hch')

    def undercutSelected(self):
        self.selectedLineSegmentMode.emit('contexts', 'unc')

    def returnOfSlopeSelected(self):
        self.selectedLineSegmentMode.emit('contexts', 'ros')

    def levelsSelected(self):
        self.selectedLevelsMode.emit('contexts', 'lvl')

    def schematicSelected(self):
        self.selectedSchematicMode.emit('contexts', 'sch')

    def sectionPinSelected(self):
        self.selectedLevelsMode.emit('base', 'sec')

    def sectionLineSelected(self):
        self.selectedLineMode.emit('base', 'sln')

    def basePointSelected(self):
        self.selectedLevelsMode.emit('base', 'bpt')

    def baseLineSelected(self):
        self.selectedLineMode.emit('base', 'bln')

    # Snapping Tools

    def setLinesBuffer(self, layer):
        self.m_snapLinesBufferTool.setLayer(layer)

    def setPolygonsBuffer(self, layer):
        self.m_snapPolygonsBufferTool.setLayer(layer)

    def setSchematicsBuffer(self, layer):
        self.m_snapSchematicsBufferTool.setLayer(layer)

    def setLinesLayer(self, layer):
        self.m_snapLinesLayerTool.setLayer(layer)

    def setPolygonsLayer(self, layer):
        self.m_snapPolygonsLayerTool.setLayer(layer)

    def setSchematicsLayer(self, layer):
        self.m_snapSchematicsLayerTool.setLayer(layer)

    def linesLayerSnapSettingsChanged(self, layerId, enabled, snappingType, unitType, tolerance, avoidIntersections):
        self.linesSnappingToggled.emit(enabled)

    def polygonsLayerSnapSettingsChanged(self, layerId, enabled, snappingType, unitType, tolerance, avoidIntersections):
        self.polygonsSnappingToggled.emit(enabled)

    def schematicLayerSnapSettingsChanged(self, layerId, enabled, snappingType, unitType, tolerance, avoidIntersections):
        self.schematicSnappingToggled.emit(enabled)
