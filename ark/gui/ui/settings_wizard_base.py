# -*- coding: utf-8 -*-

# Form implementation generated from reading ui file 'ark/gui/ui/settings_wizard_base.ui'
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

class Ui_SettingsWizard(object):
    def setupUi(self, SettingsWizard):
        SettingsWizard.setObjectName(_fromUtf8("SettingsWizard"))
        SettingsWizard.resize(655, 519)
        SettingsWizard.setOptions(QtGui.QWizard.CancelButtonOnLeft|QtGui.QWizard.NoBackButtonOnStartPage|QtGui.QWizard.NoDefaultButton)
        self.serverPage = ServerPage()
        self.serverPage.setObjectName(_fromUtf8("serverPage"))
        self.serverLayout = QtGui.QGridLayout(self.serverPage)
        self.serverLayout.setObjectName(_fromUtf8("serverLayout"))
        self.arkUrlLabel = QtGui.QLabel(self.serverPage)
        self.arkUrlLabel.setAlignment(QtCore.Qt.AlignJustify|QtCore.Qt.AlignVCenter)
        self.arkUrlLabel.setWordWrap(True)
        self.arkUrlLabel.setObjectName(_fromUtf8("arkUrlLabel"))
        self.serverLayout.addWidget(self.arkUrlLabel, 1, 0, 1, 1)
        self.arkUserIdLabel = QtGui.QLabel(self.serverPage)
        self.arkUserIdLabel.setObjectName(_fromUtf8("arkUserIdLabel"))
        self.serverLayout.addWidget(self.arkUserIdLabel, 2, 0, 1, 2)
        self.arkUserIdEdit = QtGui.QLineEdit(self.serverPage)
        self.arkUserIdEdit.setObjectName(_fromUtf8("arkUserIdEdit"))
        self.serverLayout.addWidget(self.arkUserIdEdit, 2, 2, 1, 1)
        self.arkPasswordLabel = QtGui.QLabel(self.serverPage)
        self.arkPasswordLabel.setObjectName(_fromUtf8("arkPasswordLabel"))
        self.serverLayout.addWidget(self.arkPasswordLabel, 3, 0, 1, 2)
        self.arkPasswordEdit = QtGui.QLineEdit(self.serverPage)
        self.arkPasswordEdit.setText(_fromUtf8(""))
        self.arkPasswordEdit.setEchoMode(QtGui.QLineEdit.Password)
        self.arkPasswordEdit.setObjectName(_fromUtf8("arkPasswordEdit"))
        self.serverLayout.addWidget(self.arkPasswordEdit, 3, 2, 1, 1)
        self.arkUrlEdit = QtGui.QLineEdit(self.serverPage)
        self.arkUrlEdit.setEnabled(True)
        self.arkUrlEdit.setObjectName(_fromUtf8("arkUrlEdit"))
        self.serverLayout.addWidget(self.arkUrlEdit, 1, 2, 1, 1)
        self.arkLabel = QtGui.QLabel(self.serverPage)
        self.arkLabel.setAlignment(QtCore.Qt.AlignJustify|QtCore.Qt.AlignVCenter)
        self.arkLabel.setWordWrap(True)
        self.arkLabel.setObjectName(_fromUtf8("arkLabel"))
        self.serverLayout.addWidget(self.arkLabel, 0, 0, 1, 3)
        SettingsWizard.addPage(self.serverPage)
        self.projectPage = ProjectPage()
        self.projectPage.setObjectName(_fromUtf8("projectPage"))
        self.projectLayout = QtGui.QGridLayout(self.projectPage)
        self.projectLayout.setObjectName(_fromUtf8("projectLayout"))
        self.projectLabel = QtGui.QLabel(self.projectPage)
        self.projectLabel.setAlignment(QtCore.Qt.AlignJustify|QtCore.Qt.AlignVCenter)
        self.projectLabel.setWordWrap(True)
        self.projectLabel.setObjectName(_fromUtf8("projectLabel"))
        self.projectLayout.addWidget(self.projectLabel, 0, 0, 1, 5)
        self.projectCodeLabel = QtGui.QLabel(self.projectPage)
        self.projectCodeLabel.setObjectName(_fromUtf8("projectCodeLabel"))
        self.projectLayout.addWidget(self.projectCodeLabel, 1, 0, 1, 1)
        self.projectNameLabel = QtGui.QLabel(self.projectPage)
        self.projectNameLabel.setObjectName(_fromUtf8("projectNameLabel"))
        self.projectLayout.addWidget(self.projectNameLabel, 2, 0, 1, 2)
        self.projectNameEdit = QtGui.QLineEdit(self.projectPage)
        self.projectNameEdit.setObjectName(_fromUtf8("projectNameEdit"))
        self.projectLayout.addWidget(self.projectNameEdit, 2, 2, 1, 3)
        self.siteCodesLabel = QtGui.QLabel(self.projectPage)
        self.siteCodesLabel.setAlignment(QtCore.Qt.AlignJustify|QtCore.Qt.AlignVCenter)
        self.siteCodesLabel.setWordWrap(True)
        self.siteCodesLabel.setObjectName(_fromUtf8("siteCodesLabel"))
        self.projectLayout.addWidget(self.siteCodesLabel, 3, 0, 1, 1)
        self.siteCodesEdit = QtGui.QLineEdit(self.projectPage)
        self.siteCodesEdit.setObjectName(_fromUtf8("siteCodesEdit"))
        self.projectLayout.addWidget(self.siteCodesEdit, 3, 2, 1, 3)
        self.locationLabel = QtGui.QLabel(self.projectPage)
        self.locationLabel.setObjectName(_fromUtf8("locationLabel"))
        self.projectLayout.addWidget(self.locationLabel, 4, 0, 1, 1)
        self.locationEastingEdit = QtGui.QLineEdit(self.projectPage)
        self.locationEastingEdit.setObjectName(_fromUtf8("locationEastingEdit"))
        self.projectLayout.addWidget(self.locationEastingEdit, 4, 2, 1, 1)
        self.locationNorthingEdit = QtGui.QLineEdit(self.projectPage)
        self.locationNorthingEdit.setObjectName(_fromUtf8("locationNorthingEdit"))
        self.projectLayout.addWidget(self.locationNorthingEdit, 4, 3, 1, 1)
        self.crsLabel = QtGui.QLabel(self.projectPage)
        self.crsLabel.setObjectName(_fromUtf8("crsLabel"))
        self.projectLayout.addWidget(self.crsLabel, 5, 0, 1, 1)
        self.crsButton = QtGui.QToolButton(self.projectPage)
        self.crsButton.setObjectName(_fromUtf8("crsButton"))
        self.projectLayout.addWidget(self.crsButton, 5, 4, 1, 1)
        self.crsEdit = QtGui.QLineEdit(self.projectPage)
        self.crsEdit.setReadOnly(True)
        self.crsEdit.setObjectName(_fromUtf8("crsEdit"))
        self.projectLayout.addWidget(self.crsEdit, 5, 2, 1, 2)
        self.projectCodeCombo = QtGui.QComboBox(self.projectPage)
        self.projectCodeCombo.setEditable(True)
        self.projectCodeCombo.setInsertPolicy(QtGui.QComboBox.InsertAtTop)
        self.projectCodeCombo.setObjectName(_fromUtf8("projectCodeCombo"))
        self.projectLayout.addWidget(self.projectCodeCombo, 1, 2, 1, 3)
        SettingsWizard.addPage(self.projectPage)
        self.userPage = UserPage()
        self.userPage.setObjectName(_fromUtf8("userPage"))
        self.userLayout = QtGui.QGridLayout(self.userPage)
        self.userLayout.setObjectName(_fromUtf8("userLayout"))
        self.userFullnameLabel = QtGui.QLabel(self.userPage)
        self.userFullnameLabel.setObjectName(_fromUtf8("userFullnameLabel"))
        self.userLayout.addWidget(self.userFullnameLabel, 1, 0, 1, 1)
        self.userInitialsEdit = QtGui.QLineEdit(self.userPage)
        self.userInitialsEdit.setObjectName(_fromUtf8("userInitialsEdit"))
        self.userLayout.addWidget(self.userInitialsEdit, 2, 1, 1, 1)
        self.userInitialsLabel = QtGui.QLabel(self.userPage)
        self.userInitialsLabel.setObjectName(_fromUtf8("userInitialsLabel"))
        self.userLayout.addWidget(self.userInitialsLabel, 2, 0, 1, 1)
        self.userFullnameEdit = QtGui.QLineEdit(self.userPage)
        self.userFullnameEdit.setObjectName(_fromUtf8("userFullnameEdit"))
        self.userLayout.addWidget(self.userFullnameEdit, 1, 1, 1, 1)
        self.label = QtGui.QLabel(self.userPage)
        self.label.setObjectName(_fromUtf8("label"))
        self.userLayout.addWidget(self.label, 0, 0, 1, 2)
        SettingsWizard.addPage(self.userPage)
        self.confirmPage = ConfirmPage()
        self.confirmPage.setObjectName(_fromUtf8("confirmPage"))
        self.confirmLayout = QtGui.QGridLayout(self.confirmPage)
        self.confirmLayout.setObjectName(_fromUtf8("confirmLayout"))
        self.projectFileLabel_2 = QtGui.QLabel(self.confirmPage)
        self.projectFileLabel_2.setAlignment(QtCore.Qt.AlignJustify|QtCore.Qt.AlignVCenter)
        self.projectFileLabel_2.setWordWrap(True)
        self.projectFileLabel_2.setObjectName(_fromUtf8("projectFileLabel_2"))
        self.confirmLayout.addWidget(self.projectFileLabel_2, 1, 0, 1, 1)
        self.projectFileEdit = QtGui.QLineEdit(self.confirmPage)
        self.projectFileEdit.setObjectName(_fromUtf8("projectFileEdit"))
        self.confirmLayout.addWidget(self.projectFileEdit, 2, 1, 1, 2)
        self.confirmLabel = QtGui.QLabel(self.confirmPage)
        self.confirmLabel.setWordWrap(True)
        self.confirmLabel.setObjectName(_fromUtf8("confirmLabel"))
        self.confirmLayout.addWidget(self.confirmLabel, 3, 0, 1, 3)
        self.folderLabel = QtGui.QLabel(self.confirmPage)
        self.folderLabel.setAlignment(QtCore.Qt.AlignJustify|QtCore.Qt.AlignVCenter)
        self.folderLabel.setWordWrap(True)
        self.folderLabel.setObjectName(_fromUtf8("folderLabel"))
        self.confirmLayout.addWidget(self.folderLabel, 0, 0, 1, 3)
        self.projectFolderLayout = QtGui.QHBoxLayout()
        self.projectFolderLayout.setObjectName(_fromUtf8("projectFolderLayout"))
        self.projectFolderEdit = QtGui.QLineEdit(self.confirmPage)
        self.projectFolderEdit.setObjectName(_fromUtf8("projectFolderEdit"))
        self.projectFolderLayout.addWidget(self.projectFolderEdit)
        self.projectFolderButton = QtGui.QToolButton(self.confirmPage)
        icon = QtGui.QIcon()
        icon.addPixmap(QtGui.QPixmap(_fromUtf8(":/plugins/ark/folder.png")), QtGui.QIcon.Normal, QtGui.QIcon.Off)
        self.projectFolderButton.setIcon(icon)
        self.projectFolderButton.setObjectName(_fromUtf8("projectFolderButton"))
        self.projectFolderLayout.addWidget(self.projectFolderButton)
        self.confirmLayout.addLayout(self.projectFolderLayout, 1, 1, 1, 2)
        self.projectFileLabel = QtGui.QLabel(self.confirmPage)
        self.projectFileLabel.setAlignment(QtCore.Qt.AlignJustify|QtCore.Qt.AlignVCenter)
        self.projectFileLabel.setWordWrap(True)
        self.projectFileLabel.setObjectName(_fromUtf8("projectFileLabel"))
        self.confirmLayout.addWidget(self.projectFileLabel, 2, 0, 1, 1)
        spacerItem = QtGui.QSpacerItem(20, 40, QtGui.QSizePolicy.Minimum, QtGui.QSizePolicy.Expanding)
        self.confirmLayout.addItem(spacerItem, 4, 2, 1, 1)
        SettingsWizard.addPage(self.confirmPage)
        self.projectNameLabel.setBuddy(self.projectNameEdit)
        self.siteCodesLabel.setBuddy(self.siteCodesEdit)
        self.userFullnameLabel.setBuddy(self.userFullnameEdit)
        self.userInitialsLabel.setBuddy(self.userInitialsEdit)
        self.projectFileLabel_2.setBuddy(self.projectFileEdit)
        self.folderLabel.setBuddy(self.projectFolderEdit)
        self.projectFileLabel.setBuddy(self.projectFileEdit)

        self.retranslateUi(SettingsWizard)
        QtCore.QMetaObject.connectSlotsByName(SettingsWizard)

    def retranslateUi(self, SettingsWizard):
        SettingsWizard.setWindowTitle(_translate("SettingsWizard", "ARK Spatial - Settings Wizard", None))
        self.serverPage.setTitle(_translate("SettingsWizard", "ARK Project Wizard", None))
        self.serverPage.setSubTitle(_translate("SettingsWizard", "This wizard will walk you through setting up a new or existing ARK Spatial project.", None))
        self.arkUrlLabel.setText(_translate("SettingsWizard", "ARK URL (optional):", None))
        self.arkUserIdLabel.setText(_translate("SettingsWizard", "User ID (optional):", None))
        self.arkUserIdEdit.setPlaceholderText(_translate("SettingsWizard", "dgarrod", None))
        self.arkPasswordLabel.setText(_translate("SettingsWizard", "Password (optional):", None))
        self.arkPasswordEdit.setPlaceholderText(_translate("SettingsWizard", "********", None))
        self.arkUrlEdit.setPlaceholderText(_translate("SettingsWizard", "http://www.arch.cam.ac.uk/shuqba", None))
        self.arkLabel.setText(_translate("SettingsWizard", "If you use an ARK database for project management or site recording, enter the server details to enable automatic population of your project details.", None))
        self.projectPage.setTitle(_translate("SettingsWizard", "Project Details", None))
        self.projectPage.setSubTitle(_translate("SettingsWizard", "Enter the details for the Project.", None))
        self.projectLabel.setText(_translate("SettingsWizard", "You must enter at least a Project Code and Name. If no Site Code is entered, the Project Code is used instead. If multiple Site Codes are entered then the first Site Code will be used as the default Site Code.", None))
        self.projectCodeLabel.setText(_translate("SettingsWizard", "Project Code:", None))
        self.projectNameLabel.setText(_translate("SettingsWizard", "Project Name:", None))
        self.projectNameEdit.setPlaceholderText(_translate("SettingsWizard", "Shuqba Cave, Wadi an-Natuf", None))
        self.siteCodesLabel.setText(_translate("SettingsWizard", "Site Code(s):", None))
        self.siteCodesEdit.setPlaceholderText(_translate("SettingsWizard", "SHU28", None))
        self.locationLabel.setText(_translate("SettingsWizard", "Location:", None))
        self.locationEastingEdit.setPlaceholderText(_translate("SettingsWizard", "Easting", None))
        self.locationNorthingEdit.setPlaceholderText(_translate("SettingsWizard", "Northing", None))
        self.crsLabel.setText(_translate("SettingsWizard", "CRS:", None))
        self.crsButton.setText(_translate("SettingsWizard", "...", None))
        self.crsEdit.setPlaceholderText(_translate("SettingsWizard", "CRS", None))
        self.userPage.setTitle(_translate("SettingsWizard", "User Details", None))
        self.userPage.setSubTitle(_translate("SettingsWizard", "Enter your user details.", None))
        self.userFullnameLabel.setText(_translate("SettingsWizard", "Full Name:", None))
        self.userInitialsEdit.setPlaceholderText(_translate("SettingsWizard", "DG", None))
        self.userInitialsLabel.setText(_translate("SettingsWizard", "Initials:", None))
        self.userFullnameEdit.setPlaceholderText(_translate("SettingsWizard", "Dorothy Garrod", None))
        self.label.setText(_translate("SettingsWizard", "Enter your name and initials to be recorded as metadata on edits that you make.", None))
        self.confirmPage.setTitle(_translate("SettingsWizard", "Create Project", None))
        self.confirmPage.setSubTitle(_translate("SettingsWizard", "Confirm your project file details.", None))
        self.projectFileLabel_2.setText(_translate("SettingsWizard", "Project Folder:", None))
        self.projectFileEdit.setPlaceholderText(_translate("SettingsWizard", "SHU28_DG", None))
        self.confirmLabel.setText(_translate("SettingsWizard", "Click on the Done button to create your project. All required folders and files will be created. No existing data files will be overwritten.\n"
"\n"
"Once the project is created you can modify these settings or configure more settings in the Settings Dialog.", None))
        self.folderLabel.setText(_translate("SettingsWizard", "You can choose to save the project details in the currently open project, or to save the project in a new project file.\n"
"\n"
"This folder is usually something like \"Projects/TST01\" where TST01 is the Project or Site Code. The folder will be created if it does not already exist.\n"
"\n"
"ARK Spatial will automatically organise the data under this folder.\n"
"", None))
        self.projectFolderEdit.setPlaceholderText(_translate("SettingsWizard", "Projects/TST01", None))
        self.projectFileLabel.setText(_translate("SettingsWizard", "Project Filename:", None))

from ..settings_wizard_page import ConfirmPage, ProjectPage, ServerPage, UserPage
