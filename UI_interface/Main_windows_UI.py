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
    """utilier quand le nom de la figure est changé"""
    name_changed = pyqtSignal(list)

    """utiliser qunad le plit est sous la forme d'une fenêtre et qu'il est fermé"""
    closed = pyqtSignal(str)

    """utilisé quand le plot est sous la forme d'une fenêtre et qu'il est en focus"""
    focus_in = pyqtSignal(str)

    def __init__(self, abstract_affiche):
        super().__init__()
        self.canvas = None
        self.toolbar = None
        self.edit_w = None
        self.axe_edited = None

        self.setFocusPolicy(QtCore.Qt.TabFocus)
        self.setFocus()

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

        if self.abstract_affiche.leg1 is not None:
            for artist in self.abstract_affiche.leg1.get_legend().get_texts():
                artist.set_picker(True)

        if self.abstract_affiche.leg2 is not None:
            for artist in self.abstract_affiche.leg2.get_legend().get_texts():
                artist.set_picker(True)

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
            if self.abstract_affiche.interactive:
                self.abstract_affiche.focus_off()

            else:
                self.abstract_affiche.focus_on()

    def mouseMoveEvent(self, event):
        pass

    def mousePressEvent(self, event):
        pass

    def closeEvent(self, event):
        """on check QtGui.QCloseEvent car on va close le graph ensuite ce qui va apeller la methode une nouvelle
        fois, on evite d'emit 2 fois, unf foispar qtevent par qt et une seconde CloseEvent de matplotlib"""
        if type(event).__name__ == "QCloseEvent":
            self.closed.emit(self.abstract_affiche.figure.name)

    def axes_enter_event(self, event):
        pass

    def axes_leave_event(self, event):
        pass

    def pick_event(self, event):
        """de la merde, mais pas moyen de trouver comment faire mieux....."""
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
                old_name = event.artist.get_text()
                name = QInputDialog.getText(self, "Name change", "New name ?", QLineEdit.Normal, old_name)
                if name[1]:
                    if self.abstract_affiche.figure.plot_name == old_name:

                        console_temp = Console()
                        new_name = console_temp.current_data.unique_name(name[0])
                        event.artist.set_text(new_name)

                        self.name_changed.emit([old_name, new_name])
                        self.canvas.draw()

                        del console_temp
                    else:
                        for i, text in enumerate(self.abstract_affiche.leg1.get_legend().get_texts()):
                            if text == event.artist:
                                legend_index = i
                                modulo_y1 = []
                                nb_y1 = 0
                                for data in self.abstract_affiche.figure.y1_axe.data:
                                    if data.legend is not None:
                                        nb_y1 += 1
                                if nb_y1 > self.abstract_affiche.figure.nb_legende:
                                    for j in range(self.abstract_affiche.figure.nb_legende):
                                        temp = int(nb_y1 / self.abstract_affiche.figure.nb_legende * j)
                                        if temp not in modulo_y1:
                                            modulo_y1.append(temp)

                                    self.abstract_affiche.figure.y1_axe.data[modulo_y1[i]].legend = name[0]

                                    event.artist.set_text(name[0])
                                    event.artist.set_picker(True)
                                    self.canvas.draw()
                                    return
                                else:
                                    self.abstract_affiche.figure.y1_axe.data[legend_index].legend = name[0]
                                    event.artist.set_text(name[0])
                                    event.artist.set_picker(True)
                                    self.canvas.draw()
                                    return

                        for i, text in enumerate(self.abstract_affiche.leg2.get_legend().get_texts()):
                            if text == event.artist:
                                legend_index = i
                                modulo_y2 = []
                                nb_y2 = 0
                                for data in self.abstract_affiche.figure.y2_axe.data:
                                    if data.legend is not None:
                                        nb_y2 += 1
                                if nb_y2 > self.abstract_affiche.figure.nb_legende:
                                    for j in range(self.abstract_affiche.figure.nb_legende):
                                        temp = int(nb_y2 / self.abstract_affiche.figure.nb_legende * j)
                                        if temp not in modulo_y2:
                                            modulo_y2.append(temp)

                                    self.abstract_affiche.figure.y1_axe.data[modulo_y2[i]].legend = name[0]

                                    event.artist.set_text(name[0])
                                    event.artist.set_picker(True)
                                    self.canvas.draw()
                                    return
                                else:
                                    self.abstract_affiche.figure.y2_axe.data[legend_index].legend = name[0]
                                    event.artist.set_text(name[0])
                                    event.artist.set_picker(True)
                                    self.canvas.draw()
                                    return

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

    def edit_y1_axe(self, ):
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

    def edit_y2_axe(self, ):
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

    def on_top(self):
        self.activateWindow()

    def on_back(self):
        self.lower()

    def is_on_top(self):
        return self.isActiveWindow()

    def focusInEvent(self, event):
        self.focus_in.emit(self.abstract_affiche.figure.name)


class Window(QMainWindow, Ui_MainWindow):
    def __init__(self, parent=None):
        super().__init__(parent)
        self.setupUi(self)

        self.setFocusPolicy(QtCore.Qt.StrongFocus)

        self.console = Console()
        """self.threads est de la forme : [thread, worker]"""
        self.threads = []
        """array contenant les figure ouvertes dans des fenêtre à part"""
        self.figure_w = []

        """objet qui sauvegarde le dernier état de QFileDialog pour la sauvegarde"""
        self.save_state_dialog = None

        """on connect un peu tout"""
        self.connectSignalsSlots()

    """---------------------------------------------------------------------------------"""

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
        self.tabWidget.change_current.connect(self.tab_changed)

    """---------------------------------------------------------------------------------"""

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

    """---------------------------------------------------------------------------------"""

    def open_cv(self):
        fig = Figure("test", 1)
        fig.add_data_x_Data(Data_array([1, 2, 3], None, None, "None"))
        fig.add_data_y1_Data(Data_array([10, 5, 20], None, None, "None"))

        obj = Classique_affiche(self.console.current_data, fig)

        self.figure_plot = Figure_plot(obj)
        self.figure_plot.show()

    """---------------------------------------------------------------------------------"""

    def open_gitt(self):
        """self.console.get_info_data_all()
        self.add_data_tree("figure", "test")"""

        print("current data : " + self.console.current_data.name)
        print("current figure : " + self.console.current_data.current_figure.name)

    """---------------------------------------------------------------------------------"""

    def create_current_data(self):
        """


        :return: None
        """
        if self.console.current_data is None:
            self.current_data_None()
        else:
            if self.comboBox_5.currentText() == "capa":
                """plusieurs figure retournée ici"""
                figures_res = self.console.current_data.capa()
                for figure in reversed(figures_res):
                    self.add_data_tree('figure', figure.name)
                    self.console.current_data.figures.append(figure)


            elif self.comboBox_5.currentText() == "potentio":
                """une seule figure retouné ici"""
                figures_res = self.console.current_data.potentio()

                self.add_data_tree('figure', figures_res.name)
                self.console.current_data.figures.append(figures_res)

    """---------------------------------------------------------------------------------"""

    def create_current_figure(self):
        """
        Methode appellé par le button create de current plot (action)
        Si current_figure is None, on affiche une fenêtre avec un message

        Pour le reste, à faire

        :return: None
        """
        if self.console.current_data is None or self.console.current_data.current_figure is None:
            self.current_figure_None()
        else:
            pass

    """---------------------------------------------------------------------------------"""

    def tree_click(self):
        """
        Déclanché quand item l'utilisateur clique sur un item du tree widget

        Ici on ne change que current_data et la current tab en accords avec
        le clique sur le tree widget, le reste se fait sur la détection du changement
        de tab

        pour le moment l'update de current_data se fait 2 fois, je dois le faire ici
        pour check si la tab associé à l'item du tree widget est déjà ouvert et il se
        refait sur le changement de tab, ce n'est pas grand chose, à voir si j'arrive
        à corriger cela, mais pour le moment je ne vois pas

        Si une tab contenant la figure sélectionnée elle est passé en current tab
        Si un fenêtre plot contient la figure, elle est passé en focus

        :return: None
        """
        _translate = QtCore.QCoreApplication.translate


        if self.treeWidget.currentItem().text(1) == "figure":
            # on update current_data de la console on fonction du parent de l'item sélectionné
            self.console.set_current_data_name(self.treeWidget.selectedItems()[0].parent().text(0))

            # maintenant que current data est update, on parcours les figures de current_data de la console
            for figure in self.console.current_data.figures:

                # quand on a touvé la figure
                if figure.name == self.treeWidget.currentItem().text(0):

                    # check si la tab est déja ouverte
                    for i in range(self.tabWidget.count()):

                        # si elle est ouverte dans une tab
                        if self.tabWidget.tabText(i) == figure.name:

                            # on récupére le current index de tab pour regarder si il sera effectivemeent modifié
                            # si oui l'update de current_figure et des label se fera dans le changement de tab
                            # sinon on le fait là

                            current_index = self.tabWidget.currentIndex()

                            if i == current_index:
                                # on update current data avec self.console.current_data,info update plus haut
                                self.label.setText(
                                    _translate("MainWindow", "<html><head/><body><p><span style=\" font-size:11pt;\">"
                                                             "Current data : "
                                               + self.console.current_data.name + " </span></p></body></html>"))

                                figure_name = self.tabWidget.tabText(current_index)

                                # on update current figure
                                self.console.current_data.set_current_figure_name(figure_name)

                                # on update le label current plot
                                self.label_5.setText(
                                    _translate("MainWindow", "<html><head/><body><p><span style=\" font-size:11pt;\">"
                                                             "Current plot : "
                                               + figure_name + " </span></p></body></html>"))

                            else:
                                # update de current tab
                                self.tabWidget.setCurrentIndex(i)

                            # on passe les fenêtre plot en lower
                            self.lower_plot_w()
                            return

                    # check si la figure est ouverte en fenêtre
                    if not self.on_top_plot_w(figure.name):
                        # si elle est pas ouverte comme fenêtre, toutes les fenêtre plots sont passé en lower
                        self.lower_plot_w()
                    else:
                        return

                    # à ce point de la fonction, le plot n'existe pas, il faut le créer
                    obj = Classique_affiche(self.console.current_data, figure)
                    new_tab = Figure_plot(obj)
                    new_tab.setObjectName(figure.name)
                    new_tab.name_changed.connect(self.name_changed_plot)

                    # on ajoute la tab
                    self.tabWidget.addTab(new_tab, figure.name)

                    # on place la new tab en current
                    self.tabWidget.setCurrentIndex(self.tabWidget.count() - 1)
                    self.tabWidget.setTabsClosable(True)

        else:
            # pas encore sûr de quoi faire ici

            # si l'item sélectoionnée n'est pas une figure
            self.label.setText(_translate("MainWindow", "<html><head/><body><p><span style=\" font-size:11pt;\">"
                                                        "Current data : " +
                                          self.treeWidget.selectedItems()[0].text(0) +
                                          " </span></p></body></html>"))

            # on passe le label currrent plot à None
            self.label_5.setText(_translate("MainWindow", "<html><head/><body><p><span style=\" font-size:11pt;\">"
                                                          "Current plot : None""</span></p></body></html>"))

            # on update current_data de la console
            self.console.set_current_data_name(self.treeWidget.selectedItems()[0].text(0))

    """---------------------------------------------------------------------------------"""

    def fin_thread_lecture(self):
        """
        Déclanchée à la suite de la fin de l'execution d'un thread de lecture
        On créer un nouvelle objet data associée au data récupérées par le thread

        :return: None
        """
        index = 0
        # on parcours les threads de lecture en cours
        while index < len(self.threads):

            # si le thread à fini
            if self.threads[index][1].finish:

                # si le thread n'a aucune data, le type de fichier est invalide
                # on affiche un pop_up
                if self.threads[index][1].data is None:
                    self.fichier_invalide_error()
                else:

                    # si le type de fichier lu est cccv
                    if type(self.threads[index][1]).__name__ == "Open_file_cccv":
                        # on créer un objet data cccv
                        obj_data = CCCV_data()

                        # on lui ajoute les data lu par le thread
                        obj_data.data = self.threads[index][1].data

                        # créer son nom
                        obj_data.name = obj_data.data["name"]

                        # on ajoute l'objet data à la console
                        self.console.add_data(obj_data)

                        # on update le tree widget
                        name_tab = obj_data.name
                        self.add_data_tree("cccv", name_tab)

                    # on récupére les actions disponibles pour ce type de fichier pour update
                    # current data comboBox_5
                    for action in self.console.current_data.get_operation_available():
                        self.comboBox_5.addItem(action)

                # on termine le thread
                self.threads[index][0].terminate()

                # on le suprime de la liste
                del self.threads[index]
            else:
                index += 1

    """---------------------------------------------------------------------------------"""

    def add_data_tree(self, type, name, parent=None):
        """
        fonction à refaire, ne fonctionne pas
        créer un objet qui garde trace le l'architecture des données, ne sais pas

        :param type: str de la colonne type a afficher (figure / type exp)
        :param name: str de la colonne name a afficher
        :param parent:
        :return: None
        """

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

    """---------------------------------------------------------------------------------"""

    def name_changed_tab(self, signal):
        """
        Déclanché quand le nom d'une tab est changée
        On update le nom de la figure associée dans la console
        On update le titre du plot
        On update le label current plot

        :param signal: ancien nom de la tab qui vient d'être modifié
        :return: None
        """

        # on cherche la figure portant l'ancien nom
        for figure in self.console.current_data.figures:
            if figure.name == signal:

                # le nouveau nom est celui de la tab
                name = self.tabWidget.tabText(self.tabWidget.currentIndex())

                # on update le nom de la figure dans la console
                figure.name = name

                # on update le nom de l'item de tree widget
                for i in range(self.treeWidget.topLevelItem(0).childCount()):
                    if self.treeWidget.topLevelItem(0).child(i).text(0) == signal:
                        self.treeWidget.topLevelItem(0).child(i).setText(0, name)
                        break

                # on update le nom du plot associé à la tab
                self.tabWidget.currentWidget().update_title_plot(name)

                # on update current plot
                _translate = QtCore.QCoreApplication.translate
                self.label_5.setText(_translate("MainWindow", "<html><head/><body><p><span style=\" font-size:11pt;\">"
                                                              "Current plot : "
                                                + name + " </span></p></body></html>"))
                break

    """---------------------------------------------------------------------------------"""

    def close_tab_handler(self, index):
        """
        Permet de fermet une tab quand la croix de d'une est cliqué

        :param index: index de la tab qui a déchanché cette demande de fermeture
        :return: None
        """

        # la tab à l'index est remove
        self.tabWidget.removeTab(index)

    """---------------------------------------------------------------------------------"""

    def name_changed_plot(self, signal):
        """
        Déclanchée quand le nom du plot est changé, on update le nom
        de current_figure de la console
        On update le nom de la tab associée avec le nouveau nom
        On update tree widget on conséquence
        On update le label current plot

        :param signal: [old_name, new_name]
        :return: None

        """
        old_name = signal[0]
        new_name = signal[1]

        # update du nom de current_figure
        self.console.current_data.current_figure.name = new_name

        # update du nom de la tab associé
        self.tabWidget.setTabText(self.tabWidget.currentIndex(), new_name)

        # update du nom de l'item associé dans tree widget
        for i in range(self.treeWidget.topLevelItem(0).childCount()):
            if self.treeWidget.topLevelItem(0).child(i).text(0) == old_name:
                self.treeWidget.topLevelItem(0).child(i).setText(0, new_name)
                break

        # on update le label current plot
        _translate = QtCore.QCoreApplication.translate
        self.label_5.setText(_translate("MainWindow", "<html><head/><body><p><span style=\" font-size:11pt;\">"
                                                      "Current plot : "
                                        + new_name + " </span></p></body></html>"))

    """---------------------------------------------------------------------------------"""

    def break_tab(self, signal):
        """
        Gére le fait de détacher une tab et de créer une nouvelle fenêtre
        avec le plot correspondant à la tab détachée

        Cette nouvelle fenêtre aura 3 connections :
            close_w_plot : déclenché quand la fenêtre sera fermée

            focus_in_w_plot : déclenché quand la fenêtre passera en focus

            name_changed_w_plot : déclenché qunad le nom du plot de la fenêtre sera modifié, pour garder
            la cohérence de l'affichage global

        :param signal: index de la tab détachée
        :return: None
        """
        # le focus du plot de la tab détachée est passé à off pour reset les couleurs, lignes etc
        self.tabWidget.widget(signal).abstract_affiche.focus_off()

        # une nouvelle fenêtre est créée avec comme paramétre abstract_affiche du plot de la tab détachée
        # on garde donc les éventuels résultats et calculs effectuées sur ce plot
        new_w = Figure_plot(self.tabWidget.widget(signal).abstract_affiche)

        # connection avec la nouvelle fenêtre
        new_w.closed.connect(self.close_w_plot)
        new_w.focus_in.connect(self.focus_in_w_plot)
        new_w.name_changed.connect(self.name_changed_w_plot)

        # on ajoute la nouvelle fene^tre à un vecteur pour en garder une ref
        self.figure_w.append(new_w)

        # on affiche la fenêtre
        new_w.show()

    """---------------------------------------------------------------------------------"""

    def close_w_plot(self, signal):
        """"
        La fenêtre du plot a été fermé, on recréer une tab avec la figure qui était présente sur la
        fenêtre

        :param signal: nom de la fenêtre fermée
        :return: None
        """

        # on cherche dans le vecteur de fenêtre plot la figure qui vient d'être fermée
        for i, affiche_obj in enumerate(self.figure_w):
            if affiche_obj.abstract_affiche.figure.name == signal:
                # on passe la figure en focus off pour reset les couleurs, les lignes etc
                affiche_obj.abstract_affiche.focus_off()

                # création d'une tab avec abstract_affiche de la fenêtre fermée pour garder
                # les résultats et calcules obtenus
                new_tab = Figure_plot(affiche_obj.abstract_affiche)
                new_tab.setObjectName(signal)

                # connection de la nouvelle tab
                new_tab.name_changed.connect(self.name_changed_plot)

                # on ajoute cette nouvelle tab au widget
                self.tabWidget.addTab(new_tab, signal)

                # on ferme le graph de la fenêtre
                pplot.close(self.figure_w[i].abstract_affiche.pplot_fig)

                # on supprime l'ancienne fenêtre du vecteur
                del self.figure_w[i]
                break

    """---------------------------------------------------------------------------------"""

    def focus_in_w_plot(self, signal):
        """
        Déclanché si une fenêtre plot passe en focus
        On update les informations de la fenêtre principal pour la cohérence
        On update la figure courrante de la console
        On update l'élément focus dans le tree widget


        :param signal: nom de la fenêtre qui vient d'être passée en focus
        :return: None
        """
        _translate = QtCore.QCoreApplication.translate
        # update du label affichant la figure courrante
        self.label_5.setText(_translate("MainWindow", "<html><head/><body><p><span style=\" font-size:11pt;\">"
                                                      "Current plot : "
                                        + signal + " </span></p></body></html>"))

        # update de la figure courrante de la console
        self.console.current_data.set_current_figure_name(signal)

        # update du focus du tree widget
        for i in range(self.treeWidget.topLevelItem(0).childCount()):
            if self.treeWidget.topLevelItem(0).child(i).text(0) == signal:
                self.treeWidget.setCurrentItem(self.treeWidget.topLevelItem(0).child(i))
                break

    """---------------------------------------------------------------------------------"""

    def name_changed_w_plot(self, signal):
        """
        Déclanché quand le nom du plot est modifiée sur une
        fenêtre
        Update des infommations de la fenêtre principal pour la cohérence
        Update de la console

        :param signal: [old_name, new_name]
        :return: None
        """

        old_name = signal[0]
        new_name = signal[1]

        # update du nom du current_figure de la console
        self.console.current_data.current_figure.name = new_name

        # update du nom du tree widget associé
        for i in range(self.treeWidget.topLevelItem(0).childCount()):
            if self.treeWidget.topLevelItem(0).child(i).text(0) == old_name:
                self.treeWidget.topLevelItem(0).child(i).setText(0, new_name)
                break

        # on update le label current plot
        _translate = QtCore.QCoreApplication.translate
        self.label_5.setText(_translate("MainWindow", "<html><head/><body><p><span style=\" font-size:11pt;\">"
                                                      "Current plot : "
                                        + new_name + " </span></p></body></html>"))

    """---------------------------------------------------------------------------------"""

    def lower_plot_w(self):
        """
        Passe toutes les fenêtre plot en arrière plan

        :return: None
        """
        for figure in self.figure_w:
            figure.on_back()

    """---------------------------------------------------------------------------------"""

    def on_top_plot_w(self, name):
        """
        Si la figure pourtant le nom name est ouverte comme fenêtre, on la place comme focus
        return true si la figure a été mise on top, false sinon

        :param name: nom de la figure dont la fenêtre doit être passé au premier plan
        :return: True / False
        """

        # on parcours les fenêtre plit ouverte pour trouver celle portant le nom name
        for figure in self.figure_w:
            if figure.abstract_affiche.figure.name == name:
                # si on trouve la figure comme étant une fenêtre on la place on top
                figure.on_top()

                # on update la figure courrante
                self.console.current_data.set_current_figure_name(name)

                # on update l'affichage de current plot
                _translate = QtCore.QCoreApplication.translate
                self.label_5.setText(_translate("MainWindow", "<html><head/><body><p><span style=\" font-size:11pt;\">"
                                                              "Current plot : "
                                                + name + " </span></p></body></html>"))
                return True

        return False

    """---------------------------------------------------------------------------------"""

    def tab_changed(self, signal):
        """
        si la current tab est changée il faut changer l'affichage de current plot et changer
        la figure courrante de la console

        :param signal: index de la tab qui vient d'être passe en tab courrante
        :return: None
        """

        # check si le changement de tab est dû à drag, dans ce cas il ne faut pas update
        # current plot avec le changement de tab
        for figure in self.figure_w:
            if figure.is_on_top():
                return

        _translate = QtCore.QCoreApplication.translate

        new_name = self.tabWidget.tabText(signal)

        parent = None
        # on update l'élément focus par le tree widget
        for i in range(self.treeWidget.topLevelItem(0).childCount()):
            if self.treeWidget.topLevelItem(0).child(i).text(0) == new_name:
                self.treeWidget.setCurrentItem(self.treeWidget.topLevelItem(0).child(i))

                # on récupére le parent
                parent = self.treeWidget.topLevelItem(0).child(i).parent()
                break

        # on check que l'on a bien récupéré le parent
        if parent is None:
            raise ValueError

        # on update current data de la console en premier
        self.console.set_current_data_name(parent.text(0))

        # si le type de fichier a changé, il faut update les actions disponibles
        if parent.text(1) != self.console.current_data.__name__:
            for action in self.console.current_data.get_operation_available():
                self.comboBox_5.addItem(action)


        # on update current data avec le nom du parant
        self.label.setText(_translate("MainWindow", "<html><head/><body><p><span style=\" font-size:11pt;\">"
                                                    "Current data : "
                                      + parent.text(0) + " </span></p></body></html>"))

        # on update current figure
        self.console.current_data.set_current_figure_name(new_name)

        # on update le label current plot
        self.label_5.setText(_translate("MainWindow", "<html><head/><body><p><span style=\" font-size:11pt;\">"
                                                      "Current plot : "
                                        + new_name + " </span></p></body></html>"))

    """---------------------------------------------------------------------------------"""

    def focusInEvent(self, signal):
        """
        Si la fenêtre princial repasse en focus, on update les informations
        pour quelles soit cohérente

        Si aucune tab n'est présente lors du focus aucune erreur est déclanchée, le nom
        sera juste ""

        :param signal: inutile ici
        :return: None
        """

        # si current figure n'est pas pas setup on return
        # pour ne pas déclancer des erreurs à la création de la fenêtre
        if self.console.current_data is None or self.console.current_data.current_figure is None:
            return

        _translate = QtCore.QCoreApplication.translate

        # le nom de la figure courrante est donc celui de la tab courrante
        new_name = self.tabWidget.tabText(self.tabWidget.currentIndex())

        # on update le label current plot
        self.label_5.setText(_translate("MainWindow", "<html><head/><body><p><span style=\" font-size:11pt;\">"
                                                      "Current plot : "
                                        + new_name +
                                        " </span></p></body></html>"))

        # on update la figure courrante de la console
        self.console.current_data.set_current_figure_name(new_name)

        # on update l'imte focus par tree widget
        for i in range(self.treeWidget.topLevelItem(0).childCount()):
            if self.treeWidget.topLevelItem(0).child(i).text(0) == new_name:
                self.treeWidget.setCurrentItem(self.treeWidget.topLevelItem(0).child(i))
                break

    """---------------------------------------------------------------------------------"""

    def fichier_invalide_error(self):
        """
        QMessageBox indiquand que le type de fichier sélectionné est invalide

        :return: None
        """
        msgBox = QMessageBox()
        msgBox.setIcon(QMessageBox.Warning)
        msgBox.setText("File type invalid")
        msgBox.setWindowTitle("Error")
        msgBox.setStandardButtons(QMessageBox.Ok)
        msgBox.exec()

    """---------------------------------------------------------------------------------"""

    def current_data_None(self):
        """
        QMessageBox indiquand qu'une action sur un plot ou une data
        a été demandé dans que des datas est été chargé

        :return: None
        """
        msgBox = QMessageBox()
        msgBox.setIcon(QMessageBox.Warning)
        msgBox.setText("No file open")
        msgBox.setWindowTitle("Error")
        msgBox.setStandardButtons(QMessageBox.Ok)
        msgBox.exec()

    """---------------------------------------------------------------------------------"""

    def current_figure_None(self):
        """
        QMessageBox indiquand qu'une action sur un plot a été demandé et
        qu'aucun plot n'est en figure courrante

        :return:
        """
        msgBox = QMessageBox()
        msgBox.setIcon(QMessageBox.Warning)
        msgBox.setText("No plot selected")
        msgBox.setWindowTitle("Error")
        msgBox.setStandardButtons(QMessageBox.Ok)
        msgBox.exec()

    """---------------------------------------------------------------------------------"""

    def fait(self):
        """
        QMessageBox indiquand qu'une action a été effectuée
        je ne m'en sert pas pour le moment, et peut-être jamais

        :return: None
        """
        msgBox = QMessageBox()
        msgBox.setIcon(QMessageBox.Ok)
        msgBox.setText("Done")
        msgBox.setWindowTitle("Done")
        msgBox.setStandardButtons(QMessageBox.Ok)
        msgBox.exec()


class Main_interface:
    def __init__(self):
        app = QApplication(sys.argv)
        win = Window()
        win.show()
        sys.exit(app.exec())
