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

from qgis.core import QgsApplication

from ArkSpatial.ark.lib import Application, Project


class Settings:

    @staticmethod
    def serverUrl():
        return Application.readEntry("ARK/Server", "url")

    @staticmethod
    def setServerUrl(url):
        Application.setEntry("ARK/Server", "url", url)

    @staticmethod
    def serverUser():
        return Application.readEntry("ARK/Server", "user")

    @staticmethod
    def serverPassword():
        return Application.readEntry("ARK/Server", "password")

    @staticmethod
    def setServerCredentials(user, password):
        Application.setEntry("ARK/Server", "user", user)
        Application.setEntry("ARK/Server", "password", password)

    @staticmethod
    def userFullName():
        name = Application.readEntry("ARK/User", "fullName")
        if name is None or name == '':
            name = QgsApplication.userFullName()
        return name

    @staticmethod
    def setUserFullName(fullName):
        Application.setEntry("ARK/User", "fullName", fullName)

    @classmethod
    def userInitials(cls):
        initials = Application.readEntry("ARK/User", "initials")
        if initials is None or initials == "":
            initials = ''
            for name in cls.userFullName().split(' '):
                initials += name[0]
        return initials

    @staticmethod
    def setUserInitials(initials):
        Application.setEntry("ARK/User", "initials", initials)

    @staticmethod
    def projectCode():
        return Project.readEntry('ARK/Project', 'code')

    @staticmethod
    def setProjectCode(code):
        Application.setEntry("ARK/Project", "code", code)

    @staticmethod
    def projectName():
        return Project.readEntry('ARK/Project', 'name')

    @staticmethod
    def setProjectName(name):
        Application.setEntry("ARK/Project", "name", name)

    @staticmethod
    def siteCode():
        return Project.readEntry('ARK/Project', 'siteCode')

    @staticmethod
    def setSiteCode(siteCode):
        Application.setEntry("ARK/Project", "siteCode", siteCode)
