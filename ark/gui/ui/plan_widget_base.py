# -*- coding: utf-8 -*-

# Form implementation generated from reading ui file 'ark/gui/ui/plan_widget_base.ui'
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
        self.digitisingTab = QtGui.QWidget()
        self.digitisingTab.setObjectName(_fromUtf8("digitisingTab"))
        self.verticalLayout = QtGui.QVBoxLayout(self.digitisingTab)
        self.verticalLayout.setSizeConstraint(QtGui.QLayout.SetMinimumSize)
        self.verticalLayout.setMargin(0)
        self.verticalLayout.setObjectName(_fromUtf8("verticalLayout"))
        self.digitisingWidget = DigitisingWidget(self.digitisingTab)
        self.digitisingWidget.setObjectName(_fromUtf8("digitisingWidget"))
        self.verticalLayout.addWidget(self.digitisingWidget)
        PlanWidget.addTab(self.digitisingTab, _fromUtf8(""))
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
        self.checkingScrollAreaContents.setObjectName(_fromUtf8("checkingScrollAreaContents"))
        self.verticalLayout_4 = QtGui.QVBoxLayout(self.checkingScrollAreaContents)
        self.verticalLayout_4.setSizeConstraint(QtGui.QLayout.SetMinAndMaxSize)
        self.verticalLayout_4.setMargin(0)
        self.verticalLayout_4.setObjectName(_fromUtf8("verticalLayout_4"))
        self.schematicWidget = SchematicWidget(self.checkingScrollAreaContents)
        self.schematicWidget.setObjectName(_fromUtf8("schematicWidget"))
        self.verticalLayout_4.addWidget(self.schematicWidget)
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
        self.toolsScrollAreaContents.setObjectName(_fromUtf8("toolsScrollAreaContents"))
        self.verticalLayout_6 = QtGui.QVBoxLayout(self.toolsScrollAreaContents)
        self.verticalLayout_6.setSizeConstraint(QtGui.QLayout.SetMinAndMaxSize)
        self.verticalLayout_6.setMargin(0)
        self.verticalLayout_6.setObjectName(_fromUtf8("verticalLayout_6"))
        self.snappingWidget = SnappingWidget(self.toolsScrollAreaContents)
        self.snappingWidget.setObjectName(_fromUtf8("snappingWidget"))
        self.verticalLayout_6.addWidget(self.snappingWidget)
        self.toolsScrollArea.setWidget(self.toolsScrollAreaContents)
        self.verticalLayout_5.addWidget(self.toolsScrollArea)
        PlanWidget.addTab(self.toolsTab, _fromUtf8(""))

        self.retranslateUi(PlanWidget)
        PlanWidget.setCurrentIndex(0)
        QtCore.QMetaObject.connectSlotsByName(PlanWidget)

    def retranslateUi(self, PlanWidget):
        PlanWidget.setWindowTitle(_translate("PlanWidget", "PlanWidget", None))
        PlanWidget.setTabText(PlanWidget.indexOf(self.digitisingTab), _translate("PlanWidget", "Drawing", None))
        PlanWidget.setTabText(PlanWidget.indexOf(self.checkingTab), _translate("PlanWidget", "Checking", None))
        PlanWidget.setTabText(PlanWidget.indexOf(self.toolsTab), _translate("PlanWidget", "Tools", None))

from ..digitising_widget import DigitisingWidget
from ..schematic_widget import SchematicWidget
from ..snapping_widget import SnappingWidget
