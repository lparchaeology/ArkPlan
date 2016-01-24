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
from PyQt4.QtGui import QAction, QMenu, QColor, QApplication

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
            item = (siteCode, classCode, itemId)
            items.add(item)
        action = QAction('Plan Items', self._menu)
        action.setData('top')
        self._menu.addAction(action)
        site = ''
        for item in sorted(items):
            if item[0] != site:
                site = item[0]
                self._menu.addSeparator()
                action = QAction('Site ' + site + ':', self._menu)
                action.setData('top')
                self._menu.addAction(action)
            action = IdentifyItemAction(item[0], item[1], item[2], self._project, self._menu)
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
        selected = self._menu.exec_(e.globalPos())
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
        self._project.planModule.zoomToItem(siteCode, classCode, itemId, highlight=True)

    def _pan(self, classCode, siteCode, itemId):
        self._project.planModule.panToItem(siteCode, classCode, itemId, highlight=True)

    def _filterItem(self, classCode, siteCode, itemId):
        self._project.planModule.filterItem(siteCode, classCode, itemId)

    def _excludeFilterItem(self, classCode, siteCode, itemId):
        self._project.planModule.excludeFilterItem(siteCode, classCode, itemId)

    def _highlightItem(self, classCode, siteCode, itemId):
        self._project.planModule.highlightItem(siteCode, classCode, itemId)

    def _addHighlightItem(self, classCode, siteCode, itemId):
        self._project.planModule.addHighlightItem(siteCode, classCode, itemId)

    def _openDrawings(self, classCode, siteCode, itemId):
        self._project.planModule.loadDrawing(classCode, siteCode, itemId)

    def _editInBuffers(self, classCode, siteCode, itemId):
        self._project.planModule.editInBuffers(siteCode, classCode, itemId)

    def _delete(self, classCode, siteCode, itemId):
        self._project.planModule.deleteItem(siteCode, classCode, itemId)

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

    def __init__(self, arkUrl, siteCode, classCode, itemId, label, parent=None):
        super(OpenArkAction, self).__init__(label, parent)
        mod_cd = classCode + '_cd'
        item = siteCode + '_' + str(itemId)
        self._url = arkUrl + '/micro_view.php?item_key=' + mod_cd + '&' + mod_cd + '=' + item
        self.triggered.connect(self._open)

    def _open(self):
        QApplication.clipboard().setText(self._url)
        try:
            webbrowser.get().open_new_tab(self._url)
        except:
            self._project.showWarningMessage('Unable to open browser, ARK link has been copied to the clipboard')

class IdentifyItemAction(QAction):

    openInArkSelected = pyqtSignal(str, str, str)
    editItemSelected = pyqtSignal(str, str, str)
    deleteItemSelected = pyqtSignal(str, str, str)
    panToItemSelected = pyqtSignal(str, str, str)
    zoomToItemSelected = pyqtSignal(str, str, str)
    filterItemSelected = pyqtSignal(str, str, str)
    excludeFilterItemSelected = pyqtSignal(str, str, str)
    highlightItemSelected = pyqtSignal(str, str, str)
    addHighlightItemSelected = pyqtSignal(str, str, str)
    openDrawingsSelected = pyqtSignal(str, str, str)

    siteCode = ''
    classCode = ''
    itemId = 0

    expr = ''

    _iface = None

    def __init__(self, siteCode, classCode, itemId, project, parent=None):
        super(IdentifyItemAction, self).__init__(parent)
        self._iface = project.iface
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
            self.linkAction = OpenArkAction(project.arkUrl(), siteCode, classCode, itemId, 'Open in ARK', parent)
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
                        menu.addAction(source[0] + ' ' + sourceId)
        if project.data.hasData():
            project.logMessage('has data')
            menu.addSeparator()
            if classCode == 'cxt':
                subItem = project.data.getParent(siteCode, classCode, str(itemId))
                if subItem:
                    grpItem = project.data.getParent(subItem.siteCode, subItem.classCode, subItem.itemId)
                    if project.useArkDB() and project.arkUrl():
                        self.subAction = OpenArkAction(project.arkUrl(), subItem.siteCode, subItem.classCode, subItem.itemId,
                                                    'Sub-group: ' + str(subItem.itemId), parent)
                        menu.addAction(self.subAction)
                        if grpItem:
                            self.grpAction = OpenArkAction(project.arkUrl(), grpItem.siteCode, grpItem.classCode, grpItem.itemId,
                                                        'Group: ' + str(grpItem.itemId), parent)
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
        self.editItemSelected.emit(self.classCode, self.siteCode, str(self.itemId))

    def _deleteItem(self):
        self.deleteItemSelected.emit(self.classCode, self.siteCode, str(self.itemId))

    def _panToItem(self):
        self.panToItemSelected.emit(self.classCode, self.siteCode, str(self.itemId))

    def _zoomToItem(self):
        self.zoomToItemSelected.emit(self.classCode, self.siteCode, str(self.itemId))

    def _filterItem(self):
        self.filterItemSelected.emit(self.classCode, self.siteCode, str(self.itemId))

    def _excludeFilterItem(self):
        self.excludeFilterItemSelected.emit(self.classCode, self.siteCode, str(self.itemId))

    def _highlightItem(self):
        self.highlightItemSelected.emit(self.classCode, self.siteCode, str(self.itemId))

    def _addHighlightItem(self):
        self.addHighlightItemSelected.emit(self.classCode, self.siteCode, str(self.itemId))

    def _openDrawings(self):
        self.openDrawingsSelected.emit(self.classCode, self.siteCode, str(self.itemId))
