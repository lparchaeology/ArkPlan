# -*- coding: utf-8 -*-
"""
/***************************************************************************
                                ARK Spatial
                    A QGIS plugin for Archaeological Recording.
        Part of the Archaeological Recording Kit by L-P : Archaeology
                        http://ark.lparchaeology.com
                              -------------------
        begin                : 2014-12-07
        git sha              : $Format:%H$
        copyright            : 2014, 2015 by L-P : Heritage LLP
        email                : ark@lparchaeology.com
        copyright            : 2014, 2015 by John Layt
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

import os

from PyQt4 import uic
from PyQt4.QtCore import Qt, pyqtSignal
from PyQt4.QtGui import QTabWidget, QToolButton

from ..libarkqgis.map_tools import *

import drawing_widget_base

class DrawingWidget(QTabWidget, drawing_widget_base.Ui_DrawingWidget):

    autoSchematicSelected = pyqtSignal()

    _colMax = 5
    _planPoint = 0
    _planLine = 0
    _planPolygon = 0
    _sectionPoint = 0
    _sectionLine = 0
    _sectionPolygon = 0
    _basePoint = 0
    _baseLine = 0
    _basePolygon = 0

    def __init__(self, parent=None):
        super(DrawingWidget, self).__init__(parent)
        self.setupUi(self)

    def initGui(self):
        self.autoSchematicTool.clicked.connect(self.autoSchematicSelected)

    def unloadGui(self):
        pass

    def loadProject(self, project):
        pass

    def closeProject(self):
        pass

    # Drawing Tools

    def addDrawingTool(self, collection, type, action):
        toolButton = QToolButton(self)
        toolButton.setFixedWidth(40)
        toolButton.setDefaultAction(action)
        if collection == 'plan':
            if type == FeatureType.Point or type == FeatureType.Elevation:
                self._addToolWidget(self.planPointLayout, toolButton, self._planPoint)
                self._planPoint += 1
            if type == FeatureType.Line or type == FeatureType.Segment:
                self._addToolWidget(self.planLineLayout, toolButton, self._planLine)
                self._planLine += 1
            if type == FeatureType.Polygon:
                self._addToolWidget(self.planPolygonLayout, toolButton, self._planPolygon)
                self._planPolygon += 1
        elif collection == 'section':
            if type == FeatureType.Point or type == FeatureType.Elevation:
                self._addToolWidget(self.sectionPointLayout, toolButton, self._sectionPoint)
                self._sectionPoint += 1
            if type == FeatureType.Line or type == FeatureType.Segment:
                self._addToolWidget(self.sectionLineLayout, toolButton, self._sectionLine)
                self._sectionLine += 1
            if type == FeatureType.Polygon:
                self._addToolWidget(self.sectionPolygonLayout, toolButton, self._sectionPolygon)
                self._sectionPolygon += 1
        elif collection == 'base':
            if type == FeatureType.Point or type == FeatureType.Elevation:
                self._addToolWidget(self.basePointLayout, toolButton, self._basePoint)
                self._basePoint += 1
            if type == FeatureType.Line or type == FeatureType.Segment:
                self._addToolWidget(self.baseLineLayout, toolButton, self._baseLine)
                self._baseLine += 1
            if type == FeatureType.Polygon:
                self._addToolWidget(self.basePolygonLayout, toolButton, self._basePolygon)
                self._basePolygon += 1

    def clearDrawingTools(self):
        for (i in range(layout.count() -1, 0)
            layout.takeAt(i)

    def _addToolWidget(self, layout, toolButton, counter):
        layout.addWidget(toolButton, counter // self._colMax, counter % self._colMax, Qt.AlignCenter)
