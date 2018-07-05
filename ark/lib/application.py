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

from qgis.PyQt.QtCore import QFile, QSettings
from qgis.PyQt.QtGui import QColor, QIcon

from qgis.core import NULL, Qgis, QgsApplication, QgsCoordinateReferenceSystem, QgsCRSCache

from . import utils


class Application:

    @staticmethod
    def readEntry(scope, key, default=""):
        value = QSettings().value("/" + scope + "/" + key, default)
        if value == NULL:
            return None
        return value

    @staticmethod
    def setEntry(scope, key, value):
        QSettings().setValue("/" + scope + "/" + key, value)

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
    def projectDefaultCrs():
        return QgsCRSCache.instance().crsByOgcWmsCrs(Application.projectDefaultCrsAuthid())

    @staticmethod
    def projectDefaultCrsAuthid():
        return QSettings().value("/Projections/projectDefaultCrs", "EPSG:4326")

    @staticmethod
    def setProjectDefaultCrs(crs):
        QSettings().setValue("/Projections/projectDefaultCrs", crs.authid())

    @staticmethod
    def layerDefaultCrs():
        return QgsCRSCache.instance().crsByOgcWmsCrs(Application.layerDefaultCrsAuthid())

    @staticmethod
    def layerDefaultCrsAuthid():
        return QSettings().value("/Projections/layerDefaultCrs", "EPSG:4326")

    @staticmethod
    def setLayerDefaultCrs(crs):
        QSettings().setValue("/Projections/layerDefaultCrs", crs.authid())

    @staticmethod
    def setForceDefaultCrs():
        QSettings().setValue("/Projections/defaultBehaviour", "useGlobal")

    @staticmethod
    def setForceOftTransfom():
        QSettings().setValue("/Projections/otfTransformAutoEnable", False)
        QSettings().setValue("/Projections/otfTransformEnabled", True)

    @staticmethod
    def highlightColorName():
        return QColor(QSettings().value('/Map/highlight/color', Qgis.DEFAULT_HIGHLIGHT_COLOR.name(), str))

    @staticmethod
    def highlightColorAlpha():
        return QSettings().value('/Map/highlight/colorAlpha', Qgis.DEFAULT_HIGHLIGHT_COLOR.alpha(), int)

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
        return QSettings().value('/Map/highlight/buffer', Qgis.DEFAULT_HIGHLIGHT_BUFFER_MM, float)

    @staticmethod
    def highlightMinimumWidth():
        return QSettings().value('/Map/highlight/minWidth', Qgis.DEFAULT_HIGHLIGHT_MIN_WIDTH_MM, float)

    @staticmethod
    def setComposerFont(font):
        QSettings().setValue("/Composer/defaultFont", font.family())
