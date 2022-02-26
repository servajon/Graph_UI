from PyQt5 import QtCore, QtGui, QtWidgets
from PyQt5.QtCore import pyqtSignal
from PyQt5.QtGui import QColor

from Resources_file.Emit import Emit


class Create_figure(QtWidgets.QWidget):
    finish_signal = pyqtSignal(str)

    def __init__(self, parent):
        super(Create_figure, self).__init__(parent)
        self.setWindowFlags(QtCore.Qt.Dialog | QtCore.Qt.WindowCloseButtonHint)
        self.setWindowModality(QtCore.Qt.ApplicationModal)
        self.x_items = []
        self.y1_items = []
        self.y2_items = []

        self.emit = Emit()

        self.setupUi(self)

    def setupUi(self, Dialog):
        Dialog.setObjectName("Dialog")
        Dialog.resize(260, 333)
        self.verticalLayout_3 = QtWidgets.QVBoxLayout(Dialog)
        self.verticalLayout_3.setObjectName("verticalLayout_3")
        self.horizontalLayout_8 = QtWidgets.QHBoxLayout()
        self.horizontalLayout_8.setObjectName("horizontalLayout_8")
        self.label_13 = QtWidgets.QLabel(Dialog)
        self.label_13.setMinimumSize(QtCore.QSize(111, 41))
        self.label_13.setMaximumSize(QtCore.QSize(111, 41))
        self.label_13.setObjectName("label_13")
        self.horizontalLayout_8.addWidget(self.label_13)
        self.lineEdit = QtWidgets.QLineEdit(Dialog)
        self.lineEdit.setMinimumSize(QtCore.QSize(111, 41))
        self.lineEdit.setMaximumSize(QtCore.QSize(111, 41))
        self.lineEdit.setObjectName("lineEdit")
        self.horizontalLayout_8.addWidget(self.lineEdit)
        spacerItem = QtWidgets.QSpacerItem(20, 20, QtWidgets.QSizePolicy.Expanding, QtWidgets.QSizePolicy.Minimum)
        self.horizontalLayout_8.addItem(spacerItem)
        self.verticalLayout_3.addLayout(self.horizontalLayout_8)
        self.verticalLayout = QtWidgets.QVBoxLayout()
        self.verticalLayout.setObjectName("verticalLayout")
        self.tabWidget = QtWidgets.QTabWidget(Dialog)
        self.tabWidget.setMinimumSize(QtCore.QSize(0, 0))
        self.tabWidget.setMaximumSize(QtCore.QSize(9999999, 9999999))
        self.tabWidget.setObjectName("tabWidget")
        self.tab = QtWidgets.QWidget()
        self.tab.setObjectName("tab")
        self.verticalLayout_2 = QtWidgets.QVBoxLayout(self.tab)
        self.verticalLayout_2.setObjectName("verticalLayout_2")
        self.listWidget = QtWidgets.QListWidget(self.tab)
        self.listWidget.setObjectName("listWidget")
        self.verticalLayout_2.addWidget(self.listWidget)
        self.horizontalLayout = QtWidgets.QHBoxLayout()
        self.horizontalLayout.setObjectName("horizontalLayout")
        self.pushButton_2 = QtWidgets.QPushButton(self.tab)
        self.pushButton_2.setObjectName("pushButton_2")
        self.horizontalLayout.addWidget(self.pushButton_2)
        self.verticalLayout_2.addLayout(self.horizontalLayout)
        self.horizontalLayout_6 = QtWidgets.QHBoxLayout()
        self.horizontalLayout_6.setObjectName("horizontalLayout_6")
        self.label_19 = QtWidgets.QLabel(self.tab)
        self.label_19.setMinimumSize(QtCore.QSize(93, 28))
        self.label_19.setMaximumSize(QtCore.QSize(16777215, 16777215))
        self.label_19.setObjectName("label_19")
        self.horizontalLayout_6.addWidget(self.label_19)
        spacerItem2 = QtWidgets.QSpacerItem(40, 20, QtWidgets.QSizePolicy.Expanding, QtWidgets.QSizePolicy.Expanding)
        self.horizontalLayout_6.addItem(spacerItem2)
        self.comboBox_21 = QtWidgets.QComboBox(self.tab)
        self.comboBox_21.setMinimumSize(QtCore.QSize(93, 28))
        self.comboBox_21.setMaximumSize(QtCore.QSize(16777215, 16777215))
        self.comboBox_21.setAutoFillBackground(True)
        self.comboBox_21.setSizeAdjustPolicy(QtWidgets.QComboBox.AdjustToMinimumContentsLength)
        self.comboBox_21.setObjectName("comboBox_21")
        self.comboBox_21.addItem("")
        self.comboBox_21.addItem("")
        self.horizontalLayout_6.addWidget(self.comboBox_21)
        self.verticalLayout_2.addLayout(self.horizontalLayout_6)
        self.tabWidget.addTab(self.tab, "")
        self.tab_2 = QtWidgets.QWidget()
        self.tab_2.setObjectName("tab_2")
        self.verticalLayout_4 = QtWidgets.QVBoxLayout(self.tab_2)
        self.verticalLayout_4.setObjectName("verticalLayout_4")
        self.listWidget_3 = QtWidgets.QListWidget(self.tab_2)
        self.listWidget_3.setObjectName("listWidget_3")
        self.verticalLayout_4.addWidget(self.listWidget_3)
        self.horizontalLayout_3 = QtWidgets.QHBoxLayout()
        self.horizontalLayout_3.setObjectName("horizontalLayout_3")
        self.pushButton_6 = QtWidgets.QPushButton(self.tab_2)
        self.pushButton_6.setObjectName("pushButton_6")
        self.horizontalLayout_3.addWidget(self.pushButton_6)
        self.verticalLayout_4.addLayout(self.horizontalLayout_3)
        self.horizontalLayout_5 = QtWidgets.QHBoxLayout()
        self.horizontalLayout_5.setObjectName("horizontalLayout_5")
        self.label_17 = QtWidgets.QLabel(self.tab_2)
        self.label_17.setMinimumSize(QtCore.QSize(93, 28))
        self.label_17.setMaximumSize(QtCore.QSize(16777215, 16777215))
        self.label_17.setObjectName("label_17")
        self.horizontalLayout_5.addWidget(self.label_17)
        spacerItem4 = QtWidgets.QSpacerItem(40, 20, QtWidgets.QSizePolicy.Expanding, QtWidgets.QSizePolicy.Expanding)
        self.horizontalLayout_5.addItem(spacerItem4)
        self.comboBox_19 = QtWidgets.QComboBox(self.tab_2)
        self.comboBox_19.setMinimumSize(QtCore.QSize(93, 28))
        self.comboBox_19.setMaximumSize(QtCore.QSize(16777215, 16777215))
        self.comboBox_19.setAutoFillBackground(True)
        self.comboBox_19.setSizeAdjustPolicy(QtWidgets.QComboBox.AdjustToMinimumContentsLength)
        self.comboBox_19.setObjectName("comboBox_19")
        self.comboBox_19.addItem("")
        self.comboBox_19.addItem("")
        self.horizontalLayout_5.addWidget(self.comboBox_19)
        self.verticalLayout_4.addLayout(self.horizontalLayout_5)
        self.tabWidget.addTab(self.tab_2, "")
        self.tab_4 = QtWidgets.QWidget()
        self.tab_4.setObjectName("tab_4")
        self.verticalLayout_6 = QtWidgets.QVBoxLayout(self.tab_4)
        self.verticalLayout_6.setObjectName("verticalLayout_6")
        self.listWidget_4 = QtWidgets.QListWidget(self.tab_4)
        self.listWidget_4.setObjectName("listWidget_4")
        self.verticalLayout_6.addWidget(self.listWidget_4)
        self.horizontalLayout_4 = QtWidgets.QHBoxLayout()
        self.horizontalLayout_4.setObjectName("horizontalLayout_4")
        self.pushButton_8 = QtWidgets.QPushButton(self.tab_4)
        self.pushButton_8.setObjectName("pushButton_8")
        self.horizontalLayout_4.addWidget(self.pushButton_8)
        self.verticalLayout_6.addLayout(self.horizontalLayout_4)
        self.horizontalLayout_7 = QtWidgets.QHBoxLayout()
        self.horizontalLayout_7.setObjectName("horizontalLayout_7")
        self.label_20 = QtWidgets.QLabel(self.tab_4)
        self.label_20.setMinimumSize(QtCore.QSize(93, 28))
        self.label_20.setMaximumSize(QtCore.QSize(16777215, 16777215))
        self.label_20.setObjectName("label_20")
        self.horizontalLayout_7.addWidget(self.label_20)
        spacerItem6 = QtWidgets.QSpacerItem(40, 20, QtWidgets.QSizePolicy.Expanding, QtWidgets.QSizePolicy.Expanding)
        self.horizontalLayout_7.addItem(spacerItem6)
        self.comboBox_22 = QtWidgets.QComboBox(self.tab_4)
        self.comboBox_22.setMinimumSize(QtCore.QSize(93, 28))
        self.comboBox_22.setMaximumSize(QtCore.QSize(16777215, 16777215))
        self.comboBox_22.setAutoFillBackground(True)
        self.comboBox_22.setSizeAdjustPolicy(QtWidgets.QComboBox.AdjustToMinimumContentsLength)
        self.comboBox_22.setObjectName("comboBox_22")
        self.comboBox_22.addItem("")
        self.comboBox_22.addItem("")
        self.horizontalLayout_7.addWidget(self.comboBox_22)
        self.verticalLayout_6.addLayout(self.horizontalLayout_7)
        self.tabWidget.addTab(self.tab_4, "")
        self.verticalLayout.addWidget(self.tabWidget)
        self.pushButton = QtWidgets.QPushButton(Dialog)
        self.pushButton.setMinimumSize(QtCore.QSize(0, 41))
        self.pushButton.setObjectName("pushButton")
        self.verticalLayout.addWidget(self.pushButton)
        self.verticalLayout_3.addLayout(self.verticalLayout)

        self.retranslateUi(Dialog)
        self.tabWidget.setCurrentIndex(0)
        QtCore.QMetaObject.connectSlotsByName(Dialog)

        self.listWidget.currentItemChanged.connect(lambda event: self.change_current(event, "x"))
        self.listWidget_3.currentItemChanged.connect(lambda event: self.change_current(event, "y1"))
        self.listWidget_4.currentItemChanged.connect(lambda event: self.change_current(event, "y2"))

        self.pushButton_2.clicked.connect(lambda event: self.click_button(event, "x"))
        self.pushButton_6.clicked.connect(lambda event: self.click_button(event, "y1"))
        self.pushButton_8.clicked.connect(lambda event: self.click_button(event, "y2"))

        self.pushButton.clicked.connect(self.save)




    def retranslateUi(self, Dialog):
        _translate = QtCore.QCoreApplication.translate
        Dialog.setWindowTitle(_translate("Dialog", "Dialog"))
        self.label_13.setText(_translate("Dialog", "<html><head/><body><p align=\"center\"><span style=\" font-size:12pt;\">Name</span></p></body></html>"))
        self.pushButton_2.setText(_translate("Dialog", "Add"))
        self.label_19.setText(_translate("Dialog", "<html><head/><body><p align=\"center\"><span style=\" font-size:12pt;\">Scale</span></p></body></html>"))
        self.comboBox_21.setItemText(0, _translate("Dialog", "Linear"))
        self.comboBox_21.setItemText(1, _translate("Dialog", "Log"))
        self.tabWidget.setTabText(self.tabWidget.indexOf(self.tab), _translate("Dialog", "X Axe"))
        self.pushButton_6.setText(_translate("Dialog", "Add"))
        self.label_17.setText(_translate("Dialog", "<html><head/><body><p align=\"center\"><span style=\" font-size:12pt;\">Scale</span></p></body></html>"))
        self.comboBox_19.setItemText(0, _translate("Dialog", "Linear"))
        self.comboBox_19.setItemText(1, _translate("Dialog", "Log"))
        self.tabWidget.setTabText(self.tabWidget.indexOf(self.tab_2), _translate("Dialog", "Left Axis"))
        self.pushButton_8.setText(_translate("Dialog", "Add"))
        self.label_20.setText(_translate("Dialog", "<html><head/><body><p align=\"center\"><span style=\" font-size:12pt;\">Scale</span></p></body></html>"))
        self.comboBox_22.setItemText(0, _translate("Dialog", "Linear"))
        self.comboBox_22.setItemText(1, _translate("Dialog", "Log"))
        self.tabWidget.setTabText(self.tabWidget.indexOf(self.tab_4), _translate("Dialog", "Right Axis"))
        self.pushButton.setText(_translate("Dialog", "Create"))

    def save(self):
        self.get_names()
        if not self.x_items:
            self.emit.emit("msg_console", type="msg_console", str="No data selected for the x axis",
                           foreground_color="red")
        elif not self.y1_items:
            self.emit.emit("msg_console", type="msg_console", str="You must select a data for left axis",
                           foreground_color="red")
        elif self.lineEdit.text() == "":
            self.emit.emit("msg_console", type="msg_console", str="You have to give a name to the new plot",
                           foreground_color="red")
        else:
            self.finish_signal.emit("save")

    def closeEvent(self, event):
        self.finish_signal.emit("cancel")

    def change_current(self, event, name):
        if name == "x" and self.listWidget.currentItem() is not None:
            if self.listWidget.currentItem().foreground().color() == QColor(
                    "green") and self.pushButton_2.text() == "Add":
                self.pushButton_2.setText("Remove")
            elif self.listWidget.currentItem().foreground().color() == QColor(
                    "black") and self.pushButton_2.text() == "Remove":
                self.pushButton_2.setText("Add")

        elif name == "y1" and self.listWidget_3.currentItem() is not None:
            if self.listWidget_3.currentItem().foreground().color() == QColor(
                    "green") and self.pushButton_6.text() == "Add":
                self.pushButton_6.setText("Remove")
            elif self.listWidget_3.currentItem().foreground().color() == QColor(
                    "black") and self.pushButton_6.text() == "Remove":
                self.pushButton_6.setText("Add")
        else:
            if self.listWidget_4.currentItem().foreground().color() == QColor(
                    "green") and self.pushButton_8.text() == "Add":
                self.pushButton_8.setText("Remove")
            elif self.listWidget_4.currentItem().foreground().color() == QColor(
                    "black") and self.pushButton_8.text() == "Remove":
                self.pushButton_8.setText("Add")

    def click_button(self, event, name):
        if self.listWidget.currentItem() is None and \
                self.listWidget_3.currentItem() is None and \
                self.listWidget_4.currentItem() is None:
            return

        green = QColor("green")
        if name == "x":
            if self.listWidget.currentItem().foreground().color() == green:
                self.listWidget.currentItem().setForeground(QColor("black"))
                self.pushButton_2.setText("Add")
            else:
                self.reset_color_all()
                self.listWidget.currentItem().setForeground(green)
                self.pushButton_2.setText("Remove")
        elif name == "y1":
            if self.listWidget_3.currentItem().foreground().color() == green:
                self.listWidget_3.currentItem().setForeground(QColor("black"))
                self.pushButton_6.setText("Add")
            else:
                self.listWidget_3.currentItem().setForeground(green)
                self.pushButton_6.setText("Remove")
        else:
            if self.listWidget_4.currentItem().foreground().color() == green:
                self.listWidget_4.currentItem().setForeground(QColor("black"))
                self.pushButton_8.setText("Add")
            else:
                self.listWidget_4.currentItem().setForeground(green)
                self.pushButton_8.setText("Remove")

    def reset_color_all(self):
        for i in range(self.listWidget.count()):
            self.listWidget.item(i).setForeground(QColor("black"))

    def get_names(self):
        self.x_items.clear()
        self.y1_items.clear()
        self.y2_items.clear()

        green = QColor("green")
        for i in range(self.listWidget.count()):
            if self.listWidget.item(i).foreground().color() == green:
                self.x_items.append(self.listWidget.item(i).text())

        for i in range(self.listWidget_3.count()):
            if self.listWidget_3.item(i).foreground().color() == green:
                self.y1_items.append(self.listWidget_3.item(i).text())

        for i in range(self.listWidget_4.count()):
            if self.listWidget_4.item(i).foreground().color() == green:
                self.y2_items.append(self.listWidget_4.item(i).text())



