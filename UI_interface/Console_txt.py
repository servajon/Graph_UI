from PyQt5.QtCore import pyqtSignal
from qtpy.QtCore import Qt
from PyQt5.QtGui import QTextCursor, QFont
from pyqtconsole.console import BaseConsole


class Console_txt(BaseConsole):
    _input = pyqtSignal(str)

    def __init__(self, parent=None):
        super().__init__(parent)
        self.setFont(QFont("Times", 13))

    def _show_ps(self):
        """
        On override cette methode pour ne pas avoir les tabs sur la gauche

        :return: None
        """
        pass

    def _handle_enter_key(self, event):
        if event.modifiers() & Qt.ShiftModifier:
            self.insert_input_text('<br>')
        else:
            cursor = self._textCursor()
            cursor.movePosition(QTextCursor.End)
            self._setTextCursor(cursor)
            buffer = self.input_buffer()
            self.insert_input_text('<br>', show_ps=False)

            self._last_input = buffer

            self.command_history.add(buffer)
            self._last_input = buffer
            self._update_ps(self._more)
            self._update_prompt_pos()

            self._input.emit(buffer)
        return True

    def insert_input_text(self, text, show_ps=True):
        """Insert text into input buffer."""

        self._keep_cursor_in_buffer()
        self.ensureCursorVisible()
        self._remove_selected_input(self._textCursor())

        if text == ' ':
            self._textCursor().insertHtml('<div style=color:black>&nbsp;</div>')
        else:
            self._textCursor().insertHtml('<div style=color:black>' + text + '</div>')

        if show_ps and '\n' in text:
            self._update_ps(True)
            for _ in range(text.count('\n')):
                # NOTE: need to insert in two steps, because this internally
                # uses setAlignment, which affects only the first line:
                self._insert_prompt_text('\n')
                self._insert_prompt_text(self._ps)
        elif '\n' in text:
            self._insert_prompt_text('\n' * text.count('\n'))

    def update_prompt_pos(self):
        self._update_prompt_pos()




