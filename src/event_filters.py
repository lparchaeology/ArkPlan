# -*- coding: utf-8 -*-
"""
/***************************************************************************
                                      Ark
                                 A QGIS plugin
             QGIS Plugin for ARK, the Archaeological Recording Kit
                              -------------------
        begin                : 2015-10-27
        git sha              : $Format:%H$
        copyright            : (C) 2015 by L - P: Heritage LLP
        copyright            : (C) 2015 by John Layt
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

from PyQt4.QtCore import Qt, pyqtSignal, QObject, QEvent

class ReturnPressedFilter(QObject):

    returnPressed = pyqtSignal()

    def __init__(self, parent=None):
        super(ReturnPressedFilter, self).__init__(parent)

    def eventFilter(self, obj, event):
        #FIXME WTF Sledgehammer to fix reload error nut
        if self == None or QEvent == None:
            return True
        if (event.type() == QEvent.KeyPress and (event.key() == Qt.Key_Return or event.key() == Qt.Key_Enter)):
            self.returnPressed.emit()
            return True
        return super(ReturnPressedFilter, self).eventFilter(obj, event)
