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
        FeatureWidget.resize(341, 257)
        self.gridLayout = QtGui.QGridLayout(FeatureWidget)
        self.gridLayout.setMargin(0)
        self.gridLayout.setObjectName(_fromUtf8("gridLayout"))
        self.lineToolGroup = QtGui.QGroupBox(FeatureWidget)
        font = QtGui.QFont()
        font.setPointSize(10)
        self.lineToolGroup.setFont(font)
        self.lineToolGroup.setFlat(True)
        self.lineToolGroup.setObjectName(_fromUtf8("lineToolGroup"))
        self.lineToolLayout = QtGui.QGridLayout(self.lineToolGroup)
        self.lineToolLayout.setMargin(0)
        self.lineToolLayout.setObjectName(_fromUtf8("lineToolLayout"))
        self.gridLayout.addWidget(self.lineToolGroup, 6, 0, 1, 3)
        spacerItem = QtGui.QSpacerItem(20, 40, QtGui.QSizePolicy.Minimum, QtGui.QSizePolicy.Expanding)
        self.gridLayout.addItem(spacerItem, 10, 0, 1, 3)
        self.commentLabel = QtGui.QLabel(FeatureWidget)
        self.commentLabel.setObjectName(_fromUtf8("commentLabel"))
        self.gridLayout.addWidget(self.commentLabel, 3, 0, 1, 1)
        self.featureLabel = QtGui.QLabel(FeatureWidget)
        self.featureLabel.setObjectName(_fromUtf8("featureLabel"))
        self.gridLayout.addWidget(self.featureLabel, 1, 0, 1, 1)
        self.line = QtGui.QFrame(FeatureWidget)
        self.line.setFrameShadow(QtGui.QFrame.Sunken)
        self.line.setLineWidth(0)
        self.line.setFrameShape(QtGui.QFrame.HLine)
        self.line.setObjectName(_fromUtf8("line"))
        self.gridLayout.addWidget(self.line, 4, 0, 1, 3)
        self.horizontalLayout = QtGui.QHBoxLayout()
        self.horizontalLayout.setObjectName(_fromUtf8("horizontalLayout"))
        self.autoLabel = QtGui.QLabel(FeatureWidget)
        self.autoLabel.setObjectName(_fromUtf8("autoLabel"))
        self.horizontalLayout.addWidget(self.autoLabel)
        self.autoTool = QtGui.QToolButton(FeatureWidget)
        icon = QtGui.QIcon()
        icon.addPixmap(QtGui.QPixmap(_fromUtf8(":/plugins/ark/plan/autoSchematic.png")), QtGui.QIcon.Normal, QtGui.QIcon.Off)
        self.autoTool.setIcon(icon)
        self.autoTool.setObjectName(_fromUtf8("autoTool"))
        self.horizontalLayout.addWidget(self.autoTool)
        self.gridLayout.addLayout(self.horizontalLayout, 8, 0, 1, 3)
        self.commentEdit = QtGui.QLineEdit(FeatureWidget)
        sizePolicy = QtGui.QSizePolicy(QtGui.QSizePolicy.Preferred, QtGui.QSizePolicy.Fixed)
        sizePolicy.setHorizontalStretch(0)
        sizePolicy.setVerticalStretch(0)
        sizePolicy.setHeightForWidth(self.commentEdit.sizePolicy().hasHeightForWidth())
        self.commentEdit.setSizePolicy(sizePolicy)
        self.commentEdit.setObjectName(_fromUtf8("commentEdit"))
        self.gridLayout.addWidget(self.commentEdit, 3, 1, 1, 2)
        self.horizontalLayout_2 = QtGui.QHBoxLayout()
        self.horizontalLayout_2.setObjectName(_fromUtf8("horizontalLayout_2"))
        self.classCombo = QtGui.QComboBox(FeatureWidget)
        self.classCombo.setEnabled(False)
        self.classCombo.setObjectName(_fromUtf8("classCombo"))
        self.horizontalLayout_2.addWidget(self.classCombo)
        self.idSpin = QtGui.QSpinBox(FeatureWidget)
        sizePolicy = QtGui.QSizePolicy(QtGui.QSizePolicy.Preferred, QtGui.QSizePolicy.Fixed)
        sizePolicy.setHorizontalStretch(0)
        sizePolicy.setVerticalStretch(0)
        sizePolicy.setHeightForWidth(self.idSpin.sizePolicy().hasHeightForWidth())
        self.idSpin.setSizePolicy(sizePolicy)
        self.idSpin.setMaximum(99999)
        self.idSpin.setObjectName(_fromUtf8("idSpin"))
        self.horizontalLayout_2.addWidget(self.idSpin)
        self.gridLayout.addLayout(self.horizontalLayout_2, 1, 1, 1, 2)
        self.pointToolGroup = QtGui.QGroupBox(FeatureWidget)
        font = QtGui.QFont()
        font.setPointSize(10)
        self.pointToolGroup.setFont(font)
        self.pointToolGroup.setFlat(True)
        self.pointToolGroup.setObjectName(_fromUtf8("pointToolGroup"))
        self.pointToolLayout = QtGui.QGridLayout(self.pointToolGroup)
        self.pointToolLayout.setMargin(0)
        self.pointToolLayout.setObjectName(_fromUtf8("pointToolLayout"))
        self.gridLayout.addWidget(self.pointToolGroup, 5, 0, 1, 3)
        self.polygonToolGroup = QtGui.QGroupBox(FeatureWidget)
        font = QtGui.QFont()
        font.setPointSize(10)
        self.polygonToolGroup.setFont(font)
        self.polygonToolGroup.setFlat(True)
        self.polygonToolGroup.setObjectName(_fromUtf8("polygonToolGroup"))
        self.polygonToolLayout = QtGui.QGridLayout(self.polygonToolGroup)
        self.polygonToolLayout.setMargin(0)
        self.polygonToolLayout.setObjectName(_fromUtf8("polygonToolLayout"))
        self.gridLayout.addWidget(self.polygonToolGroup, 7, 0, 1, 3)
        self.labelLabel = QtGui.QLabel(FeatureWidget)
        self.labelLabel.setObjectName(_fromUtf8("labelLabel"))
        self.gridLayout.addWidget(self.labelLabel, 2, 0, 1, 1)
        self.labelEdit = QtGui.QLineEdit(FeatureWidget)
        self.labelEdit.setObjectName(_fromUtf8("labelEdit"))
        self.gridLayout.addWidget(self.labelEdit, 2, 1, 1, 2)
        self.commentLabel.setBuddy(self.commentEdit)
        self.featureLabel.setBuddy(self.classCombo)
        self.autoLabel.setBuddy(self.autoTool)

        self.retranslateUi(FeatureWidget)
        QtCore.QMetaObject.connectSlotsByName(FeatureWidget)
        FeatureWidget.setTabOrder(self.classCombo, self.idSpin)
        FeatureWidget.setTabOrder(self.idSpin, self.commentEdit)
        FeatureWidget.setTabOrder(self.commentEdit, self.autoTool)

    def retranslateUi(self, FeatureWidget):
        FeatureWidget.setWindowTitle(_translate("FeatureWidget", "FeatureWidget", None))
        self.lineToolGroup.setTitle(_translate("FeatureWidget", "Line", None))
        self.commentLabel.setText(_translate("FeatureWidget", "Comment:", None))
        self.featureLabel.setText(_translate("FeatureWidget", "Feature:", None))
        self.autoLabel.setText(_translate("FeatureWidget", "Auto Tool:", None))
        self.autoTool.setToolTip(_translate("FeatureWidget", "<html><head/><body><p>Auto Schematic</p></body></html>", None))
        self.autoTool.setText(_translate("FeatureWidget", "...", None))
        self.idSpin.setToolTip(_translate("FeatureWidget", "Source ID", None))
        self.pointToolGroup.setTitle(_translate("FeatureWidget", "Point", None))
        self.polygonToolGroup.setTitle(_translate("FeatureWidget", "Polygon", None))
        self.labelLabel.setText(_translate("FeatureWidget", "Label:", None))

import resources_rc
