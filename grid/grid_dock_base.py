# -*- coding: utf-8 -*-

# Form implementation generated from reading ui file 'grid/grid_dock_base.ui'
#
# Created: Tue Mar  3 15:09:04 2015
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
        GridDock.resize(373, 157)
        self.GridDockContents = QtGui.QWidget()
        self.GridDockContents.setObjectName(_fromUtf8("GridDockContents"))
        self.verticalLayout = QtGui.QVBoxLayout(self.GridDockContents)
        self.verticalLayout.setObjectName(_fromUtf8("verticalLayout"))
        self.horizontalLayout = QtGui.QHBoxLayout()
        self.horizontalLayout.setObjectName(_fromUtf8("horizontalLayout"))
        self.mapToolButton = QtGui.QRadioButton(self.GridDockContents)
        self.mapToolButton.setChecked(True)
        self.mapToolButton.setObjectName(_fromUtf8("mapToolButton"))
        self.horizontalLayout.addWidget(self.mapToolButton)
        self.enterCrsButton = QtGui.QRadioButton(self.GridDockContents)
        self.enterCrsButton.setObjectName(_fromUtf8("enterCrsButton"))
        self.horizontalLayout.addWidget(self.enterCrsButton)
        self.enterLocalButton = QtGui.QRadioButton(self.GridDockContents)
        self.enterLocalButton.setObjectName(_fromUtf8("enterLocalButton"))
        self.horizontalLayout.addWidget(self.enterLocalButton)
        self.verticalLayout.addLayout(self.horizontalLayout)
        self.gridLayout = QtGui.QGridLayout()
        self.gridLayout.setObjectName(_fromUtf8("gridLayout"))
        self.label = QtGui.QLabel(self.GridDockContents)
        self.label.setObjectName(_fromUtf8("label"))
        self.gridLayout.addWidget(self.label, 0, 0, 1, 1)
        self.crsEastingSpin = QtGui.QDoubleSpinBox(self.GridDockContents)
        self.crsEastingSpin.setReadOnly(True)
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
        self.label_2 = QtGui.QLabel(self.GridDockContents)
        self.label_2.setObjectName(_fromUtf8("label_2"))
        self.gridLayout.addWidget(self.label_2, 1, 0, 1, 1)
        self.localEastingSpin = QtGui.QDoubleSpinBox(self.GridDockContents)
        self.localEastingSpin.setReadOnly(True)
        self.localEastingSpin.setMaximum(999.99)
        self.localEastingSpin.setObjectName(_fromUtf8("localEastingSpin"))
        self.gridLayout.addWidget(self.localEastingSpin, 1, 1, 1, 1)
        self.localNorthingSpin = QtGui.QDoubleSpinBox(self.GridDockContents)
        self.localNorthingSpin.setReadOnly(True)
        self.localNorthingSpin.setMaximum(999.99)
        self.localNorthingSpin.setObjectName(_fromUtf8("localNorthingSpin"))
        self.gridLayout.addWidget(self.localNorthingSpin, 1, 2, 1, 1)
        self.verticalLayout.addLayout(self.gridLayout)
        spacerItem = QtGui.QSpacerItem(20, 4, QtGui.QSizePolicy.Minimum, QtGui.QSizePolicy.Expanding)
        self.verticalLayout.addItem(spacerItem)
        GridDock.setWidget(self.GridDockContents)
        self.label.setBuddy(self.crsEastingSpin)
        self.label_2.setBuddy(self.localEastingSpin)

        self.retranslateUi(GridDock)
        QtCore.QMetaObject.connectSlotsByName(GridDock)

    def retranslateUi(self, GridDock):
        GridDock.setWindowTitle(_translate("GridDock", "Local Grid", None))
        self.mapToolButton.setText(_translate("GridDock", "Map Tool", None))
        self.enterCrsButton.setText(_translate("GridDock", "Enter CRS", None))
        self.enterLocalButton.setText(_translate("GridDock", "Enter Local", None))
        self.label.setText(_translate("GridDock", "CRS Coordinates:", None))
        self.label_2.setText(_translate("GridDock", "Local Coordinates:", None))

from ..core.dock import QgsDockWidget
