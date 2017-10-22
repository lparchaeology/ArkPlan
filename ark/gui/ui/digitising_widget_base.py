# -*- coding: utf-8 -*-

# Form implementation generated from reading ui file 'ark/gui/ui/digitising_widget_base.ui'
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

class Ui_DigitisingWidget(object):
    def setupUi(self, DigitisingWidget):
        DigitisingWidget.setObjectName(_fromUtf8("DigitisingWidget"))
        self.verticalLayout = QtGui.QVBoxLayout(DigitisingWidget)
        self.verticalLayout.setSizeConstraint(QtGui.QLayout.SetMinAndMaxSize)
        self.verticalLayout.setMargin(0)
        self.verticalLayout.setObjectName(_fromUtf8("verticalLayout"))
        self.digitisingScrollArea = QtGui.QScrollArea(DigitisingWidget)
        self.digitisingScrollArea.setFrameShape(QtGui.QFrame.NoFrame)
        self.digitisingScrollArea.setWidgetResizable(True)
        self.digitisingScrollArea.setObjectName(_fromUtf8("digitisingScrollArea"))
        self.digitisingScrollAreaContents = QtGui.QWidget()
        self.digitisingScrollAreaContents.setObjectName(_fromUtf8("digitisingScrollAreaContents"))
        self.verticalLayout_2 = QtGui.QVBoxLayout(self.digitisingScrollAreaContents)
        self.verticalLayout_2.setSizeConstraint(QtGui.QLayout.SetMinAndMaxSize)
        self.verticalLayout_2.setMargin(0)
        self.verticalLayout_2.setObjectName(_fromUtf8("verticalLayout_2"))
        self.sourceGroup = QtGui.QGroupBox(self.digitisingScrollAreaContents)
        self.sourceGroup.setObjectName(_fromUtf8("sourceGroup"))
        self.verticalLayout_3 = QtGui.QVBoxLayout(self.sourceGroup)
        self.verticalLayout_3.setObjectName(_fromUtf8("verticalLayout_3"))
        self.sourceWidget = SourceWidget(self.sourceGroup)
        self.sourceWidget.setObjectName(_fromUtf8("sourceWidget"))
        self.verticalLayout_3.addWidget(self.sourceWidget)
        self.verticalLayout_2.addWidget(self.sourceGroup)
        self.tabWidget = QtGui.QTabWidget(self.digitisingScrollAreaContents)
        self.tabWidget.setObjectName(_fromUtf8("tabWidget"))
        self.planDigitisingWidget = QtGui.QWidget()
        self.planDigitisingWidget.setObjectName(_fromUtf8("planDigitisingWidget"))
        self.verticalLayout_4 = QtGui.QVBoxLayout(self.planDigitisingWidget)
        self.verticalLayout_4.setSizeConstraint(QtGui.QLayout.SetMinAndMaxSize)
        self.verticalLayout_4.setContentsMargins(12, 0, 12, 12)
        self.verticalLayout_4.setObjectName(_fromUtf8("verticalLayout_4"))
        self.planFeatureWidget = FeatureWidget(self.planDigitisingWidget)
        self.planFeatureWidget.setObjectName(_fromUtf8("planFeatureWidget"))
        self.verticalLayout_4.addWidget(self.planFeatureWidget)
        spacerItem = QtGui.QSpacerItem(58, 25, QtGui.QSizePolicy.Minimum, QtGui.QSizePolicy.Expanding)
        self.verticalLayout_4.addItem(spacerItem)
        self.tabWidget.addTab(self.planDigitisingWidget, _fromUtf8(""))
        self.sectionDigitisingWidget = QtGui.QWidget()
        self.sectionDigitisingWidget.setObjectName(_fromUtf8("sectionDigitisingWidget"))
        self.verticalLayout_6 = QtGui.QVBoxLayout(self.sectionDigitisingWidget)
        self.verticalLayout_6.setSizeConstraint(QtGui.QLayout.SetMinAndMaxSize)
        self.verticalLayout_6.setMargin(12)
        self.verticalLayout_6.setObjectName(_fromUtf8("verticalLayout_6"))
        self.sectionFeatureWidget = FeatureWidget(self.sectionDigitisingWidget)
        self.sectionFeatureWidget.setObjectName(_fromUtf8("sectionFeatureWidget"))
        self.verticalLayout_6.addWidget(self.sectionFeatureWidget)
        spacerItem1 = QtGui.QSpacerItem(68, 25, QtGui.QSizePolicy.Minimum, QtGui.QSizePolicy.Expanding)
        self.verticalLayout_6.addItem(spacerItem1)
        self.tabWidget.addTab(self.sectionDigitisingWidget, _fromUtf8(""))
        self.siteDigitisingWidget = QtGui.QWidget()
        self.siteDigitisingWidget.setObjectName(_fromUtf8("siteDigitisingWidget"))
        self.verticalLayout_5 = QtGui.QVBoxLayout(self.siteDigitisingWidget)
        self.verticalLayout_5.setSizeConstraint(QtGui.QLayout.SetMinAndMaxSize)
        self.verticalLayout_5.setContentsMargins(12, 12, 12, 0)
        self.verticalLayout_5.setObjectName(_fromUtf8("verticalLayout_5"))
        self.siteFeatureWidget = FeatureWidget(self.siteDigitisingWidget)
        self.siteFeatureWidget.setObjectName(_fromUtf8("siteFeatureWidget"))
        self.verticalLayout_5.addWidget(self.siteFeatureWidget)
        spacerItem2 = QtGui.QSpacerItem(88, 25, QtGui.QSizePolicy.Minimum, QtGui.QSizePolicy.Expanding)
        self.verticalLayout_5.addItem(spacerItem2)
        self.tabWidget.addTab(self.siteDigitisingWidget, _fromUtf8(""))
        self.verticalLayout_2.addWidget(self.tabWidget)
        self.digitisingScrollArea.setWidget(self.digitisingScrollAreaContents)
        self.verticalLayout.addWidget(self.digitisingScrollArea)
        self.horizontalLayout = QtGui.QHBoxLayout()
        self.horizontalLayout.setObjectName(_fromUtf8("horizontalLayout"))
        self.resetButton = QtGui.QPushButton(DigitisingWidget)
        self.resetButton.setObjectName(_fromUtf8("resetButton"))
        self.horizontalLayout.addWidget(self.resetButton)
        self.mergeButton = QtGui.QPushButton(DigitisingWidget)
        self.mergeButton.setObjectName(_fromUtf8("mergeButton"))
        self.horizontalLayout.addWidget(self.mergeButton)
        self.verticalLayout.addLayout(self.horizontalLayout)

        self.retranslateUi(DigitisingWidget)
        self.tabWidget.setCurrentIndex(0)
        QtCore.QMetaObject.connectSlotsByName(DigitisingWidget)

    def retranslateUi(self, DigitisingWidget):
        DigitisingWidget.setWindowTitle(_translate("DigitisingWidget", "DigitisingWidget", None))
        self.sourceGroup.setTitle(_translate("DigitisingWidget", "Source Metadata", None))
        self.tabWidget.setTabText(self.tabWidget.indexOf(self.planDigitisingWidget), _translate("DigitisingWidget", "Plan", None))
        self.tabWidget.setTabText(self.tabWidget.indexOf(self.sectionDigitisingWidget), _translate("DigitisingWidget", "Section", None))
        self.tabWidget.setTabText(self.tabWidget.indexOf(self.siteDigitisingWidget), _translate("DigitisingWidget", "Site", None))
        self.resetButton.setToolTip(_translate("DigitisingWidget", "Clear unsaved changes from work layers", None))
        self.resetButton.setText(_translate("DigitisingWidget", "Reset", None))
        self.mergeButton.setToolTip(_translate("DigitisingWidget", "Move new context to main layers", None))
        self.mergeButton.setText(_translate("DigitisingWidget", "Merge", None))

from ..feature_widget import FeatureWidget
from ..source_widget import SourceWidget
