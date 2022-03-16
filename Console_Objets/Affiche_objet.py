import math
from abc import ABC, abstractmethod

import numpy as np
from PyQt5.QtCore import pyqtSignal
from future.backports.datetime import date

from Resources_file import Resources

from Console_Objets import Data_array
from Console_Objets import Figure
import matplotlib
import matplotlib.pyplot as pplot
from matplotlib.backend_bases import MouseButton
from scipy.stats import linregress

from Resources_file.Emit import Emit


class Abstract_objet_affiche(ABC):

    def __init__(self, data, figure):
        from UI_interface.Main_windows_UI import Emit
        self.emit = Emit()

        self.can_emit = False

        self.data = data
        self.figure = figure
        self.pplot_fig = None
        self._finish = False
        self.open = False
        self.save = None
        """de la forme : [int, str]"""
        self.mpl_connect = []
        self.interactive = False

        # cette variable indique si les information du plot ont le droit d'être édité
        # par défaut True
        self.editable = True

        # fonction passé comme callback une fois que les traitements sont fini
        self.call_back_func = None

    @abstractmethod
    def create_figure(self):
        pass

    @abstractmethod
    def interact(self):
        pass

    @abstractmethod
    def update_pplot_fig(self):
        pass

    @abstractmethod
    def set_atteractive(self):
        pass

    @abstractmethod
    def reset_color(self):
        pass

    @abstractmethod
    def disconnect_all(self):
        pass

    @abstractmethod
    def connect_all(self):
        pass

    @abstractmethod
    def disconnect_name(self, name):
        pass

    @abstractmethod
    def focus_off(self):
        pass

    @abstractmethod
    def focus_on(self):
        pass

    @abstractmethod
    def on_click(self, event):
        pass

    @abstractmethod
    def on_close(self, event):
        pass

    @abstractmethod
    def on_key(self, event):
        pass


class Classique_affiche(Abstract_objet_affiche):

    def __init__(self, data, figure):
        super().__init__(data, figure)
        self.ax1 = None
        self.ax2 = None
        self.value = None
        self.freq = None
        self.leg1 = None
        self.leg2 = None

        self.resource = Resources.Resource_class()

        self.index = None
        self.pos_x = None
        self.pos_y = None
        self.ligne1 = None
        self.ligne2 = None

        self.__name__ = "Classique_affiche"

    """----------------------------------------------------------------------------------"""

    def create_figure(self):
        """la figure est recréée à chaque fois contrairement à la version console"""
        if self.pplot_fig is not None:
            pplot.close(self.pplot_fig)

        if self.figure.type == "3d" or self.figure.type == "impedance_3d" or self.figure.type == "impedance_3d_cycle":
            if self.figure.is_data_set_3d() == 1:
                if self.save is not None:
                    self.pplot_fig, self.ax1, self.ax2, self.value, self.freq, self.leg1, self.leg2 = \
                        self.data.load_graph_3d(self.figure, self.save)
                    pplot.close(self.pplot_fig)
                    self.finish = True
                    self.pplot_fig = None
                else:
                    self.pplot_fig, self.ax1, self.ax2, self.value, self.freq, self.leg1, self.leg2 = \
                        self.data.load_graph_3d(self.figure)
                    self.pplot_fig.tight_layout()

            else:
                raise ValueError

        elif self.figure.type == "bar":
            if self.figure.is_data_set_bar() == 1:
                if self.save is not None:
                    self.pplot_fig, self.ax1, self.ax2, self.value, self.freq, self.leg1, self.leg2 = \
                        self.data.load_graph_bar(self.figure, self.save)
                    pplot.close(self.pplot_fig)
                    self.finish = True
                    self.pplot_fig = None
                else:
                    self.pplot_fig, self.ax1, self.ax2, self.value, self.freq, self.leg1, self.leg2 = \
                        self.data.load_graph_bar(self.figure)
                    self.pplot_fig.tight_layout()

            else:
                raise ValueError

        elif self.figure.type == "res_fitting_temperature":
            # pour cette figure pas d'édition possible, pour le moment
            # et pour longtemps je pense
            self.editable = False
            if self.figure.is_data_set() == 1:
                if self.save is not None:
                    self.pplot_fig = self.data.load_graph_fit(self.figure, self.save)
                    pplot.close(self.pplot_fig)
                    self.finish = True
                    self.pplot_fig = None
                else:
                    self.pplot_fig = self.data.load_graph_fit(self.figure)
            else:
                raise ValueError

        elif self.figure.type == "res_fitting_temps":
            # pour cette figure pas d'édition possible, pour le moment
            # et pour longtemps je pense
            self.editable = False
            if self.figure.is_data_set() == 1:
                if self.save is not None:
                    self.pplot_fig = self.data.load_graph_fit(self.figure, self.save)
                    pplot.close(self.pplot_fig)
                    self.finish = True
                    self.pplot_fig = None
                else:
                    self.pplot_fig = self.data.load_graph_fit(self.figure)
            else:
                raise ValueError

        elif self.figure.type == "contour":
            if self.figure.is_data_set_contour() == 1:
                if self.save is not None:
                    self.pplot_fig, self.ax1, self.ax2, self.value, self.freq, self.leg1, self.leg2 = \
                        self.data.load_graph_contour(self.figure, self.save)
                    pplot.close(self.pplot_fig)
                    self.finish = True
                    self.pplot_fig = None
                else:
                    self.pplot_fig, self.ax1, self.ax2, self.value, self.freq, self.leg1, self.leg2 = \
                        self.data.load_graph_contour(self.figure)
                    self.pplot_fig.tight_layout()
            else:
                raise ValueError









        elif self.figure.type == "res_waxs":
            if self.figure.is_data_set() == 1:
                if self.save is not None:
                    self.pplot_fig = self.data.load_graph_affichage(self.figure, self.save)
                    pplot.close(self.pplot_fig)
                    self.finish = True
                    self.pplot_fig = None
                else:
                    self.pplot_fig = self.data.load_graph_affichage(self.figure)
            else:
                self.finish = True
                return False
        elif self.figure.type == "res_saxs":
            if self.figure.is_data_set() == 1:
                if self.save is not None:
                    self.pplot_fig = self.data.load_graph_affichage(self.figure, self.save)
                    pplot.close(self.pplot_fig)
                    self.finish = True
                    self.pplot_fig = None
                else:
                    self.pplot_fig = self.data.load_graph_affichage(self.figure)
            else:
                self.finish = True
                return False



        else:
            if self.figure.is_data_set() == 1:
                if self.save is not None:
                    self.pplot_fig, self.ax1, self.ax2, self.value, self.freq, self.leg1, self.leg2 = \
                        self.data.load_graph(self.figure, self.save)
                    pplot.close(self.pplot_fig)
                    self.finish = True
                    self.pplot_fig = None
                else:
                    self.pplot_fig, self.ax1, self.ax2, self.value, self.freq, self.leg1, self.leg2 \
                        = self.data.load_graph(self.figure)

                    self.pplot_fig.tight_layout()
            else:
                raise ValueError
        return True

    """----------------------------------------------------------------------------------"""

    def interact(self):
        black = matplotlib.colors.to_rgba("black")
        test = matplotlib.patches.Circle((0.0, 0.0), 0, color='white')

        if self.pos_x is not None:
            if self.index is None:

                index_x, index_y = Resources.index_array(self.figure, [self.pos_x, self.pos_y], self.ax1, self.ax2)

                self.index = [index_x, index_y]

                if self.index[1][0] == "y1":
                    count = 0
                    for line in self.ax1.lines:
                        if "#" in line.get_color():
                            if count != self.index[1][1]:
                                color = line.get_color()
                                color = str(color)
                                color += "50"
                                line.set_color(color)
                        elif len(line.get_color()) == 4:
                            if count != self.index[1][1]:
                                hex_color = matplotlib.colors.to_hex(line.get_color())
                                color = str(hex_color)
                                color += "50"
                                line.set_color(color)
                        count += 1
                    if self.ax2 is not None:
                        for line in self.ax2.lines:
                            if "#" in line.get_color():
                                color = line.get_color()
                                color = str(color)
                                color += "50"
                                line.set_color(color)
                            elif len(line.get_color()) == 4:
                                hex_color = matplotlib.colors.to_hex(line.get_color())
                                color = str(hex_color)
                                color += "50"
                                line.set_color(color)

                else:
                    count = 0
                    for line in self.ax2.lines:
                        if "#" in line.get_color():
                            if count != self.index[1][1]:
                                color = line.get_color()
                                color = str(color)
                                color += "50"
                                line.set_color(color)
                        elif len(line.get_color()) == 4:
                            if count != self.index[1][1]:
                                hex_color = matplotlib.colors.to_hex(line.get_color())
                                color = str(hex_color)
                                color += "50"
                                line.set_color(color)
                        count += 1

                    for line in self.ax1.lines:
                        if "#" in line.get_color():
                            color = line.get_color()
                            color = str(color)
                            color += "50"
                            line.set_color(color)
                        elif len(line.get_color()) == 4:
                            hex_color = matplotlib.colors.to_hex(line.get_color())
                            color = str(hex_color)
                            color += "50"
                            line.set_color(color)

            if self.index[0] != -1:
                xtickslocs = str(self.ax1.get_xticks()[1])
                ytickslocs = str(self.ax1.get_yticks()[1])

                len_x = 4
                find = False
                for i in range(len(xtickslocs)):
                    if xtickslocs[i] == ".":
                        find = True
                    if xtickslocs[i] != "0" and find:
                        len_x = + i + 4 + xtickslocs.find(".")
                        break
                len_y = 4
                find = False
                for i in range(len(ytickslocs)):
                    if ytickslocs[i] == ".":
                        find = True
                    if ytickslocs[i] != "0" and find:
                        len_y = i + 4 + ytickslocs.find(".")
                        break

                if self.index[1][0] == "y1":
                    try:
                        res = Resources.coord_to_point([[self.pos_x, self.pos_y]],
                                                       self.figure.x_axe.data[self.index[0][1]],
                                                       self.figure.y1_axe.data[self.index[1][1]])
                    except TypeError:
                        res = -1

                    if self.can_emit:
                        self.emit.emit("update_values", res=res, index=self.index)

                    if res != -1:
                        text_legend_pointed = self.figure.y1_axe.data[self.index[1][1]].legend

                        self.value.legend([test, test, test], [
                            'courbe : ' + str(text_legend_pointed),
                            'x : ' + str(self.figure.x_axe.data[self.index[0][1]].data[res])[0:len_x],
                            'y : ' + str(self.figure.y1_axe.data[self.index[1][1]].data[res])[0:len_y]],
                                          markerscale=0, borderaxespad=0, fontsize=14, loc="center right")

                        self.ligne1 = self.ax1.axhline(y=self.figure.y1_axe.data[self.index[1][1]].data[res],
                                                       color=black)
                        self.ligne2 = self.ax1.axvline(x=self.figure.x_axe.data[self.index[0][1]].data[res],
                                                       color=black)
                else:
                    res = Resources.coord_to_point([[self.pos_x, self.pos_y]],
                                                   self.figure.x_axe.data[self.index[0][1]],
                                                   self.figure.y2_axe.data[self.index[1][1]])

                    if self.can_emit:
                        self.emit.emit("update_values", res=res, index=self.index)

                    if res != -1:
                        text_legend_pointed = self.figure.y2_axe.data[self.index[1][1]].legend

                        self.value.legend([test, test, test], [
                            'courbe : ' + str(text_legend_pointed),
                            'x : ' + str(self.figure.x_axe.data[self.index[0][1]].data[res])[0:len_x],
                            'y : ' + str(self.figure.y2_axe.data[self.index[1][1]].data[res])[0:len_y]],
                                          markerscale=0, borderaxespad=0, fontsize=14, loc="center right")

                        ratio = (self.figure.y2_axe.data[self.index[1][1]].data[res] - self.ax2.get_ybound()[0]) / \
                                (self.ax2.get_ybound()[1] - self.ax2.get_ybound()[0])

                        self.ligne1 = self.ax1.axhline(
                            y=(self.ax1.get_ybound()[1] - self.ax1.get_ybound()[0]) * ratio + self.ax1.get_ybound()[0],
                            color=black)
                        self.ligne2 = self.ax1.axvline(x=self.figure.x_axe.data[self.index[0][1]].data[res],
                                                       color=black)

                if self.freq is not None:
                    self.freq.legend([test], [
                        'freq : ' + str(self.data.data.get("freq/Hz")[res])[0:len_x] + " Hz"],
                                     markerscale=0, borderaxespad=0, fontsize=14, loc="lower right")

                if res == -1:
                    text_legend_pointed = self.figure.y1_axe.data[self.index[1][1]].legend
                    self.value.legend([test, test, test], ['courbe : ' + str(text_legend_pointed),
                                                           'x : none', 'y : none'],
                                      markerscale=0, borderaxespad=0, fontsize=14, loc="center right")

                    if self.freq is not None:
                        self.freq.legend([test], ['freq : none'],
                                         markerscale=0, borderaxespad=0, fontsize=14, loc="lower right")
            else:
                text_legend_pointed = self.figure.y1_axe.data[self.index[1][1]].legend
                self.value.legend([test, test, test], ['courbe : ' + str(text_legend_pointed), 'x : none', 'y : none'],
                                  markerscale=0, borderaxespad=0, fontsize=14, loc="center right")
                if self.freq is not None:
                    self.freq.legend([test], ['freq : none'],
                                     markerscale=0, borderaxespad=0, fontsize=14, loc="lower right")

            self.pplot_fig.canvas.draw()

    """----------------------------------------------------------------------------------"""

    def update_pplot_fig(self):
        if self.ligne1 is not None:
            try:
                self.ax1.lines.remove(self.ligne1)
            except ValueError:
                pass
            self.ligne1 = None
        if self.ligne2 is not None:
            try:
                self.ax1.lines.remove(self.ligne2)
            except ValueError:
                pass
            self.ligne2 = None
        self.interact()

    """----------------------------------------------------------------------------------"""

    def disconnect_all(self):
        while len(self.mpl_connect) != 0:
            self.pplot_fig.canvas.mpl_disconnect(self.mpl_connect[0][0])
            del self.mpl_connect[0]

    """----------------------------------------------------------------------------------"""

    def disconnect_name(self, name):
        for i in range(len(self.mpl_connect)):
            if self.mpl_connect[i][1] == name:
                self.pplot_fig.canvas.mpl_disconnect(self.mpl_connect[i][0])
                del self.mpl_connect[i]
                return

    """----------------------------------------------------------------------------------"""

    def connect_all(self):
        self.mpl_connect.append([self.pplot_fig.canvas.mpl_connect('button_press_event', self.on_click),
                                 "button_press_event"])

    """----------------------------------------------------------------------------------"""

    def set_atteractive(self):
        if self.figure.is_interact() == 0:
            return False
        else:
            return True

    """----------------------------------------------------------------------------------"""

    def reset_color(self):
        for ax in self.pplot_fig.axes:
            for line in ax.lines:
                if "#" in line.get_color():
                    color = line.get_color()
                    if len(str(color)) == 9:
                        color = str(color)
                        color = color[0:7]
                        line.set_color(color)

        texts = self.leg1.get_legend().get_texts()
        for text in texts:
            text.set_c("black")

    """----------------------------------------------------------------------------------"""

    def on_move(self, event):
        self.pos_x = event.xdata
        self.pos_y = event.ydata

        # On retire les lignes si elles sont déjà tracés et execute self.interact
        self.update_pplot_fig()

    """----------------------------------------------------------------------------------"""

    def focus_off(self):
        if not self.editable or self.figure.type == "contour":
            return

        self.interactive = False
        self.index = None
        self.pos_x = None
        self.pos_y = None

        self.disconnect_name("motion_notify_event")

        if self.value is not None:
            self.value.set_visible(False)

        if self.freq is not None:
            self.freq.set_visible(False)

        if self.ligne1 is not None:
            try:
                self.ax1.lines.remove(self.ligne1)
            except ValueError:
                pass
            self.ligne1 = None

        if self.ligne2 is not None:
            try:
                self.ax1.lines.remove(self.ligne2)
            except ValueError:
                pass
            self.ligne2 = None

        self.reset_color()
        self.pplot_fig.canvas.draw()

    """----------------------------------------------------------------------------------"""

    def focus_on(self):
        if self.figure.is_interact() == 0:
            return
        else:
            self.interactive = True

        self.mpl_connect.append([self.pplot_fig.canvas.mpl_connect('motion_notify_event', self.on_move),
                                 "motion_notify_event"])

        self.value.set_visible(True)
        if self.freq is not None:
            self.freq.set_visible(True)

        self.interact()

    """----------------------------------------------------------------------------------"""

    def on_close(self, event):
        self.disconnect_all()
        pplot.close(self.pplot_fig)

    """----------------------------------------------------------------------------------"""

    def on_key(self, event):
        pass

    """----------------------------------------------------------------------------------"""

    def on_click(self, event):
        if event.dblclick and event.inaxes is not None and event.button == MouseButton.LEFT and \
                (event.inaxes == self.ax1 or event.inaxes == self.ax2):
            if self.interactive:
                self.focus_off()

            else:
                self.focus_on()

    """----------------------------------------------------------------------------------"""


class Edit_affiche(Abstract_objet_affiche):
    def __init__(self, data, figure, norm=None):
        super().__init__(data, figure)
        self.ax1 = None
        self.ax2 = None
        self.value = None
        self.freq = None
        self.leg1 = None
        self.leg2 = None

        self.resource = Resources.Resource_class()

        self.index = None
        self.pos_x = None
        self.pos_y = None
        self.ligne1 = None
        self.ligne2 = None

        self.norm = norm

        # cette variable indique si les information du plot ont le droit d'être édité
        # sur cette interaction là on ne veut pas, elle sert juste pour rtirer des points
        # le graph sera suprimé ensuite, aucun interet donc
        self.editable = False

        self.res = None

    """----------------------------------------------------------------------------------"""

    def create_figure(self):
        """la figure est recréée à chaque fois contrairement à la version console"""
        if self.pplot_fig is not None:
            pplot.close(self.pplot_fig)
        if self.figure.is_data_set() == 1:
            self.pplot_fig, self.ax1, self.ax2, self.value, self.freq, self.leg1, self.leg2 \
                = self.data.load_graph(self.figure)
            self.pplot_fig.tight_layout()
        else:
            raise ValueError

    """----------------------------------------------------------------------------------"""

    def interact(self):
        black = matplotlib.colors.to_rgba("black")
        test = matplotlib.patches.Circle((0.0, 0.0), 0, color='white')

        if self.pos_x is not None:
            if self.index is None:
                index_x, index_y = Resources.index_array(self.figure, [self.pos_x, self.pos_y], self.ax1, self.ax2)

                self.index = [index_x, index_y]

            if self.index[0] != -1:
                xtickslocs = str(self.ax1.get_xticks()[1])
                ytickslocs = str(self.ax1.get_yticks()[1])

                len_x = 4
                find = False
                for i in range(len(xtickslocs)):
                    if xtickslocs[i] == ".":
                        find = True
                    if xtickslocs[i] != "0" and find:
                        len_x = + i + 4 + xtickslocs.find(".")
                        break
                len_y = 4
                find = False
                for i in range(len(ytickslocs)):
                    if ytickslocs[i] == ".":
                        find = True
                    if ytickslocs[i] != "0" and find:
                        len_y = i + 4 + ytickslocs.find(".")
                        break
                try:
                    res = Resources.coord_to_point([[self.pos_x, self.pos_y]],
                                                   self.figure.x_axe.data[self.index[0][1]],
                                                   self.figure.y1_axe.data[self.index[1][1]])
                except TypeError:
                    res = -1
                self.res = res
                if res != -1:
                    text_legend_pointed = self.figure.y1_axe.data[self.index[1][1]].legend

                    self.value.legend([test, test, test], [
                        'courbe : ' + str(text_legend_pointed),
                        'x : ' + str(self.figure.x_axe.data[self.index[0][1]].data[res])[0:len_x],
                        'y : ' + str(self.figure.y1_axe.data[self.index[1][1]].data[res])[0:len_y]],
                                      markerscale=0, borderaxespad=0, fontsize=14, loc="center right")

                    self.ligne1 = self.ax1.axhline(y=self.figure.y1_axe.data[self.index[1][1]].data[res], color=black)
                    self.ligne2 = self.ax1.axvline(x=self.figure.x_axe.data[self.index[0][1]].data[res], color=black)

                    if self.freq is not None:
                        self.freq.legend([test], [
                            'freq : ' + str(self.data.data.get("freq/Hz")[res])[0:len_x] + " Hz"],
                                         markerscale=0, borderaxespad=0, fontsize=14, loc="lower right")

                else:
                    text_legend_pointed = self.figure.y1_axe.data[self.index[1][1]].legend
                    self.value.legend([test, test, test], ['courbe : ' + str(text_legend_pointed),
                                                           'x : none', 'y : none'],
                                      markerscale=0, borderaxespad=0, fontsize=14, loc="center right")

                    if self.freq is not None:
                        self.freq.legend([test], ['freq : none'],
                                         markerscale=0, borderaxespad=0, fontsize=14, loc="lower right")
            else:
                text_legend_pointed = self.figure.y1_axe.data[self.index[1][1]].legend
                self.value.legend([test, test, test], ['courbe : ' + str(text_legend_pointed), 'x : none', 'y : none'],
                                  markerscale=0, borderaxespad=0, fontsize=14, loc="center right")
                if self.freq is not None:
                    self.freq.legend([test], ['freq : none'],
                                     markerscale=0, borderaxespad=0, fontsize=14, loc="lower right")

            self.pplot_fig.canvas.draw()

    """----------------------------------------------------------------------------------"""

    def update_pplot_fig(self):
        if self.ligne1 is not None:
            try:
                self.ax1.lines.remove(self.ligne1)
            except ValueError:
                pass
            self.ligne1 = None
        if self.ligne2 is not None:
            try:
                self.ax1.lines.remove(self.ligne2)
            except ValueError:
                pass
            self.ligne2 = None
        self.interact()

    """----------------------------------------------------------------------------------"""

    def disconnect_all(self):
        while len(self.mpl_connect) != 0:
            self.pplot_fig.canvas.mpl_disconnect(self.mpl_connect[0][0])
            del self.mpl_connect[0]

    """----------------------------------------------------------------------------------"""

    def disconnect_name(self, name):
        for i in range(len(self.mpl_connect)):
            if self.mpl_connect[i][1] == name:
                self.pplot_fig.canvas.mpl_disconnect(self.mpl_connect[i][0])
                del self.mpl_connect[i]
                return

    """----------------------------------------------------------------------------------"""

    def connect_all(self):
        self.mpl_connect.append([self.pplot_fig.canvas.mpl_connect('button_press_event', self.on_click),
                                 "button_press_event"])

    """----------------------------------------------------------------------------------"""

    def set_atteractive(self):
        if self.figure.is_interact() == 0:
            return False
        else:
            return True

    """----------------------------------------------------------------------------------"""

    def on_move(self, event):
        self.pos_x = event.xdata
        self.pos_y = event.ydata

        """On retire les lignes si elles sont déjà tracés et execute self.interact"""
        self.update_pplot_fig()

    """----------------------------------------------------------------------------------"""

    def focus_off(self):
        self.interactive = False
        self.index = None
        self.pos_x = None
        self.pos_y = None

        self.disconnect_name("motion_notify_event")

        self.value.set_visible(False)

        if self.freq is not None:
            self.freq.set_visible(False)

        if self.ligne1 is not None:
            try:
                self.ax1.lines.remove(self.ligne1)
            except ValueError:
                pass
            self.ligne1 = None

        if self.ligne2 is not None:
            try:
                self.ax1.lines.remove(self.ligne2)
            except ValueError:
                pass
            self.ligne2 = None

        self.pplot_fig.canvas.draw()

    """----------------------------------------------------------------------------------"""

    def focus_on(self):
        if self.figure.is_interact() == 0:
            return
        else:
            self.interactive = True

        self.mpl_connect.append([self.pplot_fig.canvas.mpl_connect('motion_notify_event', self.on_move),
                                 "motion_notify_event"])

        self.value.set_visible(True)
        if self.freq is not None:
            self.freq.set_visible(True)

        self.interact()

    """----------------------------------------------------------------------------------"""

    def on_close(self, event):
        self.disconnect_all()
        pplot.close(self.pplot_fig)

    """----------------------------------------------------------------------------------"""

    def on_key(self, event):
        pass

    """----------------------------------------------------------------------------------"""

    def on_click(self, event):
        if event.dblclick and event.inaxes is not None and event.button == MouseButton.LEFT and \
                event.inaxes == self.ax1:
            if self.interactive:
                self.focus_off()

            else:
                self.focus_on()
        elif event.dblclick and event.inaxes is not None and event.button == MouseButton.RIGHT and \
                event.inaxes == self.ax1:
            self.delect_point()

    """----------------------------------------------------------------------------------"""

    def delect_point(self):
        if self.res is None:
            print("res is none")
            return

        new_data_x = self.ax1.lines[0].get_xdata()
        new_data_y = self.ax1.lines[0].get_ydata()

        new_data_x = np.delete(new_data_x, self.res)
        new_data_y = np.delete(new_data_y, self.res)

        self.ax1.lines[0].set_xdata(new_data_x)
        self.ax1.lines[0].set_ydata(new_data_y)

        new_data_x = np.array(new_data_x.tolist())
        new_data_y = np.array(new_data_y.tolist())

        self.figure.x_axe.data[0].data = new_data_x
        self.figure.y1_axe.data[0].data = new_data_y
        if self.figure.x_axe.data[0].global_index:
            self.figure.x_axe.data[0].global_index.pop(self.res)

        self.pplot_fig.canvas.draw()

    def reset_color(self):
        pass


class Pic_selection(Abstract_objet_affiche):
    def __init__(self, data, figure):
        super().__init__(data, figure)
        self.ax1 = None
        self.ax2 = None
        self.value = None
        self.freq = None

        self.emit = Emit()

        self.pos_x = None
        self.pos_y = None
        self.ligne1 = None
        self.ligne2 = None

        self.pics = []

        self.can_be_closed = False

        self.coords = [[None, None], [None, None]]

    """----------------------------------------------------------------------------------"""

    def create_figure(self):
        if self.pplot_fig is not None:
            pplot.close(self.pplot_fig)

        if self.figure.is_data_set() == 1:
            self.pplot_fig, self.ax1, self.ax2, self.value, a, b, c = self.data.load_graph(self.figure)
            self.pplot_fig.tight_layout()
        else:
            raise ValueError

    """----------------------------------------------------------------------------------"""

    def interact(self):
        black = matplotlib.colors.to_rgba("black")
        if self.coords[0][0] is not None:
            self.ligne1 = self.ax1.axvline(x=self.coords[0][0], color=black)

        if self.coords[1][0] is not None:
            self.ligne2 = self.ax1.axvline(x=self.coords[1][0], color=black)
        self.pplot_fig.canvas.draw()

    """----------------------------------------------------------------------------------"""

    def update_pplot_fig(self):
        if self.ligne1 is not None:
            try:
                self.ax1.lines.remove(self.ligne1)
            except ValueError:
                pass
            self.ligne1 = None
        if self.ligne2 is not None:
            try:
                self.ax1.lines.remove(self.ligne2)
            except ValueError:
                pass
            self.ligne2 = None
        self.interact()

    """----------------------------------------------------------------------------------"""

    def set_atteractive(self):
        return True

    """----------------------------------------------------------------------------------"""

    def reset_color(self):
        pass

    """----------------------------------------------------------------------------------"""

    def disconnect_all(self):
        while len(self.mpl_connect) != 0:
            self.pplot_fig.canvas.mpl_disconnect(self.mpl_connect[0][0])
            del self.mpl_connect[0]

    """----------------------------------------------------------------------------------"""

    def connect_all(self):
        self.mpl_connect.append([self.pplot_fig.canvas.mpl_connect('key_press_event', self.on_key), 'key_press_event'])
        if 's' in pplot.rcParams['keymap.save']:
            pplot.rcParams['keymap.save'].remove('s')

        self.mpl_connect.append([self.pplot_fig.canvas.mpl_connect('close_event', self.on_close), 'close_event'])
        self.mpl_connect.append([self.pplot_fig.canvas.mpl_connect('button_press_event', self.on_click),
                                 "button_press_event"])

    """----------------------------------------------------------------------------------"""

    def focus_off(self):
        pass

    """----------------------------------------------------------------------------------"""

    def focus_on(self):
        pass

    """----------------------------------------------------------------------------------"""

    def on_click(self, event):
        if event.dblclick and event.inaxes is not None and event.button == MouseButton.LEFT and \
                (event.inaxes == self.ax1 or event.inaxes == self.ax2):
            if self.coords[0][0] is None:
                self.coords[0] = [event.xdata, event.ydata]
            elif self.coords[1][0] is None:
                self.coords[1] = [event.xdata, event.ydata]
            else:
                self.coords[0] = [event.xdata, event.ydata]
                self.coords[1] = [None, None]
            self.update_pplot_fig()

    """----------------------------------------------------------------------------------"""

    def on_close(self, event):
        self.disconnect_all()
        pplot.close(self.pplot_fig)

    """----------------------------------------------------------------------------------"""

    def on_key(self, event):
        if event.key == "s":
            if self.coords[0][0] is not None and self.coords[1][0] is not None:
                try:
                    self.calc()
                except ValueError:
                    self.emit.emit("msg_console", type="msg_console", str="Invalid landmarks", foreground_color="red")
                else:
                    self.emit.emit("msg_console", type="msg_console", str="Landmarks saved", foreground_color="green")
            else:
                if self.coords[0][0] is None or self.coords[1][0] is None:
                    self.emit.emit("msg_console", type="msg_console", str="there should be two landmarks",
                                   foreground_color="red")
                else:
                    self.emit.emit("msg_console", type="msg_console", str="Invalid landmarks", foreground_color="red")
        elif event.key == "r":
            self.pics = []
            self.emit.emit("msg_console", type="msg_console", str="the selection of peaks has been deleted",
                           foreground_color="red")

    """----------------------------------------------------------------------------------"""

    def disconnect_name(self, name):
        for i in range(len(self.mpl_connect)):
            if self.mpl_connect[i][1] == name:
                self.pplot_fig.canvas.mpl_disconnect(self.mpl_connect[i][0])
                del self.mpl_connect[i]
                return
        raise ValueError

    """----------------------------------------------------------------------------------"""

    def calc(self):
        data_x = self.figure.x_axe.data[0].data
        data_y = self.figure.y1_axe.data[0].data

        if self.coords[0][0] > self.coords[1][0]:
            temp = self.coords[1][0]
            self.coords[1][0] = self.coords[0][0]
            self.coords[0][0] = temp

        index = 0
        while data_x[index] < self.coords[0][0]:
            index += 1

        born_y_min = data_y[index]

        index_min = index

        val_max = data_y[index]
        index_val_max = index
        while data_x[index] < self.coords[1][0]:
            """calcule de x ou y est max"""
            if data_y[index] > val_max:
                val_max = data_y[index]
                index_val_max = index
            index += 1

        x_max = data_x[index_val_max]

        born_y_max = data_y[index]

        index_max = index

        calc = 0
        for j in range(index_min + 1, index_max + 1):
            calc += ((abs(data_x[j]) - abs(data_x[j - 1])) * data_y[j - 1] +
                     (data_y[j] - data_y[j - 1]) * (data_x[j] - data_x[j - 1]) / 2)

        area = calc

        y_milieux_gauche = (val_max - born_y_min) / 2 + born_y_min
        y_milieux_droit = (val_max - born_y_max) / 2 + born_y_max

        print(data_y)
        print(y_milieux_gauche)
        print(y_milieux_droit)

        temp_xright = None
        temp_xleft = None

        for j in range(index_min + 1, index_max + 1):
            if data_y[j] > y_milieux_gauche:
                vecteur = (data_x[j] - data_x[j - 1]) / (data_y[j] - data_y[j - 1])
                temp_xleft = (data_y[j] - y_milieux_gauche) * vecteur + data_x[j - 1]
                break

        for j in reversed(range(index_min + 1, index_max + 1)):
            if data_y[j] > y_milieux_droit:
                vecteur = (data_x[j - 1] - data_x[j]) / (data_y[j] - data_y[j - 1])
                temp_xright = (data_y[j] - y_milieux_droit) * vecteur + data_x[j - 1]
                break

        if temp_xright is None or temp_xleft is None:
            largeur = 0.04
        else:
            largeur = temp_xright - temp_xleft

        pic = {'amplitude': area,
               'fwhm': largeur,
               'center': x_max,
               'left_base': data_x[index_min],
               'right_base': data_x[index_max]}

        self.pics.append(pic)


class Gitt_affiche(Abstract_objet_affiche):
    def __init__(self, data, figure):
        super().__init__(data, figure)
        self.ax1 = None
        self.ax2 = None
        self.value = None
        self.freq = None

        self.emit = Emit()

        self.pos_x = None
        self.pos_y = None
        self.ligne1 = None
        self.ligne2 = None
        self.ligne3 = None

        self.editable = False

        self.coords = [[None, None], [None, None], [None, None]]

    """----------------------------------------------------------------------------------"""

    def create_figure(self):
        if self.pplot_fig is not None:
            return True

        if self.figure.is_data_set() == 1:
            self.pplot_fig, self.ax1, self.ax2, self.value, self.freq, a, b = self.data.load_graph(self.figure)
            self.pplot_fig.tight_layout()
        else:
            raise ValueError

    """----------------------------------------------------------------------------------"""

    def interact(self):
        black = matplotlib.colors.to_rgba("black")
        if self.coords[0][0] is not None:
            self.ligne1 = self.ax1.axvline(x=self.coords[0][0], color=black)

        if self.coords[1][0] is not None:
            self.ligne2 = self.ax1.axvline(x=self.coords[1][0], color=black)

        if self.coords[2][0] is not None:
            self.ligne3 = self.ax1.plot(self.coords[2][0], self.coords[2][1], color=black)

        self.pplot_fig.canvas.draw()

    """----------------------------------------------------------------------------------"""

    def update_pplot_fig(self):
        if self.ligne1 is not None:
            try:
                self.ax1.lines.remove(self.ligne1)
            except ValueError:
                pass
            self.ligne1 = None
        if self.ligne2 is not None:
            try:
                self.ax1.lines.remove(self.ligne2)
            except ValueError:
                pass
            self.ligne2 = None
        # ce n'est pas une ligne infinie
        if self.ligne3 is not None and len(self.ligne3) > 0:
            line3 = self.ligne3.pop(0)
            line3.remove()
        self.interact()

    """----------------------------------------------------------------------------------"""

    def set_atteractive(self):
        return True

    """----------------------------------------------------------------------------------"""

    def reset_color(self):
        pass

    """----------------------------------------------------------------------------------"""

    def disconnect_all(self):
        while len(self.mpl_connect) != 0:
            self.pplot_fig.canvas.mpl_disconnect(self.mpl_connect[0][0])
            del self.mpl_connect[0]

    """----------------------------------------------------------------------------------"""

    def connect_all(self):
        self.mpl_connect.append([self.pplot_fig.canvas.mpl_connect('key_press_event', self.on_key), 'key_press_event'])
        self.mpl_connect.append([self.pplot_fig.canvas.mpl_connect('button_press_event', self.on_click),
                                 "button_press_event"])
        if 's' in pplot.rcParams['keymap.save']:
            pplot.rcParams['keymap.save'].remove('s')

    """----------------------------------------------------------------------------------"""

    def focus_off(self):
        """On remet la touche s, oupas, a regarder comment faire"""
        self.coords = [[None, None], [None, None], [None, None]]
        self.disconnect_all()
        self.pplot_fig.canvas.draw()

    """----------------------------------------------------------------------------------"""

    def focus_on(self):
        pass

    """----------------------------------------------------------------------------------"""

    def on_click(self, event):
        if event.dblclick and event.inaxes is not None and event.button == MouseButton.LEFT and \
                (event.inaxes == self.ax1 or event.inaxes == self.ax2):
            if self.coords[0][0] is None:
                self.coords[0] = [event.xdata, event.ydata]
            elif self.coords[1][0] is None:
                self.coords[1] = [event.xdata, event.ydata]
            else:
                self.coords[0] = [event.xdata, event.ydata]
                self.coords[1] = [None, None]
        else:
            return

        if self.coords[0][0] is not None and self.coords[1][0] is not None:
            res = Resources.coord_to_point(self.coords, self.figure.x_axe.data[0], self.figure.y1_axe.data[0])
            if res == -1:
                self.emit.emit("msg_console", type="msg_console", str="Invalid mark",
                               foreground_color="red")
                return

            if res[0] > res[1]:
                temp = res[0]
                res[0] = res[1]
                res[1] = temp

            result = linregress(self.figure.x_axe.data[0].data[res[0]:res[1]],
                                self.figure.y1_axe.data[0].data[res[0]:res[1]])

            self.emit.emit("msg_console", type="msg_console", str="\nBorne 1 : " + str(self.coords[0][0]),
                           foreground_color="black")
            self.emit.emit("msg_console", type="msg_console", str="Borne 2 : " + str(self.coords[1][0]),
                           foreground_color="black")
            self.emit.emit("msg_console", type="msg_console", str="Slope : " + str(result.slope) + "\n",
                           foreground_color="black")

            array_slop_x = self.figure.x_axe.data[0].data[res[0]:res[1]]
            array_slop_y = []
            for j in range(len(array_slop_x)):
                array_slop_y.append(array_slop_x[j] * result.slope + result.intercept)
            self.coords[2][0] = array_slop_x
            self.coords[2][1] = array_slop_y

        else:
            self.coords[2][0] = None
            self.coords[2][1] = None

        self.update_pplot_fig()

    """----------------------------------------------------------------------------------"""

    def on_close(self, event):
        self.disconnect_all()
        pplot.close(self.pplot_fig)

    """----------------------------------------------------------------------------------"""

    def on_key(self, event):
        if event.key == "s" and self.coords[2][0] is not None and self.coords[2][1] is not None:
            self.call_back_func()
        else:
            if self.coords[0][0] is None or self.coords[1][0] is None:
                self.emit.emit("msg_console", type="msg_console", str="Impossible to save the marks, they must be 2",
                               foreground_color="red")
            else:
                self.emit.emit("msg_console", type="msg_console", str="Invalid mark",
                               foreground_color="red")

    """----------------------------------------------------------------------------------"""

    def disconnect_name(self, name):
        for i in range(len(self.mpl_connect)):
            if self.mpl_connect[i][1] == name:
                self.pplot_fig.canvas.mpl_disconnect(self.mpl_connect[i][0])
                del self.mpl_connect[i]
                return

    """----------------------------------------------------------------------------------"""


class Impedance_affiche(Abstract_objet_affiche):
    def __init__(self, data, figure):
        super().__init__(data, figure)

        self.res = []
        self.ax1 = None
        self.ax2 = None
        self.value = None
        self.freq = None
        self.leg2 = None
        self.leg1 = None

        self.index = None
        self.ligne1 = None
        self.ligne2 = None

        self.lines = []
        self.val_freq = []
        self.to_draw = []

        self.pos_x = None
        self.pos_y = None

        self.can_emit = True

    """----------------------------------------------------------------------------------"""

    def create_figure(self):
        if self.pplot_fig is not None:
            pplot.close(self.pplot_fig)

        if self.figure.is_data_set() == 1:
            self.pplot_fig, self.ax1, self.ax2, self.value, self.freq, self.leg1, self.leg2 \
                = self.data.load_graph(self.figure)
        else:
            raise ValueError

        self.pplot_fig.tight_layout()

    """----------------------------------------------------------------------------------"""

    def interact(self):
        black = matplotlib.colors.to_rgba("black")
        test = matplotlib.patches.Circle((0.0, 0.0), 0, color='white')

        if self.pos_x is not None:
            if self.index is None:
                index_x, index_y = Resources.index_array(self.figure, [self.pos_x, self.pos_y], self.ax1, self.ax2)

                self.index = [index_x, index_y]

            if self.index[0] != -1:
                xtickslocs = str(self.ax1.get_xticks()[1])
                ytickslocs = str(self.ax1.get_yticks()[1])

                len_x = 4
                find = False
                for i in range(len(xtickslocs)):
                    if xtickslocs[i] == ".":
                        find = True
                    if xtickslocs[i] != "0" and find:
                        len_x = + i + 4 + xtickslocs.find(".")
                        break
                len_y = 4
                find = False
                for i in range(len(ytickslocs)):
                    if ytickslocs[i] == ".":
                        find = True
                    if ytickslocs[i] != "0" and find:
                        len_y = i + 4 + ytickslocs.find(".")
                        break

                res = Resources.coord_to_point([[self.pos_x, self.pos_y]],
                                               self.figure.x_axe.data[self.index[0][1]],
                                               self.figure.y1_axe.data[self.index[1][1]])

                if res != -1:
                    text_legend_pointed = self.figure.y1_axe.data[self.index[1][1]].legend

                    self.value.legend([test, test, test], [
                        'courbe : ' + str(text_legend_pointed),
                        'x : ' + str(self.figure.x_axe.data[self.index[0][1]].data[res])[0:len_x],
                        'y : ' + str(self.figure.y1_axe.data[self.index[1][1]].data[res])[0:len_y]],
                                      markerscale=0, borderaxespad=0, fontsize=14, loc="center right")

                    self.ligne1 = self.ax1.axhline(y=self.figure.y1_axe.data[self.index[1][1]].data[res], color=black)
                    self.ligne2 = self.ax1.axvline(x=self.figure.x_axe.data[self.index[0][1]].data[res], color=black)

                    if self.freq is not None:
                        self.freq.legend([test], [
                            'freq : ' + str(self.data.data.get("freq/Hz")[res])[0:len_x] + " Hz"],
                                         markerscale=0, borderaxespad=0, fontsize=14, loc="lower right")

                else:
                    text_legend_pointed = self.figure.y1_axe.data[self.index[1][1]].legend
                    self.value.legend([test, test, test], ['courbe : ' + str(text_legend_pointed),
                                                           'x : none', 'y : none'],
                                      markerscale=0, borderaxespad=0, fontsize=14, loc="center right")

                    if self.freq is not None:
                        self.freq.legend([test], ['freq : none'],
                                         markerscale=0, borderaxespad=0, fontsize=14, loc="lower right")
            else:
                text_legend_pointed = self.figure.y1_axe.data[self.index[1][1]].legend
                self.value.legend([test, test, test], ['courbe : ' + str(text_legend_pointed), 'x : none', 'y : none'],
                                  markerscale=0, borderaxespad=0, fontsize=14, loc="center right")
                if self.freq is not None:
                    self.freq.legend([test], ['freq : none'],
                                     markerscale=0, borderaxespad=0, fontsize=14, loc="lower right")

            self.pplot_fig.canvas.draw()

    """----------------------------------------------------------------------------------"""

    def update_pplot_fig(self):
        for i in range(len(self.to_draw)):
            line = self.ax1.axvline(x=self.to_draw[i], color=matplotlib.colors.to_rgba("red"))

            # line = self.ax1.plot(self.to_draw[i][0], self.to_draw[i][1], color=self.to_draw[i][2])
            self.lines.append(line)
            self.to_draw = []

        if self.ligne1 is not None:
            try:
                self.ax1.lines.remove(self.ligne1)
            except ValueError:
                pass
            self.ligne1 = None
        if self.ligne2 is not None:
            try:
                self.ax1.lines.remove(self.ligne2)
            except ValueError:
                pass
            self.ligne2 = None
        if self.pos_x is None:
            self.pplot_fig.canvas.draw()
        else:
            self.interact()

    """----------------------------------------------------------------------------------"""

    def set_atteractive(self):
        return True

    """----------------------------------------------------------------------------------"""

    def reset_color(self):
        pass

    """----------------------------------------------------------------------------------"""

    def disconnect_all(self):
        while len(self.mpl_connect) != 0:
            self.pplot_fig.canvas.mpl_disconnect(self.mpl_connect[0][0])
            del self.mpl_connect[0]

    """----------------------------------------------------------------------------------"""

    def connect_all(self):
        self.mpl_connect.append([self.pplot_fig.canvas.mpl_connect('key_press_event', self.on_key), "key_press_event"])
        self.mpl_connect.append([self.pplot_fig.canvas.mpl_connect('button_press_event', self.on_click),
                                 "button_press_event"])
        self.mpl_connect.append([self.pplot_fig.canvas.mpl_connect('close_event', self.on_close), "close_event"])

        if 's' in pplot.rcParams['keymap.save']:
            pplot.rcParams['keymap.save'].remove('s')

    """----------------------------------------------------------------------------------"""

    def focus_off(self):
        self.interactive = False
        self.index = None
        self.pos_x = None
        self.pos_y = None

        self.disconnect_name("motion_notify_event")

        if self.value is not None:
            self.value.set_visible(False)

        if self.freq is not None:
            self.freq.set_visible(False)

        if self.ligne1 is not None:
            try:
                self.ax1.lines.remove(self.ligne1)
            except ValueError:
                pass
            self.ligne1 = None

        if self.ligne2 is not None:
            try:
                self.ax1.lines.remove(self.ligne2)
            except ValueError:
                pass
            self.ligne2 = None

        self.pplot_fig.canvas.draw()

    """----------------------------------------------------------------------------------"""

    def focus_on(self):
        self.mpl_connect.append([self.pplot_fig.canvas.mpl_connect('motion_notify_event', self.on_move),
                                 "motion_notify_event"])

        self.value.set_visible(True)
        self.freq.set_visible(True)
        if 's' in pplot.rcParams['keymap.save']:
            pplot.rcParams['keymap.save'].remove('s')
        if 'r' in pplot.rcParams['keymap.save']:
            pplot.rcParams['keymap.save'].remove('r')

    """----------------------------------------------------------------------------------"""

    def on_click(self, event):
        if event.button is MouseButton.LEFT and event.dblclick and self.interactive:
            self.focus_off()
            self.interactive = False
        elif event.button is MouseButton.LEFT and event.dblclick and not self.interactive:
            self.focus_on()
            self.interactive = True

        elif event.button is MouseButton.RIGHT and event.dblclick:
            res = Resources.coord_to_point([[self.pos_x, self.pos_y]],
                                           self.figure.x_axe.data[self.index[0][1]],
                                           self.figure.y1_axe.data[self.index[1][1]])
            if res != -1:
                self.to_draw.append(self.figure.x_axe.data[0].data[res])

                self.val_freq.append(self.data.data.get("freq/Hz")[res])
                self.update_pplot_fig()

    """----------------------------------------------------------------------------------"""

    def on_close(self, event):
        pass

    """----------------------------------------------------------------------------------"""

    def on_key(self, event):
        if event.key == "s":
            if len(self.val_freq) > 0:
                self.call_back_func()
            else:
                self.emit.emit("msg_console", type="msg_console", str="No frequency placed",
                               foreground_color="red")
        elif event.key == "r":
            for i in range(len(self.lines)):
                self.ax1.lines.remove(self.lines[i])

            self.lines = []
            self.val_freq = []
            self.update_pplot_fig()

    """----------------------------------------------------------------------------------"""

    def disconnect_name(self, name):
        for i in range(len(self.mpl_connect)):
            if self.mpl_connect[i][1] == name:
                self.pplot_fig.canvas.mpl_disconnect(self.mpl_connect[i][0])
                del self.mpl_connect[i]
                break

    """----------------------------------------------------------------------------------"""

    def on_move(self, event):
        if self.interactive:
            self.pos_x = event.xdata
            self.pos_y = event.ydata

            # On retire les lignes si elles sont déjà tracés et execute self.interact
            self.update_pplot_fig()


"""----------------------------------------------------------------------------------"""


class Time_Selection(Abstract_objet_affiche):
    def __init__(self, data, figure):
        super().__init__(data, figure)
        self.ax1 = None
        self.ax2 = None
        self.value = None
        self.freq = None

        self.emit = Emit()

        self.pos_x = None
        self.pos_y = None
        self.ligne1 = None
        self.ligne2 = None

        self.editable = False

        self.coords = [[None, None], [None, None]]

    """----------------------------------------------------------------------------------"""

    def create_figure(self):
        if self.pplot_fig is not None:
            pplot.close(self.pplot_fig)

        if self.figure.is_data_set() == 1:
            self.pplot_fig, self.ax1, self.ax2, self.value, a, b, c = self.data.load_graph(self.figure)
            self.pplot_fig.tight_layout()
        else:
            raise ValueError

    """----------------------------------------------------------------------------------"""

    def interact(self):
        black = matplotlib.colors.to_rgba("black")
        if self.coords[0][0] is not None:
            self.ligne1 = self.ax1.axvline(x=self.coords[0][0], color=black)

        if self.coords[1][0] is not None:
            self.ligne2 = self.ax1.axvline(x=self.coords[1][0], color=black)

        self.pplot_fig.canvas.draw()

    """----------------------------------------------------------------------------------"""

    def update_pplot_fig(self):
        if self.ligne1 is not None:
            try:
                self.ax1.lines.remove(self.ligne1)
            except ValueError:
                pass
            self.ligne1 = None
        if self.ligne2 is not None:
            try:
                self.ax1.lines.remove(self.ligne2)
            except ValueError:
                pass
            self.ligne2 = None

        self.interact()

    """----------------------------------------------------------------------------------"""

    def set_atteractive(self):
        return True

    """----------------------------------------------------------------------------------"""

    def reset_color(self):
        pass

    """----------------------------------------------------------------------------------"""

    def disconnect_all(self):
        while len(self.mpl_connect) != 0:
            self.pplot_fig.canvas.mpl_disconnect(self.mpl_connect[0][0])
            del self.mpl_connect[0]

    """----------------------------------------------------------------------------------"""

    def connect_all(self):
        self.mpl_connect.append([self.pplot_fig.canvas.mpl_connect('key_press_event', self.on_key), 'key_press_event'])
        self.mpl_connect.append([self.pplot_fig.canvas.mpl_connect('button_press_event', self.on_click),
                                 "button_press_event"])
        if 's' in pplot.rcParams['keymap.save']:
            pplot.rcParams['keymap.save'].remove('s')

    """----------------------------------------------------------------------------------"""

    def focus_off(self):
        """On remet la touche s, oupas, a regarder comment faire"""
        self.coords = [[None, None], [None, None], [None, None]]
        self.disconnect_all()
        self.pplot_fig.canvas.draw()

    """----------------------------------------------------------------------------------"""

    def focus_on(self):
        pass

    """----------------------------------------------------------------------------------"""

    def on_click(self, event):
        if event.dblclick and event.inaxes is not None and event.button == MouseButton.LEFT and \
                (event.inaxes == self.ax1 or event.inaxes == self.ax2):
            if self.coords[0][0] is None:
                self.coords[0] = [event.xdata, event.ydata]
            elif self.coords[1][0] is None:
                self.coords[1] = [event.xdata, event.ydata]
            else:
                self.coords[0] = [event.xdata, event.ydata]
                self.coords[1] = [None, None]
        else:
            return

        if self.coords[0][0] is not None and self.coords[1][0] is not None:
            try:
                res = Resources.coord_to_point(self.coords, self.figure.x_axe.data[0], self.figure.y1_axe.data[0])
            except TypeError:
                res = -1

            if res == -1:
                self.emit.emit("msg_console", type="msg_console", str="Invalid mark",
                               foreground_color="red")
                return

        self.update_pplot_fig()

    """----------------------------------------------------------------------------------"""

    def on_close(self, event):
        self.disconnect_all()
        pplot.close(self.pplot_fig)

    """----------------------------------------------------------------------------------"""

    def on_key(self, event):
        if event.key == "s" and self.coords[0][0] is not None:
            self.call_back_func()
        else:
            self.emit.emit("msg_console", type="msg_console", str="You have to place at least one mark",
                           foreground_color="red")

    """----------------------------------------------------------------------------------"""

    def disconnect_name(self, name):
        for i in range(len(self.mpl_connect)):
            if self.mpl_connect[i][1] == name:
                self.pplot_fig.canvas.mpl_disconnect(self.mpl_connect[i][0])
                del self.mpl_connect[i]
                return

    """----------------------------------------------------------------------------------"""


class Saxs_selection(Abstract_objet_affiche):
    """
    type: sub ou norm, en fonction on return soit l'index de la courbe dans le cas de sub
    ou [index_courbe, index]


    """
    def __init__(self, data, figure, _type):
        super().__init__(data, figure)

        self.freq = None
        self.leg = None
        self.value = None
        self.index = None
        self.ax1 = None
        self.ax2 = None

        self.pos_x = None
        self.pos_y = None

        self.ligne1 = None
        self.ligne2 = None
        self.ligne3 = None
        self.ligne4 = None

        self.selection = None
        self.type = _type

        self.res = None

    """----------------------------------------------------------------------------------"""

    def create_figure(self):
        if self.pplot_fig is not None:
            pplot.close(self.pplot_fig)

        if self.figure.is_data_set() == 1:
            self.pplot_fig, self.ax1, self.ax2, self.value, self.freq, self.leg, a = \
                self.data.load_graph(self.figure)
        else:
            raise ValueError

        self.pplot_fig.tight_layout()

    """----------------------------------------------------------------------------------"""

    def interact(self):
        black = matplotlib.colors.to_rgba("black")
        test = matplotlib.patches.Circle((0.0, 0.0), 0, color='white')

        if self.pos_x is not None:
            if self.index is None:
                index_x, index_y = Resources.index_array(self.figure, [self.pos_x, self.pos_y], self.ax1, self.ax2)
                self.index = [index_x, index_y]
                count = 0
                for ax in self.pplot_fig.axes:
                    for line in ax.lines:
                        if "#" in line.get_color():
                            if count != self.index[0][1]:
                                color = line.get_color()
                                color = str(color)
                                color += "50"
                                line.set_color(color)
                        elif len(line.get_color()) == 4:
                            if count != self.index[0][1]:
                                hex_color = matplotlib.colors.to_hex(line.get_color())
                                color = str(hex_color)
                                color += "50"
                                line.set_color(color)
                        count += 1

            if self.index[0] != -1:
                xtickslocs = str(self.ax1.get_xticks()[1])
                ytickslocs = str(self.ax1.get_yticks()[1])

                len_x = 4
                find = False
                for i in range(len(xtickslocs)):
                    if xtickslocs[i] == ".":
                        find = True
                    if xtickslocs[i] != "0" and find:
                        len_x = + i + 4 + xtickslocs.find(".")
                        break
                len_y = 4
                find = False
                for i in range(len(ytickslocs)):
                    if ytickslocs[i] == ".":
                        find = True
                    if ytickslocs[i] != "0" and find:
                        len_y = i + 4 + ytickslocs.find(".")
                        break

                res = Resources.coord_to_point([[self.pos_x, self.pos_y]],
                                               self.figure.x_axe.data[self.index[0][1]],
                                               self.figure.y1_axe.data[self.index[1][1]])
                if res != -1:
                    text_legend_pointed = self.figure.y1_axe.data[self.index[1][1]].legend

                    self.value.legend([test, test, test], [
                        'courbe : ' + str(text_legend_pointed),
                        'x : ' + str(self.figure.x_axe.data[self.index[0][1]].data[res])[0:len_x],
                        'y : ' + str(self.figure.y1_axe.data[self.index[1][1]].data[res])[0:len_y]],
                                      markerscale=0, borderaxespad=0, fontsize=14, loc="center right")

                    self.ligne1 = self.ax1.axhline(y=self.figure.y1_axe.data[self.index[1][1]].data[res], color=black)
                    self.ligne2 = self.ax1.axvline(x=self.figure.x_axe.data[self.index[0][1]].data[res], color=black)

                else:
                    text_legend_pointed = self.figure.y1_axe.data[self.index[1][1]].legend
                    self.value.legend([test, test, test], ['courbe : ' + str(text_legend_pointed),
                                                           'x : none', 'y : none'],
                                      markerscale=0, borderaxespad=0, fontsize=14, loc="center right")

            else:
                text_legend_pointed = self.figure.y1_axe.data[self.index[1][1]].legend
                self.value.legend([test, test, test], ['courbe : ' + str(text_legend_pointed), 'x : none', 'y : none'],
                                  markerscale=0, borderaxespad=0, fontsize=14, loc="center right")

            self.pplot_fig.canvas.draw()

    """----------------------------------------------------------------------------------"""

    def update_pplot_fig(self):
        if self.ligne1 is not None:
            try:
                self.ax1.lines.remove(self.ligne1)
            except ValueError:
                pass
            self.ligne1 = None
        if self.ligne2 is not None:
            try:
                self.ax1.lines.remove(self.ligne2)
            except ValueError:
                pass
            self.ligne2 = None
        self.interact()

    """----------------------------------------------------------------------------------"""

    def set_atteractive(self):
        return True

    """----------------------------------------------------------------------------------"""

    def on_move(self, event):
        self.pos_x = event.xdata
        self.pos_y = event.ydata

        # On retire les lignes si elles sont déjà tracés et execute self.interact
        self.update_pplot_fig()

    """----------------------------------------------------------------------------------"""

    def disconnect_name(self, name):
        for i in range(len(self.mpl_connect)):
            if self.mpl_connect[i][1] == name:
                self.pplot_fig.canvas.mpl_disconnect(self.mpl_connect[i][0])
                del self.mpl_connect[i]
                return

    """----------------------------------------------------------------------------------"""

    def on_click(self, event):
        if event.dblclick and event.inaxes is not None and event.button == MouseButton.LEFT and \
                (event.inaxes == self.ax1 or event.inaxes == self.ax2):
            if self.interactive:
                self.focus_off()
            else:
                self.focus_on()
        elif event.dblclick and event.inaxes is not None and event.button == MouseButton.RIGHT and \
                (event.inaxes == self.ax1 or event.inaxes == self.ax2):

            if self.interactive is False:
                return

            res = Resources.coord_to_point([[self.pos_x, self.pos_y]],
                                           self.figure.x_axe.data[self.index[0][1]],
                                           self.figure.y1_axe.data[self.index[1][1]])

            if res == -1:
                self.emit.emit("msg_console", type="msg_console", str="Invalid position", foreground_color="red")
            else:
                if self.ligne3 is not None:
                    try:
                        self.ax1.lines.remove(self.ligne3)
                    except ValueError:
                        pass
                    self.ligne3 = None
                if self.ligne4 is not None:
                    try:
                        self.ax1.lines.remove(self.ligne4)
                    except ValueError:
                        pass
                    self.ligne4 = None

                red = matplotlib.colors.to_rgba("red")

                self.ligne3 = self.ax1.axhline(y=self.figure.y1_axe.data[self.index[1][1]].data[res], color=red)
                self.ligne4 = self.ax1.axvline(x=self.figure.x_axe.data[self.index[0][1]].data[res], color=red)

                if self.type == "sub":
                    self.selection = self.index[1][1]
                elif self.type == "norm":
                    self.selection = [self.index[1][1], self.figure.y1_axe.data[self.index[1][1]].data[res]]

                self.pplot_fig.canvas.draw()

    """----------------------------------------------------------------------------------"""

    def on_close(self, event):
        pass

    """----------------------------------------------------------------------------------"""

    def disconnect_all(self):
        while len(self.mpl_connect) != 0:
            self.pplot_fig.canvas.mpl_disconnect(self.mpl_connect[0][0])
            del self.mpl_connect[0]

    """----------------------------------------------------------------------------------"""

    def connect_all(self):
        self.mpl_connect.append([self.pplot_fig.canvas.mpl_connect('key_press_event', self.on_key), 'key_press_event'])
        self.mpl_connect.append([self.pplot_fig.canvas.mpl_connect('button_press_event', self.on_click),
                                 "button_press_event"])
        if 's' in pplot.rcParams['keymap.save']:
            pplot.rcParams['keymap.save'].remove('s')

    """----------------------------------------------------------------------------------"""

    def focus_off(self):
        self.interactive = False
        self.index = None
        self.pos_x = None
        self.pos_y = None

        self.disconnect_name("motion_notify_event")

        if self.value is not None:
            self.value.set_visible(False)

        if self.freq is not None:
            self.freq.set_visible(False)

        if self.ligne1 is not None:
            try:
                self.ax1.lines.remove(self.ligne1)
            except ValueError:
                pass
            self.ligne1 = None

        if self.ligne2 is not None:
            try:
                self.ax1.lines.remove(self.ligne2)
            except ValueError:
                pass
            self.ligne2 = None

        self.reset_color()
        self.pplot_fig.canvas.draw()


    """----------------------------------------------------------------------------------"""

    def focus_on(self):
        self.interactive = True

        self.mpl_connect.append([self.pplot_fig.canvas.mpl_connect('motion_notify_event', self.on_move),
                                 "motion_notify_event"])

        self.value.set_visible(True)

        self.interact()

    """----------------------------------------------------------------------------------"""

    def on_key(self, event):
        if event.key == "s":
            if self.selection is None:
                self.emit.emit("msg_console", type="msg_console", str="No mark placed", foreground_color="red")
            else:
                self.call_back_func()


    """----------------------------------------------------------------------------------"""

    def reset_color(self):
        for ax in self.pplot_fig.axes:
            for line in ax.lines:
                if "#" in line.get_color():
                    color = line.get_color()
                    if len(str(color)) == 9:
                        color = str(color)
                        color = color[0:7]
                        line.set_color(color)

        texts = self.leg.get_legend().get_texts()
        for text in texts:
            text.set_c("black")







































class Cv_affiche(Abstract_objet_affiche):
    def __init__(self, data, figure):
        super().__init__(data, figure)
        self.ax1 = None
        self.ax2 = None
        self.value = None
        self.freq = None

        self.pos_x = None
        self.pos_y = None
        self.ligne1 = None
        self.ligne2 = None
        self.ligne3 = None

        self.can_be_closed = False

        self.coords = [[None, None], [None, None], [None, None], [None, None]]
        self.export_area = []

        self.type = self.data.data.get("type_exp")

    """----------------------------------------------------------------------------------"""

    def create_figure(self):
        if self.pplot_fig is not None:
            return True
        else:
            if self.figure.is_data_set() == 1:
                try:
                    self.pplot_fig, self.ax1, self.ax2, self.value, self.freq, a = self.data.load_graph(self.figure)
                except ValueError as err:
                    print(err)
                    self.finish = True
                    return False
            else:
                self.finish = True
                return False
            self.pplot_fig.tight_layout()

    """----------------------------------------------------------------------------------"""

    def interact(self):
        black = matplotlib.colors.to_rgba("black")
        red = matplotlib.colors.to_rgba("red")

        if self.coords[0][0] is not None:
            self.ligne1 = self.ax1.axvline(x=self.coords[0][0], color=black)

        if self.coords[1][0] is not None:
            self.ligne2 = self.ax1.axvline(x=self.coords[1][0], color=black)

        if self.coords[2][0] is not None and self.coords[3][0] is not None:
            slope = (self.coords[3][1] - self.coords[2][1]) / (self.coords[3][0] - self.coords[2][0])
            self.ligne3 = self.ax1.axline((self.coords[2][0], self.coords[2][1]), slope=slope, color=red)

    """----------------------------------------------------------------------------------"""

    def update_pplot_fig(self):
        self.pplot_fig.canvas.draw()
        self.pplot_fig.canvas.flush_events()

        if self.ligne1 is not None:
            try:
                self.ax1.lines.remove(self.ligne1)
            except ValueError:
                pass
            self.ligne1 = None
        if self.ligne2 is not None:
            try:
                self.ax1.lines.remove(self.ligne2)
            except ValueError:
                pass
            self.ligne2 = None
        if self.ligne3 is not None:
            try:
                self.ax1.lines.remove(self.ligne3)
            except ValueError:
                pass
            self.ligne3 = None

    """----------------------------------------------------------------------------------"""

    def set_atteractive(self):
        return True

    """----------------------------------------------------------------------------------"""

    def reset_color(self):
        pass

    """----------------------------------------------------------------------------------"""

    def disconnect_all(self):
        for i in self.mpl_connect:
            self.pplot_fig.canvas.mpl_disconnect(i)

    """----------------------------------------------------------------------------------"""

    def connect_all(self, array):
        self.mpl_connect.append(self.pplot_fig.canvas.mpl_connect('key_press_event', self.on_key))
        for type, func in array:
            if self.pplot_fig is not None:
                self.mpl_connect.append(self.pplot_fig.canvas.mpl_connect(type, func))

    """----------------------------------------------------------------------------------"""

    def focus_off(self):
        """On remet la touche s, oupas, a regarder comment faire"""
        self.coords = [[None, None], [None, None], [None, None], [None, None]]
        self.pplot_fig.canvas.draw()
        self.pplot_fig.canvas.flush_events()

    """----------------------------------------------------------------------------------"""

    def focus_on(self):
        """On supprime la touche s"""
        if 's' in pplot.rcParams['keymap.save']:
            pplot.rcParams['keymap.save'].remove('s')

    """----------------------------------------------------------------------------------"""

    def on_click(self, event, focus):
        if event.button is MouseButton.LEFT and event.dblclick:
            if self.coords[0][0] is None:
                self.coords[0] = [event.xdata, event.ydata]
            elif self.coords[1][0] is None:
                self.coords[1] = [event.xdata, event.ydata]
            else:
                self.coords[0] = [event.xdata, event.ydata]
                self.coords[1] = [None, None]
            self.update_pplot_fig()

        elif event.button is MouseButton.RIGHT and event.dblclick and self.type == "cv_solution":
            if self.coords[2][0] is None:
                self.coords[2] = [event.xdata, event.ydata]
            elif self.coords[3][0] is None:
                self.coords[3] = [event.xdata, event.ydata]
            else:
                self.coords[2] = [event.xdata, event.ydata]
                self.coords[3] = [None, None]
            self.update_pplot_fig()
        else:
            return

        res = None
        if self.coords[0][0] is not None and self.coords[1][0] is not None and self.type == "cv_electrode":
            res = self.traitement_coord_electrode()
        elif self.coords[0][0] is not None and self.coords[1][0] is not None and \
                self.coords[2][0] is not None and self.coords[3][0] is not None and self.type == "cv_solution":
            res = self.traitement_coord_solution()

        """immonde"""
        if res is not None:
            if "cm\u00b2/mol\u208b\u2081" in self.figure.name_axes_y1:
                unite = u"cm\u00b2/mol\u208b\u2081"
            elif "cm\u00b2" in self.figure.name_axes_y1:
                unite = u"cm\u00b2"
            else:
                unite = "g"

            print("\n----------")
            print("Borne 1 = " + str(res[1]))
            print("Borne 2 = " + str(res[2]))
            """Je n'ai plus le nom...."""
            print("x_max = " + str(res[3]))
            print("area = " + str(res[4]) + " C/" + unite)
            print("area = " + str(res[5]) + " mAh/" + unite)
            if str(res[6]) == "None":
                self.resource.print_color("largeur a mi hauteur introuvable", "work")
                print("largeur = " + str(res[6]))
            else:
                print("largeur = " + str(res[6]) + " V")
            if len(res) == 8:
                """pareil, plus le nom, a demander"""
                print("y = " + str(res[7]))

    """----------------------------------------------------------------------------------"""

    def on_close(self, event):
        pass

    """----------------------------------------------------------------------------------"""

    def on_key(self, event):
        if event.key == "s" and event:
            res = None
            if self.coords[0][0] is not None and self.coords[1][0] is not None:
                if self.type == "cv_electrode":
                    res = self.traitement_coord_electrode()
            if self.coords[0][0] is not None and self.coords[1][0] is not None and \
                    self.coords[2][0] is not None and self.coords[3][0] is not None:
                if self.type == "cv_solution":
                    res = self.traitement_coord_solution()
            if res is not None:
                if "cm\u00b2/mol\u208b\u2081" in self.figure.name_axes_y1:
                    unite = "cm2/mol-1"
                elif "cm\u00b2" in self.figure.name_axes_y1:
                    unite = "cm2"
                else:
                    unite = "g"
                if self.type == "cv_electrode":
                    self.export_area.append(["name", "borne1", "borne2", u"EP", "area C/" + unite,
                                             "area mAh/" + unite, "largeur/V"])
                elif self.type == "cv_solution":
                    self.export_area.append(["name", "borne1", "borne2", u"EP", "area C/" + unite,
                                             "area mAh/" + unite, "largeur/V", "y"])

                self.export_area.append(res)
                print("Dernière donnée sauvegardée")

    """----------------------------------------------------------------------------------"""

    @property
    def finish(self):
        return self._finish

    """----------------------------------------------------------------------------------"""

    @finish.setter
    def finish(self, arg):
        if arg is False:
            self._finish = arg
        else:
            if self.can_be_closed is False:
                self.can_be_closed = True
                obj_data = Array_Abstract_objet_affiche()
                obj_data.event_thread2.set()
            else:
                self._finish = True

    """----------------------------------------------------------------------------------"""

    def traitement_coord_electrode(self):
        if self.coords[0][0] is None or self.coords[1][0] is None:
            return
        elif (self.coords[0][1] < 0 and self.coords[1][1] > 0) or (
                self.coords[0][1] > 0 and self.coords[1][1] < 0):
            print("Merci de donner deux valeurs de même signe")
            return

        res = Resources.coord_to_point(self.coords, self.figure.data_x[0], self.figure.data_y1[0])
        if res == -1:
            print("Borne incorrect")
            return

        q0 = self.data.data.get("(Q-Qo)/C")

        for i in range(len(self.figure.norm)):
            if self.figure.norm[i][0] == "y1":
                norm = self.figure.norm[i][1]
                break

        integral = (q0[res[1]] / norm) - (q0[res[0]] / norm)

        y_min = self.figure.data_y1[0].data[0]
        y_max = self.figure.data_y1[0].data[0]
        x_min = 0
        x_max = 0

        for i in range(len(self.figure.data_y1[0].data)):
            if res[0] < i < res[1] and self.figure.data_y1[0].data[i] < y_min:
                y_min = self.figure.data_y1[0].data[i]
                x_min = self.figure.data_x[0].data[i]
            if res[0] < i < res[1] and self.figure.data_y1[0].data[i] > y_max:
                y_max = self.figure.data_y1[0].data[i]
                x_max = self.figure.data_x[0].data[i]

        if abs(y_min) > abs(y_max):
            x_max = abs(x_min)
            val_max = y_min
        else:
            x_max = abs(x_max)
            val_max = y_max

        y_milieux_gauche = (val_max - self.figure.data_y1[0].data[res[0]]) / 2 + self.figure.data_y1[0].data[res[0]]
        y_milieux_droit = (val_max - self.figure.data_y1[0].data[res[1]]) / 2 + self.figure.data_y1[0].data[res[1]]

        for j in range(res[0] + 1, res[1]):
            if abs(self.figure.data_y1[0].data[j]) > abs(y_milieux_gauche):
                temp_xleft = self.figure.data_x[0].data[j]
                temp_yleft = self.figure.data_y1[0].data[j]
                break

        for j in reversed(range(res[0] + 1, res[1])):
            if abs(self.figure.data_y1[0].data[j]) > abs(y_milieux_droit):
                temp_xright = self.figure.data_x[0].data[j]
                temp_yright = self.figure.data_y1[0].data[j]
                break
        try:
            longueur = math.sqrt((temp_xright - temp_xleft) ** 2 + (temp_yright - temp_yleft) ** 2)

            array_return = [self.data.name + "_" + self.figure.name[5:], self.figure.data_x[0].data[res[0]],
                            self.figure.data_x[0].data[res[1]], x_max, integral, integral / 3.6, longueur]
        except UnboundLocalError:
            array_return = [self.data.name + "_" + self.figure.name[5:], self.figure.data_x[0].data[res[0]],
                            self.figure.data_x[0].data[res[1]], x_max, integral, integral / 3.6, "None"]

        return array_return

    """----------------------------------------------------------------------------------"""

    def traitement_coord_solution(self):
        if (self.coords[0][1] < 0 and self.coords[1][1] > 0) or (
                self.coords[0][1] > 0 and self.coords[1][1] < 0):
            print("Merci de donner deux valeurs de même signe")
            return

        res = Resources.coord_to_point(self.coords, self.figure.data_x[0], self.figure.data_y1[0])
        if res == -1:
            print("Borne incorrect")
            return

        q0 = self.data.data.get("(Q-Qo)/C")

        for i in range(len(self.figure.norm)):
            if self.figure.norm[i][0] == "y1":
                norm = self.figure.norm[i][1]
                break

        integral = (q0[res[1]] / norm) - (q0[res[0]] / norm)

        vecteur = [self.coords[3][0] - self.coords[2][0], self.coords[3][1] - self.coords[2][1]]

        y_min = self.figure.data_y1[0].data[0]
        y_max = self.figure.data_y1[0].data[0]
        x_min = 0
        x_max = 0

        for i in range(len(self.figure.data_y1[0].data)):
            if res[0] < i < res[1] and self.figure.data_y1[0].data[i] < y_min:
                y_min = self.figure.data_y1[0].data[i]
                x_min = self.figure.data_x[0].data[i]
            if res[0] < i < res[1] and self.figure.data_y1[0].data[i] > y_max:
                y_max = self.figure.data_y1[0].data[i]
                x_max = self.figure.data_x[0].data[i]

        if abs(y_min) > abs(y_max):
            x_max = abs(x_min)
            val_max = y_min
        else:
            x_max = abs(x_max)
            val_max = y_max

        y_milieux_gauche = (val_max - self.figure.data_y1[0].data[res[0]]) / 2 + self.figure.data_y1[0].data[res[0]]
        y_milieux_droit = (val_max - self.figure.data_y1[0].data[res[1]]) / 2 + self.figure.data_y1[0].data[res[1]]

        for j in range(res[0] + 1, res[1]):
            if abs(self.figure.data_y1[0].data[j]) > abs(y_milieux_gauche):
                temp_xleft = self.figure.data_x[0].data[j]
                temp_yleft = self.figure.data_y1[0].data[j]
                break

        for j in reversed(range(res[0] + 1, res[1])):
            if abs(self.figure.data_y1[0].data[j]) > abs(y_milieux_droit):
                temp_xright = self.figure.data_x[0].data[j]
                temp_yright = self.figure.data_y1[0].data[j]
                break
        """        
        y_milieux_gauche = (val_max - self.figure.data_y1[0].data[res[0]]) / 2 + self.figure.data_y1[0].data[res[0]]
        y_milieux_droit = (val_max - self.figure.data_y1[0].data[res[1]]) / 2 + self.figure.data_y1[0].data[res[1]]

        for j in range(res[0] + 1, res[1]):
            if abs(self.figure.data_y1[0].data[j]) - abs(self.figure.data_y1[0].data[res[0]]) > abs(y_milieux_gauche):
                temp_xleft = abs(self.figure.data_x[0].data[j])
                temp_yleft = abs(self.figure.data_y1[0].data[j])
                break

        for j in reversed(range(res[0] + 1, res[1])):
            if self.figure.data_y1[0].data[j] - self.figure.data_y1[0].data[res[1]] > y_milieux_droit:
                temp_xright = self.figure.data_x[0].data[j]
                temp_yright = self.figure.data_y1[0].data[j]
                break

        """
        try:
            longueur = math.sqrt((temp_xright - temp_xleft) ** 2 + (temp_yright - temp_yleft) ** 2)

        except UnboundLocalError:
            longueur = "None"

        """essaie calcul de la hauteur entre sommet et la courbe rouge"""
        y = (vecteur[1] / vecteur[0]) * x_max + (self.coords[2][1] - (vecteur[1] / vecteur[0]) * self.coords[2][0])

        if abs(y_min) > abs(y_max):
            y_max = y_min

        array_return = [self.data.name + "_" + self.figure.name[5:], self.figure.data_x[0].data[res[0]],
                        self.figure.data_x[0].data[res[1]], x_max, abs(integral), abs(integral) / 3.6, longueur,
                        y_max - y]

        return array_return

    """----------------------------------------------------------------------------------"""


class Diffraction_affiche(Abstract_objet_affiche):
    def __init__(self, data, figure, loop_data):
        super().__init__(data, figure)
        self.loop_data = loop_data

        self.ax1 = None
        self.ax2 = None

        self.pos_x = None
        self.pos_y = None
        self.ligne1 = None
        self.ligne2 = None

        self.figure_res = []
        self.obj_affiche_res = None
        self.res_calc = []

        self.can_be_closed = False

        self.coords = [[None, None], [None, None]]

    """----------------------------------------------------------------------------------"""

    def create_figure(self):
        if self.pplot_fig is None:
            if self.figure.is_data_set() == 1:
                try:
                    self.pplot_fig, self.ax1, self.ax2, a, b, c = self.data.load_graph(self.figure)
                except ValueError as err:
                    self.resource.print_color("Les dimensions de la figure " + self.figure.name +
                                              " ne sont pas identiques", "fail")
                    print(err)
                    self.finish = True
                    return False
            else:
                self.resource.print_color("La figure " + self.figure.name + " n'est pas valide", "fail")
                self.finish = True
                return False

            self.pplot_fig.tight_layout()
            return True
        else:
            return False

    """----------------------------------------------------------------------------------"""

    def interact(self):
        black = matplotlib.colors.to_rgba("black")

        add_y = abs(self.ax1.get_yticks()[-1] * 4)
        if self.coords[0][0] is not None:
            self.ligne1 = self.ax1.plot([self.coords[0][0], self.coords[0][0]],
                                        [self.coords[0][1] - add_y, self.coords[0][1] + add_y], color=black)
        if self.coords[1][0] is not None:
            self.ligne2 = self.ax1.plot([self.coords[1][0], self.coords[1][0]],
                                        [self.coords[1][1] - add_y, self.coords[1][1] + add_y], color=black)

    """----------------------------------------------------------------------------------"""

    def update_pplot_fig(self):
        self.pplot_fig.canvas.draw()
        self.pplot_fig.canvas.flush_events()

        if self.ligne1 is not None and len(self.ligne1) > 0:
            line1 = self.ligne1.pop(0)
            line1.remove()
        if self.ligne2 is not None and len(self.ligne2) > 0:
            line2 = self.ligne2.pop(0)
            line2.remove()

    """----------------------------------------------------------------------------------"""

    def set_atteractive(self):
        return True

    """----------------------------------------------------------------------------------"""

    def reset_color(self):
        pass

    """----------------------------------------------------------------------------------"""

    def disconnect_all(self):
        for i in self.mpl_connect:
            self.pplot_fig.canvas.mpl_disconnect(i)

    """----------------------------------------------------------------------------------"""

    def connect_all(self, array):
        self.mpl_connect.append(self.pplot_fig.canvas.mpl_connect('key_press_event', self.on_key))
        for type, func in array:
            if self.pplot_fig is not None:
                self.mpl_connect.append(self.pplot_fig.canvas.mpl_connect(type, func))

    """----------------------------------------------------------------------------------"""

    def focus_off(self):
        """On remet la touche s, oupas, a regarder comment faire"""
        self.coords = [[None, None], [None, None]]
        self.pplot_fig.canvas.draw()
        self.pplot_fig.canvas.flush_events()

    """----------------------------------------------------------------------------------"""

    def focus_on(self):
        """On supprime la touche s"""
        if 's' in pplot.rcParams['keymap.save']:
            pplot.rcParams['keymap.save'].remove('s')

    """----------------------------------------------------------------------------------"""

    def on_click(self, event, focus):
        if event.button is MouseButton.LEFT and event.dblclick:
            if self.coords[0][0] is None:
                self.coords[0] = [event.xdata, event.ydata]
            elif self.coords[1][0] is None:
                self.coords[1] = [event.xdata, event.ydata]
            else:
                self.coords[0] = [event.xdata, event.ydata]
                self.coords[1] = [None, None]
            self.update_pplot_fig()
        else:
            return

        if self.coords[0][0] is not None and self.coords[1][0] is not None:
            try:
                if self.obj_affiche_res is not None:
                    pplot.close(self.obj_affiche_res.pplot_fig)

                x_max, area, largeur = self.calc()
                fig = self.create_figure_res(x_max, area, largeur)
                self.figure_res.append(fig)

                obj = Classique_affiche(self.data, fig)
                self.obj_affiche_res = obj

                array_obj = Array_Abstract_objet_affiche()
                array_obj.append(obj)

            except (IndexError, UnboundLocalError):
                self.resource.print_color("Bornes invalides", "fail")

    """----------------------------------------------------------------------------------"""

    def on_close(self, event):
        pass

    """----------------------------------------------------------------------------------"""

    def on_key(self, event):
        pass

    """----------------------------------------------------------------------------------"""

    def create_graph(self, x_max, area, largeur):
        pass

    """----------------------------------------------------------------------------------"""

    def create_figure_res(self, x_max, area, largeur):

        f1 = Figure("Diffraction_res_" + str(self.coords[0][0])[0:6] + "_" + str(self.coords[1][0])[0:6], 1)
        f1.plot_name = "Diffraction_res " + str(self.coords[0][0]) + " " + str(self.coords[1][0])

        size_w = 0
        size_c = 0
        warning_x = []
        for i in range(len(self.loop_data)):
            if self.loop_data[i][2] == "w":
                warning_x.append(self.figure.data_x[i].extra_info)
                size_w += 1

        cooling_x = []
        for i in range(len(self.loop_data)):
            if self.loop_data[i][2] == "c":
                cooling_x.append(self.figure.data_x[i].extra_info)
                size_c += 1

        """x_max"""
        if size_w != 0:
            temp_x = Data_array(warning_x, "Température [°C]", None, "nesaisias")
            temp_y = Data_array(x_max[0:size_w], "diffraction", None, "nesaispas")
            temp_x.extra_info = "warning"
            temp_y.extra_info = "warning"
            f1.add_data_x_Data(temp_x)
            f1.add_data_y1_Data(temp_y)

        if size_c != 0:
            temp_x = Data_array(cooling_x, "Température [°C]", None, "nesaisias")
            temp_y = Data_array(x_max[size_w:], "diffraction", None, "nesaispas")
            temp_x.extra_info = "cooling"
            temp_y.extra_info = "cooling"
            f1.add_data_x_Data(temp_x)
            f1.add_data_y1_Data(temp_y)

        """area"""
        if size_w != 0:
            temp_x = Data_array(warning_x, "Température [°C]", None, "nesaisias")
            temp_y = Data_array(area[0:size_w], "diffraction", None, "nesaispas")
            temp_x.extra_info = "warning"
            temp_y.extra_info = "warning"
            f1.add_data_x_Data(temp_x)
            f1.add_data_y1_Data(temp_y)

        if size_c != 0:
            temp_x = Data_array(cooling_x, "Température [°C]", None, "nesaisias")
            temp_y = Data_array(area[size_w:], "diffraction", None, "nesaispas")
            temp_x.extra_info = "cooling"
            temp_y.extra_info = "cooling"
            f1.add_data_x_Data(temp_x)
            f1.add_data_y1_Data(temp_y)

        """largeur"""
        if size_w != 0:
            temp_x = Data_array(warning_x, "Température [°C]", None, "nesaisias")
            temp_y = Data_array(largeur[0:size_w], "diffraction", None, "nesaispas")
            temp_x.extra_info = "warning"
            temp_y.extra_info = "warning"
            f1.add_data_x_Data(temp_x)
            f1.add_data_y1_Data(temp_y)

        if size_c != 0:
            temp_x = Data_array(cooling_x, "Température [°C]", None, "nesaisias")
            temp_y = Data_array(largeur[size_w:], "diffraction", None, "nesaispas")
            temp_x.extra_info = "cooling"
            temp_y.extra_info = "cooling"
            f1.add_data_x_Data(temp_x)
            f1.add_data_y1_Data(temp_y)

        f1.type = "res_diffraction"
        return f1

    """----------------------------------------------------------------------------------"""

    def calc(self):
        x_max = []
        area = []
        largeur = []

        data_x = []
        data_y = []

        array_res = []

        for i in range(len(self.figure.data_x)):
            data_x.append(self.figure.data_x[i].data)
            data_y.append(self.figure.data_y1[i].data)

        if self.coords[0][0] > self.coords[1][0]:
            temp = self.coords[1][0]
            self.coords[1][0] = self.coords[0][0]
            self.coords[0][0] = temp

        array_res.append(["born1=" + str(self.coords[0][0]) + "\t" + "born2=" + str(self.coords[1][0])])
        array_res.append(["temperature\tx_max\tarea\tlargeur"])

        for i in range(len(data_x)):
            index = 0
            while data_x[i][index] < self.coords[0][0]:
                index += 1

            born_x_min = data_x[i][index]
            born_y_min = data_y[i][index]
            index_min = index

            val_max = data_y[i][index]
            index_val_max = index
            while data_x[i][index] < self.coords[1][0]:
                """calcule de x ou y est max"""
                if data_y[i][index] > val_max:
                    val_max = data_y[i][index]
                    index_val_max = index
                index += 1

            x_max.append(data_x[i][index_val_max])

            born_x_max = data_x[i][index]
            born_y_max = data_y[i][index]
            index_max = index
            calc = 0
            for j in range(index_min + 1, index_max + 1):
                calc += ((abs(data_x[i][j]) - abs(data_x[i][j - 1])) * data_y[i][j - 1] +
                         (data_y[i][j] - data_y[i][j - 1]) * (data_x[i][j] - data_x[i][j - 1]) / 2)

            """soustraction du trapéze"""
            calc -= (born_x_max - born_x_min) * born_y_min + (born_x_max - born_x_min) * (born_y_max - born_y_min) / 2
            area.append(calc)

            y_milieux_gauche = (val_max - born_y_min) / 2 + born_y_min
            y_milieux_droit = (val_max - born_y_max) / 2 + born_y_max

            for j in range(index_min + 1, index_max + 1):
                if data_y[i][j] > y_milieux_gauche:
                    vecteur = (data_x[i][j] - data_x[i][j - 1]) / (data_y[i][j] - data_y[i][j - 1])
                    temp_xleft = (data_y[i][j] - y_milieux_gauche) * vecteur + data_x[i][j - 1]
                    temp_yleft = y_milieux_gauche
                    break

            for j in reversed(range(index_min + 1, index_max + 1)):
                if data_y[i][j] > y_milieux_droit:
                    vecteur = (data_x[i][j - 1] - data_x[i][j]) / (data_y[i][j] - data_y[i][j - 1])
                    temp_xright = (data_y[i][j] - y_milieux_droit) * vecteur + data_x[i][j - 1]
                    temp_yright = y_milieux_droit
                    break

            longueur = math.sqrt((temp_xright - temp_xleft) ** 2 + (temp_yright - temp_yleft) ** 2)
            largeur.append(longueur)

            array_res.append([str(self.figure.data_x[i].extra_info) + "\t" + str(data_x[i][index_val_max]) + "\t" + str(
                calc) + "\t" + str(longueur)])

        self.res_calc.extend(array_res)
        return x_max, area, largeur

    """----------------------------------------------------------------------------------"""

    @property
    def finish(self):
        return self._finish

    """----------------------------------------------------------------------------------"""

    @finish.setter
    def finish(self, arg):
        if arg is False:
            self._finish = arg
        else:
            if self.can_be_closed is False:
                self.can_be_closed = True
                obj_data = Array_Abstract_objet_affiche()
                obj_data.event_thread2.set()
            else:
                self._finish = True

    """----------------------------------------------------------------------------------"""


class Waxs_affiche(Abstract_objet_affiche):
    def __init__(self, data, figure):
        super().__init__(data, figure)

        self.ax1 = None
        self.ax2 = None

        self.pos_x = None
        self.pos_y = None
        self.ligne1 = None
        self.ligne2 = None

        self.figure_res = []
        self.obj_affiche_res = None
        self.res_calc = []

        self.can_be_closed = False

        self.coords = [[None, None], [None, None]]

    """----------------------------------------------------------------------------------"""

    def create_figure(self):
        if self.pplot_fig is None:
            if self.figure.is_data_set() == 1:
                try:
                    self.pplot_fig, self.ax1, self.ax2, a, b, c = self.data.load_graph(self.figure)
                except ValueError as err:
                    self.resource.print_color("Les dimensions de la figure " + self.figure.name +
                                              " ne sont pas identiques", "fail")
                    print(err)
                    self.finish = True
                    return False
            else:
                self.resource.print_color("La figure " + self.figure.name + " n'est pas valide", "fail")
                self.finish = True
                return False

            self.pplot_fig.tight_layout()
            return True
        else:
            return False

    """----------------------------------------------------------------------------------"""

    def interact(self):
        black = matplotlib.colors.to_rgba("black")

        if self.coords[0][0] is not None:
            self.ligne1 = self.ax1.axvline(x=self.coords[0][0], color=black)

        if self.coords[1][0] is not None:
            self.ligne2 = self.ax1.axvline(x=self.coords[1][0], color=black)

    """----------------------------------------------------------------------------------"""

    def update_pplot_fig(self):
        self.pplot_fig.canvas.draw()
        self.pplot_fig.canvas.flush_events()

        if self.ligne1 is not None:
            try:
                self.ax1.lines.remove(self.ligne1)
            except ValueError:
                pass
            self.ligne1 = None
        if self.ligne2 is not None:
            try:
                self.ax1.lines.remove(self.ligne2)
            except ValueError:
                pass
            self.ligne2 = None

    """----------------------------------------------------------------------------------"""

    def set_atteractive(self):
        return True

    """----------------------------------------------------------------------------------"""

    def reset_color(self):
        pass

    """----------------------------------------------------------------------------------"""

    def disconnect_all(self):
        for i in self.mpl_connect:
            self.pplot_fig.canvas.mpl_disconnect(i)

    """----------------------------------------------------------------------------------"""

    def connect_all(self, array):
        self.mpl_connect.append(self.pplot_fig.canvas.mpl_connect('key_press_event', self.on_key))
        for type, func in array:
            if self.pplot_fig is not None:
                self.mpl_connect.append(self.pplot_fig.canvas.mpl_connect(type, func))

    """----------------------------------------------------------------------------------"""

    def focus_off(self):
        """On remet la touche s, oupas, a regarder comment faire"""
        self.coords = [[None, None], [None, None]]
        self.pplot_fig.canvas.draw()
        self.pplot_fig.canvas.flush_events()

    """----------------------------------------------------------------------------------"""

    def focus_on(self):
        """On supprime la touche s"""
        if 's' in pplot.rcParams['keymap.save']:
            pplot.rcParams['keymap.save'].remove('s')

    """----------------------------------------------------------------------------------"""

    def on_click(self, event, focus):
        if event.button is MouseButton.LEFT and event.dblclick:
            if self.coords[0][0] is None:
                self.coords[0] = [event.xdata, event.ydata]
            elif self.coords[1][0] is None:
                self.coords[1] = [event.xdata, event.ydata]
            else:
                self.coords[0] = [event.xdata, event.ydata]
                self.coords[1] = [None, None]
            self.update_pplot_fig()
        else:
            return

        if self.coords[0][0] is not None and self.coords[1][0] is not None:
            try:
                if self.obj_affiche_res is not None:
                    pplot.close(self.obj_affiche_res.pplot_fig)

                x_max, area, largeur = self.calc()

                figure_obj = self.create_figure_res(x_max, area, largeur)

                figure_obj.created_from = self.figure

                self.figure_res.append(figure_obj)

                obj = Classique_affiche(self.data, figure_obj)
                self.obj_affiche_res = obj

                array_obj = Array_Abstract_objet_affiche()
                array_obj.append(obj)

            except (IndexError, UnboundLocalError):
                self.resource.print_color("Bornes invalides", "fail")

    """----------------------------------------------------------------------------------"""

    def on_close(self, event):
        pass

    """----------------------------------------------------------------------------------"""

    def on_key(self, event):
        pass

    """----------------------------------------------------------------------------------"""

    def create_graph(self, x_max, area, largeur):
        pass

    """----------------------------------------------------------------------------------"""

    def create_figure_res(self, x_max, area, largeur):

        f1 = Figure("Waxs_res_" + str(self.coords[0][0])[0:6] + "_" + str(self.coords[1][0])[0:6], 1)
        f1.plot_name = "Waxs res " + str(self.coords[0][0])[0:6] + " " + str(self.coords[1][0])[0:6]

        data_x = []
        for i in range(len(self.figure.data_x)):
            data_x.append(self.figure.data_x[i].extra_info[1])

        if self.figure.data_x[0].extra_info[0] == "scan":
            x_name = "z"
        elif self.figure.data_x[0].extra_info[0] == "frame":
            x_name = "time"

        """x_max"""
        temp_x = Data_array(data_x, x_name, None, "nesaisias")
        temp_y = Data_array(x_max, "x max", None, "nesaispas")
        f1.add_data_x_Data(temp_x)
        f1.add_data_y1_Data(temp_y)

        """area"""
        temp_x = Data_array(data_x, x_name, None, "nesaisias")
        temp_y = Data_array(area, "area", None, "nesaispas")
        f1.add_data_x_Data(temp_x)
        f1.add_data_y1_Data(temp_y)

        """largeur"""
        temp_x = Data_array(data_x, x_name, None, "nesaisias")
        temp_y = Data_array(largeur, "largeur", None, "nesaispas")

        f1.add_data_x_Data(temp_x)
        f1.add_data_y1_Data(temp_y)

        f1.type = "res_waxs"
        return f1

    """----------------------------------------------------------------------------------"""

    def calc(self):
        x_max = []
        area = []
        largeur = []

        data_x = []
        data_y = []

        array_res = []

        for i in range(len(self.figure.data_x)):
            data_x.append(self.figure.data_x[i].data)
            data_y.append(self.figure.data_y1[i].data)

        if self.coords[0][0] > self.coords[1][0]:
            temp = self.coords[1][0]
            self.coords[1][0] = self.coords[0][0]
            self.coords[0][0] = temp

        array_res.append(["born1=" + str(self.coords[0][0]) + "\t" + "born2=" + str(self.coords[1][0])])
        array_res.append(["temperature\tx_max\tarea\tlargeur"])

        for i in range(len(data_x)):
            index = 0
            while data_x[i][index] < self.coords[0][0]:
                index += 1

            born_x_min = data_x[i][index]
            born_y_min = data_y[i][index]
            index_min = index

            val_max = data_y[i][index]
            index_val_max = index
            while data_x[i][index] < self.coords[1][0]:
                """calcule de x ou y est max"""
                if data_y[i][index] > val_max:
                    val_max = data_y[i][index]
                    index_val_max = index
                index += 1

            x_max.append(data_x[i][index_val_max])

            born_x_max = data_x[i][index]
            born_y_max = data_y[i][index]
            index_max = index
            calc = 0

            for j in range(index_min + 1, index_max + 1):
                calc += ((abs(data_x[i][j]) - abs(data_x[i][j - 1])) * data_y[i][j - 1] +
                         (data_y[i][j] - data_y[i][j - 1]) * (data_x[i][j] - data_x[i][j - 1]) / 2)

            """soustraction du trapéze"""
            calc -= (born_x_max - born_x_min) * born_y_min + (born_x_max - born_x_min) * (born_y_max - born_y_min) / 2
            area.append(calc)

            y_milieux_gauche = (val_max - born_y_min) / 2 + born_y_min
            y_milieux_droit = (val_max - born_y_max) / 2 + born_y_max

            for j in range(index_min + 1, index_max + 1):
                if data_y[i][j] > y_milieux_gauche:
                    vecteur = (data_x[i][j] - data_x[i][j - 1]) / (data_y[i][j] - data_y[i][j - 1])
                    temp_xleft = (data_y[i][j] - y_milieux_gauche) * vecteur + data_x[i][j - 1]
                    temp_yleft = y_milieux_gauche
                    break

            for j in reversed(range(index_min + 1, index_max + 1)):
                if data_y[i][j] > y_milieux_droit:
                    vecteur = (data_x[i][j - 1] - data_x[i][j]) / (data_y[i][j] - data_y[i][j - 1])
                    temp_xright = (data_y[i][j] - y_milieux_droit) * vecteur + data_x[i][j - 1]
                    temp_yright = y_milieux_droit
                    break

            longueur = math.sqrt((temp_xright - temp_xleft) ** 2 + (temp_yright - temp_yleft) ** 2)
            largeur.append(longueur)

            array_res.append([str(self.figure.data_x[i].extra_info) + "\t" + str(data_x[i][index_val_max]) + "\t" + str(
                calc) + "\t" + str(longueur)])

        self.res_calc.extend(array_res)
        return x_max, area, largeur

    """----------------------------------------------------------------------------------"""

    @property
    def finish(self):
        return self._finish

    """----------------------------------------------------------------------------------"""

    @finish.setter
    def finish(self, arg):
        if arg is False:
            self._finish = arg
        else:
            if self.can_be_closed is False:
                self.can_be_closed = True
                obj_data = Array_Abstract_objet_affiche()
                obj_data.event_thread2.set()
            else:
                self._finish = True

    """----------------------------------------------------------------------------------"""


class Saxs_affiche(Abstract_objet_affiche):
    def __init__(self, data, figure):
        super().__init__(data, figure)

        self.ax1 = None
        self.ax2 = None

        self.pos_x = None
        self.pos_y = None
        self.ligne1 = None
        self.ligne2 = None

        self.figure_res = []
        self.obj_affiche_res = None
        self.res_calc = []

        self.can_be_closed = False

        self.coords = [[None, None], [None, None]]

    """----------------------------------------------------------------------------------"""

    def create_figure(self):
        if self.pplot_fig is None:
            if self.figure.is_data_set() == 1:
                try:
                    self.pplot_fig, self.ax1, self.ax2, a, b, c = self.data.load_graph(self.figure)
                except ValueError as err:
                    self.resource.print_color("Les dimensions de la figure " + self.figure.name +
                                              " ne sont pas identiques", "fail")
                    print(err)
                    self.finish = True
                    return False
            else:
                self.resource.print_color("La figure " + self.figure.name + " n'est pas valide", "fail")
                self.finish = True
                return False

            self.pplot_fig.tight_layout()
            return True
        else:
            return False

    """----------------------------------------------------------------------------------"""

    def interact(self):
        black = matplotlib.colors.to_rgba("black")

        if self.coords[0][0] is not None:
            self.ligne1 = self.ax1.axvline(x=self.coords[0][0], color=black)

        if self.coords[1][0] is not None:
            self.ligne2 = self.ax1.axvline(x=self.coords[1][0], color=black)

    """----------------------------------------------------------------------------------"""

    def update_pplot_fig(self):
        self.pplot_fig.canvas.draw()
        self.pplot_fig.canvas.flush_events()

        if self.ligne1 is not None:
            try:
                self.ax1.lines.remove(self.ligne1)
            except ValueError:
                pass
            self.ligne1 = None
        if self.ligne2 is not None:
            try:
                self.ax1.lines.remove(self.ligne2)
            except ValueError:
                pass
            self.ligne2 = None

    """----------------------------------------------------------------------------------"""

    def set_atteractive(self):
        return True

    """----------------------------------------------------------------------------------"""

    def reset_color(self):
        pass

    """----------------------------------------------------------------------------------"""

    def disconnect_all(self):
        for i in self.mpl_connect:
            self.pplot_fig.canvas.mpl_disconnect(i)

    """----------------------------------------------------------------------------------"""

    def connect_all(self, array):
        self.mpl_connect.append(self.pplot_fig.canvas.mpl_connect('key_press_event', self.on_key))
        for type, func in array:
            if self.pplot_fig is not None:
                self.mpl_connect.append(self.pplot_fig.canvas.mpl_connect(type, func))

    """----------------------------------------------------------------------------------"""

    def focus_off(self):
        """On remet la touche s, oupas, a regarder comment faire"""
        self.coords = [[None, None], [None, None]]
        self.pplot_fig.canvas.draw()
        self.pplot_fig.canvas.flush_events()

    """----------------------------------------------------------------------------------"""

    def focus_on(self):
        """On supprime la touche s"""
        if 's' in pplot.rcParams['keymap.save']:
            pplot.rcParams['keymap.save'].remove('s')

    """----------------------------------------------------------------------------------"""

    def on_click(self, event, focus):
        if event.button is MouseButton.LEFT and event.dblclick:
            if self.coords[0][0] is None:
                self.coords[0] = [event.xdata, event.ydata]
            elif self.coords[1][0] is None:
                self.coords[1] = [event.xdata, event.ydata]
            else:
                self.coords[0] = [event.xdata, event.ydata]
                self.coords[1] = [None, None]
            self.update_pplot_fig()
        else:
            return

        if self.coords[0][0] is not None and self.coords[1][0] is not None:
            try:
                if self.obj_affiche_res is not None:
                    pplot.close(self.obj_affiche_res.pplot_fig)

                integral_x, integral_y, derive1_x, derive1_y, derive2_x, derive2_y = self.calc()

                figure_obj = self.create_figure_res(integral_x, integral_y, derive1_x, derive1_y, derive2_x, derive2_y)
                figure_obj.created_from = self.figure

                self.figure_res.append(figure_obj)

                obj = Classique_affiche(self.data, figure_obj)
                self.obj_affiche_res = obj

                array_obj = Array_Abstract_objet_affiche()
                array_obj.append(obj)

            except (IndexError, UnboundLocalError):
                self.resource.print_color("Bornes invalides", "fail")

    """----------------------------------------------------------------------------------"""

    def on_close(self, event):
        pass

    """----------------------------------------------------------------------------------"""

    def on_key(self, event):
        pass

    """----------------------------------------------------------------------------------"""

    def create_graph(self, x_max, area, largeur):
        pass

    """----------------------------------------------------------------------------------"""

    def create_figure_res(self, integral_x, integral_y, derive1_x, derive1_y, derive2_x, derive2_y):

        f1 = Figure("Saxs_res_" + str(self.coords[0][0])[0:6] + "_" + str(self.coords[1][0])[0:6], 1)
        f1.plot_name = "Saxs res " + str(self.coords[0][0])[0:6] + " " + str(self.coords[1][0])[0:6]

        if self.figure.data_x[0].extra_info[0] == "scan":
            x_name = "z"
        elif self.figure.data_x[0].extra_info[0] == "frame":
            x_name = "time"

        """Integral"""
        temp_x = Data_array(integral_x, x_name, None, "nesaisias")
        temp_y = Data_array(integral_y, "Integral", None, "nesaispas")
        f1.add_data_x_Data(temp_x)
        f1.add_data_y1_Data(temp_y)

        """derivée"""
        temp_x = Data_array(derive1_x, x_name, None, "nesaisias")
        temp_y = Data_array(derive1_y, "derivée 1", None, "nesaispas")
        f1.add_data_x_Data(temp_x)
        f1.add_data_y1_Data(temp_y)

        """derivée 2"""
        temp_x = Data_array(derive2_x, x_name, None, "nesaisias")
        temp_y = Data_array(derive2_y, "derivée 2", None, "nesaispas")
        f1.add_data_x_Data(temp_x)
        f1.add_data_y1_Data(temp_y)

        f1.type = "res_saxs"
        return f1

    """----------------------------------------------------------------------------------"""

    def calc(self):
        integral_x = []
        integral_y = []

        for i in range(len(self.figure.data_x)):
            integral_x.append(self.figure.data_x[i].extra_info[1])

        derive1_x = []
        derive1_y = []

        derive2_x = []
        derive2_y = []

        data_x = []
        data_y = []

        array_res = []

        for i in range(len(self.figure.data_x)):
            data_x.append(self.figure.data_x[i].data)
            data_y.append(self.figure.data_y1[i].data)

        if self.coords[0][0] > self.coords[1][0]:
            temp = self.coords[1][0]
            self.coords[1][0] = self.coords[0][0]
            self.coords[0][0] = temp

        array_res.append(["born1=" + str(self.coords[0][0]) + "\t" + "born2=" + str(self.coords[1][0])])
        array_res.append(["temperature\tx_max\tarea\tlargeur"])

        for i in range(len(data_x)):
            index = 0
            while data_x[i][index] < self.coords[0][0]:
                index += 1

            born_x_min = data_x[i][index]
            born_y_min = data_y[i][index]
            index_min = index

            while data_x[i][index] < self.coords[1][0]:
                """calcule de x ou y est max"""
                index += 1

            born_x_max = data_x[i][index]
            born_y_max = data_y[i][index]
            index_max = index

            calc = 0
            for j in range(index_min + 1, index_max + 1):
                calc += ((abs(data_x[i][j]) - abs(data_x[i][j - 1])) * data_y[i][j - 1] +
                         (data_y[i][j] - data_y[i][j - 1]) * (data_x[i][j] - data_x[i][j - 1]) / 2)

            """soustraction du trapéze"""
            calc -= (born_x_max - born_x_min) * born_y_min + (born_x_max - born_x_min) * (born_y_max - born_y_min) / 2
            integral_y.append(calc)

            """
            val_max = self.figure.data_y1[i].data[0]
            val_min = self.figure.data_y1[i].data[0]
            for j in range(len(self.figure.data_y1[i].data)):
                if self.figure.data_y1[i].data[j] > val_max:
                    val_max = self.figure.data_y1[i].data[j]
                if self.figure.data_y1[i].data[j] < val_min:
                    val_min = self.figure.data_y1[i].data[j]

            for j in range(len(self.figure.data_y2[i].data)):
                if self.figure.data_y2[i].data[j] > val_max:
                    val_max = self.figure.data_y2[i].data[j]

                if self.figure.data_y2[i].data[j] < val_min:
                    val_min = self.figure.data_y2[i].data[j]
            pas = (val_max - val_min) / 200
            """
            index = index_min + 1
            derive1_x.append([])
            derive1_y.append([])

            while index < index_max:
                p1 = [data_x[i][index - 1], data_y[i][index - 1]]
                p2 = [data_x[i][index], data_y[i][index]]

                res_deriv = self.derive_point(p1, p2)
                if res_deriv is None:
                    index += 1
                    continue
                derive1_x[i].append(data_x[0][index])
                derive1_y[i].append(res_deriv)
                index += 1

            derive2_x.append([])
            derive2_y.append([])

            for j in range(1, len(derive1_x[i])):
                p1 = [derive1_x[i][j - 1], derive1_y[i][j - 1]]
                p2 = [derive1_x[i][j], derive1_y[i][j]]

                res_deriv = self.derive_point(p1, p2)
                if res_deriv is None:
                    continue
                derive2_x[i].append(derive1_x[i][j])
                derive2_y[i].append(res_deriv)

        self.res_calc.extend(array_res)
        return integral_x, integral_y, derive1_x, derive1_y, derive2_x, derive2_y

    """----------------------------------------------------------------------------------"""

    def derive_point(self, p1, p2):
        if p2[0] - p1[0] == 0:
            return None

        derive = (p2[1] - p1[1]) / (p2[0] - p1[0])
        """        
        if abs(derive) > 5:
            return None
        else:
            return derive"""
        return derive

    """----------------------------------------------------------------------------------"""

    @property
    def finish(self):
        return self._finish

    """----------------------------------------------------------------------------------"""

    @finish.setter
    def finish(self, arg):
        if arg is False:
            self._finish = arg
        else:
            if self.can_be_closed is False:
                self.can_be_closed = True
                obj_data = Array_Abstract_objet_affiche()
                obj_data.event_thread2.set()
            else:
                self._finish = True

    """----------------------------------------------------------------------------------"""
