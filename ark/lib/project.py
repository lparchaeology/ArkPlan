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

from qgis.core import QgsProject


class Project:

    @staticmethod
    def fileInfo():
        return QgsProject.instance().fileInfo()

    @staticmethod
    def dir():
        return QgsProject.instance().fileInfo().dir()

    @staticmethod
    def exists():
        return QgsProject.instance().fileInfo().exists()

    @staticmethod
    def filePath():
        return QgsProject.instance().fileInfo().filePath()

    @staticmethod
    def fileName():
        return QgsProject.instance().fileName()

    @staticmethod
    def setFileName(filePath):
        return QgsProject.instance().setFileName(filePath)

    @staticmethod
    def title():
        return QgsProject.instance().title()

    @staticmethod
    def setTitle(title):
        return QgsProject.instance().setTitle(title)

    @staticmethod
    def homePath():
        return QgsProject.instance().homePath()

    @staticmethod
    def write():
        return QgsProject.instance().write()

    @staticmethod
    def clear():
        return QgsProject.instance().clear()

    @staticmethod
    def setEntry(scope, key, value, default=None):
        if (value is None or value == '' or value == default):
            return QgsProject.instance().removeEntry(scope, key)
        else:
            return QgsProject.instance().writeEntry(scope, key, value)

    @staticmethod
    def removeEntry(scope, key):
        return QgsProject.instance().removeEntry(scope, key)

    @staticmethod
    def writeEntry(scope, key, value):
        return QgsProject.instance().writeEntry(scope, key, value)

    @staticmethod
    def readEntry(scope, key, default=''):
        ret = QgsProject.instance().readEntry(scope, key, default)
        if ret is None or not ret[1]:
            return default
        else:
            return ret[0]

    @staticmethod
    def readNumEntry(scope, key, default=0):
        ret = QgsProject.instance().readNumEntry(scope, key, default)
        if ret is None or not ret[1]:
            return default
        else:
            return ret[0]

    @staticmethod
    def readDoubleEntry(scope, key, default=0.0):
        ret = QgsProject.instance().readDoubleEntry(scope, key, default)
        if ret is None or not ret[1]:
            return default
        else:
            return ret[0]

    @staticmethod
    def readBoolEntry(scope, key, default=False):
        ret = QgsProject.instance().readBoolEntry(scope, key, default)
        if ret is None or not ret[1]:
            return default
        else:
            return ret[0]

    @staticmethod
    def readListEntry(scope, key, default=[]):
        ret = QgsProject.instance().readListEntry(scope, key, default)
        if ret is None or not ret[1]:
            return default
        else:
            return ret[0]
