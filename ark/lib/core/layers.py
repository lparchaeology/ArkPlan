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

from qgis.PyQt.QtCore import QFile, QFileInfo, QVariant
from qgis.PyQt.QtXml import QDomDocument

from qgis.core import (NULL, Qgis, QgsFeature, QgsFeatureRequest, QgsField, QgsLayerTreeGroup, QgsMapLayer,
                       QgsMapLayerRegistry, QgsProject, QgsVectorFileWriter, QgsVectorLayer, QgsWkbTypes)

from .. import utils

geometryType = {
    QgsWkbTypes.PointGeometry: QgsWkbTypes.Point25D,
    QgsWkbTypes.LineGeometry: QgsWkbTypes.LineString25D,
    QgsWkbTypes.PolygonGeometry: QgsWkbTypes.Polygon25D
}

geometryMultiType = {
    QgsWkbTypes.PointGeometry: QgsWkbTypes.MultiPoint25D,
    QgsWkbTypes.LineGeometry: QgsWkbTypes.MultiLineString25D,
    QgsWkbTypes.PolygonGeometry: QgsWkbTypes.MultiPolygon25D
}

wkbMemoryType = {
    QgsWkbTypes.Point: 'point',
    QgsWkbTypes.LineString: 'linestring',
    QgsWkbTypes.Polygon: 'polygon',
    QgsWkbTypes.MultiPoint: 'multipoint',
    QgsWkbTypes.MultiLineString: 'multilinestring',
    QgsWkbTypes.MultiPolygon: 'multipolygon',
    QgsWkbTypes.Point25D: 'point',
    QgsWkbTypes.LineString25D: 'linestring',
    QgsWkbTypes.Polygon25D: 'polygon',
    QgsWkbTypes.MultiPoint25D: 'multipoint',
    QgsWkbTypes.MultiLineString25D: 'multilinestring',
    QgsWkbTypes.MultiPolygon25D: 'multipolygon'
}


def geometryToWkbType(geometry, multi=True):
    if multi:
        return geometryMultiType.get(geometry, QgsWkbTypes.UnknownGeometry)
    return geometryType.get(geometry, QgsWkbTypes.UnknownGeometry)


def wkbToMemoryType(wkbType):
    return wkbMemoryType.get(wkbType, 'unknown')


def styleFile(name, layerPath, customPath, defaultPath):
    # Try find a style file to match a layer
    # First see if the layer itself has a default style saved
    if layerPath and name:
        filePath = styleFilePath(layerPath, name)
        if QFile.exists(filePath):
            return filePath
    # Next see if the default name has a style in the style folder
    if customPath and name:
        filePath = styleFilePath(customPath, name)
        if QFile.exists(filePath):
            return filePath
    # Finally, check the plugin folder for the default style
    if defaultPath and name:
        filePath = styleFilePath(defaultPath, name)
        if QFile.exists(filePath):
            return filePath
    # If we didn't find anything then don't use a style
    return ''


def filePath(path, name, suffix):
    return os.path.join(path, name + '.' + suffix)


def styleFilePath(path, name):
    return filePath(path, name, 'qml')


def shapeFilePath(path, name):
    return filePath(path, name, 'shp')


def loadShapefileLayer(filePath, layerName):
    layer = None
    layerList = QgsMapLayerRegistry.instance().mapLayersByName(layerName)
    if (len(layerList) > 0):
        layer = layerList[0]
    elif QFile.exists(filePath):
        layer = QgsVectorLayer(filePath, layerName, 'ogr')
    return layer


def createShapefile(filePath, name, wkbType, crs, fields, styleURI=None, symbology=None):
    # WARNING This will overwrite existing files
    writer = QgsVectorFileWriter(filePath, 'System', fields, wkbType, crs)
    if writer.hasError():
        utils.debug(writer.errorMessage())
    del writer
    layer = QgsVectorLayer(filePath, name, 'ogr')
    loadStyle(layer, styleURI, symbology)
    return layer


def createMemoryLayer(name, wkbType, crs, fields=None, styleURI=None, symbology=None):
    uri = wkbToMemoryType(wkbType) + "?crs=" + crs.authid() + "&index=yes"
    layer = QgsVectorLayer(uri, name, 'memory')
    if (layer and layer.isValid()):
        if fields:
            layer.dataProvider().addAttributes(fields.toList())
        else:
            layer.dataProvider().addAttributes([QgsField('id', QVariant.String, '', 10, 0, 'ID')])
        loadStyle(layer, styleURI, symbology)
    return layer


def copyFeatures(fromLayer, toLayer, selected=False):
    toLayer.startEditing()
    fi = None
    if selected:
        fi = fromLayer.selectedFeaturesIterator()
    else:
        fi = fromLayer.getFeatures()
    for feature in fi:
        toLayer.addFeature(feature)
    toLayer.commitChanges()
    return toLayer


def cloneAsShapefile(layer, filePath, name, styleURI=None, symbology=None):
    # WARNING This will overwrite existing files
    if (layer is not None and layer.isValid() and layer.type() == QgsMapLayer.VectorLayer):
        if styleURI is None and symbology is None:
            symbology = getSymbology(layer)
        return createShapefile(filePath,
                               name,
                               layer.wkbType(),
                               layer.crs(),
                               layer.dataProvider().fields(),
                               styleURI,
                               symbology)
    return QgsVectorLayer()


def duplicateAsShapefile(layer, filePath, name, selected=False):
    shp = cloneAsShapefile(layer, filePath, name)
    return copyFeatures(layer, shp, selected)


def cloneAsMemoryLayer(layer, name, styleURI=None, symbology=None):
    if (layer is not None and layer.isValid() and layer.type() == QgsMapLayer.VectorLayer):
        if styleURI is None and symbology is None:
            symbology = getSymbology(layer)
        mem = createMemoryLayer(name, layer.wkbType(), layer.crs(), layer.dataProvider().fields(), styleURI, symbology)
        # Hack required to keep fields defined!
        mem.startEditing()
        ft = QgsFeature(layer.dataProvider().fields())
        mem.addFeature(ft)
        mem.deleteFeature(ft.id())
        mem.commitChanges()
        return mem
    return QgsVectorLayer()


def duplicateAsMemoryLayer(layer, name, selected=False):
    mem = cloneAsMemoryLayer(layer, name)
    return copyFeatures(layer, mem, selected)


def loadStyle(layer, styleURI=None, symbology=None, fromLayer=None):
    if (layer is not None and layer.isValid() and layer.type() == QgsMapLayer.VectorLayer):
        if styleURI:
            layer.loadNamedStyle(styleURI)
        elif symbology:
            layer.readSymbology(symbology, '')
        elif fromLayer and fromLayer.isValid() and fromLayer.type() == QgsMapLayer.VectorLayer:
            copySymbology(fromLayer, layer)


def getSymbology(source):
    di = QDomImplementation()
    documentType = di.createDocumentType('qgis', 'http://mrcc.com/qgis.dtd', 'SYSTEM')
    doc = QDomDocument(documentType)
    rootNode = doc.createElement('qgis')
    rootNode.setAttribute('version', str(Qgis.QGIS_VERSION))
    doc.appendChild(rootNode)
    source.writeSymbology(rootNode, doc, '')
    return rootNode


def copySymbology(source, dest):
    dest.readSymbology(getSymbology(source), '')


def getGroupIndex(iface, groupName):
    groupIndex = -1
    i = 0
    for name in iface.legendInterface().groups():
        if (groupIndex < 0 and name == groupName):
            groupIndex = i
        i += 1
    return groupIndex


def createLayerGroup(iface, groupName, parentGroupName=''):
    groupIndex = getGroupIndex(iface, groupName)
    if (groupIndex >= 0):
        return groupIndex
    if parentGroupName:
        parentGroupIndex = getGroupIndex(iface, parentGroupName)
        if (parentGroupIndex >= 0):
            return iface.legendInterface().addGroup(groupName, True, parentGroupIndex)
    return iface.legendInterface().addGroup(groupName, True)


def getLayerId(layerName):
    layerList = QgsMapLayerRegistry.instance().mapLayersByName(layerName)
    if (len(layerList) > 0):
        return layerList[0].id()
    return None


def addLayerToLegend(iface, layer, group=-1):
    if (layer is not None and layer.isValid()):
        ret = QgsMapLayerRegistry.instance().addMapLayer(layer)
        if ret is not None:
            layer = ret
        if group >= 0:
            iface.legendInterface().moveLayer(layer, group)
        iface.legendInterface().refreshLayerSymbology(layer)
        iface.legendInterface().setLayerExpanded(layer, False)
        return layer
    return layer


def getAllFeaturesRequest(featureRequest, layer):
    # Stash the current selection
    selection = []
    if layer.selectedFeatureCount() > 0:
        selection = layer.selectedFeaturesIds()
    # Stash the current subset
    subset = layer.subsetString()
    # Clear the current subset
    if subset:
        layer.setSubsetString('')
    # Get all the features
    features = []
    for feature in layer.getFeatures(featureRequest):
        features.append(feature)
    # Restore the previous subset
    if subset:
        layer.setSubsetString(subset)
    # Restore the previous selection
    if len(selection) > 0:
        layer.select(selection)
    return features


def addFeatures(features, layer, undoMessage='Add features to layer', log=False, logLayer=None, timestamp=None):
    ok = False
    if log and (not logLayer or not timestamp):
        return ok
    if not isWritable(layer) or (logLayer and not isWritable(logLayer)):
        return ok
    # Stash the current subset
    subset = layer.subsetString()
    if subset:
        layer.setSubsetString('')
    # Copy the requested features
    wasEditing = layer.isEditable()
    if (wasEditing or layer.startEditing()) and (logLayer is None or logLayer.isEditable() or logLayer.startEditing()):
        if wasEditing:
            layer.beginEditCommand(undoMessage)
        logFeature = None
        if log:
            if wasEditing:
                logLayer.beginEditCommand(undoMessage)
        ft = 0
        for feature in features:
            ft += 1
            if log:
                logFeature = QgsFeature(logLayer.fields())
                if feature.hasGeometry():
                    logFeature.setGeometry(feature.geometry())
                for field in layer.fields():
                    logFeature.setAttribute(field.name(), feature.attribute(field.name()))
                logFeature.setAttribute('event', 'insert')
                logFeature.setAttribute('timestamp', timestamp)
                ok = logLayer.addFeature(logFeature) and layer.addFeature(feature)
            else:
                ok = layer.addFeature(feature)
        # If was already in edit mode, end or destroy the editing buffer
        if wasEditing:
            if ok:
                if log:
                    logLayer.endEditCommand()
                layer.endEditCommand()
            else:
                if log:
                    logLayer.destroyEditCommand()
                layer.destroyEditCommand()
        # If was already in edit mode, is up to caller to commit the log and layer
        if not wasEditing:
            if ok and log:
                ok = logLayer.commitChanges()
            if ok:
                ok = layer.commitChanges()
            if not ok:
                if log:
                    try:
                        logLayer.rollBack()
                    except Exception:
                        utils.logMessage('TODO: Rollback on log layer???')
                layer.rollBack()
        if ft == 0:
            ok = True
    # Restore the previous subset
    if subset:
        layer.setSubsetString(subset)
    return ok


def copyFeatureRequest(featureRequest,
                       fromLayer,
                       toLayer,
                       undoMessage='Copy features',
                       log=False,
                       logLayer=None,
                       timestamp=None):
    ok = False
    if log and (not logLayer or not timestamp):
        return ok
    if not isWritable(toLayer) or (logLayer and not isWritable(logLayer)):
        return ok
    # Stash the current subset
    fromSubset = fromLayer.subsetString()
    if fromSubset:
        fromLayer.setSubsetString('')
    toSubset = toLayer.subsetString()
    if toSubset:
        toLayer.setSubsetString('')
    # Copy the requested features
    wasEditing = toLayer.isEditable()
    isEditable = wasEditing or toLayer.startEditing()
    if (isEditable and (logLayer is None or logLayer.isEditable() or logLayer.startEditing())):
        if wasEditing:
            toLayer.beginEditCommand(undoMessage)
        logFeature = None
        if log:
            if wasEditing:
                logLayer.beginEditCommand(undoMessage)
        ft = 0
        for feature in fromLayer.getFeatures(featureRequest):
            ft += 1
            if log:
                logFeature = QgsFeature(logLayer.fields())
                if feature.hasGeometry():
                    logFeature.setGeometry(feature.geometry())
                for field in fromLayer.fields():
                    logFeature.setAttribute(field.name(), feature.attribute(field.name()))
                logFeature.setAttribute('event', 'insert')
                logFeature.setAttribute('timestamp', timestamp)
                ok = logLayer.addFeature(logFeature) and toLayer.addFeature(feature)
            else:
                ok = toLayer.addFeature(feature)
            if not ok:
                break
        # If was already in edit mode, end or destroy the editing buffer
        if wasEditing:
            if ok:
                if log:
                    logLayer.endEditCommand()
                toLayer.endEditCommand()
            else:
                if log:
                    logLayer.destroyEditCommand()
                toLayer.destroyEditCommand()
        # If was already in edit mode, is up to caller to commit the log and layer
        if not wasEditing:
            if ok and log:
                ok = logLayer.commitChanges()
            if ok:
                ok = toLayer.commitChanges()
            if not ok:
                if log:
                    try:
                        logLayer.rollBack()
                    except Exception:
                        utils.logMessage('TODO: Rollback on log layer???')
                toLayer.rollBack()
        if ft == 0:
            ok = True
    # Restore the previous selection and subset
    if fromSubset:
        fromLayer.setSubsetString(fromSubset)
    if toSubset:
        toLayer.setSubsetString(toSubset)
    return ok


def copyAllFeatures(fromLayer, toLayer, undoMessage='Copy features', log=False, logLayer=None, timestamp=None):
    return copyFeatureRequest(QgsFeatureRequest(), fromLayer, toLayer, undoMessage, log, logLayer, timestamp)


def deleteFeatureRequest(featureRequest, layer, undoMessage='Delete feature', log=False, logLayer=None, timestamp=None):
    ok = False
    if log and (not logLayer or not timestamp):
        return ok
    if not isWritable(layer) or (logLayer and not isWritable(logLayer)):
        return ok
    # Stash the current subset
    subset = layer.subsetString()
    if subset:
        layer.setSubsetString('')
    # Copy the requested features
    wasEditing = layer.isEditable()
    if (wasEditing or layer.startEditing()) and (logLayer is None or logLayer.isEditable() or logLayer.startEditing()):
        if wasEditing:
            layer.beginEditCommand(undoMessage)
        logFeature = None
        if log:
            if wasEditing:
                logLayer.beginEditCommand(undoMessage)
        ft = 0
        for feature in layer.getFeatures(featureRequest):
            ft += 1
            if log:
                logFeature = QgsFeature(logLayer.fields())
                if feature.hasGeometry():
                    logFeature.setGeometry(feature.geometry())
                for field in layer.fields():
                    logFeature.setAttribute(field.name(), feature.attribute(field.name()))
                logFeature.setAttribute('event', 'delete')
                logFeature.setAttribute('timestamp', timestamp)
                ok = logLayer.addFeature(logFeature) and layer.deleteFeature(feature.id())
            else:
                ok = layer.deleteFeature(feature.id())
            if not ok:
                break
        # If was already in edit mode, end or destroy the editing buffer
        if wasEditing:
            if ok:
                if log:
                    logLayer.endEditCommand()
                layer.endEditCommand()
            else:
                if log:
                    logLayer.destroyEditCommand()
                layer.destroyEditCommand()
        # If was already in edit mode, is up to caller to commit the log and layer
        if not wasEditing:
            if ok and log:
                ok = logLayer.commitChanges()
            if ok:
                ok = layer.commitChanges()
            if not ok:
                if log:
                    try:
                        logLayer.rollBack()
                    except Exception:
                        utils.logMessage('TODO: Rollback on log layer???')
                layer.rollBack()
        if ft == 0:
            ok = True
    # Restore the previous subset
    if subset:
        layer.setSubsetString(subset)
    return ok


def deleteAllFeatures(layer, undoMessage='Delete features', log=False, logLayer=None, timestamp=None):
    return deleteFeatureRequest(QgsFeatureRequest(), layer, undoMessage, log, logLayer, timestamp)


def childGroupIndex(parentGroupName, childGroupName):
    root = QgsProject.instance().layerTreeRoot()
    if root is None:
        return -1
    parent = root.findGroup(parentGroupName)
    if parent is None:
        return -1
    idx = 0
    for child in parent.children():
        if isinstance(child, QgsLayerTreeGroup) and child.name() == childGroupName:
            break
        idx += 1
    return idx


def insertChildGroup(parentGroupName, childGroupName, childIndex):
    root = QgsProject.instance().layerTreeRoot()
    if root is None:
        return None
    parent = root.findGroup(parentGroupName)
    if parent is None:
        return None
    return parent.insertGroup(childIndex, childGroupName)


def moveChildGroup(parentGroupName, childGroupName, childIndex):
    root = QgsProject.instance().layerTreeRoot()
    if root is None:
        return
    parent = root.findGroup(parentGroupName)
    if parent is None:
        return
    child = parent.findGroup(childGroupName)
    if child is None:
        return
    cloneChild = child.clone()
    parent.insertChildNode(childIndex, cloneChild)
    parent.removeChildNode(child)


def collapseChildren(groupName):
    root = QgsProject.instance().layerTreeRoot()
    if root is None:
        return
    group = root.findGroup(groupName)
    if group is None:
        return
    for child in group.children():
        child.setExpanded(False)


def applyFilter(iface, layer, expression):
    if (layer is None or not layer.isValid() or layer.type() != QgsMapLayer.VectorLayer):
        return
    iface.mapCanvas().stopRendering()
    layer.setSubsetString(expression)
    layer.updateExtents()
    iface.legendInterface().refreshLayerSymbology(layer)


def applyFilterRequest(layer, request):
    applyFilter(request.filterExpression().dump())


def applySelection(layer, expression):
    request = QgsFeatureRequest().setFilterExpression(expression)
    applySelectionRequest(layer, request)


def applySelectionRequest(layer, request):
    if (layer is None or not layer.isValid() or layer.type() != QgsMapLayer.VectorLayer):
        return
    fit = layer.getFeatures(request)
    layer.selectByIds([f.id() for f in fit])


def uniqueValues(layer, fieldName):
    res = set()
    if layer and layer.isValid():
        values = layer.uniqueValues(layer.lookupField(fieldName))
        for val in values:
            if val != NULL:
                res.add(val)
    return res


def updateAttribute(layer, attribute, value, expression=None):
    idx = layer.lookupField(attribute)
    fit = None
    if expression is None or expression == '':
        fit = layer.getFeatures()
    else:
        fit = layer.getFeatures(QgsFeatureRequest().setFilterExpression(expression))
    for f in fit:
        layer.changeAttributeValue(f.id(), idx, value)


def isValid(layer):
    return (layer is not None and layer.isValid() and layer.type() == QgsMapLayer.VectorLayer)


def isInvalid(layer):
    return not isValid(layer)


def isWritable(layer):
    if isInvalid(layer) or len(layer.vectorJoins()) > 0:
        return False
    if layer.storageType() == 'ESRI Shapefile':
        sourceList = layer.source().split('|')
        shpFile = QFileInfo(sourceList[0])
        baseFilePath = shpFile.canonicalPath() + '/' + shpFile.completeBaseName()
        shxFile = QFileInfo(baseFilePath + '.shx')
        dbfFile = QFileInfo(baseFilePath + '.dbf')
        return (shpFile.exists() and shpFile.isWritable()
                and shxFile.exists() and shxFile.isWritable()
                and dbfFile.exists() and dbfFile.isWritable())
    return True


def extendExtent(extent, layer):
    if (layer is not None and layer.isValid() and layer.featureCount() > 0):
        layer.updateExtents()
        layerExtent = layer.extent()
        if layerExtent.isNull() or layerExtent.isEmpty():
            return extent
        if extent is None:
            return layerExtent
        extent.combineExtentWith(layerExtent)
    return extent


def zoomToExtent(canvas, extent):
    if (extent is not None and not extent.isNull()):
        extent.scale(1.05)
        canvas.setExtent(extent)
        canvas.refresh()
