# -*- coding: utf-8 -*-

# Form implementation generated from reading ui file 'src/filter_set_widget_base.ui'
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

class Ui_FilterSetWidget(object):
    def setupUi(self, FilterSetWidget):
        FilterSetWidget.setObjectName(_fromUtf8("FilterSetWidget"))
        FilterSetWidget.resize(212, 248)
        self.verticalLayout = QtGui.QVBoxLayout(FilterSetWidget)
        self.verticalLayout.setMargin(0)
        self.verticalLayout.setObjectName(_fromUtf8("verticalLayout"))
        self.gridLayout = QtGui.QGridLayout()
        self.gridLayout.setObjectName(_fromUtf8("gridLayout"))
        self.siteCodeLabel = QtGui.QLabel(FilterSetWidget)
        self.siteCodeLabel.setObjectName(_fromUtf8("siteCodeLabel"))
        self.gridLayout.addWidget(self.siteCodeLabel, 1, 0, 1, 1)
        self.siteCodeCombo = QtGui.QComboBox(FilterSetWidget)
        self.siteCodeCombo.setObjectName(_fromUtf8("siteCodeCombo"))
        self.gridLayout.addWidget(self.siteCodeCombo, 1, 1, 1, 2)
        self.filterSetLabel = QtGui.QLabel(FilterSetWidget)
        self.filterSetLabel.setObjectName(_fromUtf8("filterSetLabel"))
        self.gridLayout.addWidget(self.filterSetLabel, 0, 0, 1, 1)
        self.filterSetCombo = QtGui.QComboBox(FilterSetWidget)
        self.filterSetCombo.setObjectName(_fromUtf8("filterSetCombo"))
        self.gridLayout.addWidget(self.filterSetCombo, 0, 1, 1, 2)
        self.filterSetTool = QtGui.QToolButton(FilterSetWidget)
        icon = QtGui.QIcon()
        icon.addPixmap(QtGui.QPixmap(_fromUtf8(":/plugins/ark/filter/saveFilterSet.png")), QtGui.QIcon.Normal, QtGui.QIcon.Off)
        self.filterSetTool.setIcon(icon)
        self.filterSetTool.setPopupMode(QtGui.QToolButton.MenuButtonPopup)
        self.filterSetTool.setObjectName(_fromUtf8("filterSetTool"))
        self.gridLayout.addWidget(self.filterSetTool, 0, 3, 1, 1)
        self.verticalLayout.addLayout(self.gridLayout)
        self.newFilterFrame = QtGui.QFrame(FilterSetWidget)
        self.newFilterFrame.setObjectName(_fromUtf8("newFilterFrame"))
        self.horizontalLayout_2 = QtGui.QHBoxLayout(self.newFilterFrame)
        self.horizontalLayout_2.setMargin(0)
        self.horizontalLayout_2.setObjectName(_fromUtf8("horizontalLayout_2"))
        self.verticalLayout.addWidget(self.newFilterFrame)
        self.filterClauseList = QtGui.QListWidget(FilterSetWidget)
        self.filterClauseList.setProperty("showDropIndicator", False)
        self.filterClauseList.setSelectionMode(QtGui.QAbstractItemView.NoSelection)
        self.filterClauseList.setObjectName(_fromUtf8("filterClauseList"))
        self.verticalLayout.addWidget(self.filterClauseList)
        self.schematicClauseList = QtGui.QListWidget(FilterSetWidget)
        self.schematicClauseList.setProperty("showDropIndicator", False)
        self.schematicClauseList.setSelectionMode(QtGui.QAbstractItemView.NoSelection)
        self.schematicClauseList.setObjectName(_fromUtf8("schematicClauseList"))
        self.verticalLayout.addWidget(self.schematicClauseList)
        self.saveFilterSetAction = QtGui.QAction(FilterSetWidget)
        self.saveFilterSetAction.setIcon(icon)
        self.saveFilterSetAction.setObjectName(_fromUtf8("saveFilterSetAction"))
        self.deleteFilterSetAction = QtGui.QAction(FilterSetWidget)
        icon1 = QtGui.QIcon()
        icon1.addPixmap(QtGui.QPixmap(_fromUtf8(":/plugins/ark/filter/deleteFilterSet.svg")), QtGui.QIcon.Normal, QtGui.QIcon.Off)
        self.deleteFilterSetAction.setIcon(icon1)
        self.deleteFilterSetAction.setObjectName(_fromUtf8("deleteFilterSetAction"))
        self.exportFilterSetAction = QtGui.QAction(FilterSetWidget)
        icon2 = QtGui.QIcon()
        icon2.addPixmap(QtGui.QPixmap(_fromUtf8(":/plugins/ark/filter/exportFilterSet.png")), QtGui.QIcon.Normal, QtGui.QIcon.Off)
        self.exportFilterSetAction.setIcon(icon2)
        self.exportFilterSetAction.setObjectName(_fromUtf8("exportFilterSetAction"))
        self.reloadFilterSetAction = QtGui.QAction(FilterSetWidget)
        icon3 = QtGui.QIcon()
        icon3.addPixmap(QtGui.QPixmap(_fromUtf8(":/plugins/ark/data/refreshData.svg")), QtGui.QIcon.Normal, QtGui.QIcon.Off)
        self.reloadFilterSetAction.setIcon(icon3)
        self.reloadFilterSetAction.setObjectName(_fromUtf8("reloadFilterSetAction"))

        self.retranslateUi(FilterSetWidget)
        QtCore.QMetaObject.connectSlotsByName(FilterSetWidget)

    def retranslateUi(self, FilterSetWidget):
        FilterSetWidget.setWindowTitle(_translate("FilterSetWidget", "Form", None))
        self.siteCodeLabel.setText(_translate("FilterSetWidget", "Site:", None))
        self.filterSetLabel.setText(_translate("FilterSetWidget", "Filter Set:", None))
        self.filterSetTool.setText(_translate("FilterSetWidget", "Save", None))
        self.saveFilterSetAction.setText(_translate("FilterSetWidget", "Save Filter Set", None))
        self.deleteFilterSetAction.setText(_translate("FilterSetWidget", "Delete Filter Set", None))
        self.exportFilterSetAction.setText(_translate("FilterSetWidget", "Export Filter Set", None))
        self.reloadFilterSetAction.setText(_translate("FilterSetWidget", "Reload Filter Set", None))

import resources_rc
