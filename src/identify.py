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

from PyQt4.QtCore import Qt, pyqtSignal, QSettings, QPoint
from PyQt4.QtGui import QAction, QMenu, QColor, QApplication

from qgis.core import *
from qgis.gui import QgsMapTool, QgsHighlight, QgsMapToolIdentify, QgsVertexMarker

from config import Config
from plan_item import ItemKey, ItemSource

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
        mapPoint = self.toMapCoordinates(e.pos())
        self._vertexMarker.setCenter(mapPoint)
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
            items.add(ItemKey(siteCode, classCode, itemId))
        action = QAction('Plan Items', self._menu)
        action.setData('top')
        self._menu.addAction(action)
        site = ''
        for item in sorted(items):
            if item.siteCode != site:
                site = item.siteCode
                self._menu.addSeparator()
                action = QAction('Site ' + site + ':', self._menu)
                action.setData('top')
                self._menu.addAction(action)
            action = IdentifyItemAction(item, self._project, self._menu)
            action.setData('top')
            action.zoomToItemSelected.connect(self._zoom)
            action.panToItemSelected.connect(self._pan)
            action.filterItemSelected.connect(self._filterItem)
            action.excludeFilterItemSelected.connect(self._excludeFilterItem)
            action.highlightItemSelected.connect(self._highlightItem)
            action.addHighlightItemSelected.connect(self._addHighlightItem)
            action.editItemSelected.connect(self._editInBuffers)
            action.deleteItemSelected.connect(self._delete)
            action.openDrawingsSelected.connect(self._openDrawings)
            self._actions.append(action)
            self._menu.addAction(action)
        self._menu.addSeparator()
        action = ClipboardAction('Map: ', mapPoint.toString(3), self._menu)
        action.setData('top')
        self._menu.addAction(action)
        if self._project.gridModule.mapTransformer is not None:
            localPoint = self._project.gridModule.mapTransformer.map(mapPoint)
            self._menu.addAction(ClipboardAction('Local: ', localPoint.toString(3), self._menu))
        menuPos = QPoint(e.globalX() + 100, e.globalY() - 50)
        selected = self._menu.exec_(menuPos)
        self._reset(resetVertex=False)

    def keyPressEvent(self, e):
        if (e.key() == Qt.Key_Escape):
            self._reset()
            self.canvas().unsetMapTool(self)

    def _reset(self, resetVertex=True):
        self._menu.clear()
        del self._highlights[:]
        del self._actions[:]
        if resetVertex:
            self._vertexMarker.setCenter(QgsPoint())

    def _highlight(self, item):
        if item.data() == 'top':
            del self._highlights[:]
        else:
            return
        if type(item) is not IdentifyItemAction:
            return
        request = item.itemKey.featureRequest()
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

    def _zoom(self, itemKey):
        self._project.planModule.zoomToItem(itemKey, highlight=True)

    def _pan(self, itemKey):
        self._project.planModule.panToItem(itemKey, highlight=True)

    def _filterItem(self, itemKey):
        self._project.planModule.filterItem(itemKey)

    def _excludeFilterItem(self, itemKey):
        self._project.planModule.excludeFilterItem(itemKey)

    def _highlightItem(self, itemKey):
        self._project.planModule.highlightItem(itemKey)

    def _addHighlightItem(self, itemKey):
        self._project.planModule.addHighlightItem(itemKey)

    def _openDrawings(self, itemKey):
        self._project.planModule.loadDrawing(itemKey)

    def _editInBuffers(self, itemKey):
        self._project.planModule.editInBuffers(itemKey)

    def _delete(self, itemKey):
        self._project.planModule.deleteItem(itemKey)

class ClipboardAction(QAction):

    _text = ''

    def __init__(self, label, text, parent=None):
        super(ClipboardAction, self).__init__(label + text, parent)
        self.triggered.connect(self._copy)
        self._text = text

    def _copy(self):
        QApplication.clipboard().setText(self._text)

class OpenArkAction(QAction):

    _url = ''

    def __init__(self, arkUrl, itemKey, label, parent=None):
        super(OpenArkAction, self).__init__(label, parent)
        mod_cd = itemKey.classCode + '_cd'
        item = itemKey.siteCode + '_' + itemKey.itemId
        self._url = arkUrl + '/micro_view.php?item_key=' + mod_cd + '&' + mod_cd + '=' + item
        self.triggered.connect(self._open)

    def _open(self):
        QApplication.clipboard().setText(self._url)
        try:
            webbrowser.get().open_new_tab(self._url)
        except:
            self._project.showWarningMessage('Unable to open browser, ARK link has been copied to the clipboard')

class IdentifyItemAction(QAction):

    openInArkSelected = pyqtSignal(object)
    editItemSelected = pyqtSignal(object)
    deleteItemSelected = pyqtSignal(object)
    panToItemSelected = pyqtSignal(object)
    zoomToItemSelected = pyqtSignal(object)
    filterItemSelected = pyqtSignal(object)
    excludeFilterItemSelected = pyqtSignal(object)
    highlightItemSelected = pyqtSignal(object)
    addHighlightItemSelected = pyqtSignal(object)
    openDrawingsSelected = pyqtSignal(object)

    itemKey = ItemKey()

    _iface = None

    def __init__(self, itemKey, project, parent=None):
        super(IdentifyItemAction, self).__init__(parent)
        self._iface = project.iface
        self.itemKey = itemKey
        self.setText(itemKey.itemLabel())
        menu = QMenu()
        sourceSet = set()
        area = []
        haveSchematic = False
        sectionSchematics = []
        for feature in project.plan.polygonsLayer.getFeatures(itemKey.featureRequest()):
            category = feature.attribute(project.fieldName('category'))
            if category == 'sch' or category == 'scs':
                haveSchematic = True
                source = ItemSource()
                source.fromFeature(feature)
                if source.isValid():
                    sourceSet.add(source)
                if category == 'sch':
                    area.append(feature.geometry().area())
        sourceDict = {}
        for source in sourceSet:
            if source.sourceCode not in sourceDict:
                sourceDict[source.sourceCode] = set()
            sourceDict[source.sourceCode].add(source.key)
        self.zoomAction = QAction('Zoom to Item', parent)
        self.zoomAction.triggered.connect(self._zoomToItem)
        menu.addAction(self.zoomAction)
        self.panAction = QAction('Pan to Item', parent)
        self.panAction.triggered.connect(self._panToItem)
        menu.addAction(self.panAction)
        self.filterAction = QAction('Filter Item', parent)
        self.filterAction.triggered.connect(self._filterItem)
        menu.addAction(self.filterAction)
        self.excludeFilterAction = QAction('Exclude Item from Filter', parent)
        self.excludeFilterAction.triggered.connect(self._excludeFilterItem)
        menu.addAction(self.excludeFilterAction)
        self.highlightAction = QAction('Select Item', parent)
        self.highlightAction.triggered.connect(self._highlightItem)
        menu.addAction(self.highlightAction)
        self.addHighlightAction = QAction('Add Item to Selection', parent)
        self.addHighlightAction.triggered.connect(self._addHighlightItem)
        menu.addAction(self.addHighlightAction)
        if project.useArkDB() and project.arkUrl():
            self.linkAction = OpenArkAction(project.arkUrl(), itemKey, 'Open in ARK', parent)
            menu.addAction(self.linkAction)
        self.drawingAction = QAction('Open Drawings', parent)
        self.drawingAction.triggered.connect(self._openDrawings)
        menu.addAction(self.drawingAction)
        menu.addSeparator()
        self.editAction = QAction('Edit Item', parent)
        self.editAction.triggered.connect(self._editItem)
        menu.addAction(self.editAction)
        self.deleteAction = QAction('Delete Item', parent)
        self.deleteAction.triggered.connect(self._deleteItem)
        menu.addAction(self.deleteAction)
        menu.addSeparator()
        if len(sourceDict) > 0:
            for sourceCode in sourceDict.keys():
                menu.addAction(Config.sourceCodes[sourceCode]['label'] + ':')
                sources = sorted(sourceDict[sourceCode])
                for itemKey in sources:
                    if itemKey.isValid():
                        menu.addAction(itemKey.itemLabel())
        elif haveSchematic:
            menu.addAction('Unknown Source')
        else:
            menu.addAction('No Schematic')
        if project.data.hasData():
            menu.addSeparator()
            if itemKey.classCode == 'cxt':
                subItem = project.data.getParent(itemKey)
                if subItem:
                    grpItem = project.data.getParent(subItem)
                    if project.useArkDB() and project.arkUrl():
                        self.subAction = OpenArkAction(project.arkUrl(), subItem, 'Sub-group: ' + str(subItem.itemId), parent)
                        menu.addAction(self.subAction)
                        if grpItem:
                            self.grpAction = OpenArkAction(project.arkUrl(), grpItem, 'Group: ' + str(grpItem.itemId), parent)
                            menu.addAction(self.grpAction)
                    else:
                        menu.addAction('Sub-group: ' + str(subItem.itemId))
                        if grpItem:
                            menu.addAction('Group: ' + str(grpItem.itemId))
        if len(area) > 0:
            menu.addSeparator()
            tot = 0
            for a in area:
                tot += a
            units = self._iface.mapCanvas().mapUnits()
            suffix = ''
            if units == QGis.Meters:
                suffix = u' m²'
            elif units == QGis.Feet:
                suffix = u' ft²'
            elif units == QGis.NauticalMiles:
                suffix = u' NM²'
            menu.addAction(ClipboardAction(u'Area: ', u'%.3f' % tot + suffix, parent))
        self.setMenu(menu)

    def _editItem(self):
        self.editItemSelected.emit(self.itemKey)

    def _deleteItem(self):
        self.deleteItemSelected.emit(self.itemKey)

    def _panToItem(self):
        self.panToItemSelected.emit(self.itemKey)

    def _zoomToItem(self):
        self.zoomToItemSelected.emit(self.itemKey)

    def _filterItem(self):
        self.filterItemSelected.emit(self.itemKey)

    def _excludeFilterItem(self):
        self.excludeFilterItemSelected.emit(self.itemKey)

    def _highlightItem(self):
        self.highlightItemSelected.emit(self.itemKey)

    def _addHighlightItem(self):
        self.addHighlightItemSelected.emit(self.itemKey)

    def _openDrawings(self):
        self.openDrawingsSelected.emit(self.itemKey)
