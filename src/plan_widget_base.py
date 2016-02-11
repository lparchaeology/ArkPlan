# -*- coding: utf-8 -*-

# Form implementation generated from reading ui file 'src/plan_widget_base.ui'
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

class Ui_PlanWidget(object):
    def setupUi(self, PlanWidget):
        PlanWidget.setObjectName(_fromUtf8("PlanWidget"))
        PlanWidget.resize(400, 300)
        self.drawingTab = QtGui.QWidget()
        self.drawingTab.setObjectName(_fromUtf8("drawingTab"))
        self.verticalLayout = QtGui.QVBoxLayout(self.drawingTab)
        self.verticalLayout.setMargin(0)
        self.verticalLayout.setObjectName(_fromUtf8("verticalLayout"))
        self.drawingScrollArea = QtGui.QScrollArea(self.drawingTab)
        self.drawingScrollArea.setFrameShape(QtGui.QFrame.NoFrame)
        self.drawingScrollArea.setWidgetResizable(True)
        self.drawingScrollArea.setObjectName(_fromUtf8("drawingScrollArea"))
        self.drawingScrollAreaContents = QtGui.QWidget()
        self.drawingScrollAreaContents.setGeometry(QtCore.QRect(0, 0, 392, 223))
        self.drawingScrollAreaContents.setObjectName(_fromUtf8("drawingScrollAreaContents"))
        self.verticalLayout_2 = QtGui.QVBoxLayout(self.drawingScrollAreaContents)
        self.verticalLayout_2.setMargin(0)
        self.verticalLayout_2.setObjectName(_fromUtf8("verticalLayout_2"))
        self.metadataWidget = MetadataWidget(self.drawingScrollAreaContents)
        self.metadataWidget.setObjectName(_fromUtf8("metadataWidget"))
        self.verticalLayout_2.addWidget(self.metadataWidget)
        self.drawingWidget = DrawingWidget(self.drawingScrollAreaContents)
        self.drawingWidget.setObjectName(_fromUtf8("drawingWidget"))
        self.verticalLayout_2.addWidget(self.drawingWidget)
        spacerItem = QtGui.QSpacerItem(20, 40, QtGui.QSizePolicy.Minimum, QtGui.QSizePolicy.Expanding)
        self.verticalLayout_2.addItem(spacerItem)
        self.drawingScrollArea.setWidget(self.drawingScrollAreaContents)
        self.verticalLayout.addWidget(self.drawingScrollArea)
        self.horizontalLayout = QtGui.QHBoxLayout()
        self.horizontalLayout.setObjectName(_fromUtf8("horizontalLayout"))
        self.clearButton = QtGui.QPushButton(self.drawingTab)
        self.clearButton.setObjectName(_fromUtf8("clearButton"))
        self.horizontalLayout.addWidget(self.clearButton)
        self.mergeButton = QtGui.QPushButton(self.drawingTab)
        self.mergeButton.setObjectName(_fromUtf8("mergeButton"))
        self.horizontalLayout.addWidget(self.mergeButton)
        self.verticalLayout.addLayout(self.horizontalLayout)
        PlanWidget.addTab(self.drawingTab, _fromUtf8(""))
        self.checkingTab = QtGui.QWidget()
        self.checkingTab.setObjectName(_fromUtf8("checkingTab"))
        self.verticalLayout_3 = QtGui.QVBoxLayout(self.checkingTab)
        self.verticalLayout_3.setMargin(0)
        self.verticalLayout_3.setObjectName(_fromUtf8("verticalLayout_3"))
        self.checkingScrollArea = QtGui.QScrollArea(self.checkingTab)
        self.checkingScrollArea.setFrameShape(QtGui.QFrame.NoFrame)
        self.checkingScrollArea.setWidgetResizable(True)
        self.checkingScrollArea.setObjectName(_fromUtf8("checkingScrollArea"))
        self.checkingScrollAreaContents = QtGui.QWidget()
        self.checkingScrollAreaContents.setGeometry(QtCore.QRect(0, 0, 392, 265))
        self.checkingScrollAreaContents.setObjectName(_fromUtf8("checkingScrollAreaContents"))
        self.verticalLayout_4 = QtGui.QVBoxLayout(self.checkingScrollAreaContents)
        self.verticalLayout_4.setMargin(0)
        self.verticalLayout_4.setObjectName(_fromUtf8("verticalLayout_4"))
        self.schematicWidget = SchematicWidget(self.checkingScrollAreaContents)
        self.schematicWidget.setObjectName(_fromUtf8("schematicWidget"))
        self.verticalLayout_4.addWidget(self.schematicWidget)
        spacerItem1 = QtGui.QSpacerItem(20, 204, QtGui.QSizePolicy.Minimum, QtGui.QSizePolicy.Expanding)
        self.verticalLayout_4.addItem(spacerItem1)
        self.checkingScrollArea.setWidget(self.checkingScrollAreaContents)
        self.verticalLayout_3.addWidget(self.checkingScrollArea)
        PlanWidget.addTab(self.checkingTab, _fromUtf8(""))
        self.toolsTab = QtGui.QWidget()
        self.toolsTab.setObjectName(_fromUtf8("toolsTab"))
        self.verticalLayout_5 = QtGui.QVBoxLayout(self.toolsTab)
        self.verticalLayout_5.setMargin(0)
        self.verticalLayout_5.setObjectName(_fromUtf8("verticalLayout_5"))
        self.toolsScrollArea = QtGui.QScrollArea(self.toolsTab)
        self.toolsScrollArea.setFrameShape(QtGui.QFrame.NoFrame)
        self.toolsScrollArea.setWidgetResizable(True)
        self.toolsScrollArea.setObjectName(_fromUtf8("toolsScrollArea"))
        self.toolsScrollAreaContents = QtGui.QWidget()
        self.toolsScrollAreaContents.setGeometry(QtCore.QRect(0, 0, 392, 265))
        self.toolsScrollAreaContents.setObjectName(_fromUtf8("toolsScrollAreaContents"))
        self.verticalLayout_6 = QtGui.QVBoxLayout(self.toolsScrollAreaContents)
        self.verticalLayout_6.setMargin(0)
        self.verticalLayout_6.setObjectName(_fromUtf8("verticalLayout_6"))
        self.snappingWidget = SnappingWidget(self.toolsScrollAreaContents)
        self.snappingWidget.setObjectName(_fromUtf8("snappingWidget"))
        self.verticalLayout_6.addWidget(self.snappingWidget)
        spacerItem2 = QtGui.QSpacerItem(20, 246, QtGui.QSizePolicy.Minimum, QtGui.QSizePolicy.Expanding)
        self.verticalLayout_6.addItem(spacerItem2)
        self.toolsScrollArea.setWidget(self.toolsScrollAreaContents)
        self.verticalLayout_5.addWidget(self.toolsScrollArea)
        PlanWidget.addTab(self.toolsTab, _fromUtf8(""))

        self.retranslateUi(PlanWidget)
        PlanWidget.setCurrentIndex(0)
        QtCore.QMetaObject.connectSlotsByName(PlanWidget)

    def retranslateUi(self, PlanWidget):
        PlanWidget.setWindowTitle(_translate("PlanWidget", "TabWidget", None))
        self.clearButton.setToolTip(_translate("PlanWidget", "Clear unsaved changes from work layers", None))
        self.clearButton.setText(_translate("PlanWidget", "Clear", None))
        self.mergeButton.setToolTip(_translate("PlanWidget", "Move new context to main layers", None))
        self.mergeButton.setText(_translate("PlanWidget", "Merge", None))
        PlanWidget.setTabText(PlanWidget.indexOf(self.drawingTab), _translate("PlanWidget", "Drawing", None))
        PlanWidget.setTabText(PlanWidget.indexOf(self.checkingTab), _translate("PlanWidget", "Checking", None))
        PlanWidget.setTabText(PlanWidget.indexOf(self.toolsTab), _translate("PlanWidget", "Tools", None))

from drawing_widget import DrawingWidget
from metadata_widget import MetadataWidget
from schematic_widget import SchematicWidget
from snapping_widget import SnappingWidget
