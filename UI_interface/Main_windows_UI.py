import copy
import os
import sys

import matplotlib
from PyQt5 import QtCore, QtWidgets
from PyQt5.QtCore import QThread, pyqtSignal
from PyQt5.QtGui import QColor
from PyQt5.QtWidgets import (
    QApplication, QDialog, QMainWindow, QMessageBox, QFileDialog, QWidget, QLineEdit, QVBoxLayout, QInputDialog
)
from matplotlib.backend_bases import MouseButton

from matplotlib.backends.backend_qt import NavigationToolbar2QT, SubplotToolQt
from matplotlib.backends.backend_qt5agg import FigureCanvasQTAgg as FigureCanvas
import matplotlib.pyplot as pplot
from Console_Objets.Affiche_objet import Classique_affiche, Edit_affiche
from Console_Objets.Console import Console
from Console_Objets.Data_array import Data_array
from Console_Objets.Figure import Figure
from Data_type.CCCV_data import CCCV_data
from Resources import Resources
from UI_interface import Threads_UI
from UI_interface.Main_window_QT import Ui_MainWindow, Edit_Axe, Edit_plot

"""----------------------------------------------------------------------------------"""
"""                                   Main window                                    """
"""----------------------------------------------------------------------------------"""


class Figure_plot(QWidget):
    """
    class qui gére les graphiqes matplotlib, soit en widget soit en fenêtre indépendante
    elle gére les interactions de la class Affiche objet, les interactions avec l'édition
    des axes et legendes

    """
    # utilier quand le nom de la figure est changé
    name_changed = pyqtSignal(list)

    # utiliser qunad le plit est sous la forme d'une fenêtre et qu'il est fermé
    closed = pyqtSignal(str)

    # utilisé quand le plot est sous la forme d'une fenêtre et qu'il est en focus
    focus_in = pyqtSignal(str)

    def __init__(self, abstract_affiche):
        super().__init__()
        self.canvas = None
        self.toolbar = None
        self.edit_w = None
        self.axe_edited = None

        # focus policy
        self.setFocusPolicy(QtCore.Qt.TabFocus)
        self.setFocus()

        # abstract_affiche
        self.abstract_affiche = abstract_affiche

        # setup
        self.create_plot()

    """---------------------------------------------------------------------------------"""

    def create_plot(self):
        """
        On setup tout

        Le layout
        La figure matplotlib
        Le canvas
        La toolbar
        On passe tous les piker des artistes qui nous interesse à True
            le nom du plot
            les axes
            les labels des axes
            les legendes

        On connect les events matplotlib

        :return: None
        """
        # on créer la figure matplotlib associé à self.abstract_affiche et sa figure
        self.abstract_affiche.create_figure()

        layout = QVBoxLayout()
        self.setLayout(layout)

        # création du canvas
        self.canvas = FigureCanvas(self.abstract_affiche.pplot_fig)

        # on récupére la toolbar de matplotlib
        self.toolbar = NavigationToolbar2QT(self.canvas, self, True)

        layout.addWidget(self.canvas)
        layout.addWidget(self.toolbar)

        # connections pour events matplotlib effectués sur le canvas
        self.canvas.mpl_connect('button_press_event', self.button_press_event)
        # self.canvas.mpl_connect('motion_notify_event', self.mouseMoveEvent)
        self.canvas.mpl_connect('close_event', self.closeEvent)
        self.canvas.mpl_connect('axes_enter_event', self.axes_enter_event)
        self.canvas.mpl_connect('axes_leave_event', self.axes_leave_event)

        # on connect abstract_affiche
        self.abstract_affiche.connect_all()

        self.canvas.draw()

    """---------------------------------------------------------------------------------"""

    def button_press_event(self, event):
        """
        Déclenché par un clique sur self.canvas
        Ne gére que les cliques en dehors des axes, les cliques dans les axes sont
        géré par Affiche_obj
        On check si abstract_affiche a le droit d'être édité, sinon on ne fait rien

        :param event: button_press_event
        :return: None
        """
        if self.abstract_affiche.editable and event.dblclick and event.inaxes is None and event.button == MouseButton.LEFT \
                and not self.abstract_affiche.interactive:
            self.edit_plot(event)

    """---------------------------------------------------------------------------------"""

    def edit_plot(self, event):
        """
        Callback d'un clique hors des axes du graphique

        On check si ce click a été effectué sur un avec ou label pouvant être édité
        Si oui on appelle la fonction d'édition correspondante

        :param event: MousseEvent matplotlib
        :return: None
        """

        # check de l'axe x
        if self.abstract_affiche.ax1.xaxis.contains(event)[0] or \
                self.abstract_affiche.ax1.xaxis.get_label().contains(event)[0]:
            self.edit_x_axe()

        # check de l'axe y1
        elif self.abstract_affiche.ax1.yaxis.contains(event)[0] or \
                self.abstract_affiche.ax1.yaxis.get_label().contains(event)[0]:
            self.edit_y1_axe()

        # check de l'axe y2
        elif self.abstract_affiche.ax2 is not None and \
                (self.abstract_affiche.ax2.yaxis.contains(event)[0] or
                 self.abstract_affiche.ax2.yaxis.get_label().contains(event)[0]):
            self.edit_y2_axe()

        # check du suptitle
        elif self.abstract_affiche.pplot_fig._suptitle.contains(event)[0]:
            self.edit_suptitle()

        else:
            # check de la ligne de la légende 1
            if self.abstract_affiche.leg1 is not None:
                for i, artist in enumerate(self.abstract_affiche.leg1.get_legend().get_lines()):
                    if artist.contains(event)[0]:
                        self.edit_legend_1(i)
                        return

                # check du text de la légende 1
                for i, artist in enumerate(self.abstract_affiche.leg1.get_legend().get_texts()):
                    if artist.contains(event)[0]:
                        self.edit_legend_1(i)
                        return

            if self.abstract_affiche.leg2 is not None:
                # check de la ligne de la légende 2
                for i, artist in enumerate(self.abstract_affiche.leg2.get_legend().get_lines()):
                    if artist.contains(event)[0]:
                        self.edit_legend_2(i)
                        return

                # check du text de la légende 2
                for i, artist in enumerate(self.abstract_affiche.leg2.get_legend().get_texts()):
                    if artist.contains(event)[0]:
                        self.edit_legend_2(i)
                        return

    """---------------------------------------------------------------------------------"""

    def mouseMoveEvent(self, event):
        pass

    """---------------------------------------------------------------------------------"""

    def mousePressEvent(self, event):
        pass

    """---------------------------------------------------------------------------------"""

    def closeEvent(self, event):
        """
        Déclenché quand abstract_affiche.pplot_fig est fermé (pplot.close(abstract_affiche.pplot_fig))

        Déclenché quand la fenêtre contenant le plot est fermé pour le cas ou le widget est dans une
        fenêtre indépandante

        On check QtGui.QCloseEvent car on va close le graph ensuite ce qui va apeller la methode une nouvelle
        fois, on evite d'emit 2 fois, une fois par qtevent par qt et une seconde par CloseEvent de matplotlib

        :param event: QCloseEvent / CloseEvent
        :return: None
        """

        if type(event).__name__ == "QCloseEvent":
            self.closed.emit(self.abstract_affiche.figure.name)

    """---------------------------------------------------------------------------------"""

    def axes_enter_event(self, event):
        pass

    """---------------------------------------------------------------------------------"""

    def axes_leave_event(self, event):
        pass

    """---------------------------------------------------------------------------------"""

    def edit_x_axe(self):
        """
        fonction appellée pour editer l'axe des x

        :return: None
        """
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

    """---------------------------------------------------------------------------------"""

    def edit_y1_axe(self):
        """
        fonction appellée pour editer l'axe des y1

        :return: None
        """
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

    """---------------------------------------------------------------------------------"""

    def edit_y2_axe(self):
        """
        fonction appellée pour editer l'axe des y2

        :return: None
        """
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

    """---------------------------------------------------------------------------------"""

    def edit_suptitle(self):
        """
        fonction appellée pour editer le titre du graph

        :return: None
        """
        old_name = self.abstract_affiche.pplot_fig._suptitle.get_text()
        name = QInputDialog.getText(self, "Name change", "New name ?", QLineEdit.Normal, old_name)
        if name[1] and name[0] != "":
            self.abstract_affiche.pplot_fig._suptitle.set_text(name[0])
            self.abstract_affiche.figure.name = name[0]
            self.name_changed.emit([old_name, name[0]])
            self.canvas.draw()

    """---------------------------------------------------------------------------------"""

    def edit_legend_1(self, index):
        """
        fonction appellée pour editer les légendes 1

        :return: None
        """
        # on récupére le nom du la légende édité
        old_name = self.abstract_affiche.leg1.get_legend().get_texts()[index].get_text()
        # dialogue pour récupérer le nouveau nom
        name = QInputDialog.getText(self, "Name change", "New name ?", QLineEdit.Normal, old_name)
        # si ok est pressé et que le champ n'est pas vide
        if name[1] and name[0] != "":
            modulo_y1 = []
            nb_y1 = 0
            # on check le nombre de legende
            for data in self.abstract_affiche.figure.y1_axe.data:
                if data.legend is not None:
                    nb_y1 += 1
            # si ce nombre est supérieur au nombres de légendes affichées
            if nb_y1 > self.abstract_affiche.figure.nb_legende:
                # même algo que pour la création des légendes, pour récupérer l'index de data_array correspondant
                # à l'index de la légende affiché
                for j in range(self.abstract_affiche.figure.nb_legende):
                    temp = int(nb_y1 / self.abstract_affiche.figure.nb_legende * j)
                    if temp not in modulo_y1:
                        modulo_y1.append(temp)

                # update de l'affichage + de la figure
                self.abstract_affiche.figure.y1_axe.data[modulo_y1[index]].legend = name[0]
                self.abstract_affiche.leg1.get_legend().get_texts()[index].set_text(name[0])

            else:
                # rien besoin de faire ici, les légende affiché et celle de la figure correspondent
                # update de l'affichage + de la figure
                self.abstract_affiche.figure.y1_axe.data[index].legend = name[0]
                self.abstract_affiche.leg1.get_legend().get_texts()[index].set_text(name[0])

            self.canvas.draw()

    """---------------------------------------------------------------------------------"""

    def edit_legend_2(self, index):
        """
        fonction appellée pour editer les légendes 2

        :return: None
        """
        # on récupére le nom du la légende édité
        old_name = self.abstract_affiche.leg2.get_legend().get_texts()[index].get_text()
        # dialogue pour récupérer le nouveau nom
        name = QInputDialog.getText(self, "Name change", "New name ?", QLineEdit.Normal, old_name)
        # si ok est pressé et que le champ n'est pas vide
        if name[1] and name[0] != "":
            modulo_y2 = []
            nb_y2 = 0
            for data in self.abstract_affiche.figure.y1_axe.data:
                if data.legend is not None:
                    nb_y2 += 1
            # si ce nombre est supérieur au nombres de légendes affichées
            if nb_y2 > self.abstract_affiche.figure.nb_legende:
                # même algo que pour la création des légendes, pour récupérer l'index de data_array correspondant
                # à l'index de la légende affiché
                for j in range(self.abstract_affiche.figure.nb_legende):
                    temp = int(nb_y2 / self.abstract_affiche.figure.nb_legende * j)
                    if temp not in modulo_y2:
                        modulo_y2.append(temp)

                # update de l'affichage + de la figure
                self.abstract_affiche.figure.y2_axe.data[modulo_y2[index]].legend = name[0]
                self.abstract_affiche.leg2.get_legend().get_texts()[index].set_text(name[0])

            else:
                # rien besoin de faire ici, les légende affiché et celle de la figure correspondent
                # update de l'affichage + de la figure
                self.abstract_affiche.figure.y2_axe.data[index].legend = name[0]
                self.abstract_affiche.leg2.get_legend().get_texts()[index].set_text(name[0])

            self.canvas.draw()

    """---------------------------------------------------------------------------------"""

    def update_title_plot(self, name):
        """
        Methode appellé quand le nom d'une tab est changé, pour update le titre
        du plot en conséquance

        :param name: nom du nouveau plot a affiché
        :return:
        """
        self.abstract_affiche.pplot_fig.suptitle(name).set_picker(True)
        self.canvas.draw()

    """---------------------------------------------------------------------------------"""

    def edit_finishded(self, event):
        """
        Fonction callback de la fermuture de la fenêtre d'édition d'un axe

        :param event: closed / cancel / save
        :return:
        """

        # si les données de la fen^tre sont sauvegardées
        if event == "save":
            # on récupére le nouveau nom de l'axe
            new_name = self.edit_w.lineEdit_2.text()
            if new_name != "":
                # si l'axe édité de x
                if self.axe_edited == "x":
                    # on update le graph et la figure
                    self.abstract_affiche.figure.x_axe.name = new_name
                    self.abstract_affiche.ax1.xaxis.set_label_text(new_name)
                # si l'axe édité de y1
                elif self.axe_edited == "y1":
                    # on update le graph et la figure
                    self.abstract_affiche.figure.y1_axe.name = new_name
                    self.abstract_affiche.ax1.yaxis.set_label_text(new_name)
                # si l'axe édité de y2
                elif self.axe_edited == "y2":
                    # on update le graph et la figure
                    self.abstract_affiche.figure.y2_axe.name = new_name
                    self.abstract_affiche.ax2.yaxis.set_label_text(new_name)

            # nouvelles valeurs de début et fin d'axe
            new_start = self.edit_w.lineEdit_3.text()
            new_end = self.edit_w.lineEdit_4.text()

            # si new_start a été modifié
            if new_start != "":
                try:
                    # on check que c'est un nombre qui est donné
                    new_start = float(new_start)
                    # si l'axe édité de x
                    if self.axe_edited == "x":
                        # on update le graph et la figure
                        self.abstract_affiche.figure.x_axe.first_val = new_start
                        self.abstract_affiche.ax1.set_xlim(new_start, self.abstract_affiche.ax1.get_xlim()[1])
                        # si l'axe édité de y1
                    elif self.axe_edited == "y1":
                        # on update le graph et la figure
                        self.abstract_affiche.figure.y1_axe.first_val = new_start
                        self.abstract_affiche.ax1.set_ylim(new_start, self.abstract_affiche.ax1.get_ylim()[1])
                    # si l'axe édité de y2
                    elif self.axe_edited == "y2":
                        # on update le graph et la figure
                        self.abstract_affiche.figure.y2_axe.first_val = new_start
                        self.abstract_affiche.ax2.set_ylim(new_start, self.abstract_affiche.ax2.get_ylim()[1])
                except ValueError:
                    print("valeur invalide pour new_start")

            # si new_end a été modifié
            if new_end != "":
                try:
                    new_end = float(new_end)
                    if self.axe_edited == "x":
                        self.abstract_affiche.figure.x_axe.last_val = new_end
                        self.abstract_affiche.ax1.set_xlim(self.abstract_affiche.ax1.get_xlim()[0], new_end)
                    elif self.axe_edited == "y1":
                        self.abstract_affiche.figure.y1_axe.last_val = new_end
                        self.abstract_affiche.ax1.set_ylim(self.abstract_affiche.ax1.get_ylim()[0], new_end)
                    elif self.axe_edited == "y2":
                        self.abstract_affiche.figure.y2_axe.last_val = new_end
                        self.abstract_affiche.ax2.set_ylim(self.abstract_affiche.ax2.get_ylim()[0], new_end)
                except ValueError:
                    pass

            # On check le scale de l'axe indiqué
            new_scale = self.edit_w.comboBox_18.itemText(self.edit_w.comboBox_18.currentIndex())

            # on regarde si l'édition du scale de l'axe peut être effectué
            check = True

            if new_scale == "log":
                if self.axe_edited == "x":
                    if self.abstract_affiche.ax1.get_xlim()[0] < 0 or self.abstract_affiche.ax1.get_xlim()[1] < 0:
                        check = False

                elif self.axe_edited == "y1":
                    if self.abstract_affiche.ax1.get_ylim()[0] < 0 or self.abstract_affiche.ax1.get_ylim()[1] < 0:
                        check = False

                elif self.axe_edited == "y2":
                    if self.abstract_affiche.ax2.get_ylim()[0] < 0 or self.abstract_affiche.ax2.get_ylim()[1] < 0:
                        check = False

            # si check est respé a true on edit de scale
            if check:
                # si l'axe édité de x
                if self.axe_edited == "x":
                    # on update le graph et la figure
                    self.abstract_affiche.figure.x_axe.scale = new_scale
                    self.abstract_affiche.ax1.set_xscale(new_scale)
                # si l'axe édité de y1
                elif self.axe_edited == "y1":
                    # on update le graph et la figure
                    self.abstract_affiche.figure.y1_axe.scale = new_scale
                    self.abstract_affiche.ax1.set_yscale(new_scale)
                # si l'axe édité de y2
                elif self.axe_edited == "y2":
                    # on update le graph et la figure
                    self.abstract_affiche.figure.y2_axe.scale = new_scale
                    self.abstract_affiche.ax2.set_yscale(new_scale)

            self.canvas.draw()

        self.edit_w.deleteLater()
        self.edit_w = None
        self.axe_edited = None

    """---------------------------------------------------------------------------------"""

    def on_top(self):
        """
        On passe la fenêtre on top

        :return: None
        """
        self.activateWindow()

    """---------------------------------------------------------------------------------"""

    def on_back(self):
        """
        On passe la fenêtre en arière plan

        :return: None
        """
        self.lower()

    """---------------------------------------------------------------------------------"""

    def is_on_top(self):
        """
        On check si la fenêtre est active ou pas

        :return: bool
        """
        return self.isActiveWindow()

    """---------------------------------------------------------------------------------"""

    def focusInEvent(self, event):
        """
        Quand la fenêtre passe en focus il faut update current_figure, le tree et les label
        Un signal est envoyé quand c'est le cas

        :param event: focusInEvent de QT
        :return: None
        """
        self.focus_in.emit(self.abstract_affiche.figure.name)

    """---------------------------------------------------------------------------------"""

    def update_plot(self, axe, index, array_x, array_y):
        """
        On met à jours les data du plot avec les axes donnée en paramètre

        Pas de draw ici, il se fait par ailleurs

        :param axe: Nom de l'axe : y1, y2
        :param index: index d'édition
        :param array_x: nouvelle array_x
        :param array_y: nouvelle array_y
        :return: None
        """

        if axe == "y1":
            self.abstract_affiche.ax1.lines[index].set_xdata(array_x)
            self.abstract_affiche.ax1.lines[index].set_ydata(array_y)
        elif axe == "y2":
            self.abstract_affiche.ax2.lines[index].set_xdata(array_x)
            self.abstract_affiche.ax2.lines[index].set_ydata(array_y)

    def set_visibility_2d_line(self, axe, index, visibility):
        if axe == "y1":
            self.abstract_affiche.ax1.lines[index].set_visible(visibility)
        elif axe == "y2":
            self.abstract_affiche.ax2.lines[index].set_visible(visibility)


class Window(QMainWindow, Ui_MainWindow):
    def __init__(self, parent=None):
        super().__init__(parent)
        self.setupUi(self)

        # focus policy
        self.setFocusPolicy(QtCore.Qt.StrongFocus)

        # création de la console
        self.console = Console()

        # self.threads est de la forme : [thread, worker]
        self.threads = []

        # array contenant les figure ouvertes dans des fenêtre à part
        self.figure_w = []

        # objet qui sauvegarde le dernier état de QFileDialog pour la sauvegarde
        self.save_state_dialog = None

        # on connect un peu tout
        self.connectSignalsSlots()

        # on garde en mémoire la fénêtre d'édition du plot
        self.edit_plot_w = None

        # variable qui garde en mémoire l'objet Abstract_Affiche de la figure édité
        self.edit_plot_figure_w = None

        # on sauvegarde ici les résultats obtenue lors de l'édition d'un plot
        # de la forme : {index_x de l'édition : [data_x, data_y]}
        self.edit_plot_dics = {}

    """---------------------------------------------------------------------------------"""

    def connectSignalsSlots(self):
        """
        Connection des widget de la fenêtre principale

        :return: None
        """

        self.actioncccv.triggered.connect(self.open_cccv)
        self.actioncv.triggered.connect(self.open_cv)
        self.actiongitt.triggered.connect(self.open_gitt)
        self.actionEdit_Current_Plot.triggered.connect(self.edit_current_plot)
        self.pushButton_5.clicked.connect(self.create_current_data)
        self.pushButton_4.clicked.connect(self.create_current_figure)
        self.treeWidget.clicked.connect(self.tree_click)
        self.tabWidget.tabCloseRequested.connect(self.close_tab_handler)
        self.tabWidget.name_changed_tab.connect(self.name_changed_tab)
        self.tabWidget.break_tab.connect(self.break_tab)
        self.tabWidget.change_current.connect(self.tab_changed)

    """---------------------------------------------------------------------------------"""

    def open_cccv(self):
        """
        Gestion de l'ouverture d'une expérience de cccv
        Un thread est créée pour faire la lecture du fichier

        :return: None
        """

        # création de l'objet QFileDialog
        dialog = QFileDialog()

        # si il y a une sauvegarde d'état elle est utilisée
        if self.save_state_dialog is not None:
            dialog.restoreState(self.save_state_dialog)

        dialog.setWindowTitle('Open cccv File')
        dialog.setNameFilter('EC_lab file (*.mpt *.txt)')
        dialog.setFileMode(QFileDialog.ExistingFile)

        if dialog.exec_() == QDialog.Accepted:
            filename = dialog.selectedFiles()[0]
            filename = r"C:\Users\Maxime\Desktop\fichier_test\test.txt"

            # création d'un nouveau thread
            t = QThread()

            # création du worker
            worker = Threads_UI.Open_file_cccv(filename)
            worker.moveToThread(t)

            # connection
            t.started.connect(worker.run)
            worker.finished.connect(self.fin_thread_lecture)

            self.threads.append([t, worker])
            t.start()

            # on sauvegarde l'état de la fenêtre d'ouverture de fichiers
            self.save_state_dialog = dialog.saveState()

    """---------------------------------------------------------------------------------"""

    def open_cv(self):
        """
        je m'en sers comme affichage test pour le moment

        :return: None
        """

        fig = Figure("test", 1)
        fig.add_data_x_Data(Data_array([1, 2, 3], None, None, "None"))
        fig.add_data_y1_Data(Data_array([10, 5, 20], None, None, "None"))

        obj = Classique_affiche(self.console.current_data, fig)

        self.figure_plot = Figure_plot(obj)
        self.figure_plot.show()

    """---------------------------------------------------------------------------------"""

    def open_gitt(self):
        """
        je m'en sers comme affichage test pour le moment

        :return: None
        """

        """print("current data : " + self.console.current_data.name)
        print("current figure : " + self.console.current_data.current_figure.name)"""

        f1 = Figure("f1")
        f2 = Figure("f2")
        f3 = Figure("f3")
        f4 = Figure("f4")
        f5 = Figure("f5")
        f6 = Figure("f6")
        f7 = Figure("f7")
        f8 = Figure("f8")
        f9 = Figure("f9")

        f2.created_from = f1
        f3.created_from = f2
        f4.created_from = f3
        f5.created_from = f4

        f8.created_from = f2

        self.treeWidget.add_data("cccv", "cccv1")

        self.treeWidget.add_figure(f1, "cccv1")
        self.treeWidget.add_figure(f2, "cccv1")
        self.treeWidget.add_figure(f3, "cccv1")
        self.treeWidget.add_figure(f4, "cccv1")
        self.treeWidget.add_figure(f5, "cccv1")
        self.treeWidget.add_figure(f6, "cccv1")
        self.treeWidget.add_figure(f7, "cccv1")
        self.treeWidget.add_figure(f8, "cccv1")
        self.treeWidget.add_figure(f9, "cccv1")

        print("-----------------")
        self.treeWidget.info()
        print("-----------------")

    """---------------------------------------------------------------------------------"""

    def edit_current_plot(self):
        """

        :return: None
        """
        if self.console.current_data is None:
            self.current_data_None()
        elif self.console.current_data.current_figure is None:
            self.current_figure_None()
        else:
            self.edit_plot_w = Edit_plot()

            self.edit_plot_w.label.setText(self.console.current_data.current_figure.name)

            for i, data_array in enumerate(self.console.current_data.current_figure.y1_axe.data):
                self.edit_plot_w.listWidget.addItem(data_array.legend)
                if not data_array.visible:
                    self.edit_plot_w.listWidget.item(i).setForeground(QColor("red"))

            if self.console.current_data.current_figure.y2_axe is not None:
                for i, data_array in enumerate(self.console.current_data.current_figure.y2_axe.data):
                    self.edit_plot_w.listWidget.addItem(data_array.legend)
                    if not data_array.visible:
                        self.edit_plot_w.listWidget.item(i).setForeground(QColor("red"))


            self.edit_plot_w.lineEdit.setText(self.console.current_data.current_figure.name)
            self.edit_plot_w.lineEdit_2.setText(str(self.console.current_data.current_figure.zoom))

            for color in Resources.COLOR_MAP.keys():
                self.edit_plot_w.comboBox.addItem(color)

            self.edit_plot_w.finish_signal.connect(self.res_edit_plot)
            self.edit_plot_w.edit_signal.connect(self.create_edit_plot)

            self.edit_plot_w.show()

    """---------------------------------------------------------------------------------"""

    def create_current_data(self):
        """
        Methode appellé par le button create de current data (new plot)
        on fonction du type d'expérience les item de comboBox_5 seront
        différent. L'applle de la création des figures se fait ici, on
        récupére les figures dans un vecteur


        :return: None
        """
        if self.console.current_data is None:
            # si current_data is None on affiche un fenêtre d'erreur
            self.current_data_None()
        else:
            # capa
            if self.comboBox_5.currentText() == "capa":
                # on apelle la fonction pour créer les figures et les récupére, c'est un vecteur
                figures_res = self.console.current_data.capa()

                # on parcours le vecteur, update tree widget ave le nom des figure créées
                # on ajoute les figure a current_data
                for figure in reversed(figures_res):
                    self.treeWidget.add_figure(figure, self.console.current_data.name)
                    self.console.current_data.figures.append(figure)

            # potentio
            elif self.comboBox_5.currentText() == "potentio":
                # on apelle la fonction pour créer les figures et les récupére, c'est une figure seul
                figures_res = self.console.current_data.potentio()

                # on update le tree widget
                # on ajoute la figure a current_data
                self.treeWidget.add_figure(figures_res, self.console.current_data.name)
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
        Déclenché quand item l'utilisateur clique sur un item du tree widget

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
        Déclenché à la suite de la fin de l'execution d'un thread de lecture
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
                        self.treeWidget.add_data("cccv", obj_data.name)

                    # on récupére les actions disponibles pour ce type de fichier pour update
                    # current data comboBox_5
                    self.comboBox_5.clear()
                    for action in self.console.current_data.get_operation_available():
                        self.comboBox_5.addItem(action)

                # on termine le thread
                self.threads[index][0].terminate()

                # on le suprime de la liste
                del self.threads[index]
            else:
                index += 1

    """---------------------------------------------------------------------------------"""

    def name_changed_tab(self, signal):
        """
        Déclenchée quand le nom d'une tab est changée
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
        Déclenchée quand le nom du plot est changé, on update le nom
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
        Déclenché si une fenêtre plot passe en focus
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
        Déclenché quand le nom du plot est modifiée sur une
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

        if parent is None:
            return

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

        Si aucune tab n'est présente lors du focus aucune erreur est déclenchée, le nom
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

    def res_edit_plot(self, signal):
        if signal == "cancel":
            self.edit_plot_w.deleteLater()
            self.edit_plot_w = None
        elif signal == "save":
            if len(self.edit_plot_dics) == 0:
                obj_figure_plot = None
            else:
                obj_figure_plot = self.process_del_point_plot()

            obj_figure_plot = self.hide_data_array(obj_figure_plot)
            obj_figure_plot.canvas.draw()

            self.edit_plot_dics.clear()
            self.edit_plot_w.deleteLater()
            self.edit_plot_w = None

    """---------------------------------------------------------------------------------"""

    def create_edit_plot(self, signal):
        """
        On créer la figure qui servira a sélectionner les points a supprimer
        Cette figure correspondra à un cycle de current_figure

        :param signal: current_index de la listWidget
        :return: None
        """
        # si une figure d'édition est déjà ouverte, ou return
        # un message a ajouter ici par la suite
        if self.edit_plot_figure_w is not None:
            return

        # création d'une nouvelle figure avec pour nom la légende du cycle sélectionné
        new_figure = Figure(self.edit_plot_w.listWidget.currentItem().text(), 1)

        # on ajoute à la nouvelle figure interactive une copie de data_x correspondant à l'index sélectionné
        new_figure.add_data_x_Data(copy.copy(self.console.current_data.current_figure.x_axe.data[signal]))

        # on ajoute à la nouvelle figure interactive une copie de data_y correspondant à l'index sélectionné
        # on utilise get_data_yaxe_i pour récupérer data_array, qu'il soit en y1 ou y2 en fonction de l'index
        data_y1 = copy.copy(self.console.current_data.current_figure.get_data_yaxe_i(signal))

        # si array_data n'a pas de couleur, c'est la couleur de maptplotlib par défault qu'il prends, donc
        # on prends la même pour garde une cohérence des couleurs
        if data_y1.color is None:
            list_c = matplotlib.rcParams["axes.prop_cycle"].by_key()['color']
            while len(list_c) <= signal:
                signal -= len(list_c)

            data_y1.color = list_c[signal]

        # on ajoute data_y1 comme data y1 à la nouvelle figure
        new_figure.add_data_y1_Data(data_y1)

        # on passe la ligne est point pour faciliter la supression de ces derniers
        if new_figure.format_line_y1 is None or new_figure.format_line_y1 == "-":
            new_figure.format_line_y1 = "x"

        # on créer un obj Edit_affiche, fille de Abstract_objet_affiche servant à l'édition de points
        edit_affiche = Edit_affiche(self.console.current_data, new_figure)

        # on garde une ref de l'objet créée
        self.edit_plot_figure_w = Figure_plot(edit_affiche)

        # on connect de callback, on utilise lambda pour passer signal comme arg suplémentaire
        self.edit_plot_figure_w.closed.connect(lambda event: self.edit_plot_figure_w_close(event, signal))

        # on affiche le widget
        self.edit_plot_figure_w.show()

    """---------------------------------------------------------------------------------"""

    def edit_plot_figure_w_close(self, event, index):
        """
        Methode callback de create_edit_plot pour la fermeture du plot
        d'édition
        On sauvegarde dans un dictionnaire les résultats obtenue lors de l'édition du plot

        :param event: nom de la figure qui est close
        :param index: index du cycle qui a été édité
        :return: None
        """
        new_data_x = self.edit_plot_figure_w.abstract_affiche.figure.x_axe.data[0].data
        new_data_y = self.edit_plot_figure_w.abstract_affiche.figure.y1_axe.data[0].data

        self.edit_plot_dics[index] = [new_data_x, new_data_y]

    """---------------------------------------------------------------------------------"""

    def process_del_point_plot(self):
        """
        Effectue la mise à jours des figures et des plots correspondant aux éditions effectuées

        :return: l'objet Figure_plot qui correspond à la figure courrante
        """

        obj_figure_plot = None

        # key : x_index de l'édition
        # value : [new_datax, new_datay]
        for key, value, in self.edit_plot_dics.items():

            # si l'index est plus grand que le nombre de data dans y1_axe, c'est un index pour
            # l'axe y2
            if key >= len(self.console.current_data.current_figure.y1_axe.data):
                # on calcule l'index pour l'axe y2
                y2_index = key - len(self.console.current_data.current_figure.y1_axe.data)

                # on update current_figure avec les valeurs de value
                self.console.current_data.current_figure.x_axe.data[key].data = value[0]
                self.console.current_data.current_figure.y2_axe.data[y2_index].data = value[1]

                name_figure = self.console.current_data.current_figure.name

                # on garde en mémoire si on a update
                done = False
                for obj_figure_w in self.figure_w:
                    # on cherche si la figure mise à jours est dans un fenêtre
                    if obj_figure_w.abstract_affiche.figure.name == name_figure:
                        # si oui on la met à jours
                        obj_figure_w.update_plot("y2", key, value[0], value[1])
                        obj_figure_plot = obj_figure_w
                        done = True
                        break

                if not done:
                    # la figure n'était pas dans une fenêtre
                    for i in range(self.tabWidget.count()):
                        # on cherche dans les tabs
                        if self.tabWidget.tabText(i) == name_figure:
                            # on la met à jours
                            self.tabWidget.widget(i).update_plot("y2", key, value[0], value[1])
                            obj_figure_plot = self.tabWidget.widget(i)
                            break
            else:
                # on update current_figure avec les valeurs de value
                self.console.current_data.current_figure.x_axe.data[key].data = value[0]
                self.console.current_data.current_figure.y1_axe.data[key].data = value[1]

                name_figure = self.console.current_data.current_figure.name

                # on garde en mémoire si on a update
                done = False
                for obj_figure_w in self.figure_w:
                    # on cherche si la figure mise à jours est dans un fenêtre
                    if obj_figure_w.abstract_affiche.figure.name == name_figure:
                        # si oui on la met à jours
                        obj_figure_w.update_plot("y1", key, value[0], value[1])
                        obj_figure_plot = obj_figure_w
                        done = True
                        break

                if not done:
                    # la figure n'était pas dans une fenêtre
                    for i in range(self.tabWidget.count()):
                        # on cherche dans les tabs
                        if self.tabWidget.tabText(i) == name_figure:
                            # on la met à jours
                            self.tabWidget.widget(i).update_plot("y1", key, value[0], value[1])
                            obj_figure_plot = self.tabWidget.widget(i)
                            break

        return obj_figure_plot

    """---------------------------------------------------------------------------------"""

    def hide_data_array(self, obj_figure_plot):
        if obj_figure_plot is None:
            current_name = self.console.current_data.current_figure.name

            done = False
            for obj_figure_w in self.figure_w:
                # on cherche si la figure mise à jours est dans un fenêtre
                if obj_figure_w.abstract_affiche.figure.name == current_name:
                    obj_figure_plot = obj_figure_w
                    done = True
                    break

            if not done:
                # la figure n'était pas dans une fenêtre
                for i in range(self.tabWidget.count()):
                    # on cherche dans les tabs
                    if self.tabWidget.tabText(i) == current_name:
                        # on la met à jours
                        obj_figure_plot = self.tabWidget.widget(i)
                        break

        # on update current figure pour passer en hide les éléments indiqué
        for i in range(self.edit_plot_w.listWidget.count()):
            if self.edit_plot_w.listWidget.item(i).foreground().color() == QColor("red"):
                self.console.current_data.current_figure.get_data_yaxe_i(i).visible = False
                self.console.current_data.current_figure.x_axe.data[i].visible = False

                if i >= len(self.console.current_data.current_figure.y1_axe.data):
                    index = i - len(self.console.current_data.current_figure.y1_axe.data)
                    obj_figure_plot.set_visibility_2d_line("y2", index, False)
                else:
                    index = i
                    obj_figure_plot.set_visibility_2d_line("y1", index, False)
            else:
                self.console.current_data.current_figure.get_data_yaxe_i(i).visible = True
                self.console.current_data.current_figure.x_axe.data[i].visible = True

                if i >= len(self.console.current_data.current_figure.y1_axe.data):
                    index = i - len(self.console.current_data.current_figure.y1_axe.data)
                    obj_figure_plot.set_visibility_2d_line("y2", index, True)
                else:
                    index = i
                    obj_figure_plot.set_visibility_2d_line("y1", index, True)

        return obj_figure_plot


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
