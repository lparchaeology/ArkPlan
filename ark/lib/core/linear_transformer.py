# -*- coding: utf-8 -*-
"""
/***************************************************************************
                                ARK QGIS
                        A QGIS utilities library.
        Part of the Archaeological Recording Kit by L-P : Archaeology
                        http://ark.lparchaeology.com
                              -------------------
        copyright            : 2017 by L-P : Heritage LLP
        email                : ark@lparchaeology.com
        copyright            : 2017 by John Layt
        email                : john@layt.net
        copyright            : 2014 by Olivier Dalang
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

import math

from qgis.core import QgsPointV2


class LinearTransformer():
    # Based on LinearTransformer code from VectorBender plugin
    # (C) 2014 by Olivier Dalang

    def __init__(self, a1, b1, a2, b2):
        # scale
        self.ds = (math.sqrt((b2.x() - b1.x()) ** 2.0 + (b2.y() - b1.y()) ** 2.0)
                   / math.sqrt((a2.x() - a1.x()) ** 2.0 + (a2.y() - a1.y()) ** 2.0))
        # rotation
        self.da = (math.atan2(b2.y() - b1.y(), b2.x() - b1.x())
                   - math.atan2(a2.y() - a1.y(), a2.x() - a1.x()))
        # translation
        self.dx1 = a1.x()
        self.dy1 = a1.y()
        self.dx2 = b1.x()
        self.dy2 = b1.y()

    def map(self, p):
        # move to origin (translation part 1)
        p = QgsPointV2(p.x() - self.dx1,
                     p.y() - self.dy1)
        # scale
        p = QgsPointV2(self.ds * p.x(),
                     self.ds * p.y())
        # rotation
        p = QgsPointV2(math.cos(self.da) * p.x() - math.sin(self.da) * p.y(),
                     math.sin(self.da) * p.x() + math.cos(self.da) * p.y())
        # remove to right spot (translation part 2)
        p = QgsPointV2(p.x() + self.dx2,
                     p.y() + self.dy2)
        return p
