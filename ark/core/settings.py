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

from PyQt4.QtCore import QDir

from qgis.core import QgsApplication

from ArkSpatial.ark.lib import Application, Project

from . import Config


class Settings:

    # Server settings
    # TODO Move to Auth Storage

    @staticmethod
    def serverUrl():
        return Application.readEntry("ARK", "Server/url")

    @staticmethod
    def setServerUrl(url):
        Application.setEntry("ARK", "Server/url", url)

    @staticmethod
    def serverUser():
        return Application.readEntry("ARK", "Server/user")

    @staticmethod
    def serverPassword():
        return Application.readEntry("ARK", "Server/password")

    @staticmethod
    def setServerCredentials(user, password):
        Application.setEntry("ARK", "Server/user", user)
        Application.setEntry("ARK", "Server/password", password)

    # User settings

    @staticmethod
    def userFullName():
        name = Application.readEntry("ARK", "User/fullName")
        if name is None or name == '':
            name = QgsApplication.userFullName()
        return name

    @staticmethod
    def setUserFullName(fullName):
        Application.setEntry("ARK", "User/fullName", fullName)

    @classmethod
    def userInitials(cls):
        initials = Application.readEntry("ARK", "User/initials")
        if initials is None or initials == "":
            initials = ''
            for name in cls.userFullName().split(' '):
                initials += name[0]
        return initials

    @staticmethod
    def setUserInitials(initials):
        Application.setEntry("ARK", "User/initials", initials)

    @staticmethod
    def userOrganisation():
        return Application.readEntry("ARK", "User/organisation")

    @staticmethod
    def setUserOrganisation(organisation):
        Application.setEntry("ARK", "User/organisation", organisation)

    # Project settings

    @staticmethod
    def projectCode():
        return Project.readEntry('ARK', 'Project/code')

    @staticmethod
    def setProjectCode(code):
        Project.setEntry("ARK", "Project/code", code)

    @staticmethod
    def projectName():
        return Project.readEntry('ARK', 'Project/name')

    @staticmethod
    def setProjectName(name):
        Project.setEntry("ARK", "Project/name", name)

    @staticmethod
    def siteCode():
        return Project.readEntry('ARK', 'Project/siteCode')

    @staticmethod
    def setSiteCode(siteCode):
        Project.setEntry("ARK", "Project/siteCode", siteCode)

    # Raster Drawings settings

    def drawingDir(cls, group):
        path = os.path.join(Project.homePath(), Config.drawings[group]['path'])
        if cls.useCustomPath(group):
            path = Project.readEntry("ARK", group + '/path', Config.drawings[group]['path'])
        return QDir(path)

    def setDrawingPath(cls, group, useCustomPath, absolutePath):
        cls._setDrawingEntry(group, 'useCustomPath', useCustomPath, False)
        if useCustomPath:
            cls._setDrawingEntry(group, 'path', absolutePath)
        else:
            cls._setDrawingEntry(group, 'path', '')

    def useCustomPath(cls, group):
        return cls._drawingBoolEntry(group, 'useCustomPath', False)

    def rawDrawingDir(cls, group):
        return QDir(cls.rawDrawingPath(group))

    def rawDrawingPath(cls, group):
        return cls.drawingPath(group)

    def georefDrawingDir(cls, group):
        return QDir(cls.georefDrawingPath(group))

    def georefDrawingPath(cls, group):
        if cls.useGeorefFolder():
            return cls.rawDrawingPath(group) + '/georef'
        return cls.rawDrawingPath(group)

    def drawingTransparency(self):
        return Project.readNumEntry('drawingTransparency', 50)

    def setDrawingTransparency(self, transparency):
        Project.writeEntry('drawingTransparency', transparency)

    def logUpdates(self):
        return self.readBoolEntry('logUpdates', True)

    def setLogUpdates(self, logUpdates):
        Project.writeEntry('logUpdates', logUpdates)

    def useCustomStyles(self):
        return self.readBoolEntry('useCustomStyles', False)

    def styleDir(self):
        return QDir(self.stylePath())

    def stylePath(self):
        path = Project.readEntry('stylePath', '')
        if (not path):
            return self.pluginPath + '/styles'
        return path

    def setStylePath(self, useCustomStyles, absolutePath):
        Project.writeEntry('useCustomStyles', useCustomStyles)
        if useCustomStyles:
            Project.writeEntry('stylePath', absolutePath)
        else:
            Project.writeEntry('stylePath', '')

    # Group settings

    def _drawingBoolEntry(self, group, key, default=None):
        if default is None:
            default = Config.drawings[group][key]
        return self.readBoolEntry(group + '/' + key, default)

    def _setdrawingEntry(self, group, key, value, default=None):
        if default is None:
            default = Config.drawings[group][key]
        self.setEntry(group + '/' + key, value, default)
