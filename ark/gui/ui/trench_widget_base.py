# -*- coding: utf-8 -*-

# Form implementation generated from reading ui file 'ark/gui/ui/trench_widget_base.ui'
#
# Created by: PyQt4 UI code generator 4.12.1
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

class Ui_TrenchWidget(object):
    def setupUi(self, TrenchWidget):
        TrenchWidget.setObjectName(_fromUtf8("TrenchWidget"))
        TrenchWidget.resize(443, 172)
        self.gridLayout = QtGui.QGridLayout(TrenchWidget)
        self.gridLayout.setObjectName(_fromUtf8("gridLayout"))
        self.areaCombo = QtGui.QComboBox(TrenchWidget)
        self.areaCombo.setObjectName(_fromUtf8("areaCombo"))
        self.areaCombo.addItem(_fromUtf8(""))
        self.gridLayout.addWidget(self.areaCombo, 1, 2, 1, 2)
        self.areaLabel = QtGui.QLabel(TrenchWidget)
        self.areaLabel.setObjectName(_fromUtf8("areaLabel"))
        self.gridLayout.addWidget(self.areaLabel, 1, 1, 1, 1)
        self.resultLabel = QtGui.QLabel(TrenchWidget)
        self.resultLabel.setObjectName(_fromUtf8("resultLabel"))
        self.gridLayout.addWidget(self.resultLabel, 3, 1, 1, 1)
        self.trenchLabel = QtGui.QLabel(TrenchWidget)
        self.trenchLabel.setObjectName(_fromUtf8("trenchLabel"))
        self.gridLayout.addWidget(self.trenchLabel, 2, 1, 1, 1)
        self.areaSpin = QtGui.QDoubleSpinBox(TrenchWidget)
        self.areaSpin.setFrame(False)
        self.areaSpin.setAlignment(QtCore.Qt.AlignRight|QtCore.Qt.AlignTrailing|QtCore.Qt.AlignVCenter)
        self.areaSpin.setReadOnly(True)
        self.areaSpin.setButtonSymbols(QtGui.QAbstractSpinBox.NoButtons)
        self.areaSpin.setMaximum(9999.99)
        self.areaSpin.setObjectName(_fromUtf8("areaSpin"))
        self.gridLayout.addWidget(self.areaSpin, 1, 4, 1, 1)
        self.sampleAreaSpin = QtGui.QDoubleSpinBox(TrenchWidget)
        self.sampleAreaSpin.setFrame(False)
        self.sampleAreaSpin.setAlignment(QtCore.Qt.AlignRight|QtCore.Qt.AlignTrailing|QtCore.Qt.AlignVCenter)
        self.sampleAreaSpin.setReadOnly(True)
        self.sampleAreaSpin.setButtonSymbols(QtGui.QAbstractSpinBox.NoButtons)
        self.sampleAreaSpin.setMaximum(9999.99)
        self.sampleAreaSpin.setObjectName(_fromUtf8("sampleAreaSpin"))
        self.gridLayout.addWidget(self.sampleAreaSpin, 3, 4, 1, 1)
        self.samplePercentSpin = QtGui.QDoubleSpinBox(TrenchWidget)
        self.samplePercentSpin.setAlignment(QtCore.Qt.AlignRight|QtCore.Qt.AlignTrailing|QtCore.Qt.AlignVCenter)
        self.samplePercentSpin.setProperty("value", 5.0)
        self.samplePercentSpin.setObjectName(_fromUtf8("samplePercentSpin"))
        self.gridLayout.addWidget(self.samplePercentSpin, 2, 4, 1, 1)
        self.sampleLengthSpin = QtGui.QDoubleSpinBox(TrenchWidget)
        self.sampleLengthSpin.setFrame(False)
        self.sampleLengthSpin.setAlignment(QtCore.Qt.AlignRight|QtCore.Qt.AlignTrailing|QtCore.Qt.AlignVCenter)
        self.sampleLengthSpin.setReadOnly(True)
        self.sampleLengthSpin.setButtonSymbols(QtGui.QAbstractSpinBox.NoButtons)
        self.sampleLengthSpin.setMaximum(9999.99)
        self.sampleLengthSpin.setObjectName(_fromUtf8("sampleLengthSpin"))
        self.gridLayout.addWidget(self.sampleLengthSpin, 3, 3, 1, 1)
        self.sampleCountSpin = QtGui.QSpinBox(TrenchWidget)
        self.sampleCountSpin.setFrame(False)
        self.sampleCountSpin.setAlignment(QtCore.Qt.AlignRight|QtCore.Qt.AlignTrailing|QtCore.Qt.AlignVCenter)
        self.sampleCountSpin.setReadOnly(True)
        self.sampleCountSpin.setButtonSymbols(QtGui.QAbstractSpinBox.NoButtons)
        self.sampleCountSpin.setMaximum(999)
        self.sampleCountSpin.setObjectName(_fromUtf8("sampleCountSpin"))
        self.gridLayout.addWidget(self.sampleCountSpin, 3, 2, 1, 1)
        self.lengthSpin = QtGui.QDoubleSpinBox(TrenchWidget)
        self.lengthSpin.setAlignment(QtCore.Qt.AlignRight|QtCore.Qt.AlignTrailing|QtCore.Qt.AlignVCenter)
        self.lengthSpin.setProperty("value", 20.0)
        self.lengthSpin.setObjectName(_fromUtf8("lengthSpin"))
        self.gridLayout.addWidget(self.lengthSpin, 2, 3, 1, 1)
        self.widthSpin = QtGui.QDoubleSpinBox(TrenchWidget)
        self.widthSpin.setAlignment(QtCore.Qt.AlignRight|QtCore.Qt.AlignTrailing|QtCore.Qt.AlignVCenter)
        self.widthSpin.setPrefix(_fromUtf8(""))
        self.widthSpin.setProperty("value", 2.0)
        self.widthSpin.setObjectName(_fromUtf8("widthSpin"))
        self.gridLayout.addWidget(self.widthSpin, 2, 2, 1, 1)
        spacerItem = QtGui.QSpacerItem(20, 40, QtGui.QSizePolicy.Minimum, QtGui.QSizePolicy.Expanding)
        self.gridLayout.addItem(spacerItem, 5, 1, 1, 4)

        self.retranslateUi(TrenchWidget)
        QtCore.QMetaObject.connectSlotsByName(TrenchWidget)

    def retranslateUi(self, TrenchWidget):
        TrenchWidget.setWindowTitle(_translate("TrenchWidget", "Form", None))
        self.areaCombo.setItemText(0, _translate("TrenchWidget", "Site Redline", None))
        self.areaLabel.setText(_translate("TrenchWidget", "Area:", None))
        self.resultLabel.setText(_translate("TrenchWidget", "Result:", None))
        self.trenchLabel.setText(_translate("TrenchWidget", "Trench:", None))
        self.areaSpin.setSuffix(_translate("TrenchWidget", " m2", None))
        self.sampleAreaSpin.setSuffix(_translate("TrenchWidget", " m2", None))
        self.samplePercentSpin.setSuffix(_translate("TrenchWidget", " %", None))
        self.sampleLengthSpin.setSuffix(_translate("TrenchWidget", " m", None))
        self.sampleCountSpin.setSuffix(_translate("TrenchWidget", " trenches", None))
        self.lengthSpin.setSuffix(_translate("TrenchWidget", " m", None))
        self.widthSpin.setSuffix(_translate("TrenchWidget", " m", None))

