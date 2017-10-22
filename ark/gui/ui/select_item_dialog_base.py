# -*- coding: utf-8 -*-

# Form implementation generated from reading ui file 'ark/gui/ui/select_item_dialog_base.ui'
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

class Ui_SelectItemDialog(object):
    def setupUi(self, SelectItemDialog):
        SelectItemDialog.setObjectName(_fromUtf8("SelectItemDialog"))
        SelectItemDialog.resize(255, 166)
        self.verticalLayout = QtGui.QVBoxLayout(SelectItemDialog)
        self.verticalLayout.setObjectName(_fromUtf8("verticalLayout"))
        self.label = QtGui.QLabel(SelectItemDialog)
        self.label.setObjectName(_fromUtf8("label"))
        self.verticalLayout.addWidget(self.label)
        self.itemWidget = SelectItemWidget(SelectItemDialog)
        self.itemWidget.setObjectName(_fromUtf8("itemWidget"))
        self.verticalLayout.addWidget(self.itemWidget)
        self.gridLayout = QtGui.QGridLayout()
        self.gridLayout.setObjectName(_fromUtf8("gridLayout"))
        self.loadDrawingCheck = QtGui.QCheckBox(SelectItemDialog)
        self.loadDrawingCheck.setText(_fromUtf8(""))
        self.loadDrawingCheck.setChecked(True)
        self.loadDrawingCheck.setObjectName(_fromUtf8("loadDrawingCheck"))
        self.gridLayout.addWidget(self.loadDrawingCheck, 0, 1, 1, 1)
        self.loadDrawingLabel = QtGui.QLabel(SelectItemDialog)
        self.loadDrawingLabel.setObjectName(_fromUtf8("loadDrawingLabel"))
        self.gridLayout.addWidget(self.loadDrawingLabel, 0, 0, 1, 1)
        self.zoomItemLabel = QtGui.QLabel(SelectItemDialog)
        self.zoomItemLabel.setObjectName(_fromUtf8("zoomItemLabel"))
        self.gridLayout.addWidget(self.zoomItemLabel, 1, 0, 1, 1)
        self.zoomItemCheck = QtGui.QCheckBox(SelectItemDialog)
        self.zoomItemCheck.setText(_fromUtf8(""))
        self.zoomItemCheck.setChecked(True)
        self.zoomItemCheck.setObjectName(_fromUtf8("zoomItemCheck"))
        self.gridLayout.addWidget(self.zoomItemCheck, 1, 1, 1, 1)
        self.verticalLayout.addLayout(self.gridLayout)
        spacerItem = QtGui.QSpacerItem(20, 4, QtGui.QSizePolicy.Minimum, QtGui.QSizePolicy.Expanding)
        self.verticalLayout.addItem(spacerItem)
        self.buttonBox = QtGui.QDialogButtonBox(SelectItemDialog)
        self.buttonBox.setOrientation(QtCore.Qt.Horizontal)
        self.buttonBox.setStandardButtons(QtGui.QDialogButtonBox.Cancel|QtGui.QDialogButtonBox.Ok)
        self.buttonBox.setObjectName(_fromUtf8("buttonBox"))
        self.verticalLayout.addWidget(self.buttonBox)

        self.retranslateUi(SelectItemDialog)
        QtCore.QObject.connect(self.buttonBox, QtCore.SIGNAL(_fromUtf8("accepted()")), SelectItemDialog.accept)
        QtCore.QObject.connect(self.buttonBox, QtCore.SIGNAL(_fromUtf8("rejected()")), SelectItemDialog.reject)
        QtCore.QMetaObject.connectSlotsByName(SelectItemDialog)
        SelectItemDialog.setTabOrder(self.loadDrawingCheck, self.zoomItemCheck)
        SelectItemDialog.setTabOrder(self.zoomItemCheck, self.buttonBox)

    def retranslateUi(self, SelectItemDialog):
        SelectItemDialog.setWindowTitle(_translate("SelectItemDialog", "Dialog", None))
        self.label.setText(_translate("SelectItemDialog", "Select the item to show:", None))
        self.loadDrawingLabel.setText(_translate("SelectItemDialog", "Load Drawings:", None))
        self.zoomItemLabel.setText(_translate("SelectItemDialog", "Zoom to Item:", None))

from ..select_item_widget import SelectItemWidget
