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

from PyQt4.QtCore import QEvent, QObject, Qt, pyqtSignal


class ReturnPressedFilter(QObject):

    returnPressed = pyqtSignal()

    def __init__(self, parent=None):
        super(ReturnPressedFilter, self).__init__(parent)

    def eventFilter(self, obj, event):
        # FIXME WTF Sledgehammer to fix reload error nut
        if self == None or QEvent == None:
            return True
        if (event.type() == QEvent.KeyPress and (event.key() == Qt.Key_Return or event.key() == Qt.Key_Enter)):
            self.returnPressed.emit()
            return True
        return super(ReturnPressedFilter, self).eventFilter(obj, event)
