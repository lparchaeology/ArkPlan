# -*- coding: utf-8 -*-

# Form implementation generated from reading ui file 'filter/filter_export_dialog_base.ui'
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

class Ui_FilterExportDialog(object):
    def setupUi(self, FilterExportDialog):
        FilterExportDialog.setObjectName(_fromUtf8("FilterExportDialog"))
        FilterExportDialog.resize(340, 151)
        self.gridLayout = QtGui.QGridLayout(FilterExportDialog)
        self.gridLayout.setObjectName(_fromUtf8("gridLayout"))
        self.filterSetNameLabel = QtGui.QLabel(FilterExportDialog)
        self.filterSetNameLabel.setObjectName(_fromUtf8("filterSetNameLabel"))
        self.gridLayout.addWidget(self.filterSetNameLabel, 0, 0, 1, 1)
        self.filterSetNameEdit = QtGui.QLineEdit(FilterExportDialog)
        self.filterSetNameEdit.setObjectName(_fromUtf8("filterSetNameEdit"))
        self.gridLayout.addWidget(self.filterSetNameEdit, 0, 1, 1, 1)
        self.buttonBox = QtGui.QDialogButtonBox(FilterExportDialog)
        self.buttonBox.setOrientation(QtCore.Qt.Horizontal)
        self.buttonBox.setStandardButtons(QtGui.QDialogButtonBox.Cancel|QtGui.QDialogButtonBox.Ok)
        self.buttonBox.setObjectName(_fromUtf8("buttonBox"))
        self.gridLayout.addWidget(self.buttonBox, 4, 0, 1, 2)
        self.saveButton = QtGui.QRadioButton(FilterExportDialog)
        self.saveButton.setChecked(True)
        self.saveButton.setObjectName(_fromUtf8("saveButton"))
        self.gridLayout.addWidget(self.saveButton, 1, 1, 1, 1)
        self.copySchematicButton = QtGui.QRadioButton(FilterExportDialog)
        self.copySchematicButton.setObjectName(_fromUtf8("copySchematicButton"))
        self.gridLayout.addWidget(self.copySchematicButton, 2, 1, 1, 1)
        self.copyDataButton = QtGui.QRadioButton(FilterExportDialog)
        self.copyDataButton.setObjectName(_fromUtf8("copyDataButton"))
        self.gridLayout.addWidget(self.copyDataButton, 3, 1, 1, 1)

        self.retranslateUi(FilterExportDialog)
        QtCore.QObject.connect(self.buttonBox, QtCore.SIGNAL(_fromUtf8("accepted()")), FilterExportDialog.accept)
        QtCore.QObject.connect(self.buttonBox, QtCore.SIGNAL(_fromUtf8("rejected()")), FilterExportDialog.reject)
        QtCore.QMetaObject.connectSlotsByName(FilterExportDialog)

    def retranslateUi(self, FilterExportDialog):
        FilterExportDialog.setWindowTitle(_translate("FilterExportDialog", "Filter Set Save/Export", None))
        self.filterSetNameLabel.setText(_translate("FilterExportDialog", "Name:", None))
        self.saveButton.setText(_translate("FilterExportDialog", "Save as Filter Set on Plan Data", None))
        self.copySchematicButton.setText(_translate("FilterExportDialog", "Copy selected Schematic to scratch layer", None))
        self.copyDataButton.setText(_translate("FilterExportDialog", "Copy selected Plan Data to scratch layers", None))

