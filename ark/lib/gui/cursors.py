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
        copyright            : 2010 by Jürgen E. Fischer
        copyright            : 2007 by Marco Hugentobler
        copyright            : 2006 by Martin Dobias
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

from PyQt4.QtGui import QCursor, QPixmap

_capture_point_cursor_xpm = [
    "16 16 3 1",
    " »     c None",
    ".»     c #000000",
    "+»     c #FFFFFF",
    "                ",
    "       +.+      ",
    "      ++.++     ",
    "     +.....+    ",
    "    +.     .+   ",
    "   +.   .   .+  ",
    "  +.    .    .+ ",
    " ++.    .    .++",
    " ... ...+... ...",
    " ++.    .    .++",
    "  +.    .    .+ ",
    "   +.   .   .+  ",
    "   ++.     .+   ",
    "    ++.....+    ",
    "      ++.++     ",
    "       +.+      "
]

CapturePointCursor = QCursor(QPixmap(_capture_point_cursor_xpm), 8, 8)
