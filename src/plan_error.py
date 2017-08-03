# -*- coding: utf-8 -*-
"""
/***************************************************************************
                                ARK Spatial
                    A QGIS plugin for Archaeological Recording.
        Part of the Archaeological Recording Kit by L-P : Archaeology
                        http://ark.lparchaeology.com
                              -------------------
        copyright            : 2017 by L-P : Heritage LLP
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

from PyQt4 import uic
from PyQt4.QtCore import Qt
from PyQt4.QtGui import QDialog, QApplication

from ..libarkqgis import utils
from ..libarkqgis.models import TableModel

from feature import Feature

from error_dialog_base import *

class PlanError:

    layer = ''
    row = -1
    fid = -1
    feature = Feature()
    field = ''
    message = ''
    ignore = False

    def toDict(self):
        d = {}
        d['layer'] = self.layer
        d['row'] = self.row
        d['fid'] = self.fid
        d['feature'] = self.feature
        d['field'] = self.field
        d['message'] = self.message
        return d

    def toCsv(self):
        return utils.doublequote(self.layer) + ',' + str(self.row) + ',' + utils.doublequote(self.field) + ',' + utils.doublequote(self.message)

    def toText(self):
        return str(self.layer).ljust(20) + str(self.row).rjust(5) + '   ' + str(self.field).ljust(20) + str(self.message)

    def log(self):
        return str(self.layer) + ' : ' + str(self.row) + ' : ' + str(self.field) + ' : ' + str(self.message)


class ErrorDialog(QDialog, Ui_ErrorDialog):

    _errors = []
    _model = None  # TableModel()
    _ignore = False

    def __init__(self, parent=None):
        super(ErrorDialog, self).__init__(parent)
        self.setupUi(self)
        self.okButton.clicked.connect(self.accept)
        self.ignoreButton.clicked.connect(self._ignore)
        self.copyButton.clicked.connect(self._toText)
        self.csvButton.clicked.connect(self._toCsv)

        fields = ['layer', 'row', 'field', 'message']
        nullRecord = {'layer' : '', 'row' : 0, 'field' : '', 'message' : ''}
        self._model = TableModel(fields, nullRecord)

    def loadErrors(self, errors):
        self._ignore = False
        self._errors = errors
        self._model.clear()
        for error in errors:
            self._model.appendRecord(error.toDict())
            if not error.ignore:
                self.ignoreButton.setEnabled(False)
        self.errorTable.setModel(self._model)
        self.errorTable.resizeColumnsToContents()

    def ignoreErrors(self):
        return self._ignore

    def _ignore(self):
        self._ignore = True
        self.accept()

    def _toText(self):
        txt = ''
        for error in self._errors:
            txt += error.toText() + '\n'
        QApplication.clipboard().setText(txt)
        self.accept()

    def _toCsv(self):
        csv = ''
        for error in self._errors:
            csv += error.toCsv() + '\n'
        QApplication.clipboard().setText(csv)
        self.accept()
