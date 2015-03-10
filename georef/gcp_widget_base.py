# -*- coding: utf-8 -*-

# Form implementation generated from reading ui file 'georef/gcp_widget_base.ui'
#
# Created: Tue Mar 10 10:46:33 2015
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

class Ui_GcpWidget(object):
    def setupUi(self, GcpWidget):
        GcpWidget.setObjectName(_fromUtf8("GcpWidget"))
        GcpWidget.resize(508, 391)
        self.verticalLayout = QtGui.QVBoxLayout(GcpWidget)
        self.verticalLayout.setObjectName(_fromUtf8("verticalLayout"))
        self.gcpView = GeorefGraphicsView(GcpWidget)
        self.gcpView.setInteractive(False)
        self.gcpView.setDragMode(QtGui.QGraphicsView.NoDrag)
        self.gcpView.setObjectName(_fromUtf8("gcpView"))
        self.verticalLayout.addWidget(self.gcpView)
        self.gridLayout = QtGui.QGridLayout()
        self.gridLayout.setObjectName(_fromUtf8("gridLayout"))
        self.autoButton = QtGui.QPushButton(GcpWidget)
        self.autoButton.setEnabled(False)
        self.autoButton.setObjectName(_fromUtf8("autoButton"))
        self.gridLayout.addWidget(self.autoButton, 0, 0, 1, 1)
        self.localLabel = QtGui.QLabel(GcpWidget)
        self.localLabel.setObjectName(_fromUtf8("localLabel"))
        self.gridLayout.addWidget(self.localLabel, 0, 1, 1, 1)
        self.crsLabel = QtGui.QLabel(GcpWidget)
        self.crsLabel.setObjectName(_fromUtf8("crsLabel"))
        self.gridLayout.addWidget(self.crsLabel, 0, 2, 1, 1)
        self.rawLabel = QtGui.QLabel(GcpWidget)
        self.rawLabel.setObjectName(_fromUtf8("rawLabel"))
        self.gridLayout.addWidget(self.rawLabel, 0, 3, 1, 1)
        self.xLabel = QtGui.QLabel(GcpWidget)
        self.xLabel.setObjectName(_fromUtf8("xLabel"))
        self.gridLayout.addWidget(self.xLabel, 1, 0, 1, 1)
        self.localXSpin = QtGui.QSpinBox(GcpWidget)
        self.localXSpin.setReadOnly(True)
        self.localXSpin.setMaximum(9999)
        self.localXSpin.setObjectName(_fromUtf8("localXSpin"))
        self.gridLayout.addWidget(self.localXSpin, 1, 1, 1, 1)
        self.crsXSpin = QtGui.QDoubleSpinBox(GcpWidget)
        self.crsXSpin.setReadOnly(True)
        self.crsXSpin.setDecimals(3)
        self.crsXSpin.setMaximum(999999.999)
        self.crsXSpin.setObjectName(_fromUtf8("crsXSpin"))
        self.gridLayout.addWidget(self.crsXSpin, 1, 2, 1, 1)
        self.rawXSpin = QtGui.QDoubleSpinBox(GcpWidget)
        self.rawXSpin.setDecimals(1)
        self.rawXSpin.setMaximum(99999.9)
        self.rawXSpin.setObjectName(_fromUtf8("rawXSpin"))
        self.gridLayout.addWidget(self.rawXSpin, 1, 3, 1, 1)
        self.yLabel = QtGui.QLabel(GcpWidget)
        self.yLabel.setObjectName(_fromUtf8("yLabel"))
        self.gridLayout.addWidget(self.yLabel, 2, 0, 1, 1)
        self.localYSpin = QtGui.QSpinBox(GcpWidget)
        self.localYSpin.setReadOnly(True)
        self.localYSpin.setMaximum(9999)
        self.localYSpin.setObjectName(_fromUtf8("localYSpin"))
        self.gridLayout.addWidget(self.localYSpin, 2, 1, 1, 1)
        self.crsYSpin = QtGui.QDoubleSpinBox(GcpWidget)
        self.crsYSpin.setReadOnly(True)
        self.crsYSpin.setDecimals(3)
        self.crsYSpin.setMaximum(999999.999)
        self.crsYSpin.setObjectName(_fromUtf8("crsYSpin"))
        self.gridLayout.addWidget(self.crsYSpin, 2, 2, 1, 1)
        self.rawYSpin = QtGui.QDoubleSpinBox(GcpWidget)
        self.rawYSpin.setDecimals(1)
        self.rawYSpin.setMaximum(99999.9)
        self.rawYSpin.setObjectName(_fromUtf8("rawYSpin"))
        self.gridLayout.addWidget(self.rawYSpin, 2, 3, 1, 1)
        self.verticalLayout.addLayout(self.gridLayout)

        self.retranslateUi(GcpWidget)
        QtCore.QMetaObject.connectSlotsByName(GcpWidget)

    def retranslateUi(self, GcpWidget):
        GcpWidget.setWindowTitle(_translate("GcpWidget", "Form", None))
        self.autoButton.setText(_translate("GcpWidget", "Auto", None))
        self.localLabel.setText(_translate("GcpWidget", "Local:", None))
        self.crsLabel.setText(_translate("GcpWidget", "CRS:", None))
        self.rawLabel.setText(_translate("GcpWidget", "Raw:", None))
        self.xLabel.setText(_translate("GcpWidget", "X:", None))
        self.yLabel.setText(_translate("GcpWidget", "Y:", None))

from georef_graphics_view import GeorefGraphicsView
