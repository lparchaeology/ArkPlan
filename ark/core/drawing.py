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

import string

from qgis.PyQt.QtCore import QFileInfo

from .config import Config
from .item import Item
from .source import Source


class Drawing(Source):

    def __init__(self, item=None, easting=None, northing=None, suffix=None, filename=None):

        self._easting = easting
        self._northing = northing
        self._suffix = suffix

        if isinstance(item, QFileInfo):
            super().__init__()
            self.fromFileInfo(item)
        else:
            super().__init__('drawing', item, filename)

    def __eq__(self, other):
        return (isinstance(other, Drawing)
                and self._sourceCode == other._sourceCode
                and self._item == other._item
                and self._filename == other.filename
                and self._easting == other._easting
                and self._northing == other._northing
                and self._suffix == other._suffix)

    def __hash__(self):
        return hash((self._sourceCode, self._item, self._filename, self._easting, self._northing, self._suffix))

    def __str__(self):
        return ('Drawing('
                + str(self._sourceCode) + ', '
                + str(self._item) + ', '
                + str(self._easting) + ', '
                + str(self._northing) + ', '
                + str(self._suffix) + ', '
                + str(self._filename) + ')')

    def debug(self):
        return ('Source('
                + utils.printable(self._sourceCode) + ', '
                + self._item.debug() + ', '
                + utils.printable(self._easting) + ', '
                + utils.printable(self._northing) + ', '
                + utils.printable(self._suffix) + ', '
                + utils.printable(self._filename) + ')')

    def easting(self):
        return self._easting

    def northing(self):
        return self._northing

    def setGridReference(self, easting, northing):
        self._easting = easting
        self._northing = northing

    def suffix(self):
        return self._suffix

    def setSuffix(self, suffix):
        self._suffix = suffix

    def fromFileInfo(self, fileInfo):
        self.setSource('', None, fileInfo.fileName())
        self._easting = None
        self._northing = None
        self._suffix = ''
        elements = string.split(fileInfo.completeBaseName(), '_')
        if (self._filename and len(elements) > 2):
            suffixPos = 3
            drawingCode = elements[0].lower()
            siteCode = elements[1]
            itemId = int(elements[2])
            classCode = ''
            easting = ''
            northing = ''
            suffix = ''
            for drawing in list(Config.drawings.values()):
                if drawing['code'] == drawingCode:
                    classCode = drawing['class']
            if (len(elements) >= suffixPos + 1):
                location = elements[suffixPos]
                # FIXME Make generic able to handle any length grid references
                # TODO Add support for Baseline names
                if len(location) == 8:
                    e = location[3].lower()
                    n = location[7].lower()
                    if (e == 'e' or e == 'w') and (n == 'n' or n == 's'):
                        easting = int(location[0:3])
                        if (e == 'w'):
                            easting = easting * -1
                        northing = int(location[4:7])
                        if (n == 's'):
                            northing = northing * -1
                        suffixPos += 1
            if (len(elements) >= suffixPos + 1):
                suffix = elements[suffixPos]
                if (suffix.lower() == 'r'):
                    suffix = ''
            if classCode and siteCode and itemId:
                self.setSource('drawing', Item(siteCode, classCode, itemId), fileInfo.fileName())
                self._easting = easting
                self._northing = northing
                self._suffix = suffix

    def baseName(self):
        drawingCode = ''
        for drawing in list(Config.drawings.values()):
            if drawing['class'] == self._item.classCode():
                drawingCode = drawing['code']
        if not drawingCode:
            return ''
        name = drawingCode + '_' + self._item.siteCode() + '_' + self._item.itemId()
        if self._easting is not None and self._northing is not None:
            e = 'e' if self._easting >= 0 else 'w'
            n = 'n' if self._northing >= 0 else 's'
            name = name + '_' + str(abs(self._easting)).zfill(3) + e + str(abs(self._northing)).zfill(3) + n
        if self._suffix:
            name = name + '_' + self._suffix
        return name
