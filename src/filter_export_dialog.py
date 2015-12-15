# -*- coding: utf-8 -*-
"""
/***************************************************************************
                                ARK Spatial
                    A QGIS plugin for Archaeological Recording.
        Part of the Archaeological Recording Kit by L-P : Archaeology
                        http://ark.lparchaeology.com
                              -------------------
        begin                : 2014-12-07
        git sha              : $Format:%H$
        copyright            : 2014, 2015 by L-P : Heritage LLP
        email                : ark@lparchaeology.com
        copyright            : 2014, 2015 by John Layt
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

import os.path

from PyQt4 import uic
from PyQt4.QtCore import Qt
from PyQt4.QtGui import QDialog, QColor

from filter_export_dialog_base import *

class FilterExportDialog(QDialog, Ui_FilterExportDialog):

    def __init__(self, parent=None):
        super(FilterExportDialog, self).__init__(parent)

        self.setupUi(self)
        self.schematicColorTool.setAllowAlpha(True)
        self.schematicColorTool.setColorDialogTitle('Choose Schematic Color')
        self.schematicColorTool.setDefaultColor(QColor(165, 191, 221, 102))
        self.schematicColorTool.setToDefaultColor()
        self.schematicColorTool.setShowNoColor(True)

    def accept(self):
        return super(FilterExportDialog, self).accept()

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
