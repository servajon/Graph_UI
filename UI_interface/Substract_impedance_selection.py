# -*- coding: utf-8 -*-

# Form implementation generated from reading ui file 'Substract_impedance_selection_ui.ui'
#
# Created by: PyQt5 UI code generator 5.15.6
#
# WARNING: Any manual changes made to this file will be lost when pyuic5 is
# run again.  Do not edit this file unless you know what you are doing.


from PyQt5 import QtCore, QtGui, QtWidgets
from PyQt5.QtCore import pyqtSignal

from Resources_file.Emit import Emit
from UI_interface.Line_edit_QT import Line_edit_int


class Substract_impedance_selection(QtWidgets.QWidget):
    finish_signal = pyqtSignal(str)

    def __init__(self, array_impedance_file, parent):
        super(Substract_impedance_selection, self).__init__(parent)
        self.setWindowFlags(QtCore.Qt.Dialog | QtCore.Qt.WindowCloseButtonHint)
        self.setWindowModality(QtCore.Qt.ApplicationModal)

        self.array_impedance_file = array_impedance_file

        self.emit = Emit()

        self.setupUi(self)

    def setupUi(self, Dialog):
        Dialog.setObjectName("Dialog")
        Dialog.resize(397, 205)
        self.verticalLayout = QtWidgets.QVBoxLayout(Dialog)
        self.verticalLayout.setObjectName("verticalLayout")
        self.label = QtWidgets.QLabel(Dialog)
        sizePolicy = QtWidgets.QSizePolicy(QtWidgets.QSizePolicy.Preferred, QtWidgets.QSizePolicy.Fixed)
        sizePolicy.setHorizontalStretch(0)
        sizePolicy.setVerticalStretch(0)
        sizePolicy.setHeightForWidth(self.label.sizePolicy().hasHeightForWidth())
        self.label.setSizePolicy(sizePolicy)
        self.label.setObjectName("label")
        self.verticalLayout.addWidget(self.label)
        self.line = QtWidgets.QFrame(Dialog)
        self.line.setFrameShape(QtWidgets.QFrame.HLine)
        self.line.setFrameShadow(QtWidgets.QFrame.Sunken)
        self.line.setObjectName("line")
        self.verticalLayout.addWidget(self.line)
        self.horizontalLayout_2 = QtWidgets.QHBoxLayout()
        self.horizontalLayout_2.setObjectName("horizontalLayout_2")
        self.radioButton = QtWidgets.QRadioButton(Dialog)
        self.radioButton.setObjectName("radioButton")
        self.horizontalLayout_2.addWidget(self.radioButton)
        spacerItem = QtWidgets.QSpacerItem(40, 20, QtWidgets.QSizePolicy.Fixed, QtWidgets.QSizePolicy.Minimum)
        self.horizontalLayout_2.addItem(spacerItem)
        self.radioButton_2 = QtWidgets.QRadioButton(Dialog)
        self.radioButton_2.setObjectName("radioButton_2")
        self.horizontalLayout_2.addWidget(self.radioButton_2)
        self.verticalLayout.addLayout(self.horizontalLayout_2)
        self.horizontalLayout_3 = QtWidgets.QHBoxLayout()
        self.horizontalLayout_3.setObjectName("horizontalLayout_3")
        self.label_2 = QtWidgets.QLabel(Dialog)
        self.label_2.setObjectName("label_2")
        self.horizontalLayout_3.addWidget(self.label_2)
        self.comboBox = QtWidgets.QComboBox(Dialog)
        self.comboBox.setObjectName("comboBox")
        self.horizontalLayout_3.addWidget(self.comboBox)
        spacerItem1 = QtWidgets.QSpacerItem(40, 20, QtWidgets.QSizePolicy.Expanding, QtWidgets.QSizePolicy.Minimum)
        self.horizontalLayout_3.addItem(spacerItem1)
        self.label_3 = QtWidgets.QLabel(Dialog)
        self.label_3.setObjectName("label_3")
        self.horizontalLayout_3.addWidget(self.label_3)
        self.comboBox_2 = QtWidgets.QComboBox(Dialog)
        self.comboBox_2.setObjectName("comboBox_2")
        self.horizontalLayout_3.addWidget(self.comboBox_2)
        self.verticalLayout.addLayout(self.horizontalLayout_3)
        self.horizontalLayout_4 = QtWidgets.QHBoxLayout()
        self.horizontalLayout_4.setObjectName("horizontalLayout_4")
        self.label_4 = QtWidgets.QLabel(Dialog)
        self.label_4.setObjectName("label_4")
        self.horizontalLayout_4.addWidget(self.label_4)
        self.lineEdit = Line_edit_int(Dialog)
        self.lineEdit.setObjectName("lineEdit")
        self.horizontalLayout_4.addWidget(self.lineEdit)
        spacerItem2 = QtWidgets.QSpacerItem(40, 20, QtWidgets.QSizePolicy.Expanding, QtWidgets.QSizePolicy.Minimum)
        self.horizontalLayout_4.addItem(spacerItem2)
        self.label_5 = QtWidgets.QLabel(Dialog)
        self.label_5.setObjectName("label_5")
        self.horizontalLayout_4.addWidget(self.label_5)
        self.lineEdit_2 = Line_edit_int(Dialog)
        self.lineEdit_2.setObjectName("lineEdit_2")
        self.horizontalLayout_4.addWidget(self.lineEdit_2)
        self.verticalLayout.addLayout(self.horizontalLayout_4)
        self.horizontalLayout = QtWidgets.QHBoxLayout()
        self.horizontalLayout.setObjectName("horizontalLayout")
        self.pushButton_3 = QtWidgets.QPushButton(Dialog)
        self.pushButton_3.setObjectName("pushButton_3")
        self.horizontalLayout.addWidget(self.pushButton_3)
        spacerItem3 = QtWidgets.QSpacerItem(40, 20, QtWidgets.QSizePolicy.Expanding, QtWidgets.QSizePolicy.Minimum)
        self.horizontalLayout.addItem(spacerItem3)
        self.pushButton_5 = QtWidgets.QPushButton(Dialog)
        self.pushButton_5.setObjectName("pushButton_5")
        self.horizontalLayout.addWidget(self.pushButton_5)
        self.verticalLayout.addLayout(self.horizontalLayout)

        self.retranslateUi(Dialog)
        QtCore.QMetaObject.connectSlotsByName(Dialog)

        self.pushButton_3.clicked.connect(self.save)
        self.pushButton_5.clicked.connect(self.cancel)

        self.radioButton.clicked.connect(self.click_radio)
        self.radioButton_2.clicked.connect(self.click_radio)

        self.radioButton.setChecked(True)
        self.hide_horizontalLayout_3()

        for name in self.array_impedance_file:
            self.comboBox.addItem(name)
            self.comboBox_2.addItem(name)

    def retranslateUi(self, Dialog):
        _translate = QtCore.QCoreApplication.translate
        Dialog.setWindowTitle(_translate("Dialog", "Dialog"))
        self.label.setText(_translate("Dialog",
                                      "<html><head/><body><p><span style=\" font-size:10pt;\">Substact</span></p></body></html>"))
        self.radioButton.setText(_translate("Dialog", "Same File"))
        self.radioButton_2.setText(_translate("Dialog", "Different Files"))
        self.label_2.setText(_translate("Dialog",
                                        "<html><head/><body><p><span style=\" font-size:10pt;\">First File :</span></p></body></html>"))
        self.label_3.setText(_translate("Dialog",
                                        "<html><head/><body><p><span style=\" font-size:10pt;\">Second File :</span></p></body></html>"))
        self.label_4.setText(_translate("Dialog",
                                        "<html><head/><body><p><span style=\" font-size:10pt;\">First Cycle :</span></p></body></html>"))
        self.label_5.setText(_translate("Dialog",
                                        "<html><head/><body><p><span style=\" font-size:10pt;\">Second Cycle :</span></p></body></html>"))
        self.pushButton_3.setText(_translate("Dialog", "Save"))
        self.pushButton_5.setText(_translate("Dialog", "Cancel"))

    """----------------------------------------------------------------------------------"""

    def save(self):
        if self.radioButton.isChecked() and self.lineEdit.get_value() == self.lineEdit_2.get_value():
            self.emit.emit("msg_console", type="msg_console", str="Both cycles cannot be the same",
                           foreground_color="red")
        elif self.radioButton_2.isChecked() and self.comboBox.currentText() == self.comboBox_2.currentText():
            self.emit.emit("msg_console", type="msg_console", str="Both files cannot be the same",
                           foreground_color="red")

        elif self.lineEdit.get_value() < 1 or self.lineEdit_2.get_value() < 1:
            self.emit.emit("msg_console", type="msg_console", str="Cycle number cannot be less than 1",
                           foreground_color="red")
        else:
            self.finish_signal.emit("save")

    """----------------------------------------------------------------------------------"""

    def cancel(self):
        self.finish_signal.emit("cancel")

    """----------------------------------------------------------------------------------"""

    def closeEvent(self, event):
        self.finish_signal.emit("cancel")

    """----------------------------------------------------------------------------------"""

    def click_radio(self):
        if self.radioButton.isChecked():
            self.hide_horizontalLayout_3()
        else:
            self.show_horizontalLayout_3()

    def hide_horizontalLayout_3(self):
        self.label_2.hide()
        self.comboBox.hide()
        self.label_3.hide()
        self.comboBox_2.hide()

    def show_horizontalLayout_3(self):
        self.label_2.show()
        self.comboBox.show()
        self.label_3.show()
        self.comboBox_2.show()
