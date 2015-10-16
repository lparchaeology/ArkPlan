# -*- coding: utf-8 -*-
"""
/***************************************************************************
                                      Ark
                                 A QGIS plugin
             QGIS Plugin for ARK, the Archaeological Recording Kit
                              -------------------
        begin                : 2015-03-02
        git sha              : $Format:%H$
        copyright            : (C) 2015 by L - P: Heritage LLP
        copyright            : (C) 2015 by John Layt
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
            elif (self.sourceClass == 'ctx'):
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
            if (len(elements) >= suffixPos + 2):
                easting = elements[suffixPos]
                northing = elements[suffixPos + 1]
                if (len(easting) > 1 and len(northing) > 1 and
                    easting[-1].lower() == 'e' and northing[-1].lower() == 'n'):
                    self.easting = int(easting[:-1])
                    self.northing = int(northing[:-1])
                    suffixPos += 2
            if (len(elements) >= suffixPos + 1):
                self.suffix = elements[suffixPos]
                if (self.suffix.lower() == 'r'):
                    self.suffix = ''

    def baseName(self):
        name = self.sourceClass + '_' + self.siteCode
        if (self.sourceId > 0):
            name = name + '_' + str(self.sourceId)
        if (self.easting > 0 and self.northing > 0):
            name = name + '_' + str(self.easting).zfill(3) + 'e_' + str(self.northing).zfill(3) + 'n'
        if self.suffix:
            name = name + '_' + self.suffix
        return name
