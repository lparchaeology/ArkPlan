# -*- coding: utf-8 -*-

# Form implementation generated from reading ui file 'src/edit_widget_base.ui'
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

class Ui_EditWidget(object):
    def setupUi(self, EditWidget):
        EditWidget.setObjectName(_fromUtf8("EditWidget"))
        EditWidget.resize(265, 128)
        self.verticalLayout = QtGui.QVBoxLayout(EditWidget)
        self.verticalLayout.setObjectName(_fromUtf8("verticalLayout"))
        self.gridLayout = QtGui.QGridLayout()
        self.gridLayout.setObjectName(_fromUtf8("gridLayout"))
        self.snapPlanPointsTool = QtGui.QToolButton(EditWidget)
        self.snapPlanPointsTool.setCheckable(True)
        self.snapPlanPointsTool.setPopupMode(QtGui.QToolButton.MenuButtonPopup)
        self.snapPlanPointsTool.setObjectName(_fromUtf8("snapPlanPointsTool"))
        self.gridLayout.addWidget(self.snapPlanPointsTool, 2, 1, 1, 1)
        self.snapPlanLabel = QtGui.QLabel(EditWidget)
        self.snapPlanLabel.setObjectName(_fromUtf8("snapPlanLabel"))
        self.gridLayout.addWidget(self.snapPlanLabel, 2, 0, 1, 1)
        self.snapLinesLabel = QtGui.QLabel(EditWidget)
        self.snapLinesLabel.setObjectName(_fromUtf8("snapLinesLabel"))
        self.gridLayout.addWidget(self.snapLinesLabel, 0, 2, 1, 1)
        self.snapPlanLinesTool = QtGui.QToolButton(EditWidget)
        self.snapPlanLinesTool.setCheckable(True)
        self.snapPlanLinesTool.setPopupMode(QtGui.QToolButton.MenuButtonPopup)
        self.snapPlanLinesTool.setObjectName(_fromUtf8("snapPlanLinesTool"))
        self.gridLayout.addWidget(self.snapPlanLinesTool, 2, 2, 1, 1)
        self.snapBufferLinesTool = QtGui.QToolButton(EditWidget)
        self.snapBufferLinesTool.setCheckable(True)
        self.snapBufferLinesTool.setPopupMode(QtGui.QToolButton.MenuButtonPopup)
        self.snapBufferLinesTool.setObjectName(_fromUtf8("snapBufferLinesTool"))
        self.gridLayout.addWidget(self.snapBufferLinesTool, 1, 2, 1, 1)
        self.snapBufferPointsTool = QtGui.QToolButton(EditWidget)
        self.snapBufferPointsTool.setCheckable(True)
        self.snapBufferPointsTool.setPopupMode(QtGui.QToolButton.MenuButtonPopup)
        self.snapBufferPointsTool.setObjectName(_fromUtf8("snapBufferPointsTool"))
        self.gridLayout.addWidget(self.snapBufferPointsTool, 1, 1, 1, 1)
        self.snapBufferPolygonsTool = QtGui.QToolButton(EditWidget)
        self.snapBufferPolygonsTool.setCheckable(True)
        self.snapBufferPolygonsTool.setPopupMode(QtGui.QToolButton.MenuButtonPopup)
        self.snapBufferPolygonsTool.setObjectName(_fromUtf8("snapBufferPolygonsTool"))
        self.gridLayout.addWidget(self.snapBufferPolygonsTool, 1, 3, 1, 1)
        self.snapPolygonsLabel = QtGui.QLabel(EditWidget)
        self.snapPolygonsLabel.setObjectName(_fromUtf8("snapPolygonsLabel"))
        self.gridLayout.addWidget(self.snapPolygonsLabel, 0, 3, 1, 1)
        self.snapBuffersLabel = QtGui.QLabel(EditWidget)
        self.snapBuffersLabel.setObjectName(_fromUtf8("snapBuffersLabel"))
        self.gridLayout.addWidget(self.snapBuffersLabel, 1, 0, 1, 1)
        self.snapPlanPolygonsTool = QtGui.QToolButton(EditWidget)
        self.snapPlanPolygonsTool.setCheckable(True)
        self.snapPlanPolygonsTool.setPopupMode(QtGui.QToolButton.MenuButtonPopup)
        self.snapPlanPolygonsTool.setObjectName(_fromUtf8("snapPlanPolygonsTool"))
        self.gridLayout.addWidget(self.snapPlanPolygonsTool, 2, 3, 1, 1)
        self.snapBasePointsTool = QtGui.QToolButton(EditWidget)
        self.snapBasePointsTool.setCheckable(True)
        self.snapBasePointsTool.setPopupMode(QtGui.QToolButton.MenuButtonPopup)
        self.snapBasePointsTool.setObjectName(_fromUtf8("snapBasePointsTool"))
        self.gridLayout.addWidget(self.snapBasePointsTool, 3, 1, 1, 1)
        self.snapBaseLabel = QtGui.QLabel(EditWidget)
        self.snapBaseLabel.setObjectName(_fromUtf8("snapBaseLabel"))
        self.gridLayout.addWidget(self.snapBaseLabel, 3, 0, 1, 1)
        self.snapBaseLinesTool = QtGui.QToolButton(EditWidget)
        self.snapBaseLinesTool.setCheckable(True)
        self.snapBaseLinesTool.setPopupMode(QtGui.QToolButton.MenuButtonPopup)
        self.snapBaseLinesTool.setObjectName(_fromUtf8("snapBaseLinesTool"))
        self.gridLayout.addWidget(self.snapBaseLinesTool, 3, 2, 1, 1)
        self.snapBasePolygonsTool = QtGui.QToolButton(EditWidget)
        self.snapBasePolygonsTool.setCheckable(True)
        self.snapBasePolygonsTool.setPopupMode(QtGui.QToolButton.MenuButtonPopup)
        self.snapBasePolygonsTool.setObjectName(_fromUtf8("snapBasePolygonsTool"))
        self.gridLayout.addWidget(self.snapBasePolygonsTool, 3, 3, 1, 1)
        self.snapPointsLabel = QtGui.QLabel(EditWidget)
        self.snapPointsLabel.setObjectName(_fromUtf8("snapPointsLabel"))
        self.gridLayout.addWidget(self.snapPointsLabel, 0, 1, 1, 1)
        self.verticalLayout.addLayout(self.gridLayout)
        self.snapPlanLabel.setBuddy(self.snapPlanPointsTool)
        self.snapBuffersLabel.setBuddy(self.snapBufferPointsTool)
        self.snapBaseLabel.setBuddy(self.snapBasePointsTool)

        self.retranslateUi(EditWidget)
        QtCore.QMetaObject.connectSlotsByName(EditWidget)
        EditWidget.setTabOrder(self.snapBufferPointsTool, self.snapBufferLinesTool)
        EditWidget.setTabOrder(self.snapBufferLinesTool, self.snapBufferPolygonsTool)
        EditWidget.setTabOrder(self.snapBufferPolygonsTool, self.snapPlanPointsTool)
        EditWidget.setTabOrder(self.snapPlanPointsTool, self.snapPlanLinesTool)
        EditWidget.setTabOrder(self.snapPlanLinesTool, self.snapPlanPolygonsTool)
        EditWidget.setTabOrder(self.snapPlanPolygonsTool, self.snapBasePointsTool)
        EditWidget.setTabOrder(self.snapBasePointsTool, self.snapBaseLinesTool)
        EditWidget.setTabOrder(self.snapBaseLinesTool, self.snapBasePolygonsTool)

    def retranslateUi(self, EditWidget):
        EditWidget.setWindowTitle(_translate("EditWidget", "Form", None))
        self.snapPlanPointsTool.setText(_translate("EditWidget", "...", None))
        self.snapPlanLabel.setText(_translate("EditWidget", "Snap Plan Data:", None))
        self.snapLinesLabel.setText(_translate("EditWidget", "Lines", None))
        self.snapPlanLinesTool.setText(_translate("EditWidget", "...", None))
        self.snapBufferLinesTool.setText(_translate("EditWidget", "...", None))
        self.snapBufferPointsTool.setText(_translate("EditWidget", "...", None))
        self.snapBufferPolygonsTool.setText(_translate("EditWidget", "...", None))
        self.snapPolygonsLabel.setText(_translate("EditWidget", "Polys", None))
        self.snapBuffersLabel.setText(_translate("EditWidget", "Snap Buffers:", None))
        self.snapPlanPolygonsTool.setText(_translate("EditWidget", "...", None))
        self.snapBasePointsTool.setText(_translate("EditWidget", "...", None))
        self.snapBaseLabel.setText(_translate("EditWidget", "Snap Base Data:", None))
        self.snapBaseLinesTool.setText(_translate("EditWidget", "...", None))
        self.snapBasePolygonsTool.setText(_translate("EditWidget", "...", None))
        self.snapPointsLabel.setText(_translate("EditWidget", "Points", None))

