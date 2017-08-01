# -*- coding: utf-8 -*-

# Form implementation generated from reading ui file 'src/source_widget_base.ui'
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

class Ui_SourceWidget(object):
    def setupUi(self, SourceWidget):
        SourceWidget.setObjectName(_fromUtf8("SourceWidget"))
        SourceWidget.resize(293, 240)
        sizePolicy = QtGui.QSizePolicy(QtGui.QSizePolicy.Preferred, QtGui.QSizePolicy.Fixed)
        sizePolicy.setHorizontalStretch(0)
        sizePolicy.setVerticalStretch(0)
        sizePolicy.setHeightForWidth(SourceWidget.sizePolicy().hasHeightForWidth())
        SourceWidget.setSizePolicy(sizePolicy)
        SourceWidget.setFlat(False)
        self.gridLayout = QtGui.QGridLayout(SourceWidget)
        self.gridLayout.setObjectName(_fromUtf8("gridLayout"))
        self.sourceCodeCombo = QtGui.QComboBox(SourceWidget)
        self.sourceCodeCombo.setObjectName(_fromUtf8("sourceCodeCombo"))
        self.gridLayout.addWidget(self.sourceCodeCombo, 2, 1, 1, 1)
        self.sourceFileLabel = QtGui.QLabel(SourceWidget)
        self.sourceFileLabel.setObjectName(_fromUtf8("sourceFileLabel"))
        self.gridLayout.addWidget(self.sourceFileLabel, 4, 0, 1, 1)
        self.sourceCodeLabel = QtGui.QLabel(SourceWidget)
        self.sourceCodeLabel.setObjectName(_fromUtf8("sourceCodeLabel"))
        self.gridLayout.addWidget(self.sourceCodeLabel, 2, 0, 1, 1)
        self.sourceFileEdit = QtGui.QLineEdit(SourceWidget)
        self.sourceFileEdit.setObjectName(_fromUtf8("sourceFileEdit"))
        self.gridLayout.addWidget(self.sourceFileEdit, 4, 1, 1, 1)
        self.siteLabel = QtGui.QLabel(SourceWidget)
        self.siteLabel.setObjectName(_fromUtf8("siteLabel"))
        self.gridLayout.addWidget(self.siteLabel, 0, 0, 1, 1)
        self.commentEdit = QtGui.QLineEdit(SourceWidget)
        self.commentEdit.setReadOnly(False)
        self.commentEdit.setObjectName(_fromUtf8("commentEdit"))
        self.gridLayout.addWidget(self.commentEdit, 6, 1, 1, 1)
        self.commentLabel = QtGui.QLabel(SourceWidget)
        self.commentLabel.setObjectName(_fromUtf8("commentLabel"))
        self.gridLayout.addWidget(self.commentLabel, 6, 0, 1, 1)
        self.siteCodeCombo = QtGui.QComboBox(SourceWidget)
        self.siteCodeCombo.setObjectName(_fromUtf8("siteCodeCombo"))
        self.gridLayout.addWidget(self.siteCodeCombo, 0, 1, 1, 1)
        self.editorLabel = QtGui.QLabel(SourceWidget)
        self.editorLabel.setObjectName(_fromUtf8("editorLabel"))
        self.gridLayout.addWidget(self.editorLabel, 5, 0, 1, 1)
        self.editorEdit = QtGui.QLineEdit(SourceWidget)
        self.editorEdit.setObjectName(_fromUtf8("editorEdit"))
        self.gridLayout.addWidget(self.editorEdit, 5, 1, 1, 1)
        spacerItem = QtGui.QSpacerItem(20, 0, QtGui.QSizePolicy.Minimum, QtGui.QSizePolicy.Expanding)
        self.gridLayout.addItem(spacerItem, 8, 1, 1, 1)
        self.sourceIdLabel = QtGui.QLabel(SourceWidget)
        self.sourceIdLabel.setObjectName(_fromUtf8("sourceIdLabel"))
        self.gridLayout.addWidget(self.sourceIdLabel, 1, 0, 1, 1)
        self.horizontalLayout_2 = QtGui.QHBoxLayout()
        self.horizontalLayout_2.setObjectName(_fromUtf8("horizontalLayout_2"))
        self.sourceClassCombo = QtGui.QComboBox(SourceWidget)
        self.sourceClassCombo.setObjectName(_fromUtf8("sourceClassCombo"))
        self.horizontalLayout_2.addWidget(self.sourceClassCombo)
        self.sourceIdSpin = QtGui.QSpinBox(SourceWidget)
        self.sourceIdSpin.setMaximum(99999)
        self.sourceIdSpin.setObjectName(_fromUtf8("sourceIdSpin"))
        self.horizontalLayout_2.addWidget(self.sourceIdSpin)
        self.gridLayout.addLayout(self.horizontalLayout_2, 1, 1, 1, 1)
        self.sourceFileLabel.setBuddy(self.sourceFileEdit)
        self.sourceCodeLabel.setBuddy(self.sourceCodeCombo)
        self.siteLabel.setBuddy(self.siteCodeCombo)
        self.commentLabel.setBuddy(self.commentEdit)
        self.editorLabel.setBuddy(self.editorEdit)
        self.sourceIdLabel.setBuddy(self.sourceClassCombo)

        self.retranslateUi(SourceWidget)
        QtCore.QMetaObject.connectSlotsByName(SourceWidget)
        SourceWidget.setTabOrder(self.siteCodeCombo, self.sourceClassCombo)
        SourceWidget.setTabOrder(self.sourceClassCombo, self.sourceIdSpin)
        SourceWidget.setTabOrder(self.sourceIdSpin, self.sourceCodeCombo)
        SourceWidget.setTabOrder(self.sourceCodeCombo, self.sourceFileEdit)
        SourceWidget.setTabOrder(self.sourceFileEdit, self.editorEdit)
        SourceWidget.setTabOrder(self.editorEdit, self.commentEdit)

    def retranslateUi(self, SourceWidget):
        SourceWidget.setWindowTitle(_translate("SourceWidget", "SourceWidget", None))
        SourceWidget.setTitle(_translate("SourceWidget", "Source Metadata", None))
        self.sourceFileLabel.setText(_translate("SourceWidget", "Source File:", None))
        self.sourceCodeLabel.setText(_translate("SourceWidget", "Source Type:", None))
        self.siteLabel.setText(_translate("SourceWidget", "Site Code:", None))
        self.commentLabel.setText(_translate("SourceWidget", "Comment:", None))
        self.editorLabel.setText(_translate("SourceWidget", "Digitised By:", None))
        self.sourceIdLabel.setText(_translate("SourceWidget", "Source ID:", None))
        self.sourceIdSpin.setToolTip(_translate("SourceWidget", "Source ID", None))

