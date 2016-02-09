# -*- coding: utf-8 -*-

# Form implementation generated from reading ui file 'src/schematic_widget_base.ui'
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

class Ui_SchematicWidget(object):
    def setupUi(self, SchematicWidget):
        SchematicWidget.setObjectName(_fromUtf8("SchematicWidget"))
        SchematicWidget.resize(400, 852)
        self.verticalLayout_2 = QtGui.QVBoxLayout(SchematicWidget)
        self.verticalLayout_2.setMargin(0)
        self.verticalLayout_2.setObjectName(_fromUtf8("verticalLayout_2"))
        self.scrollArea = QtGui.QScrollArea(SchematicWidget)
        sizePolicy = QtGui.QSizePolicy(QtGui.QSizePolicy.MinimumExpanding, QtGui.QSizePolicy.Expanding)
        sizePolicy.setHorizontalStretch(0)
        sizePolicy.setVerticalStretch(0)
        sizePolicy.setHeightForWidth(self.scrollArea.sizePolicy().hasHeightForWidth())
        self.scrollArea.setSizePolicy(sizePolicy)
        self.scrollArea.setFrameShape(QtGui.QFrame.NoFrame)
        self.scrollArea.setWidgetResizable(True)
        self.scrollArea.setObjectName(_fromUtf8("scrollArea"))
        self.scrollAreaWidgetContents = QtGui.QWidget()
        self.scrollAreaWidgetContents.setGeometry(QtCore.QRect(0, 0, 400, 810))
        self.scrollAreaWidgetContents.setObjectName(_fromUtf8("scrollAreaWidgetContents"))
        self.verticalLayout = QtGui.QVBoxLayout(self.scrollAreaWidgetContents)
        self.verticalLayout.setMargin(0)
        self.verticalLayout.setObjectName(_fromUtf8("verticalLayout"))
        self.checkGroup = QtGui.QGroupBox(self.scrollAreaWidgetContents)
        self.checkGroup.setObjectName(_fromUtf8("checkGroup"))
        self.gridLayout_5 = QtGui.QGridLayout(self.checkGroup)
        self.gridLayout_5.setObjectName(_fromUtf8("gridLayout_5"))
        self.contextDataStatusLabel = QtGui.QLabel(self.checkGroup)
        self.contextDataStatusLabel.setMaximumSize(QtCore.QSize(16, 16))
        self.contextDataStatusLabel.setText(_fromUtf8(""))
        self.contextDataStatusLabel.setPixmap(QtGui.QPixmap(_fromUtf8(":/plugins/ark/plan/statusUnknown.png")))
        self.contextDataStatusLabel.setObjectName(_fromUtf8("contextDataStatusLabel"))
        self.gridLayout_5.addWidget(self.contextDataStatusLabel, 2, 7, 1, 1, QtCore.Qt.AlignHCenter)
        self.editContexLabel = QtGui.QLabel(self.checkGroup)
        self.editContexLabel.setObjectName(_fromUtf8("editContexLabel"))
        self.gridLayout_5.addWidget(self.editContexLabel, 5, 0, 1, 4)
        self.label_4 = QtGui.QLabel(self.checkGroup)
        self.label_4.setText(_fromUtf8(""))
        self.label_4.setObjectName(_fromUtf8("label_4"))
        self.gridLayout_5.addWidget(self.label_4, 2, 6, 1, 1)
        self.contextSchematicLabel = QtGui.QLabel(self.checkGroup)
        self.contextSchematicLabel.setObjectName(_fromUtf8("contextSchematicLabel"))
        self.gridLayout_5.addWidget(self.contextSchematicLabel, 3, 0, 1, 4)
        self.findContextTool = QtGui.QToolButton(self.checkGroup)
        icon = QtGui.QIcon()
        icon.addPixmap(QtGui.QPixmap(_fromUtf8(":/plugins/ark/plan/search.svg")), QtGui.QIcon.Normal, QtGui.QIcon.Off)
        self.findContextTool.setIcon(icon)
        self.findContextTool.setObjectName(_fromUtf8("findContextTool"))
        self.gridLayout_5.addWidget(self.findContextTool, 0, 6, 1, 1)
        self.contextDataLabel = QtGui.QLabel(self.checkGroup)
        self.contextDataLabel.setObjectName(_fromUtf8("contextDataLabel"))
        self.gridLayout_5.addWidget(self.contextDataLabel, 2, 0, 1, 4)
        self.zoomContextTool = QtGui.QToolButton(self.checkGroup)
        icon1 = QtGui.QIcon()
        icon1.addPixmap(QtGui.QPixmap(_fromUtf8(":/plugins/ark/plan/zoomToItem.svg")), QtGui.QIcon.Normal, QtGui.QIcon.Off)
        self.zoomContextTool.setIcon(icon1)
        self.zoomContextTool.setObjectName(_fromUtf8("zoomContextTool"))
        self.gridLayout_5.addWidget(self.zoomContextTool, 0, 7, 1, 1)
        self.contextSpin = QtGui.QSpinBox(self.checkGroup)
        self.contextSpin.setMaximum(99999)
        self.contextSpin.setObjectName(_fromUtf8("contextSpin"))
        self.gridLayout_5.addWidget(self.contextSpin, 0, 1, 1, 3)
        self.editContextButton = QtGui.QPushButton(self.checkGroup)
        self.editContextButton.setObjectName(_fromUtf8("editContextButton"))
        self.gridLayout_5.addWidget(self.editContextButton, 5, 6, 1, 2)
        self.contextLabel = QtGui.QLabel(self.checkGroup)
        self.contextLabel.setObjectName(_fromUtf8("contextLabel"))
        self.gridLayout_5.addWidget(self.contextLabel, 0, 0, 1, 1)
        self.contextSchematicStatusLabel = QtGui.QLabel(self.checkGroup)
        self.contextSchematicStatusLabel.setText(_fromUtf8(""))
        self.contextSchematicStatusLabel.setPixmap(QtGui.QPixmap(_fromUtf8(":/plugins/ark/plan/statusUnknown.png")))
        self.contextSchematicStatusLabel.setObjectName(_fromUtf8("contextSchematicStatusLabel"))
        self.gridLayout_5.addWidget(self.contextSchematicStatusLabel, 3, 7, 1, 1, QtCore.Qt.AlignHCenter)
        self.label_5 = QtGui.QLabel(self.checkGroup)
        self.label_5.setText(_fromUtf8(""))
        self.label_5.setObjectName(_fromUtf8("label_5"))
        self.gridLayout_5.addWidget(self.label_5, 3, 6, 1, 1)
        self.sectionSchematicStatusLabel = QtGui.QLabel(self.checkGroup)
        self.sectionSchematicStatusLabel.setText(_fromUtf8(""))
        self.sectionSchematicStatusLabel.setPixmap(QtGui.QPixmap(_fromUtf8(":/plugins/ark/plan/statusUnknown.png")))
        self.sectionSchematicStatusLabel.setObjectName(_fromUtf8("sectionSchematicStatusLabel"))
        self.gridLayout_5.addWidget(self.sectionSchematicStatusLabel, 4, 7, 1, 1, QtCore.Qt.AlignHCenter)
        self.sectionSchematicLabel = QtGui.QLabel(self.checkGroup)
        self.sectionSchematicLabel.setObjectName(_fromUtf8("sectionSchematicLabel"))
        self.gridLayout_5.addWidget(self.sectionSchematicLabel, 4, 0, 1, 2)
        self.verticalLayout.addWidget(self.checkGroup)
        self.cloneGroup = QtGui.QGroupBox(self.scrollAreaWidgetContents)
        self.cloneGroup.setObjectName(_fromUtf8("cloneGroup"))
        self.gridLayout_3 = QtGui.QGridLayout(self.cloneGroup)
        self.gridLayout_3.setObjectName(_fromUtf8("gridLayout_3"))
        self.label_2 = QtGui.QLabel(self.cloneGroup)
        self.label_2.setObjectName(_fromUtf8("label_2"))
        self.gridLayout_3.addWidget(self.label_2, 5, 0, 1, 3)
        self.sourceContextLabel = QtGui.QLabel(self.cloneGroup)
        self.sourceContextLabel.setObjectName(_fromUtf8("sourceContextLabel"))
        self.gridLayout_3.addWidget(self.sourceContextLabel, 0, 0, 1, 1)
        self.copySourceButton = QtGui.QPushButton(self.cloneGroup)
        self.copySourceButton.setObjectName(_fromUtf8("copySourceButton"))
        self.gridLayout_3.addWidget(self.copySourceButton, 5, 3, 1, 2)
        self.label_7 = QtGui.QLabel(self.cloneGroup)
        self.label_7.setText(_fromUtf8(""))
        self.label_7.setObjectName(_fromUtf8("label_7"))
        self.gridLayout_3.addWidget(self.label_7, 3, 3, 1, 1)
        self.sourceSchematicLabel = QtGui.QLabel(self.cloneGroup)
        self.sourceSchematicLabel.setObjectName(_fromUtf8("sourceSchematicLabel"))
        self.gridLayout_3.addWidget(self.sourceSchematicLabel, 3, 0, 1, 3)
        self.label = QtGui.QLabel(self.cloneGroup)
        self.label.setObjectName(_fromUtf8("label"))
        self.gridLayout_3.addWidget(self.label, 4, 0, 1, 3)
        self.label_8 = QtGui.QLabel(self.cloneGroup)
        self.label_8.setObjectName(_fromUtf8("label_8"))
        self.gridLayout_3.addWidget(self.label_8, 6, 0, 1, 3)
        self.findSourceTool = QtGui.QToolButton(self.cloneGroup)
        self.findSourceTool.setIcon(icon)
        self.findSourceTool.setObjectName(_fromUtf8("findSourceTool"))
        self.gridLayout_3.addWidget(self.findSourceTool, 0, 3, 1, 1)
        self.zoomSourceTool = QtGui.QToolButton(self.cloneGroup)
        self.zoomSourceTool.setIcon(icon1)
        self.zoomSourceTool.setObjectName(_fromUtf8("zoomSourceTool"))
        self.gridLayout_3.addWidget(self.zoomSourceTool, 0, 4, 1, 1)
        self.sourceSchematicStatusLabel = QtGui.QLabel(self.cloneGroup)
        self.sourceSchematicStatusLabel.setMaximumSize(QtCore.QSize(16, 16))
        self.sourceSchematicStatusLabel.setText(_fromUtf8(""))
        self.sourceSchematicStatusLabel.setPixmap(QtGui.QPixmap(_fromUtf8(":/plugins/ark/plan/statusUnknown.png")))
        self.sourceSchematicStatusLabel.setObjectName(_fromUtf8("sourceSchematicStatusLabel"))
        self.gridLayout_3.addWidget(self.sourceSchematicStatusLabel, 3, 4, 1, 1, QtCore.Qt.AlignHCenter)
        self.cloneSourceButton = QtGui.QPushButton(self.cloneGroup)
        self.cloneSourceButton.setObjectName(_fromUtf8("cloneSourceButton"))
        self.gridLayout_3.addWidget(self.cloneSourceButton, 4, 3, 1, 2)
        self.sourceDataStatusLabel = QtGui.QLabel(self.cloneGroup)
        self.sourceDataStatusLabel.setMaximumSize(QtCore.QSize(16, 16))
        self.sourceDataStatusLabel.setText(_fromUtf8(""))
        self.sourceDataStatusLabel.setPixmap(QtGui.QPixmap(_fromUtf8(":/plugins/ark/plan/statusUnknown.png")))
        self.sourceDataStatusLabel.setObjectName(_fromUtf8("sourceDataStatusLabel"))
        self.gridLayout_3.addWidget(self.sourceDataStatusLabel, 2, 4, 1, 1, QtCore.Qt.AlignHCenter)
        self.sourceContextSpin = QtGui.QSpinBox(self.cloneGroup)
        self.sourceContextSpin.setMaximum(99999)
        self.sourceContextSpin.setObjectName(_fromUtf8("sourceContextSpin"))
        self.gridLayout_3.addWidget(self.sourceContextSpin, 0, 1, 1, 2)
        self.editSourceButton = QtGui.QPushButton(self.cloneGroup)
        self.editSourceButton.setObjectName(_fromUtf8("editSourceButton"))
        self.gridLayout_3.addWidget(self.editSourceButton, 6, 3, 1, 2)
        self.sourceDataLabel = QtGui.QLabel(self.cloneGroup)
        self.sourceDataLabel.setObjectName(_fromUtf8("sourceDataLabel"))
        self.gridLayout_3.addWidget(self.sourceDataLabel, 2, 0, 1, 3)
        self.label_6 = QtGui.QLabel(self.cloneGroup)
        self.label_6.setText(_fromUtf8(""))
        self.label_6.setObjectName(_fromUtf8("label_6"))
        self.gridLayout_3.addWidget(self.label_6, 2, 3, 1, 1)
        self.verticalLayout.addWidget(self.cloneGroup)
        self.metadataWidget = MetadataWidget(self.scrollAreaWidgetContents)
        self.metadataWidget.setObjectName(_fromUtf8("metadataWidget"))
        self.verticalLayout.addWidget(self.metadataWidget)
        self.drawGroup = QtGui.QGroupBox(self.scrollAreaWidgetContents)
        self.drawGroup.setObjectName(_fromUtf8("drawGroup"))
        self.gridLayout_4 = QtGui.QGridLayout(self.drawGroup)
        self.gridLayout_4.setObjectName(_fromUtf8("gridLayout_4"))
        self.contextToolsLayout = QtGui.QGridLayout()
        self.contextToolsLayout.setObjectName(_fromUtf8("contextToolsLayout"))
        self.gridLayout_4.addLayout(self.contextToolsLayout, 0, 0, 1, 2)
        self.autoSchematiclLabel = QtGui.QLabel(self.drawGroup)
        self.autoSchematiclLabel.setObjectName(_fromUtf8("autoSchematiclLabel"))
        self.gridLayout_4.addWidget(self.autoSchematiclLabel, 1, 0, 1, 1)
        self.autoSchematicTool = QtGui.QToolButton(self.drawGroup)
        icon2 = QtGui.QIcon()
        icon2.addPixmap(QtGui.QPixmap(_fromUtf8(":/plugins/ark/plan/autoSchematic.png")), QtGui.QIcon.Normal, QtGui.QIcon.Off)
        self.autoSchematicTool.setIcon(icon2)
        self.autoSchematicTool.setObjectName(_fromUtf8("autoSchematicTool"))
        self.gridLayout_4.addWidget(self.autoSchematicTool, 1, 1, 1, 1)
        self.editPolygonsLabel = QtGui.QLabel(self.drawGroup)
        self.editPolygonsLabel.setObjectName(_fromUtf8("editPolygonsLabel"))
        self.gridLayout_4.addWidget(self.editPolygonsLabel, 3, 0, 1, 1)
        self.editLinesLabel = QtGui.QLabel(self.drawGroup)
        self.editLinesLabel.setObjectName(_fromUtf8("editLinesLabel"))
        self.gridLayout_4.addWidget(self.editLinesLabel, 2, 0, 1, 1)
        self.editLinesTool = QtGui.QToolButton(self.drawGroup)
        icon3 = QtGui.QIcon()
        icon3.addPixmap(QtGui.QPixmap(_fromUtf8(":/plugins/ark/plan/nodeTool.png")), QtGui.QIcon.Normal, QtGui.QIcon.Off)
        self.editLinesTool.setIcon(icon3)
        self.editLinesTool.setObjectName(_fromUtf8("editLinesTool"))
        self.gridLayout_4.addWidget(self.editLinesTool, 2, 1, 1, 1)
        self.editPolygonsTool = QtGui.QToolButton(self.drawGroup)
        self.editPolygonsTool.setIcon(icon3)
        self.editPolygonsTool.setObjectName(_fromUtf8("editPolygonsTool"))
        self.gridLayout_4.addWidget(self.editPolygonsTool, 3, 1, 1, 1)
        self.verticalLayout.addWidget(self.drawGroup)
        spacerItem = QtGui.QSpacerItem(17, 10, QtGui.QSizePolicy.Minimum, QtGui.QSizePolicy.Expanding)
        self.verticalLayout.addItem(spacerItem)
        self.scrollArea.setWidget(self.scrollAreaWidgetContents)
        self.verticalLayout_2.addWidget(self.scrollArea)
        self.buttonGroup = QtGui.QHBoxLayout()
        self.buttonGroup.setObjectName(_fromUtf8("buttonGroup"))
        self.resetButton = QtGui.QPushButton(SchematicWidget)
        self.resetButton.setObjectName(_fromUtf8("resetButton"))
        self.buttonGroup.addWidget(self.resetButton)
        self.clearButton = QtGui.QPushButton(SchematicWidget)
        self.clearButton.setObjectName(_fromUtf8("clearButton"))
        self.buttonGroup.addWidget(self.clearButton)
        self.mergeButton = QtGui.QPushButton(SchematicWidget)
        self.mergeButton.setObjectName(_fromUtf8("mergeButton"))
        self.buttonGroup.addWidget(self.mergeButton)
        self.verticalLayout_2.addLayout(self.buttonGroup)
        self.contextLabel.setBuddy(self.contextSpin)
        self.sourceContextLabel.setBuddy(self.sourceContextSpin)

        self.retranslateUi(SchematicWidget)
        QtCore.QMetaObject.connectSlotsByName(SchematicWidget)

    def retranslateUi(self, SchematicWidget):
        SchematicWidget.setWindowTitle(_translate("SchematicWidget", "Form", None))
        self.checkGroup.setTitle(_translate("SchematicWidget", "Check", None))
        self.editContexLabel.setText(_translate("SchematicWidget", "Edit Context:", None))
        self.contextSchematicLabel.setText(_translate("SchematicWidget", "Has Schematic:", None))
        self.findContextTool.setToolTip(_translate("SchematicWidget", "<html><head/><body><p>Pan to Context</p></body></html>", None))
        self.findContextTool.setText(_translate("SchematicWidget", "...", None))
        self.contextDataLabel.setText(_translate("SchematicWidget", "Has Features:", None))
        self.zoomContextTool.setToolTip(_translate("SchematicWidget", "<html><head/><body><p>Zoom to Context</p></body></html>", None))
        self.zoomContextTool.setText(_translate("SchematicWidget", "...", None))
        self.contextSpin.setToolTip(_translate("SchematicWidget", "<html><head/><body><p>Enter Context to find</p></body></html>", None))
        self.editContextButton.setText(_translate("SchematicWidget", "Edit", None))
        self.contextLabel.setText(_translate("SchematicWidget", "Check Context:", None))
        self.sectionSchematicLabel.setText(_translate("SchematicWidget", "Has Section Schematic:", None))
        self.cloneGroup.setTitle(_translate("SchematicWidget", "Clone", None))
        self.label_2.setText(_translate("SchematicWidget", "Copy and Edit Schematic:", None))
        self.sourceContextLabel.setText(_translate("SchematicWidget", "Source Context:", None))
        self.copySourceButton.setText(_translate("SchematicWidget", "Copy", None))
        self.sourceSchematicLabel.setText(_translate("SchematicWidget", "Has Schematic:", None))
        self.label.setText(_translate("SchematicWidget", "Clone and Save Schematic:", None))
        self.label_8.setText(_translate("SchematicWidget", "Edit Source Context:", None))
        self.findSourceTool.setToolTip(_translate("SchematicWidget", "<html><head/><body><p>Pan to Context</p></body></html>", None))
        self.findSourceTool.setText(_translate("SchematicWidget", "...", None))
        self.zoomSourceTool.setToolTip(_translate("SchematicWidget", "<html><head/><body><p>Zoom to Context</p></body></html>", None))
        self.zoomSourceTool.setText(_translate("SchematicWidget", "...", None))
        self.cloneSourceButton.setText(_translate("SchematicWidget", "Clone", None))
        self.sourceContextSpin.setToolTip(_translate("SchematicWidget", "<html><head/><body><p>Enter Source Context to find</p></body></html>", None))
        self.editSourceButton.setText(_translate("SchematicWidget", "Edit", None))
        self.sourceDataLabel.setText(_translate("SchematicWidget", "Has Features:", None))
        self.drawGroup.setTitle(_translate("SchematicWidget", "Draw", None))
        self.autoSchematiclLabel.setText(_translate("SchematicWidget", "Auto Schematic:", None))
        self.autoSchematicTool.setToolTip(_translate("SchematicWidget", "<html><head/><body><p>Auto Schematic</p></body></html>", None))
        self.autoSchematicTool.setText(_translate("SchematicWidget", "...", None))
        self.editPolygonsLabel.setText(_translate("SchematicWidget", "Edit Polygon Features:", None))
        self.editLinesLabel.setText(_translate("SchematicWidget", "Edit Line Features:", None))
        self.editLinesTool.setToolTip(_translate("SchematicWidget", "<html><head/><body><p>Edit Line Features</p></body></html>", None))
        self.editLinesTool.setText(_translate("SchematicWidget", "...", None))
        self.editPolygonsTool.setToolTip(_translate("SchematicWidget", "<html><head/><body><p>Edit Polygon Features</p></body></html>", None))
        self.editPolygonsTool.setText(_translate("SchematicWidget", "...", None))
        self.resetButton.setText(_translate("SchematicWidget", "Reset", None))
        self.clearButton.setToolTip(_translate("SchematicWidget", "Clear unsaved changes from work layers", None))
        self.clearButton.setText(_translate("SchematicWidget", "Clear", None))
        self.mergeButton.setToolTip(_translate("SchematicWidget", "Move new context to main layers", None))
        self.mergeButton.setText(_translate("SchematicWidget", "Merge", None))

from metadata_widget import MetadataWidget
import resources_rc
