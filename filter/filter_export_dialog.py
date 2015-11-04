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

import os.path

from PyQt4 import uic
from PyQt4.QtCore import Qt
from PyQt4.QtGui import QDialog

from filter_export_dialog_base import *

class FilterExportDialog(QDialog, Ui_FilterExportDialog):

    def __init__(self, parent=None):
        super(FilterExportDialog, self).__init__(parent)

        self.setupUi(self)

    def accept(self):
        return super(FilterExportDialog, self).accept()

    def setName(self, name):
        self.filterSetNameEdit.setText(name)

    def name(self):
        return self.filterSetNameEdit.text()

    def saveFilterSet(self):
        return self.saveFilterSetButton.isChecked()

    def exportSchematic(self):
        return self.exportSchematicButton.isChecked()

    def exportData(self):
        return self.exportDataButton.isChecked()
