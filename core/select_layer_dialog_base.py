# -*- coding: utf-8 -*-

# Form implementation generated from reading ui file 'core/select_layer_dialog_base.ui'
#
# Created: Mon Apr 13 15:58:21 2015
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

class Ui_SelectLayerDialog(object):
    def setupUi(self, SelectLayerDialog):
        SelectLayerDialog.setObjectName(_fromUtf8("SelectLayerDialog"))
        SelectLayerDialog.resize(217, 90)
        self.verticalLayout = QtGui.QVBoxLayout(SelectLayerDialog)
        self.verticalLayout.setObjectName(_fromUtf8("verticalLayout"))
        self.horizontalLayout = QtGui.QHBoxLayout()
        self.horizontalLayout.setObjectName(_fromUtf8("horizontalLayout"))
        self.layerLabel = QtGui.QLabel(SelectLayerDialog)
        self.layerLabel.setObjectName(_fromUtf8("layerLabel"))
        self.horizontalLayout.addWidget(self.layerLabel)
        self.layerComboBox = QtGui.QComboBox(SelectLayerDialog)
        self.layerComboBox.setObjectName(_fromUtf8("layerComboBox"))
        self.horizontalLayout.addWidget(self.layerComboBox)
        self.verticalLayout.addLayout(self.horizontalLayout)
        self.buttonBox = QtGui.QDialogButtonBox(SelectLayerDialog)
        self.buttonBox.setOrientation(QtCore.Qt.Horizontal)
        self.buttonBox.setStandardButtons(QtGui.QDialogButtonBox.Cancel|QtGui.QDialogButtonBox.Ok)
        self.buttonBox.setObjectName(_fromUtf8("buttonBox"))
        self.verticalLayout.addWidget(self.buttonBox)

        self.retranslateUi(SelectLayerDialog)
        QtCore.QObject.connect(self.buttonBox, QtCore.SIGNAL(_fromUtf8("accepted()")), SelectLayerDialog.accept)
        QtCore.QObject.connect(self.buttonBox, QtCore.SIGNAL(_fromUtf8("rejected()")), SelectLayerDialog.reject)
        QtCore.QMetaObject.connectSlotsByName(SelectLayerDialog)

    def retranslateUi(self, SelectLayerDialog):
        SelectLayerDialog.setWindowTitle(_translate("SelectLayerDialog", "Dialog", None))
        self.layerLabel.setText(_translate("SelectLayerDialog", "Select layer:", None))

