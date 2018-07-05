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
    OneToTen = 0
    OneToTwenty = 1
    OneToFifty = 2
    OneToOneHundred = 3
    Scale = [0, 1, 2, 3]
    Label = ['1:10 (2.5m)', '1:20 (5m)', '1:50 (12.5m)', '1:100 (25m)']
    Factor = [2.5, 5, 12.5, 25]
