# -*- coding: utf-8 -*-

# Form implementation generated from reading ui file 'ark/lib/gui/ui/table_dialog_base.ui'
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

class Ui_TableDialog(object):
    def setupUi(self, TableDialog):
        TableDialog.setObjectName(_fromUtf8("TableDialog"))
        TableDialog.resize(631, 385)
        self.verticalLayout = QtGui.QVBoxLayout(TableDialog)
        self.verticalLayout.setObjectName(_fromUtf8("verticalLayout"))
        self.label = QtGui.QLabel(TableDialog)
        self.label.setWordWrap(True)
        self.label.setObjectName(_fromUtf8("label"))
        self.verticalLayout.addWidget(self.label)
        self.dataTable = QtGui.QTableView(TableDialog)
        self.dataTable.setObjectName(_fromUtf8("dataTable"))
        self.verticalLayout.addWidget(self.dataTable)
        self.horizontalLayout = QtGui.QHBoxLayout()
        self.horizontalLayout.setObjectName(_fromUtf8("horizontalLayout"))
        spacerItem = QtGui.QSpacerItem(40, 20, QtGui.QSizePolicy.Expanding, QtGui.QSizePolicy.Minimum)
        self.horizontalLayout.addItem(spacerItem)
        self.csvButton = QtGui.QPushButton(TableDialog)
        self.csvButton.setObjectName(_fromUtf8("csvButton"))
        self.horizontalLayout.addWidget(self.csvButton)
        self.okButton = QtGui.QPushButton(TableDialog)
        self.okButton.setDefault(True)
        self.okButton.setObjectName(_fromUtf8("okButton"))
        self.horizontalLayout.addWidget(self.okButton)
        self.verticalLayout.addLayout(self.horizontalLayout)

        self.retranslateUi(TableDialog)
        QtCore.QMetaObject.connectSlotsByName(TableDialog)
        TableDialog.setTabOrder(self.dataTable, self.okButton)
        TableDialog.setTabOrder(self.okButton, self.csvButton)

    def retranslateUi(self, TableDialog):
        TableDialog.setWindowTitle(_translate("TableDialog", "Table", None))
        self.label.setText(_translate("TableDialog", "<html><head/><body><p><span style=\" font-weight:600;\">Table:</span></p><p>Description.<br/></p></body></html>", None))
        self.csvButton.setText(_translate("TableDialog", "CSV", None))
        self.okButton.setText(_translate("TableDialog", "OK", None))

