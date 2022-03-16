import warnings

import matplotlib
import numpy as np
from PyQt5 import QtCore
from PyQt5.QtCore import pyqtSignal
from PyQt5.QtWidgets import QWidget, QVBoxLayout, QInputDialog, QLineEdit
from matplotlib.backend_bases import MouseButton
from matplotlib.backends.backend_qt import NavigationToolbar2QT
from matplotlib.backends.backend_qtagg import FigureCanvasQTAgg as FigureCanvas
from matplotlib.colorbar import Colorbar
from matplotlib.contour import QuadContourSet

import Data_type.Abstract_data
from Resources_file.Emit import Emit
from UI_interface.Edit_Axe_QT import Edit_Axe
from UI_interface.View_data_value_QT import View_data_value


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

    def __init__(self, abstract_affiche, parent=None):
        super().__init__()

        # self.setWindowFlags(QtCore.Qt.Dialog)

        self.canvas = None
        self.toolbar = None
        self.edit_w = None
        self.axe_edited = None

        # focus policy
        self.setFocusPolicy(QtCore.Qt.TabFocus)
        self.setFocus()

        # abstract_affiche
        self.abstract_affiche = abstract_affiche

        # variable qui garde en mémoire la fenêtre d'affichage des valeurs
        self.view_data_value = None

        # Array qui garde en méoire les noms des data a être affiché dans en plus lors de l'intération
        # avec un graph cela ne se fera que si self.abstract_affiche est Classique_affiche
        self.array_data_displayed = []

        # on récupére une instance de Emit
        self.emit = Emit()

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

        # pour que key_event fonctionne....
        self.canvas.setFocusPolicy(QtCore.Qt.ClickFocus)
        self.canvas.setFocus()

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
        # self.canvas.mpl_connect('button_press_event', self.on_key)

        # on connect abstract_affiche
        self.abstract_affiche.connect_all()

        # si c'est gitt_affich on lui donne une fonction de callbak pour fermer le
        # plot, dans ce cas, à voir si il y en a besoin par la suite, probablement
        if type(self.abstract_affiche).__name__ == "Gitt_affiche" or \
                type(self.abstract_affiche).__name__ == "Impedance_affiche" or \
                type(self.abstract_affiche).__name__ == "Time_Selection" or \
                type(self.abstract_affiche).__name__ == "Saxs_selection":
            self.abstract_affiche.call_back_func = self.call_back_func

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

        self.focus_in.emit(self.abstract_affiche.figure.name)

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
        # on check que le plot n'est pas un contour plot avec isinstance(self.abstract_affiche.ax2, QuadContourSet)
        # dans ce cas on ne fait rien, ax2 n'est pas un axe mais la colorbar
        elif self.abstract_affiche.ax2 is not None and not isinstance(self.abstract_affiche.ax2, QuadContourSet) and \
                (self.abstract_affiche.ax2.yaxis.contains(event)[0] or
                 self.abstract_affiche.ax2.yaxis.get_label().contains(event)[0]):

            self.edit_y2_axe()

        # check du suptitle
        elif self.abstract_affiche.pplot_fig._suptitle.contains(event)[0]:
            self.edit_suptitle()

        elif isinstance(self.abstract_affiche.value, Colorbar) and \
                self.abstract_affiche.value.ax.yaxis.get_label().contains(event)[0]:
            self.edit_color_bar()

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

    def on_key(self, event):
        pass

    """---------------------------------------------------------------------------------"""

    def edit_x_axe(self):
        """
        fonction appellée pour editer l'axe des x

        :return: None
        """
        if self.edit_w is None:
            self.axe_edited = "x"
            self.edit_w = Edit_Axe(self)
            _translate = QtCore.QCoreApplication.translate
            self.edit_w.label.setText(_translate("Form",
                                                 "<html><head/><body><p align=\"center\"><span style=\" font-size:14pt;"
                                                 "\">Edit " + self.abstract_affiche.figure.x_axe.name +
                                                 " :</span></p></body></html>"))
            self.edit_w.lineEdit_2.setText(self.abstract_affiche.figure.x_axe.name)

            if self.abstract_affiche.figure.x_axe.scale == "Linear":
                self.edit_w.comboBox_18.setCurrentIndex(0)
            elif self.abstract_affiche.figure.x_axe.scale == "Log":
                self.edit_w.comboBox_18.setCurrentIndex(1)

            # création de la combo box avec les unités disponibles
            self.edit_w.comboBox_19.addItem("unchanged")
            if self.abstract_affiche.figure.x_axe.data[0].unit is not None:
                for unit in self.abstract_affiche.figure.x_axe.data[0].unit.get_units_available():
                    self.edit_w.comboBox_19.addItem(unit.fullname)

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
            self.edit_w = Edit_Axe(self)
            _translate = QtCore.QCoreApplication.translate
            self.edit_w.label.setText(_translate("Form",
                                                 "<html><head/><body><p align=\"center\"><span style=\" font-size:14pt;"
                                                 "\">Edit " + self.abstract_affiche.figure.y1_axe.name +
                                                 " :</span></p></body></html>"))
            self.edit_w.lineEdit_2.setText(self.abstract_affiche.figure.y1_axe.name)
            if self.abstract_affiche.figure.y1_axe.scale == "Linear":
                self.edit_w.comboBox_18.setCurrentIndex(0)
            elif self.abstract_affiche.figure.y1_axe.scale == "Log":
                self.edit_w.comboBox_18.setCurrentIndex(1)

            # création de la combo box avec les unités disponibles
            self.edit_w.comboBox_19.addItem("unchanged")
            if self.abstract_affiche.figure.y1_axe.data[0].unit is not None:
                for unit in self.abstract_affiche.figure.y1_axe.data[0].unit.get_units_available():
                    self.edit_w.comboBox_19.addItem(unit.fullname)

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
            self.edit_w = Edit_Axe(self)
            _translate = QtCore.QCoreApplication.translate
            self.edit_w.label.setText(_translate("Form",
                                                 "<html><head/><body><p align=\"center\"><span style=\" font-size:14pt;"
                                                 "\">Edit " + self.abstract_affiche.figure.y2_axe.name +
                                                 " :</span></p></body></html>"))
            self.edit_w.lineEdit_2.setText(self.abstract_affiche.figure.y2_axe.name)
            if self.abstract_affiche.figure.y2_axe.scale == "Linear":
                self.edit_w.comboBox_18.setCurrentIndex(0)
            elif self.abstract_affiche.figure.y2_axe.scale == "Log":
                self.edit_w.comboBox_18.setCurrentIndex(1)

            # création de la combo box avec les unités disponibles
            self.edit_w.comboBox_19.addItem("unchanged")
            if self.abstract_affiche.figure.y2_axe.data[0].unit is not None:
                for unit in self.abstract_affiche.figure.y2_axe.data[0].unit.get_units_available():
                    self.edit_w.comboBox_19.addItem(unit.fullname)

            self.edit_w.finish.connect(self.edit_finishded)
            self.edit_w.show()

    """---------------------------------------------------------------------------------"""

    def edit_color_bar(self):
        """
        fonction appellée pour editer la colorbar du graph

        :return: None
        """
        old_name = self.abstract_affiche.figure.z1_axe.name
        name = QInputDialog.getText(self, "Name change", "New name ?", QLineEdit.Normal, old_name)
        if name[1] and name[0] != "":
            name = self.abstract_affiche.data.unique_name(name[0])
            self.abstract_affiche.figure.z1_axe.name = name

            self.abstract_affiche.value.ax.yaxis.get_label().set_text(self.abstract_affiche.figure.z1_axe.name_unit)

            self.canvas.draw()

    """---------------------------------------------------------------------------------"""

    def edit_suptitle(self):
        """
        fonction appellée pour editer le titre du graph

        :return: None
        """
        old_name = self.abstract_affiche.pplot_fig._suptitle.get_text()
        name = QInputDialog.getText(self, "Name change", "New name ?", QLineEdit.Normal, old_name)
        if name[1] and name[0] != "":
            name = self.abstract_affiche.data.unique_name(name[0])
            self.abstract_affiche.pplot_fig._suptitle.set_text(name)
            self.abstract_affiche.figure.name = name
            self.name_changed.emit([old_name, name])
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
        self.abstract_affiche.pplot_fig.suptitle(name)
        self.canvas.draw()

    """---------------------------------------------------------------------------------"""

    def update_current_title_plot(self):
        """
        Methode appellé pour update le nom du plot affiché avec celui de la figure

        :return: None
        """
        self.abstract_affiche.pplot_fig.suptitle(self.abstract_affiche.figure.plot_name)
        self.canvas.draw()

    """---------------------------------------------------------------------------------"""

    def edit_finishded(self, event):
        """
        Fonction callback de la fermuture de la fenêtre d'édition d'un axe

        :param event: closed / cancel / save
        :return:
        """

        # si les données de la fenêtre sont sauvegardées
        if event == "save":

            unit = self.edit_w.comboBox_19.itemText(self.edit_w.comboBox_19.currentIndex())
            if unit != "unchanged":
                if self.axe_edited == "x":
                    if self.abstract_affiche.figure.type == "contour":

                        self.abstract_affiche.figure.x_axe.change_unit(unit)
                        self.update_contour_plot()

                    else:
                        self.abstract_affiche.figure.x_axe.change_unit(unit)

                        _max = self.abstract_affiche.figure.x_axe.data[0].data[0]
                        _min = self.abstract_affiche.figure.x_axe.data[0].data[0]

                        for i, data_array in enumerate(self.abstract_affiche.figure.x_axe.data):
                            temp_max = max(data_array.data)
                            temp_min = min(data_array.data)
                            if temp_max > _max:
                                _max = temp_max
                            if temp_min < _min:
                                _min = temp_min

                            self.update_plot_data("x", i, data_array.data)

                            delta = _max - _min
                            self.abstract_affiche.ax1.set_xlim(_min - delta * 0.05, _max + delta * 0.05)
                            self.abstract_affiche.ax1.xaxis.set_label_text(self.abstract_affiche.figure.x_axe.name_unit)

                elif self.axe_edited == "y1":
                    if self.abstract_affiche.figure.type == "contour":
                        self.abstract_affiche.figure.y1_axe.change_unit(unit)
                        self.update_contour_plot()
                    else:
                        self.abstract_affiche.figure.y1_axe.change_unit(unit)

                        _max = self.abstract_affiche.figure.y1_axe.data[0].data[0]
                        _min = self.abstract_affiche.figure.y1_axe.data[0].data[0]

                        for i, data_array in enumerate(self.abstract_affiche.figure.y1_axe.data):
                            temp_max = max(data_array.data)
                            temp_min = min(data_array.data)
                            if temp_max > _max:
                                _max = temp_max
                            if temp_min < _min:
                                _min = temp_min

                            self.update_plot_data("y1", i, data_array.data)

                        delta = _max - _min
                        self.abstract_affiche.ax1.set_ylim(_min - delta * 0.05, _max + delta * 0.05)
                        self.abstract_affiche.ax1.yaxis.set_label_text(self.abstract_affiche.figure.y1_axe.name_unit)

                else:
                    if self.abstract_affiche.figure.type == "contour":
                        pass
                    else:
                        _max = self.abstract_affiche.figure.y2_axe.data[0].data[0]
                        _min = self.abstract_affiche.figure.y2_axe.data[0].data[0]

                        self.abstract_affiche.figure.y2_axe.change_unit(unit)
                        for i, data_array in enumerate(self.abstract_affiche.figure.y2_axe.data):
                            temp_max = max(data_array.data)
                            temp_min = min(data_array.data)
                            if temp_max > _max:
                                _max = temp_max
                            if temp_min < _min:
                                _min = temp_min

                            self.update_plot_data("y2", i, data_array.data)

                        delta = _max - _min
                        self.abstract_affiche.ax2.set_ylim(_min - delta * 0.05, _max + delta * 0.05)
                        self.abstract_affiche.ax2.yaxis.set_label_text(self.abstract_affiche.figure.y2_axe.name_unit)

            # on récupére le nouveau nom de l'axe
            new_name = self.edit_w.lineEdit_2.text()
            if new_name != "":
                # si l'axe édité de x
                if self.axe_edited == "x" and self.abstract_affiche.figure.x_axe.name != new_name:
                    # on update le graph et la figure
                    self.abstract_affiche.figure.x_axe.name = new_name
                    self.abstract_affiche.ax1.xaxis.set_label_text(self.abstract_affiche.figure.x_axe.name_unit)
                # si l'axe édité de y1
                elif self.axe_edited == "y1" and self.abstract_affiche.figure.y1_axe.name != new_name:
                    # on update le graph et la figure
                    self.abstract_affiche.figure.y1_axe.name = new_name
                    self.abstract_affiche.ax1.yaxis.set_label_text(self.abstract_affiche.figure.y1_axe.name_unit)
                # si l'axe édité de y2
                elif self.axe_edited == "y2" and self.abstract_affiche.figure.y2_axe.name != new_name:
                    # on update le graph et la figure
                    self.abstract_affiche.figure.y2_axe.name = new_name
                    self.abstract_affiche.ax2.yaxis.set_label_text(self.abstract_affiche.figure.y2_axe.name_unit)

            # nouvelles valeurs de début et fin d'axe
            new_start = self.edit_w.lineEdit_3.text()
            new_end = self.edit_w.lineEdit_4.text()

            # si new_start a été modifié
            if new_start != "":
                # on check que c'est un nombre qui est donné
                new_start = float(new_start)
                # si l'axe édité de x
                if self.axe_edited == "x":
                    # on update le graph et la figure
                    if self.abstract_affiche.figure.x_axe.scale == 'log' and new_start < 0:
                        emit = Emit()
                        emit.emit("msg_console", type="msg_console", str="Can't set a non-positive value on a "
                                                                         "log-scaled axis", foreground_color="red")
                    else:
                        self.abstract_affiche.figure.x_axe.first_val = new_start
                        self.abstract_affiche.ax1.set_xlim(new_start, self.abstract_affiche.ax1.get_xlim()[1])

                    # si l'axe édité de y1
                elif self.axe_edited == "y1":
                    # on update le graph et la figure
                    if self.abstract_affiche.figure.y1_axe.scale == 'log' and new_start < 0:
                        emit = Emit()
                        emit.emit("msg_console", type="msg_console", str="Can't set a non-positive value on a "
                                                                         "log-scaled axis", foreground_color="red")
                    else:
                        self.abstract_affiche.figure.y1_axe.first_val = new_start
                        self.abstract_affiche.ax1.set_ylim(new_start, self.abstract_affiche.ax1.get_ylim()[1])
                # si l'axe édité de y2
                elif self.axe_edited == "y2":
                    # on update le graph et la figure
                    if self.abstract_affiche.figure.y2_axe.scale == 'log' and new_start < 0:
                        emit = Emit()
                        emit.emit("msg_console", type="msg_console", str="Can't set a non-positive value on a "
                                                                         "log-scaled axis", foreground_color="red")
                    else:
                        self.abstract_affiche.figure.y2_axe.first_val = new_start
                        self.abstract_affiche.ax2.set_ylim(new_start, self.abstract_affiche.ax2.get_ylim()[1])

            # si new_end a été modifié
            if new_end != "":
                new_end = float(new_end)
                if self.axe_edited == "x":
                    if self.abstract_affiche.figure.x_axe.scale == 'log' and new_end < 0:
                        emit = Emit()
                        emit.emit("msg_console", type="msg_console", str="Can't set a non-positive value on a "
                                                                         "log-scaled axis", foreground_color="red")
                    else:
                        self.abstract_affiche.figure.x_axe.last_val = new_end
                        self.abstract_affiche.ax1.set_xlim(self.abstract_affiche.ax1.get_xlim()[0], new_end)

                elif self.axe_edited == "y1":
                    if self.abstract_affiche.figure.y1_axe.scale == 'log' and new_end < 0:
                        emit = Emit()
                        emit.emit("msg_console", type="msg_console", str="Can't set a non-positive value on a "
                                                                         "log-scaled axis", foreground_color="red")
                    else:
                        self.abstract_affiche.figure.y1_axe.last_val = new_end
                        self.abstract_affiche.ax1.set_ylim(self.abstract_affiche.ax1.get_ylim()[0], new_end)

                elif self.axe_edited == "y2":
                    if self.abstract_affiche.figure.y2_axe.scale == 'log' and new_end < 0:
                        emit = Emit()
                        emit.emit("msg_console", type="msg_console", str="Can't set a non-positive value on a "
                                                                         "log-scaled axis", foreground_color="red")
                    else:
                        self.abstract_affiche.figure.y2_axe.last_val = new_end
                        self.abstract_affiche.ax2.set_ylim(self.abstract_affiche.ax2.get_ylim()[0], new_end)

            # On check le scale de l'axe indiqué
            new_scale = self.edit_w.comboBox_18.itemText(self.edit_w.comboBox_18.currentIndex())

            # si l'axe édité de x
            if self.axe_edited == "x":
                # on update le graph et la figure
                with warnings.catch_warnings(record=True) as w:
                    self.abstract_affiche.ax1.set_xscale(new_scale)

                    if len(w) == 0:
                        self.abstract_affiche.figure.x_axe.scale = new_scale
                    else:
                        self.abstract_affiche.figure.x_axe.scale = 'linear'
                        self.abstract_affiche.ax1.set_xscale('linear')
                        emit = Emit()
                        emit.emit("msg_console", type="msg_console",
                                  str="Data has no positive values x, scale set to linear",
                                  foreground_color="red")

            # si l'axe édité de y1
            elif self.axe_edited == "y1":
                # on update le graph et la figure
                with warnings.catch_warnings(record=True) as w:
                    self.abstract_affiche.ax1.set_yscale(new_scale)

                    if len(w) == 0:
                        self.abstract_affiche.figure.y1_axe.scale = new_scale
                    else:
                        self.abstract_affiche.figure.y1_axe.scale = 'linear'
                        self.abstract_affiche.ax1.set_yscale('linear')
                        emit = Emit()
                        emit.emit("msg_console", type="msg_console",
                                  str="Data has no positive values, y1 scale set to linear",
                                  foreground_color="red")

            # si l'axe édité de y2
            elif self.axe_edited == "y2":
                # on update le graph et la figure
                with warnings.catch_warnings(record=True) as w:
                    self.abstract_affiche.ax2.set_yscale(new_scale)

                    if len(w) == 0:
                        self.abstract_affiche.figure.y2_axe.scale = new_scale
                    else:
                        self.abstract_affiche.figure.y2_axe.scale = 'linear'
                        self.abstract_affiche.ax2.set_yscale('linear')
                        emit = Emit()
                        emit.emit("msg_console", type="msg_console",
                                  str="Data has no positive values, y2 scale set to linear",
                                  foreground_color="red")

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

    def is_on_top(self):
        """
        On check si la fenêtre est active ou pas

        :return: bool
        """
        return self.isActiveWindow()

    """---------------------------------------------------------------------------------"""

    def update_plot_data(self, axe, index, array):
        """
        On met à jours les data du plot avec les axes donnée en paramètre

        Pas de draw ici, il se fait par ailleurs

        :param axe: Nom de l'axe : x, y1, y2
        :param index: index d'édition
        :param array: nouvel array
        :return: None
        """

        if axe == "x":
            if index >= len(self.abstract_affiche.ax1.lines):
                self.abstract_affiche.ax2.lines[index - len(self.abstract_affiche.ax1.lines)].set_xdata(array)
            else:
                self.abstract_affiche.ax1.lines[index].set_xdata(array)
        elif axe == "y1":
            self.abstract_affiche.ax1.lines[index].set_ydata(array)
        else:
            self.abstract_affiche.ax2.lines[index].set_ydata(array)

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

    """---------------------------------------------------------------------------------"""

    def update_color_plot(self, axe):
        """
        Les couleurs de la figure de self.abstract_affiche on était modifié, on
        update les 2dline et les légendes du plot avec les nouvelle couleurs

        :param axe: y1, y2
        :return: None
        """

        if axe == "y1":
            for i in range(len(self.abstract_affiche.figure.y1_axe.data)):
                self.abstract_affiche.ax1.lines[i].set_color(self.abstract_affiche.figure.y1_axe.data[i].color)
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

                # on parcours les légendes pour update la couleur
                for i in range(len(self.abstract_affiche.leg1.get_legend().get_lines())):
                    color = self.abstract_affiche.figure.y1_axe.data[modulo_y1[i]].color
                    self.abstract_affiche.leg1.get_legend().get_lines()[i].set_color(color)

            else:
                # on parcours les légendes pour update la couleur
                for i in range(len(self.abstract_affiche.leg1.get_legend().get_lines())):
                    color = self.abstract_affiche.figure.y1_axe.data[i].color
                    self.abstract_affiche.leg1.get_legend().get_lines()[i].set_color(color)

        elif axe == "y2":
            for i in range(len(self.abstract_affiche.figure.y2_axe.data)):
                self.abstract_affiche.ax2.lines[i].set_color(self.abstract_affiche.figure.y2_axe.data[i].color)
            modulo_y2 = []
            nb_y2 = 0
            # on check le nombre de legende
            for data in self.abstract_affiche.figure.y2_axe.data:
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

                # on parcours les légendes pour update la couleur
                for i in range(len(self.abstract_affiche.leg2.get_legend().get_lines())):
                    color = self.abstract_affiche.figure.y2_axe.data[modulo_y2[i]].color
                    self.abstract_affiche.leg2.get_legend().get_lines()[i].set_color(color)

            else:
                # on parcours les légendes pour update la couleur
                for i in range(len(self.abstract_affiche.leg2.get_legend().get_lines())):
                    color = self.abstract_affiche.figure.y2_axe.data[i].color
                    self.abstract_affiche.leg2.get_legend().get_lines()[i].set_color(color)

    """---------------------------------------------------------------------------------"""

    def reset_color_plot(self, axe):
        """
        Les couleurs de la figure de self.abstract_affiche on était reset, les
        couleurs a appliqué sont celle par défaut de matplotlib

        :param axe: y1, y2
        :return: None
        """
        colors = matplotlib.rcParams['axes.prop_cycle'].by_key()['color']
        if axe == "y1":
            index = 0
            for i in range(len(self.abstract_affiche.figure.y1_axe.data)):
                if index == len(colors):
                    index = 0

                self.abstract_affiche.ax1.lines[i].set_color(colors[index])
                index += 1

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

                # on parcours les légendes pour update la couleur
                index = 0
                for i in range(len(self.abstract_affiche.leg1.get_legend().get_lines())):
                    if index == len(colors):
                        index = 0
                    color = colors[index]
                    self.abstract_affiche.leg1.get_legend().get_lines()[i].set_color(color)
                    index += 1
            else:
                # on parcours les légendes pour update la couleur
                index = 0
                for i in range(len(self.abstract_affiche.leg1.get_legend().get_lines())):
                    if index == len(colors):
                        index = 0
                    color = colors[index]
                    self.abstract_affiche.leg1.get_legend().get_lines()[i].set_color(color)
                    index += 1

        elif axe == "y2":
            index = 0
            for i in reversed(range(len(self.abstract_affiche.figure.y2_axe.data))):
                if index == len(colors):
                    index = 0
                self.abstract_affiche.ax2.lines[i].set_color(colors[index])
                index += 1

            modulo_y2 = []
            nb_y2 = 0
            # on check le nombre de legende
            for data in self.abstract_affiche.figure.y2_axe.data:
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

                # on parcours les légendes pour update la couleur
                index = 0
                for i in reversed(range(len(self.abstract_affiche.leg2.get_legend().get_lines()))):
                    if index == len(colors):
                        index = 0
                    color = colors[index]
                    self.abstract_affiche.leg2.get_legend().get_lines()[i].set_color(color)
                    index += 1
            else:
                # on parcours les légendes pour update la couleur
                index = 0
                for i in reversed(range(len(self.abstract_affiche.leg2.get_legend().get_lines()))):
                    if index == len(colors):
                        index = 0
                    color = colors[index]
                    self.abstract_affiche.leg2.get_legend().get_lines()[i].set_color(color)
                    index += 1

    """---------------------------------------------------------------------------------"""

    def set_visibility_2d_line(self, axe, index, visibility):
        """
        On update l'arg visible de la 2dline à l'index index avec visibility

        :param axe: y1 ,y2
        :param index: index de la 2dline a update
        :param visibility: True, False
        :return: None
        """
        if axe == "y1":
            self.abstract_affiche.ax1.lines[index].set_visible(visibility)
        elif axe == "y2":
            self.abstract_affiche.ax2.lines[index].set_visible(visibility)

    """---------------------------------------------------------------------------------"""

    def update_marker_plot(self, axe, marker):
        """
        On update l'axe axe avec le nouveau marker
        :param axe: y1 / y2
        :param marker: Resource.MARKERS_PLOT
        :return: None
        """
        if axe == "y1":
            for i in range(len(self.abstract_affiche.figure.y1_axe.data)):
                self.abstract_affiche.ax1.lines[i].set_marker(marker)
                self.abstract_affiche.ax1.lines[i].set_ls('')

            for i in range(len(self.abstract_affiche.leg1.get_legend().get_lines())):
                self.abstract_affiche.leg1.get_legend().get_lines()[i].set_marker(marker)
                self.abstract_affiche.leg1.get_legend().get_lines()[i].set_ls('')

        elif axe == "y2":
            for i in range(len(self.abstract_affiche.figure.y2_axe.data)):
                self.abstract_affiche.ax2.lines[i].set_marker(marker)
                self.abstract_affiche.ax2.lines[i].set_ls('')

            for i in range(len(self.abstract_affiche.leg2.get_legend().get_lines())):
                self.abstract_affiche.leg2.get_legend().get_lines()[i].set_marker(marker)
                self.abstract_affiche.leg2.get_legend().get_lines()[i].set_ls('')

    """---------------------------------------------------------------------------------"""

    def reset_marker_plot(self, axe):
        """
        On reset le style
        :param axe: y1 / y2
        :return: None
        """
        if axe == "y1":
            for i in range(len(self.abstract_affiche.figure.y1_axe.data)):
                self.abstract_affiche.ax1.lines[i].set_marker(None)
                self.abstract_affiche.ax1.lines[i].set_ls("-")

            for i in range(len(self.abstract_affiche.leg1.get_legend().get_lines())):
                self.abstract_affiche.leg1.get_legend().get_lines()[i].set_marker(None)
                self.abstract_affiche.leg1.get_legend().get_lines()[i].set_ls("-")

        elif axe == "y2":
            for i in range(len(self.abstract_affiche.figure.y2_axe.data)):
                self.abstract_affiche.ax2.lines[i].set_marker(None)
                self.abstract_affiche.ax2.lines[i].set_ls('-')

            for i in range(len(self.abstract_affiche.leg2.get_legend().get_lines())):
                self.abstract_affiche.leg2.get_legend().get_lines()[i].set_marker(None)
                self.abstract_affiche.leg2.get_legend().get_lines()[i].set_ls("-")

    """---------------------------------------------------------------------------------"""
    """                         View data current plot start                            """
    """---------------------------------------------------------------------------------"""

    def init_window_view_data(self, list):
        """
        On update list_view_data avec l'adresse de listwidget
        de la console pour pouvoir l'éditer
        :param list_view: adresse de l'objet listwidget
        :return: None
        """

        self.array_data_displayed = list
        if self.view_data_value is not None:
            self.view_data_value.destroy()
            self.view_data_value = None

        self.view_data_value = View_data_value(self.array_data_displayed, self)

        _translate = QtCore.QCoreApplication.translate
        self.view_data_value.label.setText(_translate("Dialog",
                                                      "<html><head/><body><p><span style=\" font-size:8pt;\">Res "
                                                      "figure " + self.abstract_affiche.figure.name +
                                                      " :</span></p></body></html>"))

        self.view_data_value.setWindowFlags(
            QtCore.Qt.Window |
            QtCore.Qt.CustomizeWindowHint |
            QtCore.Qt.WindowTitleHint |
            QtCore.Qt.WindowCloseButtonHint |
            QtCore.Qt.WindowStaysOnTopHint
        )

        self.view_data_value.finish_signal.connect(self.close_view_data_value)

        self.view_data_value.show()

        # on connect index_res de self.abstract_affiche pour récupérer l'index
        # calculé lors de l'affichage du pointeur
        self.emit.connect("update_values", self.update_values)
        self.abstract_affiche.can_emit = True

    """---------------------------------------------------------------------------------"""

    def update_values(self, signal):
        """
        Fonction callback de interactive de self. abstract_affiche
        on met à jours les valeurs dans la fenêtre d'affichage des valeurs

        :param signal: signal{"res" : index_data, "index" : index_data_array}
        :return: None
        """
        index_data = signal["res"]
        index_data_array = signal["index"][0][1]

        # on récupére l'index global correspondant à index_data_array et index_data
        global_index = self.abstract_affiche.figure.x_axe.data[index_data_array].global_index[index_data]

        # on update les valeurs en utilisant global_index
        for i, data_name in enumerate(self.array_data_displayed):
            self.view_data_value.gridLayout.itemAtPosition(i, 2).widget(). \
                setText(str(self.abstract_affiche.data.data[data_name][global_index]))

    """---------------------------------------------------------------------------------"""

    def close_view_data_value(self, event):
        """
        Fonction callback de la fermeture de la fenêtre de visualisation des données

        :param event: peu importe
        :return: None
        """
        # on désactive l'émission de abstract_affiche
        self.abstract_affiche.can_emit = False

        # on déconnect update_values
        self.emit.disconnect("update_values")

        # on suprime la fenêtre
        self.view_data_value.deleteLater()
        self.view_data_value = None

        # on reset array_data_displayed
        self.array_data_displayed = []

    """---------------------------------------------------------------------------------"""
    """                         View data current plot end                              """
    """---------------------------------------------------------------------------------"""

    def update_contour_plot(self):
        """
        On update pour apliquer les changement du contour plot
        pour un contour plot value correspond à la colorbar

        :return: None
        """

        self.abstract_affiche.value.remove()
        self.abstract_affiche.ax1.clear()

        data_x = self.abstract_affiche.figure.x_axe.data
        data_y1 = self.abstract_affiche.figure.y1_axe.data
        data_z1 = self.abstract_affiche.figure.z1_axe.data

        if "norm" in self.abstract_affiche.figure.kwarks:
            norm_min = self.abstract_affiche.figure.kwarks["norm"][0]
            norm_max = self.abstract_affiche.figure.kwarks["norm"][1]

            if norm_min == -1:
                norm_min = 0

            if norm_max == -1:
                _max = 0
                for i in range(len(self.abstract_affiche.figure.z1_axe.data[0].data[0])):
                    _max = max(_max, self.abstract_affiche.figure.z1_axe.data[0].data[0][i])
                norm_max = int(_max)
        else:
            # approximation, on ne check que le premier cycle
            _max = 0
            for i in range(len(self.abstract_affiche.figure.z1_axe.data[0].data[0])):
                _max = max(_max, self.abstract_affiche.figure.z1_axe.data[0].data[0][i])
            norm_min = 0
            norm_max = int(_max)

        pas = int((norm_max - norm_min) / 8)

        for i in range(len(data_x)):
            if norm_min == -1:
                self.abstract_affiche.ax2 = self.abstract_affiche. \
                    ax1.contourf(data_x[i].data, data_y1[i].data,
                                 data_z1[i].data,
                                 cmap=data_x[i].get_color_map())
            else:
                self.abstract_affiche.ax2 = self.abstract_affiche. \
                    ax1.contourf(data_x[i].data, data_y1[i].data,
                                 data_z1[i].data,
                                 levels=np.linspace(norm_min,
                                                    norm_max,
                                                    num=200),
                                 extend='both',
                                 cmap=self.abstract_affiche.figure.y1_axe.color_map)
        if norm_min == -1:
            self.abstract_affiche.value = self.abstract_affiche.pplot_fig.colorbar(self.abstract_affiche.ax2)
        else:
            self.abstract_affiche.value = self.abstract_affiche.pplot_fig.colorbar(self.abstract_affiche.ax2,
                                                                                   ticks=range(norm_min, norm_max, pas))

        self.abstract_affiche.ax1.set_xlabel(self.abstract_affiche.figure.x_axe.name_unit, labelpad=20)
        self.abstract_affiche.ax1.set_ylabel(self.abstract_affiche.figure.y1_axe.name_unit, labelpad=20)
        self.abstract_affiche.value.ax.set_ylabel(self.abstract_affiche.figure.z1_axe.name_unit, rotation=90,
                                                  labelpad=0.7)

        Data_type.Abstract_data.format_axes_figure(self.abstract_affiche.figure, self.abstract_affiche.ax1, None)

        self.canvas.draw()

    def close_view_values(self):
        """
        fonction appelé lors de la fermeture de la tab
        on ferme la fenêtre d'affichage des valeurs si besoin

        :return: None
        """
        if self.view_data_value is not None:
            # on delet la fenêtre
            self.view_data_value.close()
            self.view_data_value = None

    def call_back_func(self, *args, **kwargs):
        if type(self.abstract_affiche).__name__ == "Gitt_affiche":
            self.close()
        elif type(self.abstract_affiche).__name__ == "Impedance_affiche":
            self.close()
        elif type(self.abstract_affiche).__name__ == "Time_Selection":
            self.close()
        elif type(self.abstract_affiche).__name__ == "Saxs_selection":
            self.close()
