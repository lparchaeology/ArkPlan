# -*- coding: utf-8 -*-

# Form implementation generated from reading ui file 'ark_georef_dialog_base.ui'
#
# Created by: PyQt4 UI code generator 4.11.2
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

class Ui_ArkGeorefDialogBase(object):
    def setupUi(self, ArkGeorefDialogBase):
        ArkGeorefDialogBase.setObjectName(_fromUtf8("ArkGeorefDialogBase"))
        ArkGeorefDialogBase.resize(616, 503)
        self.label = QtGui.QLabel(ArkGeorefDialogBase)
        self.label.setGeometry(QtCore.QRect(300, 30, 111, 16))
        self.label.setObjectName(_fromUtf8("label"))
        self.layoutWidget = QtGui.QWidget(ArkGeorefDialogBase)
        self.layoutWidget.setGeometry(QtCore.QRect(290, 240, 258, 226))
        self.layoutWidget.setObjectName(_fromUtf8("layoutWidget"))
        self.verticalLayout_2 = QtGui.QVBoxLayout(self.layoutWidget)
        self.verticalLayout_2.setMargin(0)
        self.verticalLayout_2.setObjectName(_fromUtf8("verticalLayout_2"))
        self.horizontalLayout_2 = QtGui.QHBoxLayout()
        self.horizontalLayout_2.setObjectName(_fromUtf8("horizontalLayout_2"))
        self.m_gridPoint2 = QtGui.QLabel(self.layoutWidget)
        self.m_gridPoint2.setObjectName(_fromUtf8("m_gridPoint2"))
        self.horizontalLayout_2.addWidget(self.m_gridPoint2)
        spacerItem = QtGui.QSpacerItem(40, 20, QtGui.QSizePolicy.Expanding, QtGui.QSizePolicy.Minimum)
        self.horizontalLayout_2.addItem(spacerItem)
        self.m_autoButton2 = QtGui.QPushButton(self.layoutWidget)
        self.m_autoButton2.setObjectName(_fromUtf8("m_autoButton2"))
        self.horizontalLayout_2.addWidget(self.m_autoButton2)
        self.verticalLayout_2.addLayout(self.horizontalLayout_2)
        self.m_gridView2 = QtGui.QGraphicsView(self.layoutWidget)
        self.m_gridView2.setObjectName(_fromUtf8("m_gridView2"))
        self.verticalLayout_2.addWidget(self.m_gridView2)
        self.layoutWidget_2 = QtGui.QWidget(ArkGeorefDialogBase)
        self.layoutWidget_2.setGeometry(QtCore.QRect(20, 240, 258, 226))
        self.layoutWidget_2.setObjectName(_fromUtf8("layoutWidget_2"))
        self.verticalLayout_3 = QtGui.QVBoxLayout(self.layoutWidget_2)
        self.verticalLayout_3.setMargin(0)
        self.verticalLayout_3.setObjectName(_fromUtf8("verticalLayout_3"))
        self.horizontalLayout_3 = QtGui.QHBoxLayout()
        self.horizontalLayout_3.setObjectName(_fromUtf8("horizontalLayout_3"))
        self.m_gridPoint3 = QtGui.QLabel(self.layoutWidget_2)
        self.m_gridPoint3.setObjectName(_fromUtf8("m_gridPoint3"))
        self.horizontalLayout_3.addWidget(self.m_gridPoint3)
        spacerItem1 = QtGui.QSpacerItem(40, 20, QtGui.QSizePolicy.Expanding, QtGui.QSizePolicy.Minimum)
        self.horizontalLayout_3.addItem(spacerItem1)
        self.m_autoButton3 = QtGui.QPushButton(self.layoutWidget_2)
        self.m_autoButton3.setObjectName(_fromUtf8("m_autoButton3"))
        self.horizontalLayout_3.addWidget(self.m_autoButton3)
        self.verticalLayout_3.addLayout(self.horizontalLayout_3)
        self.m_gridView3 = QtGui.QGraphicsView(self.layoutWidget_2)
        self.m_gridView3.setObjectName(_fromUtf8("m_gridView3"))
        self.verticalLayout_3.addWidget(self.m_gridView3)
        self.pushButton = QtGui.QPushButton(ArkGeorefDialogBase)
        self.pushButton.setGeometry(QtCore.QRect(310, 100, 114, 32))
        self.pushButton.setObjectName(_fromUtf8("pushButton"))
        self.lineEdit = QtGui.QLineEdit(ArkGeorefDialogBase)
        self.lineEdit.setGeometry(QtCore.QRect(450, 30, 113, 21))
        self.lineEdit.setReadOnly(True)
        self.lineEdit.setObjectName(_fromUtf8("lineEdit"))
        self.pushButton_2 = QtGui.QPushButton(ArkGeorefDialogBase)
        self.pushButton_2.setGeometry(QtCore.QRect(450, 110, 114, 32))
        self.pushButton_2.setObjectName(_fromUtf8("pushButton_2"))
        self.layoutWidget1 = QtGui.QWidget(ArkGeorefDialogBase)
        self.layoutWidget1.setGeometry(QtCore.QRect(20, 10, 258, 226))
        self.layoutWidget1.setObjectName(_fromUtf8("layoutWidget1"))
        self.verticalLayout = QtGui.QVBoxLayout(self.layoutWidget1)
        self.verticalLayout.setMargin(0)
        self.verticalLayout.setObjectName(_fromUtf8("verticalLayout"))
        self.horizontalLayout = QtGui.QHBoxLayout()
        self.horizontalLayout.setObjectName(_fromUtf8("horizontalLayout"))
        self.m_gridPoint1 = QtGui.QLabel(self.layoutWidget1)
        self.m_gridPoint1.setObjectName(_fromUtf8("m_gridPoint1"))
        self.horizontalLayout.addWidget(self.m_gridPoint1)
        spacerItem2 = QtGui.QSpacerItem(40, 20, QtGui.QSizePolicy.Expanding, QtGui.QSizePolicy.Minimum)
        self.horizontalLayout.addItem(spacerItem2)
        self.m_autoButton1 = QtGui.QPushButton(self.layoutWidget1)
        self.m_autoButton1.setObjectName(_fromUtf8("m_autoButton1"))
        self.horizontalLayout.addWidget(self.m_autoButton1)
        self.verticalLayout.addLayout(self.horizontalLayout)
        self.m_gridView1 = QtGui.QGraphicsView(self.layoutWidget1)
        self.m_gridView1.setObjectName(_fromUtf8("m_gridView1"))
        self.verticalLayout.addWidget(self.m_gridView1)
        self.label.setBuddy(self.lineEdit)

        self.retranslateUi(ArkGeorefDialogBase)
        QtCore.QMetaObject.connectSlotsByName(ArkGeorefDialogBase)

    def retranslateUi(self, ArkGeorefDialogBase):
        ArkGeorefDialogBase.setWindowTitle(_translate("ArkGeorefDialogBase", "Dialog", None))
        self.label.setText(_translate("ArkGeorefDialogBase", "Grid Square:", None))
        self.m_gridPoint2.setText(_translate("ArkGeorefDialogBase", "000 / 000 :", None))
        self.m_autoButton2.setText(_translate("ArkGeorefDialogBase", "Auto", None))
        self.m_gridPoint3.setText(_translate("ArkGeorefDialogBase", "000 / 000 :", None))
        self.m_autoButton3.setText(_translate("ArkGeorefDialogBase", "Auto", None))
        self.pushButton.setText(_translate("ArkGeorefDialogBase", "Auto All", None))
        self.pushButton_2.setText(_translate("ArkGeorefDialogBase", "Save", None))
        self.m_gridPoint1.setText(_translate("ArkGeorefDialogBase", "000 / 000 :", None))
        self.m_autoButton1.setText(_translate("ArkGeorefDialogBase", "Auto", None))

