# -*- coding: utf-8 -*-

# Form implementation generated from reading ui file 'ark/gui/ui/filter_clause_widget_base.ui'
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

class Ui_FilterClauseWidget(object):
    def setupUi(self, FilterClauseWidget):
        FilterClauseWidget.setObjectName(_fromUtf8("FilterClauseWidget"))
        FilterClauseWidget.resize(295, 34)
        self.horizontalLayout = QtGui.QHBoxLayout(FilterClauseWidget)
        self.horizontalLayout.setMargin(1)
        self.horizontalLayout.setObjectName(_fromUtf8("horizontalLayout"))
        self.filterTypeTool = QtGui.QToolButton(FilterClauseWidget)
        icon = QtGui.QIcon()
        icon.addPixmap(QtGui.QPixmap(_fromUtf8(":/plugins/ark/filter/includeFilter.png")), QtGui.QIcon.Normal, QtGui.QIcon.Off)
        self.filterTypeTool.setIcon(icon)
        self.filterTypeTool.setPopupMode(QtGui.QToolButton.InstantPopup)
        self.filterTypeTool.setObjectName(_fromUtf8("filterTypeTool"))
        self.horizontalLayout.addWidget(self.filterTypeTool)
        self.filterClassCombo = QtGui.QComboBox(FilterClauseWidget)
        self.filterClassCombo.setObjectName(_fromUtf8("filterClassCombo"))
        self.horizontalLayout.addWidget(self.filterClassCombo)
        self.filterRangeCombo = QtGui.QComboBox(FilterClauseWidget)
        sizePolicy = QtGui.QSizePolicy(QtGui.QSizePolicy.Expanding, QtGui.QSizePolicy.Fixed)
        sizePolicy.setHorizontalStretch(0)
        sizePolicy.setVerticalStretch(0)
        sizePolicy.setHeightForWidth(self.filterRangeCombo.sizePolicy().hasHeightForWidth())
        self.filterRangeCombo.setSizePolicy(sizePolicy)
        self.filterRangeCombo.setEditable(True)
        self.filterRangeCombo.setInsertPolicy(QtGui.QComboBox.InsertAtTop)
        self.filterRangeCombo.setObjectName(_fromUtf8("filterRangeCombo"))
        self.horizontalLayout.addWidget(self.filterRangeCombo)
        self.filterActionTool = QtGui.QToolButton(FilterClauseWidget)
        icon1 = QtGui.QIcon()
        icon1.addPixmap(QtGui.QPixmap(_fromUtf8(":/plugins/ark/filter/addFilter.svg")), QtGui.QIcon.Normal, QtGui.QIcon.Off)
        self.filterActionTool.setIcon(icon1)
        self.filterActionTool.setObjectName(_fromUtf8("filterActionTool"))
        self.horizontalLayout.addWidget(self.filterActionTool)

        self.retranslateUi(FilterClauseWidget)
        QtCore.QMetaObject.connectSlotsByName(FilterClauseWidget)

    def retranslateUi(self, FilterClauseWidget):
        FilterClauseWidget.setWindowTitle(_translate("FilterClauseWidget", "Form", None))
        self.filterTypeTool.setText(_translate("FilterClauseWidget", "...", None))
        self.filterActionTool.setText(_translate("FilterClauseWidget", "...", None))

