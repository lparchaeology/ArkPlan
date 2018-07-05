# -*- coding: utf-8 -*-

# Form implementation generated from reading ui file 'ark/gui/ui/select_drawing_dialog_base.ui'
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

class Ui_SelectDrawingDialog(object):
    def setupUi(self, SelectDrawingDialog):
        SelectDrawingDialog.setObjectName(_fromUtf8("SelectDrawingDialog"))
        SelectDrawingDialog.resize(540, 302)
        self.gridLayout_2 = QtGui.QGridLayout(SelectDrawingDialog)
        self.gridLayout_2.setObjectName(_fromUtf8("gridLayout_2"))
        self.verticalLayout = QtGui.QVBoxLayout()
        self.verticalLayout.setObjectName(_fromUtf8("verticalLayout"))
        self.gridLayout = QtGui.QGridLayout()
        self.gridLayout.setObjectName(_fromUtf8("gridLayout"))
        self.northingSpin = QtGui.QSpinBox(SelectDrawingDialog)
        self.northingSpin.setMaximum(99999)
        self.northingSpin.setObjectName(_fromUtf8("northingSpin"))
        self.gridLayout.addWidget(self.northingSpin, 5, 1, 1, 1)
        self.idSpin = QtGui.QSpinBox(SelectDrawingDialog)
        self.idSpin.setMaximum(99999)
        self.idSpin.setObjectName(_fromUtf8("idSpin"))
        self.gridLayout.addWidget(self.idSpin, 3, 1, 1, 1)
        self.northingLabel = QtGui.QLabel(SelectDrawingDialog)
        self.northingLabel.setObjectName(_fromUtf8("northingLabel"))
        self.gridLayout.addWidget(self.northingLabel, 5, 0, 1, 1)
        self.siteCodeLabel = QtGui.QLabel(SelectDrawingDialog)
        self.siteCodeLabel.setObjectName(_fromUtf8("siteCodeLabel"))
        self.gridLayout.addWidget(self.siteCodeLabel, 2, 0, 1, 1)
        self.eastingSpin = QtGui.QSpinBox(SelectDrawingDialog)
        self.eastingSpin.setMaximum(99999)
        self.eastingSpin.setObjectName(_fromUtf8("eastingSpin"))
        self.gridLayout.addWidget(self.eastingSpin, 4, 1, 1, 1)
        self.drawingTypeCombo = QtGui.QComboBox(SelectDrawingDialog)
        self.drawingTypeCombo.setObjectName(_fromUtf8("drawingTypeCombo"))
        self.gridLayout.addWidget(self.drawingTypeCombo, 1, 1, 1, 1)
        self.siteCodeEdit = QtGui.QLineEdit(SelectDrawingDialog)
        self.siteCodeEdit.setObjectName(_fromUtf8("siteCodeEdit"))
        self.gridLayout.addWidget(self.siteCodeEdit, 2, 1, 1, 1)
        self.drawingTypeLabel = QtGui.QLabel(SelectDrawingDialog)
        self.drawingTypeLabel.setObjectName(_fromUtf8("drawingTypeLabel"))
        self.gridLayout.addWidget(self.drawingTypeLabel, 1, 0, 1, 1)
        self.headingLabel = QtGui.QLabel(SelectDrawingDialog)
        self.headingLabel.setObjectName(_fromUtf8("headingLabel"))
        self.gridLayout.addWidget(self.headingLabel, 0, 0, 1, 2)
        self.eastingLabel = QtGui.QLabel(SelectDrawingDialog)
        self.eastingLabel.setObjectName(_fromUtf8("eastingLabel"))
        self.gridLayout.addWidget(self.eastingLabel, 4, 0, 1, 1)
        self.idLabel = QtGui.QLabel(SelectDrawingDialog)
        self.idLabel.setObjectName(_fromUtf8("idLabel"))
        self.gridLayout.addWidget(self.idLabel, 3, 0, 1, 1)
        self.findButton = QtGui.QPushButton(SelectDrawingDialog)
        self.findButton.setObjectName(_fromUtf8("findButton"))
        self.gridLayout.addWidget(self.findButton, 6, 1, 1, 1)
        self.verticalLayout.addLayout(self.gridLayout)
        spacerItem = QtGui.QSpacerItem(20, 40, QtGui.QSizePolicy.Minimum, QtGui.QSizePolicy.Expanding)
        self.verticalLayout.addItem(spacerItem)
        self.gridLayout_2.addLayout(self.verticalLayout, 0, 0, 1, 1)
        self.fileList = QtGui.QListWidget(SelectDrawingDialog)
        self.fileList.setObjectName(_fromUtf8("fileList"))
        self.gridLayout_2.addWidget(self.fileList, 0, 1, 1, 1)
        self.buttonBox = QtGui.QDialogButtonBox(SelectDrawingDialog)
        self.buttonBox.setOrientation(QtCore.Qt.Horizontal)
        self.buttonBox.setStandardButtons(QtGui.QDialogButtonBox.Cancel|QtGui.QDialogButtonBox.Open)
        self.buttonBox.setObjectName(_fromUtf8("buttonBox"))
        self.gridLayout_2.addWidget(self.buttonBox, 1, 0, 1, 2)
        self.northingLabel.setBuddy(self.northingSpin)
        self.siteCodeLabel.setBuddy(self.siteCodeEdit)
        self.drawingTypeLabel.setBuddy(self.drawingTypeCombo)
        self.eastingLabel.setBuddy(self.eastingSpin)
        self.idLabel.setBuddy(self.idSpin)

        self.retranslateUi(SelectDrawingDialog)
        QtCore.QObject.connect(self.buttonBox, QtCore.SIGNAL(_fromUtf8("accepted()")), SelectDrawingDialog.accept)
        QtCore.QObject.connect(self.buttonBox, QtCore.SIGNAL(_fromUtf8("rejected()")), SelectDrawingDialog.reject)
        QtCore.QMetaObject.connectSlotsByName(SelectDrawingDialog)
        SelectDrawingDialog.setTabOrder(self.idSpin, self.eastingSpin)
        SelectDrawingDialog.setTabOrder(self.eastingSpin, self.northingSpin)
        SelectDrawingDialog.setTabOrder(self.northingSpin, self.findButton)
        SelectDrawingDialog.setTabOrder(self.findButton, self.drawingTypeCombo)
        SelectDrawingDialog.setTabOrder(self.drawingTypeCombo, self.siteCodeEdit)
        SelectDrawingDialog.setTabOrder(self.siteCodeEdit, self.fileList)
        SelectDrawingDialog.setTabOrder(self.fileList, self.buttonBox)

    def retranslateUi(self, SelectDrawingDialog):
        SelectDrawingDialog.setWindowTitle(_translate("SelectDrawingDialog", "Select Drawing(s)", None))
        self.northingLabel.setText(_translate("SelectDrawingDialog", "Grid Northing:", None))
        self.siteCodeLabel.setText(_translate("SelectDrawingDialog", "Site Code:", None))
        self.drawingTypeLabel.setText(_translate("SelectDrawingDialog", "Drawing:", None))
        self.headingLabel.setText(_translate("SelectDrawingDialog", "Select Drawing File(s):", None))
        self.eastingLabel.setText(_translate("SelectDrawingDialog", "Grid Easting:", None))
        self.idLabel.setText(_translate("SelectDrawingDialog", "ID:", None))
        self.findButton.setText(_translate("SelectDrawingDialog", "Filter", None))
