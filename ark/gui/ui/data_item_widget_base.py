# -*- coding: utf-8 -*-

# Form implementation generated from reading ui file 'ark/gui/ui/data_item_widget_base.ui'
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

class Ui_DataItemWidget(object):
    def setupUi(self, DataItemWidget):
        DataItemWidget.setObjectName(_fromUtf8("DataItemWidget"))
        DataItemWidget.resize(297, 111)
        self.gridLayout = QtGui.QGridLayout(DataItemWidget)
        self.gridLayout.setMargin(0)
        self.gridLayout.setObjectName(_fromUtf8("gridLayout"))
        self.siteCodeCombo = QtGui.QComboBox(DataItemWidget)
        self.siteCodeCombo.setObjectName(_fromUtf8("siteCodeCombo"))
        self.gridLayout.addWidget(self.siteCodeCombo, 0, 2, 1, 2)
        self.horizontalLayout_3 = QtGui.QHBoxLayout()
        self.horizontalLayout_3.setObjectName(_fromUtf8("horizontalLayout_3"))
        self.classCodeCombo = QtGui.QComboBox(DataItemWidget)
        self.classCodeCombo.setObjectName(_fromUtf8("classCodeCombo"))
        self.horizontalLayout_3.addWidget(self.classCodeCombo)
        self.itemIdSpin = QtGui.QSpinBox(DataItemWidget)
        self.itemIdSpin.setMaximum(99999)
        self.itemIdSpin.setObjectName(_fromUtf8("itemIdSpin"))
        self.horizontalLayout_3.addWidget(self.itemIdSpin)
        self.gridLayout.addLayout(self.horizontalLayout_3, 1, 2, 1, 2)
        self.siteCodeLabel = QtGui.QLabel(DataItemWidget)
        self.siteCodeLabel.setObjectName(_fromUtf8("siteCodeLabel"))
        self.gridLayout.addWidget(self.siteCodeLabel, 0, 0, 1, 2)
        self.itemLabel = QtGui.QLabel(DataItemWidget)
        self.itemLabel.setObjectName(_fromUtf8("itemLabel"))
        self.gridLayout.addWidget(self.itemLabel, 1, 0, 1, 2)
        spacerItem = QtGui.QSpacerItem(20, 40, QtGui.QSizePolicy.Minimum, QtGui.QSizePolicy.Expanding)
        self.gridLayout.addItem(spacerItem, 2, 0, 1, 4)
        self.itemLabel.setBuddy(self.classCodeCombo)

        self.retranslateUi(DataItemWidget)
        QtCore.QMetaObject.connectSlotsByName(DataItemWidget)

    def retranslateUi(self, DataItemWidget):
        DataItemWidget.setWindowTitle(_translate("DataItemWidget", "Form", None))
        self.itemIdSpin.setToolTip(_translate("DataItemWidget", "Source ID", None))
        self.siteCodeLabel.setText(_translate("DataItemWidget", "Site Code:", None))
        self.itemLabel.setText(_translate("DataItemWidget", "I&tem ID:", None))

