# -*- coding: utf-8 -*-

# Form implementation generated from reading ui file 'settings_dialog_base.ui'
#
# Created: Fri Feb 27 14:55:08 2015
#      by: PyQt4 UI code generator 4.11.3
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

class Ui_SettingsDialogBase(object):
    def setupUi(self, SettingsDialogBase):
        SettingsDialogBase.setObjectName(_fromUtf8("SettingsDialogBase"))
        SettingsDialogBase.resize(481, 277)
        self.formLayout = QtGui.QFormLayout(SettingsDialogBase)
        self.formLayout.setObjectName(_fromUtf8("formLayout"))
        self.siteCodeLabel = QtGui.QLabel(SettingsDialogBase)
        self.siteCodeLabel.setObjectName(_fromUtf8("siteCodeLabel"))
        self.formLayout.setWidget(0, QtGui.QFormLayout.LabelRole, self.siteCodeLabel)
        self.siteCodeEdit = QtGui.QLineEdit(SettingsDialogBase)
        self.siteCodeEdit.setObjectName(_fromUtf8("siteCodeEdit"))
        self.formLayout.setWidget(0, QtGui.QFormLayout.FieldRole, self.siteCodeEdit)
        self.dataFolderLabel = QtGui.QLabel(SettingsDialogBase)
        self.dataFolderLabel.setObjectName(_fromUtf8("dataFolderLabel"))
        self.formLayout.setWidget(1, QtGui.QFormLayout.LabelRole, self.dataFolderLabel)
        self.horizontalLayout = QtGui.QHBoxLayout()
        self.horizontalLayout.setObjectName(_fromUtf8("horizontalLayout"))
        self.dataFolderEdit = QtGui.QLineEdit(SettingsDialogBase)
        self.dataFolderEdit.setObjectName(_fromUtf8("dataFolderEdit"))
        self.horizontalLayout.addWidget(self.dataFolderEdit)
        self.dataFolderButton = QtGui.QPushButton(SettingsDialogBase)
        sizePolicy = QtGui.QSizePolicy(QtGui.QSizePolicy.Preferred, QtGui.QSizePolicy.Fixed)
        sizePolicy.setHorizontalStretch(0)
        sizePolicy.setVerticalStretch(0)
        sizePolicy.setHeightForWidth(self.dataFolderButton.sizePolicy().hasHeightForWidth())
        self.dataFolderButton.setSizePolicy(sizePolicy)
        self.dataFolderButton.setObjectName(_fromUtf8("dataFolderButton"))
        self.horizontalLayout.addWidget(self.dataFolderButton)
        self.formLayout.setLayout(1, QtGui.QFormLayout.FieldRole, self.horizontalLayout)
        self.prependSiteCodeLabel = QtGui.QLabel(SettingsDialogBase)
        self.prependSiteCodeLabel.setObjectName(_fromUtf8("prependSiteCodeLabel"))
        self.formLayout.setWidget(3, QtGui.QFormLayout.LabelRole, self.prependSiteCodeLabel)
        self.prependSiteCodeCheck = QtGui.QCheckBox(SettingsDialogBase)
        self.prependSiteCodeCheck.setText(_fromUtf8(""))
        self.prependSiteCodeCheck.setChecked(True)
        self.prependSiteCodeCheck.setObjectName(_fromUtf8("prependSiteCodeCheck"))
        self.formLayout.setWidget(3, QtGui.QFormLayout.FieldRole, self.prependSiteCodeCheck)
        self.planFolderLabel = QtGui.QLabel(SettingsDialogBase)
        self.planFolderLabel.setObjectName(_fromUtf8("planFolderLabel"))
        self.formLayout.setWidget(4, QtGui.QFormLayout.LabelRole, self.planFolderLabel)
        self.horizontalLayout_2 = QtGui.QHBoxLayout()
        self.horizontalLayout_2.setObjectName(_fromUtf8("horizontalLayout_2"))
        self.planFolderEdit = QtGui.QLineEdit(SettingsDialogBase)
        self.planFolderEdit.setObjectName(_fromUtf8("planFolderEdit"))
        self.horizontalLayout_2.addWidget(self.planFolderEdit)
        self.planFolderButton = QtGui.QPushButton(SettingsDialogBase)
        sizePolicy = QtGui.QSizePolicy(QtGui.QSizePolicy.Preferred, QtGui.QSizePolicy.Fixed)
        sizePolicy.setHorizontalStretch(0)
        sizePolicy.setVerticalStretch(0)
        sizePolicy.setHeightForWidth(self.planFolderButton.sizePolicy().hasHeightForWidth())
        self.planFolderButton.setSizePolicy(sizePolicy)
        self.planFolderButton.setObjectName(_fromUtf8("planFolderButton"))
        self.horizontalLayout_2.addWidget(self.planFolderButton)
        self.formLayout.setLayout(4, QtGui.QFormLayout.FieldRole, self.horizontalLayout_2)
        self.separatePlansLabel = QtGui.QLabel(SettingsDialogBase)
        self.separatePlansLabel.setObjectName(_fromUtf8("separatePlansLabel"))
        self.formLayout.setWidget(6, QtGui.QFormLayout.LabelRole, self.separatePlansLabel)
        self.separatePlansCheck = QtGui.QCheckBox(SettingsDialogBase)
        self.separatePlansCheck.setText(_fromUtf8(""))
        self.separatePlansCheck.setChecked(True)
        self.separatePlansCheck.setObjectName(_fromUtf8("separatePlansCheck"))
        self.formLayout.setWidget(6, QtGui.QFormLayout.FieldRole, self.separatePlansCheck)
        self.planTransparencyLabel = QtGui.QLabel(SettingsDialogBase)
        self.planTransparencyLabel.setObjectName(_fromUtf8("planTransparencyLabel"))
        self.formLayout.setWidget(7, QtGui.QFormLayout.LabelRole, self.planTransparencyLabel)
        self.planTransparencySpin = QtGui.QSpinBox(SettingsDialogBase)
        self.planTransparencySpin.setMaximum(100)
        self.planTransparencySpin.setProperty("value", 50)
        self.planTransparencySpin.setObjectName(_fromUtf8("planTransparencySpin"))
        self.formLayout.setWidget(7, QtGui.QFormLayout.FieldRole, self.planTransparencySpin)
        self.buttonBox = QtGui.QDialogButtonBox(SettingsDialogBase)
        self.buttonBox.setOrientation(QtCore.Qt.Horizontal)
        self.buttonBox.setStandardButtons(QtGui.QDialogButtonBox.Cancel|QtGui.QDialogButtonBox.Ok)
        self.buttonBox.setObjectName(_fromUtf8("buttonBox"))
        self.formLayout.setWidget(8, QtGui.QFormLayout.SpanningRole, self.buttonBox)
        self.siteCodeLabel.setBuddy(self.siteCodeEdit)
        self.dataFolderLabel.setBuddy(self.dataFolderEdit)
        self.prependSiteCodeLabel.setBuddy(self.prependSiteCodeCheck)
        self.planFolderLabel.setBuddy(self.planFolderEdit)
        self.separatePlansLabel.setBuddy(self.separatePlansCheck)
        self.planTransparencyLabel.setBuddy(self.planTransparencySpin)

        self.retranslateUi(SettingsDialogBase)
        QtCore.QObject.connect(self.buttonBox, QtCore.SIGNAL(_fromUtf8("accepted()")), SettingsDialogBase.accept)
        QtCore.QObject.connect(self.buttonBox, QtCore.SIGNAL(_fromUtf8("rejected()")), SettingsDialogBase.reject)
        QtCore.QMetaObject.connectSlotsByName(SettingsDialogBase)
        SettingsDialogBase.setTabOrder(self.siteCodeEdit, self.dataFolderEdit)
        SettingsDialogBase.setTabOrder(self.dataFolderEdit, self.dataFolderButton)
        SettingsDialogBase.setTabOrder(self.dataFolderButton, self.prependSiteCodeCheck)
        SettingsDialogBase.setTabOrder(self.prependSiteCodeCheck, self.planFolderEdit)
        SettingsDialogBase.setTabOrder(self.planFolderEdit, self.planFolderButton)
        SettingsDialogBase.setTabOrder(self.planFolderButton, self.separatePlansCheck)
        SettingsDialogBase.setTabOrder(self.separatePlansCheck, self.planTransparencySpin)
        SettingsDialogBase.setTabOrder(self.planTransparencySpin, self.buttonBox)

    def retranslateUi(self, SettingsDialogBase):
        SettingsDialogBase.setWindowTitle(_translate("SettingsDialogBase", "Settings", None))
        self.siteCodeLabel.setText(_translate("SettingsDialogBase", "Site Code:", None))
        self.dataFolderLabel.setText(_translate("SettingsDialogBase", "Data Folder:", None))
        self.dataFolderButton.setText(_translate("SettingsDialogBase", "...", None))
        self.prependSiteCodeLabel.setText(_translate("SettingsDialogBase", "Prepend site code:", None))
        self.planFolderLabel.setText(_translate("SettingsDialogBase", "Plan Folder:", None))
        self.planFolderButton.setText(_translate("SettingsDialogBase", "...", None))
        self.separatePlansLabel.setText(_translate("SettingsDialogBase", "Separate plan folders:", None))
        self.separatePlansCheck.setToolTip(_translate("SettingsDialogBase", "Select if the raw and processed plans should be stored in separate folders.", None))
        self.planTransparencyLabel.setText(_translate("SettingsDialogBase", "Plan tranparency:", None))
        self.planTransparencySpin.setSuffix(_translate("SettingsDialogBase", "%", None))

