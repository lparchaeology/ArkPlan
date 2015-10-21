# -*- coding: utf-8 -*-

# Form implementation generated from reading ui file 'grid/update_layer_dialog_base.ui'
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

class Ui_UpdateLayerDialog(object):
    def setupUi(self, UpdateLayerDialog):
        UpdateLayerDialog.setObjectName(_fromUtf8("UpdateLayerDialog"))
        UpdateLayerDialog.resize(292, 237)
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
        self.createMapFieldsCheck = QtGui.QCheckBox(UpdateLayerDialog)
        self.createMapFieldsCheck.setObjectName(_fromUtf8("createMapFieldsCheck"))
        self.verticalLayout_3.addWidget(self.createMapFieldsCheck)
        self.groupBox = QtGui.QGroupBox(UpdateLayerDialog)
        self.groupBox.setTitle(_fromUtf8(""))
        self.groupBox.setFlat(True)
        self.groupBox.setObjectName(_fromUtf8("groupBox"))
        self.verticalLayout = QtGui.QVBoxLayout(self.groupBox)
        self.verticalLayout.setObjectName(_fromUtf8("verticalLayout"))
        self.updateFieldsButton = QtGui.QRadioButton(self.groupBox)
        self.updateFieldsButton.setChecked(True)
        self.updateFieldsButton.setObjectName(_fromUtf8("updateFieldsButton"))
        self.verticalLayout.addWidget(self.updateFieldsButton)
        self.updateGeometryButton = QtGui.QRadioButton(self.groupBox)
        self.updateGeometryButton.setObjectName(_fromUtf8("updateGeometryButton"))
        self.verticalLayout.addWidget(self.updateGeometryButton)
        self.verticalLayout_3.addWidget(self.groupBox)
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
        self.createMapFieldsCheck.setText(_translate("UpdateLayerDialog", "Create Map fields if they don\'t exist", None))
        self.updateFieldsButton.setText(_translate("UpdateLayerDialog", "Update fields from geometry", None))
        self.updateGeometryButton.setText(_translate("UpdateLayerDialog", "Update geometry from local fields", None))

