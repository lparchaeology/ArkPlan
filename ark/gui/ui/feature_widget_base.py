# -*- coding: utf-8 -*-

# Form implementation generated from reading ui file 'src/feature_widget_base.ui'
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

class Ui_FeatureWidget(object):
    def setupUi(self, FeatureWidget):
        FeatureWidget.setObjectName(_fromUtf8("FeatureWidget"))
        FeatureWidget.resize(352, 191)
        self.gridLayout = QtGui.QGridLayout(FeatureWidget)
        self.gridLayout.setSizeConstraint(QtGui.QLayout.SetMinAndMaxSize)
        self.gridLayout.setMargin(0)
        self.gridLayout.setObjectName(_fromUtf8("gridLayout"))
        self.pointToolGroup = QtGui.QFrame(FeatureWidget)
        font = QtGui.QFont()
        font.setPointSize(10)
        self.pointToolGroup.setFont(font)
        self.pointToolGroup.setObjectName(_fromUtf8("pointToolGroup"))
        self.pointToolLayout = QtGui.QGridLayout(self.pointToolGroup)
        self.pointToolLayout.setSizeConstraint(QtGui.QLayout.SetMinAndMaxSize)
        self.pointToolLayout.setMargin(0)
        self.pointToolLayout.setObjectName(_fromUtf8("pointToolLayout"))
        self.gridLayout.addWidget(self.pointToolGroup, 5, 0, 1, 3)
        self.polygonToolGroup = QtGui.QFrame(FeatureWidget)
        font = QtGui.QFont()
        font.setPointSize(10)
        self.polygonToolGroup.setFont(font)
        self.polygonToolGroup.setObjectName(_fromUtf8("polygonToolGroup"))
        self.polygonToolLayout = QtGui.QGridLayout(self.polygonToolGroup)
        self.polygonToolLayout.setSizeConstraint(QtGui.QLayout.SetMinAndMaxSize)
        self.polygonToolLayout.setMargin(0)
        self.polygonToolLayout.setObjectName(_fromUtf8("polygonToolLayout"))
        self.gridLayout.addWidget(self.polygonToolGroup, 9, 0, 1, 3)
        self.line_2 = QtGui.QFrame(FeatureWidget)
        self.line_2.setFrameShape(QtGui.QFrame.HLine)
        self.line_2.setFrameShadow(QtGui.QFrame.Sunken)
        self.line_2.setObjectName(_fromUtf8("line_2"))
        self.gridLayout.addWidget(self.line_2, 6, 0, 1, 3)
        self.lineToolGroup = QtGui.QFrame(FeatureWidget)
        font = QtGui.QFont()
        font.setPointSize(10)
        self.lineToolGroup.setFont(font)
        self.lineToolGroup.setObjectName(_fromUtf8("lineToolGroup"))
        self.lineToolLayout = QtGui.QGridLayout(self.lineToolGroup)
        self.lineToolLayout.setSizeConstraint(QtGui.QLayout.SetMinAndMaxSize)
        self.lineToolLayout.setMargin(0)
        self.lineToolLayout.setObjectName(_fromUtf8("lineToolLayout"))
        self.gridLayout.addWidget(self.lineToolGroup, 7, 0, 1, 3)
        spacerItem = QtGui.QSpacerItem(20, 40, QtGui.QSizePolicy.Minimum, QtGui.QSizePolicy.Expanding)
        self.gridLayout.addItem(spacerItem, 12, 0, 1, 3)
        self.commentLabel = QtGui.QLabel(FeatureWidget)
        self.commentLabel.setObjectName(_fromUtf8("commentLabel"))
        self.gridLayout.addWidget(self.commentLabel, 3, 0, 1, 1)
        self.featureLabel = QtGui.QLabel(FeatureWidget)
        self.featureLabel.setObjectName(_fromUtf8("featureLabel"))
        self.gridLayout.addWidget(self.featureLabel, 1, 0, 1, 1)
        self.line = QtGui.QFrame(FeatureWidget)
        self.line.setFrameShape(QtGui.QFrame.HLine)
        self.line.setFrameShadow(QtGui.QFrame.Sunken)
        self.line.setObjectName(_fromUtf8("line"))
        self.gridLayout.addWidget(self.line, 4, 0, 1, 3)
        self.commentEdit = QtGui.QLineEdit(FeatureWidget)
        self.commentEdit.setObjectName(_fromUtf8("commentEdit"))
        self.gridLayout.addWidget(self.commentEdit, 3, 1, 1, 2)
        self.horizontalLayout_2 = QtGui.QHBoxLayout()
        self.horizontalLayout_2.setObjectName(_fromUtf8("horizontalLayout_2"))
        self.classCombo = QtGui.QComboBox(FeatureWidget)
        self.classCombo.setEnabled(False)
        self.classCombo.setObjectName(_fromUtf8("classCombo"))
        self.horizontalLayout_2.addWidget(self.classCombo)
        self.idEdit = QtGui.QLineEdit(FeatureWidget)
        self.idEdit.setObjectName(_fromUtf8("idEdit"))
        self.horizontalLayout_2.addWidget(self.idEdit)
        self.gridLayout.addLayout(self.horizontalLayout_2, 1, 1, 1, 2)
        self.labelLabel = QtGui.QLabel(FeatureWidget)
        self.labelLabel.setObjectName(_fromUtf8("labelLabel"))
        self.gridLayout.addWidget(self.labelLabel, 2, 0, 1, 1)
        self.labelEdit = QtGui.QLineEdit(FeatureWidget)
        self.labelEdit.setObjectName(_fromUtf8("labelEdit"))
        self.gridLayout.addWidget(self.labelEdit, 2, 1, 1, 2)
        self.line_3 = QtGui.QFrame(FeatureWidget)
        self.line_3.setFrameShape(QtGui.QFrame.HLine)
        self.line_3.setFrameShadow(QtGui.QFrame.Sunken)
        self.line_3.setObjectName(_fromUtf8("line_3"))
        self.gridLayout.addWidget(self.line_3, 8, 0, 1, 3)
        self.commentLabel.setBuddy(self.commentEdit)
        self.featureLabel.setBuddy(self.classCombo)

        self.retranslateUi(FeatureWidget)
        QtCore.QMetaObject.connectSlotsByName(FeatureWidget)
        FeatureWidget.setTabOrder(self.classCombo, self.commentEdit)

    def retranslateUi(self, FeatureWidget):
        FeatureWidget.setWindowTitle(_translate("FeatureWidget", "FeatureWidget", None))
        self.commentLabel.setText(_translate("FeatureWidget", "Comment:", None))
        self.featureLabel.setText(_translate("FeatureWidget", "Feature:", None))
        self.labelLabel.setText(_translate("FeatureWidget", "Label:", None))

import resources
