# -*- coding: utf-8 -*-

# Form implementation generated from reading ui file 'ark/gui/ui/item_feature_error_dialog_base.ui'
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

class Ui_ItemFeatureErrorDialog(object):
    def setupUi(self, ItemFeatureErrorDialog):
        ItemFeatureErrorDialog.setObjectName(_fromUtf8("ItemFeatureErrorDialog"))
        ItemFeatureErrorDialog.resize(631, 385)
        self.verticalLayout = QtGui.QVBoxLayout(ItemFeatureErrorDialog)
        self.verticalLayout.setObjectName(_fromUtf8("verticalLayout"))
        self.label = QtGui.QLabel(ItemFeatureErrorDialog)
        self.label.setWordWrap(True)
        self.label.setObjectName(_fromUtf8("label"))
        self.verticalLayout.addWidget(self.label)
        self.errorTable = QtGui.QTableView(ItemFeatureErrorDialog)
        self.errorTable.setObjectName(_fromUtf8("errorTable"))
        self.verticalLayout.addWidget(self.errorTable)
        self.horizontalLayout = QtGui.QHBoxLayout()
        self.horizontalLayout.setObjectName(_fromUtf8("horizontalLayout"))
        spacerItem = QtGui.QSpacerItem(40, 20, QtGui.QSizePolicy.Expanding, QtGui.QSizePolicy.Minimum)
        self.horizontalLayout.addItem(spacerItem)
        self.csvButton = QtGui.QPushButton(ItemFeatureErrorDialog)
        self.csvButton.setObjectName(_fromUtf8("csvButton"))
        self.horizontalLayout.addWidget(self.csvButton)
        self.copyButton = QtGui.QPushButton(ItemFeatureErrorDialog)
        self.copyButton.setObjectName(_fromUtf8("copyButton"))
        self.horizontalLayout.addWidget(self.copyButton)
        self.ignoreButton = QtGui.QPushButton(ItemFeatureErrorDialog)
        self.ignoreButton.setEnabled(True)
        self.ignoreButton.setObjectName(_fromUtf8("ignoreButton"))
        self.horizontalLayout.addWidget(self.ignoreButton)
        self.okButton = QtGui.QPushButton(ItemFeatureErrorDialog)
        self.okButton.setDefault(True)
        self.okButton.setObjectName(_fromUtf8("okButton"))
        self.horizontalLayout.addWidget(self.okButton)
        self.verticalLayout.addLayout(self.horizontalLayout)

        self.retranslateUi(ItemFeatureErrorDialog)
        QtCore.QMetaObject.connectSlotsByName(ItemFeatureErrorDialog)
        ItemFeatureErrorDialog.setTabOrder(self.errorTable, self.okButton)
        ItemFeatureErrorDialog.setTabOrder(self.okButton, self.ignoreButton)
        ItemFeatureErrorDialog.setTabOrder(self.ignoreButton, self.copyButton)
        ItemFeatureErrorDialog.setTabOrder(self.copyButton, self.csvButton)

    def retranslateUi(self, ItemFeatureErrorDialog):
        ItemFeatureErrorDialog.setWindowTitle(_translate("ItemFeatureErrorDialog", "Feature Validation Errors", None))
        self.label.setText(_translate("ItemFeatureErrorDialog", "<html><head/><body><p><span style=\" font-weight:600;\">Validation Errors:</span></p><p>The following errors were found in the requested data merge. Please correct these errors and try again.<br/></p></body></html>", None))
        self.csvButton.setText(_translate("ItemFeatureErrorDialog", "CSV", None))
        self.copyButton.setText(_translate("ItemFeatureErrorDialog", "Copy", None))
        self.ignoreButton.setText(_translate("ItemFeatureErrorDialog", "Ignore", None))
        self.okButton.setText(_translate("ItemFeatureErrorDialog", "OK", None))

