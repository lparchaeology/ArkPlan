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
        copyright            : 2010 by Jürgen E. Fischer
        copyright            : 2007 by Marco Hugentobler
        copyright            : 2006 by Martin Dobias
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

from PyQt4.QtCore import QSettings, Qt
from PyQt4.QtGui import QAction

from qgis.core import QgsDistanceArea, QgsFeature, QgsProject, QgsVectorLayer
from qgis.gui import QgsAttributeDialog, QgsAttributeEditorContext


# TODO Clean up this and fix dialog problems
class FeatureAction(QAction):

    def __init__(self, name, feature, layer, action=-1, defaultAttr=-1, iface=None, parent=None):
        super(FeatureAction, self).__init__(name, parent)

        self._layer = layer
        self._feature = feature
        self._action = action
        self._idx = defaultAttr
        self._iface = iface
        self._featureSaved = False
        self._lastUsedValues = {}

    def execute(self):
        self._layer.actions().doAction(self._action, self._feature, self._idx)

    def _newDialog(self, cloneFeature):
        feature = QgsFeature()
        if (cloneFeature):
            feature = QgsFeature(self._feature)
        else:
            feature = self._feature

        context = QgsAttributeEditorContext()

        myDa = QgsDistanceArea()

        myDa.setSourceCrs(self._layer.crs())
        myDa.setEllipsoidalMode(self._iface.mapCanvas().mapSettings().hasCrsTransformEnabled())
        myDa.setEllipsoid(QgsProject.instance().readEntry('Measure', '/Ellipsoid', GEO_NONE)[0])

        context.setDistanceArea(myDa)
        context.setVectorLayerTools(self._iface.vectorLayerTools())

        dialog = QgsAttributeDialog(self._layer, feature, cloneFeature, None, True, context)

        if (self._layer.actions().size() > 0):
            dialog.setContextMenuPolicy(Qt.ActionsContextMenu)

            a = QAction(self.tr('Run actions'), dialog)
            a.setEnabled(False)
            dialog.addAction(a)

            i = 0
            for action in self._layer.actions():
                if (action.runable()):
                    a = FeatureAction(action.name(), feature, self._layer, i, -1, self._iface, dialog)
                    dialog.addAction(a)
                    a.triggered.connect(a.execute)
                    pb = dialog.findChild(action.name())
                    if (pb):
                        pb.clicked.connect(a.execute)
                i += 1

        return dialog

    def viewFeatureForm(self, h=0):
        if (not self._layer):
            return False
        dialog = self._newDialog(True)
        dialog.setHighlight(h)
        dialog.show()
        return True

    def editFeature(self, showModal=True):
        if (not self._layer):
            return False

        dialog = self._newDialog(False)

        if (not self._feature.isValid()):
            dialog.setIsAddDialog(True)

        if (showModal):
            dialog.setAttribute(Qt.WA_DeleteOnClose)
            rv = dialog.exec_()
            self._feature.setAttributes(dialog.feature().attributes())
            return rv
        else:
            dialog.show()
        return True

    def addFeature(self, defaultAttributes={}, showModal=True):
        if (self._layer is None or not self._layer.isEditable()):
            return False

        provider = self._layer.dataProvider()

        settings = QSettings()
        reuseLastValues = settings.value('/qgis/digitizing/reuseLastValues', False)

        fields = self._layer.pendingFields()
        self._feature.initAttributes(fields.count())
        for idx in range(0, fields.count()):
            v = None
            field = fields[idx]

            if (field.name() in defaultAttributes):
                v = defaultAttributes[field.name()]
            elif (reuseLastValues
                  and self._layer.id() in self._lastUsedValues
                  and idx in self._lastUsedValues[self._layer.id()]):
                v = self._lastUsedValues[self._layer.id()][idx]
            else:
                v = provider.defaultValue(idx)

            self._feature.setAttribute(idx, v)

        isDisabledAttributeValuesDlg = settings.value('/qgis/digitizing/disable_enter_attribute_values_dialog', False)
        if (fields.count() == 0 or self._layer.featureFormSuppress() == QgsVectorLayer.SuppressOn):
            isDisabledAttributeValuesDlg = True
        elif (self._layer.featureFormSuppress() == QgsVectorLayer.SuppressOff):
            isDisabledAttributeValuesDlg = False

        if (isDisabledAttributeValuesDlg):
            self._layer.beginEditCommand(self.text())
            self._featureSaved = self._layer.addFeature(self._feature)
            if (self._featureSaved):
                self._layer.endEditCommand()
            else:
                self._layer.destroyEditCommand()
        else:
            dialog = self._newDialog(False)
            dialog.setIsAddDialog(True)
            dialog.setEditCommandMessage(self.text())

            attributeForm = dialog.attributeForm()
            attributeForm.featureSaved.connect(self._onFeatureSaved)

            if (not showModal):
                self.setParent(dialog)
                dialog.show()
                return True

            dialog.setAttribute(Qt.WA_DeleteOnClose)
            dialog.exec_()

        return self._featureSaved

    def _onFeatureSaved(self, feature):
        self._featureSaved = True

        reuseLastValues = QSettings().value('/qgis/digitizing/reuseLastValues', False)

        if (reuseLastValues):
            fields = self._layer.pendingFields()
            for idx in range(0, fields.count() - 1):
                newValues = feature.attributes()
                origValues = self._lastUsedValues[self._layer.id()]
                if (origValues[idx] != newValues[idx]):
                    self._lastUsedValues[self._layer.id()][idx] = newValues[idx]
