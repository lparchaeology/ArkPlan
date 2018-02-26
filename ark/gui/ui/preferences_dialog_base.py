# -*- coding: utf-8 -*-

# Form implementation generated from reading ui file 'ark/gui/ui/preferences_dialog_base.ui'
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

class Ui_PreferencesDialogBase(object):
    def setupUi(self, PreferencesDialogBase):
        PreferencesDialogBase.setObjectName(_fromUtf8("PreferencesDialogBase"))
        PreferencesDialogBase.resize(554, 446)
        self.gridLayout = QtGui.QGridLayout(PreferencesDialogBase)
        self.gridLayout.setObjectName(_fromUtf8("gridLayout"))
        self.buttonBox = QtGui.QDialogButtonBox(PreferencesDialogBase)
        self.buttonBox.setOrientation(QtCore.Qt.Horizontal)
        self.buttonBox.setStandardButtons(QtGui.QDialogButtonBox.Cancel|QtGui.QDialogButtonBox.Ok)
        self.buttonBox.setObjectName(_fromUtf8("buttonBox"))
        self.gridLayout.addWidget(self.buttonBox, 5, 0, 1, 1)
        spacerItem = QtGui.QSpacerItem(20, 40, QtGui.QSizePolicy.Minimum, QtGui.QSizePolicy.Expanding)
        self.gridLayout.addItem(spacerItem, 4, 0, 1, 1)
        self.serverWidget = ServerWidget(PreferencesDialogBase)
        self.serverWidget.setObjectName(_fromUtf8("serverWidget"))
        self.gridLayout.addWidget(self.serverWidget, 3, 0, 1, 1)
        self.preferencesWidget = PreferencesWidget(PreferencesDialogBase)
        self.preferencesWidget.setObjectName(_fromUtf8("preferencesWidget"))
        self.gridLayout.addWidget(self.preferencesWidget, 1, 0, 1, 1)
        self.serverLabel = QtGui.QLabel(PreferencesDialogBase)
        font = QtGui.QFont()
        font.setBold(False)
        font.setWeight(50)
        self.serverLabel.setFont(font)
        self.serverLabel.setObjectName(_fromUtf8("serverLabel"))
        self.gridLayout.addWidget(self.serverLabel, 2, 0, 1, 1)
        self.preferencesLabel = QtGui.QLabel(PreferencesDialogBase)
        font = QtGui.QFont()
        font.setBold(False)
        font.setWeight(50)
        self.preferencesLabel.setFont(font)
        self.preferencesLabel.setObjectName(_fromUtf8("preferencesLabel"))
        self.gridLayout.addWidget(self.preferencesLabel, 0, 0, 1, 1)

        self.retranslateUi(PreferencesDialogBase)
        QtCore.QObject.connect(self.buttonBox, QtCore.SIGNAL(_fromUtf8("accepted()")), PreferencesDialogBase.accept)
        QtCore.QObject.connect(self.buttonBox, QtCore.SIGNAL(_fromUtf8("rejected()")), PreferencesDialogBase.reject)
        QtCore.QMetaObject.connectSlotsByName(PreferencesDialogBase)

    def retranslateUi(self, PreferencesDialogBase):
        PreferencesDialogBase.setWindowTitle(_translate("PreferencesDialogBase", "Preferences", None))
        self.serverLabel.setText(_translate("PreferencesDialogBase", "Project Server (Optional)", None))
        self.preferencesLabel.setText(_translate("PreferencesDialogBase", "Project Preferences", None))

from ..preferences_widget import PreferencesWidget
from ..server_widget import ServerWidget
