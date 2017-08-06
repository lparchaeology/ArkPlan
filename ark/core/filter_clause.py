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

import copy

from PyQt4.QtGui import QColor

from ark.lib import Project, utils

from ark.core import FilterType, Item


class FilterClause():

    item = Item()
    action = FilterType.IncludeFilter
    color = Project.highlightLineColor()
    _viewIdx = -1

    def __str__(self):
        return ('FilterClause('
                + FilterType.name(self.action) + ', '
                + str(self.item.siteCode()) + ', '
                + str(self.item.classCode()) + ', '
                + str(self.item.itemId()) + ', '
                + self.color.name() + ')')

    def debug(self):
        return ('FilterClause('
                + FilterType.name(self.action) + ', '
                + utils.printable(self.item.siteCode()) + ', '
                + utils.printable(self.item.classCode()) + ', '
                + utils.printable(self.item.itemId()) + ', '
                + self.color.name() + ')')

    def lineColor(self):
        color = QColor(self.color)  # force deep copy
        color.setAlpha(255)
        return color

    def saveSettings(self, settings):
        settings.setValue('filterType', self.action)
        settings.setValue('siteCode', self.item.siteCode())
        settings.setValue('classCode', self.item.classCode())
        settings.setValue('filterRange', self.item.itemId())
        if self.color.isValid():
            settings.setValue('highlightColor', self.color)

    def loadSettings(self, settings):
        self.action = int(settings.value('filterType', 0))
        siteCode = settings.value('siteCode', '')
        classCode = settings.value('classCode', '')
        filterRange = settings.value('filterRange', '')
        self.item = Item(siteCode, classCode, filterRange)
        if settings.contains('highlightColor'):
            self.color = settings.value('highlightColor', QColor)

    def loadItems(self, items):
        self.item = items[0]
        ids = []
        for item in items:
            if (item.siteCode() == self.item.siteCode() and item.classCode() == self.item.classCode()):
                ids.append(item.itemId())
        self.item.setItemId(sorted(ids))

    @staticmethod
    def fromSettings(settings):
        clause = FilterClause()
        clause.loadSettings(settings)
        return clause

    @staticmethod
    def fromItems(items):
        clause = FilterClause()
        clause.loadItems(items)
        return clause
