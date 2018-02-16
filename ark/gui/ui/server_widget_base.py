# -*- coding: utf-8 -*-

# Form implementation generated from reading ui file 'ark/gui/ui/server_widget_base.ui'
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

class Ui_ServerWidget(object):
    def setupUi(self, ServerWidget):
        ServerWidget.setObjectName(_fromUtf8("ServerWidget"))
        ServerWidget.resize(334, 132)
        self.gridLayout = QtGui.QGridLayout(ServerWidget)
        self.gridLayout.setObjectName(_fromUtf8("gridLayout"))
        self.passwordLabel = QtGui.QLabel(ServerWidget)
        self.passwordLabel.setObjectName(_fromUtf8("passwordLabel"))
        self.gridLayout.addWidget(self.passwordLabel, 2, 0, 1, 1)
        self.userEdit = QtGui.QLineEdit(ServerWidget)
        self.userEdit.setObjectName(_fromUtf8("userEdit"))
        self.gridLayout.addWidget(self.userEdit, 1, 1, 1, 1)
        self.userLabel = QtGui.QLabel(ServerWidget)
        self.userLabel.setObjectName(_fromUtf8("userLabel"))
        self.gridLayout.addWidget(self.userLabel, 1, 0, 1, 1)
        self.passwordEdit = QtGui.QLineEdit(ServerWidget)
        self.passwordEdit.setText(_fromUtf8(""))
        self.passwordEdit.setEchoMode(QtGui.QLineEdit.Password)
        self.passwordEdit.setObjectName(_fromUtf8("passwordEdit"))
        self.gridLayout.addWidget(self.passwordEdit, 2, 1, 1, 1)
        self.urlEdit = QtGui.QLineEdit(ServerWidget)
        self.urlEdit.setEnabled(True)
        self.urlEdit.setObjectName(_fromUtf8("urlEdit"))
        self.gridLayout.addWidget(self.urlEdit, 0, 1, 1, 1)
        self.urlLabel = QtGui.QLabel(ServerWidget)
        self.urlLabel.setAlignment(QtCore.Qt.AlignJustify|QtCore.Qt.AlignVCenter)
        self.urlLabel.setWordWrap(True)
        self.urlLabel.setObjectName(_fromUtf8("urlLabel"))
        self.gridLayout.addWidget(self.urlLabel, 0, 0, 1, 1)
        spacerItem = QtGui.QSpacerItem(20, 40, QtGui.QSizePolicy.Minimum, QtGui.QSizePolicy.Expanding)
        self.gridLayout.addItem(spacerItem, 3, 0, 1, 2)
        self.passwordLabel.setBuddy(self.passwordEdit)
        self.userLabel.setBuddy(self.userEdit)
        self.urlLabel.setBuddy(self.urlEdit)

        self.retranslateUi(ServerWidget)
        QtCore.QMetaObject.connectSlotsByName(ServerWidget)

    def retranslateUi(self, ServerWidget):
        ServerWidget.setWindowTitle(_translate("ServerWidget", "ServerWidget", None))
        self.passwordLabel.setText(_translate("ServerWidget", "Password:", None))
        self.userEdit.setPlaceholderText(_translate("ServerWidget", "dgarrod", None))
        self.userLabel.setText(_translate("ServerWidget", "User ID:", None))
        self.passwordEdit.setPlaceholderText(_translate("ServerWidget", "********", None))
        self.urlEdit.setPlaceholderText(_translate("ServerWidget", "http://www.arch.cam.ac.uk/shuqba", None))
        self.urlLabel.setText(_translate("ServerWidget", "ARK URL:", None))

