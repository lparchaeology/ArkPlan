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

from .table_model import TableModel


class ParentChildModel(TableModel):

    def __init__(self, parent=None):
        super(TableModel, self).__init__(parent)
        self._fields = ['parent', 'child']
        self._nullRecord = {'parent': None, 'child': None}

    def addChild(self, parent, child):
        self.deleteRecords('child', child)
        record = {'parent': parent, 'child': child}
        self._table.append(record)

    def getChildren(self, parent):
        children = []
        for record in self._table:
            if record['parent'] == parent:
                children.append(record['child'])
        return children

    def getParent(self, child):
        for record in self._table:
            if record['child'] == child:
                return record['parent']
        return None
