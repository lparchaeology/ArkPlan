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

from qgis.PyQt.QtGui import QColor
from qgis.PyQt.QtWidgets import QDialog

from .ui.filter_export_dialog_base import Ui_FilterExportDialog


class FilterExportDialog(QDialog, Ui_FilterExportDialog):

    def __init__(self, parent=None):
        super().__init__(parent)

        self.setupUi(self)
        self.schematicColorTool.setAllowAlpha(True)
        self.schematicColorTool.setColorDialogTitle('Choose Schematic Color')
        self.schematicColorTool.setDefaultColor(QColor(165, 191, 221, 102))
        self.schematicColorTool.setToDefaultColor()
        self.schematicColorTool.setShowNoColor(True)

    def accept(self):
        return super().accept()

    def setFilterSetName(self, name):
        self.filterSetNameEdit.setText(name)

    def setExportName(self, name):
        self.exportNameEdit.setText(name)

    def exportName(self):
        return self.exportNameEdit.text()

    def exportSchematic(self):
        return self.exportSchematicButton.isChecked()

    def exportData(self):
        return self.exportDataButton.isChecked()

    def schematicColor(self):
        return self.schematicColorTool.color()
