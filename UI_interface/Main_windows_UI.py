import copy
import math
import sys

import matplotlib

from PyQt5 import QtCore, QtWidgets
from PyQt5.QtCore import QThread
from PyQt5.QtGui import QColor, QFont, QTextCursor
from PyQt5.QtWidgets import (
    QApplication, QDialog, QMainWindow, QMessageBox, QFileDialog
)

import matplotlib.pyplot as pplot

from Console_Objets.Affiche_objet import Classique_affiche, Edit_affiche, Pic_selection, Gitt_affiche, Impedance_affiche
from Console_Objets.Console import Console
from Console_Objets.Data_Unit import Data_unit, Units
from Console_Objets.Data_array import Data_array
from Console_Objets.Figure import Figure
from Data_type import Abstract_data
from Data_type.CCCV_data import CCCV_data
from Data_type.Diffraction_data import Diffraction_data
from Data_type.Gitt_data import Gitt_data
from Data_type.Ihch_1501 import Ihch_1501
from Data_type.Impedance_data import Impedance_data
from Data_type.Traitement_cycle import Traitements_cycle_outils
from Math.Fitting import Fitting
from Resources_file import Resources
from Resources_file.Emit import Emit
from UI_interface import Threads_UI
from UI_interface.Ask_Value_QT import Ask_Value
from UI_interface.Create_figure import Create_figure
from UI_interface.Create_figure_ihch_1501 import Create_figure_ihch_1501
from UI_interface.Create_gitt import Create_gitt
from UI_interface.Cycle_selection_creation import Cycle_selection_creation
from UI_interface.Derive_Selection_QT import Derive_Selection
from UI_interface.Edit_data import Edit_data
from UI_interface.Edit_plot_contour import Edit_plot_contour
from UI_interface.Figure_plot_QT import Figure_plot
from UI_interface.Main_window_QT import Ui_MainWindow
from UI_interface.Edit_view_data_QT import Edit_view_data
from UI_interface.Cycle_Selection_QT import Cycle_Selection
from UI_interface.Edit_plot_QT import Edit_plot
from UI_interface.Selection_combo import Selection_combo

"""----------------------------------------------------------------------------------"""
"""                                   Main window                                    """
"""----------------------------------------------------------------------------------"""


class Window(QMainWindow, Ui_MainWindow):
    def __init__(self, parent=None):
        super().__init__(parent)
        self.setupUi(self)

        # focus policy
        self.setFocusPolicy(QtCore.Qt.StrongFocus)

        # création de la console
        self.console = Console()

        # on créer une instance de resource
        self.emit = Emit()

        self.resource = Resources.Resource_class()

        # self.threads est de la forme : [thread, worker]
        self.threads = []

        # array contenant les figure ouvertes dans des fenêtre à part
        self.figure_w = []

        # objet qui sauvegarde le dernier état de QFileDialog pour la sauvegarde
        self.save_state_dialog = None

        # on connect un peu tout
        self.connectSignalsSlots()

        # garde en mémoire la figure édité
        self.figure_edited = None

        # on garde en mémoire la fénêtre d'édition du plot
        self.edit_plot_w = None

        # variable qui garde en mémoire l'objet Abstract_Affiche de la figure édité
        self.edit_plot_figure_w = None

        # on garde obj_plot quand on a commencé
        self.obj_plot_show_value = None

        # fenêtre de sélection des valeurs a afficher
        self.select_value_show_w = None

        # fenêtre de selection des argument du nouveau plot
        self.argument_selection_creation_w = None

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
        self.actiondiffracion.triggered.connect(self.open_diffraction)
        self.actionIhch_1501.triggered.connect(self.open_ihch_1501)
        self.actionimpedance.triggered.connect(self.open_impedance)

        self.actionEdit_Current_Plot.triggered.connect(self.edit_current_plot)
        self.actionview_data_Current_Plot.triggered.connect(self.view_data_Current_Plot)
        self.actionDelete_Current_Plot.triggered.connect(self.delet_current_plot)
        self.export_actionPlot.triggered.connect(self.export_plot)
        self.actionEdit_data.triggered.connect(self.edit_data)

        self.pushButton_5.clicked.connect(self.create_current_data)
        self.pushButton_4.clicked.connect(self.create_figure)
        self.treeWidget.clicked.connect(self.tree_click)
        self.tabWidget.tabCloseRequested.connect(self.close_tab_handler)
        self.tabWidget.name_changed_tab.connect(self.name_changed_tab)
        self.tabWidget.break_tab.connect(self.break_tab)
        self.tabWidget.change_current.connect(self.tab_changed)

        self.console_txt._input.connect(self.process_input_console_txt)

        # sert pour faire passer des signaux pour l'affichage de text dans la zone par n'importe
        # quel class, en j'en suis très fière :)
        self.emit.connect("msg_console", self.message_console)

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
            # filename = r"C:\Users\Maxime\Desktop\fichier_test\test.txt"

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

        """fig = Figure("test", 1)
        fig.add_data_x_Data(Data_array([1, 2, 3], None, None, "None"))
        fig.add_data_y1_Data(Data_array([10, 5, 20], None, None, "None"))

        obj = Classique_affiche(self.console.current_data, fig)

        self.figure_plot = Figure_plot(obj, self)
        self.figure_plot.show()"""
        print(self.threads)
        self.console.current_data.get_info_data()

    """---------------------------------------------------------------------------------"""

    def open_gitt(self):
        """
        Gestion de l'ouverture d'une expérience de gitt
        Un thread est créée pour faire la lecture des 3 fichiers

        :return: None
        """
        files = []

        dialog = QFileDialog(self)
        # si il y a une sauvegarde d'état elle est utilisée
        if self.save_state_dialog is not None:
            dialog.restoreState(self.save_state_dialog)

        dialog.setWindowTitle('Open potentiel file')
        dialog.setNameFilter('EC_lab file (*.mpt *.txt)')

        if dialog.exec_() == QDialog.Accepted:
            files.append(dialog.selectedFiles()[0])
            # on sauvegarde l'état de la fenêtre d'ouverture de fichiers
            self.save_state_dialog = dialog.saveState()
        else:
            return

        # on sauvegarde l'état de la fenêtre d'ouverture de fichiers
        self.save_state_dialog = dialog.saveState()
        # dialog.destroy()

        # dialog = QFileDialog()

        # si il y a une sauvegarde d'état elle est utilisée
        if self.save_state_dialog is not None:
            dialog.restoreState(self.save_state_dialog)

        dialog.setWindowTitle('Open pulse file')
        dialog.setNameFilter('EC_lab file (*.mpt *.txt)')

        if dialog.exec_() == QDialog.Accepted:
            files.append(dialog.selectedFiles()[0])
            # on sauvegarde l'état de la fenêtre d'ouverture de fichiers
            self.save_state_dialog = dialog.saveState()
        else:
            return

        # on sauvegarde l'état de la fenêtre d'ouverture de fichiers
        self.save_state_dialog = dialog.saveState()
        # dialog.destroy()

        # dialog = QFileDialog()

        # si il y a une sauvegarde d'état elle est utilisée
        if self.save_state_dialog is not None:
            dialog.restoreState(self.save_state_dialog)

        dialog.setWindowTitle('Open relaxation file')
        dialog.setNameFilter('EC_lab file (*.mpt *.txt)')

        if dialog.exec_() == QDialog.Accepted:
            files.append(dialog.selectedFiles()[0])
            # on sauvegarde l'état de la fenêtre d'ouverture de fichiers
            self.save_state_dialog = dialog.saveState()
        else:
            return

        # création d'un nouveau thread
        t = QThread()

        # création du worker
        worker = Threads_UI.Open_file_gitt(files)
        worker.moveToThread(t)

        # connection
        t.started.connect(worker.run)
        worker.finished.connect(self.fin_thread_lecture)

        self.threads.append([t, worker])
        t.start()

    """---------------------------------------------------------------------------------"""

    def open_diffraction(self):
        # création de l'objet QFileDialog
        dialog = QFileDialog()
        # si il y a une sauvegarde d'état elle est utilisée
        if self.save_state_dialog is not None:
            dialog.restoreState(self.save_state_dialog)

        dialog.setWindowTitle('Open diffraction folder')
        dialog.setFileMode(QFileDialog.DirectoryOnly)

        if dialog.exec_() == QDialog.Accepted:
            folder_name = dialog.selectedFiles()[0]
            folder_name = r"C:\Users\Maxime\Desktop\diffraction_test"

            # création d'un nouveau thread
            t = QThread()

            # création du worker
            worker = Threads_UI.Open_file_diffraction(folder_name)
            worker.moveToThread(t)

            # connection
            t.started.connect(worker.run)
            worker.finished.connect(self.fin_thread_lecture)

            self.threads.append([t, worker])
            t.start()

            # on sauvegarde l'état de la fenêtre d'ouverture de fichiers
            self.save_state_dialog = dialog.saveState()

    """---------------------------------------------------------------------------------"""

    def open_ihch_1501(self):
        # création de l'objet QFileDialog
        dialog = QFileDialog()
        # si il y a une sauvegarde d'état elle est utilisée
        if self.save_state_dialog is not None:
            dialog.restoreState(self.save_state_dialog)

        dialog.setWindowTitle('Open ihch folder')
        dialog.setFileMode(QFileDialog.DirectoryOnly)

        if dialog.exec_() == QDialog.Accepted:
            folder_name = dialog.selectedFiles()[0]
            folder_name = r"C:\Users\Maxime\Desktop\Diffraction_Marta - Copie"

            # création d'un nouveau thread
            t = QThread()

            # création du worker
            worker = Threads_UI.Open_file_ihch_1501(folder_name)
            worker.moveToThread(t)

            # connection
            t.started.connect(worker.run)
            worker.finished.connect(self.fin_thread_lecture)

            self.threads.append([t, worker])
            t.start()

            # on sauvegarde l'état de la fenêtre d'ouverture de fichiers
            self.save_state_dialog = dialog.saveState()

    """---------------------------------------------------------------------------------"""

    def open_ihch_time(self, root_dir, nb_cycle):
        """

        :param root_dir: path du dossier contenant l'exp
        :param nb_cycle: nombre de cycle et donc de fichier ec_lac a ouvrir
        :return: None
        """
        # création de l'objet QFileDialog
        dialog = QFileDialog()

        dialog.setWindowTitle('Open cccv File')
        dialog.setNameFilter('EC_lab file (*.mpt *.txt)')
        dialog.setFileMode(QFileDialog.ExistingFile)

        paths_files = []
        for i in range(nb_cycle):
            if dialog.exec_() == QDialog.Accepted:
                paths_files.append(dialog.selectedFiles()[0])
            else:
                # dans le cas ou la fenêtre est fermée on return juste
                return

        # création d'un nouveau thread
        t = QThread()

        # création du worker
        worker = Threads_UI.Open_file_ihch_1501(root_dir, paths_files)
        worker.moveToThread(t)

        # connection
        t.started.connect(worker.run)
        worker.finished.connect(self.fin_lecteur_ihch_time)

        self.threads.append([t, worker])
        t.start()

        # on sauvegarde l'état de la fenêtre d'ouverture de fichiers
        self.save_state_dialog = dialog.saveState()

    """---------------------------------------------------------------------------------"""

    def fin_lecteur_ihch_time(self, event):
        """
        callback de la fonction open_ihch_time

        :param event: 0 : ok, -1: fail, -2: fail time creation, -3: fail avec création du temps
        :return: None
        """
        index = 0
        while index < len(self.threads):
            if type(self.threads[index][1]).__name__ == "Open_file_ihch_1501" and self.threads[index][1].finish:
                if event == [-1]:
                    # on termine le thread
                    self.threads[index][0].terminate()

                    # on le suprime de la liste
                    del self.threads[index]

                    self.fichier_invalide_error()
                elif event == [-2]:
                    # on termine le thread
                    self.threads[index][0].terminate()

                    # on le suprime de la liste
                    del self.threads[index]

                    self.QMessageBox_str("Error durring the creation of time")
                elif event == [-3]:
                    # on termine le thread
                    self.threads[index][0].terminate()

                    # on le suprime de la liste
                    del self.threads[index]

                    self.QMessageBox_str("Unable to process the data")
                elif event == [1]:
                    # on créer un objet data cccv
                    obj_data = Ihch_1501()

                    # on lui ajoute les data lu par le thread
                    obj_data.cycles = self.threads[index][1].data

                    # créer son nom
                    obj_data.name = "ihch A MODIFIER"

                    # on ajoute l'objet data à la console
                    self.console.add_data(obj_data)

                    # on update le tree widget
                    self.treeWidget.add_data("ihch 1501", obj_data.name)

                    # on update current data avec ne nom du nouveau fichier
                    _translate = QtCore.QCoreApplication.translate
                    self.label.setText(
                        _translate("MainWindow", "<html><head/><body><p><span style=\" font-size:11pt;\">"
                                                 "Current data : "
                                   + obj_data.name + " </span></p></body></html>"))

                    self.update_console({"str": "Done", "foreground_color": "green"})

                    # on récupére les actions disponibles pour ce type de fichier pour update
                    # current data comboBox_5
                    self.update_new_plot_combo()

                    # on termine le thread
                    self.threads[index][0].terminate()

                    # on le suprime de la liste
                    del self.threads[index]
                break

            else:
                index += 1

    """---------------------------------------------------------------------------------"""

    def open_impedance(self):
        """
        Gestion de l'ouverture d'une expérience d'impedance
        Un thread est créée pour faire la lecture du fichier

        :return: None
        """

        # création de l'objet QFileDialog
        dialog = QFileDialog()

        # si il y a une sauvegarde d'état elle est utilisée
        if self.save_state_dialog is not None:
            dialog.restoreState(self.save_state_dialog)

        dialog.setWindowTitle('Open impedance File')
        dialog.setNameFilter('EC_lab file (*.mpt *.txt)')
        dialog.setFileMode(QFileDialog.ExistingFile)

        if dialog.exec_() == QDialog.Accepted:
            filename = dialog.selectedFiles()[0]
            filename = r"C:\Users\Maxime\Desktop\fichier_test\adrien_impedance.mpt"

            # création d'un nouveau thread
            t = QThread()

            # création du worker
            worker = Threads_UI.Open_file_impedance(filename)
            worker.moveToThread(t)

            # connection
            t.started.connect(worker.run)
            worker.finished.connect(self.fin_thread_lecture)

            self.threads.append([t, worker])
            t.start()

            # on sauvegarde l'état de la fenêtre d'ouverture de fichiers
            self.save_state_dialog = dialog.saveState()

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
            if self.argument_selection_creation_w is not None:
                self.argument_selection_creation_w.deleteLater()
                self.argument_selection_creation_w = None

            # capa
            if self.comboBox_5.currentText() == "capa":
                if self.console.current_data.data["mass_electrode"] == -1:
                    self.argument_selection_creation_w = Ask_Value(self, "float", "Invalide mass Electode",
                                                                   "New Mass (mg) : ")
                    self.argument_selection_creation_w.finish_signal.connect(
                        lambda signal: self.callback_create_current_data(signal, "capa"))

                    self.argument_selection_creation_w.show()
                else:
                    # pas d'utilisation de callback ici, il n'y a pas d'argument à récupérer
                    self.callback_create_current_data({"rep": "save"}, "capa")

            # potentio
            elif self.comboBox_5.currentText() == "potentio":
                self.argument_selection_creation_w = Cycle_Selection(self)
                self.argument_selection_creation_w.finish_signal.connect(
                    lambda signal: self.callback_create_current_data(signal, "potentio"))
                self.argument_selection_creation_w.show()


            elif self.comboBox_5.currentText() == "custom":
                self.argument_selection_creation_w = Create_figure(self)
                self.argument_selection_creation_w.finish_signal.connect(
                    lambda signal: self.callback_create_current_data(signal, "custom"))
                # on ajoute le nom de toute les ligne récupéré dans le fichier ec_lab

                max_size = 0
                index = 0
                name_current_data = self.console.current_data.__name__
                for data in self.console.datas:
                    if data.__name__ == name_current_data:
                        for row_name in data.data["row_data"]:
                            self.argument_selection_creation_w.listWidget.addItem(data.name + "\t" + row_name)
                            self.argument_selection_creation_w.listWidget_3.addItem(data.name + "\t" + row_name)
                            self.argument_selection_creation_w.listWidget_4.addItem(data.name + "\t" + row_name)
                            max_size = max(max_size,
                                           self.argument_selection_creation_w.listWidget.sizeHintForRow(index),
                                           self.argument_selection_creation_w.listWidget_3.sizeHintForRow(index),
                                           self.argument_selection_creation_w.listWidget_4.sizeHintForRow(index))
                            index += 1
                self.argument_selection_creation_w.resize(max_size * 10 + 100, 400)
                self.argument_selection_creation_w.show()

            elif self.comboBox_5.currentText() == "Diffraction":
                self.callback_create_current_data("save", "Diffraction")

            elif self.comboBox_5.currentText() == "Contour":
                self.callback_create_current_data("save", "Contour")

            elif self.comboBox_5.currentText() == "Ihch 1501 plot":

                # on est sur un ihch 1501, donc pas de data ici, mais cycles
                self.argument_selection_creation_w = Create_figure_ihch_1501(self, self.console.current_data.cycles)

                self.argument_selection_creation_w.finish_signal.connect(
                    lambda signal: self.callback_create_current_data(signal, "Ihch 1501 plot"))
                self.argument_selection_creation_w.show()

            elif self.comboBox_5.currentText() == "Create gitt":
                self.argument_selection_creation_w = Create_gitt(self)
                self.argument_selection_creation_w.finish_signal.connect(
                    lambda signal: self.callback_create_current_data(signal, "Create gitt"))
                self.argument_selection_creation_w.show()

            elif self.comboBox_5.currentText() == "Impedance":
                self.callback_create_current_data("save", "Impedance")

            elif self.comboBox_5.currentText() == "Resistance":
                self.argument_selection_creation_w = Ask_Value(self, "int", "Cycle selection",
                                                               "Cycle : ")
                self.argument_selection_creation_w.finish_signal.connect(
                    lambda signal: self.callback_create_current_data(signal, "Resistance"))

                self.argument_selection_creation_w.show()

            elif self.comboBox_5.currentText() == "Bode":
                self.callback_create_current_data("save", "Bode")

            elif self.comboBox_5.currentText() == "3d":
                self.argument_selection_creation_w = Selection_combo(self, "Value used for the z-axis?", ["time", "potentiel"])

                self.argument_selection_creation_w.finish_signal.connect(
                    lambda signal: self.callback_create_current_data(signal, "3d"))

                self.argument_selection_creation_w.show()


    """---------------------------------------------------------------------------------"""

    def callback_create_current_data(self, event, name):
        """
        Fonction callback de create_current_data

        :param event: save / cancel
        :param name: capa / potentio / custom ...
        :return: None
        """

        # si l'oppéraion est cancel on reset la fenêtre et return
        if event == "cancel":
            if self.argument_selection_creation_w is not None:
                self.argument_selection_creation_w.deleteLater()
                self.argument_selection_creation_w = None
        else:
            if name == "capa":
                # si argument_selection_creation_w is not None c'est que la mass de l'électrode n'était pas connue
                # on l'a met à jour
                if self.argument_selection_creation_w is not None:
                    self.console.current_data.data["mass_electrode"] = self.argument_selection_creation_w.value

                    # on a récupérer les info, on délect la fenêtre
                    self.argument_selection_creation_w.deleteLater()
                    self.argument_selection_creation_w = None

                self.update_console({"str": str(self.console.current_data.data["mass_electrode"]) +
                                            " mg will be use as for the mass of the  electrode ",
                                     "foreground_color": "yellow"})

                # on apelle la fonction pour créer les figures et les récupére, c'est un vecteur
                figures_res = self.console.current_data.capa()

                # on parcours le vecteur, update tree widget ave le nom des figure créées
                # on ajoute les figure a current_data
                for figure in reversed(figures_res):
                    self.treeWidget.add_figure(figure, self.console.current_data.name)
                    self.console.current_data.figures.append(figure)

                self.console.current_data.current_figure = self.console.current_data.figures[-1]

            # potentio
            elif name == "potentio":
                # info de self.argument_selection_creation_w a récupérer ici pour créer la figure
                cycles = self.argument_selection_creation_w.cycles

                # on a récupérer les info, on délect la fenêtre
                self.argument_selection_creation_w.deleteLater()
                self.argument_selection_creation_w = None

                # on apelle la fonction pour créer les figures et les récupére, c'est une figure seul
                figure_res = self.console.current_data.potentio(cycles)

                # la figure n'a pas été créée, on return juste
                if figure_res is None:
                    return

                # on update le tree widget
                # on ajoute la figure a current_data
                self.treeWidget.add_figure(figure_res, self.console.current_data.name)
                self.console.current_data.figures.append(figure_res)

                # on passe la figure en figure courante
                self.console.current_data.current_figure = figure_res

            elif name == "custom":
                # on récupére la sélection de la fenêtre de création
                x_items = self.argument_selection_creation_w.x_items
                scale_x = self.argument_selection_creation_w.comboBox_21.currentText()

                y1_items = self.argument_selection_creation_w.y1_items
                scale_y1 = self.argument_selection_creation_w.comboBox_19.currentText()

                y2_items = self.argument_selection_creation_w.y2_items
                scale_y2 = self.argument_selection_creation_w.comboBox_22.currentText()

                name = self.argument_selection_creation_w.lineEdit.text()

                name = self.console.current_data.unique_name(name)

                # on a récupérer les info, on délect la fenêtre
                self.argument_selection_creation_w.deleteLater()
                self.argument_selection_creation_w = None

                # on créer une nouvelle figure
                figure = Figure(name)

                # on ajoute les données correspondantes aux sélections
                res = x_items[0].split("\t")

                for i in range(len(y1_items) + len(y2_items)):
                    data_unit = self.console.create_data_unit(res[0], res[1])
                    data_array_x = Data_array(data_unit, res[1], res[0], res[1])
                    data_array_x.global_index = [index for index in range(len(data_unit.data))]

                    figure.add_data_x_Data(data_array_x)

                # on ajoute pour y1
                for i in range(len(y1_items)):
                    res = y1_items[i].split("\t")
                    data_unit = self.console.create_data_unit(res[0], res[1])
                    data_array_y1 = Data_array(data_unit, res[1], res[0], res[1])
                    # data_array_y1.global_index = [index for index in range(len(data_unit.data))]

                    figure.add_data_y1_Data(data_array_y1)

                # on ajoute pour y2
                for i in range(len(y2_items)):
                    res = y2_items[i].split("\t")
                    data_unit = self.console.create_data_unit(res[0], res[1])
                    data_array_y2 = Data_array(data_unit, res[1], res[0], res[1])
                    # data_array_y2.global_index = [index for index in range(len(data_unit.data))]

                    figure.add_data_y2_Data(data_array_y2)

                # on set le type de la figure en fonction de si y2_items est vide ou pas
                # on set le scale des axes également
                if len(y2_items) == 0:
                    figure.x_axe.scale = scale_x
                    figure.y1_axe.scale = scale_y1
                    figure.type = "custom_y1"
                else:
                    figure.x_axe.scale = scale_x
                    figure.y1_axe.scale = scale_y1
                    figure.y2_axe.scale = scale_y2
                    figure.type = "custom_y1_y2"

                # on update le tree widget
                # on ajoute la figure a current_data
                self.treeWidget.add_figure(figure, self.console.current_data.name)
                self.console.current_data.figures.append(figure)

                # on passe la figure en figure courante
                self.console.current_data.current_figure = figure

            elif name == "Diffraction":
                new_figure = self.console.current_data.create_diffraction()

                # on update le tree widget
                # on ajoute la figure a current_data
                self.treeWidget.add_figure(new_figure, self.console.current_data.name)
                self.console.current_data.figures.append(new_figure)

                # on passe la figure en figure courante
                self.console.current_data.current_figure = new_figure

            elif name == "Contour":
                new_figure = self.console.current_data.diffraction_contour_temperature()

                # on update le tree widget
                # on ajoute la figure a current_data
                for figure in new_figure:
                    self.treeWidget.add_figure(figure, self.console.current_data.name)
                    self.console.current_data.figures.append(figure)

                # on passe la figure en figure courante
                self.console.current_data.current_figure = new_figure[0]

            elif name == "Ihch 1501 plot":
                cycles_base = self.argument_selection_creation_w.cycles_base
                cycles = self.argument_selection_creation_w.cycles
                samples = self.argument_selection_creation_w.samples
                s_w = self.argument_selection_creation_w.s_w
                f_s = self.argument_selection_creation_w.f_s

                # on a récupérer les info, on délect la fenêtre
                self.argument_selection_creation_w.deleteLater()
                self.argument_selection_creation_w = None

                figures = self.console.current_data.create_figure_cycle(s_w, f_s, cycles_base, cycles, samples)

                # on parcours le vecteur, update tree widget ave le nom des figure créées
                # on ajoute les figure a current_data
                for figure in reversed(figures):
                    self.treeWidget.add_figure(figure, self.console.current_data.name)
                    self.console.current_data.figures.append(figure)

                self.console.current_data.current_figure = self.console.current_data.figures[-1]

            elif name == "Create gitt":
                # un peu différent du reste, si une création des bornes avec des graph est requis
                # on va passer par une autre function pour faire cela
                kwarks_create_borne = {"surface": self.argument_selection_creation_w.surface,
                                       "vm": self.argument_selection_creation_w.vm}

                if self.argument_selection_creation_w.radioButton_2.isChecked():
                    kwarks_create_borne["constante_d_n"] = self.argument_selection_creation_w.delta_nb / \
                                                           len(self.console.current_data.pulse["loop_data"])
                else:
                    kwarks_create_borne["constante_d_n"] = self.argument_selection_creation_w.delta_nb

                if self.argument_selection_creation_w.input is not None:
                    if self.argument_selection_creation_w.input[0] > self.argument_selection_creation_w.input[1]:
                        b1 = [(self.argument_selection_creation_w.input[1] ** 2) / 3600 for i in
                              range(len(self.console.current_data.pulse["loop_data"]))]
                        b2 = [(self.argument_selection_creation_w.input[0] ** 2) / 3600 for i in
                              range(len(self.console.current_data.pulse["loop_data"]))]
                    else:
                        b1 = [(self.argument_selection_creation_w.input[0] ** 2) / 3600 for i in
                              range(len(self.console.current_data.pulse["loop_data"]))]
                        b2 = [(self.argument_selection_creation_w.input[1] ** 2) / 3600 for i in
                              range(len(self.console.current_data.pulse["loop_data"]))]
                    kwarks_create_borne["b1"] = b1
                    kwarks_create_borne["b2"] = b2

                    kwarks_create_borne["figures"] = []

                else:
                    kwarks_create_borne["b1"] = []
                    kwarks_create_borne["b2"] = []

                    figures = []

                    loop_pulse = self.console.current_data.pulse.get("loop_data")

                    for i in range(len(loop_pulse)):
                        figure_temp = Figure("", 1)

                        array_x = []
                        array_y = []
                        start = self.console.current_data.pulse.get("time/h")[loop_pulse[i][0]]
                        for j in range(loop_pulse[i][0], loop_pulse[i][1]):
                            array_x.append(math.sqrt(self.console.current_data.pulse.get("time/h")[j] - start) * 60)
                            array_y.append(self.console.current_data.pulse.get("Ecell/V")[j])

                        figure_temp.name = "loop " + str(i + 1)
                        data_unit_x = Data_unit(array_x, None)
                        data_unit_y = Data_unit(array_y, None)

                        figure_temp.add_data_x_Data(Data_array(data_unit_x, "", "", None))
                        figure_temp.add_data_y1_Data(Data_array(data_unit_y, "", "", "loop " + str(i + 1)))

                        figures.append(figure_temp)
                    kwarks_create_borne["figures"] = figures

                # on a récupérer les info, on délect la fenêtre
                self.argument_selection_creation_w.deleteLater()
                self.argument_selection_creation_w = None

                self.create_gitt(kwarks_create_borne)

                # la création des figure se fera dans la fonction create_gitt
                return

            elif name == "Impedance":
                figures = self.console.current_data.create_impedance()

                # on update le tree widget
                # on ajoute la figure a current_data
                for figure in figures:
                    self.treeWidget.add_figure(figure, self.console.current_data.name)
                    self.console.current_data.figures.append(figure)

                # on passe la figure en figure courante
                self.console.current_data.current_figure = figures[0]

            elif name == "Resistance":
                # on récupére le cycle selectionné
                cycle_number = self.argument_selection_creation_w.value

                # on delete la fenêtre
                self.argument_selection_creation_w.deleteLater()
                self.argument_selection_creation_w = None

                if cycle_number <= 0 or cycle_number >= len(self.console.current_data.data["loop_data"]):
                    self.update_console({"str": "Cycle selection invalid", "foreground_color": "red"})
                    return

                figure_temp = Figure("Frequencies selection", 1)
                figure_temp.plot_name = "Frequencies selection\ndouble left click to have the selector\n" \
                                        "double right click to select a point\n'r' to reset and 's' or close to save"
                figure_temp.type = "impedance"
                start = self.console.current_data.data.get("loop_data")[cycle_number - 1][0]
                end = self.console.current_data.data.get("loop_data")[cycle_number - 1][1]

                res = Traitements_cycle_outils.mode_del(self.console.current_data.data.get("Re(Z)/Ohm")[start:end],
                                                        self.console.current_data.data.get("-Im(Z)/Ohm")[start:end],
                                                        None, start, end, self.console.current_data.data.get("mode"), 3)

                units = Units()
                unit_x = units.get_unit("Re(Z)/Ohm")
                unit_y = units.get_unit("-Im(Z)/Ohm")

                for j in range(len(res[0])):
                    if j > 10 and res[0][j] * 1.5 < res[1][j]:
                        data_unit_x = Data_unit(res[0][0:j], unit_x)
                        data_unit_y = Data_unit(res[1][0:j], unit_y)

                        figure_temp.add_data_x_Data(Data_array(data_unit_x, "Re(Z)/Ohm",
                                                               self.console.current_data.name, "cycle " +
                                                               str(cycle_number)))
                        figure_temp.add_data_y1_Data(Data_array(data_unit_y, "-Im(Z)/Ohm",
                                                                self.console.current_data.name, "cycle " +
                                                                str(cycle_number)))
                        figure_temp.aspect = "equal"
                        break

                self.create_impedance_res(figure_temp)

                # la création des figure se fera dans la fonction create_impedance_res
                return

            elif name == "Bode":
                figure = self.console.current_data.impedance_bode()

                # on update le tree widget
                # on ajoute la figure a current_data
                self.treeWidget.add_figure(figure, self.console.current_data.name)
                self.console.current_data.figures.append(figure)

                # on passe la figure en figure courante
                self.console.current_data.current_figure = figure

            elif name == "3d":
                if self.argument_selection_creation_w.comboBox.currentText() == "time":
                    arg = "time/h"
                else:
                    arg = "Ecell/V"

                # on delete la fenêtre
                self.argument_selection_creation_w.deleteLater()
                self.argument_selection_creation_w = None

                figure = self.console.current_data.create_impedance_3d(arg)

                # on update le tree widget
                # on ajoute la figure a current_data
                self.treeWidget.add_figure(figure, self.console.current_data.name)
                self.console.current_data.figures.append(figure)

                # on passe la figure en figure courante
                self.console.current_data.current_figure = figure


            _translate = QtCore.QCoreApplication.translate
            self.label_5.setText(
                _translate("MainWindow", "<html><head/><body><p><span style=\" font-size:11pt;\">"
                                         "Current plot : "
                           + self.console.current_data.current_figure.name + " </span></p></body></html>"))

            # on update les actions disponibles pour cette figure
            self.update_action_combo()

    """---------------------------------------------------------------------------------"""

    def create_gitt(self, _dict, signal=None):
        """
        On utilise cette methode pour créer une boucle, si call est True c'est que l'on vient
        de faire un loop, le traitement sera différent

        :param _dict: dict d'arguement qui évolura dans le cas ou une selection des bornes
        avec un graph sera effectué
        :param signal: None si cette function n'est pas issus d'un callback, signal du callback sinon
        :return: None
        """

        if signal is not None:
            b1 = (self.argument_selection_creation_w.abstract_affiche.coords[0][0] ** 2) / 3600
            b2 = (self.argument_selection_creation_w.abstract_affiche.coords[1][0] ** 2) / 3600
            if b1 is None or b2 is None:
                self.emit.emit("msg_console", type="msg_console", str="Mark 1 or 2 missing",
                               foreground_color="red")
                return
            if b1 == b2:
                self.emit.emit("msg_console", type="msg_console", str="Mark 1 and 2 should be different",
                               foreground_color="red")
                return

            if b1 > b2:
                _dict["b1"].append(b2)
                _dict["b2"].append(b1)
            else:
                _dict["b1"].append(b1)
                _dict["b2"].append(b2)

            _dict["figures"].pop(0)
            pplot.close(self.argument_selection_creation_w.abstract_affiche.pplot_fig)
            pass

        if len(_dict["figures"]) == 0:
            try:
                figures = self.console.current_data.create_GITT(_dict["surface"], _dict["vm"], _dict["constante_d_n"],
                                                                _dict["b1"], _dict["b2"])
            except ValueError:
                return

            for figure in figures:
                self.treeWidget.add_figure(figure, self.console.current_data.name)
                self.console.current_data.figures.append(figure)

            self.console.current_data.current_figure = self.console.current_data.figures[-1]

            _translate = QtCore.QCoreApplication.translate
            self.label_5.setText(
                _translate("MainWindow", "<html><head/><body><p><span style=\" font-size:11pt;\">"
                                         "Current plot : "
                           + self.console.current_data.current_figure.name + " </span></p></body></html>"))

            # on update les actions disponibles pour cette figure
            self.update_action_combo()

        else:
            # on créer un obj Edit_affiche, fille de Abstract_objet_affiche servant à l'édition de points
            edit_affiche = Gitt_affiche(self.console.current_data, _dict["figures"][0])

            # on garde une ref de l'objet créée
            self.argument_selection_creation_w = Figure_plot(edit_affiche, self)

            # on connect de callback, on utilise lambda pour passer signal comme arg suplémentaire
            self.argument_selection_creation_w.closed.connect(lambda event: self.create_gitt(_dict, event))

            # on passe le plot d'édition en modal
            self.argument_selection_creation_w.setWindowModality(QtCore.Qt.ApplicationModal)

            # on affiche le widget
            self.argument_selection_creation_w.show()

    def create_impedance_res(self, figure, signal=None):
        """
        même principe que pour create_gitt, si signal est pas None c'est que c'est un callback

        :param figure: Figure dont on se sert pour la selection des pics
        :param signal: None si cette function n'est pas issus d'un callback, signal du callback sinon
        :return: None
        """
        if signal is not None:
            res = self.argument_selection_creation_w.abstract_affiche.val_freq
            figures = self.console.current_data.impedance_res(res)

            for figure in figures:
                self.treeWidget.add_figure(figure, self.console.current_data.name)
                self.console.current_data.figures.append(figure)

            self.console.current_data.current_figure = figures[0]

            _translate = QtCore.QCoreApplication.translate
            self.label_5.setText(
                _translate("MainWindow", "<html><head/><body><p><span style=\" font-size:11pt;\">"
                                         "Current plot : "
                           + self.console.current_data.current_figure.name + " </span></p></body></html>"))

            # on update les actions disponibles pour cette figure
            self.update_action_combo()

        else:
            # on créer un obj Edit_affiche, fille de Abstract_objet_affiche servant à l'édition de points
            edit_affiche = Impedance_affiche(self.console.current_data, figure)

            # on garde une ref de l'objet créée
            self.argument_selection_creation_w = Figure_plot(edit_affiche, self)

            # on connect de callback, on utilise lambda pour passer signal comme arg suplémentaire
            self.argument_selection_creation_w.closed.connect(lambda event: self.create_impedance_res(None, event))

            # on passe le plot d'édition en modal
            self.argument_selection_creation_w.setWindowModality(QtCore.Qt.ApplicationModal)

            # on affiche le widget
            self.argument_selection_creation_w.show()

    def create_figure(self):
        """
        Methode appellé par le button create de current plot (action)
        Si current_figure is None, on affiche une fenêtre avec un message

        Pour le reste, à faire

        :return: None
        """
        if self.console.current_data is None or self.console.current_data.current_figure is None:
            self.current_figure_None()
        else:
            if self.argument_selection_creation_w is not None:
                self.argument_selection_creation_w.deleteLater()
                self.argument_selection_creation_w = None

            if self.comboBox_4.currentText() == "derive":
                self.argument_selection_creation_w = Derive_Selection(self)
                self.argument_selection_creation_w.finish_signal.connect(
                    lambda event: self.create_figure_callback(event, "derive"))

            elif self.comboBox_4.currentText() == "shift x":
                self.argument_selection_creation_w = Ask_Value(self, "float", "Shift X axis",
                                                               "Value : ")
                self.argument_selection_creation_w.finish_signal.connect(
                    lambda event: self.create_figure_callback(event, "shift x"))
            elif self.comboBox_4.currentText() == "shift y":
                self.argument_selection_creation_w = Ask_Value(self, "float", "Shift Y axis",
                                                               "Value : ")
                self.argument_selection_creation_w.finish_signal.connect(
                    lambda event: self.create_figure_callback(event, "shift y"))
            elif self.comboBox_4.currentText() == "cycle":
                self.argument_selection_creation_w = Cycle_selection_creation \
                    (self.console.current_data.get_cycle_available(), self)

                self.argument_selection_creation_w.finish_signal.connect(
                    lambda event: self.create_figure_callback(event, "cycle"))
            elif self.comboBox_4.currentText() == "fit":
                self.create_figure_callback("save", "fit")
            elif self.comboBox_4.currentText() == "export gitt":
                self.create_figure_callback("save", "export gitt")
            elif self.comboBox_4.currentText() == "export resistances":
                self.create_figure_callback("save", "export resistances")

            # il n'y a pas toujours de fenêtre de selection de paramètre, on check si elle est None ou pas
            if self.argument_selection_creation_w is not None:
                self.argument_selection_creation_w.show()

    """---------------------------------------------------------------------------------"""

    def create_figure_callback(self, signal, name):
        if signal == "cancel":
            self.argument_selection_creation_w.deleteLater()
            self.argument_selection_creation_w = None
        else:
            if name == "derive":
                nb_point = self.argument_selection_creation_w.nb_point
                window_length = self.argument_selection_creation_w.window_length
                polyorder = self.argument_selection_creation_w.polyorder

                self.argument_selection_creation_w.deleteLater()
                self.argument_selection_creation_w = None

                figure_res = self.console.current_data.derive(nb_point,
                                                              window_length,
                                                              polyorder)

                # on update le tree widget
                # on ajoute la figure a current_data
                self.treeWidget.add_figure(figure_res, self.console.current_data.name)
                self.console.current_data.figures.append(figure_res)

                # on passe la figure en figure courante
                self.console.current_data.current_figure = figure_res

                # on update le label avec le nouveau nom de la figure
                self.update_figure_name()

                # on update les actions disponibles pour cette figure
                self.update_action_combo()

            elif name == "shift x" or name == "shift y":
                # on récupére les données
                value = self.argument_selection_creation_w.value

                # delet de la fenêtre
                self.argument_selection_creation_w.deleteLater()
                self.argument_selection_creation_w = None

                if name == "shift x":
                    figure_res = self.console.current_data.shift_axe("x", value)
                else:
                    figure_res = self.console.current_data.shift_axe("y", value)

                if figure_res is None:
                    return

                # on update le tree widget
                # on ajoute la figure a current_data
                self.treeWidget.add_figure(figure_res, self.console.current_data.name)
                self.console.current_data.figures.append(figure_res)

                # on passe la figure en figure courante
                self.console.current_data.current_figure = figure_res

                # on update le label avec le nouveau nom de la figure
                self.update_figure_name()

                # on update les actions disponibles pour cette figure
                self.update_action_combo()

            elif name == "cycle":
                # on récupére les cycles sélectionnée
                cycles = self.argument_selection_creation_w.cycles
                cycle_type = self.argument_selection_creation_w.comboBox.currentText()

                # delet de la fenêtre
                self.argument_selection_creation_w.deleteLater()
                self.argument_selection_creation_w = None

                dict = self.console.create_dictioanaries_loop()

                try:
                    figure_res = self.console.current_data.create_figure_cycle \
                        (dict=dict, type=cycle_type, cycles=cycles)
                except ValueError:
                    return

                # si plusieurs figure ont été crée
                if isinstance(figure_res, list):
                    for figure in figure_res:
                        # on update le tree widget
                        # on ajoute la figure a current_data
                        self.treeWidget.add_figure(figure, self.console.current_data.name)
                        self.console.current_data.figures.append(figure)

                        # on passe la figure en figure courante
                        self.console.current_data.current_figure = figure

                    # on update le label avec le nouveau nom de la figure
                    self.update_figure_name()

                    # on update les actions disponibles pour cette figure
                    self.update_action_combo()
                else:
                    # on update le tree widget
                    # on ajoute la figure a current_data
                    self.treeWidget.add_figure(figure_res, self.console.current_data.name)
                    self.console.current_data.figures.append(figure_res)

                    # on passe la figure en figure courante
                    self.console.current_data.current_figure = figure_res

                    # on update le label avec le nouveau nom de la figure
                    self.update_figure_name()

                    # on update les actions disponibles pour cette figure
                    self.update_action_combo()

            elif name == "fit":
                # on créer une nouvelle figure
                figure = Figure("Pic selection", 1)

                # on fait une copy des data_array 0
                data_array_x = self.console.current_data.current_figure.x_axe.data[0].copy()
                data_array_y = self.console.current_data.current_figure.y1_axe.data[0].copy()

                # on ajoute les data_array
                figure.add_data_x_Data(data_array_x)
                figure.add_data_y1_Data(data_array_y)

                # on créer Abstract_objet_affiche pour la sélection de pics
                pic_selection = Pic_selection(self.console.current_data, figure)

                # le graph ne sera pas éditable
                pic_selection.editable = False

                # on garde une ref de l'objet créée
                self.edit_plot_figure_w = Figure_plot(pic_selection, self)

                # on connect de callback
                self.edit_plot_figure_w.closed.connect(self.callback_pic_selection)

                # on passe le plot d'édition en modal
                self.edit_plot_figure_w.setWindowModality(QtCore.Qt.ApplicationModal)

                # on affiche le widget
                self.edit_plot_figure_w.show()
            elif name == "complete_gitt":
                # on récupére les données
                value = self.argument_selection_creation_w.value

                # delet de la fenêtre
                self.argument_selection_creation_w.deleteLater()
                self.argument_selection_creation_w = None

                self.console.current_data.pulse["Is"] = value

            elif name == "export gitt":
                if not self.console.current_data.export_gitt_array:
                    self.update_console({"str": "No data to be exported", "foreground_color": "red"})
                    return

                dialog = QFileDialog.getSaveFileName(filter="Text files (*.txt)")

                if dialog[0] != "":
                    self.console.current_data.export_gitt(dialog[0])
                    self.update_console({"str": "Done", "foreground_color": "green"})
                    return
                else:
                    return

            elif name == "export resistances":
                if not self.console.current_data.export_resistance_array:
                    self.update_console({"str": "No data to be exported", "foreground_color": "red"})
                    return

                dialog = QFileDialog.getSaveFileName(filter="Text files (*.txt)")

                if dialog[0] != "":
                    self.console.current_data.export_impedance_res(dialog[0])
                    self.update_console({"str": "Done", "foreground_color": "green"})
                    return
                else:
                    return

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
            temp_item = self.treeWidget.selectedItems()[0]
            while temp_item.text(1) == "figure":
                temp_item = temp_item.parent()

            self.console.set_current_data_name(temp_item.text(0))

            # maintenant que current data est update, on parcours les figures de current_data de la console
            for figure in self.console.current_data.figures:

                # quand on a touvé la figure
                if figure.name == self.treeWidget.currentItem().text(0):

                    current_index = self.tabWidget.currentIndex()

                    # check si la tab est déja ouverte
                    for i in range(self.tabWidget.count()):

                        # si elle est ouverte dans une tab
                        if self.tabWidget.tabText(i) == figure.name and self.tabWidget.widget(i).abstract_affiche.data.name == self.console.current_data.name:

                            # on récupére le current index de tab pour regarder si il sera effectivemeent modifié
                            # si oui l'update de current_figure et des label se fera dans le changement de tab
                            # sinon on le fait là

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

                                # on update les actions disponibles pour cette figure
                                self.update_action_combo()
                            else:
                                # update de current tab
                                self.tabWidget.setCurrentIndex(i)

                            return

                    # check si la figure est ouverte en fenêtre
                    if self.on_top_plot_w(figure.name):
                        return

                    # à ce point de la fonction, le plot n'existe pas, il faut le créer
                    obj = Classique_affiche(self.console.current_data, figure)

                    try:
                        new_tab = Figure_plot(obj, self)
                    except ValueError:
                        self.delete_obj_plot(obj)
                        return

                    new_tab.setObjectName(figure.name)
                    new_tab.name_changed.connect(self.name_changed_plot)
                    new_tab.focus_in.connect(self.focus_in_w_plot)

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
            # on clear la box action
            self.comboBox_4.clear()

            # on passe la current_figure à None
            self.console.current_data.current_figure = None

            # on update current_data de la console
            self.console.set_current_data_name(self.treeWidget.selectedItems()[0].text(0))

            # on update la combobox new plot
            self.update_new_plot_combo()

    """---------------------------------------------------------------------------------"""

    def fin_thread_lecture(self, event):
        """
        Déclenché à la suite de la fin de l'execution d'un thread de lecture
        On créer un nouvelle objet data associée au data récupérées par le thread

        :event: 1 tout c'est bien passé, -1, fail, -2 manque un fichier pour ihch file
        :return: None
        """
        index = 0
        # on parcours les threads de lecture en cours
        while index < len(self.threads):
            if type(self.threads[index][1]).__name__ == "Open_file_cccv" and self.threads[index][1].finish:
                if event == -1:
                    # on termine le thread
                    self.threads[index][0].terminate()

                    # on le suprime de la liste
                    del self.threads[index]

                    self.fichier_invalide_error()
                elif event == 1:
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

                    # on update current data avec ne nom du nouveau fichier
                    _translate = QtCore.QCoreApplication.translate
                    self.label.setText(
                        _translate("MainWindow", "<html><head/><body><p><span style=\" font-size:11pt;\">"
                                                 "Current data : "
                                   + obj_data.name + " </span></p></body></html>"))

                    self.update_console({"str": "Done", "foreground_color": "green"})

                    # on récupére les actions disponibles pour ce type de fichier pour update
                    # current data comboBox_5
                    self.update_new_plot_combo()

                    # on termine le thread
                    self.threads[index][0].terminate()

                    # on le suprime de la liste
                    del self.threads[index]
                break

            elif type(self.threads[index][1]).__name__ == "Open_file_diffraction" and self.threads[index][1].finish:
                if event == -1:
                    # on termine le thread
                    self.threads[index][0].terminate()

                    # on le suprime de la liste
                    del self.threads[index]

                    self.fichier_invalide_error()
                elif event == 1:
                    # on créer un objet data cccv
                    obj_data = Diffraction_data()

                    # on lui ajoute les data lu par le thread
                    obj_data.data = self.threads[index][1].data

                    # créer son nom
                    obj_data.name = obj_data.data["name"]

                    # on ajoute l'objet data à la console
                    self.console.add_data(obj_data)

                    # on update le tree widget
                    self.treeWidget.add_data("diffraction", obj_data.name)

                    # on update current data avec ne nom du nouveau fichier
                    _translate = QtCore.QCoreApplication.translate
                    self.label.setText(
                        _translate("MainWindow", "<html><head/><body><p><span style=\" font-size:11pt;\">"
                                                 "Current data : "
                                   + obj_data.name + " </span></p></body></html>"))

                    self.update_console({"str": "Done", "foreground_color": "green"})

                    # on récupére les actions disponibles pour ce type de fichier pour update
                    # current data comboBox_5
                    self.update_new_plot_combo()

                    # on termine le thread
                    self.threads[index][0].terminate()

                    # on le suprime de la liste
                    del self.threads[index]
                break
            elif type(self.threads[index][1]).__name__ == "Open_file_ihch_1501" and self.threads[index][1].finish:
                # dans le cas de ihch event est une list
                # [resultat, nb_cycles]
                if event[0] == -2:
                    root_path = self.threads[index][1].file_path
                    nb_cycles = event[1]

                    # on termine le thread
                    self.threads[index][0].terminate()

                    # on le suprime de la liste
                    del self.threads[index]

                    msgBox = QMessageBox()
                    msgBox.setIcon(QMessageBox.Warning)
                    msgBox.setText("time missing in .dat file\nSelect ec_lab file to create it")
                    msgBox.setWindowTitle("Error")
                    msgBox.setStandardButtons(QMessageBox.Ok)
                    msgBox.exec_()

                    # on passe l'event à None pour ne pas triger une seconde fois le traitement
                    # je ne sias pas du tout pouruqoi cette fonction est callback 2 fois, c'est pas super
                    # jolie mais ça fonctionne
                    event = None
                    self.open_ihch_time(root_path, nb_cycles)


                elif event[0] == -1:
                    # on termine le thread
                    self.threads[index][0].terminate()

                    # on le suprime de la liste
                    del self.threads[index]

                    self.fichier_invalide_error()
                elif event[0] == 1:
                    # on créer un objet data cccv
                    obj_data = Ihch_1501()

                    # on lui ajoute les data lu par le thread
                    obj_data.cycles = self.threads[index][1].data

                    # créer son nom
                    obj_data.name = "ihch A MODIFIER"

                    # on ajoute l'objet data à la console
                    self.console.add_data(obj_data)

                    # on update le tree widget
                    self.treeWidget.add_data("ihch 1501", obj_data.name)

                    # on update current data avec ne nom du nouveau fichier
                    _translate = QtCore.QCoreApplication.translate
                    self.label.setText(
                        _translate("MainWindow", "<html><head/><body><p><span style=\" font-size:11pt;\">"
                                                 "Current data : "
                                   + obj_data.name + " </span></p></body></html>"))

                    self.update_console({"str": "Done", "foreground_color": "green"})

                    # on récupére les actions disponibles pour ce type de fichier pour update
                    # current data comboBox_5
                    self.update_new_plot_combo()

                    # on termine le thread
                    self.threads[index][0].terminate()

                    # on le suprime de la liste
                    del self.threads[index]
                break
            elif type(self.threads[index][1]).__name__ == "Open_file_gitt" and self.threads[index][1].finish:
                if event == -1:
                    # on termine le thread
                    self.threads[index][0].terminate()

                    # on le suprime de la liste
                    del self.threads[index]

                    self.fichier_invalide_error()
                elif event == 1:
                    # on créer un objet data cccv
                    obj_data = Gitt_data()

                    # on lui ajoute les data lu par le thread
                    obj_data.potentiel = self.threads[index][1].data[0]
                    obj_data.pulse = self.threads[index][1].data[1]
                    obj_data.relaxation = self.threads[index][1].data[2]

                    # créer son nom
                    obj_data.name = obj_data.pulse["name"]

                    # on ajoute l'objet data à la console
                    self.console.add_data(obj_data)

                    # on update le tree widget
                    self.treeWidget.add_data("gitt", obj_data.name)

                    # on update current data avec ne nom du nouveau fichier
                    _translate = QtCore.QCoreApplication.translate
                    self.label.setText(
                        _translate("MainWindow", "<html><head/><body><p><span style=\" font-size:11pt;\">"
                                                 "Current data : "
                                   + obj_data.name + " </span></p></body></html>"))

                    self.update_console({"str": "Done", "foreground_color": "green"})

                    # on récupére les actions disponibles pour ce type de fichier pour update
                    # current data comboBox_5
                    self.update_new_plot_combo()

                    # on termine le thread
                    self.threads[index][0].terminate()

                    # on le suprime de la liste
                    del self.threads[index]

                    if not "Is" in self.console.current_data.pulse:
                        self.argument_selection_creation_w = Ask_Value(self, "float",
                                                                       "Data Is not found, please fill it in",
                                                                       "Is ? (µA) : ")
                        self.argument_selection_creation_w.finish_signal.connect(
                            lambda event: self.create_figure_callback(event, "complete_gitt"))
                break

            if type(self.threads[index][1]).__name__ == "Open_file_impedance" and self.threads[index][1].finish:
                if event == -1:
                    # on termine le thread
                    self.threads[index][0].terminate()

                    # on le suprime de la liste
                    del self.threads[index]

                    self.fichier_invalide_error()
                elif event == 1:
                    # on créer un objet data impedance
                    obj_data = Impedance_data()

                    # on lui ajoute les data lu par le thread
                    obj_data.data = self.threads[index][1].data

                    # créer son nom
                    obj_data.name = obj_data.data["name"]

                    # on ajoute l'objet data à la console
                    self.console.add_data(obj_data)

                    # on update le tree widget
                    self.treeWidget.add_data("impedance", obj_data.name)

                    # on update current data avec ne nom du nouveau fichier
                    _translate = QtCore.QCoreApplication.translate
                    self.label.setText(
                        _translate("MainWindow", "<html><head/><body><p><span style=\" font-size:11pt;\">"
                                                 "Current data : "
                                   + obj_data.name + " </span></p></body></html>"))

                    self.update_console({"str": "Done", "foreground_color": "green"})

                    # on récupére les actions disponibles pour ce type de fichier pour update
                    # current data comboBox_5
                    self.update_new_plot_combo()

                    # on termine le thread
                    self.threads[index][0].terminate()

                    # on le suprime de la liste
                    del self.threads[index]
                break

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

        old_name = signal[0]
        new_name = self.console.current_data.unique_name(signal[1])

        # on cherche la figure portant l'ancien nom
        for figure in self.console.current_data.figures:
            if figure.name == old_name:
                # le nouveau nom est celui de la tab
                self.tabWidget.setTabText(self.tabWidget.currentIndex(), new_name)

                # on update le nom de la figure dans la console
                figure.name = new_name

                # on update le nom de l'item de tree widget
                self.treeWidget.rename_item(old_name, new_name, 0)

                # on update le nom du plot associé à la tab
                self.tabWidget.currentWidget().update_title_plot(new_name)

                # on update current plot
                _translate = QtCore.QCoreApplication.translate
                self.label_5.setText(_translate("MainWindow", "<html><head/><body><p><span style=\" font-size:11pt;\">"
                                                              "Current plot : "
                                                + new_name + " </span></p></body></html>"))

                break

    """---------------------------------------------------------------------------------"""

    def close_tab_handler(self, index):
        """
        Permet de fermet une tab quand la croix de d'une est cliqué

        :param index: index de la tab qui a déchanché cette demande de fermeture
        :return: None
        """

        self.tabWidget.widget(index).close_view_values()

        # la tab à l'index est remove
        self.tabWidget.removeTab(index)

    """---------------------------------------------------------------------------------"""

    def name_changed_plot(self, signal):
        """
        Déclenchée quand le nom du plot est changé, on update le nom
        Le unique name se fait par la plot

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
        self.treeWidget.rename_item(old_name, new_name, 0)

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
        # pas besoin de try catch ici, le plot a déjà été créée donc il est valide
        new_w = Figure_plot(self.tabWidget.widget(signal).abstract_affiche, self)

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
                new_tab = Figure_plot(affiche_obj.abstract_affiche, self)
                new_tab.setObjectName(signal)

                # connection de la nouvelle tab
                new_tab.name_changed.connect(self.name_changed_plot)
                new_tab.focus_in.connect(self.focus_in_w_plot)

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

        if signal == self.console.current_data.current_figure.name:
            return

        _translate = QtCore.QCoreApplication.translate
        # update du label affichant la figure courrante
        self.label_5.setText(_translate("MainWindow", "<html><head/><body><p><span style=\" font-size:11pt;\">"
                                                      "Current plot : "
                                        + signal + " </span></p></body></html>"))

        # update de la figure courrante de la console
        self.console.current_data.set_current_figure_name(signal)

        # on update les actions disponibles pour cette figure
        self.update_action_combo()

        item = self.treeWidget.get_item(self.console.current_data.name, signal)

        # update du focus du tree widget
        self.treeWidget.setCurrentItem(item)

    """---------------------------------------------------------------------------------"""

    def name_changed_w_plot(self, signal):
        """
        Déclenché quand le nom du plot est modifiée sur une
        fenêtre
        Le unique name se fait par la plot

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
        item = self.treeWidget.get_item(self.console.current_data.name, old_name)
        item.setText(0, new_name)

        # on update le label current plot
        _translate = QtCore.QCoreApplication.translate
        self.label_5.setText(_translate("MainWindow", "<html><head/><body><p><span style=\" font-size:11pt;\">"
                                                      "Current plot : "
                                        + new_name + " </span></p></body></html>"))

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

        # si new_name == "", il n'y a plus de tab d'ouverte, rien à faire
        if new_name == "":
            return


        parent = self.treeWidget.get_top_item(self.console.current_data.name, new_name)

        # on reset la selection du treewidget
        self.treeWidget.clearSelection()
        # on récupére l'item
        item = self.treeWidget.get_item(self.console.current_data.name, new_name)
        # on set le focus sur lui
        item.setSelected(True)

        # on update current data de la console en premier
        self.console.set_current_data_name(parent.text(0))

        # si le type de fichier a changé, il faut update les actions disponibles
        if parent.text(1) != self.console.current_data.__name__:
            self.update_new_plot_combo()

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

        # on update les actions disponibles pour cette figure
        self.update_action_combo()

    """---------------------------------------------------------------------------------"""

    def message_console(self, signal):
        """
        Callback de self.emit, on regarde le type donnée dans le
        signal et en fonction on apelle la methode correspondante

        :param signal: dict : {type: msg_console, ...}
        :return: None
        """

        if signal["type"] == "msg_console":
            del signal["type"]
            self.update_console(signal)

    """---------------------------------------------------------------------------------"""

    def update_console(self, signal):
        """
        Callback de print_console de la classe resource pour afficher un message
        dans le widget "console"

        :param signal: dict : str
                  background_color:
                  foreground_color
                  font

        :return: None
        """
        cursor = self.console_txt.edit.textCursor()
        cursor.removeSelectedText()
        cursor.movePosition(QTextCursor.End)
        self.console_txt.edit.setTextCursor(cursor)

        self.console_txt.edit.textCursor().insertHtml('<div style=color:' + signal["foreground_color"] + '>' +
                                                      signal["str"] + '<br></div>')
        self.console_txt.update_prompt_pos()

    """---------------------------------------------------------------------------------"""

    def process_input_console_txt(self, event):
        """
        Callback de _input de la console_txt

        :param event: commande str tapé dans la console txt
        :return:
        """

        print(event)

    """---------------------------------------------------------------------------------"""

    def get_plot_from_figure(self, figure):
        """
        On cherche l'objet plot, si il existe à partir d'un objet figure, on retourne None
        si il n'y a pas d'objet plot assicié

        :param figure: objet figure
        :return: plot_obj / None
        """

        # on cherche dans les fen^tre si le plot y esst présent
        for plot_obj in self.figure_w:
            if plot_obj.abstract_affiche.figure == figure:
                return plot_obj

        # on cherche dans le tab si le plot est présent
        for i in range(self.tabWidget.count()):
            if self.tabWidget.tabText(i) == figure.name:
                return self.tabWidget.widget(i)

        # elle n'est pas présente, on return None
        return None

    """---------------------------------------------------------------------------------"""

    def update_action_combo(self):
        """
        On update la combobox des actions disponible en fonction de la figure
        courante

        :return: None
        """

        # on clear la box
        self.comboBox_4.clear()

        # on l'update avec les nouvelles actions
        actions = self.console.current_data.current_figure.get_operation()
        for action in actions:
            self.comboBox_4.addItem(action)

    """---------------------------------------------------------------------------------"""

    def update_new_plot_combo(self):
        """
        On update la combobox des actions disponible en fonction de current_data

        :return: None
        """
        self.comboBox_5.clear()
        for action in self.console.current_data.get_operation_available():
            self.comboBox_5.addItem(action)

    """---------------------------------------------------------------------------------"""

    def update_figure_name(self):
        _translate = QtCore.QCoreApplication.translate
        self.label_5.setText(
            _translate("MainWindow", "<html><head/><body><p><span style=\" font-size:11pt;\">"
                                     "Current plot : "
                       + self.console.current_data.current_figure.name + " </span></p></body></html>"))

    """---------------------------------------------------------------------------------"""

    def delet_current_plot(self):
        """
        Fonction par un clique sur delet_current_plot

        :return: None
        """
        # si il n'y a pas de current_figure, on return
        if self.console.current_data is None:
            self.current_data_None()
            return
        elif self.console.current_data.current_figure is None:
            self.current_figure_None()
            return
        else:
            found = False

            # on récupére le plot associé à cette figure
            # on cherche dans les fenêtre si le plot y est présent
            for i, _plot_obj in enumerate(self.figure_w):
                if _plot_obj.abstract_affiche.figure == self.console.current_data.current_figure:
                    _plot_obj.close()
                    _plot_obj.deleteLater()
                    self.figure_w.pop(i)
                    found = True
                    break

            if not found:
                # on cherche dans le tab si le plot est présent
                for i in range(self.tabWidget.count()):
                    if self.tabWidget.tabText(i) == self.console.current_data.current_figure.name:
                        self.tabWidget.widget(i).close()
                        self.tabWidget.widget(i).deleteLater()
                        break

            self.treeWidget.delete_figure(self.console.current_data.current_figure.name, self.console.current_data.name)

            # toutes les figure étant créée à partir de la figure suprimé ont leurs created from passé a None
            for figure in self.console.current_data.figures:
                if figure.created_from is not None and figure.created_from.name == self.console.current_data.current_figure.name:
                    figure.created_from = None

            for i in range(len(self.console.current_data.figures)):
                if self.console.current_data.figures[i].name == self.console.current_data.current_figure.name:
                    self.console.current_data.figures.pop(i)
                    self.console.current_data.current_figure = None
                    break

    """---------------------------------------------------------------------------------"""

    def delete_obj_plot(self, obj):
        """
        fonction callbak de delete de Figure_plot
        si la figure n'a pas pu être tracé, ce plot est delete
        :return: None
        """
        self.update_console({"str": obj.figure.name + " is invalide", "foreground_color": "red"})

        self.treeWidget.delete_figure(obj.figure.name, self.console.current_data.name)

        for i in range(len(self.console.current_data.figures)):
            if self.console.current_data.figures[i].name == obj.figure.name:
                self.console.current_data.figures.pop(i)
                break

    """---------------------------------------------------------------------------------"""

    def export_plot(self):
        if self.console.current_data is None:
            self.current_data_None()
            return
        elif self.console.current_data.current_figure is None:
            self.current_figure_None()
            return
        elif not self.console.current_data.current_figure.can_export():
            self.update_console({"str": "Cannot export this type of plot", "foreground_color": "red"})
        else:

            dialog = QFileDialog.getSaveFileName(filter="Text files (*.txt)")

            if dialog[0] != "":
                self.console.current_data.current_figure.export(dialog[0])
                self.update_console({"str": "Done", "foreground_color": "green"})

    """---------------------------------------------------------------------------------"""

    def edit_data(self):
        """
        fonction appellé pour l'édition du fichier courrant

        :return: None
        """

        array_edit = self.console.current_data.get_edit_data_available()

        self.argument_selection_creation_w = Edit_data(self, self.console.current_data.name, array_edit)



        self.argument_selection_creation_w.finish_signal.connect(self.edit_data_callback)
        self.argument_selection_creation_w.show()

    """---------------------------------------------------------------------------------"""

    def edit_data_callback(self, signal):
        """
        Focntion callback de edit_data, si le signal est save, on traite les changements si il y en a

        :param signal: save / cancel
        :return: None
        """

        if signal == "cancel":
            self.argument_selection_creation_w.deleteLater()
            self.argument_selection_creation_w = None

        # on savegarde les changements
        elif signal == "save":
            data_name = self.argument_selection_creation_w.lineEdit.text()

            array_res = self.argument_selection_creation_w.array_res

            self.argument_selection_creation_w.deleteLater()
            self.argument_selection_creation_w = None

            # si le nom des data a changé
            if data_name != self.console.current_data.name:

                # on garde l'ancien nom du fichier
                old_name = self.console.current_data.name

                # on update le nom
                self.console.current_data.name = data_name

                # on parcours toutes les figures pour changer le nom
                for data in self.console.datas:
                    for figure in data.figures:
                        # si l'ancien nom est contenu dans le titre du graph, il est changé

                        if len(figure.name) >= len(old_name) and figure.name[:len(old_name)] == old_name:
                            figure.name = data_name + figure.name[len(old_name):]

                        if figure.x_axe is not None:
                            for data_array in figure.x_axe.data:
                                if data_array.source == old_name:
                                    data_array.source = data_name

                        if figure.y1_axe is not None:
                            for data_array in figure.y1_axe.data:
                                if data_array.source == old_name:
                                    data_array.source = data_name

                        if figure.y2_axe is not None:
                            for data_array in figure.y2_axe.data:
                                if data_array.source == old_name:
                                    data_array.source = data_name

                        if figure.z1_axe is not None:
                            for data_array in figure.z1_axe.data:
                                if data_array.source == old_name:
                                    data_array.source = data_name

                self.treeWidget.rename_all(old_name, data_name)

                for i in range(self.tabWidget.count()):
                    self.tabWidget.widget(i).update_current_title_plot()
                    self.tabWidget.setTabText(i, self.tabWidget.widget(i).abstract_affiche.figure.name)

                for figure_plot in self.figure_w:
                    figure_plot.update_current_title_plot()

            self.console.current_data.process_edit_data(array_res)

    """---------------------------------------------------------------------------------"""


    """---------------------------------------------------------------------------------"""
    """                            Edit Current Plot start                              """
    """---------------------------------------------------------------------------------"""

    def edit_current_plot(self):
        """
        création de la fenêtre d'édition du plot

        :return: None
        """
        # si current data est None, une erreur s'affiche
        if self.console.current_data is None:
            self.current_data_None()

        # si current figure est None, une erreur s'affiche
        elif self.console.current_data.current_figure is None:
            self.current_figure_None()
        elif self.edit_plot_w is not None:
            self.edit_plot_w.activateWindow()
            return
        else:

            if self.console.current_data.current_figure.type == "bar":
                self.update_console({"str": "Bar plot cannot be edited", "foreground_color": "red"})
                return

            if self.console.current_data.current_figure.type == "contour":
                # on créer la nouvelle fenêtre
                self.edit_plot_w = Edit_plot_contour(self)

                # on sauvegarde la figure édité
                self.figure_edited = self.console.current_data.current_figure

                # on change le label pour y affiche le nom de la figure courrante
                self.edit_plot_w.label.setText(self.console.current_data.current_figure.name)
                self.edit_plot_w.label.setFont(QFont(*self.resource.default_font))

                # on compléte le combobox avec le nom de toutes le couleurs disponible
                self.edit_plot_w.comboBox_left.addItem("unchanged")
                self.edit_plot_w.comboBox_left.addItem("default")
                for color in Resources.COLOR_MAP.keys():
                    self.edit_plot_w.comboBox_left.addItem(color)

                if "norm" in self.figure_edited.kwarks:
                    if self.figure_edited.kwarks["norm"][0] != -1:
                        self.edit_plot_w.lineEdit.setText(str(self.figure_edited.kwarks["norm"][0]))

                    if self.figure_edited.kwarks["norm"][1] != -1:
                        self.edit_plot_w.lineEdit_2.setText(str(self.figure_edited.kwarks["norm"][1]))

                self.edit_plot_w.finish_signal.connect(self.res_edit_plot)

            else:
                # on créer la nouvelle fenêtre
                self.edit_plot_w = Edit_plot(self)

                # on sauvegarde la figure édité
                self.figure_edited = self.console.current_data.current_figure

                # on change le label pour y affiche le nom de la figure courrante
                self.edit_plot_w.label.setText(self.console.current_data.current_figure.name)
                self.edit_plot_w.label.setFont(QFont(*self.resource.default_font))

                # on ajoute toutes les légendes des axes pour leurs édition
                # on commence par l'axe y1
                for i, data_array in enumerate(self.console.current_data.current_figure.y1_axe.data):
                    self.edit_plot_w.listWidget.addItem(data_array.legend)
                    # si l'axe est invisible, on passe l'écriture de la légende en rouge
                    if not data_array.visible:
                        self.edit_plot_w.listWidget.item(i).setForeground(QColor("red"))

                # de même pour l'axe y2
                if self.console.current_data.current_figure.y2_axe is not None:
                    for i, data_array in enumerate(self.console.current_data.current_figure.y2_axe.data):
                        self.edit_plot_w.listWidget.addItem(data_array.legend)
                        # si l'axe est invisible, on passe l'écriture de la légende en rouge
                        if not data_array.visible:
                            self.edit_plot_w.listWidget.item(i).setForeground(QColor("red"))

                self.edit_plot_w.listWidget.setCurrentRow(0)

                # on remplie l'edit line avec le zoom actuel
                self.edit_plot_w.lineEdit_4.setText(str(self.console.current_data.current_figure.margin))

                # on compléte le combobox avec le nom de toutes le couleurs disponible
                self.edit_plot_w.comboBox_left.addItem("unchanged")
                self.edit_plot_w.comboBox_left.addItem("default")
                for color in Resources.COLOR_MAP.keys():
                    self.edit_plot_w.comboBox_left.addItem(color)

                if self.figure_edited.y2_axe is not None:
                    # color right axis
                    self.edit_plot_w.comboBox_right = QtWidgets.QComboBox(self.edit_plot_w)
                    self.edit_plot_w.comboBox_right.setObjectName("comboBox_right")
                    self.edit_plot_w.gridLayout_2.addWidget(self.edit_plot_w.comboBox_right, 3, 2, 1, 1)
                    spacerItem5 = QtWidgets.QSpacerItem(40, 20, QtWidgets.QSizePolicy.Expanding,
                                                        QtWidgets.QSizePolicy.Minimum)
                    self.edit_plot_w.gridLayout_2.addItem(spacerItem5, 3, 1, 1, 1)
                    self.edit_plot_w.label_8 = QtWidgets.QLabel(self.edit_plot_w)
                    self.edit_plot_w.label_8.setObjectName("label_8")
                    self.edit_plot_w.gridLayout_2.addWidget(self.edit_plot_w.label_8, 3, 0, 1, 1)

                    _translate = QtCore.QCoreApplication.translate
                    self.edit_plot_w.label_8.setText(_translate("Dialog",
                                                                "<html><head/><body><p><span style=\" font-size:8pt;\">"
                                                                "Color right axis</span></p></body></html>"))

                    # type line right axis
                    self.edit_plot_w.comboBox_type_line_right = QtWidgets.QComboBox(self.edit_plot_w)
                    self.edit_plot_w.comboBox_type_line_right.setObjectName("comboBox_type_line_right")
                    self.edit_plot_w.gridLayout_2.addWidget(self.edit_plot_w.comboBox_type_line_right, 4, 2, 1, 1)
                    self.edit_plot_w.create_combobox_marker(self.edit_plot_w.comboBox_type_line_right)

                    spacerItem6 = QtWidgets.QSpacerItem(40, 20, QtWidgets.QSizePolicy.Expanding,
                                                        QtWidgets.QSizePolicy.Minimum)
                    self.edit_plot_w.gridLayout_2.addItem(spacerItem6, 4, 1, 1, 1)
                    self.edit_plot_w.label_9 = QtWidgets.QLabel(self.edit_plot_w)
                    self.edit_plot_w.label_9.setObjectName("label_9")
                    self.edit_plot_w.gridLayout_2.addWidget(self.edit_plot_w.label_9, 4, 0, 1, 1)

                    self.edit_plot_w.label_9.setText(_translate("Dialog",
                                                                "<html><head/><body><p><span style=\" font-size:8pt;\">"
                                                                "Style lines right axis</span></p></body></html>"))

                    self.edit_plot_w.comboBox_right.addItem("unchanged")
                    self.edit_plot_w.comboBox_right.addItem("default")
                    for color in Resources.COLOR_MAP.keys():
                        self.edit_plot_w.comboBox_right.addItem(color)

                # on connect le signal indiquant que l'édition est fini
                self.edit_plot_w.finish_signal.connect(self.res_edit_plot)

                # signal pour la création d'une figure servant à la supréssion de points
                self.edit_plot_w.edit_signal.connect(self.create_edit_plot)

            # on affiche la fenêtre
            self.edit_plot_w.show()

    """---------------------------------------------------------------------------------"""

    def res_edit_plot(self, signal):
        """
        fonction callback de la la fin de l'édition de la fenêtre édit plot
        pour le apply je n'est encire rien fait

        :param signal: save, cancel, apply
        :return: None
        """
        # si les oppérations ne sont pas sauvegardée, on del la fenêtre
        if signal == "cancel":
            self.edit_plot_w.deleteLater()
            self.edit_plot_w = None
            self.figure_edited = None

        # on savegarde les changements
        elif signal == "save":
            if self.edit_plot_w.__name__ == "Edit_plot":
                obj_figure = self.get_plot_from_figure(self.figure_edited)
                if len(self.edit_plot_dics) != 0:
                    # on applique la suppression des points effectuée sur les différentes courbes
                    self.process_del_point_plot(obj_figure)

                # on cache les courbes qui doivent l'être
                self.hide_data_array(obj_figure)

                # on applique la couleur
                colory1 = self.edit_plot_w.comboBox_left.itemText(self.edit_plot_w.comboBox_left.currentIndex())
                if colory1 == "unchanged":
                    pass
                elif colory1 == "default":
                    for data in self.figure_edited.y1_axe.data:
                        data.color = None
                    if obj_figure is not None:
                        obj_figure.reset_color_plot("y1")
                else:
                    self.figure_edited.y1_axe.color_map = colory1
                    self.figure_edited.y1_axe.apply_color()

                    if obj_figure is not None:
                        obj_figure.update_color_plot("y1")

                # on applique le nouveau marker
                left_axis_line = self.edit_plot_w.comboBox_type_line_left.itemText \
                    (self.edit_plot_w.comboBox_type_line_left.currentIndex())

                # si la valeurs est à unchanged on n'a rien à faire
                if left_axis_line != "unchanged":
                    # on récupére la key de la value
                    for key, value in Resources.MARKERS_PLOT.items():
                        if value == left_axis_line:
                            left_axis_line = key
                            break

                    # si left_axis_line == -- c'est que l'on reset en ligne
                    if left_axis_line == "__":
                        self.figure_edited.format_line_y1 = None

                        # si le plot est ouvert, on l'update
                        if obj_figure is not None:
                            obj_figure.reset_marker_plot("y1")

                    else:
                        # on update format_line_y1 de figure_edited avec la nouvelle valeur
                        self.figure_edited.format_line_y1 = left_axis_line

                        # si le plot est ouvert, on l'update
                        if obj_figure is not None:
                            obj_figure.update_marker_plot("y1", left_axis_line)

                if self.figure_edited.y2_axe is not None:
                    colory2 = self.edit_plot_w.comboBox_right.itemText(self.edit_plot_w.comboBox_right.currentIndex())
                    if colory2 == "unchanged":
                        pass
                    elif colory2 == "default":
                        for data in self.figure_edited.y2_axe.data:
                            data.color = None
                        if obj_figure is not None:
                            obj_figure.reset_color_plot("y2")
                    else:
                        self.figure_edited.y2_axe.color_map = colory2
                        self.figure_edited.y2_axe.apply_color()

                        if obj_figure is not None:
                            obj_figure.update_color_plot("y2")

                    # on applique le nouveau marker
                    right_axis_line = self.edit_plot_w.comboBox_type_line_right.itemText \
                        (self.edit_plot_w.comboBox_type_line_right.currentIndex())

                    # si la valeurs est à unchanged on n'a rien à faire
                    if right_axis_line != "unchanged":
                        # on récupére la key de la value
                        for key, value in Resources.MARKERS_PLOT.items():
                            if value == right_axis_line:
                                right_axis_line = key
                                break

                        # si right_axis_line == -- c'est que l'on reset en ligne
                        if right_axis_line == "__":
                            self.figure_edited.format_line_y2 = None

                            # si le plot est ouvert, on l'update
                            if obj_figure is not None:
                                obj_figure.reset_marker_plot("y2")

                        else:
                            # on update format_line_y1 de figure_edited avec la nouvelle valeur
                            self.figure_edited.format_line_y2 = right_axis_line

                            # si le plot est ouvert, on l'update
                            if obj_figure is not None:
                                obj_figure.update_marker_plot("y2", right_axis_line)

                # on applique la marge
                margin = float(self.edit_plot_w.lineEdit_4.text())
                # si il y a eu un chagement
                if self.figure_edited.margin != margin:
                    # on garde en mémoire la marge précédente
                    old_margin = self.figure_edited.margin
                    self.figure_edited.margin = margin
                    if obj_figure is not None:
                        Abstract_data.resize_axe(obj_figure.abstract_affiche.ax1, obj_figure.abstract_affiche.ax2,
                                                 margin,
                                                 old_margin)

                # on met à jours le figure
                if obj_figure is not None:
                    obj_figure.canvas.draw()

                # l'édition étant terminé on clear le vecteur qui gardais en mémoire les éditions
                self.edit_plot_dics.clear()

                # on délect la fenêtre
                self.edit_plot_w.deleteLater()
                self.edit_plot_w = None
                # passe a None la figure édité
                self.figure_edited = None

            elif self.edit_plot_w.__name__ == "Edit_plot_contour":

                edit = False

                obj_figure = self.get_plot_from_figure(self.figure_edited)

                colory1 = self.edit_plot_w.comboBox_left.itemText(self.edit_plot_w.comboBox_left.currentIndex())
                if colory1 == "unchanged":
                    pass
                elif colory1 == "default":
                    self.figure_edited.y1_axe.color_map = None
                    edit = True
                else:
                    self.figure_edited.y1_axe.color_map = colory1
                    edit = True

                if self.edit_plot_w.lineEdit.text() != "":
                    _min = self.edit_plot_w.lineEdit.get_value()
                else:
                    _min = -1

                if self.edit_plot_w.lineEdit_2.text() != "":
                    _max = self.edit_plot_w.lineEdit_2.get_value()
                else:
                    _max = -1

                if _min != -1 or _max != -1:
                    if "norm" not in self.figure_edited.kwarks:
                        self.figure_edited.kwarks["norm"] = [_min, _max]
                        edit = True
                    else:
                        if _min != self.figure_edited.kwarks["norm"][0] or _max != self.figure_edited.kwarks["norm"][1]:
                            self.figure_edited.kwarks["norm"] = [_min, _max]
                            edit = True

                if edit:
                    obj_figure.update_contour_plot()

                self.edit_plot_w.deleteLater()
                self.edit_plot_w = None
                self.figure_edited = None

        else:
            raise NotImplementedError

    """---------------------------------------------------------------------------------"""

    def create_edit_plot(self, signal):
        """
        On créer la figure qui servira a sélectionner les points a supprimer
        Cette figure correspondra à un cycle de self.figure_edited

        :param signal: current_index de la listWidget
        :return: None
        """
        # si une figure d'édition est déjà ouverte, ou return
        # un message a ajouter ici par la suite
        if self.edit_plot_figure_w is not None:
            self.update_console({"str": "One figure is already being edited", "foreground_color": "red"})
            return

        # création d'une nouvelle figure avec pour nom la légende du cycle sélectionné
        new_figure = Figure(self.edit_plot_w.listWidget.currentItem().text(), 1)

        # on ajoute à la nouvelle figure interactive une copie de data_x correspondant à l'index sélectionné
        new_figure.add_data_x_Data(copy.copy(self.figure_edited.x_axe.data[signal]))

        # on ajoute à la nouvelle figure interactive une copie de data_y correspondant à l'index sélectionné
        # on utilise get_data_yaxe_i pour récupérer data_array, qu'il soit en y1 ou y2 en fonction de l'index
        data_y1 = copy.copy(self.figure_edited.get_data_yaxe_i(signal))

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
        self.edit_plot_figure_w = Figure_plot(edit_affiche, self)

        # on connect de callback, on utilise lambda pour passer signal comme arg suplémentaire
        self.edit_plot_figure_w.closed.connect(lambda event: self.edit_plot_figure_w_close(event, signal))

        # on passe le plot d'édition en modal
        self.edit_plot_figure_w.setWindowModality(QtCore.Qt.ApplicationModal)

        # on passe la fenêtre d'édition en non modal
        self.edit_plot_w.setWindowModality(QtCore.Qt.NonModal)

        # on affiche le widget
        self.edit_plot_figure_w.show()

    """---------------------------------------------------------------------------------"""

    def hide_data_array(self, obj_plot):
        """
        On set sivible du data_array de chacune des courbes, False si elles doivent être
        caché et True sinon

        :param obj_plot: objet plot de matplotlib
        :return: obj_figure_plot correspondant à la figure édité
        """

        # on update current figure pour passer en hide les éléments indiqué
        for i in range(self.edit_plot_w.listWidget.count()):
            # si la couleur du text est rouge, la courbe doit être cachée
            if self.edit_plot_w.listWidget.item(i).foreground().color() == QColor("red"):
                # on update Data_array
                self.figure_edited.get_data_yaxe_i(i).visible = False
                self.figure_edited.x_axe.data[i].visible = False

                if obj_plot is not None:
                    # on regarde l'index de l'axe y en fonction de celui de l'axe x
                    # si l'index de laxe x est plus grande que len(y1_axe)
                    # c'est l'axe y2 qui est édité
                    if i >= len(self.figure_edited.y1_axe.data):
                        # on recalcule l'index
                        index = i - len(self.figure_edited.y1_axe.data)
                        # c'est l'axe y2 qui est édité

                        obj_plot.set_visibility_2d_line("y2", index, False)
                    else:
                        # rien à faire ici
                        index = i
                        # c'est l'axe y1 qui est édité
                        obj_plot.set_visibility_2d_line("y1", index, False)
            else:
                # on update Data_array
                self.figure_edited.get_data_yaxe_i(i).visible = True
                self.figure_edited.x_axe.data[i].visible = True

                if obj_plot is not None:
                    # on regarde l'index de l'axe y en fonction de celui de l'axe x
                    # si l'index de laxe x est plus grande que len(y1_axe)
                    # c'est l'axe y2 qui est édité
                    if i >= len(self.figure_edited.y1_axe.data):
                        # on recalcule l'index
                        index = i - len(self.figure_edited.y1_axe.data)
                        # c'est l'axe y2 qui est édité
                        obj_plot.set_visibility_2d_line("y2", index, True)
                    else:
                        # rien à faire ici
                        index = i
                        # c'est l'axe y1 qui est édité
                        obj_plot.set_visibility_2d_line("y1", index, True)

    """---------------------------------------------------------------------------------"""

    def process_del_point_plot(self, obj_figure):
        """
        Effectue la mise à jours des figures et des plots correspondant aux éditions effectuées

        :return: None
        """

        # key : x_index de l'édition
        # value : [new_datax, new_datay]
        for key, value, in self.edit_plot_dics.items():

            # si l'index est plus grand que le nombre de data dans y1_axe, c'est un index pour
            # l'axe y2
            if key >= len(self.figure_edited.y1_axe.data):
                # on calcule l'index pour l'axe y2
                y2_index = key - len(self.figure_edited.y1_axe.data)

                # on update current_figure avec les valeurs de value
                self.figure_edited.x_axe.data[key].data = value[0]
                self.figure_edited.y2_axe.data[y2_index].data = value[1]

                if obj_figure is not None:
                    obj_figure.update_plot("y2", y2_index, value[0], value[1])
            else:
                # on update current_figure avec les valeurs de value
                self.figure_edited.x_axe.data[key].data = value[0]
                self.figure_edited.y1_axe.data[key].data = value[1]

                if obj_figure is not None:
                    obj_figure.update_plot("y1", key, value[0], value[1])

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

        self.edit_plot_figure_w.deleteLater()
        self.edit_plot_figure_w = None

        # on passe la fenêtre de selection en modal
        self.edit_plot_w.setWindowModality(QtCore.Qt.ApplicationModal)

    """---------------------------------------------------------------------------------"""
    """                            Edit Current Plot end                                """
    """---------------------------------------------------------------------------------"""

    """---------------------------------------------------------------------------------"""
    """                            pics fitting start                                   """
    """---------------------------------------------------------------------------------"""

    def callback_pic_selection(self, event):
        """
        fonction callback de la selection dpics pour le fitting
        Si la selection est correct on créer un thread pour faire le fitting
        sinon on return juste


        :param event: sans importance
        :return: None
        """

        # on récupére les pics selectionnés
        pics = []
        for i in range(len(self.edit_plot_figure_w.abstract_affiche.pics)):
            pics.append([])
            for j in range(len(self.edit_plot_figure_w.abstract_affiche.pics[i])):
                pics[i].append(self.edit_plot_figure_w.abstract_affiche.pics[i][j])

        pplot.close(self.edit_plot_figure_w.abstract_affiche.pplot_fig)
        self.edit_plot_figure_w.deleteLater()
        self.edit_plot_figure_w = None

        # rien à faire dans ce cas
        if len(pics) == 0:
            return

        file = open(r"C:\Users\Maxime\Desktop\export_diffraction.txt", "w")

        for i in range(len(self.console.current_data.current_figure.x_axe.data)):
            s = ""
            for j in range(len(self.console.current_data.current_figure.x_axe.data[i].data)):
                s += str(self.console.current_data.current_figure.x_axe.data[i].data[j]) + "\t"
            s = s[:-1] + "\n"
            file.write(s)
            print(s)
            s = ""
            for j in range(len(self.console.current_data.current_figure.x_axe.data[i].data)):
                s += str(self.console.current_data.current_figure.y1_axe.data[i].data[j]) + "\t"
            s = s[:-1] + "\n"
            file.write(s)
            print(s)
        file.close()

        # création d'un nouveau thread
        t = QThread()

        # création du worker
        worker = Fitting(self.console.current_data.current_figure, pics)
        worker.moveToThread(t)

        # connection
        t.started.connect(worker.run)
        worker.finished.connect(self.callback_fitting)

        # on garde une ref du thread
        self.threads.append([t, worker])

        # start
        t.start()

        """worker = Fitting(self.console.current_data.current_figure, pics)
        worker.run()"""

    """---------------------------------------------------------------------------------"""

    def callback_fitting(self):
        """
        fonctione callbak du fitting, on créer la figure résultat

        :return: None
        """
        index = 0
        # on parcours les threads de lecture en cours
        while index < len(self.threads):
            if type(self.threads[index][1]).__name__ == "Fitting" and self.threads[index][1].finished:
                center = self.threads[index][1].center
                area = self.threads[index][1].area
                fwhm = self.threads[index][1].fwhm

                figure = self.threads[index][1].figure

                init_index_min = self.threads[index][1].init_index_min
                init_index_max = self.threads[index][1].init_index_max

                init_center = self.threads[index][1].init_center

                # on termine le thread
                self.threads[index][0].terminate()

                # on le suprime de la liste
                del self.threads[index]

                nb_pics = len(center[0])

                new_xmax = []
                for i in range(nb_pics):
                    new_xmax.append([])
                    for j in range(len(center)):
                        new_xmax[-1].append(center[j][i])

                # création du vecteur area
                new_area = []
                for i in range(nb_pics):
                    new_area.append([])
                    for j in range(len(area)):
                        new_area[-1].append(area[j][i])

                # création du vecteur largeur
                newlargeur = []
                for i in range(nb_pics):
                    newlargeur.append([])
                    for j in range(len(fwhm)):
                        newlargeur[-1].append(fwhm[j][i])

                if "waxs" in figure.type:
                    figure_res = Figure("Diffraction res " + str(figure.x_axe.data[0].data[init_index_min])[0:6] + " " +
                                        str(figure.x_axe.data[0].data[init_index_max])[0:6], 1, init_center=init_center)

                    figure_res.plot_name = "Diffraction res " + str(figure.x_axe.data[0].data[init_index_min])[
                                                                0:6] + " " + \
                                           str(figure.x_axe.data[0].data[init_index_max])[0:6]
                    figure_res.type = "res_fitting_temps"
                    figure_res.created_from = figure

                    units = Units()
                    x_unit = units.get_unit(figure.x_axe.get_unit().name)
                    y_unit = units.get_unit(figure.y1_axe.get_unit().name)

                    array_time = figure.kwarks["array_time"]

                    for i in range(len(new_xmax)):
                        data_unit_x = Data_unit(copy.copy(array_time), x_unit)
                        data_unit_y = Data_unit(new_xmax[i], y_unit)

                        temp_x = Data_array(data_unit_x, "time", None, "nesaisias", temperature="warning")
                        temp_y = Data_array(data_unit_y, "ua", None, "nesaispas")
                        figure_res.add_data_x_Data(temp_x)
                        figure_res.add_data_y1_Data(temp_y)

                    for i in range(len(new_area)):
                        data_unit_x = Data_unit(copy.copy(array_time), x_unit)
                        data_unit_y = Data_unit(new_area[i], y_unit)

                        temp_x = Data_array(data_unit_x, "Température", None, "nesaisias", temperature="warning")
                        temp_y = Data_array(data_unit_y, "diffraction", None, "nesaispas")
                        figure_res.add_data_x_Data(temp_x)
                        figure_res.add_data_y1_Data(temp_y)

                    for i in range(len(newlargeur)):
                        data_unit_x = Data_unit(copy.copy(array_time), x_unit)
                        data_unit_y = Data_unit(newlargeur[i], y_unit)

                        temp_x = Data_array(data_unit_x, "Température", None, "nesaisias", temperature="cooling")
                        temp_y = Data_array(data_unit_y, "diffraction", None, "nesaispas")
                        figure_res.add_data_x_Data(temp_x)
                        figure_res.add_data_y1_Data(temp_y)

                else:

                    figure_res = Figure("Diffraction res " + str(figure.x_axe.data[0].data[init_index_min])[0:6] + " " +
                                        str(figure.x_axe.data[0].data[init_index_max])[0:6], 1, init_center=init_center)

                    figure_res.plot_name = "Diffraction res " + str(figure.x_axe.data[0].data[init_index_min])[
                                                                0:6] + " " + \
                                           str(figure.x_axe.data[0].data[init_index_max])[0:6]
                    figure_res.type = "res_fitting_temperature"
                    figure_res.created_from = figure

                    units = Units()
                    x_unit = units.get_unit(figure.x_axe.get_unit().name)
                    y_unit = units.get_unit(figure.y1_axe.get_unit().name)

                    size_w = 0
                    size_c = 0
                    warning_x = []
                    for i in range(len(self.console.current_data.data["loop_data"])):
                        if self.console.current_data.data["loop_data"][i][2] == "w":
                            warning_x.append(self.console.current_data.data["loop_data"][i][3])
                            size_w += 1

                    cooling_x = []
                    for i in range(len(self.console.current_data.data["loop_data"])):
                        if self.console.current_data.data["loop_data"][i][2] == "c":
                            cooling_x.append(self.console.current_data.data["loop_data"][i][3])
                            size_c += 1

                    # new_xmax
                    if size_w != 0:
                        for i in range(len(new_xmax)):
                            data_unit_x = Data_unit(copy.copy(warning_x), x_unit)
                            data_unit_y = Data_unit(new_xmax[i][0:size_w], y_unit)

                            temp_x = Data_array(data_unit_x, "Température", None, "nesaisias", temperature="warning")
                            temp_y = Data_array(data_unit_y, "diffraction", None, "nesaispas")
                            figure_res.add_data_x_Data(temp_x)
                            figure_res.add_data_y1_Data(temp_y)

                    if size_c != 0:
                        for i in range(len(new_xmax)):
                            data_unit_x = Data_unit(copy.copy(cooling_x), x_unit)
                            data_unit_y = Data_unit(new_xmax[i][size_w:], y_unit)

                            temp_x = Data_array(data_unit_x, "Température", None, "nesaisias", temperature="cooling")
                            temp_y = Data_array(data_unit_y, "diffraction", None, "nesaispas")
                            figure_res.add_data_x_Data(temp_x)
                            figure_res.add_data_y1_Data(temp_y)

                    # new_area
                    if size_w != 0:
                        for i in range(len(new_area)):
                            data_unit_x = Data_unit(copy.copy(warning_x), x_unit)
                            data_unit_y = Data_unit(new_area[i][0:size_w], y_unit)

                            temp_x = Data_array(data_unit_x, "Température", None, "nesaisias", temperature="warning")
                            temp_y = Data_array(data_unit_y, "diffraction", None, "nesaispas")
                            figure_res.add_data_x_Data(temp_x)
                            figure_res.add_data_y1_Data(temp_y)

                    if size_c != 0:
                        for i in range(len(new_area)):
                            data_unit_x = Data_unit(copy.copy(cooling_x), x_unit)
                            data_unit_y = Data_unit(new_area[i][size_w:], y_unit)

                            temp_x = Data_array(data_unit_x, "Température", None, "nesaisias", temperature="cooling")
                            temp_y = Data_array(data_unit_y, "diffraction", None, "nesaispas")
                            figure_res.add_data_x_Data(temp_x)
                            figure_res.add_data_y1_Data(temp_y)

                    # new fwhm
                    if size_w != 0:
                        for i in range(len(newlargeur)):
                            data_unit_x = Data_unit(copy.copy(warning_x), x_unit)
                            data_unit_y = Data_unit(newlargeur[i][0:size_w], y_unit)

                            temp_x = Data_array(data_unit_x, "Température", None, "nesaisias", temperature="warning")
                            temp_y = Data_array(data_unit_y, "diffraction", None, "nesaispas")
                            figure_res.add_data_x_Data(temp_x)
                            figure_res.add_data_y1_Data(temp_y)

                    if size_c != 0:
                        for i in range(len(newlargeur)):
                            data_unit_x = Data_unit(copy.copy(cooling_x), x_unit)
                            data_unit_y = Data_unit(newlargeur[i][size_w:], y_unit)

                            temp_x = Data_array(data_unit_x, "Température", None, "nesaisias", temperature="cooling")
                            temp_y = Data_array(data_unit_y, "diffraction", None, "nesaispas")
                            figure_res.add_data_x_Data(temp_x)
                            figure_res.add_data_y1_Data(temp_y)

                # on update le tree widget
                # on ajoute la figure a current_data
                self.treeWidget.add_figure(figure_res, self.console.current_data.name)
                self.console.current_data.figures.append(figure_res)

                # on passe la figure en figure courante
                self.console.current_data.current_figure = figure_res

                # on update le label avec le nouveau nom de la figure
                self.update_figure_name()

                # on update les actions disponibles pour cette figure
                self.update_action_combo()
                break
            index += 1

    """---------------------------------------------------------------------------------"""
    """                              pics fitting end                                   """
    """---------------------------------------------------------------------------------"""

    """---------------------------------------------------------------------------------"""
    """                        Vieux data current plot start                            """
    """---------------------------------------------------------------------------------"""

    def view_data_Current_Plot(self):
        """
        Callback du boutton View data current plot
        On check qu'un plot est bien sélectionné et on lui demande
        d'ouvrir la fenêtre de sélection des données a affichées

        Le fait de séléctionné les données et d'afficher ensuite une fenêtre avec
        les valeurs des données sera entiérement gérer par le plot lui même et non
        par la main window

        :param event: peu importe
        :return: None
        """

        if self.console.current_data is None:
            self.current_data_None()
        elif self.console.current_data.current_figure is None:
            self.current_figure_None()
        else:
            plot_obj = self.get_plot_from_figure(self.console.current_data.current_figure)
            if plot_obj is None:
                self.QMessageBox_str("No graphics are open")
                return
            else:
                if plot_obj.abstract_affiche.__name__ != "Classique_affiche":
                    self.update_console(
                        {"str": "Impossible to view data on this type of graph", "foreground_color": "red"})
                elif not plot_obj.abstract_affiche.figure.x_axe.data[0].global_index:
                    self.update_console(
                        {"str": "Impossible to view data on this type of graph", "foreground_color": "red"})
                else:
                    self.obj_plot_show_value = plot_obj

                    self.select_value_show_w = Edit_view_data(self)
                    for data_name in self.console.current_data.data["row_data"]:
                        self.select_value_show_w.listWidget.addItem(data_name)

                    self.select_value_show_w.finish_signal.connect(self.view_data_Current_Plot_callback)
                    self.select_value_show_w.show()

    def view_data_Current_Plot_callback(self, signal):
        """
        Callback de la fermeture de l'édition
        :param signal: cancel / save
        :return:
        """

        # si les donnée sont sauvegardé on créer une list view pour l'affichage des données
        if signal == "cancel":
            self.obj_plot_show_value = None
            self.select_value_show_w.deleteLater()
            self.select_value_show_w = None
        else:
            if len(self.select_value_show_w.names_selected) != 0:
                names_selected = self.select_value_show_w.names_selected
                self.obj_plot_show_value.init_window_view_data(names_selected)
                self.obj_plot_show_value = None
                self.select_value_show_w.deleteLater()
                self.select_value_show_w = None

    """---------------------------------------------------------------------------------"""
    """                        Vieux data current plot  end                             """
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

    def QMessageBox_str(self, str):
        """
        QMessageBox indiquand qu'une action sur un plot ou une data
        a été demandé dans que des datas est été chargé

        :return: None
        """
        msgBox = QMessageBox()
        msgBox.setIcon(QMessageBox.Warning)
        msgBox.setText(str)
        msgBox.setWindowTitle("Error")
        msgBox.setStandardButtons(QMessageBox.Ok)
        msgBox.exec()

    """---------------------------------------------------------------------------------"""


class Main_interface:
    def __init__(self):
        app = QApplication(sys.argv)
        win = Window()
        win.show()
        sys.exit(app.exec())
