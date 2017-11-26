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

from qgis.core import QGis, QgsApplication, QgsCoordinateReferenceSystem


class Application:

    @staticmethod
    def serverUrl():
        return QSettings().value("/ARK/Server/url", "")

    @staticmethod
    def setServerUrl(url):
        QSettings().setValue("/ARK/Server/url", url)

    @staticmethod
    def serverUser():
        return QSettings().value("/ARK/Server/user", "")

    @staticmethod
    def serverPassword():
        return QSettings().value("/ARK/Server/password", "")

    @staticmethod
    def setServerCredentials(user, password):
        QSettings().setValue("/ARK/Server/user", user)
        QSettings().setValue("/ARK/Server/password", password)

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

    @classmethod
    def projectDefaultCrs(cls):
        return QgsCoordinateReferenceSystem(cls.projectDefaultCrsId())

    @staticmethod
    def projectDefaultCrsId():
        return QSettings().value("/Projections/projectDefaultCrs", "EPSG:4326")

    @classmethod
    def layerDefaultCrs(cls):
        return QgsCoordinateReferenceSystem(cls.layerDefaultCrsId())

    @staticmethod
    def layerDefaultCrsId():
        return QSettings().value("/Projections/layerDefaultCrs", "EPSG:4326")

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
