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

from PyQt4.QtGui import QHBoxLayout, QLabel, QSizePolicy, QToolButton, QWidget


class LayerSnappingWidget(QWidget):

    def __init__(self, layer, parent=None):
        super(LayerSnappingWidget, self).__init__(parent)

        label = QLabel(layer.name(), self)
        spacer = QSpacerItem(20, 40, QSizePolicy.Minimum, QSizePolicy.Expanding, self)
        action = LayerSnappingAction(layer, self)
        tool = QToolButton(self)
        tool.setDefaultAction(action)

        layout = QHBoxLayout(self)
        layout.setObjectName(u'layout')
        layout.addWidget(label)
        layout.addWidget(spacer)
        layout.addWidget(tool)

        self.setLayout(layout)
