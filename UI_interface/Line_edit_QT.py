from PyQt5 import QtWidgets, QtCore
from PyQt5.QtGui import QKeyEvent



class Line_edit_float(QtWidgets.QLineEdit):
    _KEYS_STR = ["0", "1", "2", "3", "4", "5", "5", "6", "7", "8", "9", ".", ",", "-"]

    def __init__(self, parent=None):
        super().__init__(parent)

    def keyPressEvent(self, e: QKeyEvent):
        start_select = self.selectionStart()
        end_select = self.selectionEnd()

        if start_select == -1:
            if e.text() in self._KEYS_STR:
                self.setText(self.text() + e.text())

            elif e.key() == QtCore.Qt.Key.Key_Backspace:
                self.setText(self.text()[:-1])
        else:
            if e.text() in self._KEYS_STR:
                self.setText(self.text()[0:start_select] + e.text() + self.text()[end_select:])
            elif e.key() == QtCore.Qt.Key.Key_Backspace:
                self.setText(self.text()[0:start_select] + self.text()[end_select:])

    def get_value(self):
        return float(self.text().replace(",", "."))



class Line_edit_int(QtWidgets.QLineEdit):
    _KEYS_STR = ["0", "1", "2", "3", "4", "5", "5", "6", "7", "8", "9", "-"]

    def __init__(self, parent=None):
        super().__init__(parent)

    def keyPressEvent(self, e: QKeyEvent):
        start_select = self.selectionStart()
        end_select = self.selectionEnd()

        if start_select == -1:
            if e.text() in self._KEYS_STR:
                self.setText(self.text() + e.text())

            elif e.key() == QtCore.Qt.Key.Key_Backspace:
                self.setText(self.text()[:-1])
        else:
            if e.text() in self._KEYS_STR:
                self.setText(self.text()[0:start_select] + e.text() + self.text()[end_select:])
            elif e.key() == QtCore.Qt.Key.Key_Backspace:
                self.setText(self.text()[0:start_select] + self.text()[end_select:])

    def get_value(self):
        return int(self.text().replace(",", "."))


class Line_edit_str(QtWidgets.QLineEdit):

    def __init__(self, parent=None):
        super().__init__(parent)

    def keyPressEvent(self, e: QKeyEvent):
        start_select = self.selectionStart()
        end_select = self.selectionEnd()

        if start_select == -1:
            if e.key() == QtCore.Qt.Key.Key_Backspace:
                self.setText(self.text()[:-1])
            else:
                self.setText(self.text() + e.text())

        else:
            if e.key() == QtCore.Qt.Key.Key_Backspace:
                self.setText(self.text()[0:start_select] + self.text()[end_select:])
            else:
                self.setText(self.text()[0:start_select] + e.text() + self.text()[end_select:])


    def get_value(self):
        if self.text() == "":
            raise ValueError
        else:
            return self.text()