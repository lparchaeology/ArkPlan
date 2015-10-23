# -*- coding: utf-8 -*-

# Form implementation generated from reading ui file 'plan/metadata_widget_base.ui'
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

class Ui_MetadataWidget(object):
    def setupUi(self, MetadataWidget):
        MetadataWidget.setObjectName(_fromUtf8("MetadataWidget"))
        MetadataWidget.resize(311, 242)
        self.gridLayout_2 = QtGui.QGridLayout(MetadataWidget)
        self.gridLayout_2.setMargin(0)
        self.gridLayout_2.setObjectName(_fromUtf8("gridLayout_2"))
        self.metadataGroup = QtGui.QGroupBox(MetadataWidget)
        self.metadataGroup.setObjectName(_fromUtf8("metadataGroup"))
        self.gridLayout = QtGui.QGridLayout(self.metadataGroup)
        self.gridLayout.setObjectName(_fromUtf8("gridLayout"))
        self.sourceCodeCombo = QtGui.QComboBox(self.metadataGroup)
        self.sourceCodeCombo.setObjectName(_fromUtf8("sourceCodeCombo"))
        self.gridLayout.addWidget(self.sourceCodeCombo, 3, 1, 1, 1)
        self.sourceIdLabel = QtGui.QLabel(self.metadataGroup)
        self.sourceIdLabel.setObjectName(_fromUtf8("sourceIdLabel"))
        self.gridLayout.addWidget(self.sourceIdLabel, 4, 0, 1, 1)
        self.siteLabel = QtGui.QLabel(self.metadataGroup)
        self.siteLabel.setObjectName(_fromUtf8("siteLabel"))
        self.gridLayout.addWidget(self.siteLabel, 0, 0, 1, 1)
        self.siteEdit = QtGui.QLineEdit(self.metadataGroup)
        self.siteEdit.setReadOnly(False)
        self.siteEdit.setObjectName(_fromUtf8("siteEdit"))
        self.gridLayout.addWidget(self.siteEdit, 0, 1, 1, 1)
        self.sourceCodeLabel = QtGui.QLabel(self.metadataGroup)
        self.sourceCodeLabel.setObjectName(_fromUtf8("sourceCodeLabel"))
        self.gridLayout.addWidget(self.sourceCodeLabel, 3, 0, 1, 1)
        self.sourceFileLabel = QtGui.QLabel(self.metadataGroup)
        self.sourceFileLabel.setObjectName(_fromUtf8("sourceFileLabel"))
        self.gridLayout.addWidget(self.sourceFileLabel, 5, 0, 1, 1)
        self.sourceFileEdit = QtGui.QLineEdit(self.metadataGroup)
        self.sourceFileEdit.setObjectName(_fromUtf8("sourceFileEdit"))
        self.gridLayout.addWidget(self.sourceFileEdit, 5, 1, 1, 1)
        self.horizontalLayout_2 = QtGui.QHBoxLayout()
        self.horizontalLayout_2.setObjectName(_fromUtf8("horizontalLayout_2"))
        self.sourceClassCombo = QtGui.QComboBox(self.metadataGroup)
        self.sourceClassCombo.setObjectName(_fromUtf8("sourceClassCombo"))
        self.horizontalLayout_2.addWidget(self.sourceClassCombo)
        self.sourceIdSpin = QtGui.QSpinBox(self.metadataGroup)
        self.sourceIdSpin.setMaximum(99999)
        self.sourceIdSpin.setObjectName(_fromUtf8("sourceIdSpin"))
        self.horizontalLayout_2.addWidget(self.sourceIdSpin)
        self.gridLayout.addLayout(self.horizontalLayout_2, 4, 1, 1, 1)
        self.commentLabel = QtGui.QLabel(self.metadataGroup)
        self.commentLabel.setObjectName(_fromUtf8("commentLabel"))
        self.gridLayout.addWidget(self.commentLabel, 1, 0, 1, 1)
        self.commentEdit = QtGui.QLineEdit(self.metadataGroup)
        self.commentEdit.setReadOnly(False)
        self.commentEdit.setObjectName(_fromUtf8("commentEdit"))
        self.gridLayout.addWidget(self.commentEdit, 1, 1, 1, 1)
        self.createdByLabel = QtGui.QLabel(self.metadataGroup)
        self.createdByLabel.setObjectName(_fromUtf8("createdByLabel"))
        self.gridLayout.addWidget(self.createdByLabel, 2, 0, 1, 1)
        self.createdByEdit = QtGui.QLineEdit(self.metadataGroup)
        self.createdByEdit.setObjectName(_fromUtf8("createdByEdit"))
        self.gridLayout.addWidget(self.createdByEdit, 2, 1, 1, 1)
        self.gridLayout_2.addWidget(self.metadataGroup, 0, 0, 1, 1)
        self.sourceIdLabel.setBuddy(self.sourceClassCombo)
        self.siteLabel.setBuddy(self.siteEdit)
        self.sourceCodeLabel.setBuddy(self.sourceCodeCombo)
        self.sourceFileLabel.setBuddy(self.sourceFileEdit)
        self.commentLabel.setBuddy(self.commentEdit)
        self.createdByLabel.setBuddy(self.createdByEdit)

        self.retranslateUi(MetadataWidget)
        QtCore.QMetaObject.connectSlotsByName(MetadataWidget)
        MetadataWidget.setTabOrder(self.siteEdit, self.commentEdit)
        MetadataWidget.setTabOrder(self.commentEdit, self.createdByEdit)
        MetadataWidget.setTabOrder(self.createdByEdit, self.sourceCodeCombo)
        MetadataWidget.setTabOrder(self.sourceCodeCombo, self.sourceClassCombo)
        MetadataWidget.setTabOrder(self.sourceClassCombo, self.sourceIdSpin)
        MetadataWidget.setTabOrder(self.sourceIdSpin, self.sourceFileEdit)

    def retranslateUi(self, MetadataWidget):
        MetadataWidget.setWindowTitle(_translate("MetadataWidget", "Metadata", None))
        self.metadataGroup.setTitle(_translate("MetadataWidget", "Metadata", None))
        self.sourceIdLabel.setText(_translate("MetadataWidget", "Source ID:", None))
        self.siteLabel.setText(_translate("MetadataWidget", "Site Code:", None))
        self.sourceCodeLabel.setText(_translate("MetadataWidget", "Source:", None))
        self.sourceFileLabel.setText(_translate("MetadataWidget", "Source File:", None))
        self.sourceIdSpin.setToolTip(_translate("MetadataWidget", "Source ID", None))
        self.commentLabel.setText(_translate("MetadataWidget", "Comment:", None))
        self.createdByLabel.setText(_translate("MetadataWidget", "Digitised By:", None))

