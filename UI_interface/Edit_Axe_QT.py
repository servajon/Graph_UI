from PyQt5 import QtWidgets, QtCore
from PyQt5.QtCore import pyqtSignal
from PyQt5.QtWidgets import QWidget


class Edit_Axe(QWidget):
    finish = pyqtSignal(str)

    def __init__(self, parent):
        super().__init__(parent)
        self.setWindowFlags(QtCore.Qt.Window)
        self.setupUi(self)

    def setupUi(self, Dialog):
        Dialog.setObjectName("Dialog")
        Dialog.resize(289, 271)
        self.verticalLayout = QtWidgets.QVBoxLayout(Dialog)
        self.verticalLayout.setObjectName("verticalLayout")
        self.label = QtWidgets.QLabel(Dialog)
        self.label.setMaximumSize(QtCore.QSize(16777215, 19))
        self.label.setObjectName("label")
        self.verticalLayout.addWidget(self.label)
        self.gridLayout = QtWidgets.QGridLayout()
        self.gridLayout.setObjectName("gridLayout")
        self.label_14 = QtWidgets.QLabel(Dialog)
        self.label_14.setMinimumSize(QtCore.QSize(0, 0))
        self.label_14.setMaximumSize(QtCore.QSize(16777215, 9999999))
        self.label_14.setObjectName("label_14")
        self.gridLayout.addWidget(self.label_14, 0, 0, 1, 1)
        spacerItem = QtWidgets.QSpacerItem(40, 20, QtWidgets.QSizePolicy.Expanding, QtWidgets.QSizePolicy.Minimum)
        self.gridLayout.addItem(spacerItem, 0, 1, 1, 1)
        self.lineEdit_2 = QtWidgets.QLineEdit(Dialog)
        self.lineEdit_2.setObjectName("lineEdit_2")
        self.gridLayout.addWidget(self.lineEdit_2, 0, 2, 1, 1)
        self.label_16 = QtWidgets.QLabel(Dialog)
        self.label_16.setMinimumSize(QtCore.QSize(0, 0))
        self.label_16.setMaximumSize(QtCore.QSize(16777215, 9999999))
        self.label_16.setObjectName("label_16")
        self.gridLayout.addWidget(self.label_16, 1, 0, 1, 1)
        self.comboBox_18 = QtWidgets.QComboBox(Dialog)
        self.comboBox_18.setMinimumSize(QtCore.QSize(0, 30))
        self.comboBox_18.setObjectName("comboBox_18")
        self.comboBox_18.addItem("")
        self.comboBox_18.addItem("")
        self.gridLayout.addWidget(self.comboBox_18, 1, 2, 1, 1)
        self.label_17 = QtWidgets.QLabel(Dialog)
        self.label_17.setMinimumSize(QtCore.QSize(0, 0))
        self.label_17.setMaximumSize(QtCore.QSize(16777215, 9999999))
        self.label_17.setObjectName("label_17")
        self.gridLayout.addWidget(self.label_17, 2, 0, 1, 1)
        self.comboBox_19 = QtWidgets.QComboBox(Dialog)
        self.comboBox_19.setMinimumSize(QtCore.QSize(0, 30))
        self.comboBox_19.setObjectName("comboBox_19")
        self.comboBox_19.addItem("")
        self.comboBox_19.addItem("")
        self.comboBox_19.addItem("")
        self.gridLayout.addWidget(self.comboBox_19, 2, 2, 1, 1)
        self.verticalLayout.addLayout(self.gridLayout)
        self.horizontalLayout = QtWidgets.QHBoxLayout()
        self.horizontalLayout.setObjectName("horizontalLayout")
        self.label_18 = QtWidgets.QLabel(Dialog)
        self.label_18.setMinimumSize(QtCore.QSize(0, 0))
        self.label_18.setMaximumSize(QtCore.QSize(16777215, 9999999))
        self.label_18.setObjectName("label_18")
        self.horizontalLayout.addWidget(self.label_18)
        self.lineEdit_3 = QtWidgets.QLineEdit(Dialog)
        self.lineEdit_3.setMinimumSize(QtCore.QSize(75, 0))
        self.lineEdit_3.setMaximumSize(QtCore.QSize(75, 16777215))
        self.lineEdit_3.setObjectName("lineEdit_3")
        self.horizontalLayout.addWidget(self.lineEdit_3)
        spacerItem1 = QtWidgets.QSpacerItem(40, 20, QtWidgets.QSizePolicy.Expanding, QtWidgets.QSizePolicy.Minimum)
        self.horizontalLayout.addItem(spacerItem1)
        self.label_19 = QtWidgets.QLabel(Dialog)
        self.label_19.setMinimumSize(QtCore.QSize(0, 0))
        self.label_19.setMaximumSize(QtCore.QSize(16777215, 9999999))
        self.label_19.setObjectName("label_19")
        self.horizontalLayout.addWidget(self.label_19, 0, QtCore.Qt.AlignLeft)
        self.lineEdit_4 = QtWidgets.QLineEdit(Dialog)
        self.lineEdit_4.setMinimumSize(QtCore.QSize(75, 0))
        self.lineEdit_4.setMaximumSize(QtCore.QSize(75, 16777215))
        self.lineEdit_4.setObjectName("lineEdit_4")
        self.horizontalLayout.addWidget(self.lineEdit_4, 0, QtCore.Qt.AlignLeft)
        self.verticalLayout.addLayout(self.horizontalLayout)
        self.horizontalLayout_2 = QtWidgets.QHBoxLayout()
        self.horizontalLayout_2.setObjectName("horizontalLayout_2")
        self.pushButton = QtWidgets.QPushButton(Dialog)
        self.pushButton.setObjectName("pushButton")
        self.horizontalLayout_2.addWidget(self.pushButton)
        spacerItem2 = QtWidgets.QSpacerItem(40, 20, QtWidgets.QSizePolicy.Expanding, QtWidgets.QSizePolicy.Minimum)
        self.horizontalLayout_2.addItem(spacerItem2)
        self.pushButton_2 = QtWidgets.QPushButton(Dialog)
        self.pushButton_2.setObjectName("pushButton_2")
        self.horizontalLayout_2.addWidget(self.pushButton_2)
        self.verticalLayout.addLayout(self.horizontalLayout_2)

        self.retranslateUi(Dialog)
        QtCore.QMetaObject.connectSlotsByName(Dialog)

        self.pushButton.clicked.connect(self.save_presed)
        self.pushButton_2.clicked.connect(self.save_cancel)

    def retranslateUi(self, Dialog):
        _translate = QtCore.QCoreApplication.translate
        Dialog.setWindowTitle(_translate("Dialog", "Dialog"))
        self.label.setText(_translate("Dialog",
                                      "<html><head/><body><p><span style=\" font-size:12pt;\">Edit Axe :</span></p></body></html>"))
        self.label_14.setText(_translate("Dialog",
                                         "<html><head/><body><p><span style=\" font-size:12pt;\">New name</span></p></body></html>"))
        self.label_16.setText(_translate("Dialog",
                                         "<html><head/><body><p><span style=\" font-size:12pt;\">Scale</span></p></body></html>"))
        self.comboBox_18.setItemText(0, _translate("Dialog", "Linear"))
        self.comboBox_18.setItemText(1, _translate("Dialog", "log"))
        self.label_17.setText(_translate("Dialog",
                                         "<html><head/><body><p><span style=\" font-size:12pt;\">Unite</span></p></body></html>"))
        self.comboBox_19.setItemText(0, _translate("Dialog", "test1"))
        self.comboBox_19.setItemText(1, _translate("Dialog", "test2"))
        self.comboBox_19.setItemText(2, _translate("Dialog", "test3"))
        self.label_18.setText(_translate("Dialog",
                                         "<html><head/><body><p><span style=\" font-size:12pt;\">Start at :</span></p></body></html>"))
        self.label_19.setText(_translate("Dialog",
                                         "<html><head/><body><p><span style=\" font-size:12pt;\">to :</span></p></body></html>"))
        self.pushButton.setText(_translate("Dialog", "save"))
        self.pushButton_2.setText(_translate("Dialog", "cancel"))

    def closeEvent(self, event):
        self.finish.emit("closed")

    def save_presed(self):
        self.finish.emit("save")

    def save_cancel(self):
        self.finish.emit("cancel")