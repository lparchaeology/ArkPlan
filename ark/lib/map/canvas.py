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

from qgis.core import QgsFeature, QgsGeometry

from ..map import FeatureHighlightItem, GeometryHighlightItem


def addHighlight(canvas, featureOrGeometry, layer, lineColor=None, fillColor=None, buff=None, minWidth=None):
    # TODO Open bug report for QgsHighlight sip not having QgsFeature constructor.
    # hl = QgsHighlight(canvas, featureOrGeometry, layer)
    hl = None
    if isinstance(featureOrGeometry, QgsFeature):
        hl = FeatureHighlightItem(canvas, featureOrGeometry, layer)
        if minWidth:
            hl.setMinWidth(minWidth)
    elif isinstance(featureOrGeometry, QgsGeometry):
        hl = GeometryHighlightItem(canvas, featureOrGeometry, layer)
    if lineColor:
        hl.setLineColor(lineColor)
    if fillColor:
        hl.setFillColor(fillColor)
    if buff:
        hl.setBuffer(buff)
    return hl
