# -*- coding: utf-8 -*-

# Form implementation generated from reading ui file 'ark/gui/ui/project_dialog_base.ui'
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

class Ui_ProjectDialog(object):
    def setupUi(self, ProjectDialog):
        ProjectDialog.setObjectName(_fromUtf8("ProjectDialog"))
        ProjectDialog.resize(485, 390)
        self.verticalLayout = QtGui.QVBoxLayout(ProjectDialog)
        self.verticalLayout.setObjectName(_fromUtf8("verticalLayout"))
        self.tabWidget = QtGui.QTabWidget(ProjectDialog)
        self.tabWidget.setTabPosition(QtGui.QTabWidget.West)
        self.tabWidget.setTabShape(QtGui.QTabWidget.Rounded)
        self.tabWidget.setObjectName(_fromUtf8("tabWidget"))
        self.projectTab = ProjectWidget()
        self.projectTab.setObjectName(_fromUtf8("projectTab"))
        self.tabWidget.addTab(self.projectTab, _fromUtf8(""))
        self.baseMapTab = BaseMapWidget()
        self.baseMapTab.setObjectName(_fromUtf8("baseMapTab"))
        self.tabWidget.addTab(self.baseMapTab, _fromUtf8(""))
        self.figureTab = FigureWidget()
        self.figureTab.setObjectName(_fromUtf8("figureTab"))
        self.tabWidget.addTab(self.figureTab, _fromUtf8(""))
        self.verticalLayout.addWidget(self.tabWidget)

        self.retranslateUi(ProjectDialog)
        self.tabWidget.setCurrentIndex(0)
        QtCore.QMetaObject.connectSlotsByName(ProjectDialog)

    def retranslateUi(self, ProjectDialog):
        ProjectDialog.setWindowTitle(_translate("ProjectDialog", "Dialog", None))
        self.tabWidget.setTabText(self.tabWidget.indexOf(self.projectTab), _translate("ProjectDialog", "Project", None))
        self.tabWidget.setTabText(self.tabWidget.indexOf(self.baseMapTab), _translate("ProjectDialog", "Base Map", None))
        self.tabWidget.setTabText(self.tabWidget.indexOf(self.figureTab), _translate("ProjectDialog", "Figures", None))

from ..base_map_widget import BaseMapWidget
from ..figure_widget import FigureWidget
from ..project_widget import ProjectWidget
