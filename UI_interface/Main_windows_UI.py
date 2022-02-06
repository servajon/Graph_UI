import sys
import matplotlib
from PyQt5 import QtCore, QtGui, QtWidgets
from PyQt5.QtCore import QThread, pyqtSlot, pyqtSignal
from PyQt5.QtWidgets import (
    QApplication, QDialog, QMainWindow, QMessageBox, QFileDialog, QWidget, QLineEdit, QVBoxLayout, QInputDialog
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


class Ui_MainWindow(object):
    def setupUi(self, MainWindow):
        MainWindow.setObjectName("MainWindow")
        MainWindow.resize(1159, 724)
        self.centralwidget = QtWidgets.QWidget(MainWindow)
        self.centralwidget.setObjectName("centralwidget")
        self.gridLayout = QtWidgets.QGridLayout(self.centralwidget)
        self.gridLayout.setObjectName("gridLayout")

        self.tabWidget = TabWidget(self.centralwidget)
        self.tabWidget.setObjectName("tabWidget")
        self.tabWidget.setTabsClosable(True)

        self.gridLayout.addWidget(self.tabWidget, 0, 0, 1, 1)
        MainWindow.setCentralWidget(self.centralwidget)
        self.menubar = QtWidgets.QMenuBar(MainWindow)
        self.menubar.setGeometry(QtCore.QRect(0, 0, 1159, 21))
        self.menubar.setObjectName("menubar")
        self.menuOpen = QtWidgets.QMenu(self.menubar)
        self.menuOpen.setObjectName("menuOpen")
        self.menuOpen_2 = QtWidgets.QMenu(self.menuOpen)
        self.menuOpen_2.setObjectName("menuOpen_2")
        self.menuModulo_bat = QtWidgets.QMenu(self.menuOpen_2)
        self.menuModulo_bat.setObjectName("menuModulo_bat")
        self.menuQuit = QtWidgets.QMenu(self.menubar)
        self.menuQuit.setObjectName("menuQuit")
        MainWindow.setMenuBar(self.menubar)
        self.statusbar = QtWidgets.QStatusBar(MainWindow)
        self.statusbar.setObjectName("statusbar")
        MainWindow.setStatusBar(self.statusbar)
        self.actioncccv = QtWidgets.QAction(MainWindow)
        self.actioncccv.setObjectName("actioncccv")
        self.actioncv = QtWidgets.QAction(MainWindow)
        self.actioncv.setObjectName("actioncv")
        self.actiondiffraction = QtWidgets.QAction(MainWindow)
        self.actiondiffraction.setObjectName("actiondiffraction")
        self.actionimp_dance = QtWidgets.QAction(MainWindow)
        self.actionimp_dance.setObjectName("actionimp_dance")
        self.actioncp = QtWidgets.QAction(MainWindow)
        self.actioncp.setObjectName("actioncp")
        self.actiongitt = QtWidgets.QAction(MainWindow)
        self.actiongitt.setObjectName("actiongitt")
        self.actionvieillissement = QtWidgets.QAction(MainWindow)
        self.actionvieillissement.setObjectName("actionvieillissement")
        self.menuModulo_bat.addAction(self.actionvieillissement)
        self.menuOpen_2.addAction(self.actioncccv)
        self.menuOpen_2.addAction(self.actioncv)
        self.menuOpen_2.addAction(self.actiondiffraction)
        self.menuOpen_2.addAction(self.actionimp_dance)
        self.menuOpen_2.addAction(self.actioncp)
        self.menuOpen_2.addAction(self.actiongitt)
        self.menuOpen_2.addAction(self.menuModulo_bat.menuAction())
        self.menuOpen.addAction(self.menuOpen_2.menuAction())
        self.menubar.addAction(self.menuOpen.menuAction())
        self.menubar.addAction(self.menuQuit.menuAction())

        self.tabs = []

        """self.tab = QtWidgets.QWidget()
        self.tab.setObjectName("tab")
        self.tabWidget.addTab(self.tab, "")
        """
        self.retranslateUi(MainWindow)
        self.tabWidget.setCurrentIndex(0)
        QtCore.QMetaObject.connectSlotsByName(MainWindow)

    def retranslateUi(self, MainWindow):
        _translate = QtCore.QCoreApplication.translate
        MainWindow.setWindowTitle(_translate("MainWindow", "MainWindow"))

        self.menuOpen.setTitle(_translate("MainWindow", "File"))
        self.menuOpen_2.setTitle(_translate("MainWindow", "Open"))
        self.menuModulo_bat.setTitle(_translate("MainWindow", "Modulo bat"))
        self.menuQuit.setTitle(_translate("MainWindow", "Quit"))
        self.actioncccv.setText(_translate("MainWindow", "cccv"))
        self.actioncv.setText(_translate("MainWindow", "cv"))
        self.actiondiffraction.setText(_translate("MainWindow", "diffraction"))
        self.actionimp_dance.setText(_translate("MainWindow", "impédance"))
        self.actioncp.setText(_translate("MainWindow", "cp"))
        self.actiongitt.setText(_translate("MainWindow", "gitt"))
        self.actionvieillissement.setText(_translate("MainWindow", "vieillissement"))


class Window(QMainWindow, Ui_MainWindow):
    def __init__(self, parent=None):
        super().__init__(parent)
        self.setupUi(self)

        self.console = Console()
        self.threads = []
        self.connectSignalsSlots()

        self.tabWidget.name_changed.connect(self.name_changed)
        self.tabWidget.tabCloseRequested.connect(self.close_tab_handler)

    def connectSignalsSlots(self):
        self.actioncccv.triggered.connect(self.open_cccv)
        self.actioncv.triggered.connect(self.open_cv)
        self.actiongitt.triggered.connect(self.open_gitt)

    def open_cccv(self):
        dialog = QFileDialog()
        dialog.setWindowTitle('Open File')
        dialog.setNameFilter('EC_lab file (*.mpt *.txt)')
        dialog.setDirectory(QtCore.QDir.currentPath())
        dialog.setFileMode(QFileDialog.ExistingFile)
        if dialog.exec_() == QDialog.Accepted:
            filename = dialog.selectedFiles()[0]
            filename = r"C:\Users\Maxime\Desktop\fichier_test/test.txt"

            t = QThread()
            worker = Threads_UI.Open_file_cccv([filename, "cccv"])
            worker.moveToThread(t)

            t.started.connect(worker.run)
            worker.finished.connect(self.fin_thread_lecture)

            self.threads.append([t, worker])
            t.start()

    def open_cv(self):
        fig = Figure("test", 1)
        fig.add_data_x_Data(Data_array([1, 2, 3], None, None, "None"))
        fig.add_data_y1_Data(Data_array([10, 5, 20], None, None, "None"))

        obj = Classique_affiche(self.console.current_data, fig)

        self.figure_plot = Figure_plot(obj)
        self.figure_plot.show()

    def open_gitt(self):
        self.console.get_info_data_all()

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
                        self.creation_tab(name_tab)

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


class Main_interface:
    def __init__(self):
        app = QApplication(sys.argv)
        win = Window()
        win.show()
        sys.exit(app.exec())
