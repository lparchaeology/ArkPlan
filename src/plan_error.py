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

from PyQt4 import uic
from PyQt4.QtCore import Qt
from PyQt4.QtGui import QDialog

from ..libarkqgis.models import TableModel

from plan_item import ItemFeature

from error_dialog_base import *

class PlanError:

    layer = ''
    row = -1
    fid = -1
    feature = ItemFeature()
    field = ''
    message = ''

    def toDict(self):
        d = {}
        d['layer'] = self.layer
        d['row'] = self.row
        d['fid'] = self.fid
        d['feature'] = self.feature
        d['field'] = self.field
        d['message'] = self.message
        return d

    def log(self):
        return str(self.layer) + ' : ' + str(self.row) + ' : ' + str(self.field) + ' : ' + str(self.message)


class ErrorDialog(QDialog, Ui_ErrorDialog):

    _model = None  # TableModel()

    def __init__(self, parent=None):
        super(ErrorDialog, self).__init__(parent)
        self.setupUi(self)
        fields = ['layer', 'row', 'field', 'message']
        nullRecord = {'layer' : '', 'row' : 0, 'field' : '', 'message' : ''}
        self._model = TableModel(fields, nullRecord)

    def loadErrors(self, errors):
        self._model.clear()
        for error in errors:
            self._model.appendRecord(error.toDict())
        self.errorTable.setModel(self._model)
        self.errorTable.resizeColumnsToContents()
