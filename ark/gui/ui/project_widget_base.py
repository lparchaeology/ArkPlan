# -*- coding: utf-8 -*-

# Form implementation generated from reading ui file 'ark/gui/ui/project_widget_base.ui'
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

class Ui_ProjectWidget(object):
    def setupUi(self, ProjectWidget):
        ProjectWidget.setObjectName(_fromUtf8("ProjectWidget"))
        ProjectWidget.resize(389, 180)
        self.gridLayout = QtGui.QGridLayout(ProjectWidget)
        self.gridLayout.setObjectName(_fromUtf8("gridLayout"))
        self.projectCodeCombo = QtGui.QComboBox(ProjectWidget)
        self.projectCodeCombo.setEditable(True)
        self.projectCodeCombo.setMaxVisibleItems(1)
        self.projectCodeCombo.setMaxCount(1)
        self.projectCodeCombo.setObjectName(_fromUtf8("projectCodeCombo"))
        self.gridLayout.addWidget(self.projectCodeCombo, 0, 1, 1, 2)
        self.siteCodeLabel = QtGui.QLabel(ProjectWidget)
        self.siteCodeLabel.setAlignment(QtCore.Qt.AlignJustify|QtCore.Qt.AlignVCenter)
        self.siteCodeLabel.setWordWrap(True)
        self.siteCodeLabel.setObjectName(_fromUtf8("siteCodeLabel"))
        self.gridLayout.addWidget(self.siteCodeLabel, 2, 0, 1, 1)
        self.locationLabel = QtGui.QLabel(ProjectWidget)
        self.locationLabel.setObjectName(_fromUtf8("locationLabel"))
        self.gridLayout.addWidget(self.locationLabel, 3, 0, 1, 1)
        self.locationEastingEdit = QtGui.QLineEdit(ProjectWidget)
        self.locationEastingEdit.setObjectName(_fromUtf8("locationEastingEdit"))
        self.gridLayout.addWidget(self.locationEastingEdit, 3, 1, 1, 1)
        self.projectNameLabel = QtGui.QLabel(ProjectWidget)
        self.projectNameLabel.setObjectName(_fromUtf8("projectNameLabel"))
        self.gridLayout.addWidget(self.projectNameLabel, 1, 0, 1, 1)
        self.siteCodeEdit = QtGui.QLineEdit(ProjectWidget)
        self.siteCodeEdit.setObjectName(_fromUtf8("siteCodeEdit"))
        self.gridLayout.addWidget(self.siteCodeEdit, 2, 1, 1, 2)
        self.projectCodeLabel = QtGui.QLabel(ProjectWidget)
        self.projectCodeLabel.setObjectName(_fromUtf8("projectCodeLabel"))
        self.gridLayout.addWidget(self.projectCodeLabel, 0, 0, 1, 1)
        self.locationNorthingEdit = QtGui.QLineEdit(ProjectWidget)
        self.locationNorthingEdit.setObjectName(_fromUtf8("locationNorthingEdit"))
        self.gridLayout.addWidget(self.locationNorthingEdit, 3, 2, 1, 1)
        self.projectNameEdit = QtGui.QLineEdit(ProjectWidget)
        self.projectNameEdit.setEnabled(True)
        self.projectNameEdit.setObjectName(_fromUtf8("projectNameEdit"))
        self.gridLayout.addWidget(self.projectNameEdit, 1, 1, 1, 2)
        spacerItem = QtGui.QSpacerItem(20, 40, QtGui.QSizePolicy.Minimum, QtGui.QSizePolicy.Expanding)
        self.gridLayout.addItem(spacerItem, 4, 0, 1, 3)
        self.siteCodeLabel.setBuddy(self.siteCodeEdit)
        self.locationLabel.setBuddy(self.locationEastingEdit)
        self.projectNameLabel.setBuddy(self.projectNameEdit)
        self.projectCodeLabel.setBuddy(self.projectCodeCombo)

        self.retranslateUi(ProjectWidget)
        QtCore.QMetaObject.connectSlotsByName(ProjectWidget)
        ProjectWidget.setTabOrder(self.projectCodeCombo, self.projectNameEdit)
        ProjectWidget.setTabOrder(self.projectNameEdit, self.siteCodeEdit)
        ProjectWidget.setTabOrder(self.siteCodeEdit, self.locationEastingEdit)
        ProjectWidget.setTabOrder(self.locationEastingEdit, self.locationNorthingEdit)

    def retranslateUi(self, ProjectWidget):
        ProjectWidget.setWindowTitle(_translate("ProjectWidget", "ProjectWidget", None))
        self.siteCodeLabel.setText(_translate("ProjectWidget", "Site Code:", None))
        self.locationLabel.setText(_translate("ProjectWidget", "Location:", None))
        self.locationEastingEdit.setPlaceholderText(_translate("ProjectWidget", "Easting", None))
        self.projectNameLabel.setText(_translate("ProjectWidget", "Project Name:", None))
        self.projectCodeLabel.setText(_translate("ProjectWidget", "Project Code:", None))
        self.locationNorthingEdit.setPlaceholderText(_translate("ProjectWidget", "Northing", None))

