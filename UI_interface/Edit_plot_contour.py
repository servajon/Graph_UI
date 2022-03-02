# -*- coding: utf-8 -*-

# Form implementation generated from reading ui file 'edit_plot_contour.ui'
#
# Created by: PyQt5 UI code generator 5.15.6
#
# WARNING: Any manual changes made to this file will be lost when pyuic5 is
# run again.  Do not edit this file unless you know what you are doing.


from PyQt5 import QtCore, QtWidgets
from PyQt5.QtCore import pyqtSignal
from PyQt5.QtWidgets import QWidget

from UI_interface.Line_edit_QT import Line_edit_int


class Edit_plot_contour(QWidget):
    finish_signal = pyqtSignal(str)

    def __init__(self, parent):
        super().__init__(parent)

        self.__name__ = "Edit_plot_contour"
        self.setWindowFlags(QtCore.Qt.Dialog | QtCore.Qt.WindowCloseButtonHint)

        self.setWindowModality(QtCore.Qt.ApplicationModal)

        self.setupUi(self)

    def setupUi(self, Dialog):
        Dialog.setObjectName("Dialog")
        Dialog.resize(271, 150)
        self.verticalLayout = QtWidgets.QVBoxLayout(Dialog)
        self.verticalLayout.setObjectName("verticalLayout")
        self.label = QtWidgets.QLabel(Dialog)
        self.label.setObjectName("label")
        self.verticalLayout.addWidget(self.label)
        self.gridLayout_2 = QtWidgets.QGridLayout()
        self.gridLayout_2.setObjectName("gridLayout_2")
        self.label_6 = QtWidgets.QLabel(Dialog)
        self.label_6.setObjectName("label_6")
        self.gridLayout_2.addWidget(self.label_6, 0, 0, 1, 1)
        spacerItem = QtWidgets.QSpacerItem(40, 20, QtWidgets.QSizePolicy.Expanding, QtWidgets.QSizePolicy.Minimum)
        self.gridLayout_2.addItem(spacerItem, 0, 1, 1, 1)
        self.comboBox_left = QtWidgets.QComboBox(Dialog)
        self.comboBox_left.setObjectName("comboBox_left")
        self.gridLayout_2.addWidget(self.comboBox_left, 0, 3, 1, 1)
        self.label_7 = QtWidgets.QLabel(Dialog)
        self.label_7.setMaximumSize(QtCore.QSize(75, 23))
        self.label_7.setObjectName("label_7")
        self.gridLayout_2.addWidget(self.label_7, 1, 0, 1, 1)
        self.lineEdit = Line_edit_int(Dialog)
        self.lineEdit.setMaximumSize(QtCore.QSize(81, 20))
        self.lineEdit.setObjectName("lineEdit")
        self.gridLayout_2.addWidget(self.lineEdit, 1, 1, 1, 1)
        self.lineEdit_2 = Line_edit_int(Dialog)
        self.lineEdit_2.setMaximumSize(QtCore.QSize(81, 20))
        self.lineEdit_2.setObjectName("lineEdit_2")
        self.gridLayout_2.addWidget(self.lineEdit_2, 1, 3, 1, 1)
        spacerItem1 = QtWidgets.QSpacerItem(40, 20, QtWidgets.QSizePolicy.Expanding, QtWidgets.QSizePolicy.Minimum)
        self.gridLayout_2.addItem(spacerItem1, 0, 2, 1, 1)
        self.label_8 = QtWidgets.QLabel(Dialog)
        self.label_8.setMaximumSize(QtCore.QSize(29, 23))
        self.label_8.setObjectName("label_8")
        self.gridLayout_2.addWidget(self.label_8, 1, 2, 1, 1)
        self.verticalLayout.addLayout(self.gridLayout_2)
        self.horizontalLayout_2 = QtWidgets.QHBoxLayout()
        self.horizontalLayout_2.setObjectName("horizontalLayout_2")
        self.pushButton_3 = QtWidgets.QPushButton(Dialog)
        self.pushButton_3.setObjectName("pushButton_3")
        self.horizontalLayout_2.addWidget(self.pushButton_3)
        spacerItem2 = QtWidgets.QSpacerItem(40, 20, QtWidgets.QSizePolicy.Expanding, QtWidgets.QSizePolicy.Minimum)
        self.horizontalLayout_2.addItem(spacerItem2)
        self.pushButton_5 = QtWidgets.QPushButton(Dialog)
        self.pushButton_5.setObjectName("pushButton_5")
        self.horizontalLayout_2.addWidget(self.pushButton_5)
        self.verticalLayout.addLayout(self.horizontalLayout_2)

        self.pushButton_3.clicked.connect(self.save)
        self.pushButton_5.clicked.connect(self.cancel)

        self.retranslateUi(Dialog)
        QtCore.QMetaObject.connectSlotsByName(Dialog)

    def retranslateUi(self, Dialog):
        _translate = QtCore.QCoreApplication.translate
        Dialog.setWindowTitle(_translate("Dialog", "Dialog"))
        self.label.setText(_translate("Dialog",
                                      "<html><head/><body><p><span style=\" font-size:18pt;\">Plot1</span></p></body></html>"))
        self.label_6.setText(_translate("Dialog",
                                        "<html><head/><body><p><span style=\" font-size:14pt;\">Color</span></p></body></html>"))
        self.label_7.setText(_translate("Dialog",
                                        "<html><head/><body><p align=\"center\"><span style=\" font-size:14pt;\">Start at :</span></p></body></html>"))
        self.label_8.setText(_translate("Dialog",
                                        "<html><head/><body><p align=\"center\"><span style=\" font-size:14pt;\">to :</span></p></body></html>"))
        self.pushButton_3.setText(_translate("Dialog", "Save"))
        self.pushButton_5.setText(_translate("Dialog", "Cancel"))

    def save(self):
        self.finish_signal.emit("save")

    def cancel(self):
        self.finish_signal.emit("cancel")