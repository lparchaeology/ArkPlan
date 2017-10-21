# -*- coding: utf-8 -*-

# Form implementation generated from reading ui file 'ark/gui/ui/trench_widget_base.ui'
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

class Ui_TrenchWidget(object):
    def setupUi(self, TrenchWidget):
        TrenchWidget.setObjectName(_fromUtf8("TrenchWidget"))
        TrenchWidget.resize(383, 283)
        self.gridLayout = QtGui.QGridLayout(TrenchWidget)
        self.gridLayout.setObjectName(_fromUtf8("gridLayout"))
        self.copyMapPointTool_2 = QtGui.QToolButton(TrenchWidget)
        icon = QtGui.QIcon()
        icon.addPixmap(QtGui.QPixmap(_fromUtf8("resources/mActionCustomProjection.png")), QtGui.QIcon.Normal, QtGui.QIcon.Off)
        self.copyMapPointTool_2.setIcon(icon)
        self.copyMapPointTool_2.setObjectName(_fromUtf8("copyMapPointTool_2"))
        self.gridLayout.addWidget(self.copyMapPointTool_2, 8, 4, 1, 1)
        self.doubleSpinBox = QtGui.QDoubleSpinBox(TrenchWidget)
        self.doubleSpinBox.setProperty("value", 5.0)
        self.doubleSpinBox.setObjectName(_fromUtf8("doubleSpinBox"))
        self.gridLayout.addWidget(self.doubleSpinBox, 3, 3, 1, 2)
        self.line = QtGui.QFrame(TrenchWidget)
        self.line.setFrameShape(QtGui.QFrame.HLine)
        self.line.setFrameShadow(QtGui.QFrame.Sunken)
        self.line.setObjectName(_fromUtf8("line"))
        self.gridLayout.addWidget(self.line, 5, 2, 3, 5)
        self.label = QtGui.QLabel(TrenchWidget)
        self.label.setObjectName(_fromUtf8("label"))
        self.gridLayout.addWidget(self.label, 2, 2, 1, 1)
        self.label_4 = QtGui.QLabel(TrenchWidget)
        self.label_4.setAlignment(QtCore.Qt.AlignRight|QtCore.Qt.AlignTrailing|QtCore.Qt.AlignVCenter)
        self.label_4.setObjectName(_fromUtf8("label_4"))
        self.gridLayout.addWidget(self.label_4, 2, 6, 1, 1)
        self.label_5 = QtGui.QLabel(TrenchWidget)
        self.label_5.setObjectName(_fromUtf8("label_5"))
        self.gridLayout.addWidget(self.label_5, 4, 3, 1, 3)
        self.doubleSpinBox_3 = QtGui.QDoubleSpinBox(TrenchWidget)
        self.doubleSpinBox_3.setProperty("value", 20.0)
        self.doubleSpinBox_3.setObjectName(_fromUtf8("doubleSpinBox_3"))
        self.gridLayout.addWidget(self.doubleSpinBox_3, 3, 6, 1, 1)
        spacerItem = QtGui.QSpacerItem(7, 23, QtGui.QSizePolicy.Expanding, QtGui.QSizePolicy.Minimum)
        self.gridLayout.addItem(spacerItem, 10, 4, 1, 3)
        self.label_6 = QtGui.QLabel(TrenchWidget)
        self.label_6.setObjectName(_fromUtf8("label_6"))
        self.gridLayout.addWidget(self.label_6, 8, 2, 1, 1)
        self.copyMapPointTool_3 = QtGui.QToolButton(TrenchWidget)
        icon1 = QtGui.QIcon()
        icon1.addPixmap(QtGui.QPixmap(_fromUtf8("resources/document-save.png")), QtGui.QIcon.Normal, QtGui.QIcon.Off)
        self.copyMapPointTool_3.setIcon(icon1)
        self.copyMapPointTool_3.setObjectName(_fromUtf8("copyMapPointTool_3"))
        self.gridLayout.addWidget(self.copyMapPointTool_3, 10, 3, 1, 1)
        self.label_2 = QtGui.QLabel(TrenchWidget)
        self.label_2.setObjectName(_fromUtf8("label_2"))
        self.gridLayout.addWidget(self.label_2, 3, 2, 1, 1)
        spacerItem1 = QtGui.QSpacerItem(137, 20, QtGui.QSizePolicy.Expanding, QtGui.QSizePolicy.Minimum)
        self.gridLayout.addItem(spacerItem1, 8, 5, 1, 2)
        self.copyMapPointTool = QtGui.QToolButton(TrenchWidget)
        icon2 = QtGui.QIcon()
        icon2.addPixmap(QtGui.QPixmap(_fromUtf8("resources/document-edit.png")), QtGui.QIcon.Normal, QtGui.QIcon.Off)
        self.copyMapPointTool.setIcon(icon2)
        self.copyMapPointTool.setObjectName(_fromUtf8("copyMapPointTool"))
        self.gridLayout.addWidget(self.copyMapPointTool, 8, 3, 1, 1)
        self.label_3 = QtGui.QLabel(TrenchWidget)
        self.label_3.setObjectName(_fromUtf8("label_3"))
        self.gridLayout.addWidget(self.label_3, 4, 2, 1, 1)
        self.label_9 = QtGui.QLabel(TrenchWidget)
        self.label_9.setAlignment(QtCore.Qt.AlignCenter)
        self.label_9.setObjectName(_fromUtf8("label_9"))
        self.gridLayout.addWidget(self.label_9, 1, 2, 1, 5)
        self.label_7 = QtGui.QLabel(TrenchWidget)
        self.label_7.setObjectName(_fromUtf8("label_7"))
        self.gridLayout.addWidget(self.label_7, 10, 2, 1, 1)
        self.comboBox = QtGui.QComboBox(TrenchWidget)
        self.comboBox.setObjectName(_fromUtf8("comboBox"))
        self.comboBox.addItem(_fromUtf8(""))
        self.gridLayout.addWidget(self.comboBox, 2, 3, 1, 3)
        self.doubleSpinBox_2 = QtGui.QDoubleSpinBox(TrenchWidget)
        self.doubleSpinBox_2.setProperty("value", 2.0)
        self.doubleSpinBox_2.setObjectName(_fromUtf8("doubleSpinBox_2"))
        self.gridLayout.addWidget(self.doubleSpinBox_2, 3, 5, 1, 1)
        spacerItem2 = QtGui.QSpacerItem(20, 40, QtGui.QSizePolicy.Minimum, QtGui.QSizePolicy.Expanding)
        self.gridLayout.addItem(spacerItem2, 11, 2, 1, 5)

        self.retranslateUi(TrenchWidget)
        QtCore.QMetaObject.connectSlotsByName(TrenchWidget)

    def retranslateUi(self, TrenchWidget):
        TrenchWidget.setWindowTitle(_translate("TrenchWidget", "Form", None))
        self.copyMapPointTool_2.setText(_translate("TrenchWidget", "...", None))
        self.doubleSpinBox.setSuffix(_translate("TrenchWidget", "%", None))
        self.label.setText(_translate("TrenchWidget", "Area:", None))
        self.label_4.setText(_translate("TrenchWidget", "255 m2", None))
        self.label_5.setText(_translate("TrenchWidget", "180 m2, 60m, 3 trenches", None))
        self.doubleSpinBox_3.setSuffix(_translate("TrenchWidget", "m", None))
        self.label_6.setText(_translate("TrenchWidget", "Draw:", None))
        self.copyMapPointTool_3.setText(_translate("TrenchWidget", "...", None))
        self.label_2.setText(_translate("TrenchWidget", "Trench:", None))
        self.copyMapPointTool.setText(_translate("TrenchWidget", "...", None))
        self.label_3.setText(_translate("TrenchWidget", "Result:", None))
        self.label_9.setText(_translate("TrenchWidget", "Trench Panel", None))
        self.label_7.setText(_translate("TrenchWidget", "Export:", None))
        self.comboBox.setItemText(0, _translate("TrenchWidget", "Site Redline", None))
        self.doubleSpinBox_2.setSuffix(_translate("TrenchWidget", "m", None))

import resources
