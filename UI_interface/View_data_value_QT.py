from PyQt5 import QtWidgets, QtCore
from PyQt5.QtCore import pyqtSignal
from PyQt5.QtWidgets import QWidget, QSizePolicy


class View_data_value(QWidget):
    finish_signal = pyqtSignal(str)

    def __init__(self, array_col, parent=None):
        super().__init__(parent)
        self.setupUi(self, array_col)

    def setupUi(self, Dialog, array_col):
        Dialog.setObjectName("Dialog")
        Dialog.resize(206, 172)
        self.verticalLayout = QtWidgets.QVBoxLayout(Dialog)
        self.verticalLayout.setObjectName("verticalLayout")
        self.label = QtWidgets.QLabel(Dialog)
        self.label.setMaximumSize(QtCore.QSize(16777215, 41))
        self.label.setObjectName("label")
        self.verticalLayout.addWidget(self.label)
        self.line = QtWidgets.QFrame(Dialog)
        self.line.setFrameShape(QtWidgets.QFrame.HLine)
        self.line.setFrameShadow(QtWidgets.QFrame.Sunken)
        self.line.setObjectName("line")
        self.verticalLayout.addWidget(self.line)
        self.gridLayout = QtWidgets.QGridLayout()
        self.gridLayout.setObjectName("gridLayout")

        for i, name in enumerate(array_col):
            label_name = QtWidgets.QLabel(Dialog)
            label_name.setText(name + " : ")
            self.gridLayout.addWidget(label_name, i, 1, 1, 1)

            label_value = QtWidgets.QLabel(Dialog)
            label_value.setText("None")
            self.gridLayout.addWidget(label_value, i, 2, 1, 1)

        self.verticalLayout.addLayout(self.gridLayout)

        self.retranslateUi(Dialog)
        QtCore.QMetaObject.connectSlotsByName(Dialog)

        self.setSizePolicy(QSizePolicy.MinimumExpanding, QSizePolicy.MinimumExpanding)
        self.adjustSize()

    def retranslateUi(self, Dialog):
        _translate = QtCore.QCoreApplication.translate
        Dialog.setWindowTitle(_translate("Dialog", "View Value"))
        self.label.setText(_translate("Dialog",
                                      "<html><head/><body><p><span style=\" font-size:12pt;\">Res figure blabla :</span></p></body></html>"))

    def closeEvent(self, event):
        self.finish_signal.emit("close")