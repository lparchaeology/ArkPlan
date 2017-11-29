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

from PyQt4.QtCore import pyqtSignal
from PyQt4.QtGui import QDoubleSpinBox, QWidgetAction


class AbstractSnappingToleranceAction(QWidgetAction):

    """Abstract action for Snapping Tolerance."""

    snappingToleranceChanged = pyqtSignal(float)

    _iface = None

    def __init__(self, parent=None):
        super(AbstractSnappingToleranceAction, self).__init__(parent)

        self._toleranceSpin = QDoubleSpinBox(parent)
        self._toleranceSpin.setDecimals(5)
        self._toleranceSpin.setRange(0.0, 100000000.0)
        self.setDefaultWidget(self._toleranceSpin)
        self.setText('Snapping Tolerance')
        self.setStatusTip('Set the snapping tolerance')
        self._refresh()
        self._toleranceSpin.valueChanged.connect(self._changed)

    def setInterface(self, iface):
        self._iface = iface
        self._refresh()

    # Private API

    def _changed(self, tolerance):
        pass

    def _refresh(self):
        pass
