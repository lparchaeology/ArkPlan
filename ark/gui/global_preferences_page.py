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

import os

from qgis.PyQt.QtWidgets import QWizardPage

from qgis.gui import QgsProjectionSelectionWidget

from ArkSpatial.ark.lib import Application, utils
from ArkSpatial.ark.lib.snapping import Snapping


class GlobalPreferencesPage(QWizardPage):

    def __init__(self, parent=None):
        super(GlobalPreferencesPage, self).__init__(parent)

    def initializePage(self, parent=None):
        self.registerField("forceDefaultCrs", self.wizard().forceCrsCheck)
        self.registerField("forceOtfTransform", self.wizard().forceOtfCheck)
        self.registerField("font", self.wizard().fontCombo)
        self.registerField("snappingTolerance", self.wizard().snappingToleranceSpin)
        self.registerField("snappingUnit", self.wizard().snappingUnitCombo)

        self.wizard().crsWidget.setOptionVisible(QgsProjectionSelectionWidget.ProjectCrs, False)
        self.wizard().crsWidget.setOptionVisible(QgsProjectionSelectionWidget.DefaultCrs, True)
        self.wizard().crsWidget.setOptionVisible(QgsProjectionSelectionWidget.CurrentCrs, True)
        self.wizard().crsWidget.setCrs(Application.layerDefaultCrs())

        self.wizard().forceCrsCheck.setChecked(True)
        self.wizard().forceOtfCheck.setChecked(True)

        self.wizard().snappingToleranceSpin.setValue(10.0)

        self.wizard().snappingUnitCombo.addItem('Pixels', Snapping.Pixels)
        self.wizard().snappingUnitCombo.addItem('Layer Units', Snapping.LayerUnits)
        self.wizard().snappingUnitCombo.addItem('Project Units', Snapping.ProjectUnits)
        self.wizard().snappingUnitCombo.setCurrentIndex(0)

    def crs(self):
        return self.wizard().crsWidget.crs()

    def forceDefaultCrs(self):
        return self.wizard().forceCrsCheck.isChecked()

    def forceOtfTransform(self):
        return self.wizard().forceOtfCheck.isChecked()

    def font(self):
        return self.wizard().fontCombo.currentFont()

    def snappingTolerance(self):
        return self.wizard().snappingToleranceSpin.value()

    def snappingUnit(self):
        return self.wizard().snappingUnitCombo.itemData(self.wizard().snappingUnitCombo.currentIndex())
