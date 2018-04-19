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

from PyQt4.QtCore import QDir, QFile, QFileInfo, QObject, Qt
from PyQt4.QtGui import QFileDialog

from qgis.core import QgsGeometry

from ArkSpatial.ark.lib import utils
from ArkSpatial.ark.lib.core import layers

from ArkSpatial.ark.core import Config, Drawing, Item, ItemFeature, Module, Settings, Source
from ArkSpatial.ark.core.enum import DrawingAction, FilterAction, MapAction
from ArkSpatial.ark.georef import GeorefDialog
from ArkSpatial.ark.gui import DrawingDock, SelectDrawingDialog, SnappingDock


class DrawingModule(Module):

    def __init__(self, plugin):
        super(DrawingModule, self).__init__(plugin)

        # Project settings
        self.metadata = None  # Metadata()

        # Internal variables
        self._mapAction = MapAction.MoveMap
        self._filterAction = FilterAction.ExclusiveHighlightFilter
        self._drawingAction = DrawingAction.NoDrawingAction
        self._itemLogPath = ''

    # Create the gui when the plugin is first created
    def initGui(self):
        dock = DrawingDock(self._plugin.iface.mainWindow())
        action = self._plugin.project().addDockAction(
            ':/plugins/ark/plan/drawPlans.png',
            self.tr(u'Drawing Tools'),
            callback=self.run,
            checkable=True
        )
        self._initDockGui(dock, Qt.RightDockWidgetArea, action)

        self._dock.loadAnyFileSelected.connect(self._loadAnyPlan)
        self._dock.loadRawFileSelected.connect(self._loadRawPlan)
        self._dock.loadGeoFileSelected.connect(self._loadGeoPlan)

        self._dock.resetSelected.connect(self._plugin.project().resetBuffers)
        self._dock.mergeSelected.connect(self._plugin.project().mergeBuffers)

        self.snapDock = SnappingDock(self._plugin.iface.mainWindow())
        action = self._plugin.project().addDockAction(
            ':/plugins/ark/topologicalEditing.png',
            self.tr(u'Snapping Tools'),
            callback=self.runSnapping,
            checkable=True
        )
        self.snapDock.initGui(self._plugin.iface, Qt.LeftDockWidgetArea, action)

    # Load the project settings when project is loaded
    def loadProject(self):
        # Assume layers are loaded and filters cleared
        self._dock.loadProject(self._plugin)
        self.snapDock.loadProject(self._plugin)

        # TODO Think of a better way...
        # self.metadata = Metadata(self._dock.widget.sourceWidget)
        # self.metadata.metadataChanged.connect(self.updateMapToolAttributes)

        self._initialised = True

    # Close the project
    def closeProject(self):
        # TODO Unload the drawing tools!
        self.snapDock.closeProject()
        self._dock.closeProject()
        # self.metadata.metadataChanged.disconnect(self.updateMapToolAttributes)
        self._initialised = False

    # Unload the module when plugin is unloaded
    def unloadGui(self):
        # Unload the dock
        self.snapDock.unloadGui()
        del self.snapDock
        self._dock.unloadGui()
        del self._dock
        # Reset the initialisation
        self._initialised = False

    def run(self, checked):
        if checked and self._initialised:
            self._plugin.checking().showDock(False)
        else:
            self.showDock(False)

    def runSnapping(self, checked):
        if checked and self._initialised:
            pass
        else:
            self.snapDock.menuAction().setChecked(False)

    def collection(self):
        return self._plugin.project().collection('plan')

    def _setDrawing(self, pmd):
        self.metadata.setSiteCode(pmd.siteCode)
        self.metadata.setClassCode(pmd.sourceClass)
        if pmd.sourceId > 0:
            self.metadata.setItemId(pmd.sourceId)
            self.metadata.setSourceId(pmd.sourceId)
        self.metadata.setSourceCode('drawing')
        self.metadata.setSourceClass(pmd.sourceClass)
        self.metadata.setSourceFile(pmd.filename)
        self.metadata.setEditor(Settings.userFullName())

    def _loadAnyPlan(self):
        filePaths = QFileDialog.getOpenFileNames(
            self._dock, caption='Georeference Any File', filter='Images (*.png *.xpm *.jpg)')
        for filePath in filePaths:
            self.georeferencePlan(QFileInfo(filePath), 'free')

    def _loadRawPlan(self):
        dialog = SelectDrawingDialog('context', Settings.siteCode())
        if (dialog.exec_()):
            for filePath in dialog.selectedFiles():
                self.georeferencePlan(QFileInfo(filePath))

    def _loadGeoPlan(self):
        dialog = SelectDrawingDialog('context', Settings.siteCode(), True)
        if (dialog.exec_()):
            for filePath in dialog.selectedFiles():
                geoFile = QFileInfo(filePath)
                self._setDrawing(Drawing(geoFile))
                self._plugin.project().loadGeoLayer(geoFile)

    def loadDrawing(self, item, zoomToDrawing=True):
        if not Config.classCodes[item.classCode()]['drawing']:
            return
        drawingDir = Settings.georefDrawingDir(item.classCode())
        drawingDir.setFilter(QDir.Files | QDir.NoDotAndDotDot)
        name = item.name()
        nameList = []
        nameList.append(name + '.png')
        nameList.append(name + '.tif')
        nameList.append(name + '.tiff')
        nameList.append(name + '_*.png')
        nameList.append(name + '_*.tif')
        nameList.append(name + '_*.tiff')
        drawingDir.setNameFilters(nameList)
        drawings = drawingDir.entryInfoList()
        for drawing in drawings:
            self._setDrawing(Drawing(drawing))
            self._plugin.project().loadGeoLayer(drawing, zoomToDrawing)

    def loadSourceDrawings(self, item, clearDrawings=False):
        if item.isInvalid():
            return
        sourceKeys = set()
        sourceKeys.add(item)
        itemRequest = item.featureRequest()
        for feature in self.collection().layer('polygons').getFeatures(itemRequest):
            source = Source(feature)
            if source.item().isValid():
                sourceKeys.add(source.item())
        for feature in self.collection().layer('lines').getFeatures(itemRequest):
            source = Source(feature)
            if source.item.isValid():
                sourceKeys.add(source.item())
        for feature in self.collection().layer('points').getFeatures(itemRequest):
            source = Source(feature)
            if source.item().isValid():
                sourceKeys.add(source.item())
        if clearDrawings and len(sourceKeys) > 0:
            self._plugin.project().clearDrawings()
        for sourceKey in sorted(sourceKeys):
            self.loadDrawing(sourceKey)

    # Georeference Tools

    def georeferencePlan(self, sourceFile, mode='name'):
        drawings = Config.drawings
        for drawing in drawings:
            drawings[drawing]['raw'] = Settings.rawDrawingDir(drawing)
            drawings[drawing]['geo'] = Settings.georefDrawingDir(drawing)
            drawings[drawing]['suffix'] = '_r'
            drawings[drawing]['crs'] = self._plugin.project().crs().authid()
            drawings[drawing]['grid'] = self._plugin.project().grid.layer('points')
            drawings[drawing]['local_x'] = 'local_x'
            drawings[drawing]['local_y'] = 'local_y'
        georefDialog = GeorefDialog(drawings)
        if georefDialog.loadImage(sourceFile) and georefDialog.exec_():
            geoFile = georefDialog.geoFile()
            md = georefDialog.metadata()
            md.filename = geoFile.fileName()
            self._setDrawing(md)
            self._plugin.project().loadGeoLayer(geoFile)

    def _featureNameChanged(self, featureName):
        self.metadata.setName(featureName)
        self.updateMapToolAttributes()

    def _sectionItemList(self, siteCode):
        # TODO in 2.14 use addOrderBy()
        request = self._classItemsRequest(siteCode, 'sec')
        features = layers.getAllFeaturesRequest(request, self.collection().layer('lines'))
        lst = []
        for feature in features:
            lst.append(ItemFeature(feature))
        lst.sort()
        return lst

    def _sectionLineGeometry(self, item):
        if item and item.isValid():
            request = self._categoryRequest(item, 'sln')
            features = layers.getAllFeaturesRequest(request, self.collection().layer('lines'))
            for feature in features:
                return QgsGeometry(feature.geometry())
        return QgsGeometry()

    def _sectionChanged(self, item):
        try:
            self.mapTools['scs'].setSectionGeometry(self._sectionLineGeometry(item))
        except Exception:
            pass
