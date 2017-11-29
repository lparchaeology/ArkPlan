# -*- coding: utf-8 -*-
"""
/***************************************************************************
                                ARK QGIS
                        A QGIS utilities library.
        Part of the Archaeological Recording Kit by L-P : Archaeology
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
        Application.setValue("ARK/Server", "url", url)

    @staticmethod
    def serverUser():
        return Application.readEntry("ARK/Server", "user")

    @staticmethod
    def serverPassword():
        return Application.readEntry("ARK/Server", "password")

    @staticmethod
    def setServerCredentials(user, password):
        Application.setValue("ARK/Server", "user", user)
        Application.setValue("ARK/Server", "password", password)

    @staticmethod
    def userFullName():
        name = Application.readEntry("ARK/User", "fullName")
        if name is None or name == '':
            name = QgsApplication.userFullName()
        return name

    @classmethod
    def userInitials(cls):
        initials = Application.readEntry("ARK/User", "initials")
        if initials is None or initials == "":
            initials = ''
            for name in cls.userFullName().split(' '):
                initials += name[0]
        return initials

    @staticmethod
    def projectCode():
        return Project.readEntry('ARK/Project', 'code')

    @staticmethod
    def projectName():
        return Project.readEntry('ARK/Project', 'name')

    @staticmethod
    def siteCode():
        return Project.readEntry('ARK/Project', 'siteCode')
