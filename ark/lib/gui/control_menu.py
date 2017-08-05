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

from PyQt4.QtCore import Qt
from PyQt4.QtGui import QMenu


class ControlMenu(QMenu):

    """Menu that triggers action when Ctrl-Enter or Ctrl-Left-Mouse pressed."""

    def __init__(self, parent=None):
        super(ControlMenu, self).__init__(parent)

    def keyPressEvent(self, e):
        action = self.activeAction()
        if ((e.key() == Qt.Key_Return or e.key() == Qt.Key_Enter)
                and e.modifiers() == Qt.ControlModifier and action is not None and action.isEnabled()):
            action.trigger()
        else:
            super(ControlMenu, self).keyPressEvent(e)

    def mouseReleaseEvent(self, e):
        action = self.activeAction()
        if e.modifiers() == Qt.ControlModifier and action is not None and action.isEnabled():
            action.trigger()
        else:
            super(ControlMenu, self).mouseReleaseEvent(e)
