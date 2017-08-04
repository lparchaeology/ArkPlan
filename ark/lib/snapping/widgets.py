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

from PyQt4.QtCore import Qt, pyqtSignal
from PyQt4.QtGui import QWidget, QToolButton, QMenu, QDoubleSpinBox, QComboBox

from qgis.core import QGis, QgsProject, QgsMapLayer, QgsMapLayerRegistry
from qgis.gui import QgisInterface

from ..project import Project
from ..gui import DockWidget
import ..utils

import resources

# Snapping Widgets

class ControlMenu(QMenu):

    """Menu to change snapping mode
    """

    def __init__(self, parent=None):
        super(ControlMenu, self).__init__(parent)

    def keyPressEvent(self, e):
        action = self.activeAction()
        if ((e.key() == Qt.Key_Return or e.key() == Qt.Key_Enter)
            and e.modifiers() == Qt.ControlModifier and action is not None and action.isEnabled()):
            action.trigger()
        else:
            super(ControlMenu, self).keyPressEvent(e)

    def mouseReleaseEvent(self, e):
        action = self.activeAction()
        utils.logMessage('clicked!')
        if e.modifiers() == Qt.ControlModifier and action is not None and action.isEnabled():
            utils.logMessage('triggered active!')
            action.trigger()
        else:
            utils.logMessage('passed through!')
            super(ControlMenu, self).mouseReleaseEvent(e)

# Individual Project Snapping Widgets

class SnappingModeCombo(QComboBox):

    snappingModeChanged = pyqtSignal(int)

    _snapMode = ''
    _snapType = ''

    def __init__(self, parent=None):

        super(SnappingModeCombo, self).__init__(parent)

        self.addItem('Off', Snapping.Off)
        self.addItem('Current Layer', Snapping.CurrentLayer)
        self.addItem('All Layers', Snapping.AllLayers)
        self.addItem('Selected Layers', Snapping.SelectedLayers)
        self.setCurrentIndex(0)

        self._refresh()
        self.currentIndexChanged.connect(self._changed)

        # Make sure we catch changes in the main snapping dialog
        QgsProject.instance().snapSettingsChanged.connect(self._refresh)
        # If a new project is read, update to that project's setting
        QgsProject.instance().readProject.connect(self._refresh)
        self.snappingModeChanged.connect(QgsProject.instance().snapSettingsChanged)

    def currentMode(self):
        return self.itemData(self.currentIndex())

    # Private API

    def _changed(self, idx):
        mode = self.currentMode()
        if mode == Snapping.Off:
            Snapping.setProjectSnappingType(Snapping.Off)
            Snapping.setSnappingMode(Snapping.CurrentLayer)
        else:
            if self._snapMode == Snapping.Off and mode != Snapping.Off:
                Snapping.setProjectSnappingType(self._snapType)
            Snapping.setSnappingMode(mode)
        self._snapMode = mode
        self.snappingModeChanged.emit(mode)

    def _refresh(self):
        mode = Snapping.snappingMode()
        if self._snapMode == Snapping.Off and mode == Snapping.CurrentLayer:
            return
        self._snapType = Snapping.projectSnappingType()
        self._snapMode = mode
        idx = self.findData(self._snapMode)
        self.setCurrentIndex(idx)


class SnappingTypeCombo(QComboBox):

    snappingTypeChanged = pyqtSignal(int)

    def __init__(self, parent=None):

        super(SnappingTypeCombo, self).__init__(parent)

        self.addItem('Off', Snapping.Off)
        self.addItem('Vertex', Snapping.Vertex)
        self.addItem('Segment', Snapping.Segment)
        self.addItem('Vertex and Segment', Snapping.VertexAndSegment)
        self.setCurrentIndex(0)

        self._refresh()
        self.currentIndexChanged.connect(self._changed)

        # Make sure we catch changes in the main snapping dialog
        QgsProject.instance().snapSettingsChanged.connect(self._refresh)
        # If a new project is read, update to that project's setting
        QgsProject.instance().readProject.connect(self._refresh)
        self.snappingTypeChanged.connect(QgsProject.instance().snapSettingsChanged)

    # Private API

    def _changed(self, idx):
        snapType = self.itemData(self.currentIndex())
        Snapping.setProjectSnappingType(snapType)
        self.snappingTypeChanged.emit(snapType)

    def _refresh(self):
        snapType = Snapping.projectSnappingType()
        idx = self.findData(snapType)
        self.setCurrentIndex(idx)


class SnappingUnitCombo(QComboBox):

    snappingUnitChanged = pyqtSignal(int)

    def __init__(self, parent=None):

        super(SnappingUnitCombo, self).__init__(parent)

        self.addItem('Pixels', Snapping.Pixels)
        self.addItem('Layer Units', Snapping.LayerUnits)
        self.addItem('Project Units', Snapping.ProjectUnits)
        self.setCurrentIndex(0)

        self._refresh()
        self.currentIndexChanged.connect(self._changed)

        # Make sure we catch changes in the main snapping dialog
        QgsProject.instance().snapSettingsChanged.connect(self._refresh)
        # If a new project is read, update to that project's setting
        QgsProject.instance().readProject.connect(self._refresh)
        self.snappingUnitChanged.connect(QgsProject.instance().snapSettingsChanged)

    # Private API

    def _changed(self, idx):
        snapUnit = self.itemData(self.currentIndex())
        Snapping.setProjectSnappingUnit(snapUnit)
        self.snappingUnitChanged.emit(snapUnit)

    def _refresh(self):
        snapUnit = Snapping.projectSnappingUnit()
        idx = self.findData(snapUnit)
        self.setCurrentIndex(idx)


class SnappingToleranceSpinBox(QDoubleSpinBox):

    snappingToleranceChanged = pyqtSignal(float)

    _iface = None

    def __init__(self, parent=None):

        super(SnappingToleranceSpinBox, self).__init__(parent)

        self.setDecimals(5)
        self.setRange(0.0, 100000000.0)

        self._refresh()
        self.valueChanged.connect(self._changed)

        # Make sure we catch changes in the main snapping dialog
        QgsProject.instance().snapSettingsChanged.connect(self._refresh)
        # If a new project is read, update to that project's setting
        QgsProject.instance().readProject.connect(self._refresh)
        self.snappingToleranceChanged.connect(QgsProject.instance().snapSettingsChanged)

    def setIface(self, iface):
        self._iface = iface
        self._refresh()

    # Private API

    def _changed(self, idx):
        Snapping.setProjectSnappingTolerance(self.value())
        self.snappingToleranceChanged.emit(self.value())

    def _refresh(self):
        self.setValue(Snapping.projectSnappingTolerance())
        unit = Snapping.projectSnappingUnit()
        if (unit == Snapping.Pixels):
            self.setSuffix(' px')
        elif self._iface == None:
            self.setSuffix('')
        elif unit == Snapping.LayerUnits: # == MapUnits
            layerUnits = None
            mode = Snapping.snappingMode()
            if mode == Snapping.CurrentLayer:
                layerUnits = self._iface.mapCanvas().currentLayer().crs().mapUnits()
            else:
                # TODO Find out the correct option here for all_layers!
                layerUnits = self._iface.mapCanvas().mapUnits()
            suffix = _unitToSuffix(layerUnits)
            self.setSuffix(suffix)
        elif unit == Snapping.ProjectUnits:
            projectUnits = self._iface.mapCanvas().mapUnits()
            suffix = _unitToSuffix(projectUnits)
            self.setSuffix(suffix)

def _unitToSuffix(unit):
    if unit == QGis.Meters:
        return ' m'
    elif unit == QGis.Feet:
        return ' ft'
    elif unit == QGis.NauticalMiles:
        return ' NM'
    else:
        return ' °'

class LayerSnappingWidget(QWidget):

    def __init__(self, layer, parent=None):
        super(LayerSnappingWidget, self).__init__(parent)

        label = QLabel(layer.name(), self)
        spacer = QSpacerItem(20, 40, QSizePolicy.Minimum, QSizePolicy.Expanding, self)
        action = LayerSnappingAction(layer, self)
        tool = QToolButton(self)
        tool.setDefaultAction(action)

        layout = QHBoxLayout(self)
        layout.setObjectName(u'layout')
        layout.addWidget(label)
        layout.addWidget(spacer)
        layout.addWidget(tool)

        self.setLayout(layout)

class SnappingDock(DockWidget):

    _iface = None # QgisInterface()

    def __init__(self, iface, parent=None):
        super(SnappingDock, self).__init__(parent)
        self._iface = iface

        self.setWindowTitle(u'Snapping Panel')
        self.setObjectName(u'snappingDock')

        self._listWidget = QListWidget(self)
        self._listWidget.setSelectionMode(QtGui.QAbstractItemView.NoSelection)
        self._listWidget.setDropIndicatorShown(False)

        self._dockLayout = QVBoxLayout(self)
        self._dockLayout.setObjectName(u'dockLayout')
        self._dockLayout.addWidget(self._listWidget)

        self._dockContents = QWidget(self)
        self._dockContents.setObjectName(u'dockContents')
        self._dockContents.setLayout(self._dockLayout)
        self.setWidget(self._dockContents)

        # Keep up-to-date with layers added and removed
        QgsMapLayerRegistry.instance().layersAdded.connect(self._layersAdded)
        QgsMapLayerRegistry.instance().layersRemoved.connect(self._layersRemoved)

    def refresh(self):
        self._listWidget.clear()
        layers = QgsMapLayerRegistry.instance().mapLayers()
        layerIds = layers.keys()
        sorted(layerIds)
        for layerId in layerIds:
            self.addLayer(layers[layerId])

    def addLayer(self, layer):
        if (layer is None or not layer.isValid() or layer.type() != QgsMapLayer.VectorLayer):
            return
        newItem = QListWidgetItem()
        newItem.setData(Qt.UserRole, layer.id())
        newItem.setSizeHint(layerWidget.minimumSizeHint())
        self._listWidget.addItem(newItem);
        self._listWidget.setItemWidget(newItem, LayerSnappingWidget(layer, self))

    def removeLayer(self, layerId):
        for idx in range(0, self._listWidget.count() - 1):
            if self._listWidget.item(idx).data() == layerId:
                self._listWidget.takeItem(idx)
                return

    def _layersAdded(self, layers):
        for layer in layers:
            self.addLayer(layer)

    def _layersRemoved(self, layerIds):
        for idx in range(self._listWidget.count() - 1, 0):
            if self._listWidget.item(idx).data() in layerIds:
                self._listWidget.takeItem(idx)
