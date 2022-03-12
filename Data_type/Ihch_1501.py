import copy

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

    def impedance_res(self, freqs):
        raise ValueError

    """"----------------------------------------------------------------------------------"""

    def impedance_bode(self):
        raise ValueError

    """"----------------------------------------------------------------------------------"""

    def create_impedance_3d(self, axe_y_name):
        raise ValueError

    """"----------------------------------------------------------------------------------"""

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

    def create_figure_cycle(self, arg, type, cycles, numbers, samples):
        """
        On créer la figure associé à la selection, on check ici que les paramètres sont
        cohérent. Les list sont ordonnée du plus petit au plus grand, on ne chexk donc que
        le dernier élement des lists


        :param arg: waxs / saxs
        :param type: frame / scan
        :param cycles: list des cycle selectionnés
        :param numbers: list des frame/scan selectionnés si None => toute
        :param samples: indes des samples selectionnée
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

        if type == "frame":
            # on check que le dernier nombres de la liste (le plus grand) est infè
            """if numbers is not None and numbers[-1] >= self._cycles[0].get_nb_frame():
                emit.emit("msg_console", type="msg_console", str="There is only " + str(len(self._cycles)) + " frames"
                          , foreground_color="red")
                return"""

            figures = self.trace_frame(arg, cycles, numbers, samples)

        elif type == "scan":
            """if arg == "saxs":
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
                    return"""

            figures = self.trace_scan(arg, cycles, numbers, samples)

        else:
            raise NotImplementedError

        """for figure in figures:
            figure.name = self.unique_name(self.nom_cell + " cycle " + name + " " + figure.name)"""

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

    def trace_frame(self, type, num_cycle, num_fram, sample):
        """

        :param sample: nom des sample a tracer
        :param type: saxs/waxs
        :param num_cycle: list des cycles que l'on souhaite traiter
        :param num_fram: list des frame que l'on souhaite traiter, si None => toutes
        :return: 3 figures
        """

        if type == "saxs":
            name = "Saxs "
        else:
            name = "Waxs "

        for i in range(len(num_cycle) - 1):
            name += self._cycles[num_cycle[i]].name + " / "

        name += self._cycles[num_cycle[-1]].name + " Sample "

        # nom des samples
        for i in range(len(sample) - 1):
            waxs_sample = self._cycles[num_cycle[0]].waxs[i].name
            name += waxs_sample.name + " / "

        name += self._cycles[num_cycle[0]].waxs[sample[-1]].name + " Frame "

        # nom des Frame
        if num_fram is None:
            name += " all"
        elif len(num_fram) > 1:
            name += str(num_fram[0] + 1) + " to " + str(num_fram[-1] + 1)
        else:
            name += str(num_fram[0] + 1)

        if type == "saxs":
            fig_general = Figure(name + " general")
            fig_lit = Figure(name + " lithiation")
            fig_del = Figure(name + " delithiation")

            type = "saxs frame"
            fig_general.type = "saxs frame"
            fig_lit.type = "saxs frame"
            fig_del.type = "saxs frame"
        elif type == "waxs":
            fig_general = Figure(name + " general")
            fig_lit = Figure(name + " lithiation")
            fig_del = Figure(name + " delithiation")

            type = "waxs frame"
            fig_general.type = "waxs frame"
            fig_lit.type = "waxs frame"
            fig_del.type = "waxs frame"
        else:
            raise ValueError

        units = Units()
        x_unit = units.get_unit("degrees")
        y_unit = units.get_unit("ua")

        array_time = []

        if type == "waxs frame":
            for cycle in num_cycle:
                for i in sample:
                    waxs_sample = self._cycles[cycle].waxs[i]
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

                            legend = "time/h " + str(frame.frames[num].data["time/s"] / 3600)[0:5] + " " + frame.name
                            array_time.append(frame.frames[num].data["time/s"] / 3600)

                            fig_general.add_data_x_Data(Data_array(data_unit_x, "2th_deg", self.name, legend))
                            fig_general.add_data_y1_Data(Data_array(data_unit_y, "Intesity", self.name, legend))

                            if "lithiation" in waxs_sample.name:
                                fig_lit.add_data_x_Data(Data_array(data_unit_x, "2th_deg", self.name, legend))
                                fig_lit.add_data_y1_Data(Data_array(data_unit_y, "Intesity", self.name, legend))

                            elif "delithiation" in waxs_sample.name:
                                fig_del.add_data_x_Data(Data_array(data_unit_x, "2th_deg", self.name, legend))
                                fig_del.add_data_y1_Data(Data_array(data_unit_y, "Intesity", self.name, legend))

        else:
            for cycle in num_cycle:
                for i in sample:
                    saxs_sample = self._cycles[cycle].saxs[i]
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

                            legend = "time/h " + str(frame.frames[num].data["time/s"] / 3600)[0:5] + " z " + str(
                                num + 1)
                            array_time.append(frame.frames[num].data["time/s"] / 3600)

                            fig_general.add_data_x_Data(Data_array(data_unit_x, "q_A^-1", self.name, legend))
                            fig_general.add_data_y1_Data(Data_array(data_unit_y, "Intesity", self.name, legend))

                            if "lithiation" in saxs_sample.name:
                                fig_lit.add_data_x_Data(Data_array(data_unit_x, "q_A^-1", self.name, legend))
                                fig_lit.add_data_y1_Data(Data_array(data_unit_y, "Intesity", self.name, legend))

                            elif "delithiation" in saxs_sample.name:
                                fig_del.add_data_x_Data(Data_array(data_unit_x, "q_A^-1", self.name, legend))
                                fig_del.add_data_y1_Data(Data_array(data_unit_y, "Intesity", self.name, legend))

        fig_general.kwarks["array_time"] = array_time


        fig_general.name = self.unique_name(fig_general.name)
        fig_lit.name = self.unique_name(fig_lit.name)
        fig_del.name = self.unique_name(fig_del.name)

        figure_electroch = self.create_electroch(num_cycle[0])
        if figure_electroch is None:
            # return [fig_general, fig_lit, fig_del]
            return [fig_general]
        else:
            # return [fig_general, fig_lit, fig_del, figure_electroch]
            return [fig_general, figure_electroch]

    """----------------------------------------------------------------------------------"""

    def trace_scan(self, type, num_cycle, num_scan, sample):
        """
        num scan correspond à son numéro h5, on récupérera son index

        :param type:
        :param cycles:
        :param num_scan:
        :return:
        """
        # nom des cycles
        if type == "saxs":
            name = "Saxs "
        else:
            name = "Waxs "

        for i in range(len(num_cycle) - 1):
            name += self._cycles[num_cycle[i]].name + " / "

        name += self._cycles[num_cycle[-1]].name + " Sample "

        # nom des samples
        for i in range(len(sample) - 1):
            waxs_sample = self._cycles[num_cycle[0]].waxs[i].name
            name += waxs_sample.name + " / "

        name += self._cycles[num_cycle[0]].waxs[sample[-1]].name + " Scan "

        # nom des scans
        if num_scan is None:
            name += " all"
        elif len(num_scan) > 1:
            name += num_scan[0] + " to " + num_scan[-1]
        else:
            name += num_scan[0]

        if type == "saxs":
            type = "saxs scan"
            fig_general = Figure(name)
            fig_general.type = "saxs scan"
        elif type == "waxs":
            type = "waxs scan"
            fig_general = Figure(name)
            fig_general.type = "waxs scan"
        else:
            raise ValueError

        units = Units()
        x_unit = units.get_unit("degrees")
        y_unit = units.get_unit("ua")

        array_time = []

        if type == "waxs scan":
            for cycle in num_cycle:
                for i in sample:
                    waxs_sample = self._cycles[cycle].waxs[i]
                    if num_scan is None:
                        _num_scan = [i for i in range(len(waxs_sample.scans))]
                    else:
                        _num_scan = waxs_sample.get_scans(num_scan)

                    for num in _num_scan:
                        for i, frame in enumerate(waxs_sample.scans[num].frames):
                            data_x = frame.data["2th_deg"]
                            data_y = frame.data["I"]

                            data_unit_x = Data_unit(data_x, x_unit)
                            data_unit_y = Data_unit(data_y, y_unit)

                            legend = "time/h " + str(frame.data["time/s"] / 3600)[0:5] + " z " + str(i + 1)
                            array_time.append(frame.data["time/s"] / 3600)

                            fig_general.add_data_x_Data(Data_array(data_unit_x, "2th_deg", self.name, legend))
                            fig_general.add_data_y1_Data(Data_array(data_unit_y, "Intensity", self.name, legend))
        else:
            for cycle in num_cycle:
                for i in sample:
                    saxs_sample = self._cycles[cycle].saxs[i]
                    if num_scan is None:
                        _num_scan = [i for i in range(len(saxs_sample.scans))]
                    else:
                        _num_scan = saxs_sample.get_scans(num_scan)

                    for num in _num_scan:
                        for frame in saxs_sample.scans[num].frames:
                            data_x = frame.data["q_A^-1"]
                            data_y = frame.data["I"]

                            data_unit_x = Data_unit(data_x, x_unit)
                            data_unit_y = Data_unit(data_y, y_unit)

                            legend = "time/h " + str(frame.data["time/s"] / 3600)[0:5] + " z " + str(num + 1)
                            array_time.append(frame.data["time/s"] / 3600)

                            fig_general.add_data_x_Data(Data_array(data_unit_x, "q_A^-1", self.name, legend))
                            fig_general.add_data_y1_Data(Data_array(data_unit_y, "Intensity", self.name, legend))

        fig_general.name = self.unique_name(fig_general.name)
        fig_general.kwarks["array_time"] = array_time

        figure_electroch = self.create_electroch(num_cycle[0])
        if figure_electroch is None:
            return [fig_general]
        else:
            return [fig_general, figure_electroch]

    """----------------------------------------------------------------------------------"""

    def get_operation_available(self):
        return ["Ihch 1501 plot"]

    """----------------------------------------------------------------------------------"""

    def get_edit_data_available(self):
        return []

    """----------------------------------------------------------------------------------"""

    def process_edit_data(self, array_res):
        pass

    """----------------------------------------------------------------------------------"""

    def get_cycle_available(self):
        raise ValueError

    """----------------------------------------------------------------------------------"""

    def create_impedance(self):
        raise ValueError

    """----------------------------------------------------------------------------------"""

    def export_gitt(self, path):
        raise ValueError

    """----------------------------------------------------------------------------------"""

    def export_impedance_res(self, path):
        raise ValueError

    """----------------------------------------------------------------------------------"""

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

    def create_electroch(self, num_cycle):
        saxs_time = []
        saxs_potentiel = []
        saxs_courrant = []

        waxs_time = []
        waxs_potentiel = []
        waxs_courrant = []

        time = []
        potentiel = []
        courrant = []

        for sample_saxs in self._cycles[num_cycle].saxs:
            for scan in sample_saxs.scans:
                for frame in scan.frames:
                    try:
                        saxs_time.append(frame.data["time/s"])
                        saxs_potentiel.append(frame.data["Ecell/V"])
                        saxs_courrant.append(frame.data["<I>/mA"])
                    except KeyError:
                        print(sample_saxs.name)
                        print(scan.name)
                        print(frame.name)
                        print(frame.data)



        for sample_waxs in self._cycles[num_cycle].waxs:
            for scan in sample_waxs.scans:
                for frame in scan.frames:
                    try:
                        waxs_time.append(frame.data["time/s"])
                        waxs_potentiel.append(frame.data["Ecell/V"])
                        waxs_courrant.append(frame.data["<I>/mA"])
                    except ValueError:
                        print(sample_waxs.name)
                        print(scan.name)
                        print(frame.name)
                        print(frame.data)

        while len(saxs_time) != 0 and len(waxs_time) != 0:
            if saxs_time[0] < waxs_time[0]:
                time.append(saxs_time.pop(0))
                potentiel.append(saxs_potentiel.pop(0))
                courrant.append(saxs_courrant.pop(0))
            else:
                time.append(waxs_time.pop(0))
                potentiel.append(waxs_potentiel.pop(0))
                courrant.append(waxs_courrant.pop(0))

        if len(saxs_time) != 0:
            time.extend(saxs_time)
            potentiel.extend(saxs_potentiel)
            courrant.extend(saxs_courrant)
        else:
            time.extend(waxs_time)
            potentiel.extend(waxs_potentiel)
            courrant.extend(waxs_courrant)

        figure = Figure("check ec lab", 1)
        figure.type = "saxs"

        units = Units()
        x_unit = units.get_unit("s")
        y1_unit = units.get_unit("Ecell/V")
        y2_unit = units.get_unit("<I>/mA")

        data_unit_x1 = Data_unit(time, x_unit)
        data_unit_x2 = Data_unit(copy.copy(time), x_unit)

        data_unit_y1 = Data_unit(potentiel, y1_unit)
        data_unit_y2 = Data_unit(courrant, y2_unit)

        data_array_x1 = Data_array(data_unit_x1, "time", self.name, None)
        data_array_y1 = Data_array(data_unit_y1, "Ecell", self.name, "potentiel")

        data_array_x2 = Data_array(data_unit_x2, "time", self.name, None)
        data_array_y2 = Data_array(data_unit_y2, "<I>", self.name, "courrant")

        figure.add_data_x_Data(data_array_x1)
        figure.add_data_y1_Data(data_array_y1)

        figure.add_data_x_Data(data_array_x2)
        figure.add_data_y2_Data(data_array_y2)

        figure.name = self.unique_name(figure.name)

        return figure


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

    def get_nb_frame(self):
        return len(self.saxs[0].scans[0].frames)


class Ihch_1501_sample_waxs:
    def __init__(self, name):
        self.name = name
        self.scans = []

    def get_scans(self, array):
        array_res = []
        while len(array) != 0:
            name = array[0]
            while len(name) < 4:
                name = "0" + name

            i = 0
            while i < len(self.scans) and self.scans[i].name != name:
                i += 1

            # on n'a pas trouvé un nom
            if i == len(self.scans):
                raise ValueError
            else:
                array_res.append(i)
                array.pop(0)
        return array_res

    def is_scan_exist(self, scan_name):
        if len(scan_name) > 4:
            return False

        while len(scan_name) < 4:
            scan_name = "0" + scan_name

        i = 0
        while i < len(self.scans) and self.scans[i].name != scan_name:
            i += 1

        if i == len(self.scans):
            return False
        else:
            return True

    def get_range(self, name_start, name_end):
        res = []

        while len(name_start) < 4:
            name_start = "0" + name_start

        while len(name_end) < 4:
            name_end = "0" + name_end

        i = 0
        while i < len(self.scans) and self.scans[i].name != name_start:
            i += 1

        while i < len(self.scans) and self.scans[i].name != name_end:
            res.append(self.scans[i].name)
            i += 1

        res.append(self.scans[i].name)

        return res


class Ihch_1501_sample_saxs:
    def __init__(self, name):
        self.name = name
        self.scans = []

    def get_scans(self, array):
        array_res = []
        while len(array) != 0:
            name = array[0]
            while len(name) < 4:
                name = "0" + name

            i = 0
            while i < len(self.scans) and self.scans[i].name != name:
                i += 1

            # on n'a pas trouvé un nom
            if i == len(self.scans):
                raise ValueError
            else:
                array_res.append(i)
        return array_res

    def is_scan_exist(self, scan_name):
        if len(scan_name) > 4:
            return False

        while len(scan_name) < 4:
            scan_name = "0" + scan_name

        i = 0
        while i < len(self.scans) and self.scans[i].name != scan_name:
            i += 1

        if i == len(self.scans):
            return False
        else:
            return True

    def get_range(self, name_start, name_end):
        res = []

        while len(name_start) < 4:
            name_start = "0" + name_start

        while len(name_end) < 4:
            name_end = "0" + name_end

        i = 0
        while i < len(self.scans) and self.scans[i].name != name_start:
            i += 1

        while i < len(self.scans) and self.scans[i].name != name_end:
            res.append(self.scans[i].name)
            i += 1

        return res


class Ihch_1501_scan:
    def __init__(self, name):
        self.name = name
        self.frames = []


class Ihch_1501_frame:
    def __init__(self, name):
        self.name = name
        self.data = {}
