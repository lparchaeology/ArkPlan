# -*- coding: utf-8 -*-

# Form implementation generated from reading ui file 'ark_plan_elevation_base.ui'
#
# Created: Fri Jan  2 17:10:31 2015
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

class Ui_ArkPlanElevationBase(object):
    def setupUi(self, ArkPlanElevationBase):
        ArkPlanElevationBase.setObjectName(_fromUtf8("ArkPlanElevationBase"))
        ArkPlanElevationBase.resize(290, 105)
        self.verticalLayout = QtGui.QVBoxLayout(ArkPlanElevationBase)
        self.verticalLayout.setObjectName(_fromUtf8("verticalLayout"))
        self.m_elevationLabel = QtGui.QLabel(ArkPlanElevationBase)
        self.m_elevationLabel.setObjectName(_fromUtf8("m_elevationLabel"))
        self.verticalLayout.addWidget(self.m_elevationLabel)
        self.m_elevationSpinBox = QtGui.QDoubleSpinBox(ArkPlanElevationBase)
        self.m_elevationSpinBox.setObjectName(_fromUtf8("m_elevationSpinBox"))
        self.verticalLayout.addWidget(self.m_elevationSpinBox)
        self.m_elevationButtonBox = QtGui.QDialogButtonBox(ArkPlanElevationBase)
        self.m_elevationButtonBox.setOrientation(QtCore.Qt.Horizontal)
        self.m_elevationButtonBox.setStandardButtons(QtGui.QDialogButtonBox.Cancel|QtGui.QDialogButtonBox.Ok)
        self.m_elevationButtonBox.setObjectName(_fromUtf8("m_elevationButtonBox"))
        self.verticalLayout.addWidget(self.m_elevationButtonBox)

        self.retranslateUi(ArkPlanElevationBase)
        QtCore.QObject.connect(self.m_elevationButtonBox, QtCore.SIGNAL(_fromUtf8("accepted()")), ArkPlanElevationBase.ArkPlanDialogBase.accept)
        QtCore.QObject.connect(self.m_elevationButtonBox, QtCore.SIGNAL(_fromUtf8("rejected()")), ArkPlanElevationBase.ArkPlanDialogBase.reject)
        QtCore.QMetaObject.connectSlotsByName(ArkPlanElevationBase)

    def retranslateUi(self, ArkPlanElevationBase):
        ArkPlanElevationBase.setWindowTitle(_translate("ArkPlanElevationBase", "ArkPlan", None))
        self.m_elevationLabel.setText(_translate("ArkPlanElevationBase", "Please enter the elevation in meters (m):", None))
        self.m_elevationSpinBox.setSuffix(_translate("ArkPlanElevationBase", "m", None))

