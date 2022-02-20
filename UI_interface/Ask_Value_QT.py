from PyQt5 import QtWidgets, QtCore
from PyQt5.QtCore import pyqtSignal

from Resources_file.Emit import Emit
from UI_interface.Line_edit_QT import Line_edit_float, Line_edit_int


class Ask_Value(QtWidgets.QWidget):
    finish_signal = pyqtSignal(str)

    def __init__(self, parent, type):
        super().__init__(parent)
        self.value = None
        self.emit = Emit()
        self.type = type
        self.setWindowFlags(QtCore.Qt.Dialog | QtCore.Qt.WindowCloseButtonHint)
        self.setupUi(self)

    def setupUi(self, Dialog):
        Dialog.setObjectName("Dialog")
        Dialog.resize(291, 136)
        Dialog.setMaximumSize(QtCore.QSize(16777215, 16777215))
        self.verticalLayout = QtWidgets.QVBoxLayout(Dialog)
        self.verticalLayout.setObjectName("verticalLayout")
        self.label = QtWidgets.QLabel(Dialog)
        self.label.setMinimumSize(QtCore.QSize(269, 41))
        self.label.setMaximumSize(QtCore.QSize(269, 41))
        self.label.setObjectName("label")
        self.verticalLayout.addWidget(self.label)
        self.horizontalLayout = QtWidgets.QHBoxLayout()
        self.horizontalLayout.setObjectName("horizontalLayout")
        self.label_2 = QtWidgets.QLabel(Dialog)
        self.label_2.setObjectName("label_2")
        self.horizontalLayout.addWidget(self.label_2)

        if self.type == "int":
            self.lineEdit = Line_edit_int(Dialog)
        elif self.type == "float":
            self.lineEdit = Line_edit_float(Dialog)

        self.lineEdit.setObjectName("lineEdit")
        self.horizontalLayout.addWidget(self.lineEdit)
        self.verticalLayout.addLayout(self.horizontalLayout)
        self.horizontalLayout_2 = QtWidgets.QHBoxLayout()
        self.horizontalLayout_2.setObjectName("horizontalLayout_2")
        self.pushButton = QtWidgets.QPushButton(Dialog)
        self.pushButton.setObjectName("pushButton")
        self.horizontalLayout_2.addWidget(self.pushButton)
        spacerItem = QtWidgets.QSpacerItem(40, 20, QtWidgets.QSizePolicy.Expanding, QtWidgets.QSizePolicy.Minimum)
        self.horizontalLayout_2.addItem(spacerItem)
        self.pushButton_2 = QtWidgets.QPushButton(Dialog)
        self.pushButton_2.setObjectName("pushButton_2")
        self.horizontalLayout_2.addWidget(self.pushButton_2)
        self.verticalLayout.addLayout(self.horizontalLayout_2)

        self.retranslateUi(Dialog)
        QtCore.QMetaObject.connectSlotsByName(Dialog)

        self.pushButton.clicked.connect(self.save)
        self.pushButton_2.clicked.connect(self.cancel)

    def retranslateUi(self, Dialog):
        _translate = QtCore.QCoreApplication.translate
        Dialog.setWindowTitle(_translate("Dialog", "Dialog"))
        self.label.setText(_translate("Dialog",
                                      "<html><head/><body><p><span style=\" font-size:12pt;\">Invalide mass Electode</span></p></body></html>"))
        self.label_2.setText(_translate("Dialog",
                                        "<html><head/><body><p><span style=\" font-size:12pt;\">New Mass (mg) : </span></p></body></html>"))
        self.pushButton.setText(_translate("Dialog", "Save"))
        self.pushButton_2.setText(_translate("Dialog", "Cancel"))

    def save(self):
        try:
            self.value = self.lineEdit.get_value()
        except ValueError:
            self.emit.emit("msg_console", type="msg_console", str="Empty selection",
                           foreground_color="red")
        else:
            self.finish_signal.emit("save")

    def cancel(self):
        self.finish_signal.emit("cancel")

    def closeEvent(self, event):
        self.finish_signal.emit("cancel")
