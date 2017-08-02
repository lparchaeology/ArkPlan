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
        DrawingWidget.resize(309, 264)
        self.gridLayout_4 = QtGui.QGridLayout(DrawingWidget)
        self.gridLayout_4.setMargin(0)
        self.gridLayout_4.setObjectName(_fromUtf8("gridLayout_4"))
        self.drawingScrollArea = QtGui.QScrollArea(DrawingWidget)
        self.drawingScrollArea.setFrameShape(QtGui.QFrame.NoFrame)
        self.drawingScrollArea.setWidgetResizable(True)
        self.drawingScrollArea.setObjectName(_fromUtf8("drawingScrollArea"))
        self.drawingScrollAreaContents = QtGui.QWidget()
        self.drawingScrollAreaContents.setGeometry(QtCore.QRect(0, 0, 309, 166))
        self.drawingScrollAreaContents.setObjectName(_fromUtf8("drawingScrollAreaContents"))
        self.verticalLayout_2 = QtGui.QVBoxLayout(self.drawingScrollAreaContents)
        self.verticalLayout_2.setMargin(0)
        self.verticalLayout_2.setObjectName(_fromUtf8("verticalLayout_2"))
        self.sourceGroup = QtGui.QGroupBox(self.drawingScrollAreaContents)
        self.sourceGroup.setObjectName(_fromUtf8("sourceGroup"))
        self.gridLayout_5 = QtGui.QGridLayout(self.sourceGroup)
        self.gridLayout_5.setObjectName(_fromUtf8("gridLayout_5"))
        self.sourceWidget = SourceWidget(self.sourceGroup)
        self.sourceWidget.setObjectName(_fromUtf8("sourceWidget"))
        self.gridLayout_5.addWidget(self.sourceWidget, 0, 0, 1, 1)
        self.verticalLayout_2.addWidget(self.sourceGroup)
        self.tabWidget = QtGui.QTabWidget(self.drawingScrollAreaContents)
        sizePolicy = QtGui.QSizePolicy(QtGui.QSizePolicy.Expanding, QtGui.QSizePolicy.MinimumExpanding)
        sizePolicy.setHorizontalStretch(0)
        sizePolicy.setVerticalStretch(0)
        sizePolicy.setHeightForWidth(self.tabWidget.sizePolicy().hasHeightForWidth())
        self.tabWidget.setSizePolicy(sizePolicy)
        self.tabWidget.setObjectName(_fromUtf8("tabWidget"))
        self.planDrawingWidget = QtGui.QWidget()
        self.planDrawingWidget.setObjectName(_fromUtf8("planDrawingWidget"))
        self.gridLayout = QtGui.QGridLayout(self.planDrawingWidget)
        self.gridLayout.setObjectName(_fromUtf8("gridLayout"))
        self.planFeatureWidget = FeatureWidget(self.planDrawingWidget)
        self.planFeatureWidget.setObjectName(_fromUtf8("planFeatureWidget"))
        self.gridLayout.addWidget(self.planFeatureWidget, 0, 0, 1, 1)
        spacerItem = QtGui.QSpacerItem(58, 25, QtGui.QSizePolicy.Minimum, QtGui.QSizePolicy.Expanding)
        self.gridLayout.addItem(spacerItem, 1, 0, 1, 1)
        self.tabWidget.addTab(self.planDrawingWidget, _fromUtf8(""))
        self.sectionDrawingWidget = QtGui.QWidget()
        self.sectionDrawingWidget.setObjectName(_fromUtf8("sectionDrawingWidget"))
        self.gridLayout_2 = QtGui.QGridLayout(self.sectionDrawingWidget)
        self.gridLayout_2.setObjectName(_fromUtf8("gridLayout_2"))
        self.sectionFeatureWidget = FeatureWidget(self.sectionDrawingWidget)
        self.sectionFeatureWidget.setObjectName(_fromUtf8("sectionFeatureWidget"))
        self.gridLayout_2.addWidget(self.sectionFeatureWidget, 0, 0, 1, 1)
        spacerItem1 = QtGui.QSpacerItem(68, 25, QtGui.QSizePolicy.Minimum, QtGui.QSizePolicy.Expanding)
        self.gridLayout_2.addItem(spacerItem1, 1, 0, 1, 1)
        self.tabWidget.addTab(self.sectionDrawingWidget, _fromUtf8(""))
        self.siteDrawingWidget = QtGui.QWidget()
        self.siteDrawingWidget.setObjectName(_fromUtf8("siteDrawingWidget"))
        self.gridLayout_3 = QtGui.QGridLayout(self.siteDrawingWidget)
        self.gridLayout_3.setObjectName(_fromUtf8("gridLayout_3"))
        self.siteFeatureWidget = FeatureWidget(self.siteDrawingWidget)
        self.siteFeatureWidget.setObjectName(_fromUtf8("siteFeatureWidget"))
        self.gridLayout_3.addWidget(self.siteFeatureWidget, 0, 0, 1, 1)
        spacerItem2 = QtGui.QSpacerItem(88, 25, QtGui.QSizePolicy.Minimum, QtGui.QSizePolicy.Expanding)
        self.gridLayout_3.addItem(spacerItem2, 1, 0, 1, 1)
        self.tabWidget.addTab(self.siteDrawingWidget, _fromUtf8(""))
        self.verticalLayout_2.addWidget(self.tabWidget)
        self.drawingScrollArea.setWidget(self.drawingScrollAreaContents)
        self.gridLayout_4.addWidget(self.drawingScrollArea, 0, 0, 1, 1)
        self.horizontalLayout = QtGui.QHBoxLayout()
        self.horizontalLayout.setObjectName(_fromUtf8("horizontalLayout"))
        self.resetButton = QtGui.QPushButton(DrawingWidget)
        self.resetButton.setObjectName(_fromUtf8("resetButton"))
        self.horizontalLayout.addWidget(self.resetButton)
        self.mergeButton = QtGui.QPushButton(DrawingWidget)
        self.mergeButton.setObjectName(_fromUtf8("mergeButton"))
        self.horizontalLayout.addWidget(self.mergeButton)
        self.gridLayout_4.addLayout(self.horizontalLayout, 2, 0, 1, 1)
        spacerItem3 = QtGui.QSpacerItem(20, 40, QtGui.QSizePolicy.Minimum, QtGui.QSizePolicy.Expanding)
        self.gridLayout_4.addItem(spacerItem3, 1, 0, 1, 1)

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
