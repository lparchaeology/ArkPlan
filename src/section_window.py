# -*- coding: utf-8 -*-
"""
/***************************************************************************
                                ARK Spatial
                    A QGIS plugin for Archaeological Recording.
        Part of the Archaeological Recording Kit by L-P : Archaeology
                        http://ark.lparchaeology.com
                              -------------------
        begin                : 2016-03-09
        git sha              : $Format:%H$
        copyright            : 2016 by L-P : Heritage LLP
        email                : ark@lparchaeology.com
        copyright            : 2016 by John Layt
        email                : john@layt.net
 ***************************************************************************/

/***************************************************************************
 *                                                                         *
 *   This program is free software you can redistribute it and/or modify  *
 *   it under the terms of the GNU General Public License as published by  *
 *   the Free Software Foundation either version 2 of the License, or     *
 *   (at your option) any later version.                                   *
 *                                                                         *
 ***************************************************************************/
"""

from PyQt4 import uic
from PyQt4.QtCore import Qt, QSettings, QSize
from PyQt4.QtGui import QMainWindow, QGridLayout, QSizePolicy, QActionGroup, QLabel

from qgis.core import QgsProject, QgsRasterLayer, QgsMapLayerRegistry, QgsSnapper, QgsMessageLog, QgsFields, QgsLayerTreeModel, QgsLayerTreeNode
from qgis.gui import QgsMapCanvas, QgsMapToolZoom, QgsMapToolPan, QgsMessageBar

from ..libarkqgis.plugin import Project

from section_window_base import *

class SectionWindow(QMainWindow, Ui_SectionWindow):

    _project = None # Project()

    def __init__(self, project, parent=None):
        super(SectionWindow, self).__init__(parent)
        self._project = project

        self.setupUi(self)

        self._mapToolActionGroup = QActionGroup(self)

        self.actionPanMap.setIcon(Project.getThemeIcon('mActionPan.svg'))
        self._mapToolActionGroup.addAction(self.actionPanMap)
        self.actionPanMap.triggered.connect(self._setPanTool)

        self.actionZoomIn.setIcon(Project.getThemeIcon('mActionZoomIn.svg'))
        self._mapToolActionGroup.addAction(self.actionZoomIn)
        self.actionZoomIn.triggered.connect(self._setZoomIn)

        self.actionZoomOut.setIcon(Project.getThemeIcon('mActionZoomOut.svg'))
        self._mapToolActionGroup.addAction(self.actionZoomOut)
        self.actionZoomOut.triggered.connect(self._setZoomOut)

        self.actionZoomFull.setIcon(Project.getThemeIcon('mActionZoomFullExtent.svg'))
        self.actionZoomFull.triggered.connect(self._setZoomFull)

        self.actionZoomLast.setIcon(Project.getThemeIcon('mActionZoomLast.svg'))
        self._mapToolActionGroup.addAction(self.actionZoomLast)
        self.actionZoomLast.triggered.connect(self._setZoomLast)

        self.actionZoomNext.setIcon(Project.getThemeIcon('mActionZoomNext.svg'))
        self._mapToolActionGroup.addAction(self.actionZoomNext)
        self.actionZoomNext.triggered.connect(self._setZoomNext)

        self.actionEditMode.setIcon(Project.getThemeIcon('mActionToggleEditing.svg'))
        self.actionEditMode.toggled.connect(self._editMode)
        self.actionRefreshMap.setIcon(Project.getThemeIcon('mActionRefresh.png'))
        self.actionRefreshMap.triggered.connect(self._refreshMap)

        self.actionOpen.triggered.connect(self._open)
        self.actionClose.triggered.connect(self._close)
        self.actionClearEdits.setIcon(Project.getThemeIcon('mActionCancelEdits.svg'))
        self.actionClearEdits.triggered.connect(self._clearEdits)
        self.actionMergeEdits.setIcon(Project.getThemeIcon('mActionSaveEdits.svg'))
        self.actionMergeEdits.triggered.connect(self._mergeEdits)
        self.actionEditPoints.triggered.connect(self._editPoints)
        self.actionEditLines.triggered.connect(self._editLines)
        self.actionEditPolygons.triggered.connect(self._editPolygons)
        self.actionSelectPoints.triggered.connect(self._selectPoints)
        self.actionSelectLines.triggered.connect(self._selectLines)
        self.actionSelectPolygons.triggered.connect(self._selectPolygons)
        self.actionShowDrawings.toggled.connect(self._showDrawings)

        size = QSettings().value('/IconSize', 32, int)
        self.mainToolbar.setIconSize(QSize(size, size))

        self.restoreGeometry(project.readEntry('SectionWindow/geometry'))
        self._centralLayout = QGridLayout(self.centralWidget())
        self.centralWidget().setLayout(self._centralLayout)
        self._centralLayout.setContentsMargins(0, 0, 0, 0)

        self._canvas = QgsMapCanvas(self.centralWidget(), 'sectionCanvas')
        self._canvas.setSizePolicy(QSizePolicy.Expanding, QSizePolicy.Expanding)
        self._canvas.setCanvasColor(Qt.white)
        self._canvas.setMinimumWidth(400)
        self._centralLayout.addWidget(self._canvas, 0, 0, 2, 1)

        self._zoomInMapTool = QgsMapToolZoom(self._canvas, False)
        self._zoomInMapTool.setAction(self.actionZoomIn)

        self._zoomOutMapTool = QgsMapToolZoom(self._canvas, True)
        self._zoomOutMapTool.setAction(self.actionZoomOut)

        self._panMapTool = QgsMapToolPan(self._canvas)
        self._panMapTool.setAction(self.actionPanMap)

        self._canvas.clearExtentHistory()
        self._canvas.zoomLastStatusChanged.connect(self.actionZoomLast.setEnabled)
        self._canvas.zoomNextStatusChanged.connect(self.actionZoomNext.setEnabled)

        wheelAction = QSettings().value("/qgis/wheel_action", 2, int)
        zoomFactor = QSettings().value("/qgis/zoom_factor", 2, float)
        self._canvas.setWheelAction(wheelAction, zoomFactor)

        self.statusBar().addPermanentWidget(QLabel('Sections!'), 0 )

        self._messageBar = QgsMessageBar(self.centralWidget())
        self._messageBar.setSizePolicy(QSizePolicy.Minimum, QSizePolicy.Fixed )
        self._centralLayout.addWidget(self._messageBar, 0, 0, 1, 1)


    def _setPanTool(self):
        self._canvas.setMapTool(self._panMapTool)

    def _setZoomIn(self):
        self._canvas.setMapTool(self._zoomInMapTool)

    def _setZoomOut(self):
        self._canvas.setMapTool(self._zoomOutMapTool)

    def _setZoomFull(self):
        self._canvas.zoomToFullExtent()

    def _setZoomLast(self):
        self._canvas.zoomToPreviousExtent()

    def _setZoomNext(self):
        self._canvas.zoomToNextExtent()

    def _open(self):
        pass

    def _close(self):
        self._project.writeEntry('SectionWindow/geometry', self.saveGeometry())

    def _editMode(self):
        pass

    def _refreshMap(self):
        self._canvas.refresh()

    def _clearEdits(self):
        pass

    def _mergeEdits(self):
        pass

    def _editPoints(self):
        pass

    def _editLines(self):
        pass

    def _editPolygons(self):
        pass

    def _selectPoints(self):
        pass

    def _selectLines(self):
        pass

    def _selectPolygons(self):
        pass

    def _showDrawings(self):
        pass
