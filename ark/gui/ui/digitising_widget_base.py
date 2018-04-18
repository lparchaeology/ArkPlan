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
        DigitisingWidget.resize(372, 401)
        self.verticalLayout = QtGui.QVBoxLayout(DigitisingWidget)
        self.verticalLayout.setSizeConstraint(QtGui.QLayout.SetMinAndMaxSize)
        self.verticalLayout.setMargin(0)
        self.verticalLayout.setObjectName(_fromUtf8("verticalLayout"))
        self.digitisingScrollArea = QtGui.QScrollArea(DigitisingWidget)
        self.digitisingScrollArea.setFrameShape(QtGui.QFrame.NoFrame)
        self.digitisingScrollArea.setWidgetResizable(True)
        self.digitisingScrollArea.setObjectName(_fromUtf8("digitisingScrollArea"))
        self.digitisingScrollAreaContents = QtGui.QWidget()
        self.digitisingScrollAreaContents.setGeometry(QtCore.QRect(0, 0, 372, 358))
        self.digitisingScrollAreaContents.setObjectName(_fromUtf8("digitisingScrollAreaContents"))
        self.digitisingScrollAreaLayout = QtGui.QVBoxLayout(self.digitisingScrollAreaContents)
        self.digitisingScrollAreaLayout.setSizeConstraint(QtGui.QLayout.SetMinAndMaxSize)
        self.digitisingScrollAreaLayout.setMargin(0)
        self.digitisingScrollAreaLayout.setObjectName(_fromUtf8("digitisingScrollAreaLayout"))
        self.sourceGroup = QtGui.QGroupBox(self.digitisingScrollAreaContents)
        self.sourceGroup.setObjectName(_fromUtf8("sourceGroup"))
        self.sourceLayout = QtGui.QVBoxLayout(self.sourceGroup)
        self.sourceLayout.setObjectName(_fromUtf8("sourceLayout"))
        self.sourceWidget = SourceWidget(self.sourceGroup)
        self.sourceWidget.setObjectName(_fromUtf8("sourceWidget"))
        self.sourceLayout.addWidget(self.sourceWidget)
        self.digitisingScrollAreaLayout.addWidget(self.sourceGroup)
        self.digitisingTabWidget = QtGui.QTabWidget(self.digitisingScrollAreaContents)
        self.digitisingTabWidget.setObjectName(_fromUtf8("digitisingTabWidget"))
        self.planDigitisingWidget = QtGui.QWidget()
        self.planDigitisingWidget.setObjectName(_fromUtf8("planDigitisingWidget"))
        self.planDigitisingLayout = QtGui.QVBoxLayout(self.planDigitisingWidget)
        self.planDigitisingLayout.setSizeConstraint(QtGui.QLayout.SetMinAndMaxSize)
        self.planDigitisingLayout.setMargin(12)
        self.planDigitisingLayout.setObjectName(_fromUtf8("planDigitisingLayout"))
        self.planFeatureWidget = ItemFeatureWidget(self.planDigitisingWidget)
        self.planFeatureWidget.setObjectName(_fromUtf8("planFeatureWidget"))
        self.planDigitisingLayout.addWidget(self.planFeatureWidget)
        spacerItem = QtGui.QSpacerItem(58, 25, QtGui.QSizePolicy.Minimum, QtGui.QSizePolicy.Expanding)
        self.planDigitisingLayout.addItem(spacerItem)
        self.digitisingTabWidget.addTab(self.planDigitisingWidget, _fromUtf8(""))
        self.sectionDigitisingWidget = QtGui.QWidget()
        self.sectionDigitisingWidget.setObjectName(_fromUtf8("sectionDigitisingWidget"))
        self.sectionDigitisingLayout = QtGui.QVBoxLayout(self.sectionDigitisingWidget)
        self.sectionDigitisingLayout.setSizeConstraint(QtGui.QLayout.SetMinAndMaxSize)
        self.sectionDigitisingLayout.setMargin(12)
        self.sectionDigitisingLayout.setObjectName(_fromUtf8("sectionDigitisingLayout"))
        self.sectionFeatureWidget = ItemFeatureWidget(self.sectionDigitisingWidget)
        self.sectionFeatureWidget.setObjectName(_fromUtf8("sectionFeatureWidget"))
        self.sectionDigitisingLayout.addWidget(self.sectionFeatureWidget)
        spacerItem1 = QtGui.QSpacerItem(68, 25, QtGui.QSizePolicy.Minimum, QtGui.QSizePolicy.Expanding)
        self.sectionDigitisingLayout.addItem(spacerItem1)
        self.digitisingTabWidget.addTab(self.sectionDigitisingWidget, _fromUtf8(""))
        self.siteDigitisingWidget = QtGui.QWidget()
        self.siteDigitisingWidget.setObjectName(_fromUtf8("siteDigitisingWidget"))
        self.siteDigitisingLayout = QtGui.QVBoxLayout(self.siteDigitisingWidget)
        self.siteDigitisingLayout.setSizeConstraint(QtGui.QLayout.SetMinAndMaxSize)
        self.siteDigitisingLayout.setMargin(12)
        self.siteDigitisingLayout.setObjectName(_fromUtf8("siteDigitisingLayout"))
        self.siteFeatureWidget = ItemFeatureWidget(self.siteDigitisingWidget)
        self.siteFeatureWidget.setObjectName(_fromUtf8("siteFeatureWidget"))
        self.siteDigitisingLayout.addWidget(self.siteFeatureWidget)
        spacerItem2 = QtGui.QSpacerItem(88, 25, QtGui.QSizePolicy.Minimum, QtGui.QSizePolicy.Expanding)
        self.siteDigitisingLayout.addItem(spacerItem2)
        self.digitisingTabWidget.addTab(self.siteDigitisingWidget, _fromUtf8(""))
        self.digitisingScrollAreaLayout.addWidget(self.digitisingTabWidget)
        self.digitisingScrollArea.setWidget(self.digitisingScrollAreaContents)
        self.verticalLayout.addWidget(self.digitisingScrollArea)
        self.digitisingButtonLayout = QtGui.QHBoxLayout()
        self.digitisingButtonLayout.setObjectName(_fromUtf8("digitisingButtonLayout"))
        self.resetButton = QtGui.QPushButton(DigitisingWidget)
        self.resetButton.setObjectName(_fromUtf8("resetButton"))
        self.digitisingButtonLayout.addWidget(self.resetButton)
        self.mergeButton = QtGui.QPushButton(DigitisingWidget)
        self.mergeButton.setObjectName(_fromUtf8("mergeButton"))
        self.digitisingButtonLayout.addWidget(self.mergeButton)
        self.verticalLayout.addLayout(self.digitisingButtonLayout)

        self.retranslateUi(DigitisingWidget)
        self.digitisingTabWidget.setCurrentIndex(0)
        QtCore.QMetaObject.connectSlotsByName(DigitisingWidget)

    def retranslateUi(self, DigitisingWidget):
        DigitisingWidget.setWindowTitle(_translate("DigitisingWidget", "DigitisingWidget", None))
        self.sourceGroup.setTitle(_translate("DigitisingWidget", "Source Metadata", None))
        self.digitisingTabWidget.setTabText(self.digitisingTabWidget.indexOf(self.planDigitisingWidget), _translate("DigitisingWidget", "Plan", None))
        self.digitisingTabWidget.setTabText(self.digitisingTabWidget.indexOf(self.sectionDigitisingWidget), _translate("DigitisingWidget", "Section", None))
        self.digitisingTabWidget.setTabText(self.digitisingTabWidget.indexOf(self.siteDigitisingWidget), _translate("DigitisingWidget", "Site", None))
        self.resetButton.setToolTip(_translate("DigitisingWidget", "Clear unsaved changes from work layers", None))
        self.resetButton.setText(_translate("DigitisingWidget", "Reset", None))
        self.mergeButton.setToolTip(_translate("DigitisingWidget", "Move new context to main layers", None))
        self.mergeButton.setText(_translate("DigitisingWidget", "Merge", None))

from ..item_feature_widget import ItemFeatureWidget
from ..source_widget import SourceWidget
