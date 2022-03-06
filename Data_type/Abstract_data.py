from abc import ABC, abstractmethod

import matplotlib
import matplotlib.pyplot as pplot
import numpy as np

from Console_Objets.Axe import Axe
from Console_Objets.Figure import Figure
from Resources_file import Resources
from Resources_file.Emit import Emit


def resize_axe_y(axe1, axe2, p):
    """On augemente la taille de l'ax donné en paramétre de p %"""
    p = -p
    size_axe_y1 = axe1.get_ylim()[1] - axe1.get_ylim()[0]
    axe1.set_ylim(axe1.get_ylim()[0] - (size_axe_y1 * p / 100), axe1.get_ylim()[1] + (size_axe_y1 * p / 100))

    if axe2 is not None:
        size_axe_y2 = axe2.get_ylim()[1] - axe2.get_ylim()[0]
        axe2.set_ylim(axe2.get_ylim()[0] - (size_axe_y2 * p / 100), axe2.get_ylim()[1] + (size_axe_y2 * p / 100))


"""----------------------------------------------------------------------------------"""


def format_axes_figure(figure, ax1, ax2):
    if ax1 is not None:
        """update du min et du man pour l'axe ax1"""
        if figure.x_axe.first_val is not None and figure.x_axe.last_val is not None:
            ax1.set_xlim(figure.x_axe.first_val, figure.x_axe.last_val)

        elif figure.x_axe.first_val is not None:
            x_min, x_max = ax1.get_xlim()
            ax1.set_xlim(figure.x_axe.first_val, x_max)

        elif figure.x_axe.last_val is not None:
            x_min, x_max = ax1.get_xlim()
            ax1.set_xlim(x_min, figure.x_axe.last_val)

        if figure.y1_axe.first_val is not None and figure.y1_axe.last_val is not None:
            ax1.set_ylim(figure.y1_axe.first_val, figure.y1_axe.last_val)

        elif figure.y1_axe.first_val is not None:
            y_min, y_max = ax1.get_ylim()
            ax1.set_ylim(figure.y1_axe.first_val, y_max)

        elif figure.y1_axe.last_val is not None:
            y_min, y_max = ax1.get_xlim()
            ax1.set_ylim(y_min, figure.y1_axe.last_val)

        """update set_aspect pour l'axe ax1"""
        if figure.aspect is not None:
            ax1.set_aspect(figure.aspect, 'box')

        """update du scale pour l'axe ax1"""
        if figure.x_axe.scale is not None:
            ax1.set_xscale(figure.x_axe.scale)

        if figure.y1_axe.scale is not None:
            ax1.set_yscale(figure.y1_axe.scale)

        """update de la police de l'axe"""
        for tick in ax1.xaxis.get_major_ticks():
            tick.label1.set_fontsize(18)
            tick.label1.set_fontweight('bold')
        for tick in ax1.yaxis.get_major_ticks():
            tick.label1.set_fontsize(18)
            tick.label1.set_fontweight('bold')
        for tick in ax1.yaxis.get_major_ticks():
            tick.label2.set_fontsize(18)
            tick.label2.set_fontweight('bold')

    if ax2 is not None:
        """update du min et du man pour l'axe ax2"""
        if figure.y2_axe.first_val is not None and figure.y2_axe.last_val is not None:
            ax2.set_ylim(figure.y2_axe.first_val, figure.y2_axe.last_val)

        elif figure.y2_axe.first_val is not None:
            y_min, y_max = ax2.get_ylim()
            ax2.set_ylim(figure.y2_axe.first_val, y_max)

        elif figure.y2_axe.last_val is not None:
            y_min, y_max = ax2.get_xlim()
            ax2.set_ylim(y_min, figure.y2_axe.last_val)

        """update set_aspect pour l'axe ax2"""
        if figure.aspect is not None:
            ax2.set_aspect(figure.aspect, 'box')

        """update du scale pour l'axe ax2"""
        if figure.x_axe.scale is not None:
            ax2.set_xscale(figure.x_axe.scale)

        if figure.y2_axe.scale is not None:
            ax2.set_yscale(figure.y2_axe.scale)

        """update de la police de l'axe"""
        for tick in ax2.xaxis.get_major_ticks():
            tick.label1.set_fontsize(18)
            tick.label1.set_fontweight('bold')
        for tick in ax2.yaxis.get_major_ticks():
            tick.label1.set_fontsize(18)
            tick.label1.set_fontweight('bold')
        for tick in ax2.yaxis.get_major_ticks():
            tick.label2.set_fontsize(18)
            tick.label2.set_fontweight('bold')

    resize_axe(ax1, ax2, figure.margin)


def resize_axe(axe1, axe2, new_p, old_p=None):
    if old_p is not None:
        new_p = new_p - old_p
    if old_p is not None and old_p != 0:
        p = (100 - old_p) / 100 * new_p
    else:
        p = new_p

    if p == 0:
        return
    size_axe_x = axe1.get_xlim()[1] - axe1.get_xlim()[0]
    axe1.set_xlim(axe1.get_xlim()[0] - (size_axe_x * p / 100), axe1.get_xlim()[1] + (size_axe_x * p / 100))

    size_axe_y1 = axe1.get_ylim()[1] - axe1.get_ylim()[0]
    axe1.set_ylim(axe1.get_ylim()[0] - (size_axe_y1 * p / 100), axe1.get_ylim()[1] + (size_axe_y1 * p / 100))

    if axe2 is not None:
        size_axe_y2 = axe2.get_ylim()[1] - axe2.get_ylim()[0]
        axe2.set_ylim(axe2.get_ylim()[0] - (size_axe_y2 * p / 100),
                      axe2.get_ylim()[1] + (size_axe_y2 * p / 100))


class Abstract_data(ABC):
    def __init__(self):
        self._data = None
        self._name = None

        # self._nom_cell = None
        self._nom_cell = "temp"
        self._figures = []
        self._current_figure = None

        self._loop = False
        self._pos_x = None
        self._pos_y = None
        self._index = None

        self.resource = Resources.Resource_class()

    """----------------------------------------------------------------------------------"""
    """                                   Methode abstraite                              """
    """----------------------------------------------------------------------------------"""

    @abstractmethod
    def get_operation_available(self):
        pass

    @abstractmethod
    def capa(self):
        pass

    @abstractmethod
    def potentio(self, cycle):
        pass

    @abstractmethod
    def derive(self, *args, **kwargs):
        pass

    @abstractmethod
    def shift_axe(self, *args, **kwargs):
        pass

    @abstractmethod
    def create_figure_cycle(self, *args, **kwargs):
        pass

    @abstractmethod
    def get_dics(self):
        pass

    @abstractmethod
    def create_diffraction(self):
        pass

    @abstractmethod
    def get_cycle_available(self):
        pass

    @abstractmethod
    def diffraction_contour_temperature(self):
        pass

    @abstractmethod
    def create_GITT(self):
        pass

    def unique_name(self, name):
        """Parcours le nom des figures enregistrées et regarde si le nom donné en paramettre est unique, si il ne
        l'est pas on renvoie le même nom avec (1), (2) etc, si le nom est unique on renvoie jsute le nom """
        if self.figures is None:
            return name

        for i in self.figures:
            if i.name == name:
                """Si dans name il n'y a pas (*) à la fin, on apelle la fonction unique_name en ajoutant
                (1)"""
                if len(name) > 2 and name[len(name) - 3] != '(' and name[len(name) - 1] != ')':
                    name += "(1)"
                elif len(name) < 3:
                    name += "(1)"
                else:
                    try:
                        num = int(name[len(name) - 2]) + 1
                        temp = "(" + str(num) + ")"
                        name = name[0:len(name) - 3] + temp
                    except ValueError:
                        name += "(1)"
                return self.unique_name(name)
        return name

    """----------------------------------------------------------------------------------"""

    def load_graph(self, figure, path_save=None):
        pplot.rcParams.update({'font.size': 18})

        fig, (ax1, leg1) = pplot.subplots(ncols=2, gridspec_kw={"width_ratios": [10, 1]})
        value = leg1.twinx()
        value.axis("off")

        leg1.set_visible(figure.y1_axe.legend)

        if figure.type == "impedance":
            val_freq = value.twinx()
            val_freq.axis("off")
        else:
            val_freq = None

        fig.set_size_inches(11, 7)
        ax2 = None
        leg2 = None

        fig.canvas.manager.set_window_title(figure.plot_name)
        fig.suptitle(figure.plot_name)

        data_x = figure.x_axe.data

        """----------------------------------------------------------------------------------"""
        """                                        y1                                        """
        """----------------------------------------------------------------------------------"""

        if figure.y1_axe is not None:
            data_y1 = figure.y1_axe.data

            if figure.format_line_y1 is None:
                format_line_y1 = '-'
            else:
                format_line_y1 = figure.format_line_y1

            nb_y1 = 0
            for i in range(len(data_y1)):
                if data_y1[i].legend is not None and data_y1[i].visible:
                    nb_y1 += 1
            index_modulo_y1 = 0
            if nb_y1 > figure.nb_legende:
                modulo_y1 = []
                for i in range(figure.nb_legende):
                    temp = int(nb_y1 / figure.nb_legende * i)
                    if temp not in modulo_y1:
                        modulo_y1.append(temp)
            else:
                modulo_y1 = []

            for i in range(len(data_y1)):
                if len(data_x[i].data) != len(data_y1[i].data):
                    raise ValueError

                if len(modulo_y1) == 0 or (
                        index_modulo_y1 < len(modulo_y1) and i == modulo_y1[index_modulo_y1]):
                    index_modulo_y1 += 1
                    if data_y1[i].color is not None:
                        ax1.plot(data_x[i].data, data_y1[i].data, format_line_y1, markersize=figure.marker_size,
                                 label=data_y1[i].legend, color=data_y1[i].color, visible=data_y1[i].visible)
                    else:
                        ax1.plot(data_x[i].data, data_y1[i].data, format_line_y1, markersize=figure.marker_size,
                                 label=data_y1[i].legend, visible=data_y1[i].visible)
                else:
                    if data_y1[i].color is not None:
                        ax1.plot(data_x[i].data, data_y1[i].data, format_line_y1, markersize=figure.marker_size,
                                 color=data_y1[i].color, visible=data_y1[i].visible)
                    else:
                        ax1.plot(data_x[i].data, data_y1[i].data, format_line_y1, markersize=figure.marker_size,
                                 visible=data_y1[i].visible)

            h, l = ax1.get_legend_handles_labels()
            leg1.legend(h, l, borderaxespad=0, loc="upper right")
            leg1.axis("off")

            ax1.set_xlabel(figure.x_axe.name_unit, labelpad=20)
            ax1.set_ylabel(figure.y1_axe.name_unit, labelpad=20)

        """----------------------------------------------------------------------------------"""
        """                                        y2                                        """
        """----------------------------------------------------------------------------------"""

        if figure.y2_axe is not None:
            couleur = []
            for name in reversed(matplotlib.colors.cnames.items()):
                couleur.append(name[0])

            ax2 = ax1.twinx()
            leg2 = leg1.twinx()

            leg2.set_visible(figure.y2_axe.legend)

            len_y1 = len(figure.y1_axe)

            data_y2 = figure.y2_axe.data

            if figure.format_line_y2 is None:
                format_line_y2 = '-'
            else:
                format_line_y2 = figure.format_line_y2

            nb_y2 = 0
            for i in range(len(data_y2)):
                if data_y2[i].legend is not None and data_y2[i].visible:
                    nb_y2 += 1
            index_modulo_y2 = 0

            if nb_y2 > figure.nb_legende:
                modulo_y2 = []
                for i in range(figure.nb_legende):
                    temp = int(nb_y2 / figure.nb_legende * i)
                    if temp not in modulo_y2:
                        modulo_y2.append(temp)
            else:
                modulo_y2 = []

            index_color = 0
            for i in range(len(data_y2)):
                if index_color == len(couleur):
                    index_color = 0

                if len(modulo_y2) == 0 or (
                        index_modulo_y2 < len(modulo_y2) and i == modulo_y2[index_modulo_y2]):
                    index_modulo_y2 += 1
                    if data_y2[i].color is not None:
                        ax2.plot(data_x[i + len_y1].data, data_y2[i].data, format_line_y2,
                                 markersize=figure.marker_size,
                                 label=data_y2[i].legend,
                                 color=data_y2[i].color, visible=data_y2[i].visible)
                    else:
                        ax2.plot(data_x[i + len_y1].data, data_y2[i].data, format_line_y2,
                                 markersize=figure.marker_size,
                                 color=couleur[index_color], label=data_y2[i].legend, visible=data_y2[i].visible)
                else:
                    if data_y2[i].color is not None:
                        ax2.plot(data_x[i + len_y1].data, data_y2[i].data, format_line_y2,
                                 markersize=figure.marker_size,
                                 color=data_y2[i].color, visible=data_y2[i].visible)
                    else:
                        ax2.plot(data_x[i + len_y1].data, data_y2[i].data, format_line_y2,
                                 markersize=figure.marker_size,
                                 color=couleur[index_color], visible=data_y2[i].visible)
                index_color += 1

            h, l = ax2.get_legend_handles_labels()
            leg2.legend(h, l, borderaxespad=0, loc="lower right")
            leg2.axis("off")

            ax2.set_ylabel(figure.y2_axe.name_unit, labelpad=20)

        format_axes_figure(figure, ax1, ax2)

        if path_save is not None:
            pplot.tight_layout()
            pplot.close(fig)
            fig.savefig(path_save, bbox_inches='tight', dpi=150)

        return fig, ax1, ax2, value, val_freq, leg1, leg2

    """----------------------------------------------------------------------------------"""

    def load_graph_bar(self, figure, path_save=None):
        pplot.rcParams.update({'font.size': 18})

        fig, (ax1, leg1) = pplot.subplots(ncols=2, gridspec_kw={"width_ratios": [10, 1]})
        value = leg1.twinx()
        value.axis("off")

        if figure.type == "impedance":
            val_freq = value.twinx()
            val_freq.axis("off")
        else:
            val_freq = None

        fig.set_size_inches(11, 7)

        fig.canvas.manager.set_window_title(figure.plot_name)
        fig.suptitle(figure.plot_name)

        data_x = figure.x_axe.data

        """----------------------------------------------------------------------------------"""
        """                                        y1                                        """
        """----------------------------------------------------------------------------------"""

        if figure.y1_axe is not None:
            data_y1 = figure.y1_axe.data

            largeur = 0.75

            nb_y1 = 0
            for i in range(len(data_y1)):
                if data_y1[i].legend is not None:
                    nb_y1 += 1
            index_modulo_y1 = 0
            if nb_y1 > figure.nb_legende:
                modulo_y1 = []
                for i in range(figure.nb_legende):
                    temp = int(nb_y1 / figure.nb_legende * i)
                    if temp not in modulo_y1:
                        modulo_y1.append(temp)
            else:
                modulo_y1 = []

            for i in range(len(data_y1)):
                if len(modulo_y1) == 0 or (
                        index_modulo_y1 < len(modulo_y1) and i == modulo_y1[index_modulo_y1]):
                    index_modulo_y1 += 1
                    if data_y1[i].color is not None:
                        if i > 0:
                            ax1.bar(data_x[0].data, data_y1[i].data,
                                    width=largeur,
                                    label=data_y1[i].legend,
                                    color=data_y1[i].color,
                                    bottom=data_y1[i - 1].data)
                        else:
                            ax1.bar(data_x[0].data, data_y1[i].data,
                                    width=largeur,
                                    label=data_y1[i].legend,
                                    color=data_y1[i].color)
                    else:
                        if i > 0:
                            ax1.bar(data_x[0].data, data_y1[i].data,
                                    width=largeur,
                                    label=data_y1[i].legend,
                                    bottom=data_y1[i - 1].data)
                        else:
                            ax1.bar(data_x[0].data, data_y1[i].data,
                                    width=largeur,
                                    label=data_y1[i].legend)
                else:
                    if data_y1[i].color is not None:
                        if i > 0:
                            ax1.bar(data_x[0].data, data_y1[i].data,
                                    width=largeur,
                                    color=data_y1[i].color,
                                    bottom=data_y1[i - 1].data)
                        else:
                            ax1.bar(data_x[0].data, data_y1[i].data,
                                    width=largeur,
                                    color=data_y1[i].color)
                    else:
                        if i > 0:
                            ax1.bar(data_x[0].data, data_y1[i].data, width=largeur, bottom=data_y1[i - 1].data)
                        else:
                            ax1.bar(data_x[0].data, data_y1[i].data, width=largeur)

            h, l = ax1.get_legend_handles_labels()
            leg1.legend(h, l, borderaxespad=0, loc="upper right")
            leg1.axis("off")

            ax1.set_xlabel(figure.x_axe.name_unit, labelpad=20)
            ax1.set_ylabel(figure.y1_axe.name_unit, labelpad=20)

            format_axes_figure(figure, ax1, None)

        if path_save is not None:
            pplot.tight_layout()
            pplot.close(fig)
            fig.savefig(path_save, bbox_inches='tight', dpi=150)

        return fig, ax1, None, value, val_freq, leg1, None

    """----------------------------------------------------------------------------------"""

    def load_graph_fit(self, figure, path_save=None):
        """
        création de la figure matplotlib issu d'un fit
        graph général a revoir, il est moche


        :param figure: figure résultat d'un fit
        :param path_save: chemin d'accés en cas de sauvegarde
        :return: fig, ax1, None, value, val_freq, leg1, None
        """
        couleurs = []
        for name in matplotlib.colors.TABLEAU_COLORS:
            couleurs.append(name)

        if figure.type == "res_fitting_temperature":
            nb_cooling = 0
            nb_warning = 0
            for data in figure.x_axe.data:
                if data.kwargs["temperature"] == "cooling":
                    nb_cooling += 1
                else:
                    nb_warning += 1

            if nb_cooling != 0 and nb_warning != 0:
                nb_pics = len(figure.y1_axe.data) / 6

                index = 0

                fig = pplot.figure(figsize=(11, 7))
                gs = fig.add_gridspec(3, 3, hspace=0.1, wspace=0, width_ratios=[5, 5, 1])
                axes = gs.subplots(sharex='col', sharey='row')
                _str = figure.name
                _str = _str.replace("_", " ")
                fig.suptitle(_str)

                ligne_1 = axes[0]
                ligne_2 = axes[1]
                ligne_3 = axes[2]

                leg = ["pic " + str(figure.kwarks["init_center"][i]) for i in range(int(nb_pics))]

                for i, axe in enumerate(ligne_1):
                    if i == 2:
                        fig.delaxes(axe)
                        break
                    index_color = 0
                    for j in range(int(nb_pics)):
                        if index_color == len(couleurs):
                            index_color = 0
                        axe.plot(figure.x_axe.data[index].data, figure.y1_axe.data[index].data, "x",
                                 color=couleurs[index_color], label=leg[j])
                        index_color += 1
                        index += 1

                    axe.get_xaxis().set_visible(False)

                    if i == 0:
                        axe.set_title('warning')
                        axe.set_ylabel("x_max")
                    elif i == 1:
                        axe.set_title('cooling')
                        axe.get_yaxis().set_visible(False)

                for i, axe in enumerate(ligne_2):
                    if i == 2:
                        leg = axe
                        axe.axis("off")
                        break

                    index_color = 0
                    for j in range(int(nb_pics)):
                        if index_color == len(couleurs):
                            index_color = 0
                        axe.plot(figure.x_axe.data[index].data, figure.y1_axe.data[index].data, "x",
                                 color=couleurs[index_color])
                        index_color += 1
                        index += 1

                    axe.get_xaxis().set_visible(False)

                    if i == 0:
                        axe.set_ylabel("area")
                    elif i == 1:
                        axe.get_yaxis().set_visible(False)

                for i, axe in enumerate(ligne_3):
                    if i == 2:
                        fig.delaxes(axe)
                        break

                    index_color = 0
                    for j in range(int(nb_pics)):
                        if index_color == len(couleurs):
                            index_color = 0
                        axe.plot(figure.x_axe.data[index].data, figure.y1_axe.data[index].data, "x",
                                 color=couleurs[index_color])
                        index_color += 1
                        index += 1

                    if i == 0:
                        axe.set_ylabel("fwhm")
                        axe.set_xlabel("temperature")
                    elif i == 1:
                        axe.set_xlabel("temperature")
                        axe.invert_xaxis()
                        axe.get_yaxis().set_visible(False)

                h = []
                l = []
                leg_axe = [axes[0, 0], axes[1, 0], axes[2, 0]]

                for axe in leg_axe:
                    h1, l1 = axe.get_legend_handles_labels()
                    h.extend(h1)
                    l.extend(l1)

                leg.legend(h, l, bbox_to_anchor=(2.9, 1))
                fig.subplots_adjust(left=0.105, right=0.87)
            else:
                nb_pics = len(figure.y1_axe.data) / 3

                index = 0
                fig = pplot.figure(figsize=(11, 7))
                gs = fig.add_gridspec(3, 2, hspace=0.1, wspace=0, width_ratios=[10, 1])
                axes = gs.subplots(sharex='col', sharey='row')
                _str = figure.name
                _str = _str.replace("_", " ")
                fig.suptitle(_str)

                if nb_cooling == 0:
                    name = "warning"
                else:
                    name = "cooling"

                ligne_1 = axes[0]
                ligne_2 = axes[1]
                ligne_3 = axes[2]

                leg = ["x max", "area", "fwhm"]

                for i, axe in enumerate(ligne_1):
                    if i == 1:
                        fig.delaxes(axe)
                        break
                    for j in range(int(nb_pics)):
                        axe.plot(figure.x_axe.data[index].data, figure.y1_axe.data[index].data, "x", color=couleurs[j],
                                 label="x_max")
                        index += 1

                    axe.get_xaxis().set_visible(False)
                    resize_axe_y(axe, None, -7.5)
                    if i == 0:
                        axe.set_title(name)
                        axe.set_ylabel("x_max")

                for i, axe in enumerate(ligne_2):
                    if i == 1:
                        leg = axe
                        axe.axis("off")
                        break
                    for j in range(int(nb_pics)):
                        axe.plot(figure.x_axe.data[index].data, figure.y1_axe.data[index].data, "x", color=couleurs[j],
                                 label="area")
                        index += 1

                    axe.get_xaxis().set_visible(False)
                    resize_axe_y(axe, None, -7.5)

                    if i == 0:
                        axe.set_ylabel("area")

                for i, axe in enumerate(ligne_3):
                    if i == 1:
                        fig.delaxes(axe)
                        break
                    for j in range(int(nb_pics)):
                        axe.plot(figure.x_axe.data[index].data, figure.y1_axe.data[index].data, "x", color=couleurs[j],
                                 label="fwhm")
                        index += 1

                    resize_axe_y(axe, None, -7.5)

                    if i == 0:
                        axe.set_ylabel("largeur")
                        axe.set_xlabel("temperature")
                    if name == "cooling":
                        axe.invert_xaxis()

                h = []
                l = []
                leg_axe = [axes[0, 0], axes[1, 0], axes[2, 0]]

                for axe in leg_axe:
                    h1, l1 = axe.get_legend_handles_labels()
                    h.extend(h1)
                    l.extend(l1)

                leg.legend(h, l, bbox_to_anchor=(2.9, 1))
                fig.subplots_adjust(left=0.105, right=0.90)

            if path_save is not None:
                pplot.tight_layout()
                pplot.close(fig)
                fig.savefig(path_save, bbox_inches='tight', dpi=150)

            return fig

        else:
            raise NotImplementedError

    """----------------------------------------------------------------------------------"""

    def load_graph_contour(self, figure, path_save=None):
        """Cette focntion créer une nouvelle figure avec les paramettre de la figure donné, pas de try cach ici
        cela se fait dans les fonctions du dessus"""

        if figure.is_data_set_contour() != 1:
            return
        else:
            if "norm" in figure.kwarks:
                norm_min = figure.kwarks["norm"][0]
                norm_max = figure.kwarks["norm"][1]

                if norm_min == -1:
                    norm_min = 0

                if norm_max == -1:
                    _max = 0
                    for i in range(len(figure.z1_axe.data[0].data[0])):
                        _max = max(_max, figure.z1_axe.data[0].data[0][i])
                    norm_max = int(_max)

            else:
                # approximation, on ne check que le premier cycle
                _max = 0
                for i in range(len(figure.z1_axe.data[0].data[0])):
                    _max = max(_max, figure.z1_axe.data[0].data[0][i])

                norm_min = 0
                norm_max = int(_max)

            # self.format_figure(figure)
            pplot.rcParams.update({'font.size': 18})

            data_x = figure.x_axe.data
            data_y1 = figure.y1_axe.data
            data_z1 = figure.z1_axe.data

            fig = pplot.figure()
            fig.set_size_inches(11, 7)
            fig.canvas.manager.set_window_title(figure.plot_name)
            pplot.suptitle(figure.plot_name)
            ax1 = fig.add_subplot()

            pas = int((norm_max - norm_min) / 8)

            for i in range(len(data_x)):
                if norm_min == -1:
                    contourf_ = ax1.contourf(data_x[i].data, data_y1[i].data, data_z1[i].data,
                                             cmap=data_x[i].get_color_map())
                else:
                    contourf_ = ax1.contourf(data_x[i].data, data_y1[i].data, data_z1[i].data,
                                             levels=np.linspace(norm_min, norm_max, num=200),
                                             extend='both', cmap=figure.y1_axe.color_map)

            if norm_min == -1:
                cbar = fig.colorbar(contourf_)
            else:
                cbar = fig.colorbar(contourf_, ticks=range(norm_min, norm_max, pas))
            cbar.ax.set_ylabel(figure.z1_axe.name_unit, rotation=90, labelpad=0.7)

            ax1.set_xlabel(figure.x_axe.name_unit, labelpad=20)
            ax1.set_ylabel(figure.y1_axe.name_unit, labelpad=20)

            format_axes_figure(figure, ax1, None)

            if path_save is not None:
                pplot.tight_layout()
                pplot.close(fig)
                fig.savefig(path_save, bbox_inches='tight', dpi=150)

            return fig, ax1, contourf_, cbar, None, None, None

    """----------------------------------------------------------------------------------"""

    def get_info_data(self):
        print("info sur les données : " + self.name + "\n")
        temp = ""
        for i in range(len(self.data["row_data"])):
            temp += self.data["row_data"][i] + " | "
            if i % 5 == 0:
                temp += "\n"
        print(Resources.justify(temp))

    """----------------------------------------------------------------------------------"""

    def set_current_figure_name(self, name):
        if name == "":
            return
        for figure in self.figures:
            if figure.name == name:
                self.current_figure = figure
                return

        raise ValueError

    """----------------------------------------------------------------------------------"""

    def get_format_time(self):
        return self.resource.time_format[5:len(self.resource.time_format)]

    """----------------------------------------------------------------------------------"""

    def return_create_cycle(self, loop_data):
        """

        :param cycle: list de cycle : None, => all

        :return:
        """
        if loop_data is not None:
            if len(loop_data) == 3:
                if loop_data[1] == "to":
                    if loop_data[2] < len(self.data["loop_data"]) and loop_data[0] != 0 and loop_data[2] != 0:
                        loop_data = self.create_cycle_to(loop_data[0], loop_data[2])
                    else:
                        return
            else:
                for i in range(len(loop_data)):
                    loop_data[i] -= 1

            for i in loop_data:
                if i > len(self.data["loop_data"]) or i < 0:
                    emit = Emit()
                    emit.emit("msg_console", type="msg_console", str="Numéro de cycle " + str(i) + " invalide",
                              foreground_color="red")
                    emit.emit("msg_console", type="msg_console", str="Cycle compris entre 1 et " +
                                                                     str(len(self.data["loop_data"])),
                              foreground_color="red")
                    return None
            return loop_data
        else:
            return [i for i in range(len(self.data["loop_data"]))]

    """----------------------------------------------------------------------------------"""

    def create_unit_array(self):
        if "row_unit" not in self.data:
            units = []
            for name in self.data["row_data"]:
                units.append(Resources.UNITS[name])

            self.data["row_unit"] = units

    """----------------------------------------------------------------------------------"""

    def get_unit_name(self, unit_name):
        for unit in self.data["row_unit"]:
            if unit.name == unit_name:
                return unit
        raise ValueError

    """----------------------------------------------------------------------------------"""

    def create_cycle_to(self, min, max):
        if min > max:
            raise ValueError
        return_array = []
        for i in range(min - 1, max):
            return_array.append(i)
        return return_array

    """----------------------------------------------------------------------------------"""

    def create_array_cycle_all(self, loop_data):
        """
        On créer un array contenant tous les cycle, 0 => cycle1, 1 => cycle2 etc...
        En input loop data est un dictionaire, la fonction suivante fait pareil mais avec un array en input
        Un dictionnaire en entrèe car l'on cherche le plus petit nombre de loop contenue dedans. Utilisé quand
        on traite des loop de fichier différents

        :param loop_data: dictionaire ayant pour clé le nom d'un fichier de donnée ouvert et pour value
                          une list contenant les index des loop du fichier ec_lab correspondant

        :return: list contenant les numéros de cycles associé au dictionaire loop_data
        """

        return_array = []
        m = 0
        for i, j in enumerate(loop_data):
            m = min(m, len(loop_data[j]))

        for i in range(m):
            return_array.append(i)

        return return_array

    """----------------------------------------------------------------------------------"""

    @property
    @abstractmethod
    def data(self):
        pass

    @property
    @abstractmethod
    def name(self):
        pass

    @property
    @abstractmethod
    def nom_cell(self):
        pass

    @property
    @abstractmethod
    def figures(self):
        pass

    @property
    @abstractmethod
    def current_figure(self):
        pass

    @property
    @abstractmethod
    def resource(self):
        pass

    """                                                  """
    """                      setter                      """
    """                                                  """

    @data.setter
    @abstractmethod
    def data(self, data):
        pass

    @name.setter
    @abstractmethod
    def name(self, name):
        pass

    @nom_cell.setter
    @abstractmethod
    def nom_cell(self, name):
        pass

    @figures.setter
    @abstractmethod
    def figures(self, figures):
        pass

    @current_figure.setter
    @abstractmethod
    def current_figure(self, figure):
        pass

    @resource.setter
    @abstractmethod
    def resource(self, resource):
        pass
