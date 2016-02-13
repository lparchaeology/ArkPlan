# -*- coding: utf-8 -*-

# Form implementation generated from reading ui file 'src/settings_wizard_base.ui'
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

class Ui_SettingsWizard(object):
    def setupUi(self, SettingsWizard):
        SettingsWizard.setObjectName(_fromUtf8("SettingsWizard"))
        SettingsWizard.resize(686, 357)
        SettingsWizard.setOptions(QtGui.QWizard.CancelButtonOnLeft|QtGui.QWizard.NoBackButtonOnLastPage|QtGui.QWizard.NoBackButtonOnStartPage|QtGui.QWizard.NoDefaultButton)
        self.welcomePage = QtGui.QWizardPage()
        self.welcomePage.setObjectName(_fromUtf8("welcomePage"))
        self.gridLayout = QtGui.QGridLayout(self.welcomePage)
        self.gridLayout.setObjectName(_fromUtf8("gridLayout"))
        self.advancedButton = QtGui.QPushButton(self.welcomePage)
        self.advancedButton.setObjectName(_fromUtf8("advancedButton"))
        self.gridLayout.addWidget(self.advancedButton, 1, 1, 1, 1)
        spacerItem = QtGui.QSpacerItem(40, 20, QtGui.QSizePolicy.Expanding, QtGui.QSizePolicy.Minimum)
        self.gridLayout.addItem(spacerItem, 1, 0, 1, 1)
        self.advancedLabel = QtGui.QLabel(self.welcomePage)
        self.advancedLabel.setAlignment(QtCore.Qt.AlignJustify|QtCore.Qt.AlignVCenter)
        self.advancedLabel.setWordWrap(True)
        self.advancedLabel.setObjectName(_fromUtf8("advancedLabel"))
        self.gridLayout.addWidget(self.advancedLabel, 0, 0, 1, 2)
        SettingsWizard.addPage(self.welcomePage)
        self.folderPage = QtGui.QWizardPage()
        self.folderPage.setObjectName(_fromUtf8("folderPage"))
        self.gridLayout_2 = QtGui.QGridLayout(self.folderPage)
        self.gridLayout_2.setObjectName(_fromUtf8("gridLayout_2"))
        self.folderLabel = QtGui.QLabel(self.folderPage)
        self.folderLabel.setAlignment(QtCore.Qt.AlignJustify|QtCore.Qt.AlignVCenter)
        self.folderLabel.setWordWrap(True)
        self.folderLabel.setObjectName(_fromUtf8("folderLabel"))
        self.gridLayout_2.addWidget(self.folderLabel, 0, 0, 1, 1)
        self.projectFolderLayout = QtGui.QHBoxLayout()
        self.projectFolderLayout.setObjectName(_fromUtf8("projectFolderLayout"))
        self.projectFolderEdit = QtGui.QLineEdit(self.folderPage)
        self.projectFolderEdit.setObjectName(_fromUtf8("projectFolderEdit"))
        self.projectFolderLayout.addWidget(self.projectFolderEdit)
        self.projectFolderButton = QtGui.QToolButton(self.folderPage)
        icon = QtGui.QIcon()
        icon.addPixmap(QtGui.QPixmap(_fromUtf8(":/plugins/ark/folder.png")), QtGui.QIcon.Normal, QtGui.QIcon.Off)
        self.projectFolderButton.setIcon(icon)
        self.projectFolderButton.setObjectName(_fromUtf8("projectFolderButton"))
        self.projectFolderLayout.addWidget(self.projectFolderButton)
        self.gridLayout_2.addLayout(self.projectFolderLayout, 1, 0, 1, 1)
        SettingsWizard.addPage(self.folderPage)
        self.siteCodePage = QtGui.QWizardPage()
        self.siteCodePage.setObjectName(_fromUtf8("siteCodePage"))
        self.gridLayout_3 = QtGui.QGridLayout(self.siteCodePage)
        self.gridLayout_3.setObjectName(_fromUtf8("gridLayout_3"))
        self.siteCodeEdit = QtGui.QLineEdit(self.siteCodePage)
        self.siteCodeEdit.setObjectName(_fromUtf8("siteCodeEdit"))
        self.gridLayout_3.addWidget(self.siteCodeEdit, 3, 0, 1, 2)
        self.siteCodeLabel = QtGui.QLabel(self.siteCodePage)
        self.siteCodeLabel.setAlignment(QtCore.Qt.AlignJustify|QtCore.Qt.AlignVCenter)
        self.siteCodeLabel.setWordWrap(True)
        self.siteCodeLabel.setObjectName(_fromUtf8("siteCodeLabel"))
        self.gridLayout_3.addWidget(self.siteCodeLabel, 2, 0, 1, 2)
        self.multiSiteLabel = QtGui.QLabel(self.siteCodePage)
        self.multiSiteLabel.setAlignment(QtCore.Qt.AlignJustify|QtCore.Qt.AlignVCenter)
        self.multiSiteLabel.setWordWrap(True)
        self.multiSiteLabel.setObjectName(_fromUtf8("multiSiteLabel"))
        self.gridLayout_3.addWidget(self.multiSiteLabel, 0, 0, 1, 2)
        self.multiSiteCheck = QtGui.QCheckBox(self.siteCodePage)
        self.multiSiteCheck.setText(_fromUtf8(""))
        self.multiSiteCheck.setObjectName(_fromUtf8("multiSiteCheck"))
        self.gridLayout_3.addWidget(self.multiSiteCheck, 1, 0, 1, 2)
        SettingsWizard.addPage(self.siteCodePage)
        self.arkPage = QtGui.QWizardPage()
        self.arkPage.setObjectName(_fromUtf8("arkPage"))
        self.gridLayout_5 = QtGui.QGridLayout(self.arkPage)
        self.gridLayout_5.setObjectName(_fromUtf8("gridLayout_5"))
        self.useArkCheck = QtGui.QCheckBox(self.arkPage)
        self.useArkCheck.setText(_fromUtf8(""))
        self.useArkCheck.setChecked(True)
        self.useArkCheck.setObjectName(_fromUtf8("useArkCheck"))
        self.gridLayout_5.addWidget(self.useArkCheck, 1, 0, 1, 1)
        self.arkUrlLabel = QtGui.QLabel(self.arkPage)
        self.arkUrlLabel.setAlignment(QtCore.Qt.AlignJustify|QtCore.Qt.AlignVCenter)
        self.arkUrlLabel.setWordWrap(True)
        self.arkUrlLabel.setObjectName(_fromUtf8("arkUrlLabel"))
        self.gridLayout_5.addWidget(self.arkUrlLabel, 2, 0, 1, 1)
        self.useArkLabel = QtGui.QLabel(self.arkPage)
        self.useArkLabel.setAlignment(QtCore.Qt.AlignJustify|QtCore.Qt.AlignVCenter)
        self.useArkLabel.setWordWrap(True)
        self.useArkLabel.setObjectName(_fromUtf8("useArkLabel"))
        self.gridLayout_5.addWidget(self.useArkLabel, 0, 0, 1, 1)
        self.arkUrlEdit = QtGui.QLineEdit(self.arkPage)
        self.arkUrlEdit.setEnabled(False)
        self.arkUrlEdit.setObjectName(_fromUtf8("arkUrlEdit"))
        self.gridLayout_5.addWidget(self.arkUrlEdit, 3, 0, 1, 1)
        SettingsWizard.addPage(self.arkPage)
        self.confirmPage = QtGui.QWizardPage()
        self.confirmPage.setObjectName(_fromUtf8("confirmPage"))
        self.gridLayout_4 = QtGui.QGridLayout(self.confirmPage)
        self.gridLayout_4.setObjectName(_fromUtf8("gridLayout_4"))
        self.confirmLabel = QtGui.QLabel(self.confirmPage)
        self.confirmLabel.setAlignment(QtCore.Qt.AlignJustify|QtCore.Qt.AlignVCenter)
        self.confirmLabel.setWordWrap(True)
        self.confirmLabel.setObjectName(_fromUtf8("confirmLabel"))
        self.gridLayout_4.addWidget(self.confirmLabel, 0, 0, 1, 1)
        SettingsWizard.addPage(self.confirmPage)
        self.advancedLabel.setBuddy(self.advancedButton)
        self.folderLabel.setBuddy(self.projectFolderEdit)
        self.siteCodeLabel.setBuddy(self.siteCodeEdit)
        self.multiSiteLabel.setBuddy(self.multiSiteCheck)
        self.arkUrlLabel.setBuddy(self.arkUrlEdit)
        self.useArkLabel.setBuddy(self.useArkCheck)

        self.retranslateUi(SettingsWizard)
        QtCore.QObject.connect(self.useArkCheck, QtCore.SIGNAL(_fromUtf8("toggled(bool)")), self.arkUrlEdit.setEnabled)
        QtCore.QMetaObject.connectSlotsByName(SettingsWizard)

    def retranslateUi(self, SettingsWizard):
        SettingsWizard.setWindowTitle(_translate("SettingsWizard", "Wizard", None))
        self.welcomePage.setTitle(_translate("SettingsWizard", "New Project Wizard", None))
        self.welcomePage.setSubTitle(_translate("SettingsWizard", "This wizard will walk you through setting up a new ARK Spatial project.", None))
        self.advancedButton.setText(_translate("SettingsWizard", "Advanced", None))
        self.advancedLabel.setText(_translate("SettingsWizard", "If you require advanced custom settings, please click on the Advanced button to use the Settings dialog instead.", None))
        self.folderPage.setTitle(_translate("SettingsWizard", "Project Folder", None))
        self.folderPage.setSubTitle(_translate("SettingsWizard", "Please choose the folder where the project files will be stored.", None))
        self.folderLabel.setText(_translate("SettingsWizard", "This folder is usually something like \"Projects/TST01/GIS/\" where TST01 is the Site Code. The folder will be created if it does not already exist.\n"
"\n"
"ARK Spatial will automatically organise the data under this folder. If you wish to organise the data yourself you should choose the Advanced option on the previous page.\n"
"", None))
        self.siteCodePage.setTitle(_translate("SettingsWizard", "Site Code", None))
        self.siteCodePage.setSubTitle(_translate("SettingsWizard", "Enter the Site Code for the project.", None))
        self.siteCodeLabel.setText(_translate("SettingsWizard", "Enter the Site Code. If a Multi Site Project then enter a default Site Code.", None))
        self.multiSiteLabel.setText(_translate("SettingsWizard", "Choose if this project will support multiple sites and site codes in the same set of spatial files.", None))
        self.arkPage.setTitle(_translate("SettingsWizard", "ARK Database", None))
        self.arkPage.setSubTitle(_translate("SettingsWizard", "Configure working with an ARK Database. This is entirely optional.", None))
        self.arkUrlLabel.setText(_translate("SettingsWizard", "Please enter the root path to the ARK Database that you will be using, for example \"http://100minories.lparchaeology.com/data/\".", None))
        self.useArkLabel.setText(_translate("SettingsWizard", "Please tick if you will be using ARK Spatial with an ARK Database. Choosing this option will rename various fields and files to be compatible with ARK and will enable extra functionality to link the ARK Spatial data with the ARK Database. Note that this setting cannot be changed later.", None))
        self.confirmPage.setTitle(_translate("SettingsWizard", "Create Project", None))
        self.confirmPage.setSubTitle(_translate("SettingsWizard", "Create your new project.", None))
        self.confirmLabel.setText(_translate("SettingsWizard", "Click on the Done button to create your project. All required folders and files will be created. No existing data files will be overwritten.", None))

import resources_rc
