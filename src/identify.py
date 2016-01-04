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
import webbrowser

from PyQt4.QtCore import Qt, pyqtSignal, QSettings
from PyQt4.QtGui import QAction, QMenu, QColor

from qgis.core import *
from qgis.gui import QgsMapTool, QgsHighlight, QgsMapToolIdentify, QgsVertexMarker

from config import Config

def _quote(string):
    return "'" + string + "'"

def _doublequote(string):
    return '"' + string + '"'

class MapToolIndentifyItems(QgsMapToolIdentify):

    _menu = None # QMenu()
    _actions = []
    _highlights = []
    _project = None
    _vertexMarker = None  # QgsVertexMarker

    def __init__(self, project):
        super(MapToolIndentifyItems, self).__init__(project.mapCanvas())
        mToolName = self.tr('Identify feature')
        self._vertexMarker = QgsVertexMarker(project.mapCanvas())
        self._vertexMarker.setIconType(QgsVertexMarker.ICON_CROSS)
        self._project = project
        self._menu = QMenu(project.mapCanvas())
        self._menu.hovered.connect(self._highlight)

    def deactivate(self):
        self._reset()
        super(MapToolIndentifyItems, self).deactivate()

    def canvasPressEvent(self, e):
        self._reset()

    def canvasReleaseEvent(self, e):
        self._reset()
        if e.button() != Qt.LeftButton:
            return
        layers = [self._project.plan.pointsLayer, self._project.plan.linesLayer, self._project.plan.polygonsLayer]
        results = self.identify(e.x(), e.y(), layers, QgsMapToolIdentify.TopDownAll)
        if (len(results) < 1):
            return
        # Build the set of unique items identified
        items = set()
        for result in results:
            feature = result.mFeature
            siteCode = feature.attribute(self._project.fieldName('site'))
            classCode = feature.attribute(self._project.fieldName('class'))
            itemId = feature.attribute(self._project.fieldName('id'))
            item = (siteCode, classCode, itemId)
            items.add(item)
        action = QAction('Plan Items:', self._menu)
        action.setData('top')
        self._menu.addAction(action)
        site = ''
        for item in sorted(items):
            if item[0] != site:
                site = item[0]
                self._menu.addSeparator()
                action = QAction(site + ':', self._menu)
                action.setData('top')
                self._menu.addAction(action)
            action = IdentifyItemAction(item[0], item[1], item[2], self._project, self._menu)
            action.setData('top')
            action.zoomToItemSelected.connect(self._zoom)
            action.panToItemSelected.connect(self._pan)
            action.editItemSelected.connect(self._editInBuffers)
            action.deleteItemSelected.connect(self._delete)
            action.openInArkSelected.connect(self._openInArk)
            self._actions.append(action)
            self._menu.addAction(action)
        self._menu.addSeparator()
        mapPoint = self.toMapCoordinates(e.pos())
        self._vertexMarker.setCenter(mapPoint)
        localPoint = self._project.gridModule.mapTransformer.map(mapPoint)
        action = QAction(mapPoint.toString(3), self._menu)
        action.setData('top')
        self._menu.addAction(action)
        self._menu.addAction(localPoint.toString(3))
        selected = self._menu.exec_(e.globalPos())
        self._reset()

    def keyPressEvent(self, e):
        if (e.key() == Qt.Key_Escape):
            self._reset()
            self.canvas().unsetMapTool(self)

    def _reset(self):
        self._menu.clear()
        del self._highlights[:]
        del self._actions[:]
        self._vertexMarker.setCenter(QgsPoint())

    def _highlight(self, item):
        if item.data() == 'top':
            del self._highlights[:]
        else:
            return
        if type(item) is not IdentifyItemAction:
            return
        request = QgsFeatureRequest()
        request.setFilterExpression(item.expr)
        for feature in self._project.plan.polygonsLayer.getFeatures(request):
            self._addHighlight(self._project.mapCanvas(), feature.geometry(), self._project.plan.polygonsLayer)
        for feature in self._project.plan.linesLayer.getFeatures(request):
            self._addHighlight(self._project.mapCanvas(), feature.geometry(), self._project.plan.linesLayer)
        for feature in self._project.plan.pointsLayer.getFeatures(request):
            self._addHighlight(self._project.mapCanvas(), feature.geometry(), self._project.plan.pointsLayer)

    def _addHighlight(self, canvas, geometry, layer):
        hl = QgsHighlight(canvas, geometry, layer)
        color = QColor(QSettings().value('/Map/highlight/color', QGis.DEFAULT_HIGHLIGHT_COLOR.name(), str))
        alpha = QSettings().value('/Map/highlight/colorAlpha', QGis.DEFAULT_HIGHLIGHT_COLOR.alpha(), int)
        buff = QSettings().value('/Map/highlight/buffer', QGis.DEFAULT_HIGHLIGHT_BUFFER_MM, float)
        minWidth = QSettings().value('/Map/highlight/minWidth', QGis.DEFAULT_HIGHLIGHT_MIN_WIDTH_MM, float)
        hl.setColor(color)
        color.setAlpha(alpha)
        hl.setFillColor(color)
        hl.setBuffer(buff)
        hl.setMinWidth(minWidth)
        self._highlights.append(hl)

    def _zoom(self, classCode, siteCode, itemId):
        self._project.planModule.zoomToItem(siteCode, classCode, itemId)

    def _pan(self, classCode, siteCode, itemId):
        self._project.planModule.panToItem(siteCode, classCode, itemId)

    def _openInArk(self, classCode, siteCode, itemId):
        mod_cd = classCode + '_cd'
        item = siteCode + '_' + itemId
        url = self._project.arkUrl() + 'micro_view.php?item_key=' + mod_cd + '&' + mod_cd + '=' + item
        browser = webbrowser.get('firefox')
        if browser is None:
            browser = webbrowser.get()
        if browser:
            browser.open_new_tab(url)

    def _editInBuffers(self, classCode, siteCode, itemId):
        self._project.planModule.editInBuffers(siteCode, classCode, itemId)

    def _delete(self, classCode, siteCode, itemId):
        self._project.planModule.deleteItem(siteCode, classCode, itemId)

class IdentifyItemAction(QAction):

    openInArkSelected = pyqtSignal(str, str, str)
    editItemSelected = pyqtSignal(str, str, str)
    deleteItemSelected = pyqtSignal(str, str, str)
    panToItemSelected = pyqtSignal(str, str, str)
    zoomToItemSelected = pyqtSignal(str, str, str)

    siteCode = ''
    classCode = ''
    itemId = 0

    expr = ''

    def __init__(self, siteCode, classCode, itemId, project, parent=None):
        super(IdentifyItemAction, self).__init__(parent)
        for source in Config.planSourceClasses:
            if source[1] == classCode:
                self.setText(source[0] + ' ' + str(itemId))
        self.siteCode = siteCode
        self.classCode = classCode
        self.itemId = itemId
        self.expr = _doublequote(project.fieldName('site')) + ' = ' + _quote(siteCode) + ' and ' + \
                    _doublequote(project.fieldName('class')) + ' = ' + _quote(classCode) + ' and ' + \
                    _doublequote(project.fieldName('id')) + ' = ' + str(itemId)
        menu = QMenu()
        request = QgsFeatureRequest()
        request.setFilterExpression(self.expr)
        source = None
        area = []
        for feature in project.plan.polygonsLayer.getFeatures(request):
            if feature.attribute(project.fieldName('category')) == 'sch':
                source = (str(feature.attribute(project.fieldName('source_cd'))),
                          str(feature.attribute(project.fieldName('source_cl'))),
                          str(feature.attribute(project.fieldName('source_id'))))
                area.append(feature.geometry().area())
        self.zoomAction = QAction('Zoom to Item', parent)
        self.zoomAction.triggered.connect(self._zoomToItem)
        menu.addAction(self.zoomAction)
        self.panAction = QAction('Pan to Item', parent)
        self.panAction.triggered.connect(self._panToItem)
        menu.addAction(self.panAction)
        if project.useArkDB() and project.arkUrl():
            self.linkAction = QAction('Open in ARK', parent)
            self.linkAction.triggered.connect(self._openArk)
            menu.addAction(self.linkAction)
        menu.addSeparator()
        self.editAction = QAction('Edit Item', parent)
        self.editAction.triggered.connect(self._editItem)
        menu.addAction(self.editAction)
        self.deleteAction = QAction('Delete Item', parent)
        self.deleteAction.triggered.connect(self._deleteItem)
        menu.addAction(self.deleteAction)
        menu.addSeparator()
        if source is None:
            menu.addAction('No Schematic')
        else:
            sourceCode = feature.attribute(project.fieldName('source_cd'))
            sourceClass = feature.attribute(project.fieldName('source_cl'))
            sourceId = feature.attribute(project.fieldName('source_id'))
            sourceFile = feature.attribute(project.fieldName('file'))
            sourceText = 'Unknown Source'
            if sourceCode is not None and sourceCode != NULL and sourceCode != '':
                for source in Config.planSourceCodes:
                    if source[1] == sourceCode:
                        sourceText = source[0]
            menu.addAction(sourceText)
            if sourceId is not None and sourceId != NULL and sourceId != '' and (sourceClass != classCode or sourceId != itemId):
                for source in Config.planSourceClasses:
                    if source[1] == classCode:
                        menu.addAction(source[0] + ' ' + str(sourceId))
        if len(area) > 0:
            menu.addSeparator()
            for a in area:
                menu.addAction('Area: ' + str(a))
        self.setMenu(menu)

    def _openArk(self):
        self.openInArkSelected.emit(self.classCode, self.siteCode, str(self.itemId))

    def _editItem(self):
        self.editItemSelected.emit(self.classCode, self.siteCode, str(self.itemId))

    def _deleteItem(self):
        self.deleteItemSelected.emit(self.classCode, self.siteCode, str(self.itemId))

    def _panToItem(self):
        self.panToItemSelected.emit(self.classCode, self.siteCode, str(self.itemId))

    def _zoomToItem(self):
        self.zoomToItemSelected.emit(self.classCode, self.siteCode, str(self.itemId))
