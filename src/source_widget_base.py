# -*- coding: utf-8 -*-

# Form implementation generated from reading ui file 'src/source_widget_base.ui'
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

class Ui_SourceWidget(object):
    def setupUi(self, SourceWidget):
        SourceWidget.setObjectName(_fromUtf8("SourceWidget"))
        SourceWidget.resize(287, 135)
        self.gridLayout = QtGui.QGridLayout(SourceWidget)
        self.gridLayout.setMargin(0)
        self.gridLayout.setObjectName(_fromUtf8("gridLayout"))
        self.siteLabel = QtGui.QLabel(SourceWidget)
        self.siteLabel.setObjectName(_fromUtf8("siteLabel"))
        self.gridLayout.addWidget(self.siteLabel, 0, 0, 1, 1)
        self.siteCodeCombo = QtGui.QComboBox(SourceWidget)
        self.siteCodeCombo.setObjectName(_fromUtf8("siteCodeCombo"))
        self.gridLayout.addWidget(self.siteCodeCombo, 0, 1, 1, 1)
        self.sourceIdLabel = QtGui.QLabel(SourceWidget)
        self.sourceIdLabel.setObjectName(_fromUtf8("sourceIdLabel"))
        self.gridLayout.addWidget(self.sourceIdLabel, 1, 0, 1, 1)
        self.horizontalLayout_2 = QtGui.QHBoxLayout()
        self.horizontalLayout_2.setObjectName(_fromUtf8("horizontalLayout_2"))
        self.sourceClassCombo = QtGui.QComboBox(SourceWidget)
        self.sourceClassCombo.setObjectName(_fromUtf8("sourceClassCombo"))
        self.horizontalLayout_2.addWidget(self.sourceClassCombo)
        self.sourceIdEdit = QtGui.QLineEdit(SourceWidget)
        self.sourceIdEdit.setObjectName(_fromUtf8("sourceIdEdit"))
        self.horizontalLayout_2.addWidget(self.sourceIdEdit)
        self.gridLayout.addLayout(self.horizontalLayout_2, 1, 1, 1, 1)
        self.sourceCodeLabel = QtGui.QLabel(SourceWidget)
        self.sourceCodeLabel.setObjectName(_fromUtf8("sourceCodeLabel"))
        self.gridLayout.addWidget(self.sourceCodeLabel, 2, 0, 1, 1)
        self.sourceCodeCombo = QtGui.QComboBox(SourceWidget)
        self.sourceCodeCombo.setObjectName(_fromUtf8("sourceCodeCombo"))
        self.gridLayout.addWidget(self.sourceCodeCombo, 2, 1, 1, 1)
        self.sourceFileLabel = QtGui.QLabel(SourceWidget)
        self.sourceFileLabel.setObjectName(_fromUtf8("sourceFileLabel"))
        self.gridLayout.addWidget(self.sourceFileLabel, 3, 0, 1, 1)
        self.sourceFileEdit = QtGui.QLineEdit(SourceWidget)
        self.sourceFileEdit.setObjectName(_fromUtf8("sourceFileEdit"))
        self.gridLayout.addWidget(self.sourceFileEdit, 3, 1, 1, 1)
        spacerItem = QtGui.QSpacerItem(20, 7, QtGui.QSizePolicy.Minimum, QtGui.QSizePolicy.Expanding)
        self.gridLayout.addItem(spacerItem, 4, 1, 1, 1)
        self.siteLabel.setBuddy(self.siteCodeCombo)
        self.sourceCodeLabel.setBuddy(self.sourceCodeCombo)
        self.sourceFileLabel.setBuddy(self.sourceFileEdit)

        self.retranslateUi(SourceWidget)
        QtCore.QMetaObject.connectSlotsByName(SourceWidget)

    def retranslateUi(self, SourceWidget):
        SourceWidget.setWindowTitle(_translate("SourceWidget", "SourceWidget", None))
        self.siteLabel.setText(_translate("SourceWidget", "Site Code:", None))
        self.sourceIdLabel.setText(_translate("SourceWidget", "Source ID:", None))
        self.sourceCodeLabel.setText(_translate("SourceWidget", "Source Type:", None))
        self.sourceFileLabel.setText(_translate("SourceWidget", "Source File:", None))

