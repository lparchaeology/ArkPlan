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
            self.siteCode = elements[0]
            type = elements[1][0]
            if (type.lower() == 'p'):
                self.name = 'Plan'
                self.sourceClass = 'pln'
                self.sourceId = int(elements[1][1:])
            elif (type.lower() == 's'):
                self.name = 'Section'
                self.sourceClass = 'sec'
                self.sourceId = int(elements[1][1:])
            elif (type.lower() == 't'):
                self.name = 'Top Plan'
                self.sourceClass = 'top'
                self.sourceId = 0
            elif (type.lower() == 'm'):
                self.name = 'Matrix'
                self.sourceClass = 'mtx'
                self.sourceId = 0
            else:
                self.name = 'Context'
                self.sourceClass = 'cxt'
                self.sourceId = int(elements[1])
            suffixPos = 3
            if (len(elements) >= 4):
                if (elements[2][0].lower() == 'e' and elements[3][0].lower() == 'n'):
                    self.easting = int(elements[2][1:])
                    self.northing = int(elements[3][1:])
                    suffixPos = 4
            if (len(elements) > suffixPos):
                self.suffix = elements[suffixPos]
                if (self.suffix.lower() == 'r'):
                    self.suffix = ''

    def baseName(self):
        name = self.siteCode + '_'
        pad = 0
        if (self.sourceClass.lower() == 'cxt'):
            pad = 4
        elif (self.sourceClass.lower() == 'pln'):
            name += 'P'
        elif (self.sourceClass.lower() == 'top'):
            name += 'TP'
        elif (self.sourceClass.lower() == 'sec'):
            name += 'S'
        elif (self.sourceClass.lower() == 'mtx'):
            name += 'M'
        if (self.sourceId > 0):
            name += str(self.sourceId).zfill(pad)
        if (self.easting > 0 and self.northing > 0):
            name += '_E'
            name += str(self.easting).zfill(3)
            name += '_N'
            name += str(self.northing).zfill(3)
        if self.suffix:
            name += '_'
            name += self.suffix
        return name
