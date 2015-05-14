# -*- coding: utf-8 -*-

# Form implementation generated from reading ui file 'grid/update_layer_dialog_base.ui'
#
# Created: Thu May 14 16:16:29 2015
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

class Ui_UpdateLayerDialog(object):
    def setupUi(self, UpdateLayerDialog):
        UpdateLayerDialog.setObjectName(_fromUtf8("UpdateLayerDialog"))
        UpdateLayerDialog.resize(293, 332)
        self.verticalLayout_3 = QtGui.QVBoxLayout(UpdateLayerDialog)
        self.verticalLayout_3.setObjectName(_fromUtf8("verticalLayout_3"))
        self.headerLabel = QtGui.QLabel(UpdateLayerDialog)
        self.headerLabel.setAlignment(QtCore.Qt.AlignCenter)
        self.headerLabel.setObjectName(_fromUtf8("headerLabel"))
        self.verticalLayout_3.addWidget(self.headerLabel)
        self.horizontalLayout = QtGui.QHBoxLayout()
        self.horizontalLayout.setObjectName(_fromUtf8("horizontalLayout"))
        self.layerLabel = QtGui.QLabel(UpdateLayerDialog)
        self.layerLabel.setObjectName(_fromUtf8("layerLabel"))
        self.horizontalLayout.addWidget(self.layerLabel)
        self.layerComboBox = QtGui.QComboBox(UpdateLayerDialog)
        self.layerComboBox.setObjectName(_fromUtf8("layerComboBox"))
        self.horizontalLayout.addWidget(self.layerComboBox)
        self.verticalLayout_3.addLayout(self.horizontalLayout)
        self.groupBox = QtGui.QGroupBox(UpdateLayerDialog)
        self.groupBox.setTitle(_fromUtf8(""))
        self.groupBox.setFlat(True)
        self.groupBox.setObjectName(_fromUtf8("groupBox"))
        self.verticalLayout = QtGui.QVBoxLayout(self.groupBox)
        self.verticalLayout.setObjectName(_fromUtf8("verticalLayout"))
        self.updateFieldsButton = QtGui.QRadioButton(self.groupBox)
        self.updateFieldsButton.setObjectName(_fromUtf8("updateFieldsButton"))
        self.verticalLayout.addWidget(self.updateFieldsButton)
        self.updateGeometryFromLocalButton = QtGui.QRadioButton(self.groupBox)
        self.updateGeometryFromLocalButton.setObjectName(_fromUtf8("updateGeometryFromLocalButton"))
        self.verticalLayout.addWidget(self.updateGeometryFromLocalButton)
        self.updateGeometryFromCrsButton = QtGui.QRadioButton(self.groupBox)
        self.updateGeometryFromCrsButton.setObjectName(_fromUtf8("updateGeometryFromCrsButton"))
        self.verticalLayout.addWidget(self.updateGeometryFromCrsButton)
        self.updateLocalFieldsButton = QtGui.QRadioButton(self.groupBox)
        self.updateLocalFieldsButton.setObjectName(_fromUtf8("updateLocalFieldsButton"))
        self.verticalLayout.addWidget(self.updateLocalFieldsButton)
        self.updateCrsFieldsButton = QtGui.QRadioButton(self.groupBox)
        self.updateCrsFieldsButton.setObjectName(_fromUtf8("updateCrsFieldsButton"))
        self.verticalLayout.addWidget(self.updateCrsFieldsButton)
        self.verticalLayout_3.addWidget(self.groupBox)
        self.groupBox_2 = QtGui.QGroupBox(UpdateLayerDialog)
        self.groupBox_2.setTitle(_fromUtf8(""))
        self.groupBox_2.setFlat(True)
        self.groupBox_2.setObjectName(_fromUtf8("groupBox_2"))
        self.verticalLayout_2 = QtGui.QVBoxLayout(self.groupBox_2)
        self.verticalLayout_2.setObjectName(_fromUtf8("verticalLayout_2"))
        self.createLocalFields = QtGui.QCheckBox(self.groupBox_2)
        self.createLocalFields.setObjectName(_fromUtf8("createLocalFields"))
        self.verticalLayout_2.addWidget(self.createLocalFields)
        self.createCrsFields = QtGui.QCheckBox(self.groupBox_2)
        self.createCrsFields.setObjectName(_fromUtf8("createCrsFields"))
        self.verticalLayout_2.addWidget(self.createCrsFields)
        self.verticalLayout_3.addWidget(self.groupBox_2)
        spacerItem = QtGui.QSpacerItem(20, 0, QtGui.QSizePolicy.Minimum, QtGui.QSizePolicy.Expanding)
        self.verticalLayout_3.addItem(spacerItem)
        self.buttonBox = QtGui.QDialogButtonBox(UpdateLayerDialog)
        self.buttonBox.setOrientation(QtCore.Qt.Horizontal)
        self.buttonBox.setStandardButtons(QtGui.QDialogButtonBox.Cancel|QtGui.QDialogButtonBox.Ok)
        self.buttonBox.setObjectName(_fromUtf8("buttonBox"))
        self.verticalLayout_3.addWidget(self.buttonBox)

        self.retranslateUi(UpdateLayerDialog)
        QtCore.QObject.connect(self.buttonBox, QtCore.SIGNAL(_fromUtf8("accepted()")), UpdateLayerDialog.accept)
        QtCore.QObject.connect(self.buttonBox, QtCore.SIGNAL(_fromUtf8("rejected()")), UpdateLayerDialog.reject)
        QtCore.QMetaObject.connectSlotsByName(UpdateLayerDialog)

    def retranslateUi(self, UpdateLayerDialog):
        UpdateLayerDialog.setWindowTitle(_translate("UpdateLayerDialog", "Dialog", None))
        self.headerLabel.setText(_translate("UpdateLayerDialog", "Update Layer Coordinates", None))
        self.layerLabel.setText(_translate("UpdateLayerDialog", "Layer:", None))
        self.updateFieldsButton.setText(_translate("UpdateLayerDialog", "Update fields from geometry", None))
        self.updateGeometryFromLocalButton.setText(_translate("UpdateLayerDialog", "Update geometry from Local fields", None))
        self.updateGeometryFromCrsButton.setText(_translate("UpdateLayerDialog", "Update geometry from CRS fields", None))
        self.updateLocalFieldsButton.setText(_translate("UpdateLayerDialog", "Update Local fields from CRS fields", None))
        self.updateCrsFieldsButton.setText(_translate("UpdateLayerDialog", "Update CRS fields from Local fields", None))
        self.createLocalFields.setText(_translate("UpdateLayerDialog", "Create Local fields if they don\'t exist", None))
        self.createCrsFields.setText(_translate("UpdateLayerDialog", "Create CRS fields if they don\'t exist", None))

