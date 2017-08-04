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

from PyQt4.QtCore import pyqtSignal
from PyQt4.QtGui import QWidget, QIcon, QAction, QActionGroup, QWidgetAction, QDoubleSpinBox

from qgis.core import QGis, QgsProject, QgsMapLayer, QgsVectorLayer, QgsMapLayerRegistry
from qgis.gui import QgisInterface

from ..project import Project
import ..utils

# Snapping Actions

class ProjectSnappingEnabledAction(QAction):

    """QAction to enable snapping

    Signals:
            snapSettingsChanged(): Signal that the snapping settings has been changed by the button
    """

    snappingEnabledChanged = pyqtSignal()

    _selectedLayers = []
    _prevType = Snapping.Off

    def __init__(self, parent=None):
        """
        Initialises the snapping mode button

        Args:
            parent (QWidget): The parent widget, defaults to None.
        """

        super(ProjectSnappingEnabledAction, self).__init__(parent)

        self.setText('Toggle Snapping')
        self.setStatusTip('Enbale/disable snapping')
        self.setIcon(QIcon(':/plugins/ark/snapEnable.png'))
        self.setCheckable(True)
        self._refresh()
        self.triggered.connect(self._triggered)

        # Make sure we catch changes in the main snapping dialog
        QgsProject.instance().snapSettingsChanged.connect(self._refresh)
        # If a new project is read, update to that project's setting
        QgsProject.instance().readProject.connect(self._refresh)
        self.snappingEnabledChanged.connect(QgsProject.instance().snapSettingsChanged)

    def setInterface(self, iface):
        self._toleranceAction.setInterface(iface)

    def unload(self):
        QgsProject.instance().snapSettingsChanged.disconnect(self._refresh)
        QgsProject.instance().readProject.disconnect(self._refresh)
        self.snappingEnabledChanged.disconnect(QgsProject.instance().snapSettingsChanged)

    # Private API

    def _triggered(self, checked):
        if checked:
            if Snapping.snappingMode() == Snapping.SelectedLayers:
                Snapping.setLayerSnappingEnabledLayers(self._selectedLayers)
            else:
                Snapping.setProjectSnappingType(self._prevType)
        else:
            if Snapping.snappingMode() == Snapping.SelectedLayers:
                self._selectedLayers = Snapping.layerSnappingEnabledLayers()
                Snapping.setLayerSnappingEnabledLayers([])
            else:
                self._prevType = Snapping.projectSnappingType()
                Snapping.setProjectSnappingType(Snapping.Off)
        self.snappingEnabledChanged.emit()

    def _refresh(self):
        self.blockSignals(True)
        snapMode = Snapping.snappingMode()
        snapType = Snapping.projectSnappingType()
        if snapType != Snapping.Off:
            self._prevType = snapType
        selectedLayers = Snapping.layerSnappingEnabledLayers()
        if len(selectedLayers) > 0:
            self._selectedLayers = selectedLayers
        if snapMode == Snapping.SelectedLayers:
            self.setChecked(len(selectedLayers) > 0)
        else:
            self.setChecked(snapType != Snapping.Off)
        self.blockSignals(False)


class SnappingModeAction(QAction):

    """QAction to change Snapping Mode for a project
    """

    snappingModeChanged = pyqtSignal(int)

    def __init__(self, snapMode, parent=None):
        """Initialises the Snapping Mode Action

        Args:
            snapMode (Snapping.SnappingMode): The Snapping Mode for this action
            parent (QWidget): The parent widget, defaults to None.
        """

        super(SnappingModeAction, self).__init__(parent)

        self._snapMode = snapMode
        if snapMode == Snapping.CurrentLayer:
            self.setText('Current Layer')
            self.setStatusTip('Snap to current layer')
            self._icon = QIcon(':/plugins/ark/snapLayerCurrent.png')
        elif snapMode == Snapping.AllLayers:
            self.setText('All Layers')
            self.setStatusTip('Snap to all layers')
            self._icon = QIcon(':/plugins/ark/snapLayerAll.png')
        elif snapMode == Snapping.SelectedLayers:
            self.setText('Selected Layers')
            self.setStatusTip('Snap to selected layers')
            self._icon = QIcon(':/plugins/ark/snapLayerSelected.png')

        self.setIcon(self._icon)
        self.setCheckable(True)

        self._refresh()
        self.triggered.connect(self._triggered)

        # Make sure we catch changes in the main snapping dialog
        QgsProject.instance().snapSettingsChanged.connect(self._refresh)
        # If a new project is read, update to that project's setting
        QgsProject.instance().readProject.connect(self._refresh)
        # If we change the settings, make such others are told
        self.snappingModeChanged.connect(QgsProject.instance().snapSettingsChanged)

    def unload(self):
        self.triggered.disconnect(self._triggered)
        QgsProject.instance().snapSettingsChanged.disconnect(self._refresh)
        QgsProject.instance().readProject.disconnect(self._refresh)
        self.snappingModeChanged.disconnect(QgsProject.instance().snapSettingsChanged)

    # Private API

    def _triggered(self, checked):
        if checked:
            Snapping.setSnappingMode(self._snapMode)
            self.snappingModeChanged.emit(self._snapMode)

    def _refresh(self):
        self.blockSignals(True)
        self.setChecked(self._snapMode == Snapping.snappingMode())
        self.blockSignals(False)

class SnappingTypeAction(QAction):

    """QAction base class for Snapping Type
    """

    def __init__(self, snapType, parent=None):
        """Initialises the Snapping Type Action

        Args:
            snapType (Snapping.SnappingType): The Snapping Type for this action
            parent (QWidget): The parent widget, defaults to None.
        """

        super(SnappingTypeAction, self).__init__(parent)

        self._snapType = snapType
        if snapType == Snapping.CurrentLayer:
            self.setText('Vertex')
            self.setStatusTip('Snap to vertex')
            self._icon = QIcon(':/plugins/ark/snapVertex.png')
        elif snapType == Snapping.AllLayers:
            self.setText('Segment')
            self.setStatusTip('Snap to segment')
            self._icon = QIcon(':/plugins/ark/snapSegment.png')
        elif snapType == Snapping.SelectedLayers:
            self.setText('Vertex and Segment')
            self.setStatusTip('Snap to vertex and segment')
            self._icon = QIcon(':/plugins/ark/snapVertexSegment.png')
        self.setIcon(self._icon)
        self.setCheckable(True)

        self._refresh()
        self.triggered.connect(self._triggered)

    # Private API

    def _triggered(self, checked):
        pass

    def _refresh(self):
        pass

class ProjectSnappingTypeAction(SnappingTypeAction):

    """QAction to change Project Snapping Type for a project
    """

    snappingTypeChanged = pyqtSignal(int)

    def __init__(self, snapType, parent=None):
        """Initialises the Project Snapping Type Action

        Args:
            snapType (Snapping.SnappingType): The Snapping Type for this action
            parent (QWidget): The parent widget, defaults to None.
        """

        super(ProjectSnappingTypeAction, self).__init__(snapType, parent)

        # Make sure we catch changes in the main snapping dialog
        QgsProject.instance().snapSettingsChanged.connect(self._refresh)
        # If a new project is read, update to that project's setting
        QgsProject.instance().readProject.connect(self._refresh)
        # If we change the settings, make such others are told
        self.snappingTypeChanged.connect(QgsProject.instance().snapSettingsChanged)

    def unload(self):
        QgsProject.instance().snapSettingsChanged.disconnect(self._refresh)
        QgsProject.instance().readProject.disconnect(self._refresh)
        self.snappingTypeChanged.disconnect(QgsProject.instance().snapSettingsChanged)

    # Private API

    def _triggered(self, checked):
        if checked:
            Snapping.setProjectSnappingType(self._snapType)
            self.snappingTypeChanged.emit(self._snapType)

    def _refresh(self):
        self.blockSignals(True)
        self.setChecked(Snapping.projectSnappingType() == self._snapType)
        self.setEnabled(Snapping.snappingMode() != Snapping.SelectedLayers)
        self.blockSignals(False)

class LayerSnappingTypeAction(SnappingTypeAction):

    """QAction to change Layer Snapping Type
    """

    snappingTypeChanged = pyqtSignal(str, int)

    _layerId = ''
    _iface = None  # QgisInteface

    def __init__(self, snapLayer, snapType, parent=None):
        """Initialises the Layer Snapping Type Action

        Args:
            snapLayer (str, QgsVectorLayer or QgisInterface): The Layer ID, Layer or iface for this action, if iface then current layer used
            snapType (Snapping.SnappingType): The Snapping Type for this action
            parent (QWidget): The parent widget, defaults to None.
        """

        super(LayerSnappingTypeAction, self).__init__(snapType, parent)
        if isinstance(snapLayer, QgisInterface):
            self._iface = snapLayer
        elif isinstance(snapLayer, QgsVectorLayer):
            self._layerId = snapLayer.id()
        elif isinstance(snapLayer, str) or isinstance(snapLayer, unicode):
            self._layerId = snapLayer

        self._refresh()

        # Make sure we catch changes in the main snapping dialog
        QgsProject.instance().snapSettingsChanged.connect(self._refresh)
        # If using current layer, make sure we update when it changes
        if self._iface:
            self._iface.legendInterface().currentLayerChanged.connect(self._refresh)
        # If the layer is removed then disable the button
        QgsMapLayerRegistry.instance().layerRemoved.connect(self._layerRemoved)
        # If we change the settings, make sure others are told
        self.snappingTypeChanged.connect(QgsProject.instance().snapSettingsChanged)

    def unload(self):
        QgsProject.instance().snapSettingsChanged.disconnect(self._refresh)
        if self._iface:
            self._iface.legendInterface().currentLayerChanged.connect(self._refresh)
        QgsMapLayerRegistry.instance().layerRemoved.disconnect(self._layerRemoved)
        self.snappingTypeChanged.disconnect(QgsProject.instance().snapSettingsChanged)

    def layerId(self):
        if self._iface and self._iface.legendInterface().currentLayer():
            return self._iface.legendInterface().currentLayer().id()
        return self._layerId

    # Private API

    def _layerRemoved(self, layerId):
        if layerId == self._layerId:
            self._layerId = ''
            self.setEnabled(False)
            QgsProject.instance().snapSettingsChanged.disconnect(self._refresh)
            QgsMapLayerRegistry.instance().layerRemoved.disconnect(self._layerRemoved)
            self.snappingTypeChanged.disconnect(QgsProject.instance().snapSettingsChanged)

    def _triggered(self, checked):
        layerId = self.layerId()
        if checked and layerId:
            Snapping.setLayerSnappingType(layerId, self._snapType)
            self.snappingTypeChanged.emit(layerId, self._snapType)

    def _refresh(self):
        self.blockSignals(True)
        if self._layerId or self._iface:
            self.setChecked(Snapping.layerSnappingType(self.layerId()) == self._snapType)
            self.setEnabled(Snapping.snappingMode() == Snapping.SelectedLayers)
        else:
            self.setChecked(False)
            self.setEnabled(False)
        self.blockSignals(False)

class SnappingUnitAction(QAction):

    """QAction base class for Snapping Unit
    """

    def __init__(self, snapUnit, parent=None):
        """Initialises the Snapping Unit Action

        Args:
            snapUnits (Snapping.SnappingUnits): The Snapping Units for this action
            parent (QWidget): The parent widget, defaults to None.
        """

        super(SnappingUnitAction, self).__init__(parent)

        self._snapUnit = snapUnit
        if snapUnit == Snapping.Pixels:
            self.setText('Pixels')
            self.setStatusTip('Use pixels')
        elif snapUnit == Snapping.LayerUnits:
            self.setText('Layer Units')
            self.setStatusTip('Use layer units')
        elif snapUnit == Snapping.ProjectUnits:
            self.setText('Project Units')
            self.setStatusTip('Use project units')

        self.setCheckable(True)

        self._refresh()
        self.triggered.connect(self._triggered)

    # Private API

    def _triggered(self, checked):
        pass

    def _refresh(self):
        pass

class ProjectSnappingUnitAction(SnappingUnitAction):

    """QAction to change Snapping Unit for a project
    """

    snappingUnitChanged = pyqtSignal(int)

    def __init__(self, snapUnit, parent=None):
        """Initialises the Snapping Unit Action

        Args:
            snapUnits (Snapping.SnappingUnits): The Snapping Units for this action
            parent (QWidget): The parent widget, defaults to None.
        """

        super(ProjectSnappingUnitAction, self).__init__(snapUnit, parent)

        # Make sure we catch changes in the main snapping dialog
        QgsProject.instance().snapSettingsChanged.connect(self._refresh)
        # If a new project is read, update to that project's setting
        QgsProject.instance().readProject.connect(self._refresh)
        # If we change the settings, make such others are told
        self.snappingUnitChanged.connect(QgsProject.instance().snapSettingsChanged)

    def unload(self):
        QgsProject.instance().snapSettingsChanged.disconnect(self._refresh)
        QgsProject.instance().readProject.disconnect(self._refresh)
        self.snappingUnitChanged.disconnect(QgsProject.instance().snapSettingsChanged)

    # Private API

    def _triggered(self, checked):
        if checked:
            Snapping.setProjectSnappingUnit(self._snapUnit)
            self.snappingUnitChanged.emit(self._snapUnit)

    def _refresh(self):
        self.blockSignals(True)
        self.setChecked(Snapping.projectSnappingUnit() == self._snapUnit)
        self.setEnabled(Snapping.snappingMode() != Snapping.SelectedLayers)
        self.blockSignals(False)


class LayerSnappingUnitAction(SnappingUnitAction):

    """QAction to change Layer Snapping Unit
    """

    snappingUnitChanged = pyqtSignal(str, int)

    _layerId = ''
    _iface = None  # QgisInteface

    def __init__(self, snapLayer, snapUnit, parent=None):
        """Initialises the Snapping Unit Action

        Args:
            snapLayer (str, QgsVectorLayer or QgisInterface): The Layer ID, Layer or iface for this action, if iface then current layer used
            snapUnits (Snapping.SnappingUnits): The Snapping Units for this action
            parent (QWidget): The parent widget, defaults to None.
        """

        super(LayerSnappingUnitAction, self).__init__(snapUnit, parent)

        if isinstance(snapLayer, QgisInterface):
            self._iface = snapLayer
        elif isinstance(snapLayer, QgsVectorLayer):
            self._layerId = snapLayer.id()
        elif isinstance(snapLayer, str) or isinstance(snapLayer, unicode):
            self._layerId = snapLayer

        self._refresh()

        # Make sure we catch changes in the main snapping dialog
        QgsProject.instance().snapSettingsChanged.connect(self._refresh)
        # If using current layer, make sure we update when it changes
        if self._iface:
            self._iface.legendInterface().currentLayerChanged.connect(self._refresh)
        # If the layer is removed then disable the button
        QgsMapLayerRegistry.instance().layerRemoved.connect(self._layerRemoved)
        # If we change the settings, make such others are told
        self.snappingUnitChanged.connect(QgsProject.instance().snapSettingsChanged)

    def unload(self):
        QgsProject.instance().snapSettingsChanged.disconnect(self._refresh)
        if self._iface:
            self._iface.legendInterface().currentLayerChanged.connect(self._refresh)
        QgsMapLayerRegistry.instance().layerRemoved.disconnect(self._layerRemoved)
        self.snappingUnitChanged.disconnect(QgsProject.instance().snapSettingsChanged)

    def layerId(self):
        if self._iface and self._iface.legendInterface().currentLayer():
            return self._iface.legendInterface().currentLayer().id()
        return self._layerId

    # Private API

    def _layerRemoved(self, layerId):
        if layerId == self._layerId:
            self._layerId = ''
            self.setEnabled(False)
            QgsProject.instance().snapSettingsChanged.disconnect(self._refresh)
            QgsMapLayerRegistry.instance().layerRemoved.disconnect(self._layerRemoved)
            self.snappingUnitChanged.disconnect(QgsProject.instance().snapSettingsChanged)

    def _triggered(self, checked):
        layerId = self.layerId()
        if checked and layerId:
            Snapping.setLayerSnappingUnit(layerId, self._snapUnit)
            self.snappingUnitChanged.emit(layerId, self._snapUnit)

    def _refresh(self):
        self.blockSignals(True)
        if self._layerId or self._iface:
            self.setChecked(Snapping.layerSnappingUnit(self.layerId()) == self._snapUnit)
            self.setEnabled(Snapping.snappingMode() == Snapping.SelectedLayers)
        else:
            self.setChecked(False)
            self.setEnabled(False)
        self.blockSignals(False)

class SnappingToleranceAction(QWidgetAction):

    """QAction base class for Snapping Tolerance
    """

    snappingToleranceChanged = pyqtSignal(float)

    _iface = None

    def __init__(self, parent=None):
        """Initialises the Snapping Tolerance Editing Action

        Args:
            parent (QWidget): The parent widget, defaults to None.
        """

        super(SnappingToleranceAction, self).__init__(parent)

        self._toleranceSpin = QDoubleSpinBox(parent)
        self._toleranceSpin.setDecimals(5)
        self._toleranceSpin.setRange(0.0, 100000000.0)
        self.setDefaultWidget(self._toleranceSpin)
        self.setText('Snapping Tolerance')
        self.setStatusTip('Set the snapping tolerance')
        self._refresh()
        self._toleranceSpin.valueChanged.connect(self._changed)

    def setInterface(self, iface):
        self._iface = iface
        self._refresh()

    # Private API

    def _changed(self, tolerance):
        pass

    def _refresh(self):
        pass

class ProjectSnappingToleranceAction(SnappingToleranceAction):

    """QAction to change Project Snapping Tolerance
    """

    snappingToleranceChanged = pyqtSignal(float)

    _iface = None

    def __init__(self, parent=None):
        """Initialises the Snapping Tolerance Editing Action

        Args:
            parent (QWidget): The parent widget, defaults to None.
        """

        super(ProjectSnappingToleranceAction, self).__init__(parent)

        # Make sure we catch changes in the main snapping dialog
        QgsProject.instance().snapSettingsChanged.connect(self._refresh)
        # If a new project is read, update to that project's setting
        QgsProject.instance().readProject.connect(self._refresh)
        # If we change the settings, make such others are told
        self.snappingToleranceChanged.connect(QgsProject.instance().snapSettingsChanged)

    def unload(self):
        QgsProject.instance().snapSettingsChanged.disconnect(self._refresh)
        QgsProject.instance().readProject.disconnect(self._refresh)
        self.snappingToleranceChanged.disconnect(QgsProject.instance().snapSettingsChanged)

    def setInterface(self, iface):
        self._iface = iface
        self._refresh()

    # Private API

    def _changed(self, tolerance):
        Snapping.setProjectSnappingTolerance(tolerance)
        self.snappingToleranceChanged.emit(tolerance)

    def _refresh(self):
        self.blockSignals(True)
        self._toleranceSpin.blockSignals(True)
        self._toleranceSpin.setValue(Snapping.projectSnappingTolerance())
        unit = Snapping.projectSnappingUnit()
        if (unit == Snapping.Pixels):
            self._toleranceSpin.setSuffix(' px')
        elif self._iface == None:
            self._toleranceSpin.setSuffix('')
        elif unit == Snapping.LayerUnits: # == MapUnits
            layerUnits = None
            mode = Snapping.snappingMode()
            if mode == Snapping.CurrentLayer:
                layerUnits = self._iface.mapCanvas().currentLayer().crs().mapUnits()
            else:
                # TODO Find out the correct option here for all_layers!
                layerUnits = self._iface.mapCanvas().mapUnits()
            suffix = _unitToSuffix(layerUnits)
            self._toleranceSpin.setSuffix(suffix)
        elif unit == Snapping.ProjectUnits:
            projectUnits = self._iface.mapCanvas().mapUnits()
            suffix = _unitToSuffix(projectUnits)
            self._toleranceSpin.setSuffix(suffix)
        self.setEnabled(Snapping.snappingMode() != Snapping.SelectedLayers)
        self._toleranceSpin.blockSignals(False)
        self.blockSignals(False)

class LayerSnappingToleranceAction(SnappingToleranceAction):

    """QAction to change Layer Snapping Tolerance
    """

    snappingToleranceChanged = pyqtSignal(str, float)

    _layerId = ''
    _iface = None  # QgisInteface

    def __init__(self, snapLayer, parent=None):
        """Initialises the Snapping Tolerance Editing Action

        Args:
            snapLayer (str, QgsVectorLayer or QgisInterface): The Layer ID, Layer or iface for this action, if iface then current layer used
            parent (QWidget): The parent widget, defaults to None.
        """

        super(LayerSnappingToleranceAction, self).__init__(parent)

        if isinstance(snapLayer, QgisInterface):
            self._iface = snapLayer
        elif isinstance(snapLayer, QgsVectorLayer):
            self._layerId = snapLayer.id()
        elif isinstance(snapLayer, str) or isinstance(snapLayer, unicode):
            self._layerId = snapLayer

        self._refresh()

        # Make sure we catch changes in the main snapping dialog
        QgsProject.instance().snapSettingsChanged.connect(self._refresh)
        # If using current layer, make sure we update when it changes
        if self._iface and self._layerId == '':
            self._iface.legendInterface().currentLayerChanged.connect(self._refresh)
        # If the layer is removed then disable the button
        QgsMapLayerRegistry.instance().layerRemoved.connect(self._layerRemoved)
        # If we change the settings, make such others are told
        self.snappingToleranceChanged.connect(QgsProject.instance().snapSettingsChanged)

    def unload(self):
        QgsProject.instance().snapSettingsChanged.disconnect(self._refresh)
        if self._iface and self._layerId == '':
            self._iface.legendInterface().currentLayerChanged.disconnect(self._refresh)
        QgsMapLayerRegistry.instance().layerRemoved.disconnect(self._layerRemoved)
        self.snappingToleranceChanged.disconnect(QgsProject.instance().snapSettingsChanged)

    def layerId(self):
        if self._iface and self._layerId == '' and self._iface.legendInterface().currentLayer():
            return self._iface.legendInterface().currentLayer().id()
        return self._layerId

    def setInterface(self, iface):
        self._iface = iface
        self._refresh()

    # Private API

    def _layerRemoved(self, layerId):
        if layerId == self._layerId:
            self._layerId = ''
            self.setEnabled(False)
            QgsProject.instance().snapSettingsChanged.disconnect(self._refresh)
            QgsMapLayerRegistry.instance().layerRemoved.disconnect(self._layerRemoved)
            self.snappingToleranceChanged.disconnect(QgsProject.instance().snapSettingsChanged)

    def _changed(self, tolerance):
        layerId = self.layerId()
        if layerId:
            Snapping.setLayerSnappingTolerance(layerId, tolerance)
            self.snappingToleranceChanged.emit(layerId, tolerance)

    def _refresh(self):
        self.blockSignals(True)
        self._toleranceSpin.blockSignals(True)
        layerId = self.layerId()
        if layerId:
            self._toleranceSpin.setValue(Snapping.layerSnappingTolerance(layerId))
            unit = Snapping.layerSnappingUnit(layerId)
            if (unit == Snapping.Pixels):
                self._toleranceSpin.setSuffix(' px')
            elif self._iface == None:
                self._toleranceSpin.setSuffix('')
            elif unit == Snapping.LayerUnits:
                layerUnits = QgsMapLayerRegistry.instance().mapLayer(layerId).crs().mapUnits()
                suffix = _unitToSuffix(layerUnits)
                self._toleranceSpin.setSuffix(suffix)
            elif unit == Snapping.ProjectUnits:
                projectUnits = self._iface.mapCanvas().mapUnits()
                suffix = _unitToSuffix(projectUnits)
                self._toleranceSpin.setSuffix(suffix)
            self.setEnabled(Snapping.snappingMode() == Snapping.SelectedLayers)
        else:
            self._toleranceSpin.setValue(0.0)
            self._toleranceSpin.setSuffix('')
            self.setEnabled(False)
        self._toleranceSpin.blockSignals(False)
        self.blockSignals(False)

class LayerSnappingEnabledAction(QAction):

    """QAction for Layer Snapping Enabled
    """

    _layerId = ''
    _iface = None  # QgisInteface

    snappingEnabledChanged = pyqtSignal(str, bool)

    def __init__(self, snapLayer, parent=None):
        """Initialises the Layer Snapping Enabled Action

        Args:
            snapLayer (str, QgsVectorLayer or QgisInterface): The Layer ID, Layer or iface for this action, if iface then current layer used
            parent (QWidget): The parent widget, defaults to None.
        """

        super(LayerSnappingEnabledAction, self).__init__(parent)

        if isinstance(snapLayer, QgisInterface):
            self._iface = snapLayer
        elif isinstance(snapLayer, QgsVectorLayer):
            self._layerId = snapLayer.id()
        elif isinstance(snapLayer, str) or isinstance(snapLayer, unicode):
            self._layerId = snapLayer

        self.setCheckable(True)
        self.setText('Toggle Layer Snapping')
        self.setStatusTip('Toggle snapping on this layer')
        self.setIcon(QIcon(':/plugins/ark/snapEnable.png'))

        self._refresh()
        self.triggered.connect(self._triggered)

        # Make sure we catch changes in the main snapping dialog
        QgsProject.instance().snapSettingsChanged.connect(self._refresh)
        # If using current layer, make sure we update when it changes
        if self._iface:
            self._iface.legendInterface().currentLayerChanged.connect(self._refresh)
        # If the layer is removed then disable the button
        QgsMapLayerRegistry.instance().layerRemoved.connect(self._layerRemoved)
        # If we change the settings, make such others are told
        self.snappingEnabledChanged.connect(QgsProject.instance().snapSettingsChanged)

    def unload(self):
        self._layerRemoved(self._layerId)
        if self._iface:
            self._iface.legendInterface().currentLayerChanged.disconnect(self._refresh)

    def layerId(self):
        if self._iface and self._iface.legendInterface().currentLayer():
            return self._iface.legendInterface().currentLayer().id()
        return self._layerId

    # Private API

    def _layerRemoved(self, layerId):
        if self._layerId and layerId == self._layerId:
            self._layerId = ''
            self.setEnabled(False)
            QgsProject.instance().snapSettingsChanged.disconnect(self._refresh)
            QgsMapLayerRegistry.instance().layerRemoved.disconnect(self._layerRemoved)
            self.snappingEnabledChanged.disconnect(QgsProject.instance().snapSettingsChanged)

    def _triggered(self, status):
        layerId = self.layerId()
        utils.logMessage('_triggered ' + utils.printable(layerId))
        if layerId:
            Snapping.setLayerSnappingEnabled(layerId, status)
            self.snappingEnabledChanged.emit(layerId, status)

    def _refresh(self):
        self.blockSignals(True)
        if self._layerId or self._iface:
            self.setChecked(Snapping.layerSnappingEnabled(self.layerId()))
            self.setEnabled(Snapping.snappingMode() == Snapping.SelectedLayers)
        else:
            self.setChecked(False)
            self.setEnabled(False)
        self.blockSignals(False)


class LayerSnappingAvoidIntersectionsAction(QAction):

    """QAction to toggle Layer Avoid Intersections
    """

    _layerId = ''
    _iface = None  # QgisInteface

    avoidIntersectionsChanged = pyqtSignal(str, bool)

    def __init__(self, snapLayer, parent=None):
        """Initialises the Layer Avoid Intersections Action

        Args:
            snapLayer (str, QgsVectorLayer or QgisInterface): The Layer ID, Layer or iface for this action, if iface then current layer used
            parent (QWidget): The parent widget, defaults to None.
        """

        super(LayerSnappingAvoidIntersectionsAction, self).__init__(parent)

        if isinstance(snapLayer, QgisInterface):
            self._iface = snapLayer
        elif isinstance(snapLayer, QgsVectorLayer):
            self._layerId = snapLayer.id()
        elif isinstance(snapLayer, str) or isinstance(snapLayer, unicode):
            self._layerId = snapLayer

        self.setCheckable(True)
        self.setText('Snap overlapping edges')
        self.setStatusTip('Snap to edges of any overlapping polygons, aka "Avoid Intersections"')

        self._refresh()
        self.triggered.connect(self._triggered)

        # Make sure we catch changes in the main snapping dialog
        QgsProject.instance().snapSettingsChanged.connect(self._refresh)
        # If using current layer, make sure we update when it changes
        if self._iface:
            self._iface.legendInterface().currentLayerChanged.connect(self._refresh)
        # If the layer is removed then disable the button
        QgsMapLayerRegistry.instance().layerRemoved.connect(self._layerRemoved)
        # If we change the settings, make such others are told
        self.avoidIntersectionsChanged.connect(QgsProject.instance().snapSettingsChanged)

    def unload(self):
        QgsProject.instance().snapSettingsChanged.disconnect(self._refresh)
        if self._iface:
            self._iface.legendInterface().currentLayerChanged.disconnect(self._refresh)
        QgsMapLayerRegistry.instance().layerRemoved.disconnect(self._layerRemoved)
        self.avoidIntersectionsChanged.disconnect(QgsProject.instance().snapSettingsChanged)

    def layerId(self):
        if self._iface and self._iface.legendInterface().currentLayer():
            return self._iface.legendInterface().currentLayer().id()
        return self._layerId

    # Private API

    def _layerRemoved(self, layerId):
        if layerId == self._layerId:
            self._layerId = ''
            self.setEnabled(False)
            QgsProject.instance().snapSettingsChanged.disconnect(self._refresh)
            QgsMapLayerRegistry.instance().layerRemoved.disconnect(self._layerRemoved)
            self.avoidIntersectionsChanged.disconnect(QgsProject.instance().snapSettingsChanged)

    def _triggered(self, status):
        layerId = self.layerId()
        if checked and layerId:
            Snapping.setLayerSnappingAvoidIntersections(layerId, status)
            self.avoidIntersectionsChanged.emit(layerId, status)

    def _refresh(self):
        self.blockSignals(True)
        if self._layerId or self._iface:
            self.setChecked(Snapping.layerSnappingAvoidIntersections(self.layerId()))
            self.setEnabled(Snapping.snappingMode() == Snapping.SelectedLayers)
        else:
            self.setChecked(False)
            self.setEnabled(False)
        self.blockSignals(False)


class TopologicalEditingAction(QAction):

    """QAction to toggle Topological Editing for a project
    """

    topologicalEditingChanged = pyqtSignal(bool)

    def __init__(self, parent=None):
        """Initialises the Topological Editing Action

        Args:
            parent (QWidget): The parent widget, defaults to None.
        """

        super(TopologicalEditingAction, self).__init__(parent)

        self.setCheckable(True)
        self._icon = QIcon(':/plugins/ark/topologicalEditing.png')
        self.setIcon(self._icon)
        self.setText('Topological Editing')

        self._refresh()
        self.triggered.connect(self._triggered)

        # Make sure we catch changes in the main snapping dialog
        QgsProject.instance().snapSettingsChanged.connect(self._refresh)
        # If a new project is read, update to that project's setting
        QgsProject.instance().readProject.connect(self._refresh)
        # If we change the settings, make such others are told
        self.topologicalEditingChanged.connect(QgsProject.instance().snapSettingsChanged)

    def unload(self):
        QgsProject.instance().snapSettingsChanged.disconnect(self._refresh)
        QgsProject.instance().readProject.disconnect(self._refresh)
        self.topologicalEditingChanged.disconnect(QgsProject.instance().snapSettingsChanged)

    # Private API

    def _triggered(self, status):
        Snapping.setTopologicalEditing(status)
        self.topologicalEditingChanged.emit(status)

    def _refresh(self):
        self.blockSignals(True)
        self.setChecked(Snapping.topologicalEditing())
        self.blockSignals(False)

class IntersectionSnappingAction(QAction):

    """QAction to toggle Intersection Snapping for a project
    """

    intersectionSnappingChanged = pyqtSignal(bool)

    def __init__(self, parent=None):
        """Initialises the Intersection Snapping Action

        Args:
            parent (QWidget): The parent widget, defaults to None.
        """

        super(IntersectionSnappingAction, self).__init__(parent)

        self.setCheckable(True)
        self._icon = QIcon(':/plugins/ark/snapIntersections.png')
        self.setIcon(self._icon)
        self.setText('Intersection Snapping')

        self._refresh()
        self.triggered.connect(self._triggered)

        # Make sure we catch changes in the main snapping dialog
        QgsProject.instance().snapSettingsChanged.connect(self._refresh)
        # If a new project is read, update to that project's setting
        QgsProject.instance().readProject.connect(self._refresh)
        # If we change the settings, make such others are told
        self.intersectionSnappingChanged.connect(QgsProject.instance().snapSettingsChanged)

    def unload(self):
        QgsProject.instance().snapSettingsChanged.disconnect(self._refresh)
        QgsProject.instance().readProject.disconnect(self._refresh)
        self.intersectionSnappingChanged.disconnect(QgsProject.instance().snapSettingsChanged)

    # Private API

    def _triggered(self, status):
        Snapping.setIntersectionSnapping(status)
        self.intersectionSnappingChanged.emit(status)

    def _refresh(self):
        self.blockSignals(True)
        self.setChecked(Snapping.intersectionSnapping())
        self.blockSignals(False)

class ProjectSnappingAction(ProjectSnappingEnabledAction):

    """QAction to configure snapping

    Signals:
            snapSettingsChanged(): Signal that the snapping settings has been changed by the action
    """

    snapSettingsChanged = pyqtSignal()

    def __init__(self, parent=None):
        """
        Initialises the snapping mode button

        Args:
            parent (QWidget): The parent widget, defaults to None.
        """

        super(ProjectSnappingAction, self).__init__(parent)
        self.setCheckable(True)

        self._currentAction = SnappingModeAction(Snapping.CurrentLayer, self)
        self._allAction = SnappingModeAction(Snapping.AllLayers, self)
        self._selectedAction = SnappingModeAction(Snapping.SelectedLayers, self)

        self._snappingModeActionGroup = QActionGroup(self)
        self._snappingModeActionGroup.addAction(self._currentAction)
        self._snappingModeActionGroup.addAction(self._allAction)
        self._snappingModeActionGroup.addAction(self._selectedAction)

        self._vertexAction = ProjectSnappingTypeAction(Snapping.Vertex, self)
        self._segmentAction = ProjectSnappingTypeAction(Snapping.Segment, self)
        self._vertexSegmentAction = ProjectSnappingTypeAction(Snapping.VertexAndSegment, self)

        self._snappingTypeActionGroup = QActionGroup(self)
        self._snappingTypeActionGroup.addAction(self._vertexAction)
        self._snappingTypeActionGroup.addAction(self._segmentAction)
        self._snappingTypeActionGroup.addAction(self._vertexSegmentAction)

        self._pixelUnitsAction = ProjectSnappingUnitAction(Snapping.Pixels, self)
        self._layerUnitsAction = ProjectSnappingUnitAction(Snapping.LayerUnits, self)
        self._projectUnitsAction = ProjectSnappingUnitAction(Snapping.ProjectUnits, self)

        self._unitTypeActionGroup = QActionGroup(self)
        self._unitTypeActionGroup.addAction(self._pixelUnitsAction)
        self._unitTypeActionGroup.addAction(self._layerUnitsAction)
        self._unitTypeActionGroup.addAction(self._projectUnitsAction)

        self._toleranceAction = ProjectSnappingToleranceAction(parent)

        menu = ControlMenu(parent)
        menu.addActions(self._snappingModeActionGroup.actions())
        menu.addSeparator()
        menu.addActions(self._snappingTypeActionGroup.actions())
        menu.addSeparator()
        menu.addAction(self._toleranceAction)
        menu.addActions(self._unitTypeActionGroup.actions())
        self.setMenu(menu)

        self._refreshAction()

        # Make sure we catch changes in the main snapping dialog
        QgsProject.instance().snapSettingsChanged.connect(self._refreshAction)

    def setInterface(self, iface):
        self._toleranceAction.setInterface(iface)

    def unload(self):
        super(ProjectSnappingAction, self).unload()
        self._currentAction.unload()
        self._allAction.unload()
        self._selectedAction.unload()
        self._vertexAction.unload()
        self._segmentAction.unload()
        self._vertexSegmentAction.unload()
        self._pixelUnitsAction.unload()
        self._layerUnitsAction.unload()
        self._projectUnitsAction.unload()
        self._toleranceAction.unload()
        QgsProject.instance().snapSettingsChanged.disconnect(self._refreshAction)

    # Private API

    def _refreshAction(self):
        snapMode = Snapping.snappingMode()
        if snapMode == Snapping.SelectedLayers:
            self.setIcon(self._selectedAction.icon())
        elif snapMode == Snapping.CurrentLayer:
            self.setIcon(self._currentAction.icon())
        elif snapMode == Snapping.AllLayers:
            self.setIcon(self._allAction.icon())

class LayerSnappingAction(LayerSnappingEnabledAction):

    """Action to change snapping settings for a QGIS vector layer

    Signals:
        snapSettingsChanged(str): Signal that the layer's snap settings have been changed by the button
    """

    snapSettingsChanged = pyqtSignal(str)

    _toleranceAction = None # LayerSnappingToleranceAction()
    _avoidAction = None  # LayerSnappingAvoidIntersectionsAction()

    def __init__(self, snapLayer, parent=None):
        """Initialises the snapping action

        After creating the button, you must call setLayer().

        Args:
            parent (QWidget): The parent widget, defaults to None.
        """

        super(LayerSnappingAction, self).__init__(snapLayer, parent)

        self._vertexAction = LayerSnappingTypeAction(snapLayer, Snapping.Vertex, self)
        self._segmentAction = LayerSnappingTypeAction(snapLayer, Snapping.Segment, self)
        self._vertexSegmentAction = LayerSnappingTypeAction(snapLayer, Snapping.VertexAndSegment, self)

        self._snappingTypeActionGroup = QActionGroup(self)
        self._snappingTypeActionGroup.addAction(self._vertexAction)
        self._snappingTypeActionGroup.addAction(self._segmentAction)
        self._snappingTypeActionGroup.addAction(self._vertexSegmentAction)

        self._toleranceAction = LayerSnappingToleranceAction(snapLayer, parent)

        self._pixelUnitsAction = LayerSnappingUnitAction(snapLayer, Snapping.Pixels, self)
        self._layerUnitsAction = LayerSnappingUnitAction(snapLayer, Snapping.LayerUnits, self)
        self._projectUnitsAction = LayerSnappingUnitAction(snapLayer, Snapping.ProjectUnits, self)

        self._unitTypeActionGroup = QActionGroup(self)
        self._unitTypeActionGroup.addAction(self._pixelUnitsAction)
        self._unitTypeActionGroup.addAction(self._layerUnitsAction)
        self._unitTypeActionGroup.addAction(self._projectUnitsAction)

        menu = ControlMenu(parent)
        menu.addActions(self._snappingTypeActionGroup.actions())
        menu.addSeparator()
        menu.addAction(self._toleranceAction)
        menu.addActions(self._unitTypeActionGroup.actions())
        if isinstance(snapLayer, QgisInterface) or (isinstance(snapLayer, QgsVectorLayer) and snapLayer.geometryType() == QGis.Polygon):
            self._avoidAction = LayerSnappingAvoidIntersectionsAction(snapLayer, self)
            menu.addSeparator()
            menu.addAction(self._avoidAction)
        self.setMenu(menu)

        self._refreshAction()

        # Make sure we catch changes in the main snapping dialog
        QgsProject.instance().snapSettingsChanged.connect(self._refreshAction)
        # If using current layer, make sure we update when it changes
        if self._iface:
            self._iface.legendInterface().currentLayerChanged.connect(self._refreshAction)
        # If any of the settings change then signal, but don't tell project as actions already have
        self.snappingEnabledChanged.connect(self.snapSettingsChanged)
        self._vertexAction.snappingTypeChanged.connect(self.snapSettingsChanged)
        self._segmentAction.snappingTypeChanged.connect(self.snapSettingsChanged)
        self._vertexSegmentAction.snappingTypeChanged.connect(self.snapSettingsChanged)
        self._toleranceAction.snappingToleranceChanged.connect(self.snapSettingsChanged)
        self._pixelUnitsAction.snappingUnitChanged.connect(self.snapSettingsChanged)
        self._layerUnitsAction.snappingUnitChanged.connect(self.snapSettingsChanged)
        self._projectUnitsAction.snappingUnitChanged.connect(self.snapSettingsChanged)
        if self._avoidAction:
            self._avoidAction.avoidIntersectionsChanged.connect(self.snapSettingsChanged)

    def setInterface(self, iface):
        self._toleranceAction.setInterface(iface)

    def unload(self):
        if not self._layerId:
            return
        super(LayerSnappingAction, self).unload()
        QgsProject.instance().snapSettingsChanged.disconnect(self._refreshAction)
        self.snappingEnabledChanged.disconnect(self.snapSettingsChanged)
        self._vertexAction.snappingTypeChanged.disconnect(self.snapSettingsChanged)
        self._segmentAction.snappingTypeChanged.disconnect(self.snapSettingsChanged)
        self._vertexSegmentAction.snappingTypeChanged.disconnect(self.snapSettingsChanged)
        self._toleranceAction.snappingToleranceChanged.disconnect(self.snapSettingsChanged)
        self._pixelUnitsAction.snappingUnitChanged.disconnect(self.snapSettingsChanged)
        self._layerUnitsAction.snappingUnitChanged.disconnect(self.snapSettingsChanged)
        self._projectUnitsAction.snappingUnitChanged.disconnect(self.snapSettingsChanged)
        if self._avoidAction:
            self._avoidAction.avoidIntersectionsChanged.disconnect(self.snapSettingsChanged)
        self._vertexAction.unload()
        self._segmentAction.unload()
        self._vertexSegmentAction.unload()
        self._toleranceAction.unload()
        self._pixelUnitsAction.unload()
        self._layerUnitsAction.unload()
        self._projectUnitsAction.unload()

    # Private API

    def _refreshAction(self):
        if (self._segmentAction.isChecked()):
            self.setIcon(self._segmentAction.icon())
        elif (self._vertexSegmentAction.isChecked()):
            self.setIcon(self._vertexSegmentAction.icon())
        else: # Snapping.Vertex or undefined
            self.setIcon(self._vertexAction.icon())
        if self._iface and self._avoidAction:
            layer = QgsMapLayerRegistry.instance().mapLayer(self.layerId())
            isPolygon = (not layer is None and layer.type() == QgsMapLayer.VectorLayer and layer.geometryType() == QGis.Polygon)
            self._avoidAction.setEnabled(isPolygon)
