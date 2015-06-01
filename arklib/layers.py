# -*- coding: utf-8 -*-
"""
/***************************************************************************
                                      Ark
                                 A QGIS plugin
             QGIS Plugin for ARK, the Archaeological Recording Kit
                              -------------------
        begin                : 2015-03-02
        git sha              : $Format:%H$
        copyright            : (C) 2015 by L - P: Heritage LLP
        copyright            : (C) 2015 by John Layt
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
from PyQt4.QtGui import QDialog, QComboBox, QDialogButtonBox

from qgis.core import QGis, QgsMapLayer, QgsMapLayerRegistry, QgsVectorLayer, QgsVectorFileWriter

# Layer Widgets

class ArkLayerComboBox(QComboBox):

    layerChanged = pyqtSignal()

    _layerType = None
    _geometryType = None
    _iface = None

    def __init__(self, iface, layerType=None, geometryType=None, parent=None):
        super(ArkLayerComboBox, self).__init__(parent)
        self._iface = iface
        self._layerType = layerType
        self._geometryType = geometryType
        self._loadLayers()

    def _addLayer(self, layer):
        self.addItem(layer.name(), layer.id())

    def _loadLayers(self):
        self.clear()
        for layer in self._iface.legendInterface().layers():
            if self._layerType is None and self._geometryType is None:
                self._addLayer(layer)
            elif (self._layerType == QgsMapLayer.RasterLayer and layer.type() == QgsMapLayer.RasterLayer):
                self._addLayer(layer)
            elif layer.type() == QgsMapLayer.VectorLayer:
                if (self._geometryType == None or layer.geometryType() == self._geometryType):
                    self._addLayer(layer)


class ArkSelectLayerDialog(QDialog):

    def __init__(self, iface, text='', label='', layerType=None, geometryType=None, parent=None):

        self.setWindowTitle(self.tr("Select Layer"))

        self._dialogLayout = QtGui.QVBoxLayout(self)

        if text:
            self._textLabel = QtGui.QLabel(self)
            self._textLabel.setText(text)
            self._dialogLayout.addWidget(self._textLabel)

        if (label or not text):
            self._comboLabel = QtGui.QLabel(self)
            if label:
                self._comboLabel.setText(label)
            elif not text:
                self._comboLabel.setText(self.tr('Layer:'))
            self._comboBox = ArkLayerComboBox(iface, layerType, geometryType, self)
            self._comboLayout = QtGui.QHBoxLayout()
            self._comboLayout.addWidget(self._comboLabel)
            self._comboLayout.addWidget(self._comboBox)
            self._dialogLayout.addLayout(self._comboLayout)
        else:
            self._comboBox = ArkLayerComboBox(iface, layerType, geometryType, self)
            self._dialogLayout.addWidget(self._comboBox)

        self._buttonBox = QDialogButtonBox(QDialogButtonBox.Ok | QDialogButtonBox.Cancel, Qt.Horizontal, self)
        self._buttonBox.accepted.connect(self.accept)
        self._buttonBox.rejected.connect(self.reject)
        self._comboLayout.addWidget(self._buttonBox)

    def layer(self):
        return QgsMapLayerRegistry.instance().mapLayer(self.layerId())

    def layerName(self):
        return self.layerComboBox.currentText()

    def layerId(self):
        return self.layerComboBox.itemData(self.layerComboBox.currentIndex())


# Layer management utilities

def createShapefile(filePath, wkbType, crs, fields):
    # WARNING This will overwrite existing files
    layer = QgsVectorFileWriter(filePath, 'System', fields, wkbType, crs)
    error = layer.hasError()
    del layer
    return error

def createMemoryLayer(name, wkbType, crsId, fields=None, styleURI=None):
    uri = wkbToMemoryType(wkbType) + "?crs=" + crsId + "&index=yes"
    mem = QgsVectorLayer(uri, name, 'memory')
    if (mem is not None and mem.isValid()):
        if fields:
            mem.dataProvider().addAttributes(fields.toList())
        else:
            mem.dataProvider().addAttributes([QgsField('id', QVariant.String, '', 10, 0, 'ID')])
        if styleURI:
            mem.loadNamedStyle(styleURI)
    return mem

def cloneAsMemoryLayer(layer, name, styleURI=None):
    if (layer is not None and layer.isValid() and layer.type() == QgsMapLayer.VectorLayer):
        if not styleURI:
            styleURI = layer.styleURI()
        return createMemoryLayer(name, layer.wkbType(), layer.crs().authid(), layer.dataProvider().fields(), styleURI)
    return None

def groupNameIndex(iface, groupName):
    groupIndex = -1
    i = 0
    for name in iface.legendInterface().groups():
        if (groupIndex < 0 and name == groupName):
            groupIndex = i
        i += 1
    if (groupIndex < 0):
        groupIndex = iface.legendInterface().addGroup(groupName)
    return groupIndex

def getLayerId(layerName):
    layerList = QgsMapLayerRegistry.instance().mapLayersByName(layerName)
    if (len(layerList) > 0):
        return layerList[0].id()
    return None

def addLayerToLegend(iface, layer, group):
    if (layer is not None and layer.isValid()):
        ret = QgsMapLayerRegistry.instance().addMapLayer(layer)
        iface.legendInterface().moveLayer(layer, group)
        iface.legendInterface().refreshLayerSymbology(layer)
        return ret
    return layer

def wkbToMemoryType(wkbType):
    if (wkbType == QGis.WKBPoint):
        return 'point'
    elif (wkbType == QGis.WKBLineString):
        return 'linestring'
    elif (wkbType == QGis.WKBPolygon):
        return 'polygon'
    elif (wkbType == QGis.WKBMultiPoint):
        return 'multipoint'
    elif (wkbType == QGis.WKBMultiLineString):
        return 'multilinestring'
    elif (wkbType == QGis.WKBMultiPolygon):
        return 'multipolygon'
    elif (wkbType == QGis.WKBPoint25D):
        return 'point'
    elif (wkbType == QGis.WKBLineString25D):
        return 'linestring'
    elif (wkbType == QGis.WKBPolygon25D):
        return 'polygon'
    elif (wkbType == QGis.WKBMultiPoint25D):
        return 'multipoint'
    elif (wkbType == QGis.WKBMultiLineString25D):
        return 'multilinestring'
    elif (wkbType == QGis.WKBMultiPolygon25D):
        return 'multipolygon'
    return 'unknown'
