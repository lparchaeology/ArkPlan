# -*- coding: utf-8 -*-

# Form implementation generated from reading ui file 'ark/gui/ui/base_map_widget_base.ui'
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

class Ui_BaseMapWidget(object):
    def setupUi(self, BaseMapWidget):
        BaseMapWidget.setObjectName(_fromUtf8("BaseMapWidget"))
        BaseMapWidget.resize(364, 254)
        self.gridLayout = QtGui.QGridLayout(BaseMapWidget)
        self.gridLayout.setObjectName(_fromUtf8("gridLayout"))
        self.downloadButton = QtGui.QPushButton(BaseMapWidget)
        self.downloadButton.setObjectName(_fromUtf8("downloadButton"))
        self.gridLayout.addWidget(self.downloadButton, 3, 2, 1, 1)
        self.reloadButton = QtGui.QPushButton(BaseMapWidget)
        self.reloadButton.setObjectName(_fromUtf8("reloadButton"))
        self.gridLayout.addWidget(self.reloadButton, 4, 2, 1, 1)
        self.extentButton = QtGui.QRadioButton(BaseMapWidget)
        self.extentButton.setObjectName(_fromUtf8("extentButton"))
        self.gridLayout.addWidget(self.extentButton, 2, 0, 1, 3)
        spacerItem = QtGui.QSpacerItem(238, 31, QtGui.QSizePolicy.Expanding, QtGui.QSizePolicy.Minimum)
        self.gridLayout.addItem(spacerItem, 4, 0, 1, 2)
        spacerItem1 = QtGui.QSpacerItem(238, 31, QtGui.QSizePolicy.Expanding, QtGui.QSizePolicy.Minimum)
        self.gridLayout.addItem(spacerItem1, 3, 0, 1, 2)
        spacerItem2 = QtGui.QSpacerItem(20, 40, QtGui.QSizePolicy.Minimum, QtGui.QSizePolicy.Expanding)
        self.gridLayout.addItem(spacerItem2, 5, 0, 1, 3)
        self.titleLabel = QtGui.QLabel(BaseMapWidget)
        font = QtGui.QFont()
        font.setBold(True)
        font.setWeight(75)
        self.titleLabel.setFont(font)
        self.titleLabel.setAlignment(QtCore.Qt.AlignCenter)
        self.titleLabel.setObjectName(_fromUtf8("titleLabel"))
        self.gridLayout.addWidget(self.titleLabel, 0, 0, 1, 3)
        self.spinBox = QtGui.QSpinBox(BaseMapWidget)
        self.spinBox.setMaximum(100)
        self.spinBox.setProperty("value", 10)
        self.spinBox.setObjectName(_fromUtf8("spinBox"))
        self.gridLayout.addWidget(self.spinBox, 1, 2, 1, 1)
        self.radiusButton = QtGui.QRadioButton(BaseMapWidget)
        self.radiusButton.setObjectName(_fromUtf8("radiusButton"))
        self.gridLayout.addWidget(self.radiusButton, 1, 0, 1, 2)

        self.retranslateUi(BaseMapWidget)
        QtCore.QMetaObject.connectSlotsByName(BaseMapWidget)

    def retranslateUi(self, BaseMapWidget):
        BaseMapWidget.setWindowTitle(_translate("BaseMapWidget", "Form", None))
        self.downloadButton.setText(_translate("BaseMapWidget", "Download", None))
        self.reloadButton.setText(_translate("BaseMapWidget", "Reload", None))
        self.extentButton.setText(_translate("BaseMapWidget", "Visible Extent", None))
        self.titleLabel.setText(_translate("BaseMapWidget", "Vector Base Map", None))
        self.spinBox.setSuffix(_translate("BaseMapWidget", " km", None))
        self.radiusButton.setText(_translate("BaseMapWidget", "Site Location Radius", None))

