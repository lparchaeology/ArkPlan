# -*- coding: utf-8 -*-

# Form implementation generated from reading ui file 'grid/translate_features_dialog_base.ui'
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

class Ui_TranslateFeaturesDialog(object):
    def setupUi(self, TranslateFeaturesDialog):
        TranslateFeaturesDialog.setObjectName(_fromUtf8("TranslateFeaturesDialog"))
        TranslateFeaturesDialog.resize(245, 276)
        self.verticalLayout_3 = QtGui.QVBoxLayout(TranslateFeaturesDialog)
        self.verticalLayout_3.setContentsMargins(-1, -1, -1, 0)
        self.verticalLayout_3.setObjectName(_fromUtf8("verticalLayout_3"))
        self.headerLabel = QtGui.QLabel(TranslateFeaturesDialog)
        self.headerLabel.setAlignment(QtCore.Qt.AlignCenter)
        self.headerLabel.setObjectName(_fromUtf8("headerLabel"))
        self.verticalLayout_3.addWidget(self.headerLabel)
        self.gridLayout = QtGui.QGridLayout()
        self.gridLayout.setObjectName(_fromUtf8("gridLayout"))
        self.translateNorthSpin = QtGui.QDoubleSpinBox(TranslateFeaturesDialog)
        self.translateNorthSpin.setObjectName(_fromUtf8("translateNorthSpin"))
        self.gridLayout.addWidget(self.translateNorthSpin, 2, 1, 1, 1)
        self.layerComboBox = QtGui.QComboBox(TranslateFeaturesDialog)
        self.layerComboBox.setObjectName(_fromUtf8("layerComboBox"))
        self.gridLayout.addWidget(self.layerComboBox, 0, 1, 1, 1)
        self.translateNorthLabel = QtGui.QLabel(TranslateFeaturesDialog)
        self.translateNorthLabel.setObjectName(_fromUtf8("translateNorthLabel"))
        self.gridLayout.addWidget(self.translateNorthLabel, 2, 0, 1, 1)
        self.layerLabel = QtGui.QLabel(TranslateFeaturesDialog)
        self.layerLabel.setObjectName(_fromUtf8("layerLabel"))
        self.gridLayout.addWidget(self.layerLabel, 0, 0, 1, 1)
        self.translateEastLabel = QtGui.QLabel(TranslateFeaturesDialog)
        self.translateEastLabel.setObjectName(_fromUtf8("translateEastLabel"))
        self.gridLayout.addWidget(self.translateEastLabel, 1, 0, 1, 1)
        self.translateEastSpin = QtGui.QDoubleSpinBox(TranslateFeaturesDialog)
        self.translateEastSpin.setObjectName(_fromUtf8("translateEastSpin"))
        self.gridLayout.addWidget(self.translateEastSpin, 1, 1, 1, 1)
        self.verticalLayout_3.addLayout(self.gridLayout)
        self.groupBox = QtGui.QGroupBox(TranslateFeaturesDialog)
        self.groupBox.setTitle(_fromUtf8(""))
        self.groupBox.setFlat(True)
        self.groupBox.setObjectName(_fromUtf8("groupBox"))
        self.verticalLayout = QtGui.QVBoxLayout(self.groupBox)
        self.verticalLayout.setContentsMargins(0, -1, 0, -1)
        self.verticalLayout.setObjectName(_fromUtf8("verticalLayout"))
        self.selectedFeaturesButton = QtGui.QRadioButton(self.groupBox)
        self.selectedFeaturesButton.setChecked(True)
        self.selectedFeaturesButton.setObjectName(_fromUtf8("selectedFeaturesButton"))
        self.verticalLayout.addWidget(self.selectedFeaturesButton)
        self.allFeaturesButton = QtGui.QRadioButton(self.groupBox)
        self.allFeaturesButton.setObjectName(_fromUtf8("allFeaturesButton"))
        self.verticalLayout.addWidget(self.allFeaturesButton)
        self.verticalLayout_3.addWidget(self.groupBox)
        spacerItem = QtGui.QSpacerItem(20, 0, QtGui.QSizePolicy.Minimum, QtGui.QSizePolicy.Expanding)
        self.verticalLayout_3.addItem(spacerItem)
        self.buttonBox = QtGui.QDialogButtonBox(TranslateFeaturesDialog)
        self.buttonBox.setOrientation(QtCore.Qt.Horizontal)
        self.buttonBox.setStandardButtons(QtGui.QDialogButtonBox.Cancel|QtGui.QDialogButtonBox.Ok)
        self.buttonBox.setObjectName(_fromUtf8("buttonBox"))
        self.verticalLayout_3.addWidget(self.buttonBox)
        self.translateNorthLabel.setBuddy(self.translateNorthSpin)
        self.layerLabel.setBuddy(self.layerComboBox)
        self.translateEastLabel.setBuddy(self.translateEastSpin)

        self.retranslateUi(TranslateFeaturesDialog)
        QtCore.QObject.connect(self.buttonBox, QtCore.SIGNAL(_fromUtf8("accepted()")), TranslateFeaturesDialog.accept)
        QtCore.QObject.connect(self.buttonBox, QtCore.SIGNAL(_fromUtf8("rejected()")), TranslateFeaturesDialog.reject)
        QtCore.QMetaObject.connectSlotsByName(TranslateFeaturesDialog)
        TranslateFeaturesDialog.setTabOrder(self.layerComboBox, self.translateEastSpin)
        TranslateFeaturesDialog.setTabOrder(self.translateEastSpin, self.translateNorthSpin)
        TranslateFeaturesDialog.setTabOrder(self.translateNorthSpin, self.selectedFeaturesButton)
        TranslateFeaturesDialog.setTabOrder(self.selectedFeaturesButton, self.allFeaturesButton)
        TranslateFeaturesDialog.setTabOrder(self.allFeaturesButton, self.buttonBox)

    def retranslateUi(self, TranslateFeaturesDialog):
        TranslateFeaturesDialog.setWindowTitle(_translate("TranslateFeaturesDialog", "Dialog", None))
        self.headerLabel.setText(_translate("TranslateFeaturesDialog", "Translate Features Relative To Grid", None))
        self.translateNorthLabel.setText(_translate("TranslateFeaturesDialog", "Translate North", None))
        self.layerLabel.setText(_translate("TranslateFeaturesDialog", "Layer:", None))
        self.translateEastLabel.setText(_translate("TranslateFeaturesDialog", "Translate East", None))
        self.selectedFeaturesButton.setText(_translate("TranslateFeaturesDialog", "Selected Features Only", None))
        self.allFeaturesButton.setText(_translate("TranslateFeaturesDialog", "All Features", None))

