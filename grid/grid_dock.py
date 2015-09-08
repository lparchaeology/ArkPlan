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

from PyQt4 import uic
from PyQt4.QtCore import Qt, pyqtSignal
from PyQt4.QtGui import QIcon

from qgis.core import QgsPoint

from ..libarkqgis.dock import ArkDockWidget

import grid_dock_base


class GridDock(ArkDockWidget, grid_dock_base.Ui_GridDock):

    createGridSelected = pyqtSignal()
    identifyGridSelected = pyqtSignal(bool)
    updateLayerSelected = pyqtSignal()
    translateFeaturesSelected = pyqtSignal()
    panMapSelected = pyqtSignal()
    copyMapPointSelected = pyqtSignal()
    copyLocalPointSelected = pyqtSignal()
    pasteMapPointSelected = pyqtSignal()
    addMapPointSelected = pyqtSignal()
    gridSelectionChanged = pyqtSignal(str, str)
    convertMapSelected = pyqtSignal()
    convertLocalSelected = pyqtSignal()

    def __init__(self, parent=None):
        super(GridDock, self).__init__(parent)
        self.setupUi(self)

        #FIXME Hack around resource file issue, clean-up when separate plugin
        self.createGridAction.setIcon(QIcon(':/plugins/ArkGrid/get-hot-new-stuff.png'))
        self.identifyGridAction.setIcon(QIcon(':/plugins/ArkGrid/snap-orthogonal.png'))
        self.updateLayerAction.setIcon(QIcon(':/images/themes/default/mActionNewAttribute.png'))
        self.translateFeaturesAction.setIcon(QIcon(':/images/themes/default/mActionMoveFeature.png'))
        self.panToAction.setIcon(QIcon(':/images/themes/default/mActionPanToSelected.svg'))
        self.copyMapPointAction.setIcon(QIcon(':/images/themes/default/mActionEditCopy.png'))
        self.copyLocalPointAction.setIcon(QIcon(':/images/themes/default/mActionEditCopy.png'))
        self.pasteMapPointAction.setIcon(QIcon(':/images/themes/default/mActionEditPaste.png'))
        self.addMapPointAction.setIcon(QIcon(':/images/themes/default/mActionCapturePoint.png'))

        self.gridCombo.activated.connect(self.gridComboChanged)

        self.createGridTool.setDefaultAction(self.createGridAction)
        self.createGridAction.triggered.connect(self.createGridSelected)

        self.identifyGridTool.setDefaultAction(self.identifyGridAction)
        self.identifyGridAction.toggled.connect(self.identifyGridSelected)

        self.updateLayerTool.setDefaultAction(self.updateLayerAction)
        self.updateLayerAction.triggered.connect(self.updateLayerSelected)

        self.translateFeaturesTool.setDefaultAction(self.translateFeaturesAction)
        self.translateFeaturesAction.triggered.connect(self.translateFeaturesSelected)

        self.panToTool.setDefaultAction(self.panToAction)
        self.panToAction.triggered.connect(self.panMapSelected)

        self.copyMapPointTool.setDefaultAction(self.copyMapPointAction)
        self.copyMapPointAction.triggered.connect(self.copyMapPointSelected)

        self.copyLocalPointTool.setDefaultAction(self.copyLocalPointAction)
        self.copyLocalPointAction.triggered.connect(self.copyLocalPointSelected)

        self.pasteMapPointTool.setDefaultAction(self.pasteMapPointAction)
        self.pasteMapPointAction.triggered.connect(self.pasteMapPointSelected)

        self.addMapPointTool.setDefaultAction(self.addMapPointAction)
        self.addMapPointAction.triggered.connect(self.addMapPointSelected)

        self.mapEastingSpin.editingFinished.connect(self.convertMapSelected)
        self.mapNorthingSpin.editingFinished.connect(self.convertMapSelected)

        self.localEastingSpin.editingFinished.connect(self.convertLocalSelected)
        self.localNorthingSpin.editingFinished.connect(self.convertLocalSelected)

    def siteCode(self):
        data = self.gridCombo.itemData(self.gridCombo.currentIndex())
        if data is not None:
            return data[0]
        else:
            return ''

    def gridName(self):
        data = self.gridCombo.itemData(self.gridCombo.currentIndex())
        if data is not None:
            return data[1]
        else:
            return ''

    def setGridNames(self, names):
        self.gridCombo.clear()
        for name in names:
            self.gridCombo.addItem(name[0] + ' / ' + name[1], name)

    def gridComboChanged(self, i):
        data = self.gridCombo.itemData(i)
        self.gridSelectionChanged.emit(data[0], data[1])

    def mapPoint(self):
        return QgsPoint(self.mapEastingSpin.value(), self.mapNorthingSpin.value())

    def setMapPoint(self, point):
        self.mapEastingSpin.setValue(point.x())
        self.mapNorthingSpin.setValue(point.y())

    def localPoint(self):
        return QgsPoint(self.localEastingSpin.value(), self.localNorthingSpin.value())

    def setLocalPoint(self, point):
        self.localEastingSpin.setValue(point.x())
        self.localNorthingSpin.setValue(point.y())

    def setReadOnly(self, status):
        self.identifyGridAction.setEnabled(not status)
        self.updateLayerAction.setEnabled(not status)
        self.translateFeaturesAction.setEnabled(not status)
        self.panToAction.setEnabled(not status)
        self.copyMapPointAction.setEnabled(not status)
        self.copyLocalPointAction.setEnabled(not status)
        self.pasteMapPointAction.setEnabled(not status)
        self.addMapPointAction.setEnabled(not status)
        self.gridCombo.setEnabled(not status)
        self.mapEastingSpin.setReadOnly(status)
        self.mapNorthingSpin.setReadOnly(status)
        self.localEastingSpin.setReadOnly(status)
        self.localNorthingSpin.setReadOnly(status)
