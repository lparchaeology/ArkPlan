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

from qgis.PyQt.QtWidgets import QWidget

from ArkSpatial.ark.lib import utils

from .ui.digitising_widget_base import Ui_DigitisingWidget


class DigitisingWidget(QWidget, Ui_DigitisingWidget):

    def __init__(self, parent=None):
        super(DigitisingWidget, self).__init__(parent)
        self.setupUi(self)

    def initGui(self, iface):
        self.sourceWidget.initGui()
        self.planFeatureWidget.initGui(iface, 'plan')
        self.sectionFeatureWidget.initGui(iface, 'section')
        self.siteFeatureWidget.initGui(iface, 'site')
        self.sourceWidget.sourceChanged.connect(self._updateSource)

    def unloadGui(self):
        self.sourceWidget.unloadGui()
        self.planFeatureWidget.unloadGui()
        self.sectionFeatureWidget.unloadGui()
        self.siteFeatureWidget.unloadGui()
        self.sourceWidget.sourceChanged.disconnect(self._updateSource)

    def loadProject(self, plugin):
        self.sourceWidget.loadProject(plugin)
        self.planFeatureWidget.loadProject(plugin, 'plan')
        self.sectionFeatureWidget.loadProject(plugin, 'section')
        self.siteFeatureWidget.loadProject(plugin, 'site')

    def closeProject(self):
        self.sourceWidget.closeProject()
        self.planFeatureWidget.closeProject()
        self.sectionFeatureWidget.closeProject()
        self.siteFeatureWidget.closeProject()

    # Drawing Tools

    def setSource(self, source):
        self.sourceWidget.setSource(source)

    def _updateSource(self):
        source = self.sourceWidget.source()
        self.planFeatureWidget.itemFeature().setSource(source)
        self.sectionFeatureWidget.itemFeature().setSource(source)
        self.siteFeatureWidget.itemFeature().setSource(source)
