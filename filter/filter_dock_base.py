# -*- coding: utf-8 -*-

# Form implementation generated from reading ui file 'filter/filter_dock_base.ui'
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

class Ui_FilterDock(object):
    def setupUi(self, FilterDock):
        FilterDock.setObjectName(_fromUtf8("FilterDock"))
        FilterDock.resize(306, 306)
        self.FilterDockContents = QtGui.QWidget()
        self.FilterDockContents.setObjectName(_fromUtf8("FilterDockContents"))
        self.verticalLayout = QtGui.QVBoxLayout(self.FilterDockContents)
        self.verticalLayout.setObjectName(_fromUtf8("verticalLayout"))
        self.horizontalLayout = QtGui.QHBoxLayout()
        self.horizontalLayout.setObjectName(_fromUtf8("horizontalLayout"))
        self.zoomFilterTool = QtGui.QToolButton(self.FilterDockContents)
        icon = QtGui.QIcon()
        icon.addPixmap(QtGui.QPixmap(_fromUtf8(":/ArkFilter/mActionZoomToSelected.svg")), QtGui.QIcon.Normal, QtGui.QIcon.Off)
        self.zoomFilterTool.setIcon(icon)
        self.zoomFilterTool.setObjectName(_fromUtf8("zoomFilterTool"))
        self.horizontalLayout.addWidget(self.zoomFilterTool)
        self.buildFilterTool = QtGui.QToolButton(self.FilterDockContents)
        icon1 = QtGui.QIcon()
        icon1.addPixmap(QtGui.QPixmap(_fromUtf8(":/ArkFilter/mIconExpressionEditorOpen.svg")), QtGui.QIcon.Normal, QtGui.QIcon.Off)
        self.buildFilterTool.setIcon(icon1)
        self.buildFilterTool.setObjectName(_fromUtf8("buildFilterTool"))
        self.horizontalLayout.addWidget(self.buildFilterTool)
        self.clearFilterTool = QtGui.QToolButton(self.FilterDockContents)
        icon2 = QtGui.QIcon()
        icon2.addPixmap(QtGui.QPixmap(_fromUtf8(":/ArkFilter/delete.svg")), QtGui.QIcon.Normal, QtGui.QIcon.Off)
        self.clearFilterTool.setIcon(icon2)
        self.clearFilterTool.setObjectName(_fromUtf8("clearFilterTool"))
        self.horizontalLayout.addWidget(self.clearFilterTool)
        self.loadDataTool = QtGui.QToolButton(self.FilterDockContents)
        self.loadDataTool.setEnabled(False)
        icon3 = QtGui.QIcon()
        icon3.addPixmap(QtGui.QPixmap(_fromUtf8(":/ArkFilter/mIconDbSchema.png")), QtGui.QIcon.Normal, QtGui.QIcon.Off)
        self.loadDataTool.setIcon(icon3)
        self.loadDataTool.setObjectName(_fromUtf8("loadDataTool"))
        self.horizontalLayout.addWidget(self.loadDataTool)
        self.showDataTool = QtGui.QToolButton(self.FilterDockContents)
        self.showDataTool.setEnabled(False)
        icon4 = QtGui.QIcon()
        icon4.addPixmap(QtGui.QPixmap(_fromUtf8(":/ArkFilter/mActionOpenTable.png")), QtGui.QIcon.Normal, QtGui.QIcon.Off)
        self.showDataTool.setIcon(icon4)
        self.showDataTool.setObjectName(_fromUtf8("showDataTool"))
        self.horizontalLayout.addWidget(self.showDataTool)
        spacerItem = QtGui.QSpacerItem(40, 20, QtGui.QSizePolicy.Expanding, QtGui.QSizePolicy.Minimum)
        self.horizontalLayout.addItem(spacerItem)
        self.verticalLayout.addLayout(self.horizontalLayout)
        self.gridLayout = QtGui.QGridLayout()
        self.gridLayout.setObjectName(_fromUtf8("gridLayout"))
        self.subGroupFilterLabel = QtGui.QLabel(self.FilterDockContents)
        self.subGroupFilterLabel.setEnabled(False)
        self.subGroupFilterLabel.setObjectName(_fromUtf8("subGroupFilterLabel"))
        self.gridLayout.addWidget(self.subGroupFilterLabel, 1, 0, 1, 1)
        self.groupFilterCombo = QtGui.QComboBox(self.FilterDockContents)
        self.groupFilterCombo.setEnabled(False)
        sizePolicy = QtGui.QSizePolicy(QtGui.QSizePolicy.Expanding, QtGui.QSizePolicy.Fixed)
        sizePolicy.setHorizontalStretch(0)
        sizePolicy.setVerticalStretch(0)
        sizePolicy.setHeightForWidth(self.groupFilterCombo.sizePolicy().hasHeightForWidth())
        self.groupFilterCombo.setSizePolicy(sizePolicy)
        self.groupFilterCombo.setEditable(True)
        self.groupFilterCombo.setObjectName(_fromUtf8("groupFilterCombo"))
        self.gridLayout.addWidget(self.groupFilterCombo, 2, 1, 1, 1)
        self.groupFilterButton = QtGui.QPushButton(self.FilterDockContents)
        self.groupFilterButton.setEnabled(False)
        self.groupFilterButton.setObjectName(_fromUtf8("groupFilterButton"))
        self.gridLayout.addWidget(self.groupFilterButton, 2, 2, 1, 1)
        self.contextFilterCombo = QtGui.QComboBox(self.FilterDockContents)
        sizePolicy = QtGui.QSizePolicy(QtGui.QSizePolicy.Expanding, QtGui.QSizePolicy.Fixed)
        sizePolicy.setHorizontalStretch(0)
        sizePolicy.setVerticalStretch(0)
        sizePolicy.setHeightForWidth(self.contextFilterCombo.sizePolicy().hasHeightForWidth())
        self.contextFilterCombo.setSizePolicy(sizePolicy)
        self.contextFilterCombo.setEditable(True)
        self.contextFilterCombo.setObjectName(_fromUtf8("contextFilterCombo"))
        self.gridLayout.addWidget(self.contextFilterCombo, 0, 1, 1, 1)
        self.groupFilterLabel = QtGui.QLabel(self.FilterDockContents)
        self.groupFilterLabel.setEnabled(False)
        self.groupFilterLabel.setObjectName(_fromUtf8("groupFilterLabel"))
        self.gridLayout.addWidget(self.groupFilterLabel, 2, 0, 1, 1)
        self.subGroupFilterCombo = QtGui.QComboBox(self.FilterDockContents)
        self.subGroupFilterCombo.setEnabled(False)
        sizePolicy = QtGui.QSizePolicy(QtGui.QSizePolicy.Expanding, QtGui.QSizePolicy.Fixed)
        sizePolicy.setHorizontalStretch(0)
        sizePolicy.setVerticalStretch(0)
        sizePolicy.setHeightForWidth(self.subGroupFilterCombo.sizePolicy().hasHeightForWidth())
        self.subGroupFilterCombo.setSizePolicy(sizePolicy)
        self.subGroupFilterCombo.setEditable(True)
        self.subGroupFilterCombo.setObjectName(_fromUtf8("subGroupFilterCombo"))
        self.gridLayout.addWidget(self.subGroupFilterCombo, 1, 1, 1, 1)
        self.contextFilterLabel = QtGui.QLabel(self.FilterDockContents)
        self.contextFilterLabel.setObjectName(_fromUtf8("contextFilterLabel"))
        self.gridLayout.addWidget(self.contextFilterLabel, 0, 0, 1, 1)
        self.subGroupFilterButton = QtGui.QPushButton(self.FilterDockContents)
        self.subGroupFilterButton.setEnabled(False)
        self.subGroupFilterButton.setObjectName(_fromUtf8("subGroupFilterButton"))
        self.gridLayout.addWidget(self.subGroupFilterButton, 1, 2, 1, 1)
        self.contextFilterButton = QtGui.QPushButton(self.FilterDockContents)
        self.contextFilterButton.setObjectName(_fromUtf8("contextFilterButton"))
        self.gridLayout.addWidget(self.contextFilterButton, 0, 2, 1, 1)
        self.verticalLayout.addLayout(self.gridLayout)
        self.filterEdit = QtGui.QLineEdit(self.FilterDockContents)
        self.filterEdit.setReadOnly(True)
        self.filterEdit.setObjectName(_fromUtf8("filterEdit"))
        self.verticalLayout.addWidget(self.filterEdit)
        self.gridLayout_3 = QtGui.QGridLayout()
        self.gridLayout_3.setObjectName(_fromUtf8("gridLayout_3"))
        self.showPointsLabel = QtGui.QLabel(self.FilterDockContents)
        self.showPointsLabel.setObjectName(_fromUtf8("showPointsLabel"))
        self.gridLayout_3.addWidget(self.showPointsLabel, 0, 1, 1, 1, QtCore.Qt.AlignHCenter)
        self.showPolygonsLabel = QtGui.QLabel(self.FilterDockContents)
        self.showPolygonsLabel.setObjectName(_fromUtf8("showPolygonsLabel"))
        self.gridLayout_3.addWidget(self.showPolygonsLabel, 0, 3, 1, 1, QtCore.Qt.AlignHCenter)
        self.showLinesLabel = QtGui.QLabel(self.FilterDockContents)
        self.showLinesLabel.setObjectName(_fromUtf8("showLinesLabel"))
        self.gridLayout_3.addWidget(self.showLinesLabel, 0, 2, 1, 1, QtCore.Qt.AlignHCenter)
        self.showPolygonsCheck = QtGui.QCheckBox(self.FilterDockContents)
        self.showPolygonsCheck.setText(_fromUtf8(""))
        self.showPolygonsCheck.setChecked(True)
        self.showPolygonsCheck.setObjectName(_fromUtf8("showPolygonsCheck"))
        self.gridLayout_3.addWidget(self.showPolygonsCheck, 1, 3, 1, 1, QtCore.Qt.AlignHCenter)
        self.showLinesCheck = QtGui.QCheckBox(self.FilterDockContents)
        self.showLinesCheck.setText(_fromUtf8(""))
        self.showLinesCheck.setChecked(True)
        self.showLinesCheck.setObjectName(_fromUtf8("showLinesCheck"))
        self.gridLayout_3.addWidget(self.showLinesCheck, 1, 2, 1, 1, QtCore.Qt.AlignHCenter)
        self.showLabel = QtGui.QLabel(self.FilterDockContents)
        self.showLabel.setObjectName(_fromUtf8("showLabel"))
        self.gridLayout_3.addWidget(self.showLabel, 1, 0, 1, 1)
        self.showPointsCheck = QtGui.QCheckBox(self.FilterDockContents)
        self.showPointsCheck.setText(_fromUtf8(""))
        self.showPointsCheck.setChecked(True)
        self.showPointsCheck.setObjectName(_fromUtf8("showPointsCheck"))
        self.gridLayout_3.addWidget(self.showPointsCheck, 1, 1, 1, 1, QtCore.Qt.AlignHCenter)
        self.verticalLayout.addLayout(self.gridLayout_3)
        spacerItem1 = QtGui.QSpacerItem(20, 7, QtGui.QSizePolicy.Minimum, QtGui.QSizePolicy.Expanding)
        self.verticalLayout.addItem(spacerItem1)
        self.filterEdit.raise_()
        FilterDock.setWidget(self.FilterDockContents)
        self.zoomFilterAction = QtGui.QAction(FilterDock)
        self.zoomFilterAction.setIcon(icon)
        self.zoomFilterAction.setObjectName(_fromUtf8("zoomFilterAction"))
        self.buildFilterAction = QtGui.QAction(FilterDock)
        self.buildFilterAction.setIcon(icon1)
        self.buildFilterAction.setObjectName(_fromUtf8("buildFilterAction"))
        self.clearFilterAction = QtGui.QAction(FilterDock)
        self.clearFilterAction.setIcon(icon2)
        self.clearFilterAction.setObjectName(_fromUtf8("clearFilterAction"))
        self.loadDataAction = QtGui.QAction(FilterDock)
        self.loadDataAction.setIcon(icon3)
        self.loadDataAction.setObjectName(_fromUtf8("loadDataAction"))
        self.showDataAction = QtGui.QAction(FilterDock)
        self.showDataAction.setIcon(icon4)
        self.showDataAction.setObjectName(_fromUtf8("showDataAction"))
        self.subGroupFilterLabel.setBuddy(self.subGroupFilterCombo)
        self.groupFilterLabel.setBuddy(self.groupFilterCombo)
        self.contextFilterLabel.setBuddy(self.contextFilterCombo)

        self.retranslateUi(FilterDock)
        QtCore.QMetaObject.connectSlotsByName(FilterDock)

    def retranslateUi(self, FilterDock):
        FilterDock.setWindowTitle(_translate("FilterDock", "Filter Ark Layers", None))
        self.zoomFilterTool.setText(_translate("FilterDock", "Zoom", None))
        self.buildFilterTool.setText(_translate("FilterDock", "Build", None))
        self.clearFilterTool.setText(_translate("FilterDock", "Clear", None))
        self.loadDataTool.setText(_translate("FilterDock", "Load", None))
        self.showDataTool.setText(_translate("FilterDock", "Show", None))
        self.subGroupFilterLabel.setText(_translate("FilterDock", "Sub-Groups:", None))
        self.groupFilterButton.setText(_translate("FilterDock", "Apply", None))
        self.groupFilterLabel.setText(_translate("FilterDock", "Groups:", None))
        self.contextFilterLabel.setText(_translate("FilterDock", "Contexts:", None))
        self.subGroupFilterButton.setText(_translate("FilterDock", "Apply", None))
        self.contextFilterButton.setText(_translate("FilterDock", "Apply", None))
        self.showPointsLabel.setText(_translate("FilterDock", "Points", None))
        self.showPolygonsLabel.setText(_translate("FilterDock", "Polys", None))
        self.showLinesLabel.setText(_translate("FilterDock", "Lines", None))
        self.showPolygonsCheck.setToolTip(_translate("FilterDock", "Show existing polygons", None))
        self.showLinesCheck.setToolTip(_translate("FilterDock", "Show existing lines", None))
        self.showLabel.setText(_translate("FilterDock", "Show:", None))
        self.showPointsCheck.setToolTip(_translate("FilterDock", "Show existing levels", None))
        self.zoomFilterAction.setText(_translate("FilterDock", "Zoom To Selection", None))
        self.buildFilterAction.setText(_translate("FilterDock", "Build Filter", None))
        self.clearFilterAction.setText(_translate("FilterDock", "Clear Filter", None))
        self.loadDataAction.setText(_translate("FilterDock", "Load Data", None))
        self.showDataAction.setText(_translate("FilterDock", "Show Data", None))

from ..libarkqgis.dock import ArkDockWidget
import resources_rc
