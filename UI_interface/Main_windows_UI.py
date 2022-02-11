import copy
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
from UI_interface.Main_window_QT import Ui_MainWindow, Edit_Axe

"""----------------------------------------------------------------------------------"""
"""                                   Main window                                    """
"""----------------------------------------------------------------------------------"""


class Figure_plot(QWidget):
    name_changed = pyqtSignal(str)
    closed = pyqtSignal(str)

    def __init__(self, abstract_affiche):
        super().__init__()
        self.canvas = None
        self.toolbar = None
        self.edit_w = None
        self.axe_edited = None

        """abstract_affiche"""
        self.abstract_affiche = abstract_affiche
        """création du canvas + widget matplotlib"""
        self.create_plot()

    def create_plot(self):
        self.abstract_affiche.create_figure()

        layout = QVBoxLayout()
        self.setLayout(layout)
        self.canvas = FigureCanvas(self.abstract_affiche.pplot_fig)
        self.toolbar = NavigationToolbar2QT(self.canvas, self, True)

        for artist in self.abstract_affiche.pplot_fig.get_children():
            if type(artist).__name__ == "Text":
                artist.set_picker(True)

        if self.abstract_affiche.ax1 is not None:
            self.abstract_affiche.ax1.xaxis.get_label().set_picker(True)
            self.abstract_affiche.ax1.yaxis.get_label().set_picker(True)
        else:
            self.abstract_affiche.ax2.xaxis.get_label().set_picker(True)

        if self.abstract_affiche.ax2 is not None:
            self.abstract_affiche.ax2.yaxis.get_label().set_picker(True)

        if self.abstract_affiche.ax1 is not None:
            self.abstract_affiche.ax1.xaxis.set_picker(True)
            self.abstract_affiche.ax1.yaxis.set_picker(True)
        else:
            self.abstract_affiche.ax2.xaxis.set_picker(True)

        if self.abstract_affiche.ax2 is not None:
            self.abstract_affiche.ax2.xaxis.set_picker(True)

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
        if event.inaxes is not None and (event.inaxes == self.abstract_affiche.ax1 or
                                         event.inaxes == self.abstract_affiche.ax2):
            black = matplotlib.colors.to_rgba("black")
            event.inaxes.axhline(y=event.ydata, color=black)
            event.inaxes.axvline(x=event.xdata, color=black)
            self.canvas.draw()

    def mouseMoveEvent(self, event):
        pass

    def mousePressEvent(self, event):
        pass

    def closeEvent(self, event):
        self.closed.emit(self.abstract_affiche.figure.name)

    def axes_enter_event(self, event):
        pass

    def axes_leave_event(self, event):
        pass

    def pick_event(self, event):
        """de la merde, mais pas moyen de trouver comment faire mieux......"""

        if event.mouseevent.button == 1 and event.mouseevent.dblclick:
            """on prends le centre de la figure, si le click est plus loi que le centre c'est l'axe de
            droite, gauche sinon"""
            center = (self.canvas.figure.get_size_inches()[0] * 96) * 0.9 / 2

            if type(event.artist).__name__ == "XAxis" and self.abstract_affiche.ax1 is not None and \
                    event.artist == self.abstract_affiche.ax1.xaxis:
                self.edit_x_axe()

            elif type(event.artist).__name__ == "Text" and self.abstract_affiche.ax1 is not None and \
                    event.artist == self.abstract_affiche.ax1.xaxis.get_label():
                self.edit_x_axe()

            elif type(event.artist).__name__ == "XAxis" and self.abstract_affiche.ax2 is not None and \
                    event.artist == self.abstract_affiche.ax2.xaxis:
                self.edit_x_axe()

            elif type(event.artist).__name__ == "Text" and self.abstract_affiche.ax2 is not None and \
                    event.artist == self.abstract_affiche.ax2.xaxis.get_label():
                self.edit_x_axe()

            elif type(event.artist).__name__ == "YAxis" and self.abstract_affiche.ax1 is not None and \
                    event.mouseevent.x < center:
                self.edit_y1_axe()

            elif type(event.artist).__name__ == "Text" and self.abstract_affiche.ax1 is not None and \
                    event.artist == self.abstract_affiche.ax1.yaxis.get_label():
                self.edit_y1_axe()

            elif type(event.artist).__name__ == "YAxis" and self.abstract_affiche.ax2 is not None and \
                    event.mouseevent.x >= center:
                self.edit_y2_axe()

            elif type(event.artist).__name__ == "Text" and self.abstract_affiche.ax2 is not None and \
                    event.artist == self.abstract_affiche.ax2.yaxis.get_label():
                self.edit_y2_axe()

            else:
                if event.mouseevent.dblclick:
                    name = QInputDialog.getText(self, "Name change", "New name ?", QLineEdit.Normal)
                    if name[1]:
                        event.artist.set_text(name[0])
                        self.abstract_affiche.figure.plot_name = name[0]
                        self.name_changed.emit(name[0])
                        self.canvas.draw()

    def edit_x_axe(self):
        if self.edit_w is None:
            self.axe_edited = "x"
            self.edit_w = Edit_Axe()
            _translate = QtCore.QCoreApplication.translate
            self.edit_w.label.setText(_translate("Form",
                                                 "<html><head/><body><p align=\"center\"><span style=\" font-size:14pt;"
                                                 "\">Edit " + self.abstract_affiche.figure.x_axe.name +
                                                 " :</span></p></body></html>"))
            self.edit_w.lineEdit_2.setText(self.abstract_affiche.figure.x_axe.name)
            if self.abstract_affiche.figure.x_axe.scale == "linear":
                self.edit_w.comboBox_18.setCurrentIndex(0)
            elif self.abstract_affiche.figure.x_axe.scale == "log":
                self.edit_w.comboBox_18.setCurrentIndex(1)

            self.edit_w.finish.connect(self.edit_finishded)
            self.edit_w.show()

    def edit_y1_axe(self,):
        if self.edit_w is None:
            self.axe_edited = "y1"
            self.edit_w = Edit_Axe()
            _translate = QtCore.QCoreApplication.translate
            self.edit_w.label.setText(_translate("Form",
                                                 "<html><head/><body><p align=\"center\"><span style=\" font-size:14pt;"
                                                 "\">Edit " + self.abstract_affiche.figure.y1_axe.name +
                                                 " :</span></p></body></html>"))
            self.edit_w.lineEdit_2.setText(self.abstract_affiche.figure.y1_axe.name)
            if self.abstract_affiche.figure.y1_axe.scale == "linear":
                self.edit_w.comboBox_18.setCurrentIndex(0)
            elif self.abstract_affiche.figure.y1_axe.scale == "log":
                self.edit_w.comboBox_18.setCurrentIndex(1)

            self.edit_w.finish.connect(self.edit_finishded)
            self.edit_w.show()

    def edit_y2_axe(self,):
        if self.edit_w is None:
            self.axe_edited = "y2"
            self.edit_w = Edit_Axe()
            _translate = QtCore.QCoreApplication.translate
            self.edit_w.label.setText(_translate("Form",
                                                 "<html><head/><body><p align=\"center\"><span style=\" font-size:14pt;"
                                                 "\">Edit " + self.abstract_affiche.figure.y2_axe.name +
                                                 " :</span></p></body></html>"))
            self.edit_w.lineEdit_2.setText(self.abstract_affiche.figure.y2_axe.name)
            if self.abstract_affiche.figure.y2_axe.scale == "linear":
                self.edit_w.comboBox_18.setCurrentIndex(0)
            elif self.abstract_affiche.figure.y2_axe.scale == "log":
                self.edit_w.comboBox_18.setCurrentIndex(1)

            self.edit_w.finish.connect(self.edit_finishded)
            self.edit_w.show()

    def update_title_plot(self, name):
        self.abstract_affiche.pplot_fig.suptitle(name).set_picker(True)
        self.canvas.draw()

    def edit_finishded(self, event):
        if event == "save":
            new_name = self.edit_w.lineEdit_2.text()
            if new_name != "":
                if self.axe_edited == "x":
                    self.abstract_affiche.figure.x_axe.name = new_name
                    self.abstract_affiche.ax1.xaxis.set_label_text(new_name)
                elif self.axe_edited == "y1":
                    self.abstract_affiche.figure.y1_axe.name = new_name
                    self.abstract_affiche.ax1.yaxis.set_label_text(new_name)
                elif self.axe_edited == "y2":
                    self.abstract_affiche.figure.y2_axe.name = new_name
                    self.abstract_affiche.ax2.yaxis.set_label_text(new_name)

            new_scale = self.edit_w.comboBox_18.itemText(self.edit_w.comboBox_18.currentIndex())
            if self.axe_edited == "x":
                self.abstract_affiche.figure.x_axe.scale = new_scale
                self.abstract_affiche.ax1.set_xscale(new_scale)
                self.abstract_affiche.ax1.xaxis.set_picker(True)
            elif self.axe_edited == "y1":
                self.abstract_affiche.figure.y1_axe.scale = new_scale
                self.abstract_affiche.ax1.set_yscale(new_scale)
                self.abstract_affiche.ax1.yaxis.set_picker(True)
            elif self.axe_edited == "y2":
                self.abstract_affiche.figure.y2_axe.scale = new_scale
                self.abstract_affiche.ax2.set_yscale(new_scale)
                self.abstract_affiche.ax2.yaxis.set_picker(True)

            self.canvas.draw()

        self.edit_w.deleteLater()
        self.edit_w = None
        self.axe_edited = None


class Window(QMainWindow, Ui_MainWindow):
    def __init__(self, parent=None):
        super().__init__(parent)
        self.setupUi(self)

        self.console = Console()
        """self.threads est de la forme : [thread, worker]"""
        self.threads = []
        """array contenant les figure ouvertes dans des fenêtre à part"""
        self.figure_w = []

        """objet qui sauvegarde le dernier état de QFileDialog pour la sauvegarde"""
        self.save_state_dialog = None
        self.connectSignalsSlots()

    def connectSignalsSlots(self):
        self.actioncccv.triggered.connect(self.open_cccv)
        self.actioncv.triggered.connect(self.open_cv)
        self.actiongitt.triggered.connect(self.open_gitt)
        self.pushButton_5.clicked.connect(self.create_current_data)
        self.pushButton_4.clicked.connect(self.create_current_figure)
        self.treeWidget.clicked.connect(self.tree_click)
        self.tabWidget.tabCloseRequested.connect(self.close_tab_handler)
        self.tabWidget.name_changed_tab.connect(self.name_changed_tab)
        self.tabWidget.break_tab.connect(self.break_tab)
        self.treeWidget.itemSelectionChanged.connect(self.tree_select_change)

    """----------------------------------------------------------------------------------"""
    """                                     Signals                                      """
    """----------------------------------------------------------------------------------"""

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

    def create_current_data(self):
        if self.console.current_data is None:
            self.current_data_None()
        else:
            if self.comboBox_5.currentText() == "capa":
                figures_res = self.console.current_data.capa()
                for figure in reversed(figures_res):
                    self.add_data_tree('figure', figure.name)
                    self.console.current_data.figures.append(figure)

    def create_current_figure(self):
        if self.console.current_data is None or self.console.current_data.current_figure is None:
            self.current_figure_None()
        else:
            pass

    def tree_click(self):
        if self.treeWidget.currentItem().text(1) == "figure":
            for figure in self.console.current_data.figures:
                if figure.name == self.treeWidget.currentItem().text(0):
                    """check si la tab est déja ouverte"""
                    for i in range(self.tabWidget.count()):
                        if self.tabWidget.tabText(i) == figure.name:
                            self.tabWidget.setCurrentIndex(i)
                            return

                    obj = Classique_affiche(self.console.current_data, figure)
                    new_tab = Figure_plot(obj)
                    new_tab.setObjectName(figure.name)
                    new_tab.name_changed.connect(self.name_changed_plot)
                    self.tabWidget.addTab(new_tab, figure.name)

                    self.tabWidget.setCurrentIndex(self.tabWidget.count() - 1)
                    self.tabWidget.setTabsClosable(True)

    def fichier_invalide_error(self):
        msgBox = QMessageBox()
        msgBox.setIcon(QMessageBox.Warning)
        msgBox.setText("File type invalid")
        msgBox.setWindowTitle("Error")
        msgBox.setStandardButtons(QMessageBox.Ok)
        msgBox.exec()

    def current_data_None(self):
        msgBox = QMessageBox()
        msgBox.setIcon(QMessageBox.Warning)
        msgBox.setText("No file open")
        msgBox.setWindowTitle("Error")
        msgBox.setStandardButtons(QMessageBox.Ok)
        msgBox.exec()

    def current_figure_None(self):
        msgBox = QMessageBox()
        msgBox.setIcon(QMessageBox.Warning)
        msgBox.setText("No plot selected")
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

                        for action in self.console.current_data.get_operation_available():
                            self.comboBox_5.addItem(action)

                self.threads[index][0].terminate()
                del self.threads[index]
            else:
                index += 1

    def add_data_tree(self, type, name, parent=None):
        if type == "figure":
            for itm in self.tree_items:
                for i, child_item in enumerate(itm):
                    if child_item.isSelected():
                        child = QTreeWidgetItem([name, type])
                        child.setSelected(True)
                        itm[0].insertChild(i, child)
                        itm.append([child])
                        break
        else:
            item = QTreeWidgetItem([name, type])
            self.treeWidget.insertTopLevelItem(len(self.tree_items), item)
            self.tree_items.append([item])
            for itm in self.tree_items:
                for child in itm:
                    child.setSelected(False)
            item.setSelected(True)

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
                                              + parent.text(0) + " </span></p></body></html>"))
                self.console.set_current_data_name(parent.text(0))
                self.console.current_data.set_current_figure_name(self.treeWidget.selectedItems()[0].text(0))
            else:
                self.label.setText(_translate("MainWindow", "<html><head/><body><p><span style=\" font-size:11pt;\">"
                                                            "Current data : " +
                                              self.treeWidget.selectedItems()[0].text(0) +
                                              " </span></p></body></html>"))
                self.label_5.setText(_translate("MainWindow", "<html><head/><body><p><span style=\" font-size:11pt;\">"
                                                              "Current plot : None""</span></p></body></html>"))
                self.console.set_current_data_name(self.treeWidget.selectedItems()[0].text(0))

    def name_changed_tab(self, signal):
        for figure in self.console.current_data.figures:
            if figure.name == signal:
                name = self.tabWidget.tabText(self.tabWidget.currentIndex())
                figure.name = name
                for i in range(self.treeWidget.topLevelItem(0).childCount()):
                    if self.treeWidget.topLevelItem(0).child(i).text(0) == signal:
                        self.treeWidget.topLevelItem(0).child(i).setText(0, name)
                self.tabWidget.currentWidget().update_title_plot(name)
                break

    def close_tab_handler(self, index):
        name = self.tabWidget.tabText(index)
        for i, data in enumerate(self.console.datas):
            if data.name == name:
                del self.console.datas[i]
                break
        self.tabWidget.removeTab(index)

    def name_changed_plot(self, signal):
        self.console.current_data.current_figure.name = signal
        old_name = self.tabWidget.tabText(self.tabWidget.currentIndex())
        self.tabWidget.setTabText(self.tabWidget.currentIndex(), signal)
        for i in range(self.treeWidget.topLevelItem(0).childCount()):
            if self.treeWidget.topLevelItem(0).child(i).text(0) == old_name:
                self.treeWidget.topLevelItem(0).child(i).setText(0, signal)

    def break_tab(self, event):
        obj = Classique_affiche(self.console.current_data, self.console.current_data.current_figure)
        new_w = Figure_plot(obj)
        new_w.closed.connect(self.plot_w_closed)
        self.figure_w.append(new_w)
        new_w.show()

    def plot_w_closed(self, event):
        for i, affiche_obj in enumerate(self.figure_w):
            if affiche_obj.abstract_affiche.figure.name == event:
                obj = Classique_affiche(self.console.current_data, affiche_obj.abstract_affiche.figure)
                new_tab = Figure_plot(obj)
                new_tab.setObjectName(event)
                new_tab.name_changed.connect(self.name_changed_plot)
                self.tabWidget.addTab(new_tab, event)
                del self.figure_w[i]
                break

class Main_interface:
    def __init__(self):
        app = QApplication(sys.argv)
        win = Window()
        win.show()
        sys.exit(app.exec())
