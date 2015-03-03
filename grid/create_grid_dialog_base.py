# -*- coding: utf-8 -*-

# Form implementation generated from reading ui file 'grid/create_grid_dialog_base.ui'
#
# Created: Tue Mar  3 15:46:43 2015
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

class Ui_CreateGridDialog(object):
    def setupUi(self, CreateGridDialog):
        CreateGridDialog.setObjectName(_fromUtf8("CreateGridDialog"))
        CreateGridDialog.resize(493, 176)
        CreateGridDialog.setSizeGripEnabled(False)
        self.verticalLayout = QtGui.QVBoxLayout(CreateGridDialog)
        self.verticalLayout.setObjectName(_fromUtf8("verticalLayout"))
        self.gridLayout = QtGui.QGridLayout()
        self.gridLayout.setObjectName(_fromUtf8("gridLayout"))
        self.originLabel = QtGui.QLabel(CreateGridDialog)
        self.originLabel.setObjectName(_fromUtf8("originLabel"))
        self.gridLayout.addWidget(self.originLabel, 0, 0, 1, 1)
        self.crsOriginEastingSpin = QtGui.QDoubleSpinBox(CreateGridDialog)
        self.crsOriginEastingSpin.setDecimals(3)
        self.crsOriginEastingSpin.setMaximum(999999.999)
        self.crsOriginEastingSpin.setObjectName(_fromUtf8("crsOriginEastingSpin"))
        self.gridLayout.addWidget(self.crsOriginEastingSpin, 0, 1, 1, 1)
        self.crsOriginNorthingSpin = QtGui.QDoubleSpinBox(CreateGridDialog)
        self.crsOriginNorthingSpin.setDecimals(3)
        self.crsOriginNorthingSpin.setMaximum(999999.999)
        self.crsOriginNorthingSpin.setObjectName(_fromUtf8("crsOriginNorthingSpin"))
        self.gridLayout.addWidget(self.crsOriginNorthingSpin, 0, 2, 1, 1)
        self.originFromMapButton = QtGui.QPushButton(CreateGridDialog)
        self.originFromMapButton.setObjectName(_fromUtf8("originFromMapButton"))
        self.gridLayout.addWidget(self.originFromMapButton, 0, 3, 1, 1)
        self.axisLabel = QtGui.QLabel(CreateGridDialog)
        self.axisLabel.setObjectName(_fromUtf8("axisLabel"))
        self.gridLayout.addWidget(self.axisLabel, 1, 0, 1, 1)
        self.crsAxisEastingSpin = QtGui.QDoubleSpinBox(CreateGridDialog)
        self.crsAxisEastingSpin.setDecimals(3)
        self.crsAxisEastingSpin.setMaximum(999999.999)
        self.crsAxisEastingSpin.setObjectName(_fromUtf8("crsAxisEastingSpin"))
        self.gridLayout.addWidget(self.crsAxisEastingSpin, 1, 1, 1, 1)
        self.crsAxisNorthingSpin = QtGui.QDoubleSpinBox(CreateGridDialog)
        self.crsAxisNorthingSpin.setDecimals(3)
        self.crsAxisNorthingSpin.setMaximum(999999.999)
        self.crsAxisNorthingSpin.setObjectName(_fromUtf8("crsAxisNorthingSpin"))
        self.gridLayout.addWidget(self.crsAxisNorthingSpin, 1, 2, 1, 1)
        self.axisFromMapButton = QtGui.QPushButton(CreateGridDialog)
        self.axisFromMapButton.setObjectName(_fromUtf8("axisFromMapButton"))
        self.gridLayout.addWidget(self.axisFromMapButton, 1, 3, 1, 1)
        self.verticalLayout.addLayout(self.gridLayout)
        self.horizontalLayout_2 = QtGui.QHBoxLayout()
        self.horizontalLayout_2.setObjectName(_fromUtf8("horizontalLayout_2"))
        self.label_3 = QtGui.QLabel(CreateGridDialog)
        self.label_3.setObjectName(_fromUtf8("label_3"))
        self.horizontalLayout_2.addWidget(self.label_3)
        self.xAxisButton = QtGui.QRadioButton(CreateGridDialog)
        self.xAxisButton.setObjectName(_fromUtf8("xAxisButton"))
        self.horizontalLayout_2.addWidget(self.xAxisButton)
        self.yAxisButton = QtGui.QRadioButton(CreateGridDialog)
        self.yAxisButton.setObjectName(_fromUtf8("yAxisButton"))
        self.horizontalLayout_2.addWidget(self.yAxisButton)
        spacerItem = QtGui.QSpacerItem(40, 20, QtGui.QSizePolicy.Expanding, QtGui.QSizePolicy.Minimum)
        self.horizontalLayout_2.addItem(spacerItem)
        self.verticalLayout.addLayout(self.horizontalLayout_2)
        self.horizontalLayout = QtGui.QHBoxLayout()
        self.horizontalLayout.setObjectName(_fromUtf8("horizontalLayout"))
        spacerItem1 = QtGui.QSpacerItem(40, 20, QtGui.QSizePolicy.Expanding, QtGui.QSizePolicy.Minimum)
        self.horizontalLayout.addItem(spacerItem1)
        self.cancelButton = QtGui.QPushButton(CreateGridDialog)
        self.cancelButton.setObjectName(_fromUtf8("cancelButton"))
        self.horizontalLayout.addWidget(self.cancelButton)
        self.createGridButton = QtGui.QPushButton(CreateGridDialog)
        self.createGridButton.setDefault(True)
        self.createGridButton.setObjectName(_fromUtf8("createGridButton"))
        self.horizontalLayout.addWidget(self.createGridButton)
        self.verticalLayout.addLayout(self.horizontalLayout)
        self.originLabel.setBuddy(self.crsOriginEastingSpin)
        self.axisLabel.setBuddy(self.crsAxisEastingSpin)
        self.label_3.setBuddy(self.xAxisButton)

        self.retranslateUi(CreateGridDialog)
        QtCore.QMetaObject.connectSlotsByName(CreateGridDialog)
        CreateGridDialog.setTabOrder(self.crsOriginEastingSpin, self.crsOriginNorthingSpin)
        CreateGridDialog.setTabOrder(self.crsOriginNorthingSpin, self.originFromMapButton)
        CreateGridDialog.setTabOrder(self.originFromMapButton, self.crsAxisEastingSpin)
        CreateGridDialog.setTabOrder(self.crsAxisEastingSpin, self.crsAxisNorthingSpin)
        CreateGridDialog.setTabOrder(self.crsAxisNorthingSpin, self.axisFromMapButton)
        CreateGridDialog.setTabOrder(self.axisFromMapButton, self.xAxisButton)
        CreateGridDialog.setTabOrder(self.xAxisButton, self.yAxisButton)
        CreateGridDialog.setTabOrder(self.yAxisButton, self.cancelButton)
        CreateGridDialog.setTabOrder(self.cancelButton, self.createGridButton)

    def retranslateUi(self, CreateGridDialog):
        CreateGridDialog.setWindowTitle(_translate("CreateGridDialog", "Create Grid", None))
        self.originLabel.setText(_translate("CreateGridDialog", "Origin Coordinates:", None))
        self.originFromMapButton.setText(_translate("CreateGridDialog", "From Map", None))
        self.axisLabel.setText(_translate("CreateGridDialog", "Axis Coordinates:", None))
        self.axisFromMapButton.setText(_translate("CreateGridDialog", "From Map", None))
        self.label_3.setText(_translate("CreateGridDialog", "On Axis:", None))
        self.xAxisButton.setText(_translate("CreateGridDialog", "X Axis / Easting", None))
        self.yAxisButton.setText(_translate("CreateGridDialog", "Y Axis / Northing", None))
        self.cancelButton.setText(_translate("CreateGridDialog", "Cancel", None))
        self.createGridButton.setText(_translate("CreateGridDialog", "Create", None))

