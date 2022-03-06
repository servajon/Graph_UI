from Console_Objets.Data_Unit import Units, Data_unit
from Console_Objets.Data_array import Data_array
from Console_Objets.Figure import Figure
from Data_type.Abstract_data import Abstract_data
from Data_type.Traitement_cycle import Traitement_cycle_diffraction

import matplotlib.pyplot as pplot

from Resources_file.Emit import Emit


class Ihch_1501(Abstract_data):
    def __init__(self):
        super().__init__()
        self.__name__ = "ihch 1501"

        self._cycles = []
        self.res_calc_saxs = []
        self.res_calc_waxs = []

    """----------------------------------------------------------------------------------"""

    def capa(self):
        raise ValueError

    """----------------------------------------------------------------------------------"""

    def potentio(self, cycle=None):
        raise ValueError

    """----------------------------------------------------------------------------------"""

    def derive(self, pas=None):
        raise ValueError

    """----------------------------------------------------------------------------------"""

    def shift_axe(self, info):
        raise ValueError

    """----------------------------------------------------------------------------------"""

    def get_dics(self):
        raise ValueError

    """----------------------------------------------------------------------------------"""

    def diffraction_contour_temperature(self, color_arg=None):
        raise ValueError

    """----------------------------------------------------------------------------------"""

    def create_diffraction(self):
        raise ValueError

    """----------------------------------------------------------------------------------"""

    def create_GITT(self, *args, **kwargs):
        raise ValueError

    """----------------------------------------------------------------------------------"""

    def get_info_data(self):
        print("info sur les données : " + self.name + "\n")
        for cycle in self._cycles:
            print("\tsaxs")
            for sample_saxs in cycle.saxs:
                print("\t\t" + sample_saxs.name)
                for scans in sample_saxs.scans:
                    print("\t\t\t\t" + scans.name)
                    for frame in scans.frames:
                        print("\t\t\t\t\t\t" + frame.name)
                        for key, value in frame.data.items():
                            try:
                                print("\t\t\t\t\t\t\t\t" + str(len(value)))
                            except TypeError:
                                print("\t\t\t\t\t\t\t\t" + key + " : " + str(value))
            print("\twaxs")
            for sample_waxs in cycle.waxs:
                print("\t\t" + sample_waxs.name)
                for scans in sample_waxs.scans:
                    print("\t\t\t\t" + scans.name)
                    for frame in scans.frames:
                        print("\t\t\t\t\t\t" + frame.name)
                        for key, value in frame.data.items():
                            try:
                                print("\t\t\t\t\t\t\t\t" + str(len(value)))
                            except TypeError:
                                print("\t\t\t\t\t\t\t\t" + key + " : " + str(value))

    """----------------------------------------------------------------------------------"""

    def create_figure_cycle(self, arg, type, cycles, numbers):
        """
        On créer la figure associé à la selection, on check ici que les paramètres sont
        cohérent. Les list sont ordonnée du plus petit au plus grand, on ne chexk donc que
        le dernier élement des lists


        :param arg: waxs / saxs
        :param type: frame / scan
        :param cycles: list des cycle selectionnés
        :param numbers: list des frame/scan selectionnés si None => toute
        :return: figure / None : figure si tout c'est bien passé, None sinon
        """

        emit = Emit()

        # on check si les cycles selectionnée sont valides
        if cycles[-1] > len(self._cycles):
            emit.emit("msg_console", type="msg_console", str="There is only " + str(len(self._cycles)) + " cycle(s)"
                      , foreground_color="red")
            return

        s = ""
        for i in cycles:
            s += str(i) + " "
        name = s[0:-1]

        print(cycles)
        print(arg)
        print(type)
        print(numbers)

        if type == "frame":
            # on check que le dernier nombres de la liste (le plus grand) est infè
            if numbers is not None and numbers[-1] >= self._cycles[0].get_nb_frame():
                emit.emit("msg_console", type="msg_console", str="There is only " + str(len(self._cycles)) + " frames"
                          , foreground_color="red")
                return

            figures = self.trace_frame(arg, cycles, numbers)

        elif type == "scan":
            if arg == "saxs":
                if numbers is not None and numbers[-1] >= self._cycles[cycles[-1] - 1].get_nb_scan_saxs():
                    emit.emit("msg_console", type="msg_console",
                              str="There is only " + str(self._cycles[cycles[-1]].get_nb_frame()) + " scans on saxs"
                              , foreground_color="red")
                    return

            else:
                if numbers is not None and numbers[-1] >= self._cycles[cycles[-1]].get_nb_scan_waxs():
                    emit.emit("msg_console", type="msg_console",
                              str="There is only " + str(self._cycles[cycles[-1] - 1].get_nb_frame()) + " scans on waxs"
                              , foreground_color="red")
                    return

            figures = self.trace_scan(arg, cycles, numbers)

        else:
            raise NotImplementedError

        for figure in figures:
            figure.name = self.unique_name(self.nom_cell + " cycle " + name + " " + figure.name)

        return figures

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

    """------------------------------------------------------------------------------"""

    """                                                                              """
    """                               methode de class                               """
    """                                                                              """

    def trace_frame(self, type, num_cycle, num_fram):
        """

        :param type: saxs/waxs
        :param num_cycle: list des cycles que l'on souhaite traiter
        :param num_fram: list des frame que l'on souhaite traiter, si None => toutes
        :return: 3 figures
        """

        if num_fram is None:
            s = " all"
        else:
            s = ""
            for num in num_fram:
                s += " " + str(num + 1)

        if type == "saxs":
            fig_general = Figure("saxs_Frame" + s + " general")
            fig_lit = Figure("saxs_Frame" + s + " lithiation")
            fig_del = Figure("saxs Frame" + s + " delithiation")
            fig_general.type = "saxs"
            fig_lit.type = "saxs"
            fig_del.type = "saxs"
        elif type == "waxs":
            fig_general = Figure("waxs Frame " + s + " general")
            fig_lit = Figure("waxs Frame" + s + " lithiation")
            fig_del = Figure("waxs Frame" + s + " delithiation")
            fig_general.type = "waxs"
            fig_lit.type = "waxs"
            fig_del.type = "waxs"
        else:
            raise ValueError

        units = Units()
        x_unit = units.get_unit("degrees")
        y_unit = units.get_unit("<I>/mA")


        if type == "waxs":
            for cycle in num_cycle:
                for waxs_sample in self._cycles[cycle].waxs:
                    for frame in waxs_sample.scans:
                        if num_fram is None:
                            _num_fram = [i for i in range(len(frame.frames))]
                        else:
                            _num_fram = num_fram

                        for num in _num_fram:
                            data_x = frame.frames[num].data["2th_deg"]
                            data_y = frame.frames[num].data["I"]

                            data_unit_x = Data_unit(data_x, x_unit)
                            data_unit_y = Data_unit(data_y, y_unit)

                            legend = "time/h " + str(frame.frames[num].data["time/s"] / 3600)[0:5] + " z " + str(num + 1)

                            fig_general.add_data_x_Data(Data_array(data_unit_x, "2th_deg", self.name, legend))
                            fig_general.add_data_y1_Data(Data_array(data_unit_y, "current", self.name, legend))

                            if "lithiation" in waxs_sample.name:
                                fig_lit.add_data_x_Data(Data_array(data_unit_x, "2th_deg", self.name, legend))
                                fig_lit.add_data_y1_Data(Data_array(data_unit_y, "current", self.name, legend))

                            elif "delithiation" in waxs_sample.name:
                                fig_del.add_data_x_Data(Data_array(data_unit_x, "2th_deg", self.name, legend))
                                fig_del.add_data_y1_Data(Data_array(data_unit_y, "current", self.name, legend))

        else:
            for cycle in num_cycle:
                for saxs_sample in self._cycles[cycle].saxs:
                    for frame in saxs_sample.scans:
                        if num_fram is None:
                            _num_fram = [i for i in range(len(frame.frames))]
                        else:
                            _num_fram = num_fram

                        for num in _num_fram:
                            data_x = frame.frames[num].data["q_A^-1"]
                            data_y = frame.frames[num].data["I"]

                            data_unit_x = Data_unit(data_x, x_unit)
                            data_unit_y = Data_unit(data_y, y_unit)

                            legend = "time/h " + str(frame.frames[num].data["time/s"] / 3600)[0:5] + " z " + str(num + 1)

                            fig_general.add_data_x_Data(Data_array(data_unit_x, "q_A^-1", self.name, legend))
                            fig_general.add_data_y1_Data(Data_array(data_unit_y, "current", self.name, legend))

                            if "lithiation" in saxs_sample.name:
                                fig_lit.add_data_x_Data(Data_array(data_unit_x, "q_A^-1", self.name, legend))
                                fig_lit.add_data_y1_Data(Data_array(data_unit_y, "current", self.name, legend))

                            elif "delithiation" in saxs_sample.name:
                                fig_del.add_data_x_Data(Data_array(data_unit_x, "q_A^-1", self.name, legend))
                                fig_del.add_data_y1_Data(Data_array(data_unit_y, "current", self.name, legend))


        fig_general.name = self.unique_name(fig_general.name)
        fig_lit.name = self.unique_name(fig_lit.name)
        fig_del.name = self.unique_name(fig_del.name)

        return [fig_general, fig_lit, fig_del]

    """----------------------------------------------------------------------------------"""

    def trace_scan(self, type, num_cycle, num_scan):
        """

        :param type:
        :param cycles:
        :param num_scan:
        :param color_arg:
        :return:
        """

        if num_scan is None:
            s = " all"
        else:
            s = ""
            for num in num_scan:
                s += " " + str(num + 1)

        if type == "saxs":
            fig_general = Figure("saxs Scan " + s + " general")
            fig_general.type = "saxs"
        elif type == "waxs":
            fig_general = Figure("waxs Scan " + s + " general")
            fig_general.type = "waxs"
        else:
            raise ValueError

        units = Units()
        x_unit = units.get_unit("degrees")
        y_unit = units.get_unit("<I>/mA")


        if type == "waxs":
            for cycle in num_cycle:
                for waxs_sample in self._cycles[cycle].waxs:
                    print(len(waxs_sample.scans))
                    if num_scan is None:
                        _num_scan = [i for i in range(len(waxs_sample.scans))]
                    else:
                        _num_scan = num_scan
                    for num in _num_scan:
                        for i, frame in enumerate(waxs_sample.scans[num].frames):
                            data_x = frame.data["2th_deg"]
                            data_y = frame.data["I"]

                            data_unit_x = Data_unit(data_x, x_unit)
                            data_unit_y = Data_unit(data_y, y_unit)

                            legend = "time/h " + str(frame.data["time/s"] / 3600)[0:5] + " z " + str(i + 1)

                            fig_general.add_data_x_Data(Data_array(data_unit_x, "2th_deg", self.name, legend))
                            fig_general.add_data_y1_Data(Data_array(data_unit_y, "current", self.name, legend))
        else:
            for cycle in num_cycle:
                for saxs_sample in self._cycles[cycle].saxs:
                    print(len(saxs_sample.scans))
                    if num_scan is None:
                        _num_scan = [i for i in range(len(saxs_sample.scans))]
                    else:
                        _num_scan = num_scan
                    for num in _num_scan:
                        for frame in saxs_sample.scans[num].frames:
                            data_x = frame.data["q_A^-1"]
                            data_y = frame.data["I"]

                            data_unit_x = Data_unit(data_x, x_unit)
                            data_unit_y = Data_unit(data_y, y_unit)

                            legend = "time/h " + str(frame.data["time/s"] / 3600)[0:5] + " z " + str(num + 1)

                            fig_general.add_data_x_Data(Data_array(data_unit_x, "q_A^-1", self.name, legend))
                            fig_general.add_data_y1_Data(Data_array(data_unit_y, "current", self.name, legend))


        fig_general.name = self.unique_name(fig_general.name)
        return [fig_general]

    """----------------------------------------------------------------------------------"""

    def get_operation_available(self):
        return ["Ihch 1501 plot"]

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
                index += 1
                if i == 0:
                    axe.set_ylabel(leg_name[1])

            for i, axe in enumerate(ligne_3):
                if i == 1:
                    fig.delaxes(axe)
                    break
                axe.plot(figure.data_x[index].data, figure.data_y1[index].data, "x", color='r', label=leg_name[2])
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
    def cycles(self):
        return self._cycles

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

    @cycles.setter
    def cycles(self, cycles):
        self._cycles = cycles

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
