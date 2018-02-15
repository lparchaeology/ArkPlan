# -*- coding: utf-8 -*-

# Form implementation generated from reading ui file 'ark/gui/ui/preferences_widget_base.ui'
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

class Ui_Form(object):
    def setupUi(self, Form):
        Form.setObjectName(_fromUtf8("Form"))
        Form.resize(635, 173)
        self.gridLayout = QtGui.QGridLayout(Form)
        self.gridLayout.setObjectName(_fromUtf8("gridLayout"))
        self.projectsFolderLabel = QtGui.QLabel(Form)
        self.projectsFolderLabel.setObjectName(_fromUtf8("projectsFolderLabel"))
        self.gridLayout.addWidget(self.projectsFolderLabel, 0, 0, 1, 1)
        self.projectsFolderEdit = QtGui.QLineEdit(Form)
        self.projectsFolderEdit.setObjectName(_fromUtf8("projectsFolderEdit"))
        self.gridLayout.addWidget(self.projectsFolderEdit, 0, 1, 1, 1)
        self.projectsFolderButton = QtGui.QToolButton(Form)
        icon = QtGui.QIcon()
        icon.addPixmap(QtGui.QPixmap(_fromUtf8(":/plugins/ark/folder.png")), QtGui.QIcon.Normal, QtGui.QIcon.Off)
        self.projectsFolderButton.setIcon(icon)
        self.projectsFolderButton.setObjectName(_fromUtf8("projectsFolderButton"))
        self.gridLayout.addWidget(self.projectsFolderButton, 0, 2, 1, 1)
        self.userFullNameLabel = QtGui.QLabel(Form)
        self.userFullNameLabel.setObjectName(_fromUtf8("userFullNameLabel"))
        self.gridLayout.addWidget(self.userFullNameLabel, 1, 0, 1, 1)
        self.userFullNameEdit = QtGui.QLineEdit(Form)
        self.userFullNameEdit.setObjectName(_fromUtf8("userFullNameEdit"))
        self.gridLayout.addWidget(self.userFullNameEdit, 1, 1, 1, 2)
        self.userInitialsLabel = QtGui.QLabel(Form)
        self.userInitialsLabel.setObjectName(_fromUtf8("userInitialsLabel"))
        self.gridLayout.addWidget(self.userInitialsLabel, 2, 0, 1, 1)
        self.userInitialsEdit = QtGui.QLineEdit(Form)
        self.userInitialsEdit.setObjectName(_fromUtf8("userInitialsEdit"))
        self.gridLayout.addWidget(self.userInitialsEdit, 2, 1, 1, 2)
        self.organisationLabel = QtGui.QLabel(Form)
        self.organisationLabel.setObjectName(_fromUtf8("organisationLabel"))
        self.gridLayout.addWidget(self.organisationLabel, 3, 0, 1, 1)
        self.organisationEdit = QtGui.QLineEdit(Form)
        self.organisationEdit.setObjectName(_fromUtf8("organisationEdit"))
        self.gridLayout.addWidget(self.organisationEdit, 3, 1, 1, 2)
        spacerItem = QtGui.QSpacerItem(608, 17, QtGui.QSizePolicy.Minimum, QtGui.QSizePolicy.Expanding)
        self.gridLayout.addItem(spacerItem, 4, 0, 1, 3)
        self.projectsFolderLabel.setBuddy(self.projectsFolderEdit)
        self.userFullNameLabel.setBuddy(self.userFullNameEdit)
        self.userInitialsLabel.setBuddy(self.userInitialsEdit)

        self.retranslateUi(Form)
        QtCore.QMetaObject.connectSlotsByName(Form)

    def retranslateUi(self, Form):
        Form.setWindowTitle(_translate("Form", "Form", None))
        self.projectsFolderLabel.setText(_translate("Form", "Projects Folder:", None))
        self.projectsFolderEdit.setPlaceholderText(_translate("Form", "/Disk/Data/Projects", None))
        self.userFullNameLabel.setText(_translate("Form", "Full Name:", None))
        self.userFullNameEdit.setPlaceholderText(_translate("Form", "Dorothy Garrod", None))
        self.userInitialsLabel.setText(_translate("Form", "Initials:", None))
        self.userInitialsEdit.setPlaceholderText(_translate("Form", "DG", None))
        self.organisationLabel.setText(_translate("Form", "Organisation:", None))
        self.organisationEdit.setPlaceholderText(_translate("Form", "Disney Professor of Archaeology, University of Cambridge", None))

