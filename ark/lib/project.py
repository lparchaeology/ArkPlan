# -*- coding: utf-8 -*-
"""
/***************************************************************************
                                ARK QGIS
                        A QGIS utilities library.
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

from PyQt4.QtCore import QFile, QSettings
from PyQt4.QtGui import QColor, QIcon

from qgis.core import QGis, QgsApplication, QgsProject


class Project:

    @staticmethod
    def getThemeIcon(iconName):
        iconName = '/' + iconName
        if QFile.exists(QgsApplication.activeThemePath() + iconName):
            return QIcon(QgsApplication.activeThemePath() + iconName)
        elif QFile.exists(QgsApplication.defaultThemePath() + iconName):
            return QIcon(QgsApplication.defaultThemePath() + iconName)
        else:
            themePath = ':/icons/' + QSettings().value('/Themes', '', str) + iconName
            if QFile.exists(themePath):
                return QIcon(themePath)
            else:
                return QIcon(':/icons/default' + iconName)

    @staticmethod
    def crs(iface):
        return iface.mapCanvas().mapSettings().destinationCrs()

    @staticmethod
    def highlightColorName():
        return QColor(QSettings().value('/Map/highlight/color', QGis.DEFAULT_HIGHLIGHT_COLOR.name(), str))

    @staticmethod
    def highlightColorAlpha():
        return QSettings().value('/Map/highlight/colorAlpha', QGis.DEFAULT_HIGHLIGHT_COLOR.alpha(), int)

    @classmethod
    def highlightLineColor(cls):
        color = QColor(cls.highlightColorName())
        return color

    @classmethod
    def highlightFillColor(cls):
        color = QColor(cls.highlightColorName())
        color.setAlpha(cls.highlightColorAlpha())
        return color

    @staticmethod
    def highlightBuffer():
        return QSettings().value('/Map/highlight/buffer', QGis.DEFAULT_HIGHLIGHT_BUFFER_MM, float)

    @staticmethod
    def highlightMinimumWidth():
        return QSettings().value('/Map/highlight/minWidth', QGis.DEFAULT_HIGHLIGHT_MIN_WIDTH_MM, float)

    @staticmethod
    def filePath():
        return QgsProject.instance().fileinfo().canonicalFilePath()

    @staticmethod
    def setEntry(scope, key, value, default=None):
        if (value == None or value == '' or value == default):
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
