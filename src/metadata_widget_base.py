# -*- coding: utf-8 -*-

# Form implementation generated from reading ui file 'src/metadata_widget_base.ui'
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
        MetadataWidget.resize(289, 271)
        self.gridLayout_2 = QtGui.QGridLayout(MetadataWidget)
        self.gridLayout_2.setMargin(0)
        self.gridLayout_2.setObjectName(_fromUtf8("gridLayout_2"))
        self.metadataGroup = QtGui.QGroupBox(MetadataWidget)
        self.metadataGroup.setObjectName(_fromUtf8("metadataGroup"))
        self.gridLayout = QtGui.QGridLayout(self.metadataGroup)
        self.gridLayout.setObjectName(_fromUtf8("gridLayout"))
        self.siteEdit = QtGui.QLineEdit(self.metadataGroup)
        self.siteEdit.setReadOnly(False)
        self.siteEdit.setObjectName(_fromUtf8("siteEdit"))
        self.gridLayout.addWidget(self.siteEdit, 0, 1, 1, 1)
        self.sourceCodeLabel = QtGui.QLabel(self.metadataGroup)
        self.sourceCodeLabel.setObjectName(_fromUtf8("sourceCodeLabel"))
        self.gridLayout.addWidget(self.sourceCodeLabel, 4, 0, 1, 1)
        self.sourceIdLabel = QtGui.QLabel(self.metadataGroup)
        self.sourceIdLabel.setObjectName(_fromUtf8("sourceIdLabel"))
        self.gridLayout.addWidget(self.sourceIdLabel, 5, 0, 1, 1)
        self.siteLabel = QtGui.QLabel(self.metadataGroup)
        self.siteLabel.setObjectName(_fromUtf8("siteLabel"))
        self.gridLayout.addWidget(self.siteLabel, 0, 0, 1, 1)
        self.sourceFileLabel = QtGui.QLabel(self.metadataGroup)
        self.sourceFileLabel.setObjectName(_fromUtf8("sourceFileLabel"))
        self.gridLayout.addWidget(self.sourceFileLabel, 6, 0, 1, 1)
        self.sourceFileEdit = QtGui.QLineEdit(self.metadataGroup)
        self.sourceFileEdit.setObjectName(_fromUtf8("sourceFileEdit"))
        self.gridLayout.addWidget(self.sourceFileEdit, 6, 1, 1, 1)
        self.sourceCodeCombo = QtGui.QComboBox(self.metadataGroup)
        self.sourceCodeCombo.setObjectName(_fromUtf8("sourceCodeCombo"))
        self.gridLayout.addWidget(self.sourceCodeCombo, 4, 1, 1, 1)
        self.commentLabel = QtGui.QLabel(self.metadataGroup)
        self.commentLabel.setObjectName(_fromUtf8("commentLabel"))
        self.gridLayout.addWidget(self.commentLabel, 7, 0, 1, 1)
        self.horizontalLayout_3 = QtGui.QHBoxLayout()
        self.horizontalLayout_3.setObjectName(_fromUtf8("horizontalLayout_3"))
        self.classCombo = QtGui.QComboBox(self.metadataGroup)
        self.classCombo.setObjectName(_fromUtf8("classCombo"))
        self.horizontalLayout_3.addWidget(self.classCombo)
        self.idSpin = QtGui.QSpinBox(self.metadataGroup)
        self.idSpin.setMaximum(99999)
        self.idSpin.setObjectName(_fromUtf8("idSpin"))
        self.horizontalLayout_3.addWidget(self.idSpin)
        self.gridLayout.addLayout(self.horizontalLayout_3, 1, 1, 1, 1)
        self.horizontalLayout_2 = QtGui.QHBoxLayout()
        self.horizontalLayout_2.setObjectName(_fromUtf8("horizontalLayout_2"))
        self.sourceClassCombo = QtGui.QComboBox(self.metadataGroup)
        self.sourceClassCombo.setObjectName(_fromUtf8("sourceClassCombo"))
        self.horizontalLayout_2.addWidget(self.sourceClassCombo)
        self.sourceIdSpin = QtGui.QSpinBox(self.metadataGroup)
        self.sourceIdSpin.setMaximum(99999)
        self.sourceIdSpin.setObjectName(_fromUtf8("sourceIdSpin"))
        self.horizontalLayout_2.addWidget(self.sourceIdSpin)
        self.gridLayout.addLayout(self.horizontalLayout_2, 5, 1, 1, 1)
        self.label = QtGui.QLabel(self.metadataGroup)
        self.label.setObjectName(_fromUtf8("label"))
        self.gridLayout.addWidget(self.label, 1, 0, 1, 1)
        self.commentEdit = QtGui.QLineEdit(self.metadataGroup)
        self.commentEdit.setReadOnly(False)
        self.commentEdit.setObjectName(_fromUtf8("commentEdit"))
        self.gridLayout.addWidget(self.commentEdit, 7, 1, 1, 1)
        self.createdByLabel = QtGui.QLabel(self.metadataGroup)
        self.createdByLabel.setObjectName(_fromUtf8("createdByLabel"))
        self.gridLayout.addWidget(self.createdByLabel, 8, 0, 1, 1)
        self.createdByEdit = QtGui.QLineEdit(self.metadataGroup)
        self.createdByEdit.setObjectName(_fromUtf8("createdByEdit"))
        self.gridLayout.addWidget(self.createdByEdit, 8, 1, 1, 1)
        self.gridLayout_2.addWidget(self.metadataGroup, 0, 0, 1, 1)
        self.sourceCodeLabel.setBuddy(self.sourceCodeCombo)
        self.sourceIdLabel.setBuddy(self.sourceClassCombo)
        self.siteLabel.setBuddy(self.siteEdit)
        self.sourceFileLabel.setBuddy(self.sourceFileEdit)
        self.commentLabel.setBuddy(self.commentEdit)
        self.createdByLabel.setBuddy(self.createdByEdit)

        self.retranslateUi(MetadataWidget)
        QtCore.QMetaObject.connectSlotsByName(MetadataWidget)
        MetadataWidget.setTabOrder(self.siteEdit, self.sourceCodeCombo)
        MetadataWidget.setTabOrder(self.sourceCodeCombo, self.sourceClassCombo)
        MetadataWidget.setTabOrder(self.sourceClassCombo, self.sourceIdSpin)
        MetadataWidget.setTabOrder(self.sourceIdSpin, self.sourceFileEdit)

    def retranslateUi(self, MetadataWidget):
        MetadataWidget.setWindowTitle(_translate("MetadataWidget", "Metadata", None))
        self.metadataGroup.setTitle(_translate("MetadataWidget", "Metadata", None))
        self.sourceCodeLabel.setText(_translate("MetadataWidget", "Source:", None))
        self.sourceIdLabel.setText(_translate("MetadataWidget", "Source ID:", None))
        self.siteLabel.setText(_translate("MetadataWidget", "Site Code:", None))
        self.sourceFileLabel.setText(_translate("MetadataWidget", "Source File:", None))
        self.commentLabel.setText(_translate("MetadataWidget", "Comment:", None))
        self.idSpin.setToolTip(_translate("MetadataWidget", "Source ID", None))
        self.sourceIdSpin.setToolTip(_translate("MetadataWidget", "Source ID", None))
        self.label.setText(_translate("MetadataWidget", "Item ID:", None))
        self.createdByLabel.setText(_translate("MetadataWidget", "Digitised By:", None))

