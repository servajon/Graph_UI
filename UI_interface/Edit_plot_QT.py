import sys

from PyQt5 import QtWidgets, QtCore
from PyQt5.QtCore import pyqtSignal
from PyQt5.QtGui import QColor, QIcon
from PyQt5.QtWidgets import QWidget

from Resources_file import Resources


class Edit_plot(QWidget):
    finish_signal = pyqtSignal(str)

    edit_signal = pyqtSignal(int)

    def __init__(self, parent):
        super().__init__(parent)
        self.setWindowFlags(QtCore.Qt.Dialog | QtCore.Qt.WindowCloseButtonHint)
        self.setupUi(self)

    def setupUi(self, Dialog):
        Dialog.setObjectName("Edit Plot")
        Dialog.resize(325, 313)
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
        self.pushButton_2 = QtWidgets.QPushButton(Dialog)
        self.pushButton_2.setObjectName("pushButton_2")
        self.horizontalLayout.addWidget(self.pushButton_2)
        self.verticalLayout.addLayout(self.horizontalLayout)
        self.gridLayout_2 = QtWidgets.QGridLayout()
        self.gridLayout_2.setObjectName("gridLayout_2")
        self.label_5 = QtWidgets.QLabel(Dialog)
        self.label_5.setObjectName("label_5")
        self.gridLayout_2.addWidget(self.label_5, 0, 0, 1, 1)
        self.lineEdit_4 = QtWidgets.QLineEdit(Dialog)
        self.lineEdit_4.setObjectName("lineEdit_4")
        self.gridLayout_2.addWidget(self.lineEdit_4, 0, 2, 1, 1)
        self.label_6 = QtWidgets.QLabel(Dialog)
        self.label_6.setObjectName("label_6")
        self.gridLayout_2.addWidget(self.label_6, 1, 0, 1, 1)
        self.comboBox_left = QtWidgets.QComboBox(Dialog)
        self.comboBox_left.setObjectName("comboBox_left")
        self.gridLayout_2.addWidget(self.comboBox_left, 1, 2, 1, 1)
        spacerItem = QtWidgets.QSpacerItem(40, 20, QtWidgets.QSizePolicy.Expanding, QtWidgets.QSizePolicy.Minimum)
        self.gridLayout_2.addItem(spacerItem, 0, 1, 1, 1)
        spacerItem1 = QtWidgets.QSpacerItem(40, 20, QtWidgets.QSizePolicy.Expanding, QtWidgets.QSizePolicy.Minimum)
        self.gridLayout_2.addItem(spacerItem1, 1, 1, 1, 1)

        self.comboBox_type_line_left = QtWidgets.QComboBox(Dialog)
        self.comboBox_type_line_left.setObjectName("comboBox_type_line_left")
        self.gridLayout_2.addWidget(self.comboBox_type_line_left, 2, 2, 1, 1)
        spacerItem2 = QtWidgets.QSpacerItem(40, 20, QtWidgets.QSizePolicy.Expanding, QtWidgets.QSizePolicy.Minimum)
        self.gridLayout_2.addItem(spacerItem2, 2, 1, 1, 1)
        self.label_7 = QtWidgets.QLabel(Dialog)
        self.label_7.setObjectName("label_7")
        self.gridLayout_2.addWidget(self.label_7, 2, 0, 1, 1)

        self.verticalLayout.addLayout(self.gridLayout_2)
        self.horizontalLayout_2 = QtWidgets.QHBoxLayout()
        self.horizontalLayout_2.setObjectName("horizontalLayout_2")
        self.pushButton_3 = QtWidgets.QPushButton(Dialog)
        self.pushButton_3.setObjectName("pushButton_3")
        self.horizontalLayout_2.addWidget(self.pushButton_3)
        spacerItem3 = QtWidgets.QSpacerItem(40, 20, QtWidgets.QSizePolicy.Expanding, QtWidgets.QSizePolicy.Minimum)
        self.horizontalLayout_2.addItem(spacerItem3)
        self.pushButton_5 = QtWidgets.QPushButton(Dialog)
        self.pushButton_5.setObjectName("pushButton_5")
        self.horizontalLayout_2.addWidget(self.pushButton_5)
        self.verticalLayout.addLayout(self.horizontalLayout_2)

        self.retranslateUi(Dialog)
        QtCore.QMetaObject.connectSlotsByName(Dialog)

        self.pushButton_3.clicked.connect(self.save)
        self.pushButton_5.clicked.connect(self.cancel)
        self.pushButton.clicked.connect(self.edit)
        self.pushButton_2.clicked.connect(self.hide)

        self.listWidget.currentItemChanged.connect(self.change_current)

        # vecteur qui garde la trace de quel axe a été édité
        self.edited = []

    def retranslateUi(self, Dialog):
        _translate = QtCore.QCoreApplication.translate
        Dialog.setWindowTitle(_translate("Dialog", "Edit Plot"))
        self.label.setText(_translate("Dialog",
                                      "<html><head/><body><p><span style=\" font-size:18pt;\">Plot1</span></p></body></html>"))
        self.pushButton.setText(_translate("Dialog", "Edit"))
        self.pushButton_2.setText(_translate("Dialog", "Hide"))
        self.label_5.setText(_translate("Dialog",
                                        "<html><head/><body><p><span style=\" font-size:8pt;\">Rescale Margin (%)</span></p></body></html>"))
        self.label_6.setText(_translate("Dialog",
                                        "<html><head/><body><p><span style=\" font-size:8pt;\">Color left axis</span></p></body></html>"))
        self.label_7.setText(_translate("Dialog",
                                        "<html><head/><body><p><span style=\" font-size:8pt;\">Style lines left axis</span></p></body></html>"))
        self.pushButton_3.setText(_translate("Dialog", "Save"))
        self.pushButton_5.setText(_translate("Dialog", "Cancel"))

        self.create_combobox_marker(self.comboBox_type_line_left)

    def save(self):
        self.finish_signal.emit("save")

    def cancel(self):
        self.finish_signal.emit("cancel")

    def closeEvent(self, event):
        self.finish_signal.emit("cancel")

    def change_current(self):
        if self.listWidget.currentItem() is not None:
            if self.listWidget.currentItem().foreground().color() == QColor(
                    "red") and self.pushButton_2.text() == "Hide":
                self.pushButton_2.setText("Show")
            elif self.listWidget.currentItem().foreground().color() == QColor(
                    "black") and self.pushButton_2.text() == "Show":
                self.pushButton_2.setText("Hide")

    def edit(self):
        self.edit_signal.emit(self.listWidget.currentRow())
        self.listWidget.item(0).foreground()

    def create_combobox_marker(self, combo_item):
        index = 1
        combo_item.addItem("unchanged")
        for key, value in Resources.MARKERS_PLOT.items():
            path = sys.path[0] + "/Resources_img/Marker_plot/" + value + ".png"
            icon = QIcon(path)
            combo_item.addItem(str(value))
            combo_item.setItemIcon(index, icon)
            index += 1

    def hide(self):
        red = QColor("red")
        if self.listWidget.currentItem().foreground().color() == red:
            self.listWidget.currentItem().setForeground(QColor("black"))
            self.pushButton_2.setText("Hide")

        else:
            self.listWidget.currentItem().setForeground(red)
            self.pushButton_2.setText("Show")