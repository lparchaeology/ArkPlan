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
        DrawingWidget.resize(330, 125)
        self.contextsTab = QtGui.QWidget()
        self.contextsTab.setObjectName(_fromUtf8("contextsTab"))
        self.gridLayout = QtGui.QGridLayout(self.contextsTab)
        self.gridLayout.setContentsMargins(12, -1, 12, 12)
        self.gridLayout.setObjectName(_fromUtf8("gridLayout"))
        self.autoSchematiclLabel = QtGui.QLabel(self.contextsTab)
        self.autoSchematiclLabel.setObjectName(_fromUtf8("autoSchematiclLabel"))
        self.gridLayout.addWidget(self.autoSchematiclLabel, 1, 0, 1, 1)
        spacerItem = QtGui.QSpacerItem(20, 40, QtGui.QSizePolicy.Minimum, QtGui.QSizePolicy.Expanding)
        self.gridLayout.addItem(spacerItem, 2, 0, 1, 2)
        self.contextToolsLayout = QtGui.QGridLayout()
        self.contextToolsLayout.setObjectName(_fromUtf8("contextToolsLayout"))
        self.gridLayout.addLayout(self.contextToolsLayout, 0, 0, 1, 2)
        self.autoSchematicTool = QtGui.QToolButton(self.contextsTab)
        icon = QtGui.QIcon()
        icon.addPixmap(QtGui.QPixmap(_fromUtf8(":/plugins/ark/plan/autoSchematic.png")), QtGui.QIcon.Normal, QtGui.QIcon.Off)
        self.autoSchematicTool.setIcon(icon)
        self.autoSchematicTool.setObjectName(_fromUtf8("autoSchematicTool"))
        self.gridLayout.addWidget(self.autoSchematicTool, 1, 1, 1, 1)
        DrawingWidget.addTab(self.contextsTab, _fromUtf8(""))
        self.featuresTab = QtGui.QWidget()
        self.featuresTab.setObjectName(_fromUtf8("featuresTab"))
        self.gridLayout_2 = QtGui.QGridLayout(self.featuresTab)
        self.gridLayout_2.setContentsMargins(12, -1, 12, 12)
        self.gridLayout_2.setObjectName(_fromUtf8("gridLayout_2"))
        self.featureNameLabel = QtGui.QLabel(self.featuresTab)
        self.featureNameLabel.setObjectName(_fromUtf8("featureNameLabel"))
        self.gridLayout_2.addWidget(self.featureNameLabel, 0, 0, 1, 1)
        self.featureNameEdit = QtGui.QLineEdit(self.featuresTab)
        self.featureNameEdit.setObjectName(_fromUtf8("featureNameEdit"))
        self.gridLayout_2.addWidget(self.featureNameEdit, 0, 1, 1, 1)
        self.featureToolsLayout = QtGui.QGridLayout()
        self.featureToolsLayout.setObjectName(_fromUtf8("featureToolsLayout"))
        self.gridLayout_2.addLayout(self.featureToolsLayout, 1, 0, 1, 2)
        spacerItem1 = QtGui.QSpacerItem(118, 121, QtGui.QSizePolicy.Minimum, QtGui.QSizePolicy.Expanding)
        self.gridLayout_2.addItem(spacerItem1, 2, 0, 1, 2)
        DrawingWidget.addTab(self.featuresTab, _fromUtf8(""))
        self.sectionsTab = QtGui.QWidget()
        self.sectionsTab.setObjectName(_fromUtf8("sectionsTab"))
        self.gridLayout_3 = QtGui.QGridLayout(self.sectionsTab)
        self.gridLayout_3.setObjectName(_fromUtf8("gridLayout_3"))
        self.sectionLabel = QtGui.QLabel(self.sectionsTab)
        self.sectionLabel.setObjectName(_fromUtf8("sectionLabel"))
        self.gridLayout_3.addWidget(self.sectionLabel, 0, 0, 1, 1)
        self.sectionCombo = QtGui.QComboBox(self.sectionsTab)
        self.sectionCombo.setObjectName(_fromUtf8("sectionCombo"))
        self.gridLayout_3.addWidget(self.sectionCombo, 0, 1, 1, 1)
        self.sectionToolsLayout = QtGui.QGridLayout()
        self.sectionToolsLayout.setObjectName(_fromUtf8("sectionToolsLayout"))
        self.gridLayout_3.addLayout(self.sectionToolsLayout, 1, 0, 1, 2)
        spacerItem2 = QtGui.QSpacerItem(88, 134, QtGui.QSizePolicy.Minimum, QtGui.QSizePolicy.Expanding)
        self.gridLayout_3.addItem(spacerItem2, 2, 0, 1, 2)
        DrawingWidget.addTab(self.sectionsTab, _fromUtf8(""))
        self.featureNameLabel.setBuddy(self.featureNameEdit)

        self.retranslateUi(DrawingWidget)
        DrawingWidget.setCurrentIndex(0)
        QtCore.QMetaObject.connectSlotsByName(DrawingWidget)

    def retranslateUi(self, DrawingWidget):
        DrawingWidget.setWindowTitle(_translate("DrawingWidget", "TabWidget", None))
        self.autoSchematiclLabel.setText(_translate("DrawingWidget", "Auto Schematic:", None))
        self.autoSchematicTool.setToolTip(_translate("DrawingWidget", "<html><head/><body><p>Auto Schematic</p></body></html>", None))
        self.autoSchematicTool.setText(_translate("DrawingWidget", "...", None))
        DrawingWidget.setTabText(DrawingWidget.indexOf(self.contextsTab), _translate("DrawingWidget", "Contexts", None))
        self.featureNameLabel.setText(_translate("DrawingWidget", "Name:", None))
        DrawingWidget.setTabText(DrawingWidget.indexOf(self.featuresTab), _translate("DrawingWidget", "Features", None))
        self.sectionLabel.setText(_translate("DrawingWidget", "Section:", None))
        DrawingWidget.setTabText(DrawingWidget.indexOf(self.sectionsTab), _translate("DrawingWidget", "Sections", None))

import resources
