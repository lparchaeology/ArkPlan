# -*- coding: utf-8 -*-
"""
/***************************************************************************
                                ARK Spatial
                    A QGIS plugin for Archaeological Recording.
        Part of the Archaeological Recording Kit by L-P : Archaeology
                        http://ark.lparchaeology.com
                              -------------------
        begin                : 2016-06-01
        git sha              : $Format:%H$
        copyright            : 2016 by L-P : Heritage LLP
        email                : ark@lparchaeology.com
        copyright            : 2016 by John Layt
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
import re, copy

from PyQt4.QtCore import QSettings
from PyQt4.QtGui import QColor

from ..libarkqgis import utils
from ..libarkqgis.project import Project

from config import Config
from plan_item import ItemKey

class FilterType():
    IncludeFilter = 0
    ExcludeFilter = 1
    SelectFilter = 2
    HighlightFilter = 3

    @classmethod
    def name(self, filterType):
        if (filterType == FilterType.IncludeFilter):
            return 'Include'
        elif (filterType == FilterType.ExcludeFilter):
            return 'Exclude'
        elif (filterType == FilterType.SelectFilter):
            return 'Select'
        elif (filterType == FilterType.HighlightFilter):
            return 'Highlight'
        else:
            return 'Invalid'

class FilterWidgetAction():
    AddFilter = 0
    RemoveFilter = 1
    LockFilter = 2

class FilterClause():

    key = ItemKey()
    action = FilterType.IncludeFilter
    color = Project.highlightLineColor()
    _viewIdx = -1

    def __str__(self):
        return 'FilterClause(' + FilterType.name(self.action) + ', ' + str(self.key.siteCode) + ', ' +  str(self.key.classCode) + ', ' +  str(self.key.itemId) + ', ' + self.color.name() + ')'

    def debug(self):
        return 'FilterClause(' + FilterType.name(self.action) + ', ' + utils.printable(self.key.siteCode) + ', ' +  utils.printable(self.key.classCode) + ', ' +  utils.printable(self.key.itemId) + ', ' + self.color.name() + ')'

    def lineColor(self):
        color = QColor(self.color) # force deep copy
        color.setAlpha(255)
        return color

    def saveSettings(self, settings):
        settings.setValue('filterType', self.action)
        settings.setValue('siteCode', self.key.siteCode)
        settings.setValue('classCode', self.key.classCode)
        settings.setValue('filterRange', self.key.itemId)
        if self.color.isValid():
            settings.setValue('highlightColor', self.color)

    def loadSettings(self, settings):
        utils.logMessage(str(settings.childKeys()))
        self.action = int(settings.value('filterType', 0))
        siteCode = settings.value('siteCode', '')
        classCode = settings.value('classCode', '')
        filterRange = settings.value('filterRange', '')
        utils.logMessage('siteCode = ' + siteCode)
        utils.logMessage('classCode = ' + classCode)
        utils.logMessage('filterRange = ' + filterRange)
        self.key = ItemKey(siteCode, classCode, filterRange)
        if settings.contains('highlightColor'):
            self.color = settings.value('highlightColor', QColor)

    def loadItems(self, items):
        self.key = items[0]
        ids = []
        for item in items:
            if (item.siteCode == self.key.siteCode and item.classCode == self.key.classCode):
                ids.append(item.itemId)
        self.key.setItemId(sorted(ids))

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


class FilterSet():

    key = ''
    name = ''
    source = '' # qgis, ark
    status = '' # created/loaded/edited/?
    expression = ''
    selection = ''
    _clauses = [] # [ItemKey()]
    _group = ''
    _project = None  # Project()

    def __str__(self):
        return 'FilterSet(' + str(self.key) + ', ' + str(self.name) + ', ' +  str(self.source) + ', ' +  str(self.status) + ', ' + str(self.expression) + ')'

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
        self._project.logMessage(self._group + ' = ' + str(x))
        self._project.logMessage(str(settings.childKeys()))
        if x > 0:
            for i in range(0, x):
                settings.setArrayIndex(i)
                self._project.logMessage(str(settings.childKeys()))
                clause = FilterClause.fromSettings(settings)
                self._clauses.append(clause)
            self.status = 'loaded'
        settings.endArray()

    def _loadArk(self):
        items = self._project.data.getFilterItems(self._group)
        siteItems = {}
        for item in items:
            if item.siteCode not in siteItems:
                siteItems[item.siteCode] = {}
            if item.classCode not in siteItems[item.siteCode]:
                siteItems[item.siteCode][item.classCode] = []
            siteItems[item.siteCode][item.classCode].append(item)
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
            filterItemKey = self._project.data.nodesItemKey(clause.key)
            if clause.action == FilterType.SelectFilter:
                if firstSelect:
                    firstSelect = False
                else:
                    selectString += ' or '
                selectString += filterItemKey.filterClause()
            elif clause.action == FilterType.ExcludeFilter:
                if firstExclude:
                    firstExclude = False
                else:
                    excludeString += ' or '
                excludeString += filterItemKey.filterClause()
            elif clause.action == FilterType.IncludeFilter:
                if firstInclude:
                    firstInclude = False
                else:
                    includeString += ' or '
                includeString += filterItemKey.filterClause()
        if includeString and excludeString:
            self.expression = '(' + includeString + ') and NOT (' + excludeString + ')'
        elif excludeString:
            self.expression = 'NOT (' + excludeString + ')'
        else:
            self.expression = includeString
        self.selection = selectString

    @staticmethod
    def fromSettings(project, path, key):
        fs = FilterSet()
        fs._project = project
        fs._group = path + '/' + key
        fs.key = key
        fs.name = QSettings().value(fs._group + '/Name')
        fs.source = 'qgis'
        fs.status = 'created'
        return fs

    @staticmethod
    def fromArk(project, key, name):
        fs = FilterSet()
        fs._project = project
        fs._group = key
        fs.key = 'ark_' + str(key)
        fs.name = name
        fs.source = 'ark'
        fs.status = 'created'
        return fs

    @staticmethod
    def fromSchematic(project):
        fs = FilterSet()
        fs._project = project
        fs._group = 'schematic'
        fs.key = 'schematic'
        fs.name = 'schematic'
        fs.source = 'schematic'
        fs.status = 'created'
        return fs

    @staticmethod
    def fromName(project, path, key, name):
        fs = FilterSet()
        fs._project = project
        fs._group = path + '/' + key
        fs.key = key
        fs.name = name
        fs.source = 'qgis'
        fs.status = 'created'
        return fs
