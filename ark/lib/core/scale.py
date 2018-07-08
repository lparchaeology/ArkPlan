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


class Scale:

    # Scale enum
    OneToTen = (0, '1:10 (2.5m)', 2.5)
    OneToTwenty = (1, '1:20 (5m)', 5)
    OneToFifty = (2, '1:50 (12.5m)', 12.5)
    OneToOneHundred = (3, '1:100 (25m)', 25)

    def __new__(cls, value, label, factor):
        obj = object.__new__(cls)
        obj._value_ = value
        obj.label = label
        obj.factor = factor
        return obj
