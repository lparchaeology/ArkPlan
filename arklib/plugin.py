# -*- coding: utf-8 -*-
"""
/***************************************************************************
                                 A QGIS plugin
                              -------------------
        begin                : 2015-05-25
        git sha              : $Format:%H$
        copyright            : (C) 2015 by John Layt / LP Heritage LLP
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

from PyQt4.QtCore import Qt, QObject, QSettings, QTranslator, qVersion, QCoreApplication
from PyQt4.QtGui import QAction, QIcon

from qgis.core import QGis, QgsProject, QgsMessageLog
from qgis.gui import QgsMessageBar

# Initialize Qt resources from file resources.py
import resources_rc

class Plugin(QObject):
    """QGIS Plugin Base Class."""

    # MenuType enum
    PluginsMenu = 0
    DatabaseMenu = 1
    RasterMenu = 2
    VectorMenu = 3
    WebMenu = 4

    # Public variables
    iface = None  # QgsInteface()
    pluginName = ''
    pluginPath = ''
    pluginIconPath = ''
    displayName = ''
    menuType = 0  # MenuType
    actions = []
    toolbar = None  # QToolBar()

    def __init__(self, iface, pluginName, pluginIconPath, pluginPath, menuType):
        """Constructor.

        :param iface: An interface instance that will be passed to this class
            which provides the hook by which you can manipulate the QGIS
            application at run time.
        :type iface: QgsInterface

        :param pluginName: Untranslated name of the plugin.
        :type pluginName: str

        :param pluginPath: The plugin directory.
        :type pluginPath: str

        :param pluginIconPath: Plugin icon path, either file or resource.
        :type pluginIconPath: str

        :param menuType: The menu type to add the plugin to.
        :type menuType: int
        """
        self.iface = iface
        self.pluginName = pluginName
        self.pluginPath = pluginPath
        self.pluginIconPath = pluginIconPath
        self.menuType = menuType

        # initialize locale
        locale = QSettings().value('locale/userLocale')[0:2]
        locale_path = os.path.join(self.pluginPath, 'i18n', 'ArkGrid_{}.qm'.format(locale))
        if os.path.exists(locale_path):
            self.translator = QTranslator()
            self.translator.load(locale_path)
            QCoreApplication.installTranslator(self.translator)

        # Declare instance attributes
        self.toolbar = self.iface.addToolBar(self.pluginName)
        self.toolbar.setObjectName(self.pluginName)

    def setDisplayName(self, name):
        """Set the translated display to be used in the menu and elsewhere
        :param name: Translated plugin name.
        :type name: str, QString
        """
        self.displayName = name

    # noinspection PyMethodMayBeStatic
    def tr(self, message):
        """Get the translation for a string using Qt translation API.

        We implement this ourselves since we do not inherit QObject.

        :param message: String for translation.
        :type message: str, QString

        :returns: Translated version of message.
        :rtype: QString
        """
        # noinspection PyTypeChecker,PyArgumentList,PyCallByClass
        return QCoreApplication.translate(self.pluginName, message)

    def addAction(
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
        """Add a toolbar icon to the toolbar.

        :param iconPath: Path to the icon for this action. Can be a resource
            path (e.g. ':/plugins/foo/bar.png') or a normal file system path.
        :type iconPath: str

        :param text: Text that should be shown in menu items for this action.
        :type text: str

        :param callback: Function to be called when the action is triggered.
        :type callback: function

        :param enabled: A flag indicating if the action should be enabled
            by default. Defaults to True.
        :type enabled: bool

        :param checkable: A flag indicating if the action should be checkable
            by default. Defaults to False.
        :type chenckable: bool

        :param addToMenu: Flag indicating whether the action should also
            be added to the menu. Defaults to True.
        :type addToMenu: bool

        :param addToToolbar: Flag indicating whether the action should also
            be added to the toolbar. Defaults to True.
        :type addToToolbar: bool

        :param tip: Optional text to show in a popup when mouse pointer
            hovers over the action.
        :type tip: str

        :param parent: Parent widget for the new action. Defaults None.
        :type parent: QWidget

        :param whatsThis: Optional text to show in the status bar when the
            mouse pointer hovers over the action.

        :returns: The action that was created. Note that the action is also
            added to self.actions list.
        :rtype: QAction
        """

        icon = QIcon(iconPath)
        if parent is None:
            parent = self.iface.mainWindow()
        action = QAction(icon, text, parent)
        if callback is not None:
            action.triggered.connect(callback)
        action.setEnabled(enabled)
        action.setCheckable(checkable)

        if tip is not None:
            action.setStatusTip(tip)

        if whatsThis is not None:
            action.setWhatsThis(whatsThis)

        if addToToolbar:
            if self.toolbar is None:
                self.toolbar = self.iface.addToolBar(self.pluginName)
                self.toolbar.setObjectName(self.pluginName)
            self.toolbar.addAction(action)

        if addToMenu:
            if self.menuType == Plugin.PluginsMenu:
                self.iface.addPluginToMenu(self.displayName, action)
            elif self.menuType == Plugin.DatabaseMenu:
                self.iface.addPluginToDatabaseMenu(self.displayName, action)
            elif self.menuType == Plugin.RasterMenu:
                self.iface.addPluginToRasterMenu(self.displayName, action)
            elif self.menuType == Plugin.VectorMenu:
                self.iface.addPluginToVectorMenu(self.displayName, action)
            elif self.menuType == Plugin.WebMenu:
                self.iface.addPluginToWebMenu(self.displayName, action)

        self.actions.append(action)
        return action

    def initGui(self):
        """Create the menu entries and toolbar icons inside the QGIS GUI."""
        # Reimplement in inplementation
        pass

    def unload(self):
        """Removes the plugin menu item and icon from QGIS GUI."""
        # Reimplement and call in inplementation
        for action in self.actions:
            if self.menuType == Plugin.PluginsMenu:
                self.iface.removePluginMenu(self.displayName, action)
            elif self.menuType == Plugin.DatabaseMenu:
                self.iface.removePluginDatabaseMenu(self.displayName, action)
            elif self.menuType == Plugin.RasterMenu:
                self.iface.removePluginRasterMenu(self.displayName, action)
            elif self.menuType == Plugin.VectorMenu:
                self.iface.removePluginVectorMenu(self.displayName, action)
            elif self.menuType == Plugin.WebMenu:
                self.iface.removePluginWebMenu(self.displayName, action)
            self.iface.removeToolBarIcon(action)
        # remove the toolbar
        del self.toolbar

    def run(self):
        """Run method that performs all the real work"""
        # Reimplement in inplementation
        pass

    # Convenience logging functions

    def logCriticalMessage(self, text):
        self.logMessage(text, QgsMessageLog.CRITICAL)

    def logWarningMessage(self, text):
        self.logMessage(text, QgsMessageLog.WARNING)

    def logInfoMessage(self, text):
        self.logMessage(text, QgsMessageLog.INFO)

    def logMessage(self, text, level=QgsMessageLog.INFO):
        QgsMessageLog.logMessage(text, self.pluginName, level)

    def showCriticalMessage(self, text, duration=0):
        self.showMessage(text, QgsMessageBar.CRITICAL, duration)

    def showWarningMessage(self, text, duration=0):
        self.showMessage(text, QgsMessageBar.WARNING, duration)

    def showInfoMessage(self, text, duration=0):
        self.showMessage(text, QgsMessageBar.INFO, duration)

    def showMessage(self, text, level=QgsMessageBar.INFO, duration=0):
        self.iface.messageBar().pushMessage(text, level, duration)

    def showStatusMessage(self, text):
        utils.showStatusMessage(self.iface, text)

    # Project utilities

    def projectCrs(self):
        if QGis.QGIS_VERSION_INT >= 20400:
            return self.iface.mapCanvas().mapSettings().destinationCrs()
        else:
            return self.iface.mapCanvas().mapRenderer().destinationCrs()

    # Settings utilities

    def setEntry(self, key, value, default=None):
        if (value == None or value == '' or value == default):
            self.removeEntry(key)
        else:
            self.writeEntry(key, value)

    def removeEntry(self, key):
        QgsProject.instance().removeEntry(self.pluginName, key)

    def writeEntry(self, key, value):
        QgsProject.instance().writeEntry(self.pluginName, key, value)

    def readEntry(self, key, default=''):
        ret = QgsProject.instance().readEntry(self.pluginName, key, default)
        if ret is None or not ret[1]:
            return default
        else:
            return ret[0]

    def readNumEntry(self, key, default=0):
        ret = QgsProject.instance().readNumEntry(self.pluginName, key, default)
        if ret is None or not ret[1]:
            return default
        else:
            return ret[0]

    def readDoubleEntry(self, key, default=0.0):
        ret = QgsProject.instance().readDoubleEntry(self.pluginName, key, default)
        if ret is None or not ret[1]:
            return default
        else:
            return ret[0]

    def readBoolEntry(self, key, default=False):
        ret = QgsProject.instance().readBoolEntry(self.pluginName, key, default)
        if ret is None or not ret[1]:
            return default
        else:
            return ret[0]

    def readListEntry(self, key, default=[]):
        QgsProject.instance().readListEntry(self.pluginName, key, default)

    # QgsInterface utilities

    def mapCanvas(self):
        return self.iface.mapCanvas()

    def legendInterface(self):
        return self.iface.legendInterface()

# Template implementation classes, copy one of these into your main plugin file

class MyPlugin(Plugin):
    """QGIS Plugin Implementation."""

    def __init__(self, iface):
        super(MyPlugin, self).__init__(iface, u'MyPlugin', ':/plugins/MyPlugin/icon.png',
                                       os.path.dirname(__file__), Plugin.PluginsMenu)
        # Set display / menu name now we have tr() set up
        self.setDisplayName(self.tr(u'&MyPlugin'))

    def initGui(self):
        """Create the menu entries and toolbar icons inside the QGIS GUI."""
        super(MyPlugin, self).initGui()

        # Connect a simple button and menu item to your main action
        self.addAction(self.pluginIconPath, self.displayName, self.run)

    def unload(self):
        """Removes the plugin menu item and icon from QGIS GUI."""
        # Destroy/disable any plugin objects here
        super(MyPlugin, self).unload()

    def run(self):
        """Run method that performs all the real work"""
        # Create and show the dialog or dock for the plugin, then process the result
        pass


class MyDockPlugin(Plugin):
    """QGIS Plugin Implementation."""

    def __init__(self, iface):
        super(MyPlugin, self).__init__(iface, u'MyDockPlugin', ':/plugins/MyPlugin/icon.png',
                                       os.path.dirname(__file__), Plugin.PluginsMenu)
        # Set display / menu name now we have tr() set up
        self.setDisplayName(self.tr(u'&MyPlugin'))

    def initGui(self):
        """Create the menu entries and toolbar icons inside the QGIS GUI."""
        super(MyPlugin, self).initGui()

        self.dock = MyDock()  # Your dock implementation derived from ArkDockWidget
        dockAction = self.addAction(self.tr(u'Dock Name'), ':/plugins/MyPlugin/icon.png', True)
        self.dock.load(self.iface, Qt.LeftDockWidgetArea, dockAction)
        self.dock.toggled.connect(self.run)
        self.dock.someSignal.connect(self.someMethod)

    def unload(self):
        """Removes the plugin menu item and icon from QGIS GUI."""
        # Destroy/disable any plugin objects here
        self.dock.unload()
        super(MyPlugin, self).unload()

    def run(self, checked):
        """Run method that performs all the real work"""
        # If the dock has been enabled, do something if needed
        if checked:
            pass
