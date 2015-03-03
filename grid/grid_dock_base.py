# -*- coding: utf-8 -*-

# Form implementation generated from reading ui file 'grid/grid_dock_base.ui'
#
# Created: Tue Mar  3 12:45:25 2015
#      by: PyQt4 UI code generator 4.11.3
#
# WARNING! All changes made in this file will be lost!

from PyQt4 import QtCore, QtGui

try:
    _fromUtf8 = QtCore.QString.fromUtf8
except AttributeError:
    def _fromUtf8(s):
        return s

try:
    _encoding = QtGui.QApplication.UnicodeUTF8
    def _translate(context, text, disambig):
        return QtGui.QApplication.translate(context, text, disambig, _encoding)
except AttributeError:
    def _translate(context, text, disambig):
        return QtGui.QApplication.translate(context, text, disambig)

class Ui_GridDock(object):
    def setupUi(self, GridDock):
        GridDock.setObjectName(_fromUtf8("GridDock"))
        GridDock.resize(345, 114)
        self.GridDockContents = QtGui.QWidget()
        self.GridDockContents.setObjectName(_fromUtf8("GridDockContents"))
        self.verticalLayout = QtGui.QVBoxLayout(self.GridDockContents)
        self.verticalLayout.setObjectName(_fromUtf8("verticalLayout"))
        GridDock.setWidget(self.GridDockContents)

        self.retranslateUi(GridDock)
        QtCore.QMetaObject.connectSlotsByName(GridDock)

    def retranslateUi(self, GridDock):
        GridDock.setWindowTitle(_translate("GridDock", "Ark Grid", None))

from ..core.dock import QgsDockWidget
