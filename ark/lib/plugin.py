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

import os.path

from PyQt4.QtCore import QCoreApplication, QObject, QSettings, Qt, QTranslator
from PyQt4.QtGui import QAction, QIcon

from qgis.core import QgsMessageLog
from qgis.gui import QgsMessageBar

from project import Project


class Plugin(QObject):

    """QGIS Plugin Base Class."""

    # InterfaceGroup enum
    NoGroup = 0
    OwnGroup = 1
    PluginsGroup = 2
    DatabaseGroup = 3
    RasterGroup = 4
    VectorGroup = 5
    WebGroup = 6

    # Public variables
    iface = None  # QgsInteface()
    pluginAction = None  # QAction()
    pluginName = ''
    pluginPath = ''
    pluginIconPath = ''
    displayName = ''

    # Private variables
    _actions = []
    _checkable = False
    _menuGroup = 0  # MenuType
    _menu = None  # QMenu()
    _toolbarGroup = 0  # MenuType
    _toolbar = None  # QToolBar()

    def __init__(self, iface, pluginName, pluginIconPath, pluginPath,
                 menuGroup=PluginsGroup, toolbarGroup=PluginsGroup, checkable=False, parent=None):
        """Constructor."""
        super(Plugin, self).__init__(parent)
        self.iface = iface
        self.pluginName = pluginName
        self.pluginPath = pluginPath
        self.pluginIconPath = pluginIconPath
        self._menuGroup = menuGroup
        self._toolbarGroup = toolbarGroup
        self._checkable = checkable

        # initialize translation
        locale = QSettings().value('locale/userLocale')[0:2]
        locale_path = os.path.join(self.pluginPath, 'i18n', self.pluginName + '_{}.qm'.format(locale))
        if os.path.exists(locale_path):
            self.translator = QTranslator()
            self.translator.load(locale_path)
            QCoreApplication.installTranslator(self.translator)

    def setDisplayName(self, name):
        """Set the translated display to be used in the menu and elsewhere."""
        self.displayName = name

    def initGui(self):
        """Create the menu entries and toolbar icons inside the QGIS GUI."""
        # Reimplement and call in inplementation

        # Unload in case plugin crash durign reload left remnants behind
        Plugin.unload(self)

        if self._menuGroup == Plugin.OwnGroup:
            self._menu = self.iface.mainWindow().menuBar().addMenu(self.pluginName)
            self._menu.setObjectName(self.pluginName)
        if self._toolbarGroup == Plugin.OwnGroup:
            self._toolbar = self.iface.addToolBar(self.pluginName)
            self._toolbar.setObjectName(self.pluginName)

        self.pluginAction = self.addNewAction(
            self.pluginIconPath, self.displayName, callback=self.run, checkable=self._checkable)

    def unload(self):
        """Removes the plugin menu item and icon from QGIS GUI."""
        # Reimplement and call in inplementation
        for action in self._actions:

            if self._menuGroup == Plugin.OwnGroup or self._menuGroup == Plugin.PluginsGroup:
                self.iface.removePluginMenu(self.displayName, action)
            elif self._menuGroup == Plugin.DatabaseGroup:
                self.iface.removePluginDatabaseMenu(self.displayName, action)
            elif self._menuGroup == Plugin.RasterGroup:
                self.iface.removePluginRasterMenu(self.displayName, action)
            elif self._menuGroup == Plugin.VectorGroup:
                self.iface.removePluginVectorMenu(self.displayName, action)
            elif self._menuGroup == Plugin.WebGroup:
                self.iface.removePluginWebMenu(self.displayName, action)

            if self._toolbarGroup == Plugin.OwnGroup:
                self._toolbar.removeAction(action)
            elif self._toolbarGroup == Plugin.PluginsGroup:
                self.iface.removeToolBarIcon(action)
            elif self._toolbarGroup == Plugin.DatabaseGroup:
                self.iface.removeDatabaseToolBarIcon(action)
            elif self._toolbarGroup == Plugin.RasterGroup:
                self.iface.removeRasterToolBarIcon(action)
            elif self._toolbarGroup == Plugin.VectorGroup:
                self.iface.removeVectorToolBarIcon(action)
            elif self._toolbarGroup == Plugin.WebGroup:
                self.iface.removeWebToolBarIcon(action)

        # remove the menu
        if self._menu:
            del self._menu
        # remove the toolbar
        if self._toolbar:
            del self._toolbar

    def run(self):
        """Run method that performs all the real work"""
        # Reimplement in inplementation
        pass

    def addNewAction(
            self,
            iconPath,
            text,
            callback=None,
            enabled=True,
            checkable=False,
            addToMenu=True,
            addToToolbar=True,
            tip=None,
            whatsThis=None,
            parent=None):
        """Add a toolbar icon to the toolbar"""

        if parent is None:
            parent = self.iface.mainWindow()
        action = QAction(QIcon(iconPath), text, parent)
        if tip is not None:
            action.setStatusTip(tip)
        if whatsThis is not None:
            action.setWhatsThis(whatsThis)

        if callback is not None:
            action.triggered.connect(callback)
        action.setEnabled(enabled)
        action.setCheckable(checkable)

        self.addAction(action, addToMenu, addToToolbar)
        return action

    def addAction(self, action, addToMenu=True, addToToolbar=True):
        """Add an action to the menu and/or toolbar."""

        if addToToolbar:
            if self._toolbarGroup == Plugin.OwnGroup:
                self._toolbar.addAction(action)
            elif self._toolbarGroup == Plugin.PluginsGroup:
                self.iface.addToolBarIcon(action)
            elif self._toolbarGroup == Plugin.DatabaseGroup:
                self.iface.addDatabaseToolBarIcon(action)
            elif self._toolbarGroup == Plugin.RasterGroup:
                self.iface.addRasterToolBarIcon(action)
            elif self._toolbarGroup == Plugin.VectorGroup:
                self.iface.addVectorToolBarIcon(action)
            elif self._toolbarGroup == Plugin.WebGroup:
                self.iface.addWebToolBarIcon(action)

        if addToMenu:
            if self._menuGroup == Plugin.OwnGroup:
                self._menu.addAction(action)
            elif self._menuGroup == Plugin.PluginsGroup:
                self.iface.addPluginToMenu(self.displayName, action)
            elif self._menuGroup == Plugin.DatabaseGroup:
                self.iface.addPluginToDatabaseMenu(self.displayName, action)
            elif self._menuGroup == Plugin.RasterGroup:
                self.iface.addPluginToRasterMenu(self.displayName, action)
            elif self._menuGroup == Plugin.VectorGroup:
                self.iface.addPluginToVectorMenu(self.displayName, action)
            elif self._menuGroup == Plugin.WebGroup:
                self.iface.addPluginToWebMenu(self.displayName, action)

        self._actions.append(action)

    # Convenience logging functions

    def logCriticalMessage(self, text):
        self.logMessage(text, QgsMessageLog.CRITICAL)

    def logWarningMessage(self, text):
        self.logMessage(text, QgsMessageLog.WARNING)

    def logInfoMessage(self, text):
        self.logMessage(text, QgsMessageLog.INFO)

    def logMessage(self, text, level=QgsMessageLog.INFO):
        QgsMessageLog.logMessage(text, self.pluginName, level)

    def showCriticalMessage(self, text, duration=5):
        self.showMessage(text, QgsMessageBar.CRITICAL, duration)

    def showWarningMessage(self, text, duration=5):
        self.showMessage(text, QgsMessageBar.WARNING, duration)

    def showInfoMessage(self, text, duration=5):
        self.showMessage(text, QgsMessageBar.INFO, duration)

    def showMessage(self, text, level=QgsMessageBar.INFO, duration=5):
        self.iface.messageBar().pushMessage(text, level, duration)

    def showStatusMessage(self, text):
        self.iface.mainWindow().statusBar().showMessage(text)

    # Project utilities

    def projectCrs(self):
        return Project.crs(self.iface)

    def projectFilePath():
        return Project.filePath()

    # Settings utilities

    def setEntry(self, key, value, default=None):
        return Project.setEntry(self.pluginName, key, value, default)

    def removeEntry(self, key):
        return Project.removeEntry(self.pluginName, key)

    def writeEntry(self, key, value):
        return Project.writeEntry(self.pluginName, key, value)

    def readEntry(self, key, default=''):
        return Project.readEntry(self.pluginName, key, default)

    def readNumEntry(self, key, default=0):
        return Project.readNumEntry(self.pluginName, key, default)

    def readDoubleEntry(self, key, default=0.0):
        return Project.readDoubleEntry(self.pluginName, key, default)

    def readBoolEntry(self, key, default=False):
        return Project.readBoolEntry(self.pluginName, key, default)

    def readListEntry(self, key, default=[]):
        return Project.readListEntry(self.pluginName, key, default)

    # QgsInterface utilities

    def mapCanvas(self):
        return self.iface.mapCanvas()

    def legendInterface(self):
        return self.iface.legendInterface()


"""Template implementation classes, copy one of these into your main plugin file"""


class MyPlugin(Plugin):

    """QGIS Plugin Implementation for dialog or single-shot process."""

    def __init__(self, iface):
        super(MyPlugin, self).__init__(iface, u'MyPlugin', ':/plugins/MyPlugin/icon.png', os.path.dirname(__file__),
                                       Plugin.PluginsGroup, Plugin.PluginsGroup)
        # Set display / menu name now we have tr() set up
        self.setDisplayName(self.tr(u'&MyPlugin'))

    def initGui(self):
        """Create the menu entries and toolbar icons inside the QGIS GUI."""
        super(MyPlugin, self).initGui()

        # Connect a simple button and menu item to your main action

    def unload(self):
        """Removes the plugin menu item and icon from QGIS GUI."""
        # Destroy/disable any plugin objects here
        super(MyPlugin, self).unload()

    def run(self):
        """Run method when plugin action triggered"""
        pass


class MyDockPlugin(Plugin):

    """QGIS Plugin Implementation for dock."""

    def __init__(self, iface):
        super(MyPlugin, self).__init__(iface, u'MyDockPlugin', ':/plugins/MyPlugin/icon.png', os.path.dirname(__file__),
                                       Plugin.PluginsGroup, Plugin.PluginsGroup, checkable=True)
        # Set display / menu name now we have tr() set up
        self.setDisplayName(self.tr(u'&MyPlugin'))

    def initGui(self):
        """Create the menu entries and toolbar icons inside the QGIS GUI."""
        super(MyPlugin, self).initGui()

        self.dock = MyDock()  # noqa # Your dock implementation derived from ArkDockWidget
        self.dock.load(self.iface, Qt.LeftDockWidgetArea, self.pluginAction)
        self.dock.someSignal.connect(self.someMethod)

    def unload(self):
        """Removes the plugin menu item and icon from QGIS GUI."""
        # Destroy/disable any plugin objects here
        self.dock.unload()
        super(MyPlugin, self).unload()

    def run(self, checked):
        """Run method when dock toggled"""
        if checked:
            pass
