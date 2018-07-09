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

import csv
from io import open

from qgis.PyQt.QtCore import QFile

from ArkSpatial.ark.lib.core import TableModel

from ArkSpatial.ark.core import Item


class ItemModel(TableModel):

    def __init__(self, filePath, keyFields, parent=None):
        super().__init__(parent)

        if QFile.exists(filePath):
            with open(filePath) as csvFile:
                reader = csv.DictReader(csvFile)
                self._fields = reader.fieldnames
                self._nullRecord = {}
                for field in self._fields:
                    self._nullRecord[field] = ''
                for record in reader:
                    item = Item(record[keyFields.siteCode], record[keyFields.classCode], record[keyFields.itemId])
                    self._addItem(item, record)

    def getItem(self, item):
        return self.getRecord('item', item)

    def _addItem(self, item, itemRecord):
        record = {}
        record.update(self._nullRecord)
        record.update({'item': item})
        record.update(itemRecord)
        self._table.append(record)
