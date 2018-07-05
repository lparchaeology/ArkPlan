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

from ArkSpatial.ark.lib import Application, Plugin, utils
from ArkSpatial.ark.lib.snapping import (IntersectionSnappingAction, ProjectSnappingAction, Snapping,
                                         TopologicalEditingAction)

from ArkSpatial.ark.core import Config, Settings
from ArkSpatial.ark.grid import GridModule
from ArkSpatial.ark.gui import PreferencesDialog, PreferencesWizard

from .checking_module import CheckingModule
from .data_module import DataModule
from .drawing_module import DrawingModule
from .filter_module import FilterModule
from .project_module import ProjectModule
from .trench_module import TrenchModule
from . import georef.ui.resources
from . import grid.ui.resources
from . import gui.ui.resources
from . import lib.snapping.resources


class ArkSpatialPlugin(Plugin):

    """QGIS Plugin Implementation."""

    def __init__(self, iface, pluginPath):
        super(ArkSpatialPlugin, self).__init__(
            iface=iface,
            pluginName=Config.pluginName,
            pluginScope=Config.pluginScope,
            pluginIconPath=':/plugins/ark/icon.png',
            pluginPath=pluginPath,
            menuGroup=Plugin.PluginsGroup,
            toolbarGroup=Plugin.PluginsGroup,
            checkable=True
        )

        # Modules
        self._checkingModule = None  # CheckingModule()
        self._dataModule = None  # DataModule()
        self._drawingModule = None  # DrawingModule()
        self._filterModule = None  # FilterModule()
        self._gridModule = None  # GridModule()
        self._projectModule = None  # ProjectModule()
        self._trenchModule = None  # TrenchModule()

        # Private settings
        self._initialised = False
        self._loaded = False

        # Set display / menu name now we have tr() set up
        self.setDisplayName(self.tr(u'&ARK Spatial BETA'))

        # Menu Actions
        # TODO Snapping Tools - Make own plugin!
        self._snappingAction = ProjectSnappingAction(iface.mainWindow())
        self._snappingAction.setInterface(iface)
        self.iface.addToolBarIcon(self._snappingAction)
        self._interAction = IntersectionSnappingAction(iface.mainWindow())
        self.iface.addToolBarIcon(self._interAction)
        self._topoAction = TopologicalEditingAction(iface.mainWindow())
        self.iface.addToolBarIcon(self._topoAction)

    def isInitialised(self):
        return self._initialised

    def isLoaded(self):
        return self._loaded

    # Load the plugin gui
    def initGui(self):
        super(ArkSpatialPlugin, self).initGui()

        # Init the project dock so we have something to show on first run
        self._projectModule = ProjectModule(self)
        self._projectModule.initGui()
        self.addNewAction(':/plugins/ark/settings.svg', self.tr(u'Preferences'),
                          self.configurePlugin, addToToolbar=False)

    # Initialise plugin gui
    def initialise(self):
        if self._initialised:
            return True

        # Init the modules and add to the toolbar
        self._dataModule = DataModule(self)
        self._dataModule.initGui()
        self._projectModule.addDockSeparator()
        self._gridModule = GridModule(self)
        self._gridModule.initGui()
        self._filterModule = FilterModule(self)
        self._filterModule.initGui()
        self._drawingModule = DrawingModule(self)
        self._drawingModule.initGui()
        self._checkingModule = CheckingModule(self)
        self._checkingModule.initGui()
        self._trenchModule = TrenchModule(self)
        self._trenchModule.initGui()

        # If the project or layers or legend indexes change make sure we stay updated
        self.iface.projectRead.connect(self.loadProject)
        self.iface.newProjectCreated.connect(self.closeProject)

        self._initialised = True
        return self._initialised

    # Load the project settings when project is loaded
    def loadProject(self):
        if self.isLoaded():
            return
        if self.isInitialised() and self._projectModule.loadProject():
            self._checkingModule.loadProject()
            self._dataModule.loadProject()
            self._drawingModule.loadProject()
            self._filterModule.loadProject()
            self._gridModule.loadProject()
            self._trenchModule.loadProject()
            self._loaded = True

    # Write the project for saving
    def writeProject(self):
        if self.isLoaded():
            self._checkingModule.writeProject()
            self._dataModule.writeProject()
            self._drawingModule.writeProject()
            self._filterModule.writeProject()
            self._gridModule.writeProject()
            self._trenchModule.writeProject()
            # Always do project last
            self._projectModule.writeProject()

    # Close the project
    def closeProject(self):
        if self.isLoaded():
            self.writeProject()
            self.iface.actionPan().trigger()
            self._checkingModule.closeProject()
            self._dataModule.closeProject()
            self._drawingModule.closeProject()
            self._filterModule.closeProject()
            self._gridModule.closeProject()
            self._trenchModule.closeProject()
            # Always do project last
            self._projectModule.closeProject()
            self._loaded = False

    # Unload the plugin
    def unload(self):
        self.iface.actionPan().trigger()
        if self.isInitialised():
            self.closeProject()

            # Restore the original QGIS gui
            self.pluginAction.setChecked(False)

            # Unload the modules in dependence order
            self._checkingModule.unloadGui()
            self._dataModule.unloadGui()
            self._drawingModule.unloadGui()
            self._filterModule.unloadGui()
            self._gridModule.unloadGui()
            self._trenchModule.unloadGui()
            self._projectModule.unloadGui()

            self._initialised = False

        self.iface.removeToolBarIcon(self._snappingAction)
        self._snappingAction.unload()
        del self._snappingAction
        self.iface.removeToolBarIcon(self._interAction)
        self._interAction.unload()
        del self._interAction
        self.iface.removeToolBarIcon(self._topoAction)
        self._topoAction.unload()
        del self._topoAction

        # Removes the plugin menu item and icon from QGIS GUI.
        super(ArkSpatialPlugin, self).unload()

    def run(self, checked):
        if checked and self.initialise() and self.configure():
            if not self._loaded:
                self.loadProject()
        else:
            if self._initialised:
                self.iface.actionPan().trigger()
                self._dataModule.showDock(False)
                self._drawingModule.showDock(False)
                self._checkingModule.showDock(False)
                self._gridModule.showDock(False)
                self._filterModule.showDock(False)
                self._trenchModule.showDock(False)
                self._projectModule.showDock(False)

    def project(self):
        return self._projectModule

    def data(self):
        return self._dataModule

    def filter(self):
        return self._filterModule

    def grid(self):
        return self._gridModule

    def checking(self):
        return self._checkingModule

    def drawing(self):
        return self._drawingModule

    def configurePlugin(self):
        if Settings.isPluginConfigured():
            prefs = PreferencesDialog(self.iface.mainWindow())
        else:
            prefs = PreferencesWizard(self.iface.mainWindow())

        ok = prefs.exec_() and prefs.preferences().projectsDir().exists()

        if ok:
            Settings.setUserFullName(prefs.preferences().userFullName())
            Settings.setUserInitials(prefs.preferences().userInitials())
            Settings.setUserOrganisation(prefs.preferences().userOrganisation())
            Settings.setProjectsFolder(prefs.preferences().projectsFolder())

            Settings.setServerUrl(prefs.server().url())
            Settings.setServerCredentials(prefs.server().user(), prefs.server().password())

            if prefs.globals().crs().authid():
                Application.setLayerDefaultCrs(prefs.globals().crs())
                Application.setProjectDefaultCrs(prefs.globals().crs())
            if prefs.globals().forceDefaultCrs():
                Application.setForceDefaultCrs()
            if prefs.globals().forceOtfTransform():
                Application.setForceOftTransfom()

            Snapping.setDefaultSnappingTolerance(prefs.globals().snappingTolerance())
            Snapping.setDefaultSnappingUnit(prefs.globals().snappingUnit())

            Application.setComposerFont(prefs.globals().font())

            Settings.setPluginConfigured()

        return ok

    # Configure the project, i.e. load all settings for QgsProject but don't load anything until needed
    def configure(self):
        # Configure the plugin if required
        if not Settings.isPluginConfigured():
            if not self.configurePlugin():
                return False

        if not Settings.isProjectConfigured():
            self.project().configure()

        if Settings.isProjectConfigured():
            return True

        self.showCriticalMessage('ARK Spatial not configured, unable to continue!')
        self.project().showDock(False)
        return False
