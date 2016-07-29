# -*- coding: utf-8 -*-

# Form implementation generated from reading ui file 'grid/grid_widget_base.ui'
#
# Created by: PyQt4 UI code generator 4.11.4
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

class Ui_GridWidget(object):
    def setupUi(self, GridWidget):
        GridWidget.setObjectName(_fromUtf8("GridWidget"))
        GridWidget.resize(309, 135)
        self.verticalLayout = QtGui.QVBoxLayout(GridWidget)
        self.verticalLayout.setObjectName(_fromUtf8("verticalLayout"))
        self.gridLayout = QtGui.QGridLayout()
        self.gridLayout.setObjectName(_fromUtf8("gridLayout"))
        self.gridLabel = QtGui.QLabel(GridWidget)
        self.gridLabel.setObjectName(_fromUtf8("gridLabel"))
        self.gridLayout.addWidget(self.gridLabel, 0, 0, 1, 1)
        self.gridCombo = QtGui.QComboBox(GridWidget)
        self.gridCombo.setObjectName(_fromUtf8("gridCombo"))
        self.gridLayout.addWidget(self.gridCombo, 0, 1, 1, 3)
        self.copyMapPointTool = QtGui.QToolButton(GridWidget)
        icon = QtGui.QIcon()
        icon.addPixmap(QtGui.QPixmap(_fromUtf8(":/plugins/ark/grid/copyPoint.png")), QtGui.QIcon.Normal, QtGui.QIcon.Off)
        self.copyMapPointTool.setIcon(icon)
        self.copyMapPointTool.setObjectName(_fromUtf8("copyMapPointTool"))
        self.gridLayout.addWidget(self.copyMapPointTool, 1, 3, 1, 1)
        self.localLabel = QtGui.QLabel(GridWidget)
        self.localLabel.setObjectName(_fromUtf8("localLabel"))
        self.gridLayout.addWidget(self.localLabel, 2, 0, 1, 1)
        self.localEastingSpin = QtGui.QDoubleSpinBox(GridWidget)
        self.localEastingSpin.setReadOnly(False)
        self.localEastingSpin.setDecimals(3)
        self.localEastingSpin.setMaximum(9999.99)
        self.localEastingSpin.setObjectName(_fromUtf8("localEastingSpin"))
        self.gridLayout.addWidget(self.localEastingSpin, 2, 1, 1, 1)
        self.mapNorthingSpin = QtGui.QDoubleSpinBox(GridWidget)
        self.mapNorthingSpin.setReadOnly(False)
        self.mapNorthingSpin.setDecimals(3)
        self.mapNorthingSpin.setMaximum(999999.999)
        self.mapNorthingSpin.setObjectName(_fromUtf8("mapNorthingSpin"))
        self.gridLayout.addWidget(self.mapNorthingSpin, 1, 2, 1, 1)
        self.copyLocalPointTool = QtGui.QToolButton(GridWidget)
        self.copyLocalPointTool.setIcon(icon)
        self.copyLocalPointTool.setObjectName(_fromUtf8("copyLocalPointTool"))
        self.gridLayout.addWidget(self.copyLocalPointTool, 2, 3, 1, 1)
        self.localNorthingSpin = QtGui.QDoubleSpinBox(GridWidget)
        self.localNorthingSpin.setReadOnly(False)
        self.localNorthingSpin.setDecimals(3)
        self.localNorthingSpin.setMaximum(9999.99)
        self.localNorthingSpin.setObjectName(_fromUtf8("localNorthingSpin"))
        self.gridLayout.addWidget(self.localNorthingSpin, 2, 2, 1, 1)
        self.mapLabel = QtGui.QLabel(GridWidget)
        self.mapLabel.setObjectName(_fromUtf8("mapLabel"))
        self.gridLayout.addWidget(self.mapLabel, 1, 0, 1, 1)
        self.mapEastingSpin = QtGui.QDoubleSpinBox(GridWidget)
        self.mapEastingSpin.setReadOnly(False)
        self.mapEastingSpin.setPrefix(_fromUtf8(""))
        self.mapEastingSpin.setSuffix(_fromUtf8(""))
        self.mapEastingSpin.setDecimals(3)
        self.mapEastingSpin.setMaximum(999999.999)
        self.mapEastingSpin.setObjectName(_fromUtf8("mapEastingSpin"))
        self.gridLayout.addWidget(self.mapEastingSpin, 1, 1, 1, 1)
        self.verticalLayout.addLayout(self.gridLayout)
        spacerItem = QtGui.QSpacerItem(20, 3, QtGui.QSizePolicy.Minimum, QtGui.QSizePolicy.Expanding)
        self.verticalLayout.addItem(spacerItem)
        self.copyMapPointAction = QtGui.QAction(GridWidget)
        self.copyMapPointAction.setIcon(icon)
        self.copyMapPointAction.setObjectName(_fromUtf8("copyMapPointAction"))
        self.copyLocalPointAction = QtGui.QAction(GridWidget)
        self.copyLocalPointAction.setIcon(icon)
        self.copyLocalPointAction.setObjectName(_fromUtf8("copyLocalPointAction"))
        self.gridLabel.setBuddy(self.gridCombo)
        self.localLabel.setBuddy(self.localEastingSpin)
        self.mapLabel.setBuddy(self.mapEastingSpin)

        self.retranslateUi(GridWidget)
        QtCore.QMetaObject.connectSlotsByName(GridWidget)
        GridWidget.setTabOrder(self.gridCombo, self.mapEastingSpin)
        GridWidget.setTabOrder(self.mapEastingSpin, self.mapNorthingSpin)
        GridWidget.setTabOrder(self.mapNorthingSpin, self.copyMapPointTool)
        GridWidget.setTabOrder(self.copyMapPointTool, self.localEastingSpin)
        GridWidget.setTabOrder(self.localEastingSpin, self.localNorthingSpin)
        GridWidget.setTabOrder(self.localNorthingSpin, self.copyLocalPointTool)

    def retranslateUi(self, GridWidget):
        GridWidget.setWindowTitle(_translate("GridWidget", "Form", None))
        self.gridLabel.setText(_translate("GridWidget", "Grid:", None))
        self.copyMapPointTool.setText(_translate("GridWidget", "...", None))
        self.localLabel.setText(_translate("GridWidget", "Local:", None))
        self.copyLocalPointTool.setText(_translate("GridWidget", "...", None))
        self.mapLabel.setText(_translate("GridWidget", "Map:", None))
        self.copyMapPointAction.setText(_translate("GridWidget", "Copy", None))
        self.copyMapPointAction.setToolTip(_translate("GridWidget", "Copy Map Point", None))
        self.copyLocalPointAction.setText(_translate("GridWidget", "Copy", None))
        self.copyLocalPointAction.setToolTip(_translate("GridWidget", "Copy Local Point", None))

import resources
