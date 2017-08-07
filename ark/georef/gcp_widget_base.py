# -*- coding: utf-8 -*-

# Form implementation generated from reading ui file 'ark/georef/gcp_widget_base.ui'
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
        self.gcpView = GcpGraphicsView(GcpWidget)
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
        self.localLabel.setAlignment(QtCore.Qt.AlignCenter)
        self.localLabel.setObjectName(_fromUtf8("localLabel"))
        self.gridLayout.addWidget(self.localLabel, 0, 1, 1, 1)
        self.rawLabel = QtGui.QLabel(GcpWidget)
        self.rawLabel.setAlignment(QtCore.Qt.AlignCenter)
        self.rawLabel.setObjectName(_fromUtf8("rawLabel"))
        self.gridLayout.addWidget(self.rawLabel, 0, 3, 1, 1)
        self.rawXSpin = QtGui.QDoubleSpinBox(GcpWidget)
        self.rawXSpin.setDecimals(1)
        self.rawXSpin.setMaximum(99999.9)
        self.rawXSpin.setObjectName(_fromUtf8("rawXSpin"))
        self.gridLayout.addWidget(self.rawXSpin, 1, 3, 1, 1)
        self.mapLabel = QtGui.QLabel(GcpWidget)
        self.mapLabel.setAlignment(QtCore.Qt.AlignCenter)
        self.mapLabel.setObjectName(_fromUtf8("mapLabel"))
        self.gridLayout.addWidget(self.mapLabel, 0, 2, 1, 1)
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
        self.localX = QtGui.QLabel(GcpWidget)
        self.localX.setFrameShape(QtGui.QFrame.Panel)
        self.localX.setFrameShadow(QtGui.QFrame.Sunken)
        self.localX.setAlignment(QtCore.Qt.AlignRight|QtCore.Qt.AlignTrailing|QtCore.Qt.AlignVCenter)
        self.localX.setIndent(5)
        self.localX.setObjectName(_fromUtf8("localX"))
        self.gridLayout.addWidget(self.localX, 1, 1, 1, 1)
        self.localY = QtGui.QLabel(GcpWidget)
        self.localY.setFrameShape(QtGui.QFrame.Panel)
        self.localY.setFrameShadow(QtGui.QFrame.Sunken)
        self.localY.setAlignment(QtCore.Qt.AlignRight|QtCore.Qt.AlignTrailing|QtCore.Qt.AlignVCenter)
        self.localY.setIndent(5)
        self.localY.setObjectName(_fromUtf8("localY"))
        self.gridLayout.addWidget(self.localY, 2, 1, 1, 1)
        self.mapX = QtGui.QLabel(GcpWidget)
        self.mapX.setFrameShape(QtGui.QFrame.Panel)
        self.mapX.setFrameShadow(QtGui.QFrame.Sunken)
        self.mapX.setLineWidth(1)
        self.mapX.setAlignment(QtCore.Qt.AlignRight|QtCore.Qt.AlignTrailing|QtCore.Qt.AlignVCenter)
        self.mapX.setIndent(5)
        self.mapX.setObjectName(_fromUtf8("mapX"))
        self.gridLayout.addWidget(self.mapX, 1, 2, 1, 1)
        self.mapY = QtGui.QLabel(GcpWidget)
        self.mapY.setFrameShape(QtGui.QFrame.Panel)
        self.mapY.setFrameShadow(QtGui.QFrame.Sunken)
        self.mapY.setAlignment(QtCore.Qt.AlignRight|QtCore.Qt.AlignTrailing|QtCore.Qt.AlignVCenter)
        self.mapY.setIndent(5)
        self.mapY.setObjectName(_fromUtf8("mapY"))
        self.gridLayout.addWidget(self.mapY, 2, 2, 1, 1)
        self.verticalLayout.addLayout(self.gridLayout)
        self.localX.setBuddy(self.rawXSpin)
        self.localY.setBuddy(self.rawYSpin)
        self.mapX.setBuddy(self.rawXSpin)
        self.mapY.setBuddy(self.rawYSpin)

        self.retranslateUi(GcpWidget)
        QtCore.QMetaObject.connectSlotsByName(GcpWidget)
        GcpWidget.setTabOrder(self.gcpView, self.rawXSpin)
        GcpWidget.setTabOrder(self.rawXSpin, self.rawYSpin)

    def retranslateUi(self, GcpWidget):
        GcpWidget.setWindowTitle(_translate("GcpWidget", "Form", None))
        self.localLabel.setText(_translate("GcpWidget", "Local Grid", None))
        self.rawLabel.setText(_translate("GcpWidget", "Raw Image", None))
        self.mapLabel.setText(_translate("GcpWidget", "Map", None))
        self.xLabel.setText(_translate("GcpWidget", "X:", None))
        self.yLabel.setText(_translate("GcpWidget", "Y:", None))
        self.localX.setText(_translate("GcpWidget", "0.0", None))
        self.localY.setText(_translate("GcpWidget", "0.0", None))
        self.mapX.setText(_translate("GcpWidget", "0.0", None))
        self.mapY.setText(_translate("GcpWidget", "0.0", None))

from gcp_graphics_view import GcpGraphicsView
