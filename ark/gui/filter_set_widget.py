# -*- coding: utf-8 -*-
"""
/***************************************************************************
                                ARK Spatial
                    A QGIS plugin for Archaeological Recording.
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

from PyQt4.QtGui import QActionGroup, QMenu, QWidget

from .ui.filter_set_widget_base import Ui_FilterSetWidget


class FilterSetWidget(QWidget, Ui_FilterSetWidget):

    def __init__(self, parent=None):
        super(FilterSetWidget, self).__init__(parent)
        self.setupUi(self)
        self._filterSetActionGroup = QActionGroup(self)
        self._filterSetActionGroup.addAction(self.saveFilterSetAction)
        self._filterSetActionGroup.addAction(self.reloadFilterSetAction)
        self._filterSetActionGroup.addAction(self.deleteFilterSetAction)
        self._filterSetActionGroup.addAction(self.exportFilterSetAction)
        self._filterSetMenu = QMenu(self)
        self._filterSetMenu.addActions(self._filterSetActionGroup.actions())
        self.filterSetTool.setMenu(self._filterSetMenu)
        self.filterSetTool.setDefaultAction(self.saveFilterSetAction)

    def setFilterSet(self, filterSet):
        self.setFilterSetKey(filterSet.key)
        if filterSet.source == 'ark':
            self.saveFilterSetAction.setEnabled(False)
            self.deleteFilterSetAction.setEnabled(False)
            self.filterSetTool.setDefaultAction(self.reloadFilterSetAction)
        else:
            self.saveFilterSetAction.setEnabled(True)
            self.deleteFilterSetAction.setEnabled(True)
            self.filterSetTool.setDefaultAction(self.saveFilterSetAction)

    def setFilterSetKey(self, key):
        self.filterSetCombo.setCurrentIndex(self.filterSetCombo.findData(key))

    def currentFilterSetKey(self):
        return self.filterSetCombo.itemData(self.filterSetCombo.currentIndex())

    def currentFilterSetName(self):
        return self.filterSetCombo.currentText()
