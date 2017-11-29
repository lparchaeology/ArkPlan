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

from PyQt4.QtCore import QFile, QSettings
from PyQt4.QtGui import QColor, QIcon

from qgis.core import QGis, QgsProject


class Project:

    @classmethod
    def exists(cls):
        return cls.fileInfo().exists()

    @staticmethod
    def fileInfo():
        return QgsProject.instance().fileInfo()

    @staticmethod
    def fileName():
        return QgsProject.instance().fileName()

    @staticmethod
    def filePath():
        return QgsProject.instance().homePath()

    @classmethod
    def dir(cls):
        return cls.fileInfo().dir()

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
