# -*- coding: utf-8 -*-

# Form implementation generated from reading ui file 'ark/gui/ui/preferences_wizard_base.ui'
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

class Ui_PreferencesWizard(object):
    def setupUi(self, PreferencesWizard):
        PreferencesWizard.setObjectName(_fromUtf8("PreferencesWizard"))
        PreferencesWizard.resize(771, 443)
        PreferencesWizard.setOptions(QtGui.QWizard.CancelButtonOnLeft|QtGui.QWizard.NoBackButtonOnStartPage|QtGui.QWizard.NoDefaultButton)
        self.welcomePage = QtGui.QWizardPage()
        self.welcomePage.setObjectName(_fromUtf8("welcomePage"))
        self.gridLayout = QtGui.QGridLayout(self.welcomePage)
        self.gridLayout.setObjectName(_fromUtf8("gridLayout"))
        self.label = QtGui.QLabel(self.welcomePage)
        self.label.setText(_fromUtf8(""))
        self.label.setObjectName(_fromUtf8("label"))
        self.gridLayout.addWidget(self.label, 0, 0, 1, 1)
        PreferencesWizard.addPage(self.welcomePage)
        self.preferencesPage = PreferencesWizardPage()
        self.preferencesPage.setObjectName(_fromUtf8("preferencesPage"))
        self.gridLayout_2 = QtGui.QGridLayout(self.preferencesPage)
        self.gridLayout_2.setObjectName(_fromUtf8("gridLayout_2"))
        self.preferencesWidget = PreferencesWidget(self.preferencesPage)
        self.preferencesWidget.setObjectName(_fromUtf8("preferencesWidget"))
        self.gridLayout_2.addWidget(self.preferencesWidget, 0, 0, 1, 1)
        PreferencesWizard.addPage(self.preferencesPage)
        self.serverPage = ServerWizardPage()
        self.serverPage.setObjectName(_fromUtf8("serverPage"))
        self.serverLayout = QtGui.QGridLayout(self.serverPage)
        self.serverLayout.setObjectName(_fromUtf8("serverLayout"))
        self.serverWidget = ServerWidget(self.serverPage)
        self.serverWidget.setObjectName(_fromUtf8("serverWidget"))
        self.serverLayout.addWidget(self.serverWidget, 0, 0, 1, 1)
        PreferencesWizard.addPage(self.serverPage)
        self.globalPage = GlobalPage()
        self.globalPage.setObjectName(_fromUtf8("globalPage"))
        self.gridLayout_3 = QtGui.QGridLayout(self.globalPage)
        self.gridLayout_3.setObjectName(_fromUtf8("gridLayout_3"))
        self.snappingLabel = QtGui.QLabel(self.globalPage)
        self.snappingLabel.setObjectName(_fromUtf8("snappingLabel"))
        self.gridLayout_3.addWidget(self.snappingLabel, 2, 0, 1, 1)
        self.fontLabel = QtGui.QLabel(self.globalPage)
        self.fontLabel.setObjectName(_fromUtf8("fontLabel"))
        self.gridLayout_3.addWidget(self.fontLabel, 1, 0, 1, 1)
        self.snappingToleranceSpin = QtGui.QDoubleSpinBox(self.globalPage)
        self.snappingToleranceSpin.setObjectName(_fromUtf8("snappingToleranceSpin"))
        self.gridLayout_3.addWidget(self.snappingToleranceSpin, 2, 1, 1, 1)
        self.crsAuthidLabel = QtGui.QLabel(self.globalPage)
        self.crsAuthidLabel.setObjectName(_fromUtf8("crsAuthidLabel"))
        self.gridLayout_3.addWidget(self.crsAuthidLabel, 0, 0, 1, 1)
        self.snappingUnitCombo = QtGui.QComboBox(self.globalPage)
        self.snappingUnitCombo.setObjectName(_fromUtf8("snappingUnitCombo"))
        self.gridLayout_3.addWidget(self.snappingUnitCombo, 2, 2, 1, 1)
        self.fontCombo = QtGui.QFontComboBox(self.globalPage)
        self.fontCombo.setObjectName(_fromUtf8("fontCombo"))
        self.gridLayout_3.addWidget(self.fontCombo, 1, 1, 1, 2)
        self.crsWidget = QgsProjectionSelectionWidget(self.globalPage)
        self.crsWidget.setObjectName(_fromUtf8("crsWidget"))
        self.gridLayout_3.addWidget(self.crsWidget, 0, 1, 1, 2)
        PreferencesWizard.addPage(self.globalPage)

        self.retranslateUi(PreferencesWizard)
        QtCore.QMetaObject.connectSlotsByName(PreferencesWizard)

    def retranslateUi(self, PreferencesWizard):
        PreferencesWizard.setWindowTitle(_translate("PreferencesWizard", "ARKspatial Preferences Wizard", None))
        self.welcomePage.setTitle(_translate("PreferencesWizard", "ARKspatial Preferences Wizard", None))
        self.welcomePage.setSubTitle(_translate("PreferencesWizard", "This is the first time you have run ARKspatial, so we need to set up some default settings first before creating a new project.", None))
        self.preferencesPage.setTitle(_translate("PreferencesWizard", "Project Preferences", None))
        self.preferencesPage.setSubTitle(_translate("PreferencesWizard", "Enter the default location for saving your projects, and your personal details for recording metadata.", None))
        self.serverPage.setTitle(_translate("PreferencesWizard", "ARK Server Settings", None))
        self.serverPage.setSubTitle(_translate("PreferencesWizard", "If you use an ARK database for project management or site recording, enter the server details to enable automatic population of your project details.", None))
        self.globalPage.setTitle(_translate("PreferencesWizard", "QGIS Preferences", None))
        self.globalPage.setSubTitle(_translate("PreferencesWizard", "We recommend you set some sensible defaults for your QGIS preferences.", None))
        self.snappingLabel.setText(_translate("PreferencesWizard", "Snapping:", None))
        self.fontLabel.setText(_translate("PreferencesWizard", "Font:", None))
        self.crsAuthidLabel.setText(_translate("PreferencesWizard", "CRS:", None))

from ..preferences_widget import PreferencesWidget
from ..preferences_wizard_page import PreferencesWizardPage
from ..server_widget import ServerWidget
from ..server_wizard_page import ServerWizardPage
from ..wizard_page import GlobalPage
from qgis.gui import QgsProjectionSelectionWidget
