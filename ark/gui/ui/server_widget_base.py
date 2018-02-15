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

class Ui_Form(object):
    def setupUi(self, Form):
        Form.setObjectName(_fromUtf8("Form"))
        Form.resize(334, 132)
        self.gridLayout = QtGui.QGridLayout(Form)
        self.gridLayout.setObjectName(_fromUtf8("gridLayout"))
        self.arkPasswordLabel = QtGui.QLabel(Form)
        self.arkPasswordLabel.setObjectName(_fromUtf8("arkPasswordLabel"))
        self.gridLayout.addWidget(self.arkPasswordLabel, 2, 0, 1, 1)
        self.arkUserEdit = QtGui.QLineEdit(Form)
        self.arkUserEdit.setObjectName(_fromUtf8("arkUserEdit"))
        self.gridLayout.addWidget(self.arkUserEdit, 1, 1, 1, 1)
        self.arkUserLabel = QtGui.QLabel(Form)
        self.arkUserLabel.setObjectName(_fromUtf8("arkUserLabel"))
        self.gridLayout.addWidget(self.arkUserLabel, 1, 0, 1, 1)
        self.arkPasswordEdit = QtGui.QLineEdit(Form)
        self.arkPasswordEdit.setText(_fromUtf8(""))
        self.arkPasswordEdit.setEchoMode(QtGui.QLineEdit.Password)
        self.arkPasswordEdit.setObjectName(_fromUtf8("arkPasswordEdit"))
        self.gridLayout.addWidget(self.arkPasswordEdit, 2, 1, 1, 1)
        self.arkUrlEdit = QtGui.QLineEdit(Form)
        self.arkUrlEdit.setEnabled(True)
        self.arkUrlEdit.setObjectName(_fromUtf8("arkUrlEdit"))
        self.gridLayout.addWidget(self.arkUrlEdit, 0, 1, 1, 1)
        self.arkUrlLabel = QtGui.QLabel(Form)
        self.arkUrlLabel.setAlignment(QtCore.Qt.AlignJustify|QtCore.Qt.AlignVCenter)
        self.arkUrlLabel.setWordWrap(True)
        self.arkUrlLabel.setObjectName(_fromUtf8("arkUrlLabel"))
        self.gridLayout.addWidget(self.arkUrlLabel, 0, 0, 1, 1)
        spacerItem = QtGui.QSpacerItem(20, 40, QtGui.QSizePolicy.Minimum, QtGui.QSizePolicy.Expanding)
        self.gridLayout.addItem(spacerItem, 3, 0, 1, 2)
        self.arkPasswordLabel.setBuddy(self.arkPasswordEdit)
        self.arkUserLabel.setBuddy(self.arkUserEdit)
        self.arkUrlLabel.setBuddy(self.arkUrlEdit)

        self.retranslateUi(Form)
        QtCore.QMetaObject.connectSlotsByName(Form)

    def retranslateUi(self, Form):
        Form.setWindowTitle(_translate("Form", "Form", None))
        self.arkPasswordLabel.setText(_translate("Form", "Password:", None))
        self.arkUserEdit.setPlaceholderText(_translate("Form", "dgarrod", None))
        self.arkUserLabel.setText(_translate("Form", "User ID:", None))
        self.arkPasswordEdit.setPlaceholderText(_translate("Form", "********", None))
        self.arkUrlEdit.setPlaceholderText(_translate("Form", "http://www.arch.cam.ac.uk/shuqba", None))
        self.arkUrlLabel.setText(_translate("Form", "ARK URL:", None))

