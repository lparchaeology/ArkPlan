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
        copyright            : 2010 by Jürgen E. Fischer
        copyright            : 2007 by Marco Hugentobler
        copyright            : 2006 by Martin Dobias
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

from qgis.PyQt.QtCore import Qt, pyqtSignal

from qgis.core import QgsFeature
from qgis.gui import QgsMapToolIdentify


class MapToolIndentifyFeatures(QgsMapToolIdentify):

    featureIdentified = pyqtSignal(QgsFeature)

    def __init__(self, canvas):
        super().__init__(canvas)
        mToolName = self.tr('Identify feature')

    def canvasReleaseEvent(self, e):
        if e.button() != Qt.LeftButton:
            return
        results = self.identify(e.x(), e.y(), QgsMapToolIdentify.LayerSelection, QgsMapToolIdentify.VectorLayer)
        if (len(results) < 1):
            return
        # TODO: display a menu when several features identified
        self.featureIdentified.emit(results[0].mFeature)

    def keyPressEvent(self, e):
        if (e.key() == Qt.Key_Escape):
            self.canvas().unsetMapTool(self)
