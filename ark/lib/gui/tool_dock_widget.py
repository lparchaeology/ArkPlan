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

from PyQt4.QtCore import Qt, QSize
from PyQt4.QtGui import QWidget, QVBoxLayout, QToolBar

from dock_widget import DockWidget

class ToolDockWidget(DockWidget):

    toolbar = None  # QToolBar()
    widget = None  # QWidget()

    _spacer = None  # QSpacerItem()
    _contents = None  # QWidget()

    def __init__(self, widget, parent=None):
        super(ToolDockWidget, self).__init__(parent)

        self.toolbar = QToolBar(self)
        self.toolbar.setObjectName(u'toolbar')
        self.toolbar.setIconSize(QSize(22, 22))

        self.toolbar2 = QToolBar(self)
        self.toolbar2.setObjectName(u'toolbar')
        self.toolbar2.setIconSize(QSize(22, 22))
        self.toolbar2.setVisible(False)

        widget.setParent(self)
        self.widget = widget

        self._layout = QVBoxLayout(self)
        self._layout.setAlignment(Qt.AlignTop)
        self._layout.setObjectName(u'layout')
        self._layout.setContentsMargins(0, 0, 0, 0)
        self._layout.addWidget(self.toolbar)
        self._layout.addWidget(self.toolbar2)
        self._layout.addWidget(self.widget)

        self._contents = QWidget(self)
        self._contents.setObjectName(u'contents')
        self._contents.setLayout(self._layout)
        self.setWidget(self._contents)

    def initGui(self, iface, location, menuAction):
        super(ToolDockWidget, self).initGui(iface, location, menuAction)

    def unloadGui(self):
        super(ToolDockWidget, self).unloadGui()
