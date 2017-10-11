# -*- coding: utf-8 -*-

# Form implementation generated from reading ui file 'src/select_item_widget_base.ui'
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

class Ui_SelectItemWidget(object):
    def setupUi(self, SelectItemWidget):
        SelectItemWidget.setObjectName(_fromUtf8("SelectItemWidget"))
        SelectItemWidget.resize(240, 105)
        self.gridLayout = QtGui.QGridLayout(SelectItemWidget)
        self.gridLayout.setMargin(0)
        self.gridLayout.setObjectName(_fromUtf8("gridLayout"))
        self.siteCodeLabel = QtGui.QLabel(SelectItemWidget)
        self.siteCodeLabel.setObjectName(_fromUtf8("siteCodeLabel"))
        self.gridLayout.addWidget(self.siteCodeLabel, 0, 0, 1, 1)
        self.siteCodeCombo = QtGui.QComboBox(SelectItemWidget)
        self.siteCodeCombo.setObjectName(_fromUtf8("siteCodeCombo"))
        self.gridLayout.addWidget(self.siteCodeCombo, 0, 1, 1, 1)
        self.classCodeLabel = QtGui.QLabel(SelectItemWidget)
        self.classCodeLabel.setObjectName(_fromUtf8("classCodeLabel"))
        self.gridLayout.addWidget(self.classCodeLabel, 1, 0, 1, 1)
        self.classCodeCombo = QtGui.QComboBox(SelectItemWidget)
        self.classCodeCombo.setObjectName(_fromUtf8("classCodeCombo"))
        self.gridLayout.addWidget(self.classCodeCombo, 1, 1, 1, 1)
        self.itemIdLabel = QtGui.QLabel(SelectItemWidget)
        self.itemIdLabel.setObjectName(_fromUtf8("itemIdLabel"))
        self.gridLayout.addWidget(self.itemIdLabel, 2, 0, 1, 1)
        self.itemIdEdit = QtGui.QLineEdit(SelectItemWidget)
        self.itemIdEdit.setObjectName(_fromUtf8("itemIdEdit"))
        self.gridLayout.addWidget(self.itemIdEdit, 2, 1, 1, 1)
        self.siteCodeLabel.setBuddy(self.siteCodeCombo)
        self.classCodeLabel.setBuddy(self.classCodeCombo)
        self.itemIdLabel.setBuddy(self.itemIdEdit)

        self.retranslateUi(SelectItemWidget)
        QtCore.QMetaObject.connectSlotsByName(SelectItemWidget)
        SelectItemWidget.setTabOrder(self.itemIdEdit, self.siteCodeCombo)
        SelectItemWidget.setTabOrder(self.siteCodeCombo, self.classCodeCombo)

    def retranslateUi(self, SelectItemWidget):
        SelectItemWidget.setWindowTitle(_translate("SelectItemWidget", "Form", None))
        self.siteCodeLabel.setText(_translate("SelectItemWidget", "Site Code:", None))
        self.classCodeLabel.setText(_translate("SelectItemWidget", "Item Type:", None))
        self.itemIdLabel.setText(_translate("SelectItemWidget", "Item ID:", None))

