# -*- coding: utf-8 -*-

# Form implementation generated from reading ui file 'project_settings_dialog_base.ui'
#
# Created by: PyQt4 UI code generator 4.11.3
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

class Ui_ProjectSettingsDialogBase(object):
    def setupUi(self, ProjectSettingsDialogBase):
        ProjectSettingsDialogBase.setObjectName(_fromUtf8("ProjectSettingsDialogBase"))
        ProjectSettingsDialogBase.resize(481, 265)
        self.formLayout = QtGui.QFormLayout(ProjectSettingsDialogBase)
        self.formLayout.setObjectName(_fromUtf8("formLayout"))
        self.siteCodeLabel = QtGui.QLabel(ProjectSettingsDialogBase)
        self.siteCodeLabel.setObjectName(_fromUtf8("siteCodeLabel"))
        self.formLayout.setWidget(0, QtGui.QFormLayout.LabelRole, self.siteCodeLabel)
        self.siteCodeEdit = QtGui.QLineEdit(ProjectSettingsDialogBase)
        self.siteCodeEdit.setObjectName(_fromUtf8("siteCodeEdit"))
        self.formLayout.setWidget(0, QtGui.QFormLayout.FieldRole, self.siteCodeEdit)
        self.dataFolderLabel = QtGui.QLabel(ProjectSettingsDialogBase)
        self.dataFolderLabel.setObjectName(_fromUtf8("dataFolderLabel"))
        self.formLayout.setWidget(1, QtGui.QFormLayout.LabelRole, self.dataFolderLabel)
        self.horizontalLayout = QtGui.QHBoxLayout()
        self.horizontalLayout.setObjectName(_fromUtf8("horizontalLayout"))
        self.dataFolderEdit = QtGui.QLineEdit(ProjectSettingsDialogBase)
        self.dataFolderEdit.setObjectName(_fromUtf8("dataFolderEdit"))
        self.horizontalLayout.addWidget(self.dataFolderEdit)
        self.dataFolderButton = QtGui.QPushButton(ProjectSettingsDialogBase)
        sizePolicy = QtGui.QSizePolicy(QtGui.QSizePolicy.Preferred, QtGui.QSizePolicy.Fixed)
        sizePolicy.setHorizontalStretch(0)
        sizePolicy.setVerticalStretch(0)
        sizePolicy.setHeightForWidth(self.dataFolderButton.sizePolicy().hasHeightForWidth())
        self.dataFolderButton.setSizePolicy(sizePolicy)
        self.dataFolderButton.setObjectName(_fromUtf8("dataFolderButton"))
        self.horizontalLayout.addWidget(self.dataFolderButton)
        self.formLayout.setLayout(1, QtGui.QFormLayout.FieldRole, self.horizontalLayout)
        self.prependSiteCodeLabel = QtGui.QLabel(ProjectSettingsDialogBase)
        self.prependSiteCodeLabel.setObjectName(_fromUtf8("prependSiteCodeLabel"))
        self.formLayout.setWidget(3, QtGui.QFormLayout.LabelRole, self.prependSiteCodeLabel)
        self.prependSiteCodeCheck = QtGui.QCheckBox(ProjectSettingsDialogBase)
        self.prependSiteCodeCheck.setText(_fromUtf8(""))
        self.prependSiteCodeCheck.setChecked(True)
        self.prependSiteCodeCheck.setObjectName(_fromUtf8("prependSiteCodeCheck"))
        self.formLayout.setWidget(3, QtGui.QFormLayout.FieldRole, self.prependSiteCodeCheck)
        self.planFolderLabel = QtGui.QLabel(ProjectSettingsDialogBase)
        self.planFolderLabel.setObjectName(_fromUtf8("planFolderLabel"))
        self.formLayout.setWidget(4, QtGui.QFormLayout.LabelRole, self.planFolderLabel)
        self.horizontalLayout_2 = QtGui.QHBoxLayout()
        self.horizontalLayout_2.setObjectName(_fromUtf8("horizontalLayout_2"))
        self.planFolderEdit = QtGui.QLineEdit(ProjectSettingsDialogBase)
        self.planFolderEdit.setObjectName(_fromUtf8("planFolderEdit"))
        self.horizontalLayout_2.addWidget(self.planFolderEdit)
        self.planFolderButton = QtGui.QPushButton(ProjectSettingsDialogBase)
        sizePolicy = QtGui.QSizePolicy(QtGui.QSizePolicy.Preferred, QtGui.QSizePolicy.Fixed)
        sizePolicy.setHorizontalStretch(0)
        sizePolicy.setVerticalStretch(0)
        sizePolicy.setHeightForWidth(self.planFolderButton.sizePolicy().hasHeightForWidth())
        self.planFolderButton.setSizePolicy(sizePolicy)
        self.planFolderButton.setObjectName(_fromUtf8("planFolderButton"))
        self.horizontalLayout_2.addWidget(self.planFolderButton)
        self.formLayout.setLayout(4, QtGui.QFormLayout.FieldRole, self.horizontalLayout_2)
        self.separatePlansLabel = QtGui.QLabel(ProjectSettingsDialogBase)
        self.separatePlansLabel.setObjectName(_fromUtf8("separatePlansLabel"))
        self.formLayout.setWidget(6, QtGui.QFormLayout.LabelRole, self.separatePlansLabel)
        self.separatePlansCheck = QtGui.QCheckBox(ProjectSettingsDialogBase)
        self.separatePlansCheck.setText(_fromUtf8(""))
        self.separatePlansCheck.setChecked(True)
        self.separatePlansCheck.setObjectName(_fromUtf8("separatePlansCheck"))
        self.formLayout.setWidget(6, QtGui.QFormLayout.FieldRole, self.separatePlansCheck)
        self.planOpacityLabel = QtGui.QLabel(ProjectSettingsDialogBase)
        self.planOpacityLabel.setObjectName(_fromUtf8("planOpacityLabel"))
        self.formLayout.setWidget(7, QtGui.QFormLayout.LabelRole, self.planOpacityLabel)
        self.planOpacitySpin = QtGui.QSpinBox(ProjectSettingsDialogBase)
        self.planOpacitySpin.setMaximum(100)
        self.planOpacitySpin.setProperty("value", 50)
        self.planOpacitySpin.setObjectName(_fromUtf8("planOpacitySpin"))
        self.formLayout.setWidget(7, QtGui.QFormLayout.FieldRole, self.planOpacitySpin)
        self.buttonBox = QtGui.QDialogButtonBox(ProjectSettingsDialogBase)
        self.buttonBox.setOrientation(QtCore.Qt.Horizontal)
        self.buttonBox.setStandardButtons(QtGui.QDialogButtonBox.Cancel|QtGui.QDialogButtonBox.Ok)
        self.buttonBox.setObjectName(_fromUtf8("buttonBox"))
        self.formLayout.setWidget(8, QtGui.QFormLayout.SpanningRole, self.buttonBox)
        self.siteCodeLabel.setBuddy(self.siteCodeEdit)
        self.dataFolderLabel.setBuddy(self.dataFolderEdit)
        self.prependSiteCodeLabel.setBuddy(self.prependSiteCodeCheck)
        self.planFolderLabel.setBuddy(self.planFolderEdit)
        self.separatePlansLabel.setBuddy(self.separatePlansCheck)
        self.planOpacityLabel.setBuddy(self.planOpacitySpin)

        self.retranslateUi(ProjectSettingsDialogBase)
        QtCore.QObject.connect(self.buttonBox, QtCore.SIGNAL(_fromUtf8("accepted()")), ProjectSettingsDialogBase.accept)
        QtCore.QObject.connect(self.buttonBox, QtCore.SIGNAL(_fromUtf8("rejected()")), ProjectSettingsDialogBase.reject)
        QtCore.QMetaObject.connectSlotsByName(ProjectSettingsDialogBase)
        ProjectSettingsDialogBase.setTabOrder(self.siteCodeEdit, self.dataFolderEdit)
        ProjectSettingsDialogBase.setTabOrder(self.dataFolderEdit, self.dataFolderButton)
        ProjectSettingsDialogBase.setTabOrder(self.dataFolderButton, self.prependSiteCodeCheck)
        ProjectSettingsDialogBase.setTabOrder(self.prependSiteCodeCheck, self.planFolderEdit)
        ProjectSettingsDialogBase.setTabOrder(self.planFolderEdit, self.planFolderButton)
        ProjectSettingsDialogBase.setTabOrder(self.planFolderButton, self.separatePlansCheck)
        ProjectSettingsDialogBase.setTabOrder(self.separatePlansCheck, self.planOpacitySpin)
        ProjectSettingsDialogBase.setTabOrder(self.planOpacitySpin, self.buttonBox)

    def retranslateUi(self, ProjectSettingsDialogBase):
        ProjectSettingsDialogBase.setWindowTitle(_translate("ProjectSettingsDialogBase", "ArkPlan Project Settings", None))
        self.siteCodeLabel.setText(_translate("ProjectSettingsDialogBase", "Site Code:", None))
        self.dataFolderLabel.setText(_translate("ProjectSettingsDialogBase", "Data Folder:", None))
        self.dataFolderButton.setText(_translate("ProjectSettingsDialogBase", "...", None))
        self.prependSiteCodeLabel.setText(_translate("ProjectSettingsDialogBase", "Prepend site code:", None))
        self.planFolderLabel.setText(_translate("ProjectSettingsDialogBase", "Plan Folder:", None))
        self.planFolderButton.setText(_translate("ProjectSettingsDialogBase", "...", None))
        self.separatePlansLabel.setText(_translate("ProjectSettingsDialogBase", "Separate raw / processed:", None))
        self.planOpacityLabel.setText(_translate("ProjectSettingsDialogBase", "Plan opacity:", None))
        self.planOpacitySpin.setSuffix(_translate("ProjectSettingsDialogBase", "%", None))

