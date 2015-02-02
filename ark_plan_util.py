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
    suffix  = ''
    easting = 0
    northing = 0
    if name:
        elements = string.split(name, '_')
        site = elements[0]
        type = elements[1][0]
        if (type.lower() == 'c'):
            type = 'Context'
        elif (type.lower() == 'p'):
            type = 'Plan'
        elif (type.lower() == 's'):
            type = 'Section'
        elif (type.lower() == 'm'):
            type = 'Matrix'
        else:
            type = ''
        number = int(elements[1][1:5])
        if (len(elements[1]) > 5):
            suffix = elements[1][5:]
        easting = int(elements[2][1:])
        northing = int(elements[3][1:])
    return site, type, number, suffix, easting, northing

def planName(site, type, number, suffix, easting, northing):
    name = site + '_'
    if (type.lower() == 'context' or type.lower() == 'c'):
        name += 'C'
    elif (type.lower() == 'plan' or type.lower() == 'p'):
        name += 'P'
    elif (type.lower() == 'section' or type.lower() == 's'):
        name += 'S'
    elif (type.lower() == 'matrix' or type.lower() == 'm'):
        name += 'M'
    if (number > 0):
        #TODO pad to 4
        name += str(number)
    name += suffix
    if (easting > 0 and northing > 0):
        #TODO Pad to 3
        name += '_E'
        name += str(easting)
        name += '_N'
        name += str(northing)
    return name
