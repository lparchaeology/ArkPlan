# -*- coding: utf-8 -*-

# Form implementation generated from reading ui file 'src/drawing_widget_base.ui'
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

class Ui_DrawingWidget(object):
    def setupUi(self, DrawingWidget):
        DrawingWidget.setObjectName(_fromUtf8("DrawingWidget"))
        self.verticalLayout = QtGui.QVBoxLayout(DrawingWidget)
        self.verticalLayout.setSizeConstraint(QtGui.QLayout.SetMinAndMaxSize)
        self.verticalLayout.setMargin(0)
        self.verticalLayout.setObjectName(_fromUtf8("verticalLayout"))
        self.drawingScrollArea = QtGui.QScrollArea(DrawingWidget)
        self.drawingScrollArea.setFrameShape(QtGui.QFrame.NoFrame)
        self.drawingScrollArea.setWidgetResizable(True)
        self.drawingScrollArea.setObjectName(_fromUtf8("drawingScrollArea"))
        self.drawingScrollAreaContents = QtGui.QWidget()
        self.drawingScrollAreaContents.setObjectName(_fromUtf8("drawingScrollAreaContents"))
        self.verticalLayout_2 = QtGui.QVBoxLayout(self.drawingScrollAreaContents)
        self.verticalLayout_2.setSizeConstraint(QtGui.QLayout.SetMinAndMaxSize)
        self.verticalLayout_2.setMargin(0)
        self.verticalLayout_2.setObjectName(_fromUtf8("verticalLayout_2"))
        self.sourceGroup = QtGui.QGroupBox(self.drawingScrollAreaContents)
        self.sourceGroup.setObjectName(_fromUtf8("sourceGroup"))
        self.verticalLayout_3 = QtGui.QVBoxLayout(self.sourceGroup)
        self.verticalLayout_3.setObjectName(_fromUtf8("verticalLayout_3"))
        self.sourceWidget = SourceWidget(self.sourceGroup)
        self.sourceWidget.setObjectName(_fromUtf8("sourceWidget"))
        self.verticalLayout_3.addWidget(self.sourceWidget)
        self.verticalLayout_2.addWidget(self.sourceGroup)
        self.tabWidget = QtGui.QTabWidget(self.drawingScrollAreaContents)
        self.tabWidget.setObjectName(_fromUtf8("tabWidget"))
        self.planDrawingWidget = QtGui.QWidget()
        self.planDrawingWidget.setObjectName(_fromUtf8("planDrawingWidget"))
        self.verticalLayout_4 = QtGui.QVBoxLayout(self.planDrawingWidget)
        self.verticalLayout_4.setSizeConstraint(QtGui.QLayout.SetMinAndMaxSize)
        self.verticalLayout_4.setContentsMargins(12, -1, 12, 12)
        self.verticalLayout_4.setObjectName(_fromUtf8("verticalLayout_4"))
        self.planFeatureWidget = FeatureWidget(self.planDrawingWidget)
        self.planFeatureWidget.setObjectName(_fromUtf8("planFeatureWidget"))
        self.verticalLayout_4.addWidget(self.planFeatureWidget)
        spacerItem = QtGui.QSpacerItem(58, 25, QtGui.QSizePolicy.Minimum, QtGui.QSizePolicy.Expanding)
        self.verticalLayout_4.addItem(spacerItem)
        self.tabWidget.addTab(self.planDrawingWidget, _fromUtf8(""))
        self.sectionDrawingWidget = QtGui.QWidget()
        self.sectionDrawingWidget.setObjectName(_fromUtf8("sectionDrawingWidget"))
        self.verticalLayout_6 = QtGui.QVBoxLayout(self.sectionDrawingWidget)
        self.verticalLayout_6.setSizeConstraint(QtGui.QLayout.SetMinAndMaxSize)
        self.verticalLayout_6.setMargin(12)
        self.verticalLayout_6.setObjectName(_fromUtf8("verticalLayout_6"))
        self.sectionFeatureWidget = FeatureWidget(self.sectionDrawingWidget)
        self.sectionFeatureWidget.setObjectName(_fromUtf8("sectionFeatureWidget"))
        self.verticalLayout_6.addWidget(self.sectionFeatureWidget)
        spacerItem1 = QtGui.QSpacerItem(68, 25, QtGui.QSizePolicy.Minimum, QtGui.QSizePolicy.Expanding)
        self.verticalLayout_6.addItem(spacerItem1)
        self.tabWidget.addTab(self.sectionDrawingWidget, _fromUtf8(""))
        self.siteDrawingWidget = QtGui.QWidget()
        self.siteDrawingWidget.setObjectName(_fromUtf8("siteDrawingWidget"))
        self.verticalLayout_5 = QtGui.QVBoxLayout(self.siteDrawingWidget)
        self.verticalLayout_5.setSizeConstraint(QtGui.QLayout.SetMinAndMaxSize)
        self.verticalLayout_5.setContentsMargins(12, 12, 12, 0)
        self.verticalLayout_5.setObjectName(_fromUtf8("verticalLayout_5"))
        self.siteFeatureWidget = FeatureWidget(self.siteDrawingWidget)
        self.siteFeatureWidget.setObjectName(_fromUtf8("siteFeatureWidget"))
        self.verticalLayout_5.addWidget(self.siteFeatureWidget)
        spacerItem2 = QtGui.QSpacerItem(88, 25, QtGui.QSizePolicy.Minimum, QtGui.QSizePolicy.Expanding)
        self.verticalLayout_5.addItem(spacerItem2)
        self.tabWidget.addTab(self.siteDrawingWidget, _fromUtf8(""))
        self.verticalLayout_2.addWidget(self.tabWidget)
        self.drawingScrollArea.setWidget(self.drawingScrollAreaContents)
        self.verticalLayout.addWidget(self.drawingScrollArea)
        self.horizontalLayout = QtGui.QHBoxLayout()
        self.horizontalLayout.setObjectName(_fromUtf8("horizontalLayout"))
        self.resetButton = QtGui.QPushButton(DrawingWidget)
        self.resetButton.setObjectName(_fromUtf8("resetButton"))
        self.horizontalLayout.addWidget(self.resetButton)
        self.mergeButton = QtGui.QPushButton(DrawingWidget)
        self.mergeButton.setObjectName(_fromUtf8("mergeButton"))
        self.horizontalLayout.addWidget(self.mergeButton)
        self.verticalLayout.addLayout(self.horizontalLayout)

        self.retranslateUi(DrawingWidget)
        self.tabWidget.setCurrentIndex(0)
        QtCore.QMetaObject.connectSlotsByName(DrawingWidget)

    def retranslateUi(self, DrawingWidget):
        DrawingWidget.setWindowTitle(_translate("DrawingWidget", "DrawingWidget", None))
        self.sourceGroup.setTitle(_translate("DrawingWidget", "Source Metadata", None))
        self.tabWidget.setTabText(self.tabWidget.indexOf(self.planDrawingWidget), _translate("DrawingWidget", "Plan", None))
        self.tabWidget.setTabText(self.tabWidget.indexOf(self.sectionDrawingWidget), _translate("DrawingWidget", "Section", None))
        self.tabWidget.setTabText(self.tabWidget.indexOf(self.siteDrawingWidget), _translate("DrawingWidget", "Site", None))
        self.resetButton.setToolTip(_translate("DrawingWidget", "Clear unsaved changes from work layers", None))
        self.resetButton.setText(_translate("DrawingWidget", "Reset", None))
        self.mergeButton.setToolTip(_translate("DrawingWidget", "Move new context to main layers", None))
        self.mergeButton.setText(_translate("DrawingWidget", "Merge", None))

from feature_widget import FeatureWidget
from source_widget import SourceWidget
