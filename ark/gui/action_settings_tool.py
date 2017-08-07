# -*- coding: utf-8 -*-
"""
/***************************************************************************
                                ARK Spatial
                    A QGIS plugin for Archaeological Recording.
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

from PyQt4.QtCore import pyqtSignal
from PyQt4.QtGui import QAction, QActionGroup, QIcon, QMenu, QToolButton

from ArkSpatial.ark.core.enum import DrawingAction, FilterAction, MapAction

import resources


class ActionSettingsTool(QToolButton):

    settingsChanged = pyqtSignal()
    mapActionChanged = pyqtSignal(int)
    filterActionChanged = pyqtSignal(int)
    drawingActionChanged = pyqtSignal(int)

    def __init__(self, parent=None):
        super(ActionSettingsTool, self).__init__(parent)

        self._mapActionGroup = QActionGroup(self)
        self._noMapAction = self._addMapAction(MapAction.NoMapAction, 'No map action')
        self._zoomMapAction = self._addMapAction(MapAction.ZoomMap, 'Zoom map view')
        self._panMapAction = self._addMapAction(MapAction.PanMap, 'Pan map view')
        self._moveMapAction = self._addMapAction(MapAction.MoveMap, 'Move map view')
        self._moveMapAction.setChecked(True)

        self._filterActionGroup = QActionGroup(self)
        self._noFilterAction = self._addFilterAction(FilterAction.NoFilterAction, 'No filter action')
        self._includeFilterAction = self._addFilterAction(FilterAction.IncludeFilter, 'Add to filter')
        self._exclusiveFilterAction = self._addFilterAction(FilterAction.ExclusiveFilter, 'Exclusive filter')
        self._selectFilterAction = self._addFilterAction(FilterAction.SelectFilter, 'Add to selection')
        self._exclusiveSelectFilterAction = self._addFilterAction(
            FilterAction.ExclusiveSelectFilter, 'Exclusive selection')
        self._highlightFilterAction = self._addFilterAction(FilterAction.HighlightFilter, 'Add to highlight')
        self._exclusiveHighlightFilterAction = self._addFilterAction(
            FilterAction.ExclusiveHighlightFilter, 'Exclusive highlight')
        self._exclusiveHighlightFilterAction.setChecked(True)

        self._drawingActionGroup = QActionGroup(self)
        self._noDrawingAction = self._addDrawingAction(DrawingAction.NoDrawingAction, 'No drawing action')
        self._noDrawingAction.setChecked(True)
        self._loadDrawingsAction = self._addDrawingAction(DrawingAction.LoadDrawings, 'Load drawings')
        self._addDrawingsAction = self._addDrawingAction(DrawingAction.AddDrawings, 'Add drawings')

        self._settingsMenu = QMenu(self)
        self._settingsMenu.addActions(self._mapActionGroup.actions())
        self._settingsMenu.addSeparator()
        self._settingsMenu.addActions(self._filterActionGroup.actions())
        self._settingsMenu.addSeparator()
        self._settingsMenu.addActions(self._drawingActionGroup.actions())

        self._settingsAction = QAction(QIcon(':/plugins/ark/settings.svg'), "Action Settings", self)
        self._settingsAction.setMenu(self._settingsMenu)
        self.setDefaultAction(self._settingsAction)
        self.setPopupMode(QToolButton.InstantPopup)

    def setMapAction(self, mapAction):
        if mapAction == MapAction.NoMapAction:
            self._noMapAction.setChecked(True)
        elif mapAction == MapAction.ZoomMap:
            self._zoomMapAction.setChecked(True)
        elif mapAction == MapAction.PanMap:
            self._panMapAction.setChecked(True)
        elif mapAction == MapAction.MoveMap:
            self._moveMapAction.setChecked(True)

    def setFilterAction(self, filterAction):
        if filterAction == FilterAction.NoFilterAction:
            self._noFilterAction.setChecked(True)
        elif filterAction == FilterAction.IncludeFilter:
            self._includeFilterAction.setChecked(True)
        elif filterAction == FilterAction.ExclusiveFilter:
            self._exclusiveFilterAction.setChecked(True)
        elif filterAction == FilterAction.SelectFilter:
            self._selectFilterAction.setChecked(True)
        elif filterAction == FilterAction.ExclusiveSelectFilter:
            self._exclusiveSelectFilterAction.setChecked(True)
        elif filterAction == FilterAction.HighlightFilter:
            self._highlightFilterAction.setChecked(True)
        elif filterAction == FilterAction.ExclusiveHighlightFilter:
            self._exclusiveHighlightFilterAction.setChecked(True)

    def setDrawingAction(self, drawingAction):
        if drawingAction == DrawingAction.NoDrawingAction:
            self._noDrawingAction.setChecked(True)
        elif drawingAction == DrawingAction.LoadDrawings:
            self._loadDrawingsAction.setChecked(True)
        elif drawingAction == DrawingAction.AddDrawings:
            self._addDrawingsAction.setChecked(True)

    def _addMapAction(self, mapAction, text):
        action = QAction(text, self)
        action.setCheckable(True)
        action.setData(mapAction)
        action.triggered.connect(self._mapActionSelected)
        self._mapActionGroup.addAction(action)
        return action

    def _mapActionSelected(self):
        self.mapActionChanged.emit(self._mapActionGroup.checkedAction().data())
        self.settingsChanged.emit()

    def _addFilterAction(self, filterAction, text):
        action = QAction(text, self)
        action.setCheckable(True)
        action.setData(filterAction)
        action.triggered.connect(self._filterActionSelected)
        self._filterActionGroup.addAction(action)
        return action

    def _filterActionSelected(self):
        self.filterActionChanged.emit(self._filterActionGroup.checkedAction().data())
        self.settingsChanged.emit()

    def _addDrawingAction(self, drawingAction, text):
        action = QAction(text, self)
        action.setCheckable(True)
        action.setData(drawingAction)
        action.triggered.connect(self._drawingActionSelected)
        self._drawingActionGroup.addAction(action)
        return action

    def _drawingActionSelected(self):
        self.drawingActionChanged.emit(self._drawingActionGroup.checkedAction().data())
        self.settingsChanged.emit()
