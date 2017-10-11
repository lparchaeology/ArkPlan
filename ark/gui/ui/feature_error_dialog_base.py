# -*- coding: utf-8 -*-

# Form implementation generated from reading ui file 'ark/gui/feature_error_dialog_base.ui'
#
# Created by: PyQt4 UI code generator 4.12
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

class Ui_FeatureErrorDialog(object):
    def setupUi(self, FeatureErrorDialog):
        FeatureErrorDialog.setObjectName(_fromUtf8("FeatureErrorDialog"))
        FeatureErrorDialog.resize(631, 385)
        self.verticalLayout = QtGui.QVBoxLayout(FeatureErrorDialog)
        self.verticalLayout.setObjectName(_fromUtf8("verticalLayout"))
        self.label = QtGui.QLabel(FeatureErrorDialog)
        self.label.setWordWrap(True)
        self.label.setObjectName(_fromUtf8("label"))
        self.verticalLayout.addWidget(self.label)
        self.errorTable = QtGui.QTableView(FeatureErrorDialog)
        self.errorTable.setObjectName(_fromUtf8("errorTable"))
        self.verticalLayout.addWidget(self.errorTable)
        self.horizontalLayout = QtGui.QHBoxLayout()
        self.horizontalLayout.setObjectName(_fromUtf8("horizontalLayout"))
        spacerItem = QtGui.QSpacerItem(40, 20, QtGui.QSizePolicy.Expanding, QtGui.QSizePolicy.Minimum)
        self.horizontalLayout.addItem(spacerItem)
        self.csvButton = QtGui.QPushButton(FeatureErrorDialog)
        self.csvButton.setObjectName(_fromUtf8("csvButton"))
        self.horizontalLayout.addWidget(self.csvButton)
        self.copyButton = QtGui.QPushButton(FeatureErrorDialog)
        self.copyButton.setObjectName(_fromUtf8("copyButton"))
        self.horizontalLayout.addWidget(self.copyButton)
        self.ignoreButton = QtGui.QPushButton(FeatureErrorDialog)
        self.ignoreButton.setEnabled(True)
        self.ignoreButton.setObjectName(_fromUtf8("ignoreButton"))
        self.horizontalLayout.addWidget(self.ignoreButton)
        self.okButton = QtGui.QPushButton(FeatureErrorDialog)
        self.okButton.setDefault(True)
        self.okButton.setObjectName(_fromUtf8("okButton"))
        self.horizontalLayout.addWidget(self.okButton)
        self.verticalLayout.addLayout(self.horizontalLayout)

        self.retranslateUi(FeatureErrorDialog)
        QtCore.QMetaObject.connectSlotsByName(FeatureErrorDialog)
        FeatureErrorDialog.setTabOrder(self.errorTable, self.okButton)
        FeatureErrorDialog.setTabOrder(self.okButton, self.ignoreButton)
        FeatureErrorDialog.setTabOrder(self.ignoreButton, self.copyButton)
        FeatureErrorDialog.setTabOrder(self.copyButton, self.csvButton)

    def retranslateUi(self, FeatureErrorDialog):
        FeatureErrorDialog.setWindowTitle(_translate("FeatureErrorDialog", "Feature Validation Errors", None))
        self.label.setText(_translate("FeatureErrorDialog", "<html><head/><body><p><span style=\" font-weight:600;\">Validation Errors:</span></p><p>The following errors were found in the requested data merge. Please correct these errors and try again.<br/></p></body></html>", None))
        self.csvButton.setText(_translate("FeatureErrorDialog", "CSV", None))
        self.copyButton.setText(_translate("FeatureErrorDialog", "Copy", None))
        self.ignoreButton.setText(_translate("FeatureErrorDialog", "Ignore", None))
        self.okButton.setText(_translate("FeatureErrorDialog", "OK", None))

