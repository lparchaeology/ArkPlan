# -*- coding: utf-8 -*-

# Form implementation generated from reading ui file 'core/settings_dialog_base.ui'
#
# Created: Wed Apr  8 14:38:46 2015
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
        SettingsDialogBase.resize(537, 354)
        self.verticalLayout = QtGui.QVBoxLayout(SettingsDialogBase)
        self.verticalLayout.setObjectName(_fromUtf8("verticalLayout"))
        self.tabWidget = QtGui.QTabWidget(SettingsDialogBase)
        self.tabWidget.setObjectName(_fromUtf8("tabWidget"))
        self.siteTab = QtGui.QWidget()
        self.siteTab.setObjectName(_fromUtf8("siteTab"))
        self.gridLayout_5 = QtGui.QGridLayout(self.siteTab)
        self.gridLayout_5.setObjectName(_fromUtf8("gridLayout_5"))
        self.siteFolderLabel = QtGui.QLabel(self.siteTab)
        self.siteFolderLabel.setObjectName(_fromUtf8("siteFolderLabel"))
        self.gridLayout_5.addWidget(self.siteFolderLabel, 0, 0, 1, 1)
        self.siteCodeEdit = QtGui.QLineEdit(self.siteTab)
        self.siteCodeEdit.setObjectName(_fromUtf8("siteCodeEdit"))
        self.gridLayout_5.addWidget(self.siteCodeEdit, 2, 2, 1, 1)
        spacerItem = QtGui.QSpacerItem(20, 40, QtGui.QSizePolicy.Minimum, QtGui.QSizePolicy.Expanding)
        self.gridLayout_5.addItem(spacerItem, 6, 2, 1, 1)
        self.customStylesLabel = QtGui.QLabel(self.siteTab)
        self.customStylesLabel.setObjectName(_fromUtf8("customStylesLabel"))
        self.gridLayout_5.addWidget(self.customStylesLabel, 5, 0, 1, 2)
        self.siteCodeLabel = QtGui.QLabel(self.siteTab)
        self.siteCodeLabel.setObjectName(_fromUtf8("siteCodeLabel"))
        self.gridLayout_5.addWidget(self.siteCodeLabel, 2, 0, 1, 1)
        self.defaultStylesLabel = QtGui.QLabel(self.siteTab)
        self.defaultStylesLabel.setObjectName(_fromUtf8("defaultStylesLabel"))
        self.gridLayout_5.addWidget(self.defaultStylesLabel, 4, 0, 1, 2)
        self.prependSiteCodeLabel = QtGui.QLabel(self.siteTab)
        self.prependSiteCodeLabel.setObjectName(_fromUtf8("prependSiteCodeLabel"))
        self.gridLayout_5.addWidget(self.prependSiteCodeLabel, 3, 0, 1, 1)
        self.defaultStylesCheck = QtGui.QCheckBox(self.siteTab)
        self.defaultStylesCheck.setText(_fromUtf8(""))
        self.defaultStylesCheck.setChecked(True)
        self.defaultStylesCheck.setObjectName(_fromUtf8("defaultStylesCheck"))
        self.gridLayout_5.addWidget(self.defaultStylesCheck, 4, 2, 1, 1)
        self.horizontalLayout_5 = QtGui.QHBoxLayout()
        self.horizontalLayout_5.setObjectName(_fromUtf8("horizontalLayout_5"))
        self.styleFolderEdit = QtGui.QLineEdit(self.siteTab)
        self.styleFolderEdit.setEnabled(False)
        self.styleFolderEdit.setObjectName(_fromUtf8("styleFolderEdit"))
        self.horizontalLayout_5.addWidget(self.styleFolderEdit)
        self.styleFolderButton = QtGui.QPushButton(self.siteTab)
        self.styleFolderButton.setEnabled(False)
        sizePolicy = QtGui.QSizePolicy(QtGui.QSizePolicy.Preferred, QtGui.QSizePolicy.Fixed)
        sizePolicy.setHorizontalStretch(0)
        sizePolicy.setVerticalStretch(0)
        sizePolicy.setHeightForWidth(self.styleFolderButton.sizePolicy().hasHeightForWidth())
        self.styleFolderButton.setSizePolicy(sizePolicy)
        self.styleFolderButton.setObjectName(_fromUtf8("styleFolderButton"))
        self.horizontalLayout_5.addWidget(self.styleFolderButton)
        self.gridLayout_5.addLayout(self.horizontalLayout_5, 5, 2, 1, 1)
        self.prependSiteCodeCheck = QtGui.QCheckBox(self.siteTab)
        self.prependSiteCodeCheck.setText(_fromUtf8(""))
        self.prependSiteCodeCheck.setChecked(True)
        self.prependSiteCodeCheck.setObjectName(_fromUtf8("prependSiteCodeCheck"))
        self.gridLayout_5.addWidget(self.prependSiteCodeCheck, 3, 2, 1, 1)
        self.siteFolderLayout = QtGui.QHBoxLayout()
        self.siteFolderLayout.setObjectName(_fromUtf8("siteFolderLayout"))
        self.siteFolderEdit = QtGui.QLineEdit(self.siteTab)
        self.siteFolderEdit.setObjectName(_fromUtf8("siteFolderEdit"))
        self.siteFolderLayout.addWidget(self.siteFolderEdit)
        self.siteFolderButton = QtGui.QPushButton(self.siteTab)
        sizePolicy = QtGui.QSizePolicy(QtGui.QSizePolicy.Preferred, QtGui.QSizePolicy.Fixed)
        sizePolicy.setHorizontalStretch(0)
        sizePolicy.setVerticalStretch(0)
        sizePolicy.setHeightForWidth(self.siteFolderButton.sizePolicy().hasHeightForWidth())
        self.siteFolderButton.setSizePolicy(sizePolicy)
        self.siteFolderButton.setObjectName(_fromUtf8("siteFolderButton"))
        self.siteFolderLayout.addWidget(self.siteFolderButton)
        self.gridLayout_5.addLayout(self.siteFolderLayout, 0, 2, 1, 1)
        self.tabWidget.addTab(self.siteTab, _fromUtf8(""))
        self.gridTab = QtGui.QWidget()
        self.gridTab.setObjectName(_fromUtf8("gridTab"))
        self.gridLayout_4 = QtGui.QGridLayout(self.gridTab)
        self.gridLayout_4.setObjectName(_fromUtf8("gridLayout_4"))
        self.gridFolderLayout = QtGui.QHBoxLayout()
        self.gridFolderLayout.setObjectName(_fromUtf8("gridFolderLayout"))
        self.gridFolderEdit = QtGui.QLineEdit(self.gridTab)
        self.gridFolderEdit.setObjectName(_fromUtf8("gridFolderEdit"))
        self.gridFolderLayout.addWidget(self.gridFolderEdit)
        self.gridFolderButton = QtGui.QPushButton(self.gridTab)
        sizePolicy = QtGui.QSizePolicy(QtGui.QSizePolicy.Preferred, QtGui.QSizePolicy.Fixed)
        sizePolicy.setHorizontalStretch(0)
        sizePolicy.setVerticalStretch(0)
        sizePolicy.setHeightForWidth(self.gridFolderButton.sizePolicy().hasHeightForWidth())
        self.gridFolderButton.setSizePolicy(sizePolicy)
        self.gridFolderButton.setObjectName(_fromUtf8("gridFolderButton"))
        self.gridFolderLayout.addWidget(self.gridFolderButton)
        self.gridLayout_4.addLayout(self.gridFolderLayout, 0, 1, 1, 1)
        self.gridFolderLabel = QtGui.QLabel(self.gridTab)
        self.gridFolderLabel.setObjectName(_fromUtf8("gridFolderLabel"))
        self.gridLayout_4.addWidget(self.gridFolderLabel, 0, 0, 1, 1)
        self.gridPolygonsNameLabel = QtGui.QLabel(self.gridTab)
        self.gridPolygonsNameLabel.setObjectName(_fromUtf8("gridPolygonsNameLabel"))
        self.gridLayout_4.addWidget(self.gridPolygonsNameLabel, 4, 0, 1, 1)
        self.gridPointsNameEdit = QtGui.QLineEdit(self.gridTab)
        self.gridPointsNameEdit.setObjectName(_fromUtf8("gridPointsNameEdit"))
        self.gridLayout_4.addWidget(self.gridPointsNameEdit, 2, 1, 1, 1)
        self.gridLinesNameLabel = QtGui.QLabel(self.gridTab)
        self.gridLinesNameLabel.setObjectName(_fromUtf8("gridLinesNameLabel"))
        self.gridLayout_4.addWidget(self.gridLinesNameLabel, 3, 0, 1, 1)
        self.gridPolygonsNameEdit = QtGui.QLineEdit(self.gridTab)
        self.gridPolygonsNameEdit.setObjectName(_fromUtf8("gridPolygonsNameEdit"))
        self.gridLayout_4.addWidget(self.gridPolygonsNameEdit, 4, 1, 1, 1)
        spacerItem1 = QtGui.QSpacerItem(20, 40, QtGui.QSizePolicy.Minimum, QtGui.QSizePolicy.Expanding)
        self.gridLayout_4.addItem(spacerItem1, 5, 1, 1, 1)
        self.gridLinesNameEdit = QtGui.QLineEdit(self.gridTab)
        self.gridLinesNameEdit.setObjectName(_fromUtf8("gridLinesNameEdit"))
        self.gridLayout_4.addWidget(self.gridLinesNameEdit, 3, 1, 1, 1)
        self.gridPointNameLabel = QtGui.QLabel(self.gridTab)
        self.gridPointNameLabel.setObjectName(_fromUtf8("gridPointNameLabel"))
        self.gridLayout_4.addWidget(self.gridPointNameLabel, 2, 0, 1, 1)
        self.gridGroupNameEdit = QtGui.QLineEdit(self.gridTab)
        self.gridGroupNameEdit.setObjectName(_fromUtf8("gridGroupNameEdit"))
        self.gridLayout_4.addWidget(self.gridGroupNameEdit, 1, 1, 1, 1)
        self.gridGroupNameLabel = QtGui.QLabel(self.gridTab)
        self.gridGroupNameLabel.setObjectName(_fromUtf8("gridGroupNameLabel"))
        self.gridLayout_4.addWidget(self.gridGroupNameLabel, 1, 0, 1, 1)
        self.tabWidget.addTab(self.gridTab, _fromUtf8(""))
        self.contextsTab = QtGui.QWidget()
        self.contextsTab.setObjectName(_fromUtf8("contextsTab"))
        self.gridLayout_3 = QtGui.QGridLayout(self.contextsTab)
        self.gridLayout_3.setObjectName(_fromUtf8("gridLayout_3"))
        self.contextsFolderLayout = QtGui.QHBoxLayout()
        self.contextsFolderLayout.setObjectName(_fromUtf8("contextsFolderLayout"))
        self.contextsFolderEdit = QtGui.QLineEdit(self.contextsTab)
        self.contextsFolderEdit.setObjectName(_fromUtf8("contextsFolderEdit"))
        self.contextsFolderLayout.addWidget(self.contextsFolderEdit)
        self.contextsFolderButton = QtGui.QPushButton(self.contextsTab)
        sizePolicy = QtGui.QSizePolicy(QtGui.QSizePolicy.Preferred, QtGui.QSizePolicy.Fixed)
        sizePolicy.setHorizontalStretch(0)
        sizePolicy.setVerticalStretch(0)
        sizePolicy.setHeightForWidth(self.contextsFolderButton.sizePolicy().hasHeightForWidth())
        self.contextsFolderButton.setSizePolicy(sizePolicy)
        self.contextsFolderButton.setObjectName(_fromUtf8("contextsFolderButton"))
        self.contextsFolderLayout.addWidget(self.contextsFolderButton)
        self.gridLayout_3.addLayout(self.contextsFolderLayout, 0, 1, 1, 1)
        self.contextsFolderLabel = QtGui.QLabel(self.contextsTab)
        self.contextsFolderLabel.setObjectName(_fromUtf8("contextsFolderLabel"))
        self.gridLayout_3.addWidget(self.contextsFolderLabel, 0, 0, 1, 1)
        spacerItem2 = QtGui.QSpacerItem(20, 40, QtGui.QSizePolicy.Minimum, QtGui.QSizePolicy.Expanding)
        self.gridLayout_3.addItem(spacerItem2, 10, 1, 1, 1)
        self.contextsScopeNameLabel = QtGui.QLabel(self.contextsTab)
        self.contextsScopeNameLabel.setObjectName(_fromUtf8("contextsScopeNameLabel"))
        self.gridLayout_3.addWidget(self.contextsScopeNameLabel, 9, 0, 1, 1)
        self.contextsPointsNameEdit = QtGui.QLineEdit(self.contextsTab)
        self.contextsPointsNameEdit.setObjectName(_fromUtf8("contextsPointsNameEdit"))
        self.gridLayout_3.addWidget(self.contextsPointsNameEdit, 4, 1, 1, 1)
        self.contextsGroupNameLabel = QtGui.QLabel(self.contextsTab)
        self.contextsGroupNameLabel.setObjectName(_fromUtf8("contextsGroupNameLabel"))
        self.gridLayout_3.addWidget(self.contextsGroupNameLabel, 2, 0, 1, 1)
        self.contextsGroupNameEdit = QtGui.QLineEdit(self.contextsTab)
        self.contextsGroupNameEdit.setObjectName(_fromUtf8("contextsGroupNameEdit"))
        self.gridLayout_3.addWidget(self.contextsGroupNameEdit, 2, 1, 1, 1)
        self.contextsPolygonsNameEdit = QtGui.QLineEdit(self.contextsTab)
        self.contextsPolygonsNameEdit.setObjectName(_fromUtf8("contextsPolygonsNameEdit"))
        self.gridLayout_3.addWidget(self.contextsPolygonsNameEdit, 8, 1, 1, 1)
        self.contextsLinesNameLabel = QtGui.QLabel(self.contextsTab)
        self.contextsLinesNameLabel.setObjectName(_fromUtf8("contextsLinesNameLabel"))
        self.gridLayout_3.addWidget(self.contextsLinesNameLabel, 6, 0, 1, 1)
        self.contextsScopeNameEdit = QtGui.QLineEdit(self.contextsTab)
        self.contextsScopeNameEdit.setObjectName(_fromUtf8("contextsScopeNameEdit"))
        self.gridLayout_3.addWidget(self.contextsScopeNameEdit, 9, 1, 1, 1)
        self.contextsLinesNameEdit = QtGui.QLineEdit(self.contextsTab)
        self.contextsLinesNameEdit.setObjectName(_fromUtf8("contextsLinesNameEdit"))
        self.gridLayout_3.addWidget(self.contextsLinesNameEdit, 6, 1, 1, 1)
        self.contextsPointNameLabel = QtGui.QLabel(self.contextsTab)
        self.contextsPointNameLabel.setObjectName(_fromUtf8("contextsPointNameLabel"))
        self.gridLayout_3.addWidget(self.contextsPointNameLabel, 4, 0, 1, 1)
        self.contextsPolygonsNameLabel = QtGui.QLabel(self.contextsTab)
        self.contextsPolygonsNameLabel.setObjectName(_fromUtf8("contextsPolygonsNameLabel"))
        self.gridLayout_3.addWidget(self.contextsPolygonsNameLabel, 8, 0, 1, 1)
        self.contextsBufferGroupNameEdit = QtGui.QLineEdit(self.contextsTab)
        self.contextsBufferGroupNameEdit.setObjectName(_fromUtf8("contextsBufferGroupNameEdit"))
        self.gridLayout_3.addWidget(self.contextsBufferGroupNameEdit, 3, 1, 1, 1)
        self.contextsBufferGroupNameLabel = QtGui.QLabel(self.contextsTab)
        self.contextsBufferGroupNameLabel.setObjectName(_fromUtf8("contextsBufferGroupNameLabel"))
        self.gridLayout_3.addWidget(self.contextsBufferGroupNameLabel, 3, 0, 1, 1)
        self.tabWidget.addTab(self.contextsTab, _fromUtf8(""))
        self.plansTab = QtGui.QWidget()
        self.plansTab.setObjectName(_fromUtf8("plansTab"))
        self.gridLayout_2 = QtGui.QGridLayout(self.plansTab)
        self.gridLayout_2.setObjectName(_fromUtf8("gridLayout_2"))
        self.separatePlansCheck = QtGui.QCheckBox(self.plansTab)
        self.separatePlansCheck.setText(_fromUtf8(""))
        self.separatePlansCheck.setChecked(True)
        self.separatePlansCheck.setObjectName(_fromUtf8("separatePlansCheck"))
        self.gridLayout_2.addWidget(self.separatePlansCheck, 1, 1, 1, 1)
        self.horizontalLayout_2 = QtGui.QHBoxLayout()
        self.horizontalLayout_2.setObjectName(_fromUtf8("horizontalLayout_2"))
        self.planFolderEdit = QtGui.QLineEdit(self.plansTab)
        self.planFolderEdit.setObjectName(_fromUtf8("planFolderEdit"))
        self.horizontalLayout_2.addWidget(self.planFolderEdit)
        self.planFolderButton = QtGui.QPushButton(self.plansTab)
        sizePolicy = QtGui.QSizePolicy(QtGui.QSizePolicy.Preferred, QtGui.QSizePolicy.Fixed)
        sizePolicy.setHorizontalStretch(0)
        sizePolicy.setVerticalStretch(0)
        sizePolicy.setHeightForWidth(self.planFolderButton.sizePolicy().hasHeightForWidth())
        self.planFolderButton.setSizePolicy(sizePolicy)
        self.planFolderButton.setObjectName(_fromUtf8("planFolderButton"))
        self.horizontalLayout_2.addWidget(self.planFolderButton)
        self.gridLayout_2.addLayout(self.horizontalLayout_2, 0, 1, 1, 1)
        self.planTransparencyLabel = QtGui.QLabel(self.plansTab)
        self.planTransparencyLabel.setObjectName(_fromUtf8("planTransparencyLabel"))
        self.gridLayout_2.addWidget(self.planTransparencyLabel, 2, 0, 1, 1)
        self.separatePlansLabel = QtGui.QLabel(self.plansTab)
        self.separatePlansLabel.setObjectName(_fromUtf8("separatePlansLabel"))
        self.gridLayout_2.addWidget(self.separatePlansLabel, 1, 0, 1, 1)
        self.horizontalLayout_4 = QtGui.QHBoxLayout()
        self.horizontalLayout_4.setObjectName(_fromUtf8("horizontalLayout_4"))
        self.planTransparencySpin = QtGui.QSpinBox(self.plansTab)
        self.planTransparencySpin.setMaximum(100)
        self.planTransparencySpin.setProperty("value", 50)
        self.planTransparencySpin.setObjectName(_fromUtf8("planTransparencySpin"))
        self.horizontalLayout_4.addWidget(self.planTransparencySpin)
        spacerItem3 = QtGui.QSpacerItem(40, 20, QtGui.QSizePolicy.Expanding, QtGui.QSizePolicy.Minimum)
        self.horizontalLayout_4.addItem(spacerItem3)
        self.gridLayout_2.addLayout(self.horizontalLayout_4, 2, 1, 1, 1)
        self.planFolderLabel = QtGui.QLabel(self.plansTab)
        self.planFolderLabel.setObjectName(_fromUtf8("planFolderLabel"))
        self.gridLayout_2.addWidget(self.planFolderLabel, 0, 0, 1, 1)
        spacerItem4 = QtGui.QSpacerItem(20, 40, QtGui.QSizePolicy.Minimum, QtGui.QSizePolicy.Expanding)
        self.gridLayout_2.addItem(spacerItem4, 3, 1, 1, 1)
        self.tabWidget.addTab(self.plansTab, _fromUtf8(""))
        self.verticalLayout.addWidget(self.tabWidget)
        self.buttonBox = QtGui.QDialogButtonBox(SettingsDialogBase)
        self.buttonBox.setOrientation(QtCore.Qt.Horizontal)
        self.buttonBox.setStandardButtons(QtGui.QDialogButtonBox.Cancel|QtGui.QDialogButtonBox.Ok)
        self.buttonBox.setObjectName(_fromUtf8("buttonBox"))
        self.verticalLayout.addWidget(self.buttonBox)
        self.siteCodeLabel.setBuddy(self.siteCodeEdit)
        self.prependSiteCodeLabel.setBuddy(self.prependSiteCodeCheck)
        self.contextsFolderLabel.setBuddy(self.contextsFolderEdit)
        self.contextsScopeNameLabel.setBuddy(self.contextsScopeNameEdit)
        self.contextsGroupNameLabel.setBuddy(self.contextsGroupNameEdit)
        self.contextsLinesNameLabel.setBuddy(self.contextsLinesNameEdit)
        self.contextsPointNameLabel.setBuddy(self.contextsPointsNameEdit)
        self.contextsPolygonsNameLabel.setBuddy(self.contextsPolygonsNameEdit)
        self.planTransparencyLabel.setBuddy(self.planTransparencySpin)
        self.separatePlansLabel.setBuddy(self.separatePlansCheck)
        self.planFolderLabel.setBuddy(self.planFolderEdit)

        self.retranslateUi(SettingsDialogBase)
        self.tabWidget.setCurrentIndex(0)
        QtCore.QObject.connect(self.buttonBox, QtCore.SIGNAL(_fromUtf8("accepted()")), SettingsDialogBase.accept)
        QtCore.QObject.connect(self.buttonBox, QtCore.SIGNAL(_fromUtf8("rejected()")), SettingsDialogBase.reject)
        QtCore.QMetaObject.connectSlotsByName(SettingsDialogBase)
        SettingsDialogBase.setTabOrder(self.contextsFolderEdit, self.contextsFolderButton)
        SettingsDialogBase.setTabOrder(self.contextsFolderButton, self.planFolderEdit)
        SettingsDialogBase.setTabOrder(self.planFolderEdit, self.planFolderButton)
        SettingsDialogBase.setTabOrder(self.planFolderButton, self.planTransparencySpin)
        SettingsDialogBase.setTabOrder(self.planTransparencySpin, self.buttonBox)

    def retranslateUi(self, SettingsDialogBase):
        SettingsDialogBase.setWindowTitle(_translate("SettingsDialogBase", "Settings", None))
        self.siteFolderLabel.setText(_translate("SettingsDialogBase", "Site Folder:", None))
        self.customStylesLabel.setText(_translate("SettingsDialogBase", "Custom Styles Folder:", None))
        self.siteCodeLabel.setText(_translate("SettingsDialogBase", "Site Code:", None))
        self.defaultStylesLabel.setText(_translate("SettingsDialogBase", "Use Default Styles:", None))
        self.prependSiteCodeLabel.setText(_translate("SettingsDialogBase", "Prepend site code:", None))
        self.styleFolderButton.setText(_translate("SettingsDialogBase", "...", None))
        self.siteFolderButton.setText(_translate("SettingsDialogBase", "...", None))
        self.tabWidget.setTabText(self.tabWidget.indexOf(self.siteTab), _translate("SettingsDialogBase", "Site", None))
        self.gridFolderButton.setText(_translate("SettingsDialogBase", "...", None))
        self.gridFolderLabel.setText(_translate("SettingsDialogBase", "Folder:", None))
        self.gridPolygonsNameLabel.setText(_translate("SettingsDialogBase", "Polygons Base Name:", None))
        self.gridLinesNameLabel.setText(_translate("SettingsDialogBase", "Lines Base Name:", None))
        self.gridPointNameLabel.setText(_translate("SettingsDialogBase", "Points Base Name:", None))
        self.gridGroupNameLabel.setText(_translate("SettingsDialogBase", "Group Name:", None))
        self.tabWidget.setTabText(self.tabWidget.indexOf(self.gridTab), _translate("SettingsDialogBase", "Grid", None))
        self.contextsFolderButton.setText(_translate("SettingsDialogBase", "...", None))
        self.contextsFolderLabel.setText(_translate("SettingsDialogBase", "Contexts Folder:", None))
        self.contextsScopeNameLabel.setText(_translate("SettingsDialogBase", "Scope Base Name:", None))
        self.contextsGroupNameLabel.setText(_translate("SettingsDialogBase", "Group Name:", None))
        self.contextsLinesNameLabel.setText(_translate("SettingsDialogBase", "Lines Base Name:", None))
        self.contextsPointNameLabel.setText(_translate("SettingsDialogBase", "Points Base Name:", None))
        self.contextsPolygonsNameLabel.setText(_translate("SettingsDialogBase", "Polygons Base Name:", None))
        self.contextsBufferGroupNameLabel.setText(_translate("SettingsDialogBase", "Buffer Group Name:", None))
        self.tabWidget.setTabText(self.tabWidget.indexOf(self.contextsTab), _translate("SettingsDialogBase", "Contexts", None))
        self.separatePlansCheck.setToolTip(_translate("SettingsDialogBase", "Select if the raw and processed plans should be stored in separate folders.", None))
        self.planFolderButton.setText(_translate("SettingsDialogBase", "...", None))
        self.planTransparencyLabel.setText(_translate("SettingsDialogBase", "Plan tranparency:", None))
        self.separatePlansLabel.setText(_translate("SettingsDialogBase", "Separate plan folders:", None))
        self.planTransparencySpin.setSuffix(_translate("SettingsDialogBase", "%", None))
        self.planFolderLabel.setText(_translate("SettingsDialogBase", "Plan Folder:", None))
        self.tabWidget.setTabText(self.tabWidget.indexOf(self.plansTab), _translate("SettingsDialogBase", "Plans", None))

