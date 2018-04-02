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

from PyQt4.QtGui import QApplication, QDialog

from .. import utils
from ..core import TableModel
from .ui.table_dialog_base import Ui_TableDialog


class TableDialog(QDialog, Ui_TableDialog):

    def __init__(self, title, text, fields, nullRecord, parent=None):
        super(TableDialog, self).__init__(parent)
        self.setupUi(self)

        self._fields = []
        self._nullRecord = {}
        self._model = None  # TableModel()

        self.setWindowTitle(title)
        self.label.setText(text)

        self._fields = fields
        self._nullRecord = nullRecord
        self._model = TableModel(fields, nullRecord)
        self.dataTable.setModel(self._model)

        self.okButton.clicked.connect(self.accept)
        self.csvButton.clicked.connect(self._toCsv)

    def tableModel(self):
        return self._model

    def clear(self):
        self._model.clear()

    def setRows(self, rows):
        self.clear()
        self.addRows(rows)

    def addRows(self, rows):
        for row in rows:
            self._model.appendRecord(row)
        self.dataTable.resizeColumnsToContents()

    def addRow(self, row):
        self._model.appendRecord(row)
        self.dataTable.resizeColumnsToContents()

    def toCsv(self):
        csv = utils.csv(self._fields) + '\n'
        rows = self._model.getList()
        for row in rows:
            vals = []
            for field in self._fields:
                vals.append(row[field])
            csv += utils.csv(vals) + '\n'
        return csv

    def _toCsv(self):
        QApplication.clipboard().setText(self.toCsv())
        self.accept()
