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
        FilterExportDialog.resize(432, 222)
        self.gridLayout = QtGui.QGridLayout(FilterExportDialog)
        self.gridLayout.setObjectName(_fromUtf8("gridLayout"))
        self.exportNameLabel = QtGui.QLabel(FilterExportDialog)
        self.exportNameLabel.setObjectName(_fromUtf8("exportNameLabel"))
        self.gridLayout.addWidget(self.exportNameLabel, 2, 0, 1, 1)
        self.exportDataButton = QtGui.QRadioButton(FilterExportDialog)
        self.exportDataButton.setObjectName(_fromUtf8("exportDataButton"))
        self.gridLayout.addWidget(self.exportDataButton, 4, 1, 1, 1)
        self.exportSchematicButton = QtGui.QRadioButton(FilterExportDialog)
        self.exportSchematicButton.setChecked(True)
        self.exportSchematicButton.setObjectName(_fromUtf8("exportSchematicButton"))
        self.gridLayout.addWidget(self.exportSchematicButton, 3, 1, 1, 1)
        self.buttonBox = QtGui.QDialogButtonBox(FilterExportDialog)
        self.buttonBox.setOrientation(QtCore.Qt.Horizontal)
        self.buttonBox.setStandardButtons(QtGui.QDialogButtonBox.Cancel|QtGui.QDialogButtonBox.Ok)
        self.buttonBox.setObjectName(_fromUtf8("buttonBox"))
        self.gridLayout.addWidget(self.buttonBox, 5, 0, 1, 2)
        self.filterSetNameEdit = QtGui.QLineEdit(FilterExportDialog)
        self.filterSetNameEdit.setReadOnly(True)
        self.filterSetNameEdit.setObjectName(_fromUtf8("filterSetNameEdit"))
        self.gridLayout.addWidget(self.filterSetNameEdit, 1, 1, 1, 1)
        self.exportNameEdit = QtGui.QLineEdit(FilterExportDialog)
        self.exportNameEdit.setObjectName(_fromUtf8("exportNameEdit"))
        self.gridLayout.addWidget(self.exportNameEdit, 2, 1, 1, 1)
        self.filterSetNameLabel = QtGui.QLabel(FilterExportDialog)
        self.filterSetNameLabel.setObjectName(_fromUtf8("filterSetNameLabel"))
        self.gridLayout.addWidget(self.filterSetNameLabel, 1, 0, 1, 1)
        self.infoLabel = QtGui.QLabel(FilterExportDialog)
        self.infoLabel.setTextFormat(QtCore.Qt.LogText)
        self.infoLabel.setWordWrap(True)
        self.infoLabel.setObjectName(_fromUtf8("infoLabel"))
        self.gridLayout.addWidget(self.infoLabel, 0, 0, 1, 2)

        self.retranslateUi(FilterExportDialog)
        QtCore.QObject.connect(self.buttonBox, QtCore.SIGNAL(_fromUtf8("accepted()")), FilterExportDialog.accept)
        QtCore.QObject.connect(self.buttonBox, QtCore.SIGNAL(_fromUtf8("rejected()")), FilterExportDialog.reject)
        QtCore.QMetaObject.connectSlotsByName(FilterExportDialog)

    def retranslateUi(self, FilterExportDialog):
        FilterExportDialog.setWindowTitle(_translate("FilterExportDialog", "Filter Set Export", None))
        self.exportNameLabel.setText(_translate("FilterExportDialog", "Export Name:", None))
        self.exportDataButton.setText(_translate("FilterExportDialog", "Export selected Plan Data to scratch layers", None))
        self.exportSchematicButton.setText(_translate("FilterExportDialog", "Export selected Schematic to scratch layer", None))
        self.filterSetNameLabel.setText(_translate("FilterExportDialog", "Filter Set:", None))
        self.infoLabel.setText(_translate("FilterExportDialog", "Export the results of the selected filter set. Note the resulting layer(s) will not be updated as the source Plan Data is updated. Choosing the name of an existing export will overwrite the existing layer(s).", None))

