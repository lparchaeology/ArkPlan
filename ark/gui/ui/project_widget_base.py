# -*- coding: utf-8 -*-

# Form implementation generated from reading ui file 'ark/gui/ui/project_widget_base.ui'
#
# Created by: PyQt4 UI code generator 4.12.1
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

class Ui_ProjectWidget(object):
    def setupUi(self, ProjectWidget):
        ProjectWidget.setObjectName(_fromUtf8("ProjectWidget"))
        ProjectWidget.resize(365, 310)
        self.gridLayout = QtGui.QGridLayout(ProjectWidget)
        self.gridLayout.setObjectName(_fromUtf8("gridLayout"))
        spacerItem = QtGui.QSpacerItem(350, 41, QtGui.QSizePolicy.Minimum, QtGui.QSizePolicy.Expanding)
        self.gridLayout.addItem(spacerItem, 7, 0, 1, 4)
        self.lineEdit = QtGui.QLineEdit(ProjectWidget)
        self.lineEdit.setReadOnly(True)
        self.lineEdit.setObjectName(_fromUtf8("lineEdit"))
        self.gridLayout.addWidget(self.lineEdit, 2, 1, 1, 3)
        self.comboBox = QtGui.QComboBox(ProjectWidget)
        self.comboBox.setEditable(True)
        self.comboBox.setObjectName(_fromUtf8("comboBox"))
        self.gridLayout.addWidget(self.comboBox, 1, 1, 1, 2)
        self.lineEdit_2 = QtGui.QLineEdit(ProjectWidget)
        self.lineEdit_2.setReadOnly(True)
        self.lineEdit_2.setObjectName(_fromUtf8("lineEdit_2"))
        self.gridLayout.addWidget(self.lineEdit_2, 4, 1, 1, 3)
        self.pushButton = QtGui.QPushButton(ProjectWidget)
        self.pushButton.setObjectName(_fromUtf8("pushButton"))
        self.gridLayout.addWidget(self.pushButton, 1, 3, 1, 1)
        self.label_4 = QtGui.QLabel(ProjectWidget)
        self.label_4.setObjectName(_fromUtf8("label_4"))
        self.gridLayout.addWidget(self.label_4, 4, 0, 1, 1)
        self.label_2 = QtGui.QLabel(ProjectWidget)
        self.label_2.setObjectName(_fromUtf8("label_2"))
        self.gridLayout.addWidget(self.label_2, 3, 0, 1, 1)
        self.label_5 = QtGui.QLabel(ProjectWidget)
        self.label_5.setObjectName(_fromUtf8("label_5"))
        self.gridLayout.addWidget(self.label_5, 1, 0, 1, 1)
        self.label_3 = QtGui.QLabel(ProjectWidget)
        self.label_3.setObjectName(_fromUtf8("label_3"))
        self.gridLayout.addWidget(self.label_3, 6, 0, 1, 1)
        self.label = QtGui.QLabel(ProjectWidget)
        self.label.setObjectName(_fromUtf8("label"))
        self.gridLayout.addWidget(self.label, 2, 0, 1, 1)
        self.lineEdit_3 = QtGui.QLineEdit(ProjectWidget)
        self.lineEdit_3.setReadOnly(True)
        self.lineEdit_3.setObjectName(_fromUtf8("lineEdit_3"))
        self.gridLayout.addWidget(self.lineEdit_3, 6, 1, 1, 3)
        self.spinBox = QtGui.QSpinBox(ProjectWidget)
        self.spinBox.setReadOnly(True)
        self.spinBox.setMaximum(99999)
        self.spinBox.setObjectName(_fromUtf8("spinBox"))
        self.gridLayout.addWidget(self.spinBox, 3, 1, 1, 1)
        self.titleLabel = QtGui.QLabel(ProjectWidget)
        font = QtGui.QFont()
        font.setBold(True)
        font.setWeight(75)
        self.titleLabel.setFont(font)
        self.titleLabel.setAlignment(QtCore.Qt.AlignCenter)
        self.titleLabel.setObjectName(_fromUtf8("titleLabel"))
        self.gridLayout.addWidget(self.titleLabel, 0, 0, 1, 4)
        self.spinBox_2 = QtGui.QSpinBox(ProjectWidget)
        self.spinBox_2.setReadOnly(True)
        self.spinBox_2.setMaximum(99999)
        self.spinBox_2.setObjectName(_fromUtf8("spinBox_2"))
        self.gridLayout.addWidget(self.spinBox_2, 3, 2, 1, 1)
        spacerItem1 = QtGui.QSpacerItem(40, 20, QtGui.QSizePolicy.Expanding, QtGui.QSizePolicy.Minimum)
        self.gridLayout.addItem(spacerItem1, 3, 3, 1, 1)
        self.lineEdit_4 = QtGui.QLineEdit(ProjectWidget)
        self.lineEdit_4.setReadOnly(True)
        self.lineEdit_4.setObjectName(_fromUtf8("lineEdit_4"))
        self.gridLayout.addWidget(self.lineEdit_4, 5, 1, 1, 3)
        self.label_6 = QtGui.QLabel(ProjectWidget)
        self.label_6.setObjectName(_fromUtf8("label_6"))
        self.gridLayout.addWidget(self.label_6, 5, 0, 1, 1)

        self.retranslateUi(ProjectWidget)
        QtCore.QMetaObject.connectSlotsByName(ProjectWidget)

    def retranslateUi(self, ProjectWidget):
        ProjectWidget.setWindowTitle(_translate("ProjectWidget", "Form", None))
        self.pushButton.setText(_translate("ProjectWidget", "Fetch", None))
        self.label_4.setText(_translate("ProjectWidget", "Grid", None))
        self.label_2.setText(_translate("ProjectWidget", "Location", None))
        self.label_5.setText(_translate("ProjectWidget", "Project", None))
        self.label_3.setText(_translate("ProjectWidget", "County", None))
        self.label.setText(_translate("ProjectWidget", "Name", None))
        self.titleLabel.setText(_translate("ProjectWidget", "Project Details", None))
        self.label_6.setText(_translate("ProjectWidget", "Post Code", None))

