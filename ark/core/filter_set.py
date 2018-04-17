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

import copy

from PyQt4.QtCore import QSettings

from ArkSpatial.ark.core import Config, FilterClause

from .filter_type import FilterType


class FilterSet():

    def __init__(self):
        self.key = ''
        self.name = ''
        self.source = ''  # qgis, ark
        self.status = ''  # created/loaded/edited/?
        self.expression = ''
        self.selection = ''
        self._clauses = []  # [Item()]
        self._group = ''
        self._plugin = None  # Plugin()

    def __str__(self):
        return ('FilterSet('
                + str(self.key) + ', '
                + str(self.name) + ', '
                + str(self.source) + ', '
                + str(self.status) + ', '
                + str(self.expression) + ')')

    def debug(self, showClauses=False):
        if showClauses:
            ret = str(self) + '\n'
            for clause in self._clauses:
                ret += '    ' + str(clause) + '\n'
            return ret
        return str(self)

    def clauses(self):
        self.loadClauses()
        return self._clauses

    def setClauses(self, clauses):
        self._clauses = copy.deepcopy(clauses)
        if self.status == 'created':
            self.status = 'loaded'
        else:
            self.status = 'edited'
        self._generateFilters()

    def addClause(self, clause):
        self._clauses.append(copy.deepcopy(clause))
        if self.status == 'created':
            self.status = 'loaded'
        else:
            self.status = 'edited'
        self._generateFilters()

    def clearClauses(self):
        self._clauses = []
        self.expression = ''
        self.selection = ''
        self.status = 'created'

    def loadClauses(self):
        if self.status == 'loaded' or self.status == 'edited':
            return
        self.reloadClauses()

    def reloadClauses(self):
        self.clearClauses()
        if self.source == 'qgis':
            self._loadSettings()
        elif self.source == 'ark':
            self._loadArk()
        self._generateFilters()

    def save(self):
        if self.source == 'qgis':
            self._saveSettings()

    def delete(self):
        if self.source == 'qgis':
            self._deleteSettings()

    def _deleteSettings(self):
        settings = QSettings()
        settings.remove(self._group)
        self.clearClauses()
        self.status = ''

    def _saveSettings(self):
        settings = QSettings()
        settings.remove(self._group)
        settings.setValue(self._group + '/' + 'Name', self.name)
        settings.beginWriteArray(self._group)
        i = 0
        for clause in self._clauses:
            settings.setArrayIndex(i)
            clause.saveSettings(settings)
            i += 1
        settings.endArray()
        self.status = 'loaded'

    def _loadSettings(self):
        settings = QSettings()
        x = settings.beginReadArray(self._group)
        if x > 0:
            for i in range(0, x):
                settings.setArrayIndex(i)
                clause = FilterClause.fromSettings(settings)
                self._clauses.append(clause)
            self.status = 'loaded'
        settings.endArray()

    def _loadArk(self):
        items = self._plugin.data().getFilterItems(self._group)
        siteItems = {}
        for item in items:
            if item.siteCode not in siteItems:
                siteItems[item.siteCode] = {}
            if item.classCode() not in siteItems[item.siteCode()]:
                siteItems[item.siteCode()][item.classCode()] = []
            siteItems[item.siteCode()][item.classCode()].append(item)
        for siteCode in siteItems:
            for classCode in siteItems[siteCode]:
                if Config.classCodes[classCode]['plan'] or Config.classCodes[classCode]['group']:
                    clause = FilterClause.fromItems(siteItems[siteCode][classCode])
                    self._clauses.append(clause)
        self.status = 'loaded'

    def _generateFilters(self):
        if self.status != 'loaded' and self.status != 'edited':
            return
        excludeString = ''
        firstInclude = True
        includeString = ''
        firstExclude = True
        selectString = ''
        firstSelect = True
        for clause in self._clauses:
            filterItem = self._plugin.data().nodesItem(clause.key)
            if clause.action == FilterType.Select:
                if firstSelect:
                    firstSelect = False
                else:
                    selectString += ' or '
                selectString += filterItem.filterClause()
            elif clause.action == FilterType.Exclude:
                if firstExclude:
                    firstExclude = False
                else:
                    excludeString += ' or '
                excludeString += filterItem.filterClause()
            elif clause.action == FilterType.Include:
                if firstInclude:
                    firstInclude = False
                else:
                    includeString += ' or '
                includeString += filterItem.filterClause()
        if includeString and excludeString:
            self.expression = '(' + includeString + ') and NOT (' + excludeString + ')'
        elif excludeString:
            self.expression = 'NOT (' + excludeString + ')'
        else:
            self.expression = includeString
        self.selection = selectString

    @staticmethod
    def fromSettings(plugin, path, key):
        fs = FilterSet()
        fs._plugin = plugin
        fs._group = path + '/' + key
        fs.key = key
        fs.name = QSettings().value(fs._group + '/Name')
        fs.source = 'qgis'
        fs.status = 'created'
        return fs

    @staticmethod
    def fromArk(plugin, key, name):
        fs = FilterSet()
        fs._plugin = plugin
        fs._group = key
        fs.key = 'ark_' + str(key)
        fs.name = name
        fs.source = 'ark'
        fs.status = 'created'
        return fs

    @staticmethod
    def fromSchematic(plugin):
        fs = FilterSet()
        fs._plugin = plugin
        fs._group = 'schematic'
        fs.key = 'schematic'
        fs.name = 'schematic'
        fs.source = 'schematic'
        fs.status = 'created'
        return fs

    @staticmethod
    def fromName(plugin, path, key, name):
        fs = FilterSet()
        fs._plugin = plugin
        fs._group = path + '/' + key
        fs.key = key
        fs.name = name
        fs.source = 'qgis'
        fs.status = 'created'
        return fs
