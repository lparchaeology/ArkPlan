# -*- coding: utf-8 -*-

# Form implementation generated from reading ui file 'src/data_widget_base.ui'
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

class Ui_DataWidget(object):
    def setupUi(self, DataWidget):
        DataWidget.setObjectName(_fromUtf8("DataWidget"))
        DataWidget.resize(269, 332)
        self.gridLayout = QtGui.QGridLayout(DataWidget)
        self.gridLayout.setObjectName(_fromUtf8("gridLayout"))
        self.itemDataView = QtWebKit.QWebView(DataWidget)
        self.itemDataView.setUrl(QtCore.QUrl(_fromUtf8("about:blank")))
        self.itemDataView.setObjectName(_fromUtf8("itemDataView"))
        self.gridLayout.addWidget(self.itemDataView, 2, 0, 1, 4)
        self.siteCodeCombo = QtGui.QComboBox(DataWidget)
        self.siteCodeCombo.setObjectName(_fromUtf8("siteCodeCombo"))
        self.gridLayout.addWidget(self.siteCodeCombo, 0, 2, 1, 2)
        self.itemLabel = QtGui.QLabel(DataWidget)
        self.itemLabel.setObjectName(_fromUtf8("itemLabel"))
        self.gridLayout.addWidget(self.itemLabel, 1, 0, 1, 2)
        self.horizontalLayout_3 = QtGui.QHBoxLayout()
        self.horizontalLayout_3.setObjectName(_fromUtf8("horizontalLayout_3"))
        self.classCodeCombo = QtGui.QComboBox(DataWidget)
        self.classCodeCombo.setObjectName(_fromUtf8("classCodeCombo"))
        self.horizontalLayout_3.addWidget(self.classCodeCombo)
        self.itemIdSpin = QtGui.QSpinBox(DataWidget)
        self.itemIdSpin.setMaximum(99999)
        self.itemIdSpin.setObjectName(_fromUtf8("itemIdSpin"))
        self.horizontalLayout_3.addWidget(self.itemIdSpin)
        self.gridLayout.addLayout(self.horizontalLayout_3, 1, 2, 1, 2)
        self.siteCodeLabel = QtGui.QLabel(DataWidget)
        self.siteCodeLabel.setObjectName(_fromUtf8("siteCodeLabel"))
        self.gridLayout.addWidget(self.siteCodeLabel, 0, 0, 1, 2)
        self.itemLabel.setBuddy(self.classCodeCombo)

        self.retranslateUi(DataWidget)
        QtCore.QMetaObject.connectSlotsByName(DataWidget)

    def retranslateUi(self, DataWidget):
        DataWidget.setWindowTitle(_translate("DataWidget", "Form", None))
        self.itemLabel.setText(_translate("DataWidget", "Item ID:", None))
        self.itemIdSpin.setToolTip(_translate("DataWidget", "Source ID", None))
        self.siteCodeLabel.setText(_translate("DataWidget", "Site Code:", None))

from PyQt4 import QtWebKit
import resources_rc
