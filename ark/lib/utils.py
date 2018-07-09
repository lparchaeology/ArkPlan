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

from qgis.PyQt.QtCore import QDateTime, QRectF, QRegExp, Qt

from qgis.core import NULL, Qgis, QgsFeature, QgsFeatureRequest, QgsGeometry, QgsMessageLog, QgsPointXY, QgsPointV2

safeChars = [
    " ",
    ".",
    ",",
    "_",
    "-",
    "(",
    ")"
]

replaceChars = {
    "&": "and",
    "[": "(",
    "]": ")",
    "{": "(",
    "}": ")",
    ":": "-",
    "/": "-",
    "\\": "-"
}

escapedChars = {
    "&amp;": "&"
}


def safeFilename(name):
    if name is None or name == "":
        return ""
    safe = []
    for escape, char in escapedChars.items():
        name = name.replace(escape, char)
    for char in name:
        if char.isalpha() or char.isdigit() or char in safeChars:
            safe.append(char)
        elif char in replaceChars:
            safe.append(replaceChars[char])
    safe = "".join(safe).strip()
    return safe


def bound(minVal, val, maxVal):
    return max(min(val, maxVal), minVal)


def timestamp():
    return QDateTime.currentDateTimeUtc().toString(Qt.ISODate)


def printable(val):
    if val is None or val == NULL:
        return str(val)
    if val == '':
        return '<EMPTY>'
    if type(val) == str:
        return doublequote(val)
    if type(val) == QRectF:
        return 'QRectF(' + str(val.x()) + ', ' + str(val.y()) + ', ' + str(val.width()) + ', ' + str(val.height()) + ')'
    if type(val) == QgsPointXY:
        return 'QgsPointXY(' + str(val.x()) + ', ' + str(val.y()) + ')'
    if type(val) == QgsPointV2:
        return 'QgsPointV2(' + str(val.x()) + ', ' + str(val.y()) + ')'
    if type(val) == QgsGeometry:
        return 'QgsGeometry(' + val.exportToGeoJSON() + ')'
    if type(val) == QgsFeature:
        return 'QgsFeature(' + str(val.id()) + ')'
    if type(val) == QgsFeatureRequest:
        return 'QgsFeatureRequest(' + val.filterExpression().dump() + ')'
    return str(val).strip()


def string(val):
    if val is None or val == NULL:
        return ''
    return str(val).strip()


def strip(value):
    if isinstance(value, str):
        value = value.strip()
        if value == '':
            return None
    return value


def quote(val):
    return "'" + str(val) + "'"


def doublequote(val):
    return '"' + str(val) + '"'


def csv(values):
    return ','.join(csvValue(value) for value in values)


def csvValue(value):
    if isinstance(value, str):
        return doublequote(value)
    else:
        return str(value)


def unitToSuffix(unit):
    if unit == Qgis.Meters:
        return ' m'
    elif unit == Qgis.Feet:
        return ' ft'
    elif unit == Qgis.NauticalMiles:
        return ' NM'
    else:
        return ' °'


def eqClause(field, value):
    return doublequote(field) + ' = ' + quote(value)


def neClause(field, value):
    return doublequote(field) + ' != ' + quote(value)


def natsorted(l):
    return sorted(l, key=lambda item: (int(item.partition(' ')[0]) if item[0].isdigit() else float('inf'), item))


def rangeToList(valueRange):
    lst = []
    for clause in valueRange.split():
        if clause.find('-') >= 0:
            valueList = clause.split('-')
            for i in range(int(valueList[0]), int(valueList[1])):
                lst.append(i)
        else:
            lst.append(int(clause))
    return sorted(lst)


def listToRange(valueList):
    valueRange = ''
    if len(valueList) == 0:
        return valueRange
    inList = natsorted(set(valueList))
    prev = inList[0]
    start = prev
    for this in inList[1:]:
        if int(this) != int(prev) + 1:
            if prev == start:
                valueRange = valueRange + ' ' + str(prev)
            else:
                valueRange = valueRange + ' ' + str(start) + '-' + str(prev)
            start = this
        prev = this
    if prev == start:
        valueRange = valueRange + ' ' + str(prev)
    else:
        valueRange = valueRange + ' ' + str(start) + '-' + str(this)
    return valueRange


def listToRegExp(lst):
    if (len(lst) < 1):
        return QRegExp()
    exp = str(lst[0])
    if (len(lst) > 1):
        for element in lst[1:]:
            exp = exp + '|' + str(element)
    return QRegExp('\\b(' + exp + ')\\b')


def debug(msg, group='Debug'):
    if isinstance(msg, str):
        QgsMessageLog.logMessage(msg, group, QgsMessageLog.INFO)
    else:
        QgsMessageLog.logMessage(printable(msg), group, QgsMessageLog.INFO)


def dump(msg, group='Debug'):
    debug(msg, group)


def isEmpty(value):
    return value is None or value == NULL or (isinstance(value, str) and (value.strip() == ''))


def featureRequest(expr):
    request = QgsFeatureRequest()
    request.setFilterExpression(expr)
    return request
