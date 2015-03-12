# -*- coding: utf-8 -*-

# Form implementation generated from reading ui file 'grid/grid_dock_base.ui'
#
# Created: Thu Mar 12 12:58:40 2015
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
        GridDock.resize(347, 159)
        self.GridDockContents = QtGui.QWidget()
        self.GridDockContents.setObjectName(_fromUtf8("GridDockContents"))
        self.verticalLayout = QtGui.QVBoxLayout(self.GridDockContents)
        self.verticalLayout.setObjectName(_fromUtf8("verticalLayout"))
        self.horizontalLayout = QtGui.QHBoxLayout()
        self.horizontalLayout.setObjectName(_fromUtf8("horizontalLayout"))
        self.mapGridTool = QtGui.QToolButton(self.GridDockContents)
        self.mapGridTool.setCheckable(True)
        self.mapGridTool.setObjectName(_fromUtf8("mapGridTool"))
        self.horizontalLayout.addWidget(self.mapGridTool)
        spacerItem = QtGui.QSpacerItem(40, 20, QtGui.QSizePolicy.Expanding, QtGui.QSizePolicy.Minimum)
        self.horizontalLayout.addItem(spacerItem)
        self.newGridTool = QtGui.QToolButton(self.GridDockContents)
        self.newGridTool.setToolTip(_fromUtf8(""))
        self.newGridTool.setObjectName(_fromUtf8("newGridTool"))
        self.horizontalLayout.addWidget(self.newGridTool)
        self.verticalLayout.addLayout(self.horizontalLayout)
        self.gridLayout = QtGui.QGridLayout()
        self.gridLayout.setObjectName(_fromUtf8("gridLayout"))
        self.crsLabel = QtGui.QLabel(self.GridDockContents)
        self.crsLabel.setObjectName(_fromUtf8("crsLabel"))
        self.gridLayout.addWidget(self.crsLabel, 0, 0, 1, 1)
        self.crsEastingSpin = QtGui.QDoubleSpinBox(self.GridDockContents)
        self.crsEastingSpin.setReadOnly(True)
        self.crsEastingSpin.setPrefix(_fromUtf8(""))
        self.crsEastingSpin.setSuffix(_fromUtf8(""))
        self.crsEastingSpin.setDecimals(3)
        self.crsEastingSpin.setMaximum(999999.999)
        self.crsEastingSpin.setObjectName(_fromUtf8("crsEastingSpin"))
        self.gridLayout.addWidget(self.crsEastingSpin, 0, 1, 1, 1)
        self.crsNorthingSpin = QtGui.QDoubleSpinBox(self.GridDockContents)
        self.crsNorthingSpin.setReadOnly(True)
        self.crsNorthingSpin.setDecimals(3)
        self.crsNorthingSpin.setMaximum(999999.999)
        self.crsNorthingSpin.setObjectName(_fromUtf8("crsNorthingSpin"))
        self.gridLayout.addWidget(self.crsNorthingSpin, 0, 2, 1, 1)
        self.localLabel = QtGui.QLabel(self.GridDockContents)
        self.localLabel.setObjectName(_fromUtf8("localLabel"))
        self.gridLayout.addWidget(self.localLabel, 1, 0, 1, 1)
        self.localEastingSpin = QtGui.QDoubleSpinBox(self.GridDockContents)
        self.localEastingSpin.setReadOnly(True)
        self.localEastingSpin.setDecimals(3)
        self.localEastingSpin.setMaximum(9999.99)
        self.localEastingSpin.setObjectName(_fromUtf8("localEastingSpin"))
        self.gridLayout.addWidget(self.localEastingSpin, 1, 1, 1, 1)
        self.localNorthingSpin = QtGui.QDoubleSpinBox(self.GridDockContents)
        self.localNorthingSpin.setReadOnly(True)
        self.localNorthingSpin.setDecimals(3)
        self.localNorthingSpin.setMaximum(9999.99)
        self.localNorthingSpin.setObjectName(_fromUtf8("localNorthingSpin"))
        self.gridLayout.addWidget(self.localNorthingSpin, 1, 2, 1, 1)
        self.verticalLayout.addLayout(self.gridLayout)
        spacerItem1 = QtGui.QSpacerItem(20, 4, QtGui.QSizePolicy.Minimum, QtGui.QSizePolicy.Expanding)
        self.verticalLayout.addItem(spacerItem1)
        GridDock.setWidget(self.GridDockContents)
        self.crsLabel.setBuddy(self.crsEastingSpin)
        self.localLabel.setBuddy(self.localEastingSpin)

        self.retranslateUi(GridDock)
        QtCore.QMetaObject.connectSlotsByName(GridDock)

    def retranslateUi(self, GridDock):
        GridDock.setWindowTitle(_translate("GridDock", "Local Grid", None))
        self.mapGridTool.setText(_translate("GridDock", "Map", None))
        self.newGridTool.setText(_translate("GridDock", "New", None))
        self.crsLabel.setText(_translate("GridDock", "CRS:", None))
        self.localLabel.setText(_translate("GridDock", "Local:", None))

from ..core.dock import QgsDockWidget
