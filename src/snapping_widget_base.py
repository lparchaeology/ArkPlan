# -*- coding: utf-8 -*-

# Form implementation generated from reading ui file 'src/snapping_widget_base.ui'
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

class Ui_SnappingWidget(object):
    def setupUi(self, SnappingWidget):
        SnappingWidget.setObjectName(_fromUtf8("SnappingWidget"))
        SnappingWidget.resize(292, 186)
        sizePolicy = QtGui.QSizePolicy(QtGui.QSizePolicy.Preferred, QtGui.QSizePolicy.Minimum)
        sizePolicy.setHorizontalStretch(0)
        sizePolicy.setVerticalStretch(0)
        sizePolicy.setHeightForWidth(SnappingWidget.sizePolicy().hasHeightForWidth())
        SnappingWidget.setSizePolicy(sizePolicy)
        self.gridLayout = QtGui.QGridLayout(SnappingWidget)
        self.gridLayout.setObjectName(_fromUtf8("gridLayout"))
        self.snapPointsLabel = QtGui.QLabel(SnappingWidget)
        self.snapPointsLabel.setObjectName(_fromUtf8("snapPointsLabel"))
        self.gridLayout.addWidget(self.snapPointsLabel, 0, 1, 1, 1)
        self.snapLinesLabel = QtGui.QLabel(SnappingWidget)
        self.snapLinesLabel.setObjectName(_fromUtf8("snapLinesLabel"))
        self.gridLayout.addWidget(self.snapLinesLabel, 0, 2, 1, 1)
        self.snapPolygonsLabel = QtGui.QLabel(SnappingWidget)
        self.snapPolygonsLabel.setObjectName(_fromUtf8("snapPolygonsLabel"))
        self.gridLayout.addWidget(self.snapPolygonsLabel, 0, 3, 1, 1)
        self.snapBuffersLabel = QtGui.QLabel(SnappingWidget)
        self.snapBuffersLabel.setObjectName(_fromUtf8("snapBuffersLabel"))
        self.gridLayout.addWidget(self.snapBuffersLabel, 1, 0, 1, 1)
        self.snapBufferPointsTool = QtGui.QToolButton(SnappingWidget)
        self.snapBufferPointsTool.setCheckable(True)
        self.snapBufferPointsTool.setPopupMode(QtGui.QToolButton.MenuButtonPopup)
        self.snapBufferPointsTool.setObjectName(_fromUtf8("snapBufferPointsTool"))
        self.gridLayout.addWidget(self.snapBufferPointsTool, 1, 1, 1, 1)
        self.snapBufferLinesTool = QtGui.QToolButton(SnappingWidget)
        self.snapBufferLinesTool.setCheckable(True)
        self.snapBufferLinesTool.setPopupMode(QtGui.QToolButton.MenuButtonPopup)
        self.snapBufferLinesTool.setObjectName(_fromUtf8("snapBufferLinesTool"))
        self.gridLayout.addWidget(self.snapBufferLinesTool, 1, 2, 1, 1)
        self.snapBufferPolygonsTool = QtGui.QToolButton(SnappingWidget)
        self.snapBufferPolygonsTool.setCheckable(True)
        self.snapBufferPolygonsTool.setPopupMode(QtGui.QToolButton.MenuButtonPopup)
        self.snapBufferPolygonsTool.setObjectName(_fromUtf8("snapBufferPolygonsTool"))
        self.gridLayout.addWidget(self.snapBufferPolygonsTool, 1, 3, 1, 1)
        self.snapPlanLabel = QtGui.QLabel(SnappingWidget)
        self.snapPlanLabel.setObjectName(_fromUtf8("snapPlanLabel"))
        self.gridLayout.addWidget(self.snapPlanLabel, 2, 0, 1, 1)
        self.snapPlanPointsTool = QtGui.QToolButton(SnappingWidget)
        self.snapPlanPointsTool.setCheckable(True)
        self.snapPlanPointsTool.setPopupMode(QtGui.QToolButton.MenuButtonPopup)
        self.snapPlanPointsTool.setObjectName(_fromUtf8("snapPlanPointsTool"))
        self.gridLayout.addWidget(self.snapPlanPointsTool, 2, 1, 1, 1)
        self.snapPlanLinesTool = QtGui.QToolButton(SnappingWidget)
        self.snapPlanLinesTool.setCheckable(True)
        self.snapPlanLinesTool.setPopupMode(QtGui.QToolButton.MenuButtonPopup)
        self.snapPlanLinesTool.setObjectName(_fromUtf8("snapPlanLinesTool"))
        self.gridLayout.addWidget(self.snapPlanLinesTool, 2, 2, 1, 1)
        self.snapPlanPolygonsTool = QtGui.QToolButton(SnappingWidget)
        self.snapPlanPolygonsTool.setCheckable(True)
        self.snapPlanPolygonsTool.setPopupMode(QtGui.QToolButton.MenuButtonPopup)
        self.snapPlanPolygonsTool.setObjectName(_fromUtf8("snapPlanPolygonsTool"))
        self.gridLayout.addWidget(self.snapPlanPolygonsTool, 2, 3, 1, 1)
        self.snapBaseLabel = QtGui.QLabel(SnappingWidget)
        self.snapBaseLabel.setObjectName(_fromUtf8("snapBaseLabel"))
        self.gridLayout.addWidget(self.snapBaseLabel, 3, 0, 1, 1)
        self.snapBasePointsTool = QtGui.QToolButton(SnappingWidget)
        self.snapBasePointsTool.setCheckable(True)
        self.snapBasePointsTool.setPopupMode(QtGui.QToolButton.MenuButtonPopup)
        self.snapBasePointsTool.setObjectName(_fromUtf8("snapBasePointsTool"))
        self.gridLayout.addWidget(self.snapBasePointsTool, 3, 1, 1, 1)
        self.snapBaseLinesTool = QtGui.QToolButton(SnappingWidget)
        self.snapBaseLinesTool.setCheckable(True)
        self.snapBaseLinesTool.setPopupMode(QtGui.QToolButton.MenuButtonPopup)
        self.snapBaseLinesTool.setObjectName(_fromUtf8("snapBaseLinesTool"))
        self.gridLayout.addWidget(self.snapBaseLinesTool, 3, 2, 1, 1)
        self.snapBasePolygonsTool = QtGui.QToolButton(SnappingWidget)
        self.snapBasePolygonsTool.setCheckable(True)
        self.snapBasePolygonsTool.setPopupMode(QtGui.QToolButton.MenuButtonPopup)
        self.snapBasePolygonsTool.setObjectName(_fromUtf8("snapBasePolygonsTool"))
        self.gridLayout.addWidget(self.snapBasePolygonsTool, 3, 3, 1, 1)
        spacerItem = QtGui.QSpacerItem(238, 7, QtGui.QSizePolicy.Minimum, QtGui.QSizePolicy.Expanding)
        self.gridLayout.addItem(spacerItem, 4, 0, 1, 4)
        self.snapBuffersLabel.setBuddy(self.snapBufferPointsTool)
        self.snapPlanLabel.setBuddy(self.snapPlanPointsTool)
        self.snapBaseLabel.setBuddy(self.snapBasePointsTool)

        self.retranslateUi(SnappingWidget)
        QtCore.QMetaObject.connectSlotsByName(SnappingWidget)

    def retranslateUi(self, SnappingWidget):
        SnappingWidget.setWindowTitle(_translate("SnappingWidget", "GroupBox", None))
        SnappingWidget.setTitle(_translate("SnappingWidget", "Snapping Layers", None))
        self.snapPointsLabel.setText(_translate("SnappingWidget", "Points", None))
        self.snapLinesLabel.setText(_translate("SnappingWidget", "Lines", None))
        self.snapPolygonsLabel.setText(_translate("SnappingWidget", "Polys", None))
        self.snapBuffersLabel.setText(_translate("SnappingWidget", "Snap Buffers:", None))
        self.snapBufferPointsTool.setText(_translate("SnappingWidget", "...", None))
        self.snapBufferLinesTool.setText(_translate("SnappingWidget", "...", None))
        self.snapBufferPolygonsTool.setText(_translate("SnappingWidget", "...", None))
        self.snapPlanLabel.setText(_translate("SnappingWidget", "Snap Plan Data:", None))
        self.snapPlanPointsTool.setText(_translate("SnappingWidget", "...", None))
        self.snapPlanLinesTool.setText(_translate("SnappingWidget", "...", None))
        self.snapPlanPolygonsTool.setText(_translate("SnappingWidget", "...", None))
        self.snapBaseLabel.setText(_translate("SnappingWidget", "Snap Base Data:", None))
        self.snapBasePointsTool.setText(_translate("SnappingWidget", "...", None))
        self.snapBaseLinesTool.setText(_translate("SnappingWidget", "...", None))
        self.snapBasePolygonsTool.setText(_translate("SnappingWidget", "...", None))

