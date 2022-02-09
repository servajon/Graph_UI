import sys
import matplotlib
from PyQt5 import QtCore, QtGui, QtWidgets
from PyQt5.QtCore import QThread, pyqtSlot, pyqtSignal
from PyQt5.QtWidgets import (
    QApplication, QDialog, QMainWindow, QMessageBox, QFileDialog, QWidget, QLineEdit, QVBoxLayout, QInputDialog,
    QTreeWidgetItem
)
from matplotlib.backends.backend_qt import NavigationToolbar2QT
from matplotlib.backends.backend_qt5agg import FigureCanvasQTAgg as FigureCanvas
import matplotlib.pyplot as pplot

from Console_Objets.Affiche_objet import Classique_affiche
from Console_Objets.Console import Console
from Console_Objets.Data_array import Data_array
from Console_Objets.Figure import Figure
from Data_type.CCCV_data import CCCV_data
from Resources import Resources
from UI_interface import Threads_UI
from UI_interface.Main_window_QT import Ui_MainWindow

"""----------------------------------------------------------------------------------"""
"""                                   Main window                                    """
"""----------------------------------------------------------------------------------"""


class Figure_plot(QWidget):
    def __init__(self, abstract_affiche):
        super().__init__()
        self.canvas = None
        self.toolbar = None

        self.fig = None
        self.ax1 = None
        self.ax2 = None
        self.value = None
        self.freq = None
        self.leg1 = None

        """abstract_affiche"""
        self.abstract_affiche = abstract_affiche
        """création du canvas + widget matplotlib"""
        self.create_plot()

    def create_plot(self):
        self.fig, self.ax1, self.ax2, self.value, self.freq, self.leg1 = \
            self.abstract_affiche.data.load_graph(self.abstract_affiche.figure)

        layout = QVBoxLayout()
        self.setLayout(layout)
        self.canvas = FigureCanvas(self.fig)
        self.toolbar = NavigationToolbar2QT(self.canvas, self, True)

        for artist in self.fig.get_children():
            if type(artist).__name__ == "Text":
                artist.set_picker(True)

        layout.addWidget(self.canvas)
        layout.addWidget(self.toolbar)

        """connections"""
        self.canvas.mpl_connect('button_press_event', self.button_press_event)
        self.canvas.mpl_connect('motion_notify_event', self.mouseMoveEvent)
        self.canvas.mpl_connect('close_event', self.closeEvent)
        self.canvas.mpl_connect('axes_enter_event', self.axes_enter_event)
        self.canvas.mpl_connect('axes_leave_event', self.axes_leave_event)
        self.canvas.mpl_connect('pick_event', self.pick_event)

        self.canvas.draw()

    def button_press_event(self, event):
        if event.dblclick:
            self.mouseDoubleClickEvent(event)
        else:
            pass

    def mouseDoubleClickEvent(self, event):
        """ajouter ces methode à l'ojjet self.abstract_affiche
        pour que chaque type fasse ses traitements"""
        if event.inaxes is not None and event.inaxes == self.ax1:
            black = matplotlib.colors.to_rgba("black")
            event.inaxes.axhline(y=event.ydata, color=black)
            event.inaxes.axvline(x=event.xdata, color=black)
            self.canvas.draw()

    def mouseMoveEvent(self, event):
        pass

    def closeEvent(self, event):
        pass

    def axes_enter_event(self, event):
        pass

    def axes_leave_event(self, event):
        pass

    def pick_event(self, event):
        print(event.artist)
        print(event.guiEvent)


class Tab(QWidget):
    def __init__(self):
        QWidget.__init__(self)


class TabWidget(QtWidgets.QTabWidget):
    name_changed = pyqtSignal(str)

    def __init__(self, parent=None):
        super().__init__(parent)
        self.tabBarDoubleClicked.connect(self.clique_bar)

    def clique_bar(self):
        name = QInputDialog.getText(self, "Name change", "New name ?", QLineEdit.Normal)
        if name[1] and name[0] != '':
            old_name = self.tabText(self.currentIndex())
            names = []
            for i in range(0, self.count()):
                if i != self.currentIndex():
                    names.append(self.tabText(i))

            new_name = Resources.unique_name(names, name[0])
            self.setTabText(self.currentIndex(), new_name)
            self.name_changed.emit(old_name)

    def mouseDoubleClickEvent(self, event):
        print("Mouse Double Click Event")


class Window(QMainWindow, Ui_MainWindow):
    def __init__(self, parent=None):
        super().__init__(parent)
        self.setupUi(self)

        self.console = Console()
        """self.threads est de la forme : [thread, worker]"""
        self.threads = []
        self.connectSignalsSlots()

        """self.tabWidget.objectNameChanged.connect(self.name_changed)
        self.tabWidget.tabCloseRequested.connect(self.close_tab_handler)"""

        self.treeWidget.itemSelectionChanged.connect(self.tree_select_change)

        """objet qui sauvegarde le dernier état de QFileDialog pour la sauvegarde"""
        self.save_state_dialog = None

    def connectSignalsSlots(self):
        self.actioncccv.triggered.connect(self.open_cccv)
        self.actioncv.triggered.connect(self.open_cv)
        self.actiongitt.triggered.connect(self.open_gitt)

    def open_cccv(self):
        """création de l'objet QFileDialog"""
        dialog = QFileDialog()
        """si il y a une sauvegarde d'état elle est utilisée"""
        if self.save_state_dialog is not None:
            dialog.restoreState(self.save_state_dialog)

        dialog.setWindowTitle('Open cccv File')
        dialog.setNameFilter('EC_lab file (*.mpt *.txt)')
        dialog.setFileMode(QFileDialog.ExistingFile)

        if dialog.exec_() == QDialog.Accepted:
            filename = dialog.selectedFiles()[0]
            filename = r"C:\Users\Maxime\Desktop\fichier_test/test.txt"

            """création d'un nouveau thread"""
            t = QThread()
            """création du worker"""
            worker = Threads_UI.Open_file_cccv(filename)
            worker.moveToThread(t)
            """connection"""
            t.started.connect(worker.run)
            worker.finished.connect(self.fin_thread_lecture)

            self.threads.append([t, worker])
            t.start()

        self.save_state_dialog = dialog.saveState()

    def open_cv(self):
        fig = Figure("test", 1)
        fig.add_data_x_Data(Data_array([1, 2, 3], None, None, "None"))
        fig.add_data_y1_Data(Data_array([10, 5, 20], None, None, "None"))

        obj = Classique_affiche(self.console.current_data, fig)

        self.figure_plot = Figure_plot(obj)
        self.figure_plot.show()

    def open_gitt(self):
        self.console.get_info_data_all()
        self.add_data_tree("figure", "test")

    def fichier_invalide_error(self):
        msgBox = QMessageBox()
        msgBox.setIcon(QMessageBox.Warning)
        msgBox.setText("File type invalid")
        msgBox.setWindowTitle("Error")
        msgBox.setStandardButtons(QMessageBox.Ok)
        msgBox.exec()

    def fait(self):
        msgBox = QMessageBox()
        msgBox.setIcon(QMessageBox.Ok)
        msgBox.setText("Done")
        msgBox.setWindowTitle("Done")
        msgBox.setStandardButtons(QMessageBox.Ok)
        msgBox.exec()

    def fin_thread_lecture(self):
        index = 0
        while index < len(self.threads):
            if self.threads[index][1].finish:
                if self.threads[index][1].data is None:
                    self.fichier_invalide_error()
                else:
                    if type(self.threads[index][1]).__name__ == "Open_file_cccv":
                        obj_data = CCCV_data()
                        obj_data.data = self.threads[index][1].data
                        obj_data.name = obj_data.data["name"]

                        self.console.add_data(obj_data)

                        name_tab = obj_data.name
                        self.add_data_tree("cccv", name_tab)

                self.threads[index][0].terminate()
                del self.threads[index]
            else:
                index += 1

    def creation_tab(self, name):
        _translate = QtCore.QCoreApplication.translate
        new_tab = Tab()
        new_tab.setObjectName(name)
        self.tabWidget.addTab(new_tab, "")
        self.tabWidget.setTabText(self.tabWidget.indexOf(new_tab), _translate("MainWindow", name))

    def add_data_tree(self, type, name):
        if type == "figure":
            for itm in self.tree_items:
                for i, child_item in enumerate(itm):
                    if child_item.isSelected():
                        child = QTreeWidgetItem([name, type])
                        child.setSelected(True)
                        itm[0].insertChild(i, child)
                        itm.append(child)
                        break
        else:
            item = QTreeWidgetItem([name, type])
            self.treeWidget.insertTopLevelItem(len(self.tree_items), item)
            self.tree_items.append([item])
            for itm in self.tree_items:
                for child in itm:
                    child.setSelected(False)
            item.setSelected(True)

    def name_changed(self, signal):
        for data in self.console.datas:
            if data.name == signal:
                name = self.tabWidget.tabText(self.tabWidget.currentIndex())
                data.name = name
                break

    def close_tab_handler(self, index):
        name = self.tabWidget.tabText(index)
        for i, data in enumerate(self.console.datas):
            if data.name == name:
                del self.console.datas[i]
                break
        self.tabWidget.removeTab(index)

    def tree_select_change(self):
        _translate = QtCore.QCoreApplication.translate
        if len(self.treeWidget.selectedItems()):
            if self.treeWidget.selectedItems()[0].text(1) == "figure":
                self.label_5.setText(_translate("MainWindow", "<html><head/><body><p><span style="
                                                              "\" font-size:11pt;\">Current plot : " +
                                                self.treeWidget.selectedItems()[0].text(0) +
                                                "</span></p></body></html>"))
                parent = self.treeWidget.selectedItems()[0].parent()
                self.label.setText(_translate("MainWindow", "<html><head/><body><p><span style=\" font-size:11pt;\">"
                                                            "Current data : "
                                              + parent.text(0) +" </span></p></body></html>"))
                self.update_current_data(parent.text(0))
            else:
                self.label.setText(_translate("MainWindow", "<html><head/><body><p><span style=\" font-size:11pt;\">"
                                                            "Current data : " + self.treeWidget.selectedItems()[0].text(0) +
                                              " </span></p></body></html>"))
                self.label_5.setText(_translate("MainWindow", "<html><head/><body><p><span style=\" font-size:11pt;\">"
                                                            "Current plot : None""</span></p></body></html>"))
                self.update_current_data(self.treeWidget.selectedItems()[0].text(0))

            print(self.console.current_data.name)
            try:
                print(self.console.current_data.current_figure.name)
            except AttributeError:
                pass

    def update_current_data(self, name):
        found = False
        for data in self.console.datas:
            if data.name == name:
                self.console.current_data = data
                found = True
                break
        if not found:
            raise ValueError

class Main_interface:
    def __init__(self):
        app = QApplication(sys.argv)
        win = Window()
        win.show()
        sys.exit(app.exec())
