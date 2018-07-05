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

from qgis.PyQt.QtCore import QDir

from qgis.core import QgsApplication

from ArkSpatial.ark.lib import Application, Project

from . import Config


class Settings:

    @staticmethod
    def isPluginConfigured():
        return Application.readEntry("ARK", "configured", False)

    @staticmethod
    def setPluginConfigured():
        Application.setEntry("ARK", "configured", True)

    @staticmethod
    def projectsFolder():
        return Application.readEntry("ARK", "projectsFolder", "")

    @staticmethod
    def setProjectsFolder(path):
        Application.setEntry("ARK", "projectsFolder", path)

    # Projects Server settings
    # TODO Move to Auth Storage

    @classmethod
    def useProjectServer(cls):
        serverUrl = cls.serverUrl()
        return serverUrl is not None and serverUrl != ''

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
    def projectDir():
        proj = Project.dir()
        proj.cdUp()
        return proj

    @staticmethod
    def projectPath():
        return Settings.projectDir().absolutePath()

    @staticmethod
    def isProjectConfigured():
        return Project.readBoolEntry("ARK", "Project/configured", False)

    @staticmethod
    def setProjectConfigured():
        Project.setEntry("ARK", "Project/configured", True)

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

    @classmethod
    def siteCodes(cls):
        if cls.siteCode():
            return [cls.siteCode()]
        return []

    @staticmethod
    def siteCode():
        return Project.readEntry('ARK', 'Project/siteCode')

    @staticmethod
    def setSiteCode(siteCode):
        Project.setEntry("ARK", "Project/siteCode", siteCode)

    @staticmethod
    def locationEasting():
        return Project.readEntry('ARK', 'Project/easting')

    @staticmethod
    def locationNorthing():
        return Project.readEntry('ARK', 'Project/northing')

    @staticmethod
    def setLocation(easting, northing):
        Project.setEntry("ARK", "Project/easting", easting)
        Project.setEntry("ARK", "Project/northing", northing)

    @staticmethod
    def logUpdates():
        return Project.readBoolEntry("ARK", "Project/logUpdates", False)

    @staticmethod
    def setLogUpdates(logUpdates):
        Project.writeEntry('Project/logUpdates', logUpdates)

    # Projects Server settings
    # TODO Move to Auth Storage

    @staticmethod
    def siteServerUrl():
        return Project.readEntry("ARK", "Project/Server/url")

    @staticmethod
    def setSiteServerUrl(url):
        Project.setEntry("ARK", "Project/Server/url", url)

    @staticmethod
    def siteServerUser():
        return Project.readEntry("ARK", "Project/Server/user")

    @staticmethod
    def siteServerPassword():
        return Project.readEntry("ARK", "Project/Server/password")

    @staticmethod
    def setSiteServerCredentials(user, password):
        Project.setEntry("ARK", "Project/Server/user", user)
        Project.setEntry("ARK", "Project/Server/password", password)

    # Raster Drawings settings

    @staticmethod
    def useCustomDrawingPath(drawing):
        return Project.readBoolEntry("ARK", 'Project/Drawings/' + drawing + '/useCustomPath', False)

    @staticmethod
    def drawingDir(drawing):
        return QDir(Settings.drawingPath(drawing))

    @staticmethod
    def drawingPath(drawing):
        path = os.path.join(Settings.projectPath(), Config.drawings[drawing]['path'])
        if Settings.useCustomDrawingPath(drawing):
            path = Project.readEntry("ARK", 'Project/Drawings/' + drawing + '/customPath', path)
        return path

    @staticmethod
    def setDrawingPath(drawing, useCustomPath, absolutePath):
        Project.setEntry("ARK", 'Project/Drawings/' + drawing + '/useCustomPath', useCustomPath)
        Project.setEntry("ARK", 'Project/Drawings/' + drawing + '/customPath', absolutePath)

    @staticmethod
    def georefDrawingDir(drawing):
        return QDir(Settings.georefDrawingPath(drawing))

    @staticmethod
    def georefDrawingPath(drawing):
        return os.path.join(Settings.drawingPath(drawing), 'georef')

    @staticmethod
    def drawingTransparency():
        return Project.readNumEntry("ARK", 'Project/Drawings/transparency', 50)

    @staticmethod
    def setDrawingTransparency(transparency):
        Project.writeEntry("ARK", 'Project/Drawings/transparency', transparency)

    @staticmethod
    def useCustomStyles():
        return Project.readBoolEntry("ARK", 'Project/Styles/useCustomStyles', False)

    @staticmethod
    def customStylesDir():
        return QDir(Settings.customStylesPath())

    @staticmethod
    def customStylesPath():
        return Project.readEntry("ARK", 'Project/Styles/customPath', '')

    @staticmethod
    def setCustomStylesPath(useCustomStyles, absolutePath):
        Project.setEntry("ARK", 'Project/Styles/useCustomStyles', useCustomStyles)
        Project.setEntry("ARK", 'Project/Styles/customPath', absolutePath)
