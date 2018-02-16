# -*- coding: utf-8 -*-
"""
/***************************************************************************
                                ARKspatial
                    A QGIS plugin for Archaeological Recording.
        Part of the Archaeological Recording Kit by L - P : Archaeology
                        http://ark.lparchaeology.com
                              -------------------
        copyright            : 2017 by L - P : Heritage LLP
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

from PyQt4.QtCore import pyqtSignal

from ArkSpatial.ark.lib.gui import ToolDockWidget

from .trench_widget import TrenchWidget


class TrenchDock(ToolDockWidget):

    drawTrenchSelected = pyqtSignal()
    generateTrenchSelected = pyqtSignal()
    exportTrenchSelected = pyqtSignal()

    sampleChanged = pyqtSignal()
    sampleAreaChanged = pyqtSignal(str)
    samplePercentChanged = pyqtSignal(float)
    trenchWidthChanged = pyqtSignal(float)
    trenchLengthChanged = pyqtSignal(float)

    def __init__(self, parent=None):
        super(TrenchDock, self).__init__(TrenchWidget(), parent)

        self.setWindowTitle(u'ARK Trench')
        self.setObjectName(u'TrenchDock')

    def initGui(self, iface, location, menuAction):
        super(TrenchDock, self).initGui(iface, location, menuAction)

        self._drawTrenchAction = self.addToolbarAction(
            ':/plugins/ark/trench/draw.svg',
            'Draw Trench',
            self.drawTrenchSelected
        )

        self._generateTrenchAction = self.addToolbarAction(
            ':/plugins/ark/trench/generate.svg',
            'Generate Trenches',
            self.generateTrenchSelected
        )

        self._exportTrenchAction = self.addToolbarAction(
            ':/plugins/ark/trench/export.svg',
            'Export Trenches',
            self.exportTrenchSelected
        )

        self.widget.areaCombo.currentIndexChanged.connect(self.sampleChanged)
        self.widget.areaCombo.currentIndexChanged.connect(self._areaChanged)
        self.widget.samplePercentSpin.valueChanged.connect(self.sampleChanged)
        self.widget.samplePercentSpin.valueChanged.connect(self.samplePercentChanged)
        self.widget.widthSpin.valueChanged.connect(self.sampleChanged)
        self.widget.widthSpin.valueChanged.connect(self.trenchWidthChanged)
        self.widget.lengthSpin.valueChanged.connect(self.sampleChanged)
        self.widget.lengthSpin.valueChanged.connect(self.trenchLengthChanged)

    def unloadGui(self):
        pass

    def loadProject(self, plugin):
        self.areaCombo.clear()
        for area in []:
            self.areaCombo.addItem(area, area)

    def closeProject(self):
        pass

    def setArea(self, id, size):
        idx = self.areaCombo.findData(id)
        if idx >= 0:
            self.areaCombo.setCurrentIndex(idx)
        self.widget.areaSpin.setValue(size)

    def samplePercent(self):
        return self.widget.samplePercentSpin.value()

    def setSamplePercent(self, percent):
        self.widget.samplePercentSpin.setValue(percent)

    def trenchWidth(self):
        return self.widget.widthSpin.value()

    def setTrenchWidth(self, width):
        self.widget.widthSpin.setValue(width)

    def trenchLength(self):
        return self.widget.lengthSpin.value()

    def setTrenchLength(self, length):
        self.widget.lengthSpin.setValue(length)

    def setResult(self, count, length, area):
        self.widget.sampleCountSpin.setValue(count)
        self.widget.sampleLengthSpin.setValue(count)
        self.widget.sampleAreaSpin.setValue(count)

    def _areaChanged(self, idx):
        self.sampleAreaChanged.emit(self.widget.areaCombo.itemData(idx))
