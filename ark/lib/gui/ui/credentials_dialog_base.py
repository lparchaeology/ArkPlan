# -*- coding: utf-8 -*-

# Form implementation generated from reading ui file 'ark/lib/gui/ui/credentials_dialog_base.ui'
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

class Ui_CredentialsDialog(object):
    def setupUi(self, CredentialsDialog):
        CredentialsDialog.setObjectName(_fromUtf8("CredentialsDialog"))
        CredentialsDialog.resize(330, 175)
        self.verticalLayout = QtGui.QVBoxLayout(CredentialsDialog)
        self.verticalLayout.setObjectName(_fromUtf8("verticalLayout"))
        self.label = QtGui.QLabel(CredentialsDialog)
        self.label.setObjectName(_fromUtf8("label"))
        self.verticalLayout.addWidget(self.label)
        self.gridLayout = QtGui.QGridLayout()
        self.gridLayout.setObjectName(_fromUtf8("gridLayout"))
        self.usernameLabel = QtGui.QLabel(CredentialsDialog)
        self.usernameLabel.setObjectName(_fromUtf8("usernameLabel"))
        self.gridLayout.addWidget(self.usernameLabel, 0, 0, 1, 1)
        self.usernameEdit = QtGui.QLineEdit(CredentialsDialog)
        self.usernameEdit.setObjectName(_fromUtf8("usernameEdit"))
        self.gridLayout.addWidget(self.usernameEdit, 0, 1, 1, 1)
        self.passwordLabel = QtGui.QLabel(CredentialsDialog)
        self.passwordLabel.setObjectName(_fromUtf8("passwordLabel"))
        self.gridLayout.addWidget(self.passwordLabel, 1, 0, 1, 1)
        self.passwordEdit = QtGui.QLineEdit(CredentialsDialog)
        self.passwordEdit.setObjectName(_fromUtf8("passwordEdit"))
        self.gridLayout.addWidget(self.passwordEdit, 1, 1, 1, 1)
        self.verticalLayout.addLayout(self.gridLayout)
        spacerItem = QtGui.QSpacerItem(20, 18, QtGui.QSizePolicy.Minimum, QtGui.QSizePolicy.Expanding)
        self.verticalLayout.addItem(spacerItem)
        self.buttonBox = QtGui.QDialogButtonBox(CredentialsDialog)
        self.buttonBox.setOrientation(QtCore.Qt.Horizontal)
        self.buttonBox.setStandardButtons(QtGui.QDialogButtonBox.Cancel|QtGui.QDialogButtonBox.Ok)
        self.buttonBox.setObjectName(_fromUtf8("buttonBox"))
        self.verticalLayout.addWidget(self.buttonBox)

        self.retranslateUi(CredentialsDialog)
        QtCore.QObject.connect(self.buttonBox, QtCore.SIGNAL(_fromUtf8("accepted()")), CredentialsDialog.accept)
        QtCore.QObject.connect(self.buttonBox, QtCore.SIGNAL(_fromUtf8("rejected()")), CredentialsDialog.reject)
        QtCore.QMetaObject.connectSlotsByName(CredentialsDialog)

    def retranslateUi(self, CredentialsDialog):
        CredentialsDialog.setWindowTitle(_translate("CredentialsDialog", "Dialog", None))
        self.label.setText(_translate("CredentialsDialog", "Please enter your ARK username and password:", None))
        self.usernameLabel.setText(_translate("CredentialsDialog", "Username:", None))
        self.passwordLabel.setText(_translate("CredentialsDialog", "Password:", None))

