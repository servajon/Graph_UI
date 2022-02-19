from PyQt5 import QtWidgets
from PyQt5.QtCore import pyqtSignal, QEvent
from PyQt5.QtWidgets import QInputDialog, QLineEdit

from Resources_file import Resources


class TabWidget(QtWidgets.QTabWidget):
    name_changed_tab = pyqtSignal(str)
    break_tab = pyqtSignal(int)
    change_current = pyqtSignal(int)

    def __init__(self, parent=None):
        super().__init__(parent)
        self.setAcceptDrops(True)
        self.tabBar = self.tabBar()
        self.tabBar.setMouseTracking(True)
        self.setMovable(True)
        self.setAcceptDrops(True)

        self.tabBarDoubleClicked.connect(self.db_clique_bar)
        self.currentChanged.connect(self.onChange)
        self.tabBar.installEventFilter(self)

        self.start_drag_y = None

    def eventFilter(self, obj, event):
        if event.type() == QEvent.HoverMove:  # Catch the TouchBegin event.
            self.hoverMove(event)

        if event.type() == QEvent.MouseButtonPress:  # Catch the TouchBegin event.
            self.mousePressEvent(event)

        if event.type() == QEvent.MouseButtonRelease:  # Catch the TouchBegin event.
            self.mouseReleaseEvent(event)

        return super(TabWidget, self).eventFilter(obj, event)

    def db_clique_bar(self, event):
        name = QInputDialog.getText(self, "Name change", "New name ?", QLineEdit.Normal)
        if name[1] and name[0] != '':
            old_name = self.tabText(self.currentIndex())
            names = []
            for i in range(0, self.count()):
                if i != self.currentIndex():
                    names.append(self.tabText(i))

            new_name = Resources.unique_name(names, name[0])
            self.setTabText(self.currentIndex(), new_name)
            self.name_changed_tab.emit(old_name)

    def mousePressEvent(self, event):
        self.start_drag_y = event.y()

    def mouseReleaseEvent(self, event):
        self.start_drag_y = None

    def hoverMove(self, event):
        if self.start_drag_y is None:
            return
        sub = event.pos().y() - self.start_drag_y
        if sub > 50:
            self.break_tab.emit(self.currentIndex())
            self.removeTab(self.currentIndex())
            self.start_drag_y = None

    def onChange(self, event):
        self.change_current.emit(event)