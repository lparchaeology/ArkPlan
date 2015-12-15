# -*- coding: utf-8 -*-
"""
/***************************************************************************
                                ARK Spatial
                    A QGIS plugin for Archaeological Recording.
        Part of the Archaeological Recording Kit by L-P : Archaeology
                        http://ark.lparchaeology.com
                              -------------------
        begin                : 2014-12-07
        git sha              : $Format:%H$
        copyright            : 2014, 2015 by L-P : Heritage LLP
        email                : ark@lparchaeology.com
        copyright            : 2014, 2015 by John Layt
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

import string

from PyQt4.QtCore import Qt, QVariant, QFileInfo, QObject, QDir

class PlanMetadata:
    siteCode = ''
    sourceClass = ''
    name = ''
    sourceId = None
    easting = None
    northing = None
    suffix  = ''
    filename = ''

    def __init__(self, fileInfo=None):
        if fileInfo is not None:
            self.setFile(fileInfo)

    def setMetadata(self, siteCode, sourceClass, sourceId=None, easting=None, northing=None, suffix=''):
        self.siteCode = siteCode
        self.sourceClass = sourceClass
        self.sourceId = sourceId
        self.easting = easting
        self.northing = northing
        self.suffix = suffix
        self.filename = ''

    def setFile(self, fileInfo):
        self.filename = fileInfo.fileName()
        elements = string.split(fileInfo.completeBaseName(), '_')
        if (self.filename and len(elements) >= 2):
            suffixPos = 3
            self.sourceClass = elements[0].lower()
            self.siteCode = elements[1]
            if (self.sourceClass == 'pln'):
                self.name = 'Plan'
                self.sourceId = int(elements[2])
            elif (self.sourceClass == 'cxt'):
                self.name = 'Context'
                self.sourceId = int(elements[2])
            elif (self.sourceClass == 'sec'):
                self.name = 'Section'
                self.sourceId = int(elements[2])
            elif (self.sourceClass == 'tim'):
                self.name = 'Timber'
                self.sourceId = int(elements[2])
            elif (self.sourceClass == 'top'):
                self.name = 'Top Plan'
                self.sourceId = None
                suffixPos = 2
            elif (self.sourceClass == 'mtx'):
                self.name = 'Matrix'
                self.sourceId = None
                suffixPos = 2
            else:
                self.name = 'Unknown'
                self.sourceId = None
                self.easting = None
                self.northing = None
                self.suffix = None
                return
            if (len(elements) >= suffixPos + 1):
                location = elements[suffixPos]
                #FIXME Make generic able to handle any length grid references
                #TODO Add support for Baseline names
                if len(location) == 8 and location[3].lower() == 'e' and location[7].lower() == 'n':
                    self.easting = int(location[0:3])
                    self.northing = int(location[4:7])
                    suffixPos += 1
            if (len(elements) >= suffixPos + 1):
                self.suffix = elements[suffixPos]
                if (self.suffix.lower() == 'r'):
                    self.suffix = ''

    def baseName(self):
        name = self.sourceClass + '_' + self.siteCode
        if (self.sourceId > 0):
            name = name + '_' + str(self.sourceId)
        if (self.easting > 0 and self.northing > 0):
            name = name + '_' + str(self.easting).zfill(3) + 'e' + str(self.northing).zfill(3) + 'n'
        if self.suffix:
            name = name + '_' + self.suffix
        return name
