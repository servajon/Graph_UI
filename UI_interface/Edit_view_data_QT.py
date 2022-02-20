from PyQt5 import QtWidgets, QtCore
from PyQt5.QtCore import pyqtSignal
from PyQt5.QtGui import QColor
from PyQt5.QtWidgets import QWidget


class Edit_view_data(QWidget):
    finish_signal = pyqtSignal(str)

    def __init__(self, parent):
        super().__init__(parent)
        self.setWindowFlags(QtCore.Qt.Dialog | QtCore.Qt.WindowCloseButtonHint)
        self.setupUi(self)
        self.names_selected = []

    def setupUi(self, Dialog):
        Dialog.setObjectName("Dialog")
        Dialog.resize(343, 324)
        self.verticalLayout = QtWidgets.QVBoxLayout(Dialog)
        self.verticalLayout.setObjectName("verticalLayout")
        self.label = QtWidgets.QLabel(Dialog)
        self.label.setObjectName("label")
        self.verticalLayout.addWidget(self.label)
        self.listWidget = QtWidgets.QListWidget(Dialog)
        self.listWidget.setObjectName("listWidget")
        self.verticalLayout.addWidget(self.listWidget)
        self.horizontalLayout = QtWidgets.QHBoxLayout()
        self.horizontalLayout.setObjectName("horizontalLayout")
        self.pushButton = QtWidgets.QPushButton(Dialog)
        self.pushButton.setObjectName("pushButton")
        self.horizontalLayout.addWidget(self.pushButton)
        self.verticalLayout.addLayout(self.horizontalLayout)
        self.horizontalLayout_2 = QtWidgets.QHBoxLayout()
        self.horizontalLayout_2.setObjectName("horizontalLayout_2")
        self.pushButton_3 = QtWidgets.QPushButton(Dialog)
        self.pushButton_3.setObjectName("pushButton_3")
        self.horizontalLayout_2.addWidget(self.pushButton_3)
        spacerItem = QtWidgets.QSpacerItem(40, 20, QtWidgets.QSizePolicy.Expanding, QtWidgets.QSizePolicy.Minimum)
        self.horizontalLayout_2.addItem(spacerItem)
        self.pushButton_5 = QtWidgets.QPushButton(Dialog)
        self.pushButton_5.setObjectName("pushButton_5")
        self.horizontalLayout_2.addWidget(self.pushButton_5)
        self.verticalLayout.addLayout(self.horizontalLayout_2)

        self.retranslateUi(Dialog)
        QtCore.QMetaObject.connectSlotsByName(Dialog)

        self.pushButton_3.clicked.connect(self.save)
        self.pushButton_5.clicked.connect(self.cancel)
        self.pushButton.clicked.connect(self.edit)
        self.listWidget.currentItemChanged.connect(self.change_current)

    def retranslateUi(self, Dialog):
        _translate = QtCore.QCoreApplication.translate
        Dialog.setWindowTitle(_translate("Dialog", "Edit view data"))
        self.label.setText(
            _translate("Dialog", "<html><head/><body><p><span style=\" font-size:14pt;\"></span></p></body></html>"))
        self.pushButton.setText(_translate("Dialog", "Add"))
        self.pushButton_3.setText(_translate("Dialog", "Save"))
        self.pushButton_5.setText(_translate("Dialog", "Cancel"))

    def save(self):
        self.finish_signal.emit("save")

    def cancel(self):
        self.finish_signal.emit("cancel")

    def closeEvent(self, event):
        self.finish_signal.emit("cancel")

    def edit(self):
        green = QColor("green")
        if self.listWidget.currentItem().foreground().color() == green:
            self.names_selected.remove(self.listWidget.currentItem().text())
            self.listWidget.currentItem().setForeground(QColor("black"))
            self.pushButton.setText("Add")

        else:
            self.names_selected.append(self.listWidget.currentItem().text())
            self.listWidget.currentItem().setForeground(green)
            self.pushButton.setText("Remove")

    def change_current(self):
        if self.listWidget.currentItem() is not None:
            if self.listWidget.currentItem().foreground().color() == QColor(
                    "green") and self.pushButton.text() == "Add":
                self.pushButton.setText("Remove")
            elif self.listWidget.currentItem().foreground().color() == QColor(
                    "black") and self.pushButton.text() == "Remove":
                self.pushButton.setText("Add")