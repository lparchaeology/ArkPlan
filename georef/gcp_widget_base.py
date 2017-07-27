# -*- coding: utf-8 -*-

# Form implementation generated from reading ui file 'georef/gcp_widget_base.ui'
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

class Ui_GcpWidget(object):
    def setupUi(self, GcpWidget):
        GcpWidget.setObjectName(_fromUtf8("GcpWidget"))
        GcpWidget.resize(508, 391)
        self.verticalLayout = QtGui.QVBoxLayout(GcpWidget)
        self.verticalLayout.setMargin(0)
        self.verticalLayout.setObjectName(_fromUtf8("verticalLayout"))
        self.gcpView = GeorefGraphicsView(GcpWidget)
        self.gcpView.setVerticalScrollBarPolicy(QtCore.Qt.ScrollBarAlwaysOff)
        self.gcpView.setHorizontalScrollBarPolicy(QtCore.Qt.ScrollBarAlwaysOff)
        self.gcpView.setInteractive(False)
        self.gcpView.setDragMode(QtGui.QGraphicsView.NoDrag)
        self.gcpView.setObjectName(_fromUtf8("gcpView"))
        self.verticalLayout.addWidget(self.gcpView)
        self.gridLayout = QtGui.QGridLayout()
        self.gridLayout.setObjectName(_fromUtf8("gridLayout"))
        self.rawYSpin = QtGui.QDoubleSpinBox(GcpWidget)
        self.rawYSpin.setDecimals(1)
        self.rawYSpin.setMaximum(99999.9)
        self.rawYSpin.setObjectName(_fromUtf8("rawYSpin"))
        self.gridLayout.addWidget(self.rawYSpin, 2, 3, 1, 1)
        self.localLabel = QtGui.QLabel(GcpWidget)
        self.localLabel.setObjectName(_fromUtf8("localLabel"))
        self.gridLayout.addWidget(self.localLabel, 0, 1, 1, 1)
        self.rawLabel = QtGui.QLabel(GcpWidget)
        self.rawLabel.setObjectName(_fromUtf8("rawLabel"))
        self.gridLayout.addWidget(self.rawLabel, 0, 3, 1, 1)
        self.mapYSpin = QtGui.QDoubleSpinBox(GcpWidget)
        self.mapYSpin.setReadOnly(True)
        self.mapYSpin.setDecimals(3)
        self.mapYSpin.setMaximum(999999.999)
        self.mapYSpin.setObjectName(_fromUtf8("mapYSpin"))
        self.gridLayout.addWidget(self.mapYSpin, 2, 2, 1, 1)
        self.rawXSpin = QtGui.QDoubleSpinBox(GcpWidget)
        self.rawXSpin.setDecimals(1)
        self.rawXSpin.setMaximum(99999.9)
        self.rawXSpin.setObjectName(_fromUtf8("rawXSpin"))
        self.gridLayout.addWidget(self.rawXSpin, 1, 3, 1, 1)
        self.mapLabel = QtGui.QLabel(GcpWidget)
        self.mapLabel.setObjectName(_fromUtf8("mapLabel"))
        self.gridLayout.addWidget(self.mapLabel, 0, 2, 1, 1)
        self.localYSpin = QtGui.QSpinBox(GcpWidget)
        self.localYSpin.setReadOnly(True)
        self.localYSpin.setMaximum(9999)
        self.localYSpin.setObjectName(_fromUtf8("localYSpin"))
        self.gridLayout.addWidget(self.localYSpin, 2, 1, 1, 1)
        self.mapXSpin = QtGui.QDoubleSpinBox(GcpWidget)
        self.mapXSpin.setReadOnly(True)
        self.mapXSpin.setDecimals(3)
        self.mapXSpin.setMaximum(999999.999)
        self.mapXSpin.setObjectName(_fromUtf8("mapXSpin"))
        self.gridLayout.addWidget(self.mapXSpin, 1, 2, 1, 1)
        self.localXSpin = QtGui.QSpinBox(GcpWidget)
        self.localXSpin.setReadOnly(True)
        self.localXSpin.setMaximum(9999)
        self.localXSpin.setObjectName(_fromUtf8("localXSpin"))
        self.gridLayout.addWidget(self.localXSpin, 1, 1, 1, 1)
        self.xLabel = QtGui.QLabel(GcpWidget)
        sizePolicy = QtGui.QSizePolicy(QtGui.QSizePolicy.Fixed, QtGui.QSizePolicy.Preferred)
        sizePolicy.setHorizontalStretch(0)
        sizePolicy.setVerticalStretch(0)
        sizePolicy.setHeightForWidth(self.xLabel.sizePolicy().hasHeightForWidth())
        self.xLabel.setSizePolicy(sizePolicy)
        self.xLabel.setObjectName(_fromUtf8("xLabel"))
        self.gridLayout.addWidget(self.xLabel, 1, 0, 1, 1)
        self.yLabel = QtGui.QLabel(GcpWidget)
        sizePolicy = QtGui.QSizePolicy(QtGui.QSizePolicy.Fixed, QtGui.QSizePolicy.Preferred)
        sizePolicy.setHorizontalStretch(0)
        sizePolicy.setVerticalStretch(0)
        sizePolicy.setHeightForWidth(self.yLabel.sizePolicy().hasHeightForWidth())
        self.yLabel.setSizePolicy(sizePolicy)
        self.yLabel.setObjectName(_fromUtf8("yLabel"))
        self.gridLayout.addWidget(self.yLabel, 2, 0, 1, 1)
        self.verticalLayout.addLayout(self.gridLayout)

        self.retranslateUi(GcpWidget)
        QtCore.QMetaObject.connectSlotsByName(GcpWidget)

    def retranslateUi(self, GcpWidget):
        GcpWidget.setWindowTitle(_translate("GcpWidget", "Form", None))
        self.localLabel.setText(_translate("GcpWidget", "Local:", None))
        self.rawLabel.setText(_translate("GcpWidget", "Raw:", None))
        self.mapLabel.setText(_translate("GcpWidget", "Map:", None))
        self.xLabel.setText(_translate("GcpWidget", "X:", None))
        self.yLabel.setText(_translate("GcpWidget", "Y:", None))

from georef_graphics_view import GeorefGraphicsView
