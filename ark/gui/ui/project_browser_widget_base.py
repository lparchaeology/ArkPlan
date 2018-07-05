# -*- coding: utf-8 -*-

# Form implementation generated from reading ui file 'ark/gui/ui/project_browser_widget_base.ui'
#
# Created by: PyQt4 UI code generator 4.12.1
#
# WARNING! All changes made in this file will be lost!

from qgis.PyQt import QtCore, QtGui

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

class Ui_ProjectBrowserWidget(object):
    def setupUi(self, ProjectBrowserWidget):
        ProjectBrowserWidget.setObjectName(_fromUtf8("ProjectBrowserWidget"))
        ProjectBrowserWidget.resize(399, 339)
        self.gridLayout = QtGui.QGridLayout(ProjectBrowserWidget)
        self.gridLayout.setObjectName(_fromUtf8("gridLayout"))
        self.projectLabel = QtGui.QLabel(ProjectBrowserWidget)
        self.projectLabel.setObjectName(_fromUtf8("projectLabel"))
        self.gridLayout.addWidget(self.projectLabel, 0, 0, 1, 1)
        self.projectCodeEdit = QtGui.QLineEdit(ProjectBrowserWidget)
        self.projectCodeEdit.setReadOnly(True)
        self.projectCodeEdit.setObjectName(_fromUtf8("projectCodeEdit"))
        self.gridLayout.addWidget(self.projectCodeEdit, 0, 1, 1, 1)
        self.projectNameLabel = QtGui.QLabel(ProjectBrowserWidget)
        self.projectNameLabel.setObjectName(_fromUtf8("projectNameLabel"))
        self.gridLayout.addWidget(self.projectNameLabel, 1, 0, 1, 1)
        self.siteCodeEdit = QtGui.QLineEdit(ProjectBrowserWidget)
        self.siteCodeEdit.setReadOnly(True)
        self.siteCodeEdit.setObjectName(_fromUtf8("siteCodeEdit"))
        self.gridLayout.addWidget(self.siteCodeEdit, 0, 2, 1, 1)
        self.projectNameEdit = QtGui.QLineEdit(ProjectBrowserWidget)
        self.projectNameEdit.setReadOnly(True)
        self.projectNameEdit.setObjectName(_fromUtf8("projectNameEdit"))
        self.gridLayout.addWidget(self.projectNameEdit, 1, 1, 1, 2)
        self.projectTreeView = ProjectTreeView(ProjectBrowserWidget)
        self.projectTreeView.setObjectName(_fromUtf8("projectTreeView"))
        self.gridLayout.addWidget(self.projectTreeView, 2, 0, 1, 3)

        self.retranslateUi(ProjectBrowserWidget)
        QtCore.QMetaObject.connectSlotsByName(ProjectBrowserWidget)

    def retranslateUi(self, ProjectBrowserWidget):
        ProjectBrowserWidget.setWindowTitle(_translate("ProjectBrowserWidget", "ProjectBrowserWidget", None))
        self.projectLabel.setText(_translate("ProjectBrowserWidget", "Project:", None))
        self.projectNameLabel.setText(_translate("ProjectBrowserWidget", "Name:", None))

from ..project_tree_view import ProjectTreeView
