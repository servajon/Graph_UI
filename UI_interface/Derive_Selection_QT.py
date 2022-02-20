from PyQt5 import QtCore, QtGui, QtWidgets
from PyQt5.QtCore import pyqtSignal

from Resources_file.Emit import Emit
from UI_interface.Line_edit_QT import Line_edit_int


class Derive_Selection(QtWidgets.QWidget):
    finish_signal = pyqtSignal(str)

    def __init__(self, parent):
        super().__init__(parent)
        self.setWindowFlags(QtCore.Qt.Dialog | QtCore.Qt.WindowCloseButtonHint)

        self.emit = Emit()
        self.nb_point = None
        self.window_length = None
        self.polyorder = None

        self.setupUi(self)

    def setupUi(self, Dialog):
        Dialog.setObjectName("Dialog")
        Dialog.resize(262, 218)
        Dialog.setMinimumSize(QtCore.QSize(262, 218))
        Dialog.setMaximumSize(QtCore.QSize(262, 218))
        self.verticalLayout_2 = QtWidgets.QVBoxLayout(Dialog)
        self.verticalLayout_2.setObjectName("verticalLayout_2")
        self.verticalLayout = QtWidgets.QVBoxLayout()
        self.verticalLayout.setObjectName("verticalLayout")
        self.label_4 = QtWidgets.QLabel(Dialog)
        self.label_4.setMaximumSize(QtCore.QSize(242, 19))
        self.label_4.setObjectName("label_4")
        self.verticalLayout.addWidget(self.label_4)
        self.line = QtWidgets.QFrame(Dialog)
        self.line.setFrameShape(QtWidgets.QFrame.HLine)
        self.line.setFrameShadow(QtWidgets.QFrame.Sunken)
        self.line.setObjectName("line")
        self.verticalLayout.addWidget(self.line)
        self.checkBox = QtWidgets.QCheckBox(Dialog)
        self.checkBox.setObjectName("checkBox")
        self.verticalLayout.addWidget(self.checkBox)
        self.horizontalLayout = QtWidgets.QHBoxLayout()
        self.horizontalLayout.setObjectName("horizontalLayout")
        self.label = QtWidgets.QLabel(Dialog)
        self.label.setMinimumSize(QtCore.QSize(168, 0))
        self.label.setObjectName("label")
        self.horizontalLayout.addWidget(self.label)
        spacerItem = QtWidgets.QSpacerItem(40, 20, QtWidgets.QSizePolicy.Expanding, QtWidgets.QSizePolicy.Minimum)
        self.horizontalLayout.addItem(spacerItem)
        self.lineEdit = Line_edit_int(Dialog)
        self.lineEdit.setMaximumSize(QtCore.QSize(54, 20))
        self.lineEdit.setObjectName("lineEdit")
        self.horizontalLayout.addWidget(self.lineEdit)
        spacerItem1 = QtWidgets.QSpacerItem(40, 20, QtWidgets.QSizePolicy.Expanding, QtWidgets.QSizePolicy.Minimum)
        self.horizontalLayout.addItem(spacerItem1)
        self.verticalLayout.addLayout(self.horizontalLayout)
        self.line_2 = QtWidgets.QFrame(Dialog)
        self.line_2.setFrameShape(QtWidgets.QFrame.HLine)
        self.line_2.setFrameShadow(QtWidgets.QFrame.Sunken)
        self.line_2.setObjectName("line_2")
        self.verticalLayout.addWidget(self.line_2)
        self.checkBox_2 = QtWidgets.QCheckBox(Dialog)
        self.checkBox_2.setObjectName("checkBox_2")
        self.verticalLayout.addWidget(self.checkBox_2)
        self.horizontalLayout_2 = QtWidgets.QHBoxLayout()
        self.horizontalLayout_2.setObjectName("horizontalLayout_2")
        self.label_2 = QtWidgets.QLabel(Dialog)
        self.label_2.setMinimumSize(QtCore.QSize(168, 0))
        self.label_2.setObjectName("label_2")
        self.horizontalLayout_2.addWidget(self.label_2)
        spacerItem2 = QtWidgets.QSpacerItem(40, 20, QtWidgets.QSizePolicy.Expanding, QtWidgets.QSizePolicy.Minimum)
        self.horizontalLayout_2.addItem(spacerItem2)
        self.lineEdit_2 = Line_edit_int(Dialog)
        self.lineEdit_2.setMinimumSize(QtCore.QSize(0, 0))
        self.lineEdit_2.setMaximumSize(QtCore.QSize(54, 20))
        self.lineEdit_2.setObjectName("lineEdit_2")
        self.horizontalLayout_2.addWidget(self.lineEdit_2)
        spacerItem3 = QtWidgets.QSpacerItem(40, 20, QtWidgets.QSizePolicy.Expanding, QtWidgets.QSizePolicy.Minimum)
        self.horizontalLayout_2.addItem(spacerItem3)
        self.verticalLayout.addLayout(self.horizontalLayout_2)
        self.horizontalLayout_3 = QtWidgets.QHBoxLayout()
        self.horizontalLayout_3.setObjectName("horizontalLayout_3")
        self.label_3 = QtWidgets.QLabel(Dialog)
        self.label_3.setMinimumSize(QtCore.QSize(168, 0))
        self.label_3.setObjectName("label_3")
        self.horizontalLayout_3.addWidget(self.label_3)
        spacerItem4 = QtWidgets.QSpacerItem(40, 20, QtWidgets.QSizePolicy.Expanding, QtWidgets.QSizePolicy.Minimum)
        self.horizontalLayout_3.addItem(spacerItem4)
        self.lineEdit_3 = Line_edit_int(Dialog)
        self.lineEdit_3.setMaximumSize(QtCore.QSize(54, 20))
        self.lineEdit_3.setObjectName("lineEdit_3")
        self.horizontalLayout_3.addWidget(self.lineEdit_3)
        spacerItem5 = QtWidgets.QSpacerItem(40, 20, QtWidgets.QSizePolicy.Expanding, QtWidgets.QSizePolicy.Minimum)
        self.horizontalLayout_3.addItem(spacerItem5)
        self.verticalLayout.addLayout(self.horizontalLayout_3)
        self.horizontalLayout_4 = QtWidgets.QHBoxLayout()
        self.horizontalLayout_4.setObjectName("horizontalLayout_4")
        self.pushButton = QtWidgets.QPushButton(Dialog)
        self.pushButton.setObjectName("pushButton")
        self.horizontalLayout_4.addWidget(self.pushButton)
        spacerItem6 = QtWidgets.QSpacerItem(40, 20, QtWidgets.QSizePolicy.Expanding, QtWidgets.QSizePolicy.Minimum)
        self.horizontalLayout_4.addItem(spacerItem6)
        self.pushButton_2 = QtWidgets.QPushButton(Dialog)
        self.pushButton_2.setObjectName("pushButton_2")
        self.horizontalLayout_4.addWidget(self.pushButton_2)
        self.verticalLayout.addLayout(self.horizontalLayout_4)
        self.verticalLayout_2.addLayout(self.verticalLayout)

        self.retranslateUi(Dialog)
        QtCore.QMetaObject.connectSlotsByName(Dialog)

        self.checkBox.clicked.connect(self.click_radio)
        self.checkBox_2.clicked.connect(self.click_radio)

        self.pushButton.clicked.connect(self.save)
        self.pushButton_2.clicked.connect(self.cancel)

        self.set_visibility_horizontalLayout(False)
        self.set_visibility_horizontalLayout_2_3(False)

    def retranslateUi(self, Dialog):
        _translate = QtCore.QCoreApplication.translate
        Dialog.setWindowTitle(_translate("Dialog", "Dialog"))
        self.label_4.setText(_translate("Dialog", "<html><head/><body><p><span style=\" font-size:12pt;\">Derive</span></p></body></html>"))
        self.checkBox.setText(_translate("Dialog", "Number Point Selection"))
        self.label.setText(_translate("Dialog", "Number of points for the derivate :"))
        self.checkBox_2.setText(_translate("Dialog", "savgol filter"))
        self.label_2.setText(_translate("Dialog", "window_length :"))
        self.label_3.setText(_translate("Dialog", "polyorder :"))
        self.pushButton.setText(_translate("Dialog", "Save"))
        self.pushButton_2.setText(_translate("Dialog", "Cancel"))

    def set_visibility_horizontalLayout(self, bool):
        self.label.setVisible(bool)
        self.lineEdit.setVisible(bool)
        self.label_4.setMaximumSize(QtCore.QSize(242, 19))

    def set_visibility_horizontalLayout_2_3(self, bool):
        self.label_2.setVisible(bool)
        self.lineEdit_2.setVisible(bool)
        self.label_3.setVisible(bool)
        self.lineEdit_3.setVisible(bool)
        self.label_4.setMaximumSize(QtCore.QSize(242, 19))

    def save(self):
        if self.checkBox.isChecked():
            try:
                self.nb_point = self.lineEdit.get_value()
            except ValueError:
                self.emit.emit("msg_console", type="msg_console", str="Empty selection",
                               foreground_color="red")
                return

        if self.checkBox_2.isChecked():
            try:
                self.window_length = self.lineEdit_2.get_value()
                self.polyorder = self.lineEdit_3.get_value()
            except ValueError:
                self.emit.emit("msg_console", type="msg_console", str="Empty selection",
                               foreground_color="red")
                return

        self.finish_signal.emit("save")

    def cancel(self):
        self.finish_signal.emit("cancel")

    def closeEvent(self, a0):
        self.finish_signal.emit("cancel")

    def click_radio(self):
        if self.checkBox.isChecked():
            self.set_visibility_horizontalLayout(True)
        else:
            self.set_visibility_horizontalLayout(False)

        if self.checkBox_2.isChecked():
            self.set_visibility_horizontalLayout_2_3(True)
        else:
            self.set_visibility_horizontalLayout_2_3(False)
