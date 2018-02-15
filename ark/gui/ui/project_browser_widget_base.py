# -*- coding: utf-8 -*-

# Form implementation generated from reading ui file 'ark/gui/ui/project_browser_widget_base.ui'
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
        Form.resize(399, 339)
        self.gridLayout = QtGui.QGridLayout(Form)
        self.gridLayout.setObjectName(_fromUtf8("gridLayout"))
        self.projectLabel = QtGui.QLabel(Form)
        self.projectLabel.setObjectName(_fromUtf8("projectLabel"))
        self.gridLayout.addWidget(self.projectLabel, 0, 0, 1, 1)
        self.projectEdit = QtGui.QLineEdit(Form)
        self.projectEdit.setReadOnly(True)
        self.projectEdit.setObjectName(_fromUtf8("projectEdit"))
        self.gridLayout.addWidget(self.projectEdit, 0, 1, 1, 1)
        self.projectNameLabel = QtGui.QLabel(Form)
        self.projectNameLabel.setObjectName(_fromUtf8("projectNameLabel"))
        self.gridLayout.addWidget(self.projectNameLabel, 1, 0, 1, 1)
        self.projectNameEdit = QtGui.QLineEdit(Form)
        self.projectNameEdit.setReadOnly(True)
        self.projectNameEdit.setObjectName(_fromUtf8("projectNameEdit"))
        self.gridLayout.addWidget(self.projectNameEdit, 1, 1, 1, 1)
        self.projectTreeView = ProjectTreeView(Form)
        self.projectTreeView.setObjectName(_fromUtf8("projectTreeView"))
        self.gridLayout.addWidget(self.projectTreeView, 2, 0, 1, 2)

        self.retranslateUi(Form)
        QtCore.QMetaObject.connectSlotsByName(Form)

    def retranslateUi(self, Form):
        Form.setWindowTitle(_translate("Form", "Form", None))
        self.projectLabel.setText(_translate("Form", "Project:", None))
        self.projectNameLabel.setText(_translate("Form", "Name:", None))

from ..project_tree_view import ProjectTreeView
