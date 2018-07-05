# -*- coding: utf-8 -*-

# Form implementation generated from reading ui file 'ark/gui/ui/figure_widget_base.ui'
#
# Created by: PyQt4 UI code generator 4.12.1
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

class Ui_FigureWidget(object):
    def setupUi(self, FigureWidget):
        FigureWidget.setObjectName(_fromUtf8("FigureWidget"))
        FigureWidget.resize(413, 352)
        self.gridLayout = QtGui.QGridLayout(FigureWidget)
        self.gridLayout.setObjectName(_fromUtf8("gridLayout"))
        self.titleLabel = QtGui.QLabel(FigureWidget)
        font = QtGui.QFont()
        font.setBold(True)
        font.setWeight(75)
        self.titleLabel.setFont(font)
        self.titleLabel.setAlignment(QtCore.Qt.AlignCenter)
        self.titleLabel.setObjectName(_fromUtf8("titleLabel"))
        self.gridLayout.addWidget(self.titleLabel, 0, 0, 1, 3)
        self.label = QtGui.QLabel(FigureWidget)
        self.label.setObjectName(_fromUtf8("label"))
        self.gridLayout.addWidget(self.label, 1, 0, 1, 1)
        self.comboBox = QtGui.QComboBox(FigureWidget)
        self.comboBox.setObjectName(_fromUtf8("comboBox"))
        self.gridLayout.addWidget(self.comboBox, 1, 1, 1, 1)
        self.doubleSpinBox = QtGui.QDoubleSpinBox(FigureWidget)
        self.doubleSpinBox.setDecimals(1)
        self.doubleSpinBox.setMinimum(1.0)
        self.doubleSpinBox.setProperty("value", 1.0)
        self.doubleSpinBox.setObjectName(_fromUtf8("doubleSpinBox"))
        self.gridLayout.addWidget(self.doubleSpinBox, 1, 2, 1, 1)
        self.label_2 = QtGui.QLabel(FigureWidget)
        self.label_2.setObjectName(_fromUtf8("label_2"))
        self.gridLayout.addWidget(self.label_2, 2, 0, 1, 1)
        self.comboBox_2 = QtGui.QComboBox(FigureWidget)
        self.comboBox_2.setEditable(False)
        self.comboBox_2.setObjectName(_fromUtf8("comboBox_2"))
        self.gridLayout.addWidget(self.comboBox_2, 2, 1, 1, 1)
        self.label_4 = QtGui.QLabel(FigureWidget)
        self.label_4.setObjectName(_fromUtf8("label_4"))
        self.gridLayout.addWidget(self.label_4, 3, 0, 1, 1)
        self.lineEdit = QtGui.QLineEdit(FigureWidget)
        self.lineEdit.setObjectName(_fromUtf8("lineEdit"))
        self.gridLayout.addWidget(self.lineEdit, 3, 1, 1, 2)
        self.label_5 = QtGui.QLabel(FigureWidget)
        self.label_5.setObjectName(_fromUtf8("label_5"))
        self.gridLayout.addWidget(self.label_5, 4, 0, 1, 1)
        self.lineEdit_2 = QtGui.QLineEdit(FigureWidget)
        self.lineEdit_2.setObjectName(_fromUtf8("lineEdit_2"))
        self.gridLayout.addWidget(self.lineEdit_2, 4, 1, 1, 2)
        self.label_3 = QtGui.QLabel(FigureWidget)
        self.label_3.setObjectName(_fromUtf8("label_3"))
        self.gridLayout.addWidget(self.label_3, 5, 0, 1, 1)
        self.label_6 = QtGui.QLabel(FigureWidget)
        self.label_6.setObjectName(_fromUtf8("label_6"))
        self.gridLayout.addWidget(self.label_6, 6, 0, 1, 1)
        self.pushButton = QtGui.QPushButton(FigureWidget)
        self.pushButton.setObjectName(_fromUtf8("pushButton"))
        self.gridLayout.addWidget(self.pushButton, 7, 2, 1, 1)
        self.comboBox_3 = QtGui.QComboBox(FigureWidget)
        self.comboBox_3.setObjectName(_fromUtf8("comboBox_3"))
        self.gridLayout.addWidget(self.comboBox_3, 5, 1, 1, 2)
        self.comboBox_4 = QtGui.QComboBox(FigureWidget)
        self.comboBox_4.setObjectName(_fromUtf8("comboBox_4"))
        self.gridLayout.addWidget(self.comboBox_4, 6, 1, 1, 2)
        spacerItem = QtGui.QSpacerItem(398, 45, QtGui.QSizePolicy.Minimum, QtGui.QSizePolicy.Expanding)
        self.gridLayout.addItem(spacerItem, 8, 0, 1, 3)
        spacerItem1 = QtGui.QSpacerItem(40, 20, QtGui.QSizePolicy.Expanding, QtGui.QSizePolicy.Minimum)
        self.gridLayout.addItem(spacerItem1, 7, 1, 1, 1)
        self.spinBox_2 = QtGui.QSpinBox(FigureWidget)
        self.spinBox_2.setMinimum(1)
        self.spinBox_2.setProperty("value", 1)
        self.spinBox_2.setObjectName(_fromUtf8("spinBox_2"))
        self.gridLayout.addWidget(self.spinBox_2, 2, 2, 1, 1)

        self.retranslateUi(FigureWidget)
        QtCore.QMetaObject.connectSlotsByName(FigureWidget)

    def retranslateUi(self, FigureWidget):
        FigureWidget.setWindowTitle(_translate("FigureWidget", "Form", None))
        self.titleLabel.setText(_translate("FigureWidget", "Figure Builder", None))
        self.label.setText(_translate("FigureWidget", "Document", None))
        self.doubleSpinBox.setPrefix(_translate("FigureWidget", "v ", None))
        self.label_2.setText(_translate("FigureWidget", "Figure", None))
        self.label_4.setText(_translate("FigureWidget", "Title", None))
        self.label_5.setText(_translate("FigureWidget", "Description", None))
        self.label_3.setText(_translate("FigureWidget", "Licence", None))
        self.label_6.setText(_translate("FigureWidget", "Template", None))
        self.pushButton.setText(_translate("FigureWidget", "Build", None))
