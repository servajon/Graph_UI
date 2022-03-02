from Console_Objets.Data_Unit import Units, Data_unit
from Console_Objets.Data_array import Data_array
from Console_Objets.Figure import Figure
from Data_type.Abstract_data import Abstract_data
from Data_type.Traitement_cycle import Traitement_cycle_diffraction

import matplotlib.pyplot as pplot


class Ihch_1501(Abstract_data):
    def __init__(self):
        super().__init__()
        self._cycles = []
        self.res_calc_saxs = []
        self.res_calc_waxs = []

    """----------------------------------------------------------------------------------"""

    def capa(self):
        self.resource.print_color("Opération invalide pour un fichier de Ihch 1501", "fail")
        raise ValueError

    """----------------------------------------------------------------------------------"""

    def potentio(self, cycle=None):
        self.resource.print_color("Opération invalide pour un fichier de Ihch 1501", "fail")
        raise ValueError

    """----------------------------------------------------------------------------------"""

    def derive(self, pas=None):
        self.resource.print_color("Opération invalide pour un fichier de Ihch 1501", "fail")
        raise ValueError

    """----------------------------------------------------------------------------------"""

    def shift_axe(self, info):
        self.resource.print_color("Opération invalide pour un fichier de Ihch 1501", "fail")
        raise ValueError

    """----------------------------------------------------------------------------------"""

    def get_dics(self):
        self.resource.print_color("Opération invalide pour un fichier de Ihch 1501", "fail")
        raise ValueError

    """----------------------------------------------------------------------------------"""

    def diffraction_contour_temperature(self, color_arg=None):
        self.resource.print_color("Opération invalide pour un fichier de Ihch 1501", "fail")
        raise ValueError

    """----------------------------------------------------------------------------------"""

    def create_diffraction(self):
        self.resource.print_color("Opération invalide pour un fichier de Ihch 1501", "fail")
        raise ValueError

    """----------------------------------------------------------------------------------"""

    def get_info_data(self):
        print("info sur les données : " + self.name + "\n")
        for cycle in self._cycles:
            print(cycle.name)

            for sample_saxs in cycle.saxs:
                print("\t\t" + sample_saxs.name)
                for scans in sample_saxs.scans:
                    print("\t\t\t\t" + scans.name)
                    for frame in scans.frames:
                        print("\t\t\t\t\t\t" + frame.name)

            for sample_waxs in cycle.waxs:
                print("\t\t" + sample_waxs.name)
                for scans in sample_waxs.scans:
                    print("\t\t\t\t" + scans.name)
                    for frame in scans.frames:
                        print("\t\t\t\t\t\t" + frame.name)
                        for key, value in frame.data.items():
                            print("\t\t\t\t\t\t\t\t" + str(len(value)))

    """----------------------------------------------------------------------------------"""

    def creation_figure_ihch(self, arg, type, cycle_number, number, color_arg=None):
        """
        return -1 si la format est invalide
        arg : waxs / saxs
        type : frame / scan / sample
        number :
        cycle_number :
        color : color
        """

        try:
            number = int(number)
            number -= 1
        except ValueError:
            self.resource.print_color("Un nombre est demandé", "fail")
            raise ValueError

        try:
            cycle_number = int(cycle_number)
            cycle_number -= 1
        except ValueError:
            self.resource.print_color("Un nombre de cycle est demandé", "fail")
            raise ValueError

        if type == "frame":
            if cycle_number >= len(self._cycles):
                self.resource.print_color("Il n'y a que " + str(len(self._cycles)) + "cycle(s)", "fail")
                raise ValueError
            if number >= self._cycles[0].get_nb_frame():
                self.resource.print_color("Il n'y a que " + str(self._cycles[0].get_nb_frame()) + "frame", "fail")
                raise ValueError

            self.trace_frame(arg, cycle_number, number, color_arg)

        elif type == "scan":
            if cycle_number >= len(self._cycles):
                self.resource.print_color("Il n'y a que " + str(len(self._cycles)) + "cycle(s)", "fail")
                raise ValueError
            if arg == "saxs":
                if number >= self._cycles[cycle_number].get_nb_scan_saxs():
                    self.resource.print_color("Il n'y a que " + str(self._cycles[cycle_number].get_nb_frame())
                                              + "scan saxs", "fail")
                    raise ValueError
            else:
                if number >= self._cycles[cycle_number].get_nb_scan_waxs():
                    self.resource.print_color("Il n'y a que " + str(self._cycles[cycle_number].get_nb_frame())
                                              + "scan waxs", "fail")
                    raise ValueError

            self.trace_scan(arg, cycle_number, number, color_arg)

        else:
            raise NotImplementedError

    """----------------------------------------------------------------------------------"""

    def calc_figure_ihch(self):
        array_obj_data = Array_Abstract_objet_affiche()
        if self.current_figure.type == "waxs":
            obj = array_obj_data.append(Waxs_affiche(self, self.current_figure))
        elif self.current_figure.type == "saxs":
            obj = array_obj_data.append(Saxs_affiche(self, self.current_figure))

        array_obj_data.event_thread2.wait()
        array_obj_data.event_thread2.clear()

        for i in range(len(obj.figure_res)):
            res = obj.figure_res[i]
            res.name = self.unique_name(res.name)
            self.figures.append(res)

        if self.current_figure is None and len(self.figures) > 0:
            self.current_figure = self.figures[0]

        self.res_calc_saxs.append(obj.res_calc)
        obj.finish = True

    """----------------------------------------------------------------------------------"""

    def format_axes(self, axe, type, name):
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
            if type == "saxs" and name == "y1":
                axe.set_yscale('log')
                axe.set_xscale('log')

    """----------------------------------------------------------------------------------"""

    def resize_axe(self, axe1, axe2, p, figure=None):
        if figure is not None and figure.type == "saxs":
            return
        else:
            """On augemente la taille de l'ax donné en paramétre de p %"""
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

    def norm_ihch(self):
        if self.current_figure.type is not None and self.current_figure.type != "saxs":
            self.resource.print_color("Opération uniquement disponible pour saxs", "fail")
            return
        elif self.current_figure.dirty is not None:
            self.resource.print_color("La figure que vous souhaitez utiliser possède des données modifiées, merci "
                                      "d'utiliser une figure où les données sont intègres", "fail")
            return
        else:
            array_obj_data = Array_Abstract_objet_affiche()
            obj = array_obj_data.append(Saxs_selection(self, self.current_figure))
            array_obj_data.event_thread2.wait()
            array_obj_data.event_thread2.clear()
            courbe_index = obj.index
            point_index = obj.res
            obj.finish = True

            if courbe_index is None or point_index is None:
                self.resource.print_color("Aucun point sélectionné", "fail")
                return

            fig = Figure("res_norm", 1)
            fig.type = "saxs"

            data_x = []
            data_y = []

            val_y = self.current_figure.data_y1[courbe_index[1][1]].data[point_index]

            for i in range(len(self.current_figure.data_y1)):
                data_x.append(copy.copy(self.current_figure.data_x[i]))

                norm = val_y / self.current_figure.data_y1[i].data[point_index]
                if norm != 1:
                    new_data_y = []
                    for j in range(len(self.current_figure.data_y1[i].data)):
                        new_data_y.append(self.current_figure.data_y1[i].data[j] * norm)
                else:
                    new_data_y = self.current_figure.data_y1[i].data
                data_array = copy.copy(self.current_figure.data_y1[i])
                data_array.data = new_data_y
                data_y.append(data_array)

            for i in range(len(data_x)):
                fig.add_data_x_Data(data_x[i])
                fig.add_data_y1_Data(data_y[i])

            fig.created_from = self.current_figure
            fig.name = self.unique_name(fig.name)
            self.current_figure = fig
            self.figures.append(fig)

    """----------------------------------------------------------------------------------"""

    def sub_ihch(self):
        if self.current_figure.type is not None and self.current_figure.type != "saxs":
            self.resource.print_color("Opération uniquement disponible pour saxs", "fail")
            return
        elif self.current_figure.dirty is not None:
            self.resource.print_color("La figure que vous souhaitez utiliser possède des données modifiées, merci "
                                      "d'utiliser une figure où les données sont intègres", "fail")
            return
        else:
            array_obj_data = Array_Abstract_objet_affiche()
            obj = array_obj_data.append(Saxs_selection(self, self.current_figure))
            array_obj_data.event_thread2.wait()
            array_obj_data.event_thread2.clear()
            courbe_index = obj.index
            obj.finish = True

            if courbe_index is None:
                self.resource.print_color("Aucune courbe électionnée", "fail")
                return
            fig = Figure("res_sub", 1)
            fig.type = "saxs"

            data_x = []
            data_y = []

            data_sub = self.current_figure.data_y1[courbe_index[1][1]]

            for i in range(len(self.current_figure.data_y1)):
                data_x.append(copy.copy(self.current_figure.data_x[i]))
                new_data_y = []
                if i != courbe_index:
                    for j in range(len(self.current_figure.data_y1[i].data)):
                        new_data_y.append(self.current_figure.data_y1[i].data[j] - data_sub.data[j])
                    data_array = copy.copy(self.current_figure.data_y1[i])
                    data_array.data = new_data_y
                    data_y.append(data_array)
                else:
                    data_array = copy.copy(self.current_figure.data_y1[i])
                    data_y.append(data_array)

            for i in range(len(data_x)):
                fig.add_data_x_Data(data_x[i])
                fig.add_data_y1_Data(data_y[i])

            fig.created_from = self.current_figure
            fig.name = self.unique_name(fig.name)
            self.current_figure = fig
            self.figures.append(fig)

    """----------------------------------------------------------------------------------"""
    """                                                                              """
    """                               methode de class                               """
    """                                                                              """

    def trace_frame(self, type, num_cycle, num_fram, color_arg=None):
        if type == "saxs":
            fig_general = Figure("saxs_Frame_" + str(num_fram + 1) + "_general")
            fig_lit = Figure("saxs_Frame_" + str(num_fram + 1) + "_lithiation")
            fig_del = Figure("saxs Frame_" + str(num_fram + 1) + "_delithiation")
            fig_general.type = "saxs"
            fig_lit.type = "saxs"
            fig_del.type = "saxs"
        elif type == "waxs":
            fig_general = Figure("waxs_Frame " + str(num_fram + 1) + "_general")
            fig_lit = Figure("waxs_Frame " + str(num_fram + 1) + "_lithiation")
            fig_del = Figure("waxs_Frame " + str(num_fram + 1) + "_delithiation")
            fig_general.type = "waxs"
            fig_lit.type = "waxs"
            fig_del.type = "waxs"
        else:
            raise ValueError

        num_cycle -= 1

        data_x = []
        data_y = []

        data_x_lit = []
        data_y_lit = []

        data_x_del = []
        data_y_del = []
        if type == "waxs":
            for waxs_sample in self._cycles[num_cycle].waxs:
                for scan in waxs_sample.scans:
                    data_x.append(scan.frames[num_fram].data["2th_deg"])
                    data_y.append(scan.frames[num_fram].data["I"])

            for waxs_sample in self._cycles[num_cycle].waxs:
                if "-lithiation-" in waxs_sample.name:
                    for scan in waxs_sample.scans:
                        data_x_lit.append(scan.frames[num_fram].data["2th_deg"])
                        data_y_lit.append(scan.frames[num_fram].data["I"])

            for waxs_sample in self._cycles[num_cycle].waxs:
                if "-delithiation-" in waxs_sample.name:
                    for scan in waxs_sample.scans:
                        data_x_del.append(scan.frames[num_fram].data["2th_deg"])
                        data_y_del.append(scan.frames[num_fram].data["I"])
        elif type == "saxs":
            for saxs_sample in self._cycles[num_cycle].saxs:
                for scan in saxs_sample.scans:
                    data_x.append(scan.frames[num_fram].data["q_A^-1"])
                    data_y.append(scan.frames[num_fram].data["I"])

            for saxs_sample in self._cycles[num_cycle].saxs:
                if "-lithiation-" in saxs_sample.name:
                    for scan in saxs_sample.scans:
                        data_x_lit.append(scan.frames[num_fram].data["q_A^-1"])
                        data_y_lit.append(scan.frames[num_fram].data["I"])

            for saxs_sample in self._cycles[num_cycle].saxs:
                if "-delithiation-" in saxs_sample.name:
                    for scan in saxs_sample.scans:
                        data_x_del.append(scan.frames[num_fram].data["q_A^-1"])
                        data_y_del.append(scan.frames[num_fram].data["I"])

        if color_arg is not None:
            if color_arg not in Resource.COLOR_MAP:
                self.resource.print_color(color_arg + " : couleur invalide", "fail")
                color_arg = None

        color_y1 = []
        if color_arg is not None:
            color_map = Resource.get_color_map(color_arg)
            color_y1.append(Traitement_cycle_outils.create_array_color(color_map, len(data_x)))

        for i in range(len(data_x)):

            if type == "waxs":
                temp_x = Data_array(data_x[i], "2th_deg", self.name, "time " + str(i) + " z " + str(num_fram + 1))
            else:
                temp_x = Data_array(data_x[i], "q(A\u207b\u00B9)", self.name, "time " + str(i) + " z " +
                                    str(num_fram + 1))
            temp_x.extra_info = ["frame", i]
            fig_general.add_data_x_Data(temp_x)

            if color_arg is None:
                temp_y = Data_array(data_y[i], "Saxs intensity (u.a)", self.name, "time " + str(i) + " z " + str(num_fram + 1))

            else:
                temp_y = Data_array(data_y[i], "Saxs intensity (u.a)", self.name, "time " + str(i) + " z " +
                                    str(num_fram + 1), color_y1[0][i])

            temp_y.extra_info = ["frame", i]
            fig_general.add_data_y1_Data(temp_y)

        color_y1 = []
        if color_arg is not None:
            color_map = Resource.get_color_map(color_arg)
            color_y1.append(Traitement_cycle_outils.create_array_color(color_map, len(data_x_lit)))

        for i in range(len(data_x_lit)):
            if type == "waxs":
                temp_x = Data_array(data_x_lit[i], "2th_deg", self.name, "time " + str(i) + " z " + str(num_fram + 1))
            else:
                temp_x = Data_array(data_x_lit[i], "q(A\u207b\u00B9)", self.name,
                                    "time " + str(i) + " z " + str(num_fram + 1))

            temp_x.extra_info = ["frame", i]
            fig_lit.add_data_x_Data(temp_x)

            if color_arg is None:
                temp_y = Data_array(data_y_lit[i], "Saxs intensity (u.a)", self.name, "time " + str(i) + " z " + str(num_fram + 1))

            else:
                temp_y = Data_array(data_y_lit[i], "Saxs intensity (u.a)", self.name, "time " + str(i) + " z " +
                                    str(num_fram + 1), color_y1[0][i])

            temp_y.extra_info = ["frame", i]
            fig_lit.add_data_y1_Data(temp_y)

        color_y1 = []
        if color_arg is not None:
            color_map = Resource.get_color_map(color_arg)
            color_y1.append(Traitement_cycle_outils.create_array_color(color_map, len(data_x_del)))

        for i in range(len(data_x_del)):
            if type == "waxs":
                temp_x = Data_array(data_x_del[i], "2 θ[°]", self.name, "time " + str(i) + " z " + str(num_fram + 1))
            else:
                temp_x = Data_array(data_x_del[i], "q(A\u207b\u00B9)", self.name,
                                    "time " + str(i) + " z " + str(num_fram + 1))

            temp_x.extra_info = ["frame", i]
            fig_del.add_data_x_Data(temp_x)

            if color_arg is None:
                temp_y = Data_array(data_y_del[i], "Saxs intensity (u.a)", self.name, "time " + str(i) + " z " + str(num_fram + 1))

            else:
                temp_y = Data_array(data_y_del[i], "Saxs intensity (u.a)", self.name, "time " + str(i) + " z " +
                                    str(num_fram + 1), color_y1[0][i])

            temp_y.extra_info = ["frame", i]
            fig_del.add_data_y1_Data(temp_y)

        fig_general.name = self.unique_name(fig_general.name)
        fig_lit.name = self.unique_name(fig_lit.name)
        fig_del.name = self.unique_name(fig_del.name)

        self.figures.append(fig_general)
        self.figures.append(fig_lit)
        self.figures.append(fig_del)

        self.current_figure = fig_general

    """----------------------------------------------------------------------------------"""

    def trace_scan(self, type, num_cycle, num_scan, color_arg=None):
        if type == "saxs":
            fig_general = Figure("saxs_Scan_" + str(num_scan + 1) + "_general")
            fig_general.type = "saxs"
        elif type == "waxs":
            fig_general = Figure("waxs_Scan_" + str(num_scan + 1) + "_general")
            fig_general.type = "waxs"

        num_cycle -= 1

        data_x = []
        data_y = []

        if type == "waxs":
            scan = self._cycles[num_cycle].get_frame_waxs(num_scan)
            for frame in scan.frames:
                data_x.append(frame.data["2th_deg"])
                data_y.append(frame.data["I"])

        elif type == "saxs":
            scan = self._cycles[num_cycle].get_frame_saxs(num_scan)
            for frame in scan.frames:
                data_x.append(frame.data["q_A^-1"])
                data_y.append(frame.data["I"])

        if color_arg is not None:
            if color_arg not in Resource.COLOR_MAP:
                self.resource.print_color(color_arg + " : couleur invalide", "fail")
                color_arg = None

        color_y1 = []
        if color_arg is not None:
            color_map = Resource.get_color_map(color_arg)
            color_y1.append(Traitement_cycle_outils.create_array_color(color_map, len(data_x)))

        for i in range(len(data_x)):
            if type == "waxs":
                temp_x = Data_array(data_x[i], "2 θ[°]", self.name, "time " + str(num_scan + 1) + " z " + str(i))

            else:
                temp_x = Data_array(data_x[i], "q(A\u207b\u00B9)", self.name, "time " + str(num_scan + 1) + " z " + str(i))

            temp_x.extra_info = ["scan", i]
            fig_general.add_data_x_Data(temp_x)

            if color_arg is None:
                temp_y = Data_array(data_y[i], "Saxs intensity (u.a)", self.name, "time " + str(num_scan + 1) + " z " + str(i))

            else:
                temp_y = Data_array(data_y[i], "Saxs intensity (u.a)", self.name, "time " + str(num_scan + 1) + " z " + str(i), color_y1[0][i])

            temp_y.extra_info = ["scan", i]
            fig_general.add_data_y1_Data(temp_y)

        fig_general.name = self.unique_name(fig_general.name)
        self.figures.append(fig_general)
        self.current_figure = fig_general

    """----------------------------------------------------------------------------------"""

    def get_operation_available(self):
        return ["à faire"]

    def create_figure_cycle(self, *args, **kwargs):
        raise ValueError

    def get_cycle_available(self):
        raise ValueError

    def load_graph_affichage(self, figure, path_save=None):
        if figure.type == "res_waxs":
            index = 0
            fig = pplot.figure(figsize=(11, 7))
            gs = fig.add_gridspec(3, 2, hspace=0.1, wspace=0, width_ratios=[10, 1])
            axes = gs.subplots(sharex='col', sharey='row')

            pplot.suptitle(figure.plot_name)

            ligne_1 = axes[0]
            ligne_2 = axes[1]
            ligne_3 = axes[2]

            leg_name = []
            for i in range(len(figure.data_y1)):
                leg_name.append(figure.data_y1[i].name)

            for i, axe in enumerate(ligne_1):
                if i == 1:
                    fig.delaxes(axe)
                    break

                axe.plot(figure.data_x[index].data, figure.data_y1[index].data, "x", color='b', label=leg_name[0])
                axe.get_xaxis().set_visible(False)
                self.resize_axe_y(axe, None, -7.5)
                index += 1
                if i == 0:
                    axe.set_ylabel(leg_name[0])

            for i, axe in enumerate(ligne_2):
                if i == 1:
                    leg = axe
                    axe.axis("off")
                    break
                axe.plot(figure.data_x[index].data, figure.data_y1[index].data, "x", color='g', label=leg_name[1])
                axe.get_xaxis().set_visible(False)
                self.resize_axe_y(axe, None, -7.5)
                index += 1
                if i == 0:
                    axe.set_ylabel(leg_name[1])

            for i, axe in enumerate(ligne_3):
                if i == 1:
                    fig.delaxes(axe)
                    break
                axe.plot(figure.data_x[index].data, figure.data_y1[index].data, "x", color='r', label=leg_name[2])
                self.resize_axe_y(axe, None, -7.5)
                index += 1
                if i == 0:
                    axe.set_ylabel(leg_name[2])
                    axe.set_xlabel(figure.data_x[0].name)

            h = []
            l = []
            leg_axe = [axes[0, 0], axes[1, 0], axes[2, 0]]

            for axe in leg_axe:
                h1, l1 = axe.get_legend_handles_labels()
                h.extend(h1)
                l.extend(l1)

            leg.legend(h, l, bbox_to_anchor=(2.75, 1))
            fig.subplots_adjust(left=0.130, right=0.865)

            if path_save is not None:
                pplot.tight_layout()
                pplot.close(fig)
                fig.savefig(path_save, bbox_inches='tight', dpi=150)

            return fig

        elif figure.type == "res_saxs":
            index = 0
            fig = pplot.figure(figsize=(11, 7))
            gs = fig.add_gridspec(3, 2, hspace=0.4, wspace=0, width_ratios=[10, 1])
            axes = gs.subplots()

            pplot.suptitle(figure.plot_name)

            ligne_1 = axes[0]
            ligne_2 = axes[1]
            ligne_3 = axes[2]

            leg_name = []
            for i in range(len(figure.data_y1)):
                leg_name.append(figure.data_y1[i].name)

            for i, axe in enumerate(ligne_1):
                if i == 1:
                    fig.delaxes(axe)
                    break

                axe.plot(figure.data_x[index].data, figure.data_y1[index].data, "x", color='b', label=leg_name[0])
                self.resize_axe_y(axe, None, -7.5)
                index += 1
                if i == 0:
                    axe.set_ylabel(leg_name[0])
                    axe.set_xlabel(figure.data_x[0].name)

            for i, axe in enumerate(ligne_2):
                if i == 1:
                    leg = axe
                    axe.axis("off")
                    break
                for j in range(len(figure.data_x[index].data)):
                    axe.plot(figure.data_x[index].data[j], figure.data_y1[index].data[j], color='g', label=leg_name[1])

                self.resize_axe_y(axe, None, -7.5)
                axe.set_xscale('log')
                index += 1
                if i == 0:
                    axe.set_ylabel(leg_name[1])
                    axe.set_xlabel(figure.data_x[0].name)

            for i, axe in enumerate(ligne_3):
                if i == 1:
                    fig.delaxes(axe)
                    break
                for j in range(len(figure.data_x[index].data)):
                    axe.plot(figure.data_x[index].data[j], figure.data_y1[index].data[j], color='r', label=leg_name[2])

                self.resize_axe_y(axe, None, -7.5)
                axe.set_xscale('log')
                index += 1
                if i == 0:
                    axe.set_ylabel(leg_name[2])
                    axe.set_xlabel(figure.data_x[0].name)

            h = []
            l = []
            leg_axe = [axes[0, 0], axes[1, 0], axes[2, 0]]

            for axe in leg_axe:
                h1, l1 = axe.get_legend_handles_labels()
                h.append(h1[0])
                l.append(l1[0])

            leg.legend(h, l, bbox_to_anchor=(2.75, 1))
            fig.subplots_adjust(left=0.130, right=0.865, top=0.94)

            if path_save is not None:
                pplot.tight_layout()
                pplot.close(fig)
                fig.savefig(path_save, bbox_inches='tight', dpi=150)

            return fig
        else:
            raise ValueError

    @property
    def data(self):
        raise ValueError("Opération invalide pour un fichier de Ihch 1501 (get_data)")

    @property
    def name(self):
        return self._name

    @property
    def nom_cell(self):
        return self._nom_cell

    @property
    def figures(self):
        return self._figures

    @property
    def current_figure(self):
        return self._current_figure

    @property
    def resource(self):
        return self._resource

    @data.setter
    def data(self, data):
        raise ValueError("Opération invalide pour un fichier de Ihch 1501 (set_data)")

    @name.setter
    def name(self, name):
        """On replace les espaces par des '_'"""
        self._name = name

    @nom_cell.setter
    def nom_cell(self, name):
        """On replace les espaces par des '_'"""
        self._nom_cell = name

    @figures.setter
    def figures(self, figures):
        print("Impossible d'utiliser le setter de figures de la class abstract data")

    @current_figure.setter
    def current_figure(self, figure):
        self._current_figure = figure

    @resource.setter
    def resource(self, resource):
        self._resource = resource


class Ihch_1501_cycle:
    def __init__(self, name):
        self.name = name
        self.waxs = []
        self.saxs = []

        self._nb_frame = None
        self._nb_scan_saxs = None
        self._nb_scan_waxs = None

    def get_nb_frame(self):
        if self._nb_frame is None:
            self._nb_frame = len(self.waxs[0].scans[0].frames)
        return self._nb_frame

    def get_nb_scan_saxs(self):
        if self._nb_scan_saxs is None:
            nb = 0
            for sample in self.saxs:
                nb += len(sample.scans)
            self._nb_scan_saxs = nb
        return self._nb_scan_saxs

    def get_nb_scan_waxs(self):
        if self._nb_scan_waxs is None:
            nb = 0
            for sample in self.waxs:
                nb += len(sample.scans)
            self._nb_scan_waxs = nb
        return self._nb_scan_waxs

    def get_frame_saxs(self, nb):
        count = 0
        for sample in self.saxs:
            for scan in sample.scans:
                if count == nb:
                    return scan
                count += 1

    def get_frame_waxs(self, nb):
        count = 0
        for sample in self.waxs:
            for scan in sample.scans:
                if count == nb:
                    return scan
                count += 1


class Ihch_1501_sample_waxs:
    def __init__(self, name):
        self.name = name
        self.scans = []


class Ihch_1501_sample_saxs:
    def __init__(self, name):
        self.name = name
        self.scans = []


class Ihch_1501_scan:
    def __init__(self, name):
        self.name = name
        self.frames = []


class Ihch_1501_frame:
    def __init__(self, name):
        self.name = name
        self.data = {}
        time = None
        potentiel = None
        courrant = None
