# -*- coding: utf-8 -*-

# Form implementation generated from reading ui file 'src/error_dialog_base.ui'
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

class Ui_ErrorDialog(object):
    def setupUi(self, ErrorDialog):
        ErrorDialog.setObjectName(_fromUtf8("ErrorDialog"))
        ErrorDialog.resize(631, 385)
        self.verticalLayout = QtGui.QVBoxLayout(ErrorDialog)
        self.verticalLayout.setObjectName(_fromUtf8("verticalLayout"))
        self.label = QtGui.QLabel(ErrorDialog)
        self.label.setWordWrap(True)
        self.label.setObjectName(_fromUtf8("label"))
        self.verticalLayout.addWidget(self.label)
        self.errorTable = QtGui.QTableView(ErrorDialog)
        self.errorTable.setObjectName(_fromUtf8("errorTable"))
        self.verticalLayout.addWidget(self.errorTable)
        self.horizontalLayout = QtGui.QHBoxLayout()
        self.horizontalLayout.setObjectName(_fromUtf8("horizontalLayout"))
        spacerItem = QtGui.QSpacerItem(40, 20, QtGui.QSizePolicy.Expanding, QtGui.QSizePolicy.Minimum)
        self.horizontalLayout.addItem(spacerItem)
        self.csvButton = QtGui.QPushButton(ErrorDialog)
        self.csvButton.setObjectName(_fromUtf8("csvButton"))
        self.horizontalLayout.addWidget(self.csvButton)
        self.copyButton = QtGui.QPushButton(ErrorDialog)
        self.copyButton.setObjectName(_fromUtf8("copyButton"))
        self.horizontalLayout.addWidget(self.copyButton)
        self.ignoreButton = QtGui.QPushButton(ErrorDialog)
        self.ignoreButton.setEnabled(True)
        self.ignoreButton.setObjectName(_fromUtf8("ignoreButton"))
        self.horizontalLayout.addWidget(self.ignoreButton)
        self.okButton = QtGui.QPushButton(ErrorDialog)
        self.okButton.setDefault(True)
        self.okButton.setObjectName(_fromUtf8("okButton"))
        self.horizontalLayout.addWidget(self.okButton)
        self.verticalLayout.addLayout(self.horizontalLayout)

        self.retranslateUi(ErrorDialog)
        QtCore.QMetaObject.connectSlotsByName(ErrorDialog)
        ErrorDialog.setTabOrder(self.errorTable, self.okButton)
        ErrorDialog.setTabOrder(self.okButton, self.ignoreButton)
        ErrorDialog.setTabOrder(self.ignoreButton, self.copyButton)
        ErrorDialog.setTabOrder(self.copyButton, self.csvButton)

    def retranslateUi(self, ErrorDialog):
        ErrorDialog.setWindowTitle(_translate("ErrorDialog", "Validation Errors", None))
        self.label.setText(_translate("ErrorDialog", "<html><head/><body><p><span style=\" font-weight:600;\">Validation Errors:</span></p><p>The following errors were found in the requested data merge. Please correct these errors and try again.<br/></p></body></html>", None))
        self.csvButton.setText(_translate("ErrorDialog", "CSV", None))
        self.copyButton.setText(_translate("ErrorDialog", "Copy", None))
        self.ignoreButton.setText(_translate("ErrorDialog", "Ignore", None))
        self.okButton.setText(_translate("ErrorDialog", "OK", None))

