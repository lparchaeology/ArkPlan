# -*- coding: utf-8 -*-

# Form implementation generated from reading ui file 'src/metadata_widget_base.ui'
#
# Created by: PyQt4 UI code generator 4.11.4
#
# WARNING! All changes made in this file will be lost!

from qgis.PyQt import QtCore, QtGui

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
        MetadataWidget.resize(289, 280)
        sizePolicy = QtGui.QSizePolicy(QtGui.QSizePolicy.Preferred, QtGui.QSizePolicy.Fixed)
        sizePolicy.setHorizontalStretch(0)
        sizePolicy.setVerticalStretch(0)
        sizePolicy.setHeightForWidth(MetadataWidget.sizePolicy().hasHeightForWidth())
        MetadataWidget.setSizePolicy(sizePolicy)
        MetadataWidget.setFlat(False)
        self.gridLayout = QtGui.QGridLayout(MetadataWidget)
        self.gridLayout.setObjectName(_fromUtf8("gridLayout"))
        self.editorLabel = QtGui.QLabel(MetadataWidget)
        self.editorLabel.setObjectName(_fromUtf8("editorLabel"))
        self.gridLayout.addWidget(self.editorLabel, 6, 0, 1, 1)
        self.horizontalLayout_3 = QtGui.QHBoxLayout()
        self.horizontalLayout_3.setObjectName(_fromUtf8("horizontalLayout_3"))
        self.classCombo = QtGui.QComboBox(MetadataWidget)
        self.classCombo.setObjectName(_fromUtf8("classCombo"))
        self.horizontalLayout_3.addWidget(self.classCombo)
        self.idSpin = QtGui.QSpinBox(MetadataWidget)
        self.idSpin.setMaximum(99999)
        self.idSpin.setObjectName(_fromUtf8("idSpin"))
        self.horizontalLayout_3.addWidget(self.idSpin)
        self.gridLayout.addLayout(self.horizontalLayout_3, 1, 1, 1, 1)
        self.horizontalLayout_2 = QtGui.QHBoxLayout()
        self.horizontalLayout_2.setObjectName(_fromUtf8("horizontalLayout_2"))
        self.sourceClassCombo = QtGui.QComboBox(MetadataWidget)
        self.sourceClassCombo.setObjectName(_fromUtf8("sourceClassCombo"))
        self.horizontalLayout_2.addWidget(self.sourceClassCombo)
        self.sourceIdSpin = QtGui.QSpinBox(MetadataWidget)
        self.sourceIdSpin.setMaximum(99999)
        self.sourceIdSpin.setObjectName(_fromUtf8("sourceIdSpin"))
        self.horizontalLayout_2.addWidget(self.sourceIdSpin)
        self.gridLayout.addLayout(self.horizontalLayout_2, 3, 1, 1, 1)
        self.sourceCodeCombo = QtGui.QComboBox(MetadataWidget)
        self.sourceCodeCombo.setObjectName(_fromUtf8("sourceCodeCombo"))
        self.gridLayout.addWidget(self.sourceCodeCombo, 2, 1, 1, 1)
        self.sourceFileLabel = QtGui.QLabel(MetadataWidget)
        self.sourceFileLabel.setObjectName(_fromUtf8("sourceFileLabel"))
        self.gridLayout.addWidget(self.sourceFileLabel, 4, 0, 1, 1)
        self.sourceIdLabel = QtGui.QLabel(MetadataWidget)
        self.sourceIdLabel.setObjectName(_fromUtf8("sourceIdLabel"))
        self.gridLayout.addWidget(self.sourceIdLabel, 3, 0, 1, 1)
        self.sourceCodeLabel = QtGui.QLabel(MetadataWidget)
        self.sourceCodeLabel.setObjectName(_fromUtf8("sourceCodeLabel"))
        self.gridLayout.addWidget(self.sourceCodeLabel, 2, 0, 1, 1)
        self.sourceFileEdit = QtGui.QLineEdit(MetadataWidget)
        self.sourceFileEdit.setObjectName(_fromUtf8("sourceFileEdit"))
        self.gridLayout.addWidget(self.sourceFileEdit, 4, 1, 1, 1)
        self.siteLabel = QtGui.QLabel(MetadataWidget)
        self.siteLabel.setObjectName(_fromUtf8("siteLabel"))
        self.gridLayout.addWidget(self.siteLabel, 0, 0, 1, 1)
        self.editorEdit = QtGui.QLineEdit(MetadataWidget)
        self.editorEdit.setObjectName(_fromUtf8("editorEdit"))
        self.gridLayout.addWidget(self.editorEdit, 6, 1, 1, 1)
        self.commentEdit = QtGui.QLineEdit(MetadataWidget)
        self.commentEdit.setReadOnly(False)
        self.commentEdit.setObjectName(_fromUtf8("commentEdit"))
        self.gridLayout.addWidget(self.commentEdit, 5, 1, 1, 1)
        self.commentLabel = QtGui.QLabel(MetadataWidget)
        self.commentLabel.setObjectName(_fromUtf8("commentLabel"))
        self.gridLayout.addWidget(self.commentLabel, 5, 0, 1, 1)
        self.label = QtGui.QLabel(MetadataWidget)
        self.label.setObjectName(_fromUtf8("label"))
        self.gridLayout.addWidget(self.label, 1, 0, 1, 1)
        self.siteCodeCombo = QtGui.QComboBox(MetadataWidget)
        self.siteCodeCombo.setObjectName(_fromUtf8("siteCodeCombo"))
        self.gridLayout.addWidget(self.siteCodeCombo, 0, 1, 1, 1)
        spacerItem = QtGui.QSpacerItem(20, 0, QtGui.QSizePolicy.Minimum, QtGui.QSizePolicy.Expanding)
        self.gridLayout.addItem(spacerItem, 7, 1, 1, 1)
        self.editorLabel.setBuddy(self.editorEdit)
        self.sourceFileLabel.setBuddy(self.sourceFileEdit)
        self.sourceIdLabel.setBuddy(self.sourceClassCombo)
        self.sourceCodeLabel.setBuddy(self.sourceCodeCombo)
        self.commentLabel.setBuddy(self.commentEdit)
        self.label.setBuddy(self.classCombo)

        self.retranslateUi(MetadataWidget)
        QtCore.QMetaObject.connectSlotsByName(MetadataWidget)
        MetadataWidget.setTabOrder(self.siteCodeCombo, self.classCombo)
        MetadataWidget.setTabOrder(self.classCombo, self.idSpin)
        MetadataWidget.setTabOrder(self.idSpin, self.sourceCodeCombo)
        MetadataWidget.setTabOrder(self.sourceCodeCombo, self.sourceClassCombo)
        MetadataWidget.setTabOrder(self.sourceClassCombo, self.sourceIdSpin)
        MetadataWidget.setTabOrder(self.sourceIdSpin, self.sourceFileEdit)
        MetadataWidget.setTabOrder(self.sourceFileEdit, self.commentEdit)
        MetadataWidget.setTabOrder(self.commentEdit, self.editorEdit)

    def retranslateUi(self, MetadataWidget):
        MetadataWidget.setTitle(_translate("MetadataWidget", "Source Metadata", None))
        self.editorLabel.setText(_translate("MetadataWidget", "Digitised By:", None))
        self.idSpin.setToolTip(_translate("MetadataWidget", "Source ID", None))
        self.sourceIdSpin.setToolTip(_translate("MetadataWidget", "Source ID", None))
        self.sourceFileLabel.setText(_translate("MetadataWidget", "Source File:", None))
        self.sourceIdLabel.setText(_translate("MetadataWidget", "Source ID:", None))
        self.sourceCodeLabel.setText(_translate("MetadataWidget", "Source:", None))
        self.siteLabel.setText(_translate("MetadataWidget", "Site Code:", None))
        self.commentLabel.setText(_translate("MetadataWidget", "Comment:", None))
        self.label.setText(_translate("MetadataWidget", "Item ID:", None))
