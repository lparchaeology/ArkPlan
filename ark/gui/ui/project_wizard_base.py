# -*- coding: utf-8 -*-

# Form implementation generated from reading ui file 'ark/gui/ui/project_wizard_base.ui'
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

class Ui_ProjectWizard(object):
    def setupUi(self, ProjectWizard):
        ProjectWizard.setObjectName(_fromUtf8("ProjectWizard"))
        ProjectWizard.resize(768, 425)
        ProjectWizard.setOptions(QtGui.QWizard.CancelButtonOnLeft|QtGui.QWizard.NoBackButtonOnStartPage|QtGui.QWizard.NoDefaultButton)
        self.welcomePage = QtGui.QWizardPage()
        self.welcomePage.setObjectName(_fromUtf8("welcomePage"))
        self.gridLayout_2 = QtGui.QGridLayout(self.welcomePage)
        self.gridLayout_2.setObjectName(_fromUtf8("gridLayout_2"))
        self.welcomeLabel = QtGui.QLabel(self.welcomePage)
        self.welcomeLabel.setText(_fromUtf8(""))
        self.welcomeLabel.setObjectName(_fromUtf8("welcomeLabel"))
        self.gridLayout_2.addWidget(self.welcomeLabel, 0, 0, 1, 1)
        ProjectWizard.addPage(self.welcomePage)
        self.projectPage = ProjectWizardPage()
        self.projectPage.setObjectName(_fromUtf8("projectPage"))
        self.projectLayout = QtGui.QGridLayout(self.projectPage)
        self.projectLayout.setObjectName(_fromUtf8("projectLayout"))
        self.projectLabel = QtGui.QLabel(self.projectPage)
        self.projectLabel.setAlignment(QtCore.Qt.AlignJustify|QtCore.Qt.AlignVCenter)
        self.projectLabel.setWordWrap(True)
        self.projectLabel.setObjectName(_fromUtf8("projectLabel"))
        self.projectLayout.addWidget(self.projectLabel, 0, 0, 1, 2)
        self.projectWidget = ProjectWidget(self.projectPage)
        self.projectWidget.setObjectName(_fromUtf8("projectWidget"))
        self.projectLayout.addWidget(self.projectWidget, 1, 0, 1, 2)
        ProjectWizard.addPage(self.projectPage)
        self.serverPage = ServerWizardPage()
        self.serverPage.setObjectName(_fromUtf8("serverPage"))
        self.serverLayout = QtGui.QGridLayout(self.serverPage)
        self.serverLayout.setObjectName(_fromUtf8("serverLayout"))
        self.serverWidget = ServerWidget(self.serverPage)
        self.serverWidget.setObjectName(_fromUtf8("serverWidget"))
        self.serverLayout.addWidget(self.serverWidget, 0, 0, 1, 2)
        ProjectWizard.addPage(self.serverPage)
        self.confirmPage = ConfirmPage()
        self.confirmPage.setObjectName(_fromUtf8("confirmPage"))
        self.gridLayout = QtGui.QGridLayout(self.confirmPage)
        self.gridLayout.setObjectName(_fromUtf8("gridLayout"))
        self.projectFolderButton = QtGui.QToolButton(self.confirmPage)
        icon = QtGui.QIcon()
        icon.addPixmap(QtGui.QPixmap(_fromUtf8(":/plugins/ark/folder.png")), QtGui.QIcon.Normal, QtGui.QIcon.Off)
        self.projectFolderButton.setIcon(icon)
        self.projectFolderButton.setObjectName(_fromUtf8("projectFolderButton"))
        self.gridLayout.addWidget(self.projectFolderButton, 3, 3, 1, 1)
        self.projectFolderLabel = QtGui.QLabel(self.confirmPage)
        self.projectFolderLabel.setObjectName(_fromUtf8("projectFolderLabel"))
        self.gridLayout.addWidget(self.projectFolderLabel, 3, 0, 1, 2)
        self.projectFullPath = QtGui.QLabel(self.confirmPage)
        self.projectFullPath.setObjectName(_fromUtf8("projectFullPath"))
        self.gridLayout.addWidget(self.projectFullPath, 7, 2, 1, 1)
        self.projectFolderEdit = QtGui.QLineEdit(self.confirmPage)
        self.projectFolderEdit.setObjectName(_fromUtf8("projectFolderEdit"))
        self.gridLayout.addWidget(self.projectFolderEdit, 3, 2, 1, 1)
        self.projectFileLabel = QtGui.QLabel(self.confirmPage)
        self.projectFileLabel.setObjectName(_fromUtf8("projectFileLabel"))
        self.gridLayout.addWidget(self.projectFileLabel, 6, 0, 1, 2)
        spacerItem = QtGui.QSpacerItem(20, 40, QtGui.QSizePolicy.Minimum, QtGui.QSizePolicy.Expanding)
        self.gridLayout.addItem(spacerItem, 9, 2, 1, 1)
        self.projectFullPathLabel = QtGui.QLabel(self.confirmPage)
        self.projectFullPathLabel.setObjectName(_fromUtf8("projectFullPathLabel"))
        self.gridLayout.addWidget(self.projectFullPathLabel, 7, 0, 1, 2)
        self.confirmPageLabel = QtGui.QLabel(self.confirmPage)
        self.confirmPageLabel.setAlignment(QtCore.Qt.AlignJustify|QtCore.Qt.AlignVCenter)
        self.confirmPageLabel.setWordWrap(True)
        self.confirmPageLabel.setObjectName(_fromUtf8("confirmPageLabel"))
        self.gridLayout.addWidget(self.confirmPageLabel, 0, 0, 1, 3)
        self.projectFileEdit = QtGui.QLineEdit(self.confirmPage)
        self.projectFileEdit.setObjectName(_fromUtf8("projectFileEdit"))
        self.gridLayout.addWidget(self.projectFileEdit, 6, 2, 1, 1)
        self.newProjectCheck = QtGui.QCheckBox(self.confirmPage)
        self.newProjectCheck.setText(_fromUtf8(""))
        self.newProjectCheck.setObjectName(_fromUtf8("newProjectCheck"))
        self.gridLayout.addWidget(self.newProjectCheck, 2, 2, 1, 1)
        self.newProjectLabel = QtGui.QLabel(self.confirmPage)
        self.newProjectLabel.setObjectName(_fromUtf8("newProjectLabel"))
        self.gridLayout.addWidget(self.newProjectLabel, 2, 0, 1, 2)
        ProjectWizard.addPage(self.confirmPage)
        self.projectFolderLabel.setBuddy(self.projectFolderEdit)
        self.projectFileLabel.setBuddy(self.projectFileEdit)
        self.newProjectLabel.setBuddy(self.newProjectCheck)

        self.retranslateUi(ProjectWizard)
        QtCore.QObject.connect(self.newProjectCheck, QtCore.SIGNAL(_fromUtf8("toggled(bool)")), self.projectFolderEdit.setEnabled)
        QtCore.QObject.connect(self.newProjectCheck, QtCore.SIGNAL(_fromUtf8("toggled(bool)")), self.projectFolderButton.setEnabled)
        QtCore.QObject.connect(self.newProjectCheck, QtCore.SIGNAL(_fromUtf8("toggled(bool)")), self.projectFileEdit.setEnabled)
        QtCore.QMetaObject.connectSlotsByName(ProjectWizard)
        ProjectWizard.setTabOrder(self.newProjectCheck, self.projectFolderEdit)
        ProjectWizard.setTabOrder(self.projectFolderEdit, self.projectFolderButton)
        ProjectWizard.setTabOrder(self.projectFolderButton, self.projectFileEdit)

    def retranslateUi(self, ProjectWizard):
        ProjectWizard.setWindowTitle(_translate("ProjectWizard", "ARKspatial Project Wizard", None))
        self.welcomePage.setTitle(_translate("ProjectWizard", "ARKspatial Project Wizard", None))
        self.welcomePage.setSubTitle(_translate("ProjectWizard", "This wizard will walk you through setting up a new or existing ARKspatial project.", None))
        self.projectPage.setTitle(_translate("ProjectWizard", "Project Details", None))
        self.projectPage.setSubTitle(_translate("ProjectWizard", "Enter the details for the Project.", None))
        self.projectLabel.setText(_translate("ProjectWizard", "You must enter at least a Project Code and Name. If no Site Code is entered, the Project Code is used instead. The Location will be used to create a site centre point.", None))
        self.serverPage.setTitle(_translate("ProjectWizard", "ARK Server Settings", None))
        self.serverPage.setSubTitle(_translate("ProjectWizard", "If you use an ARK database for site recording, enter the server details to enable querying the database.", None))
        self.confirmPage.setTitle(_translate("ProjectWizard", "Create Project", None))
        self.confirmPage.setSubTitle(_translate("ProjectWizard", "Confirm your project file details.", None))
        self.projectFolderLabel.setText(_translate("ProjectWizard", "Project Folder:", None))
        self.projectFolderEdit.setPlaceholderText(_translate("ProjectWizard", "/Disk/Data/Projects/TST01/GIS", None))
        self.projectFileLabel.setText(_translate("ProjectWizard", "Project Filename:", None))
        self.projectFullPathLabel.setText(_translate("ProjectWizard", "Full Path:", None))
        self.confirmPageLabel.setText(_translate("ProjectWizard", "You can choose to save the project details in the currently open project, or to save the project in a new project file.\n"
"\n"
"This folder is usually something like \"Projects/TST01/GIS\" where TST01 is the Project Code. The folder will be created if it does not already exist.\n"
"\n"
"ARK Spatial will automatically organise the data under this folder.\n"
"", None))
        self.projectFileEdit.setPlaceholderText(_translate("ProjectWizard", "SHU28_DG", None))
        self.newProjectLabel.setText(_translate("ProjectWizard", "Create New Project File:", None))

from ..project_widget import ProjectWidget
from ..project_wizard_page import ProjectWizardPage
from ..server_widget import ServerWidget
from ..server_wizard_page import ServerWizardPage
from ..wizard_page import ConfirmPage
