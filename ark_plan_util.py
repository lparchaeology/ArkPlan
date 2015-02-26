# -*- coding: utf-8 -*-
"""
/***************************************************************************
 ArkPlan
                                 A QGIS plugin
 Plugin to assist in digitising of Archaeological plans.
                              -------------------
        begin                : 2015-02-02
        git sha              : $Format:%H$
        copyright            : (C) 2014 by John Layt
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

def planMetadata(name):
    site = ''
    type = ''
    number = 0
    easting = 0
    northing = 0
    suffix  = ''
    elements = string.split(name, '_')
    if (name and len(elements) >= 2):
        site = elements[0]
        type = elements[1][0]
        if (type.lower() == 'p'):
            type = 'Plan'
            number = int(elements[1][1:])
        elif (type.lower() == 's'):
            type = 'Section'
            number = int(elements[1][1:])
        elif (type.lower() == 't'):
            type = 'Top Plan'
            number = 0
        elif (type.lower() == 'm'):
            type = 'Matrix'
            number = 0
        else:
            type = 'Context'
            number = int(elements[1])
        suffixPos = 3
        if (len(elements) >= 4):
            if (elements[2][0].lower() == 'e' and elements[3][0].lower() == 'n'):
                easting = int(elements[2][1:])
                northing = int(elements[3][1:])
                suffixPos = 4
        if (len(elements) > suffixPos):
            suffix = elements[suffixPos]
            if (suffix.lower() == 'r'):
                suffix = ''

    return site, type, number, easting, northing, suffix

def planName(site, type, number, easting, northing, suffix):
    name = site + '_'
    pad = 0
    if (type.lower() == 'context' or type.lower() == 'c'):
        pad = 4
    elif (type.lower() == 'plan' or type.lower() == 'p'):
        name += 'P'
    elif (type.lower() == 'top plan' or type.lower() == 'tp'):
        name += 'TP'
    elif (type.lower() == 'section' or type.lower() == 's'):
        name += 'S'
    elif (type.lower() == 'matrix' or type.lower() == 'm'):
        name += 'M'
    if (number > 0):
        name += str(number).zfill(pad)
    if (easting > 0 and northing > 0):
        name += '_E'
        name += str(easting).zfill(3)
        name += '_N'
        name += str(northing).zfill(3)
    if suffix:
        name += '_'
        name += suffix
    return name
