from abc import ABC, abstractmethod

import matplotlib
import matplotlib.pyplot as pplot
from Resources import Resources


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

        """for tick in ax1.zaxis.get_major_ticks():
            tick.label1.set_fontsize(18)
            tick.label1.set_fontweight('bold')"""

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

        """for tick in ax2.zaxis.get_major_ticks():
            tick.label1.set_fontsize(18)
            tick.label1.set_fontweight('bold')"""


class Abstract_data(ABC):
    def __init__(self):
        self._data = None
        self._name = None
        #self._nom_cell = None
        self._nom_cell = "temp"
        self._figures = []
        self._current_figure = None

        self._loop = False
        self._pos_x = None
        self._pos_y = None
        self._index = None

        self.resource = Resources.Resource_class()

    """----------------------------------------------------------------------------------"""

    @abstractmethod
    def get_operation_available(self):
        pass

    """----------------------------------------------------------------------------------"""

    @abstractmethod
    def capa(self):
        pass

    """----------------------------------------------------------------------------------"""

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
                self.unique_name(name)
        return name

    """----------------------------------------------------------------------------------"""

    def load_graph2(self, figure, path_save=None):
        """Cette focntion créer une nouvelle figure avec les paramettre de la figure donné, pas de try cach ici
        cela se fait dans les fonctions du dessus"""

        if figure.is_data_set() != 1:
            return
        else:
            self.format_figure(figure)

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
            ax2 = None

            fig.canvas.manager.set_window_title(figure.plot_name)

            fig.suptitle(figure.plot_name)

            if figure.name_axes_x != "":
                ax1.set_xlabel(figure.name_axes_x, labelpad=20)
            else:
                ax1.set_xlabel(figure.data_x[0].name, labelpad=20)

            if figure.name_axes_y1 != "":
                ax1.set_ylabel(figure.name_axes_y1, labelpad=20)
            else:
                ax1.set_ylabel(figure.data_y1[0].name, labelpad=20)

            data_x = figure.data_x
            data_y1 = figure.data_y1
            data_y2 = figure.data_y2

            if figure.format_line_y1 is None:
                format_line_y1 = '-'
            else:
                format_line_y1 = figure.format_line_y1

            if figure.format_line_y2 is None:
                format_line_y2 = '-'
            else:
                format_line_y2 = figure.format_line_y2

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

            nb_y2 = 0
            for i in range(len(data_y2)):
                if data_y2[i].legend is not None:
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

            self.format_axes(ax1, figure.type, "y1")
            if len(data_x) != 0:
                """Dans ce cas pas besoin de faire grnad chose, on boucle sur data_y1 et on prends data_x[0]
                à chaque fois"""
                if len(data_x) == 1:
                    for i in range(len(data_y1)):
                        if len(modulo_y1) == 0 or (
                                index_modulo_y1 < len(modulo_y1) and i == modulo_y1[index_modulo_y1]):
                            index_modulo_y1 += 1
                            if data_y1[i].color is not None:
                                ax1.plot(data_x[0].data, data_y1[i].data, format_line_y1, markersize=figure.marker_size,
                                         label=data_y1[i].legend,
                                         color=data_y1[i].color)
                            else:
                                ax1.plot(data_x[0].data, data_y1[i].data, format_line_y1, markersize=figure.marker_size,
                                         label=data_y1[i].legend)
                        else:
                            if data_y1[i].color is not None:
                                ax1.plot(data_x[0].data, data_y1[i].data, format_line_y1, markersize=figure.marker_size,
                                         color=data_y1[i].color)
                            else:
                                ax1.plot(data_x[0].data, data_y1[i].data, format_line_y1, markersize=figure.marker_size)

                elif len(data_x) != len(data_y1) + len(data_y2):
                    """nb compte le nombre de fois ou l'origine de la data n'est pas celui de la figure
                    dans ce cas on prends la data_x[i] et incrémente i"""
                    nb = 0
                    for i in range(len(data_y1)):
                        if self.name != data_y1[i].source:
                            nb += 1
                            if len(modulo_y1) == 0 or (
                                    index_modulo_y1 < len(modulo_y1) and i == modulo_y1[index_modulo_y1]):
                                index_modulo_y1 += 1
                                if data_y1[i].color is not None:
                                    ax1.plot(data_x[nb].data, data_y1[i].data, format_line_y1,
                                             markersize=figure.marker_size,
                                             label=data_y1[i].legend,
                                             color=data_y1[i].color)
                                else:
                                    ax1.plot(data_x[nb].data, data_y1[i].data, format_line_y1,
                                             markersize=figure.marker_size,
                                             label=data_y1[i].legend)
                            else:
                                if data_y1[i].color is not None:
                                    ax1.plot(data_x[nb].data, data_y1[i].data, format_line_y1,
                                             markersize=figure.marker_size, color=data_y1[i].color)
                                else:
                                    ax1.plot(data_x[nb].data, data_y1[i].data, format_line_y1,
                                             markersize=figure.marker_size)
                        else:
                            if index_modulo_y1 < len(modulo_y1) and i == modulo_y1[index_modulo_y1]:
                                if data_y1[i].color is not None:
                                    ax1.plot(data_x[0].data, data_y1[i].data, format_line_y1,
                                             markersize=figure.marker_size,
                                             label=data_y1[i].legend,
                                             color=data_y1[i].color)
                                else:
                                    ax1.plot(data_x[0].data, data_y1[i].data, format_line_y1,
                                             markersize=figure.marker_size,
                                             label=data_y1[i].legend)
                            else:
                                if data_y1[i].color is not None:
                                    ax1.plot(data_x[0].data, data_y1[i].data, format_line_y1,
                                             markersize=figure.marker_size, color=data_y1[i].color)
                                else:
                                    ax1.plot(data_x[0].data, data_y1[i].data, format_line_y1,
                                             markersize=figure.marker_size)
                else:
                    """Pas grand chose à faire non plus, data_x et data_y1 sont associé 1 à 1, on boucle sur data_y1
                    et prends l'index pour les deux"""
                    for i in range(len(data_y1)):
                        if len(modulo_y1) == 0 or (
                                index_modulo_y1 < len(modulo_y1) and i == modulo_y1[index_modulo_y1]):
                            index_modulo_y1 += 1
                            if data_y1[i].color is not None:
                                ax1.plot(data_x[i].data, data_y1[i].data, format_line_y1, markersize=figure.marker_size,
                                         label=data_y1[i].legend,
                                         color=data_y1[i].color)
                            else:
                                ax1.plot(data_x[i].data, data_y1[i].data, format_line_y1, markersize=figure.marker_size,
                                         label=data_y1[i].legend)
                        else:
                            if data_y1[i].color is not None:
                                ax1.plot(data_x[i].data, data_y1[i].data, format_line_y1, markersize=figure.marker_size,
                                         color=data_y1[i].color)
                            else:
                                ax1.plot(data_x[i].data, data_y1[i].data, format_line_y1, markersize=figure.marker_size)

                h, l = ax1.get_legend_handles_labels()
                leg1.legend(h, l, borderaxespad=0, loc="upper right")
                leg1.axis("off")

                if figure.start_x is not None and figure.end_x is not None:
                    ax1.set_xlim(figure.start_x, figure.end_x)

                elif figure.start_x is not None:
                    x_min, x_max = ax1.get_xlim()
                    ax1.set_xlim(figure.start_x, x_max)

                elif figure.end_x is not None:
                    x_min, x_max = ax1.get_xlim()
                    ax1.set_xlim(x_min, figure.end_x)

                if figure.start_y1 is not None and figure.end_y1 is not None:
                    ax1.set_ylim(figure.start_y1, figure.end_y1)

                elif figure.start_y1 is not None:
                    y_min, y_max = ax1.get_ylim()
                    ax1.set_ylim(figure.start_y1, y_max)

                elif figure.end_y1 is not None:
                    y_min, y_max = ax1.get_xlim()
                    ax1.set_ylim(y_min, figure.end_y1)

            if len(data_y2) != 0:
                ax2 = ax1.twinx()
                leg2 = leg1.twinx()
                self.format_axes(ax2, figure.type, "y2")

                if figure.start_y2 is not None and figure.end_y2 is not None:
                    ax2.set_ylim(figure.start_y2, figure.end_y2)
                elif figure.start_y2 is not None:
                    y_min, y_max = ax2.get_ylim()
                    ax2.set_ylim(figure.start_y2, y_max)
                elif figure.end_y2 is not None:
                    y_min, y_max = ax2.get_xlim()
                    ax2.set_ylim(y_min, figure.end_y2)

                couleur = []
                for name in reversed(matplotlib.colors.cnames.items()):
                    couleur.append(name[0])

                if figure.name_axes_y2 != "":
                    ax2.set_ylabel(figure.name_axes_y2)
                else:
                    ax2.set_ylabel(data_y2[0].name, labelpad=10)

                index_color = 0

                if len(data_x) == 1:
                    for i in range(len(data_y2)):
                        if index_color == len(couleur):
                            index_color = 0

                        if len(modulo_y2) == 0 or (
                                index_modulo_y2 < len(modulo_y2) and i == modulo_y2[index_modulo_y2]):
                            index_modulo_y2 += 1
                            if data_y2[i].color is not None:
                                ax2.plot(data_x[0].data, data_y2[i].data, format_line_y2, markersize=figure.marker_size,
                                         color=data_y2[i].color,
                                         label=data_y2[i].legend)
                            else:
                                ax2.plot(data_x[0].data, data_y2[i].data, format_line_y2, markersize=figure.marker_size,
                                         color=couleur[index_color],
                                         label=data_y2[i].legend)
                        else:
                            if data_y2[i].color is not None:
                                ax2.plot(data_x[0].data, data_y2[i].data, format_line_y2, markersize=figure.marker_size,
                                         color=data_y1[i].color)
                            else:
                                ax2.plot(data_x[0].data, data_y2[i].data, format_line_y2, markersize=figure.marker_size,
                                         color=couleur[index_color])
                        index_color += 1
                elif len(data_x) != len(data_y1) + len(data_y2):
                    """nb compte le nombre de fois ou l'origine de la data n'est pas celui de la figure
                    dans ce cas on prends la data_x[i] et incrémente i"""
                    for i in range(len(data_y2)):
                        if index_color == len(couleur):
                            index_color = 0
                        if self.name != data_y2[i].source:
                            nb += 1
                            """nb n'est pas remis à zero ici pour garder la trace du nombre de décalage dans data_x
                            on a effectuer dans data_y1"""
                            if len(modulo_y2) == 0 or (
                                    index_modulo_y2 < len(modulo_y2) and i == modulo_y2[index_modulo_y2]):
                                index_modulo_y2 += 1
                                if data_y2[i].color is not None:
                                    ax2.plot(data_x[nb].data, data_y2[i].data, format_line_y2,
                                             markersize=figure.marker_size,
                                             label=data_y2[i].legend,
                                             color=data_y2[i].color)
                                else:
                                    ax2.plot(data_x[nb].data, data_y2[i].data, format_line_y2,
                                             markersize=figure.marker_size,
                                             label=data_y2[i].legend)
                            else:
                                if data_y2[i].color is not None:
                                    ax2.plot(data_x[nb].data, data_y2[i].data, format_line_y2,
                                             markersize=figure.marker_size, color=data_y2[i].color)
                                else:
                                    ax2.plot(data_x[nb].data, data_y2[i].data, format_line_y2,
                                             markersize=figure.marker_size)
                            index_color += 1
                else:
                    for i in range(len(data_y2)):
                        if index_color == len(couleur):
                            index_color = 0
                        if len(modulo_y2) == 0 or (
                                index_modulo_y2 < len(modulo_y2) and i == modulo_y2[index_modulo_y2]):
                            index_modulo_y2 += 1
                            if data_y2[i].color is not None:
                                ax2.plot(data_x[len(data_y1) + i].data, data_y2[i].data, format_line_y2,
                                         markersize=figure.marker_size,
                                         color=data_y2[i].color,
                                         label=data_y2[i].legend)
                            else:
                                ax2.plot(data_x[len(data_y1) + i].data, data_y2[i].data, format_line_y2,
                                         markersize=figure.marker_size,
                                         color=couleur[index_color],
                                         label=data_y2[i].legend)
                        else:
                            if data_y2[i].color is not None:
                                ax2.plot(data_x[len(data_y1) + i].data, data_y2[i].data, format_line_y2,
                                         markersize=figure.marker_size,
                                         color=data_y2[i].color)
                            else:
                                ax2.plot(data_x[len(data_y1) + i].data, data_y2[i].data, format_line_y2,
                                         markersize=figure.marker_size,
                                         color=couleur[index_color])
                        index_color += 1
                h, l = ax2.get_legend_handles_labels()
                leg2.legend(h, l, borderaxespad=0, loc="lower right")
                leg2.axis("off")

                if figure.start_y2 is not None and figure.end_y2 is not None:
                    ax2.set_ylim(figure.start_y2, figure.end_y2)
                elif figure.start_y2 is not None:
                    y_min, y_max = ax2.get_ylim()
                    ax2.set_ylim(figure.start_y2, y_max)
                elif figure.end_y2 is not None:
                    y_min, y_max = ax2.get_xlim()
                    ax2.set_ylim(y_min, figure.end_y2)

            self.resize_axe(ax1, ax2, figure.zoom, figure)

            if path_save is not None:
                pplot.tight_layout()
                pplot.close(fig)
                fig.savefig(path_save, bbox_inches='tight', dpi=150)

            return fig, ax1, ax2, value, val_freq, leg1

    """----------------------------------------------------------------------------------"""

    def load_graph(self, figure, path_save=None):
        """on s'assure que la figure est le même nombre de data sur l'axe des x que des y1 + y2"""
        figure.format_x_axe()

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
                        ax1.plot(data_x[i].data, data_y1[i].data, format_line_y1, markersize=figure.marker_size,
                                 label=data_y1[i].legend,
                                 color=data_y1[i].color)
                    else:
                        ax1.plot(data_x[i].data, data_y1[i].data, format_line_y1, markersize=figure.marker_size,
                                 label=data_y1[i].legend)
                else:
                    if data_y1[i].color is not None:
                        ax1.plot(data_x[i].data, data_y1[i].data, format_line_y1, markersize=figure.marker_size,
                                 color=data_y1[i].color)
                    else:
                        ax1.plot(data_x[i].data, data_y1[i].data, format_line_y1, markersize=figure.marker_size)

            h, l = ax1.get_legend_handles_labels()
            leg1.legend(h, l, borderaxespad=0, loc="upper right")
            leg1.axis("off")

            ax1.set_xlabel(figure.x_axe.name, labelpad=20)
            ax1.set_ylabel(figure.y1_axe.name, labelpad=20)

        """----------------------------------------------------------------------------------"""
        """                                        y2                                        """
        """----------------------------------------------------------------------------------"""

        if figure.y2_axe is not None:
            couleur = []
            for name in reversed(matplotlib.colors.cnames.items()):
                couleur.append(name[0])

            ax2 = ax1.twinx()
            leg2 = leg1.twinx()

            if figure.y1_axe is None:
                len_y1 = 0
            else:
                len_y1 = len(figure.y1_axe)

            data_y2 = figure.y2_axe.data

            if figure.format_line_y2 is None:
                format_line_y2 = '-'
            else:
                format_line_y2 = figure.format_line_y2

            nb_y2 = 0
            for i in range(len(data_y2)):
                if data_y2[i].legend is not None:
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
                        ax2.plot(data_x[i + len_y1].data, data_y2[i].data, format_line_y2, markersize=figure.marker_size,
                                 label=data_y2[i].legend,
                                 color=data_y2[i].color)
                    else:
                        ax2.plot(data_x[i+ len_y1].data, data_y2[i].data, format_line_y2, markersize=figure.marker_size,
                                 color=couleur[index_color], label=data_y2[i].legend)
                else:
                    if data_y2[i].color is not None:
                        ax2.plot(data_x[i + len_y1].data, data_y2[i].data, format_line_y2, markersize=figure.marker_size,
                                 color=data_y2[i].color)
                    else:
                        ax2.plot(data_x[i+ len_y1].data, data_y2[i].data, format_line_y2, markersize=figure.marker_size,
                                 color=couleur[index_color])

            h, l = ax2.get_legend_handles_labels()
            leg2.legend(h, l, borderaxespad=0, loc="lower right")
            leg2.axis("off")

            ax2.set_ylabel(figure.y2_axe.name, labelpad=20)

        format_axes_figure(figure, ax1, ax2)

        if path_save is not None:
            pplot.tight_layout()
            pplot.close(fig)
            fig.savefig(path_save, bbox_inches='tight', dpi=150)

        return fig, ax1, ax2, value, val_freq, leg1

    """----------------------------------------------------------------------------------"""

    def load_graph_bar(self, figure, path_save=None):
        """on s'assure que la figure est le même nombre de data sur l'axe des x que des y1 + y2"""
        figure.format_x_axe()

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

            ax1.set_xlabel(figure.x_axe.name, labelpad=20)
            ax1.set_ylabel(figure.y1_axe.name, labelpad=20)

            format_axes_figure(figure, ax1, None)

        if path_save is not None:
            pplot.tight_layout()
            pplot.close(fig)
            fig.savefig(path_save, bbox_inches='tight', dpi=150)

        return fig, ax1, None, value, val_freq, leg1

    """----------------------------------------------------------------------------------"""

    def load_graph_bar2(self, figure, path_save=None):
        """Cette focntion créer une nouvelle figure avec les paramettre de la figure donné, pas de try cach ici
        cela se fait dans les fonctions du dessus"""

        if figure.is_data_set() != 1:
            return
        else:
            self.format_figure(figure)

            pplot.rcParams.update({'font.size': 18})

            fig, (ax1, leg1) = pplot.subplots(ncols=2, gridspec_kw={"width_ratios": [10, 1]})

            fig.set_size_inches(11, 7)

            fig.canvas.manager.set_window_title(figure.plot_name)

            pplot.suptitle(figure.plot_name)

            if figure.name_axes_x != "":
                ax1.set_xlabel(figure.name_axes_x, labelpad=20)
            else:
                ax1.set_xlabel(figure.data_x[0].name, labelpad=20)

            if figure.name_axes_y1 != "":
                ax1.set_ylabel(figure.name_axes_y1, labelpad=20)
            else:
                ax1.set_ylabel(figure.data_y1[0].name, labelpad=20)

            data_x = figure.data_x
            data_y1 = figure.data_y1
            data_y2 = figure.data_y2

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

            largeur = 0.75

            self.format_axes(ax1, figure.type, "y1")
            if len(data_x) != 0:
                """Dans ce cas pas besoin de faire grnad chose, on boucle sur data_y1 et on prends data_x[0]
                à chaque fois"""
                if len(data_x) == 1:
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

                elif len(data_x) != len(data_y1) + len(data_y2):
                    """nb compte le nombre de fois ou l'origine de la data n'est pas celui de la figure
                    dans ce cas on prends la data_x[i] et incrémente i"""
                    nb = 0
                    for i in range(len(data_y1)):
                        if self.name != data_y1[i].source:
                            nb += 1
                            if len(modulo_y1) == 0 or (
                                    index_modulo_y1 < len(modulo_y1) and i == modulo_y1[index_modulo_y1]):
                                index_modulo_y1 += 1
                                if data_y1[i].color is not None:
                                    ax1.bar(data_x[nb].data, data_y1[i].data,
                                            width=largeur,
                                            label=data_y1[i].legend,
                                            color=data_y1[i].color)
                                else:
                                    ax1.bar(data_x[nb].data, data_y1[i].data,
                                            width=largeur,
                                            label=data_y1[i].legend)
                            else:
                                if data_y1[i].color is not None:
                                    ax1.bar(data_x[nb].data, data_y1[i].data,
                                            width=largeur,
                                            color=data_y1[i].color)
                                else:
                                    ax1.bar(data_x[nb].data, data_y1[i].data, width=largeur)
                        else:
                            if index_modulo_y1 < len(modulo_y1) and i == modulo_y1[index_modulo_y1]:
                                if data_y1[i].color is not None:
                                    ax1.bar(data_x[0].data, data_y1[i].data,
                                            label=data_y1[i].legend,
                                            width=largeur,
                                            color=data_y1[i].color)
                                else:
                                    ax1.bar(data_x[0].data, data_y1[i].data, label=data_y1[i].legend,
                                            width=largeur)
                            else:
                                if data_y1[i].color is not None:
                                    ax1.bar(data_x[0].data, data_y1[i].data, color=data_y1[i].color, width=largeur)
                                else:
                                    ax1.bar(data_x[0].data, data_y1[i].data, width=largeur)
                else:
                    """Pas grand chose à faire non plus, data_x et data_y1 sont associé 1 à 1, on boucle sur data_y1
                    et prends l'index pour les deux"""
                    for i in range(len(data_y1)):
                        if len(modulo_y1) == 0 or (
                                index_modulo_y1 < len(modulo_y1) and i == modulo_y1[index_modulo_y1]):
                            index_modulo_y1 += 1
                            if data_y1[i].color is not None:
                                ax1.bar(data_x[i].data, data_y1[i].data,
                                        width=largeur,
                                        label=data_y1[i].legend,
                                        color=data_y1[i].color)
                            else:
                                ax1.bar(data_x[i].data, data_y1[i].data,
                                        width=largeur,
                                        label=data_y1[i].legend)
                        else:
                            if data_y1[i].color is not None:
                                ax1.bar(data_x[i].data, data_y1[i].data,
                                        width=largeur,
                                        color=data_y1[i].color)
                            else:
                                ax1.bar(data_x[i].data, data_y1[i].data, width=largeur)

                h, l = ax1.get_legend_handles_labels()
                leg1.legend(h, l, borderaxespad=0, loc="upper right")
                leg1.axis("off")

                if figure.start_x is not None and figure.end_x is not None:
                    ax1.set_xlim(figure.start_x, figure.end_x)

                elif figure.start_x is not None:
                    x_min, x_max = ax1.get_xlim()
                    ax1.set_xlim(figure.start_x, x_max)

                elif figure.end_x is not None:
                    x_min, x_max = ax1.get_xlim()
                    ax1.set_xlim(x_min, figure.end_x)

                if figure.start_y1 is not None and figure.end_y1 is not None:
                    ax1.set_ylim(figure.start_y1, figure.end_y1)

                elif figure.start_y1 is not None:
                    y_min, y_max = ax1.get_ylim()
                    ax1.set_ylim(figure.start_y1, y_max)

                elif figure.end_y1 is not None:
                    y_min, y_max = ax1.get_xlim()
                    ax1.set_ylim(y_min, figure.end_y1)

            if path_save is not None:
                pplot.tight_layout()
                pplot.close(fig)
                fig.savefig(path_save, bbox_inches='tight', dpi=150)

            return fig, ax1, None, None, None, leg1

    """----------------------------------------------------------------------------------"""

    def resize_axe(self, axe1, axe2, p, figure=None):
        if figure is not None and figure.type == "bode":
            return
        else:
            p = -p
            size_axe_x = axe1.get_xlim()[1] - axe1.get_xlim()[0]
            axe1.set_xlim(axe1.get_xlim()[0] - (size_axe_x * p / 100), axe1.get_xlim()[1] + (size_axe_x * p / 100))

            size_axe_y1 = axe1.get_ylim()[1] - axe1.get_ylim()[0]
            axe1.set_ylim(axe1.get_ylim()[0] - (size_axe_y1 * p / 100), axe1.get_ylim()[1] + (size_axe_y1 * p / 100))

            if axe2 is not None:
                size_axe_y2 = axe2.get_ylim()[1] - axe2.get_ylim()[0]
                axe2.set_ylim(axe2.get_ylim()[0] - (size_axe_y2 * p / 100),
                              axe2.get_ylim()[1] + (size_axe_y2 * p / 100))

    """----------------------------------------------------------------------------------"""

    def format_figure(self, figure):
        if figure.name_axes_y1 == "":
            if figure.data_y1[0].name == "Ecell/V":
                #figure.data_y1[i].name = self.resource.Ecell_name_format
                figure.name_axes_y1 = self.resource.Ecell_name_format

            elif figure.data_y1[0].name == "<I>/mA":
                # figure.data_y1[i].name = self.resource.I_format
                figure.name_axes_y1 = self.resource.I_format

            elif figure.data_y1[0].name == "time/h":
                #figure.data_y1[i].name = self.resource.time_h_format
                figure.name_axes_y1 = self.resource.time_h_format

            elif figure.data_y1[0].name == "time/s":
                #figure.data_y1[i].name = self.resource.time_s_format
                figure.name_axes_y1 = self.resource.time_s_format

            elif figure.data_y1[0].name == "time/min":
                #figure.data_y1[i].name = self.resource.time_min_format
                figure.name_axes_y1 = self.resource.time_min_format

            elif figure.data_y1[0].name == "Q_charge/mA.h":
                #figure.data_y1[i].name = self.resource.Q_charge_format
                figure.name_axes_y1 = self.resource.Q_charge_format

            elif figure.data_y1[0].name == "(Q-Qo)/mA.h derive":
                #figure.data_y1[i].name = "dQ / dE"
                figure.name_axes_y1 = "dQ / dE"

            elif figure.data_y1[0].name == "Ecell/V derive":
                #figure.data_y1[i].name = self.resource.Ecell_name_format
                figure.name_axes_y1 = self.resource.Ecell_name_format

        if figure.name_axes_y2 == "":
            if figure.data_y2[0].name == "Ecell/V":
                #figure.data_y2[i].name = self.resource.Ecell_name_format
                figure.name_axes_y2 = self.resource.Ecell_name_format

            elif figure.data_y2[0].name == "<I>/mA":
                #figure.data_y2[i].name = self.resource.I_format
                figure.name_axes_y2 = self.resource.I_format

            elif figure.data_y2[0].name == "time/h":
                #figure.data_y2[i].name = self.resource.time_h_format
                figure.name_axes_y2 = self.resource.time_h_format

            elif figure.data_y2[0].name == "time/s":
                #figure.data_y2[i].name = self.resource.time_s_format
                figure.name_axes_y2 = self.resource.time_s_format

            elif figure.data_y2[0].name == "time/min":
                #figure.data_y2[i].name = self.resource.time_min_format
                figure.name_axes_y2 = self.resource.time_min_format

            elif figure.data_y2[0].name == "Q_charge/mA.h":
                #figure.data_y2[i].name = self.resource.Q_charge_format
                figure.name_axes_y2 = self.resource.Q_charge_format

            elif figure.data_y2[0].name == "(Q-Qo)/mA.h derive":
                #figure.data_y2[i].name = "dQ / dE"
                figure.name_axes_y2 = "dQ / dE"

            elif figure.data_y2[0].name == "Ecell/V derive":
                #figure.data_y2[i].name = self.resource.Ecell_name_format
                figure.name_axes_y2 = self.resource.Ecell_name_format

        if figure.name_axes_x == "":
            if figure.data_x[0].name == "Ecell/V":
                #figure.data_x[0].name = self.resource.Ecell_name_format
                figure.name_axes_x = self.resource.Ecell_name_format

            elif figure.data_x[0].name == "<I>/mA":
                #figure.data_x[0].name = self.resource.I_format
                figure.name_axes_x = self.resource.I_format

            elif figure.data_x[0].name == "time/h":
                #figure.data_x[0].name = self.resource.time_h_format
                figure.name_axes_x = self.resource.time_h_format

            elif figure.data_x[0].name == "time/s":
                #figure.data_x[0].name = self.resource.time_s_format
                figure.name_axes_x = self.resource.time_s_format

            elif figure.data_x[0].name == "time/min":
                #figure.data_x[0].name = self.resource.time_min_format
                figure.name_axes_x = self.resource.time_min_format

            elif figure.data_x[0].name == "Q_charge/mA.h":
                #figure.data_x[0].name = self.resource.Q_charge_format
                figure.name_axes_x = self.resource.Q_charge_format

            elif figure.data_x[0].name == "(Q-Qo)/mA.h derive":
                #figure.data_x[0].name = "dQ / dE"
                figure.name_axes_x = "dQ / dE"

            elif figure.data_x[0].name == "Ecell/V derive":
                #figure.data_x[0].name = self.resource.Ecell_name_format
                figure.name_axes_x = self.resource.Ecell_name_format

    """----------------------------------------------------------------------------------"""

    def format_axes(self, axe, type, name):
        if type is not None and "3d" in type:
            if axe is not None:
                for tick in axe.xaxis.get_major_ticks():
                    tick.label1.set_fontsize(18)
                    tick.label1.set_fontweight('bold')
                for tick in axe.yaxis.get_major_ticks():
                    tick.label1.set_fontsize(18)
                    tick.label1.set_fontweight('bold')
                for tick in axe.yaxis.get_major_ticks():
                    tick.label2.set_fontsize(18)
                    tick.label2.set_fontweight('bold')
                for tick in axe.zaxis.get_major_ticks():
                    tick.label1.set_fontsize(18)
                    tick.label1.set_fontweight('bold')
                """je le fais comme ça vu qu'il n'y a que 1 graph en 3d, à modifier par la suite au cas ou"""
                axe.set_aspect('equal', 'box')
        else:
            if axe is not None:
                for tick in axe.xaxis.get_major_ticks():
                    tick.label1.set_fontsize(18)
                    tick.label1.set_fontweight('bold')
                for tick in axe.yaxis.get_major_ticks():
                    tick.label1.set_fontsize(18)
                    tick.label1.set_fontweight('bold')
                for tick in axe.yaxis.get_major_ticks():
                    tick.label2.set_fontsize(18)
                    tick.label2.set_fontweight('bold')

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
        for figure in self.figures:
            if figure.name == name:
                self.current_figure = figure
                return

        raise ValueError

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