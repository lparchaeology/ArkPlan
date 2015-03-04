# -*- coding: utf-8 -*-

# Form implementation generated from reading ui file 'filter/data_dialog_base.ui'
#
# Created: Wed Mar  4 15:55:56 2015
#      by: PyQt4 UI code generator 4.11.3
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

class Ui_DataDialog(object):
    def setupUi(self, DataDialog):
        DataDialog.setObjectName(_fromUtf8("DataDialog"))
        DataDialog.resize(974, 687)
        self.verticalLayout = QtGui.QVBoxLayout(DataDialog)
        self.verticalLayout.setObjectName(_fromUtf8("verticalLayout"))
        self.label = QtGui.QLabel(DataDialog)
        self.label.setObjectName(_fromUtf8("label"))
        self.verticalLayout.addWidget(self.label)
        self.contextTableView = QtGui.QTableView(DataDialog)
        self.contextTableView.setEditTriggers(QtGui.QAbstractItemView.NoEditTriggers)
        self.contextTableView.setSortingEnabled(True)
        self.contextTableView.setCornerButtonEnabled(False)
        self.contextTableView.setObjectName(_fromUtf8("contextTableView"))
        self.verticalLayout.addWidget(self.contextTableView)
        self.label_2 = QtGui.QLabel(DataDialog)
        self.label_2.setObjectName(_fromUtf8("label_2"))
        self.verticalLayout.addWidget(self.label_2)
        self.subGroupTableView = QtGui.QTableView(DataDialog)
        self.subGroupTableView.setEditTriggers(QtGui.QAbstractItemView.NoEditTriggers)
        self.subGroupTableView.setSortingEnabled(True)
        self.subGroupTableView.setObjectName(_fromUtf8("subGroupTableView"))
        self.verticalLayout.addWidget(self.subGroupTableView)
        self.label_3 = QtGui.QLabel(DataDialog)
        self.label_3.setObjectName(_fromUtf8("label_3"))
        self.verticalLayout.addWidget(self.label_3)
        self.groupTableView = QtGui.QTableView(DataDialog)
        self.groupTableView.setEditTriggers(QtGui.QAbstractItemView.NoEditTriggers)
        self.groupTableView.setSortingEnabled(True)
        self.groupTableView.setObjectName(_fromUtf8("groupTableView"))
        self.verticalLayout.addWidget(self.groupTableView)
        self.buttonBox = QtGui.QDialogButtonBox(DataDialog)
        self.buttonBox.setOrientation(QtCore.Qt.Horizontal)
        self.buttonBox.setStandardButtons(QtGui.QDialogButtonBox.Close)
        self.buttonBox.setObjectName(_fromUtf8("buttonBox"))
        self.verticalLayout.addWidget(self.buttonBox)

        self.retranslateUi(DataDialog)
        QtCore.QObject.connect(self.buttonBox, QtCore.SIGNAL(_fromUtf8("accepted()")), DataDialog.accept)
        QtCore.QObject.connect(self.buttonBox, QtCore.SIGNAL(_fromUtf8("rejected()")), DataDialog.reject)
        QtCore.QMetaObject.connectSlotsByName(DataDialog)

    def retranslateUi(self, DataDialog):
        DataDialog.setWindowTitle(_translate("DataDialog", "Dialog", None))
        self.label.setText(_translate("DataDialog", "Context Data:", None))
        self.label_2.setText(_translate("DataDialog", "Sub-Group Data:", None))
        self.label_3.setText(_translate("DataDialog", "Group Data:", None))

