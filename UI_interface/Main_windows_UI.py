import copy
import sys

import matplotlib

from PyQt5 import QtCore, QtWidgets
from PyQt5.QtCore import QThread
from PyQt5.QtGui import QColor, QFont
from PyQt5.QtWidgets import (
    QApplication, QDialog, QMainWindow, QMessageBox, QFileDialog
)

import matplotlib.pyplot as pplot
from Console_Objets.Affiche_objet import Classique_affiche, Edit_affiche
from Console_Objets.Console import Console
from Console_Objets.Data_array import Data_array
from Console_Objets.Figure import Figure
from Data_type import Abstract_data
from Data_type.CCCV_data import CCCV_data
from Resources_file import Resources
from Resources_file.Emit import Emit
from UI_interface import Threads_UI
from UI_interface.Ask_Value_QT import Ask_Value
from UI_interface.Derive_Selection_QT import Derive_Selection
from UI_interface.Figure_plot_QT import Figure_plot
from UI_interface.Main_window_QT import Ui_MainWindow
from UI_interface.Edit_view_data_QT import Edit_view_data
from UI_interface.Cycle_Selection_QT import Cycle_Selection
from UI_interface.Edit_plot_QT import Edit_plot

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
        self.actionEdit_Current_Plot.triggered.connect(self.edit_current_plot)
        self.actionview_data_Current_Plot.triggered.connect(self.view_data_Current_Plot)

        self.pushButton_5.clicked.connect(self.create_current_data)
        self.pushButton_4.clicked.connect(self.create_figure)
        self.treeWidget.clicked.connect(self.tree_click)
        self.tabWidget.tabCloseRequested.connect(self.close_tab_handler)
        self.tabWidget.name_changed_tab.connect(self.name_changed_tab)
        self.tabWidget.break_tab.connect(self.break_tab)
        self.tabWidget.change_current.connect(self.tab_changed)

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

        self.figure_plot = Figure_plot(obj, self)
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
                    self.argument_selection_creation_w = Ask_Value(self, "float", "Invalide mass Electode", "New Mass (mg) : ")
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

    """---------------------------------------------------------------------------------"""

    def callback_create_current_data(self, event, name):
        """

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

                # on update le tree widget
                # on ajoute la figure a current_data
                self.treeWidget.add_figure(figure_res, self.console.current_data.name)
                self.console.current_data.figures.append(figure_res)

                # on passe la figure en figure courante
                self.console.current_data.current_figure = figure_res

            _translate = QtCore.QCoreApplication.translate
            self.label_5.setText(
                _translate("MainWindow", "<html><head/><body><p><span style=\" font-size:11pt;\">"
                                         "Current plot : "
                           + self.console.current_data.current_figure.name + " </span></p></body></html>"))

            # on update les actions disponibles pour cette figure
            self.update_action_combo()

    """---------------------------------------------------------------------------------"""

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

            elif name == "shift x" or name == "shift y":
                value = self.argument_selection_creation_w.value
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

            _translate = QtCore.QCoreApplication.translate
            self.label_5.setText(
                _translate("MainWindow", "<html><head/><body><p><span style=\" font-size:11pt;\">"
                                         "Current plot : "
                           + self.console.current_data.current_figure.name + " </span></p></body></html>"))

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
                        if self.tabWidget.tabText(i) == figure.name:

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

                            # on passe les fenêtre plot en lower
                            self.lower_plot_w()
                            return

                    # check si la figure est ouverte en fenêtre
                    if self.on_top_plot_w(figure.name):
                        return

                    # à ce point de la fonction, le plot n'existe pas, il faut le créer
                    obj = Classique_affiche(self.console.current_data, figure)
                    new_tab = Figure_plot(obj, self)
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
            # on clear la box action
            self.comboBox_4.clear()

            # on passe la current_figure à None
            self.console.current_data.current_figure = None

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

                        # on update current data avec ne nom du nouveau fichier
                        _translate = QtCore.QCoreApplication.translate
                        self.label.setText(
                            _translate("MainWindow", "<html><head/><body><p><span style=\" font-size:11pt;\">"
                                                     "Current data : "
                                       + obj_data.name + " </span></p></body></html>"))

                        self.update_console({"str": "Done", "foreground_color": "green"})

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

        self.tabWidget.widget(index).close_view_values()

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

        # on update les actions disponibles pour cette figure
        self.update_action_combo()

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

        parent = self.treeWidget.get_top_item(new_name)

        # on reset la selection du treewidget
        self.treeWidget.clearSelection()
        # on récupére l'item
        item = self.treeWidget.get_item(new_name)
        # on set le focus sur lui
        item.setSelected(True)

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

        # on update les actions disponibles pour cette figure
        self.update_action_combo()

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
        # pour ne pas déclancher des erreurs à la création de la fenêtre
        # si current_index == -1 c'est qu'il n'y a plus de tab parce qu'elle a été détachée
        # on update pas les lable et la console dans ce cas
        if self.console.current_data is None or self.console.current_data.current_figure is None or \
                self.tabWidget.currentIndex() == -1:
            return



        # le nom de la figure courrante est donc celui de la tab courrante
        new_name = self.tabWidget.tabText(self.tabWidget.currentIndex())

        # si le nom est le même que celui de la figure courante, il est inutile d'update quoi que ce soit
        # rien n'a été modifié, c'est jsute un clique sur l'interface
        if new_name == self.console.current_data.current_figure.name:
            return

        _translate = QtCore.QCoreApplication.translate

        # on update le label current plot
        self.label_5.setText(_translate("MainWindow", "<html><head/><body><p><span style=\" font-size:11pt;\">"
                                                      "Current plot : "
                                        + new_name +
                                        " </span></p></body></html>"))

        # on update la figure courrante de la console
        self.console.current_data.set_current_figure_name(new_name)

        # on update les actions disponibles pour cette figure
        self.update_action_combo()

        # on update l'item focus par tree widget
        for i in range(self.treeWidget.topLevelItem(0).childCount()):
            if self.treeWidget.topLevelItem(0).child(i).text(0) == new_name:
                self.treeWidget.setCurrentItem(self.treeWidget.topLevelItem(0).child(i))
                break

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
                              background-color:
                              foreground-color
                              font

        :return: None
        """

        # on crééer un nouvel item
        item = QtWidgets.QListWidgetItem()
        # il ne doit pas être interactif
        item.setFlags(QtCore.Qt.NoItemFlags)
        # on set le text
        item.setText(signal["str"])

        # on check dans le dict de signal les arguments pour la mise en forme du text
        if "background_color:" in signal:
            item.setBackground(QColor(signal["background_color:"]))

        if "foreground_color" in signal:
            item.setForeground(QColor(signal["foreground_color"]))

        if "font" in signal:
            item.setFont(QFont(signal["font"]))
        else:
            item.setFont(QFont(*self.resource.default_font))

        # on add l'item à la listWidget
        self.listWidget.addItem(item)

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
                    Abstract_data.resize_axe(obj_figure.abstract_affiche.ax1, obj_figure.abstract_affiche.ax2, margin,
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

    """---------------------------------------------------------------------------------"""
    """                            Edit Current Plot end                                """
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
