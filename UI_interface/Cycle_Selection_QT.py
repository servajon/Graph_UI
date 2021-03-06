from PyQt5 import QtWidgets, QtCore
from PyQt5.QtCore import pyqtSignal
from PyQt5.QtGui import QKeyEvent
from PyQt5.QtWidgets import QWidget

from Resources_file.Emit import Emit


class Cycle_Selection(QWidget):

    finish_signal = pyqtSignal(str)

    def __init__(self, parent):
        super().__init__(parent)
        self.setWindowFlags(QtCore.Qt.Dialog | QtCore.Qt.WindowCloseButtonHint)

        self.setWindowModality(QtCore.Qt.ApplicationModal)

        self.cycles = None
        self.emit = Emit()

        self.setupUi(self)


    """----------------------------------------------------------------------------------"""

    def setupUi(self, Dialog):
        Dialog.setObjectName("Dialog")
        Dialog.resize(236, 184)

        self.setMinimumSize(285, 0)

        self.verticalLayout_2 = QtWidgets.QVBoxLayout(Dialog)
        self.verticalLayout_2.setObjectName("verticalLayout_2")
        self.verticalLayout = QtWidgets.QVBoxLayout()
        self.verticalLayout.setObjectName("verticalLayout")
        self.label = QtWidgets.QLabel(Dialog)
        self.label.setMaximumSize(QtCore.QSize(16777215, 25))
        self.label.setObjectName("label")
        self.verticalLayout.addWidget(self.label)
        self.line = QtWidgets.QFrame(Dialog)
        self.line.setFrameShape(QtWidgets.QFrame.HLine)
        self.line.setFrameShadow(QtWidgets.QFrame.Sunken)
        self.line.setObjectName("line")
        self.verticalLayout.addWidget(self.line)
        self.radioButton = QtWidgets.QRadioButton(Dialog)
        self.radioButton.setObjectName("radioButton")
        self.verticalLayout.addWidget(self.radioButton)
        self.radioButton_2 = QtWidgets.QRadioButton(Dialog)
        self.radioButton_2.setObjectName("radioButton_2")
        self.verticalLayout.addWidget(self.radioButton_2)
        self.radioButton_3 = QtWidgets.QRadioButton(Dialog)
        self.radioButton_3.setObjectName("radioButton_3")
        self.verticalLayout.addWidget(self.radioButton_3)
        self.verticalLayout_2.addLayout(self.verticalLayout)

        self.cycle_to_layout = None
        self.cycle_numbers_layout = None
        self.cycle_all_layout = None

        self.horizontalLayout_3 = QtWidgets.QHBoxLayout()
        self.horizontalLayout_3.setObjectName("horizontalLayout_3")
        self.pushButton = QtWidgets.QPushButton(Dialog)
        self.pushButton.setObjectName("pushButton")
        self.horizontalLayout_3.addWidget(self.pushButton)
        spacerItem4 = QtWidgets.QSpacerItem(40, 20, QtWidgets.QSizePolicy.Expanding, QtWidgets.QSizePolicy.Minimum)
        self.horizontalLayout_3.addItem(spacerItem4)
        self.pushButton_2 = QtWidgets.QPushButton(Dialog)
        self.pushButton_2.setObjectName("pushButton_2")
        self.horizontalLayout_3.addWidget(self.pushButton_2)
        self.verticalLayout_2.addLayout(self.horizontalLayout_3)

        self.retranslateUi(Dialog)
        QtCore.QMetaObject.connectSlotsByName(Dialog)

        self.radioButton.clicked.connect(self.click_radio)
        self.radioButton_2.clicked.connect(self.click_radio)
        self.radioButton_3.clicked.connect(self.click_radio)

        self.radioButton.setChecked(True)
        self.create_cycle_all_layout()

        self.pushButton.clicked.connect(self.save)
        self.pushButton_2.clicked.connect(self.cancel)

    """----------------------------------------------------------------------------------"""

    def retranslateUi(self, Dialog):
        _translate = QtCore.QCoreApplication.translate
        Dialog.setWindowTitle(_translate("Dialog", "Select Cycles"))
        self.label.setText(_translate("Dialog",
                                      "<html><head/><body><p><span style=\" font-size:12pt;\">Cycle Selection</span></p></body></html>"))
        self.radioButton.setText(_translate("Dialog", "All"))
        self.radioButton_2.setText(_translate("Dialog", "Manual s??lection"))
        self.radioButton_3.setText(_translate("Dialog", "Range"))

        self.pushButton.setText(_translate("Dialog", "Save"))
        self.pushButton_2.setText(_translate("Dialog", "Cancel"))

    """----------------------------------------------------------------------------------"""

    def click_radio(self):
        if self.radioButton.isChecked():
            if self.cycle_numbers_layout is not None:
                self.delete_cycle_numbers_layout()
            elif self.cycle_to_layout is not None:
                self.delete_cycle_to_layout()

            if self.cycle_all_layout is None:
                self.create_cycle_all_layout()
                self.update()

        elif self.radioButton_2.isChecked():
            if self.cycle_all_layout is not None:
                self.delete_cycle_all_layout()
            elif self.cycle_to_layout is not None:
                self.delete_cycle_to_layout()

            if self.cycle_numbers_layout is None:
                self.create_cycle_numbers_layout()
                self.update()

        else:
            if self.cycle_all_layout is not None:
                self.delete_cycle_all_layout()
            elif self.cycle_numbers_layout is not None:
                self.delete_cycle_numbers_layout()

            if self.cycle_to_layout is None:
                self.create_cycle_to_layout()
                self.update()

    """----------------------------------------------------------------------------------"""

    def create_cycle_to_layout(self):
        self.cycle_to_layout = QtWidgets.QHBoxLayout()
        self.cycle_to_layout.setObjectName("horizontalLayout_2")
        self.label_3 = QtWidgets.QLabel(self)
        self.label_3.setObjectName("label_3")
        self.cycle_to_layout.addWidget(self.label_3)

        spacerItem1 = QtWidgets.QSpacerItem(40, 20, QtWidgets.QSizePolicy.Expanding, QtWidgets.QSizePolicy.Minimum)
        self.cycle_to_layout.addItem(spacerItem1)

        self.lineEdit_2 = Line_edit(self)
        self.lineEdit_2.setMaximumSize(QtCore.QSize(30, 16777215))
        self.lineEdit_2.setObjectName("lineEdit_2")
        self.cycle_to_layout.addWidget(self.lineEdit_2)

        self.label_4 = QtWidgets.QLabel(self)
        self.label_4.setObjectName("label_4")
        self.cycle_to_layout.addWidget(self.label_4)

        self.lineEdit_3 = Line_edit(self)
        self.lineEdit_3.setMaximumSize(QtCore.QSize(30, 16777215))
        self.lineEdit_3.setObjectName("lineEdit_3")
        self.cycle_to_layout.addWidget(self.lineEdit_3)
        spacerItem2 = QtWidgets.QSpacerItem(40, 20, QtWidgets.QSizePolicy.Expanding, QtWidgets.QSizePolicy.Minimum)
        self.cycle_to_layout.addItem(spacerItem2)
        self.verticalLayout_2.insertLayout(1, self.cycle_to_layout)
        _translate = QtCore.QCoreApplication.translate
        self.label_3.setText(_translate("Dialog",
                                        "<html><head/><body><p><span style=\" font-size:12pt;\">Cycle numbers :"
                                        "</span></p></body></html>"))
        self.label_4.setText(
            _translate("Dialog", "<html><head/><body><p><span style=\" font-size:12pt;\">to</span></p></body></html>"))

    """----------------------------------------------------------------------------------"""

    def delete_cycle_to_layout(self):
        self.lineEdit_3.deleteLater()
        self.label_4.deleteLater()
        self.lineEdit_2.deleteLater()
        self.label_3.deleteLater()
        self.cycle_to_layout.deleteLater()
        self.cycle_to_layout = None

    """----------------------------------------------------------------------------------"""

    def create_cycle_numbers_layout(self):
        self.cycle_numbers_layout = QtWidgets.QHBoxLayout()
        self.cycle_numbers_layout.setObjectName("cycle_numbers_layout")
        self.label_8 = QtWidgets.QLabel(self)
        self.label_8.setObjectName("label_8")
        self.cycle_numbers_layout.addWidget(self.label_8)

        spacerItem3 = QtWidgets.QSpacerItem(10, 20, QtWidgets.QSizePolicy.Expanding, QtWidgets.QSizePolicy.Minimum)
        self.cycle_numbers_layout.addItem(spacerItem3)

        self.lineEdit_5 = Line_edit(self)
        self.lineEdit_5.setMaximumSize(QtCore.QSize(16777215, 16777215))
        self.lineEdit_5.setObjectName("lineEdit_2")
        self.cycle_numbers_layout.addWidget(self.lineEdit_5)

        self.verticalLayout_2.insertLayout(1, self.cycle_numbers_layout)

        _translate = QtCore.QCoreApplication.translate
        self.label_8.setText(_translate("Dialog",
                                        "<html><head/><body><p><span style=\" font-size:12pt;\">Cycle numbers :"
                                        "</span></p></body></html>"))

    """----------------------------------------------------------------------------------"""

    def delete_cycle_numbers_layout(self):
        self.lineEdit_5.deleteLater()
        self.label_8.deleteLater()
        self.cycle_numbers_layout.deleteLater()
        self.cycle_numbers_layout = None

    """----------------------------------------------------------------------------------"""

    def create_cycle_all_layout(self):
        self.cycle_all_layout = QtWidgets.QHBoxLayout()
        self.cycle_all_layout.setObjectName("cycle_all_layout")
        self.label_5 = QtWidgets.QLabel(self)
        self.label_5.setObjectName("label_5")
        self.label_5.setMaximumSize(QtCore.QSize(16777215, 30))
        self.cycle_all_layout.addWidget(self.label_5)

        spacerItem3 = QtWidgets.QSpacerItem(46, 20, QtWidgets.QSizePolicy.Fixed, QtWidgets.QSizePolicy.Minimum)
        self.cycle_all_layout.addItem(spacerItem3)

        self.label_6 = QtWidgets.QLabel(self)
        self.label_6.setObjectName("label_6")
        self.label_6.setMaximumSize(QtCore.QSize(30, 20))
        self.cycle_all_layout.addWidget(self.label_6)

        spacerItem3 = QtWidgets.QSpacerItem(10, 20, QtWidgets.QSizePolicy.Expanding, QtWidgets.QSizePolicy.Minimum)
        self.cycle_all_layout.addItem(spacerItem3)

        self.verticalLayout_2.insertLayout(1, self.cycle_all_layout)
        _translate = QtCore.QCoreApplication.translate
        self.label_5.setText(_translate("Dialog",
                                        "<html><head/><body><p><span style=\" font-size:12pt;\">Cycle numbers :"
                                        "</span></p></body></html>"))

        self.label_6.setText(_translate("Dialog",
                                        "<html><head/><body><p><span style=\" font-size:12pt;\">all"
                                        "</span></p></body></html>"))

    """----------------------------------------------------------------------------------"""

    def delete_cycle_all_layout(self):
        self.label_5.deleteLater()
        self.label_6.deleteLater()
        self.cycle_all_layout.deleteLater()
        self.cycle_all_layout = None

    """----------------------------------------------------------------------------------"""

    def save(self):
        """
        Fonction qui emit le r??sultat de la fen??tre
        Le signal est de la forme :

        rep : save / cancel
        arg : all / to / selected
        cycle : array_cycle / None

        :return: None
        """
        if self.cycle_to_layout is not None:
            if self.lineEdit_2.text() == "" or self.lineEdit_3.text() == "":
                self.emit.emit("msg_console", type="msg_console", str="Empty selection",
                               foreground_color="red")
                return
            elif int(self.lineEdit_2.text()) > int(self.lineEdit_3.text()):
                self.emit.emit("msg_console", type="msg_console", str="Left number is largeur than the right one",
                               foreground_color="red")
                return

            else:
                self.cycles = [int(self.lineEdit_2.text()), "to", int(self.lineEdit_3.text())]


        elif self.cycle_numbers_layout is not None:
            s = self.lineEdit_5.text()
            if s == "":
                self.emit.emit("msg_console", type="msg_console", str="Selection empty",
                               foreground_color="red")
                return

            temp = s.split(" ")
            array = []
            for data in temp:
                data = int(data)
                if data not in array:
                    array.append(data)

            array.sort()
            self.cycles = array

        else:
            self.cycles = None

        self.finish_signal.emit("save")

    """----------------------------------------------------------------------------------"""

    def cancel(self):
        self.finish_signal.emit("cancel")

    """----------------------------------------------------------------------------------"""

    def closeEvent(self, event):
        self.finish_signal.emit("cancel")

    """----------------------------------------------------------------------------------"""

    def focusOutEvent(self, a0):
        print(a0)
        self.activateWindow()


class Line_edit(QtWidgets.QLineEdit):
    _KEYS_STR = ["0", "1", "2", "3", "4", "5", "5", "6", "7", "8", "9", " "]

    def __init__(self, parent=None):
        super().__init__(parent)

    def keyPressEvent(self, e: QKeyEvent):
        start_select = self.selectionStart()
        end_select = self.selectionEnd()

        if start_select == -1:
            if e.text() in self._KEYS_STR:
                if len(e.text()) == 0 or (e.text() == " " and self.text()[-1] == " "):
                    pass
                else:
                    self.setText(self.text() + e.text())
            elif e.key() == QtCore.Qt.Key.Key_Backspace:
                self.setText(self.text()[:-1])
        else:
            if e.text() in self._KEYS_STR and e.text() != " ":
                self.setText(self.text()[0:start_select] + e.text() + self.text()[end_select:])
            elif e.key() == QtCore.Qt.Key.Key_Backspace:
                self.setText(self.text()[0:start_select] + self.text()[end_select:])
