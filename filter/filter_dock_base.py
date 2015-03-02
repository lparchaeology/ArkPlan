# -*- coding: utf-8 -*-

# Form implementation generated from reading ui file 'filter/filter_dock_base.ui'
#
# Created: Mon Mar  2 16:14:50 2015
#      by: PyQt4 UI code generator 4.11.3
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

class Ui_FilterDock(object):
    def setupUi(self, filterDock):
        filterDock.setObjectName(_fromUtf8("filterDock"))
        filterDock.setGeometry(QtCore.QRect(0, 0, 321, 239))
        self.arkFilterDockContents = QtGui.QWidget()
        self.arkFilterDockContents.setObjectName(_fromUtf8("arkFilterDockContents"))
        self.verticalLayout = QtGui.QVBoxLayout(self.arkFilterDockContents)
        self.verticalLayout.setObjectName(_fromUtf8("verticalLayout"))
        self.horizontalLayout = QtGui.QHBoxLayout()
        self.horizontalLayout.setObjectName(_fromUtf8("horizontalLayout"))
        self.loadDataButton = QtGui.QPushButton(self.arkFilterDockContents)
        self.loadDataButton.setObjectName(_fromUtf8("loadDataButton"))
        self.horizontalLayout.addWidget(self.loadDataButton)
        self.zoomButton = QtGui.QPushButton(self.arkFilterDockContents)
        self.zoomButton.setObjectName(_fromUtf8("zoomButton"))
        self.horizontalLayout.addWidget(self.zoomButton)
        self.buildFilterButton = QtGui.QPushButton(self.arkFilterDockContents)
        self.buildFilterButton.setObjectName(_fromUtf8("buildFilterButton"))
        self.horizontalLayout.addWidget(self.buildFilterButton)
        self.clearFilterButton = QtGui.QPushButton(self.arkFilterDockContents)
        self.clearFilterButton.setObjectName(_fromUtf8("clearFilterButton"))
        self.horizontalLayout.addWidget(self.clearFilterButton)
        self.verticalLayout.addLayout(self.horizontalLayout)
        self.gridLayout = QtGui.QGridLayout()
        self.gridLayout.setObjectName(_fromUtf8("gridLayout"))
        self.subGroupFilterLabel = QtGui.QLabel(self.arkFilterDockContents)
        self.subGroupFilterLabel.setObjectName(_fromUtf8("subGroupFilterLabel"))
        self.gridLayout.addWidget(self.subGroupFilterLabel, 1, 0, 1, 1)
        self.groupFilterCombo = QtGui.QComboBox(self.arkFilterDockContents)
        sizePolicy = QtGui.QSizePolicy(QtGui.QSizePolicy.Expanding, QtGui.QSizePolicy.Fixed)
        sizePolicy.setHorizontalStretch(0)
        sizePolicy.setVerticalStretch(0)
        sizePolicy.setHeightForWidth(self.groupFilterCombo.sizePolicy().hasHeightForWidth())
        self.groupFilterCombo.setSizePolicy(sizePolicy)
        self.groupFilterCombo.setEditable(True)
        self.groupFilterCombo.setObjectName(_fromUtf8("groupFilterCombo"))
        self.gridLayout.addWidget(self.groupFilterCombo, 2, 1, 1, 1)
        self.groupFilterButton = QtGui.QPushButton(self.arkFilterDockContents)
        self.groupFilterButton.setObjectName(_fromUtf8("groupFilterButton"))
        self.gridLayout.addWidget(self.groupFilterButton, 2, 2, 1, 1)
        self.contextFilterCombo = QtGui.QComboBox(self.arkFilterDockContents)
        sizePolicy = QtGui.QSizePolicy(QtGui.QSizePolicy.Expanding, QtGui.QSizePolicy.Fixed)
        sizePolicy.setHorizontalStretch(0)
        sizePolicy.setVerticalStretch(0)
        sizePolicy.setHeightForWidth(self.contextFilterCombo.sizePolicy().hasHeightForWidth())
        self.contextFilterCombo.setSizePolicy(sizePolicy)
        self.contextFilterCombo.setEditable(True)
        self.contextFilterCombo.setObjectName(_fromUtf8("contextFilterCombo"))
        self.gridLayout.addWidget(self.contextFilterCombo, 0, 1, 1, 1)
        self.groupFilterLabel = QtGui.QLabel(self.arkFilterDockContents)
        self.groupFilterLabel.setObjectName(_fromUtf8("groupFilterLabel"))
        self.gridLayout.addWidget(self.groupFilterLabel, 2, 0, 1, 1)
        self.subGroupFilterCombo = QtGui.QComboBox(self.arkFilterDockContents)
        sizePolicy = QtGui.QSizePolicy(QtGui.QSizePolicy.Expanding, QtGui.QSizePolicy.Fixed)
        sizePolicy.setHorizontalStretch(0)
        sizePolicy.setVerticalStretch(0)
        sizePolicy.setHeightForWidth(self.subGroupFilterCombo.sizePolicy().hasHeightForWidth())
        self.subGroupFilterCombo.setSizePolicy(sizePolicy)
        self.subGroupFilterCombo.setEditable(True)
        self.subGroupFilterCombo.setObjectName(_fromUtf8("subGroupFilterCombo"))
        self.gridLayout.addWidget(self.subGroupFilterCombo, 1, 1, 1, 1)
        self.contextFilterLabel = QtGui.QLabel(self.arkFilterDockContents)
        self.contextFilterLabel.setObjectName(_fromUtf8("contextFilterLabel"))
        self.gridLayout.addWidget(self.contextFilterLabel, 0, 0, 1, 1)
        self.subGroupFilterButton = QtGui.QPushButton(self.arkFilterDockContents)
        self.subGroupFilterButton.setObjectName(_fromUtf8("subGroupFilterButton"))
        self.gridLayout.addWidget(self.subGroupFilterButton, 1, 2, 1, 1)
        self.contextFilterButton = QtGui.QPushButton(self.arkFilterDockContents)
        self.contextFilterButton.setObjectName(_fromUtf8("contextFilterButton"))
        self.gridLayout.addWidget(self.contextFilterButton, 0, 2, 1, 1)
        self.verticalLayout.addLayout(self.gridLayout)
        self.filterEdit = QtGui.QLineEdit(self.arkFilterDockContents)
        self.filterEdit.setReadOnly(True)
        self.filterEdit.setObjectName(_fromUtf8("filterEdit"))
        self.verticalLayout.addWidget(self.filterEdit)
        spacerItem = QtGui.QSpacerItem(20, 7, QtGui.QSizePolicy.Minimum, QtGui.QSizePolicy.Expanding)
        self.verticalLayout.addItem(spacerItem)
        filterDock.setWidget(self.arkFilterDockContents)
        self.subGroupFilterLabel.setBuddy(self.subGroupFilterCombo)
        self.groupFilterLabel.setBuddy(self.groupFilterCombo)
        self.contextFilterLabel.setBuddy(self.contextFilterCombo)

        self.retranslateUi(filterDock)
        QtCore.QMetaObject.connectSlotsByName(filterDock)

    def retranslateUi(self, filterDock):
        filterDock.setWindowTitle(_translate("FilterDock", "Filter Ark Layers", None))
        self.loadDataButton.setText(_translate("FilterDock", "Data", None))
        self.zoomButton.setText(_translate("FilterDock", "Zoom", None))
        self.buildFilterButton.setText(_translate("FilterDock", "Build", None))
        self.clearFilterButton.setText(_translate("FilterDock", "Clear", None))
        self.subGroupFilterLabel.setText(_translate("FilterDock", "Sub-Groups:", None))
        self.groupFilterButton.setText(_translate("FilterDock", "Apply", None))
        self.groupFilterLabel.setText(_translate("FilterDock", "Groups:", None))
        self.contextFilterLabel.setText(_translate("FilterDock", "Contexts:", None))
        self.subGroupFilterButton.setText(_translate("FilterDock", "Apply", None))
        self.contextFilterButton.setText(_translate("FilterDock", "Apply", None))

from ..core.dock import QgsDockWidget
