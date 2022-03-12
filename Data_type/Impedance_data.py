from Console_Objets.Data_Unit import Units, Data_unit
from Console_Objets.Data_array import Data_array
from Console_Objets.Figure import Figure
from Data_type.Abstract_data import Abstract_data
from Data_type.Traitement_cycle import Traitements_cycle_outils, Traitement_cycle_impedance
from Resources_file.Emit import Emit


class Impedance_data(Abstract_data):
    def __init__(self):
        super().__init__()

        self.__name__ = "Impedance_data"

        self._nb_electrodes = None
        self.export_resistance_array = []
        self.norm = None

    """----------------------------------------------------------------------------------"""

    def create_figure_cycle(self, *args, **kwargs):
        """
        La création de cycle passe par cette methode, en fonction du type de cycle
        on appelle la methode de création correspondante

        :param args:
        :param kwargs:
        :return: None
        """
        """if self.current_figure.type == "impedance_3d":
            emit = Emit()
            emit.emit("msg_console", type="msg_console", str="Cycle processing not possible for a 3d figure",
                      foreground_color="red")
            return"""

        cycle_type = kwargs["type"]
        cycles = kwargs["cycles"]


        if cycles is not None and len(cycles) == 3 and cycles[1] == "to":
            name = str(cycles[0]) + " to " + str(cycles[2])
        elif cycles is None:
            name = "all"
        else:
            s = ""
            for i in cycles:
                s += str(i) + " "
            name = s[0:-1]

        cycles = self.return_create_cycle(cycles)

        if cycles is None:
            return

        if cycle_type == "Cycle":
            figure = self.cycle(cycles)
        else:
            raise ValueError

        if isinstance(figure, list):
            for f in figure:
                f.name = self.unique_name(self.current_figure.name + " cycle " + name + f.name)
        else:
            figure.name = self.unique_name(self.current_figure.name + " cycle " + name + figure.name)

        return figure

    """----------------------------------------------------------------------------------"""

    def cycle(self, cycle):
        return Traitement_cycle_impedance.cycle_impedance(self.current_figure, cycle)

    """----------------------------------------------------------------------------------"""

    def capa(self):
        raise ValueError

    """----------------------------------------------------------------------------------"""

    def potentio(self, cycle=None):
        raise ValueError

    """----------------------------------------------------------------------------------"""

    def derive(self, pas=None):
        raise NotImplementedError

    """----------------------------------------------------------------------------------"""

    def area(self):
        raise ValueError

    """----------------------------------------------------------------------------------"""

    def shift_axe(self, info):
        raise NotImplementedError

    """----------------------------------------------------------------------------------"""

    def create_GITT(self):
        raise ValueError

    """----------------------------------------------------------------------------------"""

    def get_GITT_array(self):
        raise ValueError

    """----------------------------------------------------------------------------------"""

    def diffraction_contour_temperature(self, color_arg=None):
        raise ValueError

    """----------------------------------------------------------------------------------"""

    def create_diffraction(self):
        raise ValueError

    """----------------------------------------------------------------------------------"""

    def calc_diffraction(self):
        raise ValueError

    """----------------------------------------------------------------------------------"""

    def get_cycle_available(self):
        return ["Cycle"]

    """----------------------------------------------------------------------------------"""

    def export_gitt(self, path):
        raise ValueError

    """----------------------------------------------------------------------------------"""

    def get_dics(self):
        return "loop_data", self.resource.freq

    """----------------------------------------------------------------------------------"""

    def get_dics_sub(self):
        return "loop_data", self.resource.freq, "Re(Z)/Ohm", "-Im(Z)/Ohm"

    """----------------------------------------------------------------------------------"""

    def get_operation_available(self):
        return ["Impedance", "Resistance", "Resistance all", "Bode", "3d", "Subtract"]

    """----------------------------------------------------------------------------------"""

    def get_edit_data_available(self):
        return []

    """----------------------------------------------------------------------------------"""

    def process_edit_data(self, array_res):
        pass

    """----------------------------------------------------------------------------------"""

    def create_impedance(self):
        """
        création d'un figure d'impedance classique

        :return: Figure impedance
        """

        new_figure = Figure(self.name + " impedance")
        new_figure_brut = Figure(self.name + " impedance_brut")

        new_figure.type = "impedance"
        new_figure_brut.type = "impedance"

        units = Units()
        unit_x = units.get_unit("Re(Z)/Ohm")
        unit_y = units.get_unit("-Im(Z)/Ohm")

        for i in range(len(self.data.get("loop_data"))):
            start = self.data.get("loop_data")[i][0]
            end = self.data.get("loop_data")[i][1]

            global_index = [i for i in range(start, end)]

            res = Traitements_cycle_outils.mode_del(self.data.get("Re(Z)/Ohm")[start:end],
                                                    self.data.get("-Im(Z)/Ohm")[start:end],
                                                    global_index, start, end, self.data.get("mode"), 3)

            data_unit_x = Data_unit(res[0], unit_x)
            data_unit_y = Data_unit(res[1], unit_y)

            data_array_x = Data_array(data_unit_x, "Re(Z)/Ohm", self.name, "cycle " + str(i + 1))
            data_array_y = Data_array(data_unit_y, "-Im(Z)/Ohm", self.name, "cycle " + str(i + 1))

            data_array_x.global_index = res[2]

            new_figure_brut.add_data_x_Data(data_array_x)
            new_figure_brut.add_data_y1_Data(data_array_y)


            for j in range(len(res[0])):
                if j > 10 and res[0][j] * 1.5 < res[1][j]:
                    data_unit_x = Data_unit(res[0][0:j], unit_x)
                    data_unit_y = Data_unit(res[1][0:j], unit_y)

                    data_array_x = Data_array(data_unit_x, "Re(Z)/Ohm", self.name, "cycle " + str(i + 1))
                    data_array_y = Data_array(data_unit_y, "-Im(Z)/Ohm", self.name, "cycle " + str(i + 1))

                    data_array_x.global_index = res[2][0:j]

                    new_figure.add_data_x_Data(data_array_x)
                    new_figure.add_data_y1_Data(data_array_y)
                    break

            if len(new_figure.x_axe.data) != i + 1:
                data_unit_x = Data_unit(res[0][0:j], unit_x)
                data_unit_y = Data_unit(res[1][0:j], unit_y)

                data_array_x = Data_array(data_unit_x, "Re(Z)/Ohm", self.name, "cycle " + str(i + 1))
                data_array_y = Data_array(data_unit_y, "-Im(Z)/Ohm", self.name, "cycle " + str(i + 1))

                data_array_x.global_index = res[2][0:j]

                new_figure.add_data_x_Data(data_array_x)
                new_figure.add_data_y1_Data(data_array_y)

        new_figure.type = "impedance"
        new_figure_brut.type = "impedance"

        new_figure.aspect = "equal"
        new_figure_brut.aspect = "equal"

        new_figure.name = self.unique_name(new_figure.name)
        new_figure_brut.name = self.unique_name(new_figure_brut.name)

        return [new_figure, new_figure_brut]

    """----------------------------------------------------------------------------------"""

    def impedance_res(self, freqs):
        """
        création du graph de resistance
        A voir si par la suite je passe par un fit plutôt que cette dérivé de *****

        :param freqs:
        :return:
        """

        units = Units()
        unit_x = units.get_unit("time/h")
        unit_y = None

        new_figure = Figure("Rse reel", 1)
        new_figure.plot_name = self.name + " R\u209b\u2091 reel"

        new_figure_2 = Figure("Rse img", 1)
        new_figure_2.plot_name = self.name + " R\u209b\u2091 img"

        new_figure_3 = Figure("Rse phase", 1)
        new_figure_3.plot_name = self.name + " R\u209b\u2091 phase"

        new_figure_4 = Figure("Rse module", 1)
        new_figure_4.plot_name = self.name + " R\u209b\u2091 module"

        loop_data = self.data.get("loop_data")
        img = self.data.get("-Im(Z)/Ohm")
        reel = self.data.get("Re(Z)/Ohm")
        phase = self.data.get("Phase(Z)/deg")
        module = self.data.get("|Z|/Ohm")

        array_x = []
        array_y = []
        self.export_resistance_array = []

        for i in range(len(loop_data)):
            val_min = loop_data[i][0]
            val_max = loop_data[i][1]
            for j in range(val_min, val_max + 1):
                if j - val_min > 10 and self.data.get("Re(Z)/Ohm")[j] * 1.5 < self.data.get("-Im(Z)/Ohm")[j]:
                    val_max = j
                    break

            min_x = self.data.get("time/h")[val_min]

            data_x = []
            data_y = []
            data_x2 = []
            data_y2 = []

            for j in range(val_min + 2, val_max + 1):
                p1 = [reel[j - 1], img[j - 1]]
                p2 = [reel[j], img[j]]
                derive = self.derive_point(p1, p2)

                if derive is None:
                    continue
                data_x.append(reel[j])
                data_y.append(derive)

            for j in range(1, len(data_x)):
                p1 = [data_x[j - 1], data_y[j - 1]]
                p2 = [data_x[j], data_y[j]]
                derive = self.derive_point(p1, p2)
                if derive is None:
                    continue
                data_x2.append(data_x[j])
                data_y2.append(abs(derive))

            sort_array_x = []
            sort_array_y = []

            for freq in freqs:
                index = 0
                while index < len(data_y2) and \
                        self.data["freq/Hz"][val_min:val_max][index] > freq:
                    index += 1
                if 0 < index < len(data_y2) and \
                        abs(self.data["freq/Hz"][val_min:val_max][index - 1] - freq) < \
                        abs(self.data["freq/Hz"][val_min:val_max][index] - freq):
                    index -= 1

                if index == 0:
                    if data_y2[0] > data_y2[1]:

                        sort_array_x.append(data_x2[0])
                        sort_array_y.append(data_y2[0])
                    else:
                        sort_array_x.append(data_x2[1])
                        sort_array_y.append(data_y2[1])
                elif index == len(data_y2):
                    if data_y2[index - 1] > data_y2[index - 2]:
                        sort_array_x.append(data_x2[index - 1])
                        sort_array_y.append(data_y2[index - 1])
                    else:
                        sort_array_x.append(data_x2[index - 2])
                        sort_array_y.append(data_y2[index - 2])
                elif index == len(data_y2) - 1:
                    if data_y2[index] > data_y2[index - 1]:
                        sort_array_x.append(data_x2[index])
                        sort_array_y.append(data_y2[index])
                    else:
                        sort_array_x.append(data_x2[index - 1])
                        sort_array_y.append(data_y2[index - 1])
                else:
                    min_ = data_y2[index - 1]
                    max_ = data_y2[index + 1]
                    centre_ = data_y2[index]
                    if min_ == max(min_, max_, centre_):
                        sort_array_x.append(data_x2[index - 1])
                        sort_array_y.append(data_y2[index - 1])
                    elif max_ == max(min_, max_, centre_):
                        sort_array_x.append(data_x2[index + 1])
                        sort_array_y.append(data_y2[index + 1])
                    else:
                        sort_array_x.append(data_x2[index])
                        sort_array_y.append(data_y2[index])

            array_x.append(min_x)
            array_y.append(sort_array_x)
            self.export_resistance_array.append([min_x, sort_array_x])

        img_data = []
        phase_data = []
        module_data = []
        for i in range(len(loop_data)):
            val_min = loop_data[i][0]
            val_max = loop_data[i][1]
            img_data.append([])
            phase_data.append([])
            module_data.append([])
            for j in range(val_min, val_max + 1):
                for k in range(len(array_y[0])):
                    if reel[j] == array_y[i][k]:
                        img_data[-1].append(img[j])
                        phase_data[-1].append(phase[j])
                        module_data[-1].append(module[j])
                        break

        for i in range(len(freqs)):
            temp_y = []
            temp_y2 = []
            temp_y3 = []
            temp_y4 = []
            for j in range(len(array_x)):
                temp_y.append(array_y[j][i])
                temp_y2.append(img_data[j][i])
                temp_y3.append(phase_data[j][i])
                temp_y4.append(module_data[j][i])

            # figure 1
            data_unit_x = Data_unit(array_x, unit_x)
            data_unit_y = Data_unit(temp_y, unit_y)

            data_array_x = Data_array(data_unit_x, "time", self.name, "R(\u209b\u2091) freq " + str(freqs[i]))
            data_array_y = Data_array(data_unit_y, "Re(Z) [Ohm]", self.name, "R(\u209b\u2091) freq " + str(freqs[i]))

            new_figure.add_data_x_Data(data_array_x)
            new_figure.add_data_y1_Data(data_array_y)

            # figure 2
            data_unit_y = Data_unit(temp_y2, unit_y)
            data_array_y = Data_array(data_unit_y, "-Im(Z) [Ohm]", self.name, "R(\u209b\u2091) freq " + str(freqs[i]))

            new_figure_2.add_data_x_Data(data_array_x)
            new_figure_2.add_data_y1_Data(data_array_y)

            # figure 3
            data_unit_y = Data_unit(temp_y3, unit_y)
            data_array_y = Data_array(data_unit_y, "Phase(Z) [Ohm]", self.name, "R(\u209b\u2091) freq " + str(freqs[i]))

            new_figure_3.add_data_x_Data(data_array_x)
            new_figure_3.add_data_y1_Data(data_array_y)

            # figure 4
            data_unit_y = Data_unit(temp_y4, unit_y)
            data_array_y = Data_array(data_unit_y, "|Z|(Z) [Ohm]", self.name, "R(\u209b\u2091) freq " + str(freqs[i]))

            new_figure_4.add_data_x_Data(data_array_x)
            new_figure_4.add_data_y1_Data(data_array_y)


        new_figure.format_line_y1 = 'x'
        new_figure_2.format_line_y1 = 'x'
        new_figure_3.format_line_y1 = 'x'
        new_figure_4.format_line_y1 = 'x'

        new_figure.type = "impedance_res"
        new_figure_2.type = "impedance_res"
        new_figure_3.type = "impedance_res"
        new_figure_4.type = "impedance_res"

        new_figure.name = self.unique_name(new_figure.name)
        new_figure_2.name = self.unique_name(new_figure_2.name)
        new_figure_3.name = self.unique_name(new_figure_3.name)
        new_figure_4.name = self.unique_name(new_figure_4.name)

        """test_derive1 = Figure("test_derive1", 1)
        test_derive2 = Figure("test_derive2", 1)
        val_min = loop_data[0][0]
        val_max = loop_data[0][1]
        for i in range(val_min, val_max + 1):
            if i - val_min > 10 and self.data.get("Re(Z)/Ohm")[i] * 1.5 < self.data.get("-Im(Z)/Ohm")[i]:
                val_max = i
                break

        data_traite_x = self.data.get("Re(Z)/Ohm")[val_min:val_max]
        data_traite_y = self.data.get("-Im(Z)/Ohm")[val_min:val_max]

        temp_x1 = []
        temp_y1 = []

        current_val = data_traite_x[0]
        for i in range(len(data_traite_y)):
            if data_traite_x[i] > current_val:
                temp_x1.append(data_traite_x[i])
                temp_y1.append(data_traite_y[i])
                current_val = data_traite_x[i]

        fig_point = Figure("test", 1)
        fig_point.add_data_x_Data(Data_array(temp_x1, None, None, None))
        fig_point.add_data_y1_Data(Data_array(temp_y1, None, None, None))

        self.figures.append(fig_point)

        reel = temp_x1
        img = temp_y1

        data_x = []
        data_y = []

        for i in range(1, len(reel)):
            p1 = [reel[i - 1], img[i - 1]]
            p2 = [reel[i], img[i]]
            derive = self.derive_point(p1, p2)

            if derive is None:
                continue
            data_x.append(reel[i])
            data_y.append(abs(derive))

        test_derive1.add_data_x_Data(Data_array(data_x, "reel", self.name, "derive test"))
        test_derive1.add_data_y1_Data(Data_array(data_y, "img", self.name, "derive test"))
        # test_derive1.format_line_y1 = "x"
        self.figures.append(test_derive1)

        data_x2 = []
        data_y2 = []
        for i in range(1, len(data_x)):
            p1 = [data_x[i - 1], data_y[i - 1]]
            p2 = [data_x[i], data_y[i]]
            derive = self.derive_point(p1, p2)
            if derive is None:
                continue
            data_x2.append(data_x[i])
            data_y2.append(abs(derive))

        test_derive2.add_data_x_Data(Data_array(data_x2, "reel", self.name, "derive test"))
        test_derive2.add_data_y1_Data(Data_array(data_y2, "img", self.name, "derive test"))

        self.current_figure = test_derive2
        self.figures.append(test_derive2)"""

        return [new_figure, new_figure_2, new_figure_3, new_figure_4]

    """----------------------------------------------------------------------------------"""

    def export_impedance_res(self, path):
        file = open(path, "w")

        array_res = [[self.export_resistance_array, self.name]]

        for i in range(len(array_res)):
            entete = array_res[i][1] + "\ntime/h\tcycle"
            for m in range(len(array_res[i][0][0][1])):
                entete += "\tres_" + str(m + 1)
            file.write(entete + "\n")
            for j in range(len(array_res[i][0])):
                file.write("cycle_" + str(j + 1) + "\t" + str(array_res[i][0][j][0]))
                for l in range(len(array_res[i][0][j][1])):
                    file.write("\t" + str(array_res[i][0][j][1][l]))
                file.write("\n")

        file.close()

    """----------------------------------------------------------------------------------"""

    def impedance_bode(self):
        """
        Création d'un diagramme de bode, pas grand chose à faire ici

        :return: figure diagramme de bode
        """
        new_figure = Figure(self.name + " diagramme_bode")

        units = Units()
        unit_x = units.get_unit("freq/Hz")
        unit_y1 = units.get_unit("|Z|/Ohm")
        unit_y2 = units.get_unit("Phase(Z)/deg")

        for i in range(len(self.data.get("loop_data"))):
            start = self.data.get("loop_data")[i][0]
            end = self.data.get("loop_data")[i][1]

            gloabal_index = [val for val in range(start, end)]

            res = Traitements_cycle_outils.mode_del(self.data.get("freq/Hz")[start:end],
                                                   self.data.get("|Z|/Ohm")[start:end], gloabal_index,
                                                   start, end, self.data.get("mode"), 3)

            data_unit_x = Data_unit(res[0], unit_x)
            data_unit_y1 = Data_unit(res[1], unit_y1)

            data_array_x = Data_array(data_unit_x, "freq/Hz", self.name, "cycle " + str(i + 1) + " module")
            data_array_y1 = Data_array(data_unit_y1, "|Z|/Ohm", self.name, "cycle " + str(i + 1) + " module")

            data_array_x.global_index = res[2]

            new_figure.add_data_x_Data(data_array_x)
            new_figure.add_data_y1_Data(data_array_y1)

        for i in range(len(self.data.get("loop_data"))):

            start = self.data.get("loop_data")[i][0]
            end = self.data.get("loop_data")[i][1]

            gloabal_index = [val for val in range(start, end)]

            res = Traitements_cycle_outils.mode_del(self.data.get("freq/Hz")[start:end],
                                                   self.data.get("Phase(Z)/deg")[start:end], gloabal_index,
                                                   start, end, self.data.get("mode"), 3)

            data_unit_x = Data_unit(res[0], unit_x)
            data_unit_y2 = Data_unit(res[1], unit_y2)

            data_array_x = Data_array(data_unit_x, "freq/Hz", self.name, "cycle " + str(i + 1) + " phase")
            data_array_y2 = Data_array(data_unit_y2, "Phase(Z)/deg", self.name, "cycle " + str(i + 1) + " phase")

            data_array_x.global_index = res[2]

            new_figure.add_data_x_Data(data_array_x)
            new_figure.add_data_y2_Data(data_array_y2)

        new_figure.type = "bode"
        new_figure.x_axe.scale = "Log"
        new_figure.y1_axe.scale = "Log"

        new_figure.name = self.unique_name(new_figure.name)

        return new_figure

    """----------------------------------------------------------------------------------"""

    def create_impedance_3d(self, axe_y_name):
        """
        création d'un graph 3d d'impedance

        :param axe_y_name: time/h ou Ecell/V
        :return: figure 3d
        """
        new_figure = Figure(self.name + " impedance_3d")

        for i in range(len(self.data.get("loop_data"))):

            start = self.data.get("loop_data")[i][0]
            end = self.data.get("loop_data")[i][1]

            res = Traitements_cycle_outils.mode_del_3d(self.data.get("Re(Z)/Ohm")[start:end],
                                                      self.data.get("-Im(Z)/Ohm")[start:end],
                                                      self.data.get(axe_y_name)[start:end], start, end,
                                                      self.data.get("mode"), 3)

            for j in range(len(res[0])):
                if j > 10 and res[0][j] * 1.5 < res[1][j]:
                    data_unit_x = Data_unit(res[0][0:j], None)
                    data_unit_y1 = Data_unit(res[1][0:j], None)
                    data_unit_z1 = Data_unit(res[2][0:j], None)


                    new_figure.add_data_x_Data(Data_array(data_unit_x, "Re(Z)/Ohm",
                                                          self.name, "cycle " + str(i + 1)))
                    new_figure.add_data_z1_Data(Data_array(data_unit_y1, "-Im(Z)/Ohm",
                                                           self.name, "cycle " + str(i + 1)))
                    new_figure.add_data_y1_Data(Data_array(data_unit_z1, axe_y_name,
                                                           self.name, "cycle " + str(i + 1)))
                    break
            if len(new_figure.x_axe.data) != i + 1:
                data_unit_x = Data_unit(res[0][0:j], None)
                data_unit_y1 = Data_unit(res[1][0:j], None)
                data_unit_z1 = Data_unit(res[2][0:j], None)

                new_figure.add_data_x_Data(Data_array(data_unit_x, "Re(Z)/Ohm",
                                                      self.name, "Re(Z)/Ohm"))
                new_figure.add_data_z1_Data(Data_array(data_unit_y1, "-Im(Z)/Ohm",
                                                       self.name, "cycle " + str(i + 1)))
                new_figure.add_data_y1_Data(Data_array(data_unit_z1, axe_y_name,
                                                       self.name, "cycle " + str(i + 1)))

        new_figure.type = "impedance_3d"

        new_figure.name = self.unique_name(new_figure.name)

        return new_figure

    """----------------------------------------------------------------------------------"""

    def impedance_sub(self, *args, **kwargs):
        loop = kwargs["loop"]

        dics = kwargs["dics"]
        loop_data = dics["loop_data"]
        reel = dics["Re(Z)/Ohm"]
        img = dics["-Im(Z)/Ohm"]
        freq = dics["freq/Hz"]

        if len(freq) == 2:
            if freq[0][0] != freq[1][0] or freq[0][-1] != freq[1][-1] or freq[0][1] != freq[1][1]:
                print("Soustraction impossible")
                return

            if loop[0] > len(loop_data[0]):
                self.resource.print_color("Numéro de cycle " + str(loop[0]) + " invalide", "fail")
                self.resource.print_color("Cycle compris entre 1 et " + str(len(loop_data[0])), "fail")

                return
            if loop[1] > len(loop_data[1]):
                self.resource.print_color("Numéro de cycle " + str(loop[1]) + " invalide", "fail")
                self.resource.print_color("Cycle compris entre 1 et " + str(len(loop_data[1])), "fail")
                return
        else:
            if loop[0] > len(loop_data[0]):
                self.resource.print_color("Numéro de cycle " + str(loop[0]) + " invalide", "fail")
                self.resource.print_color("Cycle compris entre 1 et " + str(len(loop_data[0])), "fail")
                return
            if loop[0] > len(loop_data[0]):
                self.resource.print_color("Numéro de cycle " + str(loop[0]) + " invalide", "fail")
                self.resource.print_color("Cycle compris entre 1 et " + str(len(loop_data[0])), "fail")
                return

        new_figure = Figure("impedance_sub_" + str(loop[0]) + "_" + str(loop[1]))
        new_figure.type = "impedance"

        loop[0] -= 1
        loop[1] -= 1

        index_min_1 = loop_data[0][loop[0]][0]
        index_max_1 = loop_data[0][loop[0]][1]

        if len(loop_data) == 2:
            index_min_2 = loop_data[1][loop[1]][0]
            index_max_2 = loop_data[1][loop[-1]][1]
        else:
            index_min_2 = loop_data[0][loop[1]][0]
            index_max_2 = loop_data[0][loop[-1]][1]

        reel_temp = []
        img_temp = []

        res = Traitement_cycle_outils.mode_del(reel[0][index_min_1: index_max_1], img[0][index_min_1: index_max_1],
                                               index_min_1, index_max_1, self.data.get("mode"), 3)
        reel_temp.append(res[0])
        img_temp.append(res[1])

        if len(freq) == 2:
            res = Traitement_cycle_outils.mode_del(reel[1][index_min_2:index_max_2], img[1][index_min_2: index_max_2],
                                                   index_min_2, index_max_2, self.data.get("mode"), 3)
            reel_temp.append(res[0])
            img_temp.append(res[1])
        else:
            res = Traitement_cycle_outils.mode_del(reel[0][index_min_2:index_max_2], img[0][index_min_2: index_max_2],
                                                   index_min_2, index_max_2, self.data.get("mode"), 3)
            reel_temp.append(res[0])
            img_temp.append(res[1])

        reel = reel_temp
        img = img_temp

        if len(reel[0]) < len(reel[1]):
            val_min = len(reel[0])
        else:
            val_min = len(reel[1])

        new_array_x = []
        new_array_y = []

        for i in range(0, val_min):
            x = reel[0][i] - reel[1][i]
            y = img[0][i] - img[1][i]
            new_array_x.append(x)
            new_array_y.append(y)

        new_figure.add_data_x_Data(Data_array(new_array_x, "Re(Z)/Ohm", None,
                                              "sub_" + str(loop[0] + 1) + "_" + str(loop[1] + 1)))
        new_figure.add_data_y1_Data(Data_array(new_array_y, "-Im(Z)/Ohm", None,
                                               "sub_" + str(loop[0] + 1) + "_" + str(loop[1] + 1)))

        self.current_figure = new_figure
        self.figures.append(new_figure)

    """----------------------------------------------------------------------------------"""


    """                                                            """
    """                      Methode de class                      """
    """                                                            """

    def derive_point(self, p1, p2):
        if p2[0] - p1[0] == 0:
            return None
        derive = (p2[1] - p1[1]) / (p2[0] - p1[0])
        if abs(derive) > 5:
            return None
        else:
            return derive

    """----------------------------------------------------------------------------------"""

    def outil_min(self, val, array, pc):
        for i in range(len(array)):
            off_set = array[i] * pc / 100
            if val - off_set < array[i] < val + off_set:
                return False
        return True

    """----------------------------------------------------------------------------------"""

    """                                                  """
    """                      getter                      """
    """                                                  """

    @property
    def data(self):
        return self._data

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

    """                                                  """
    """                      setter                      """
    """                                                  """

    @data.setter
    def data(self, data):
        self._data = data

    @name.setter
    def name(self, name):
        self._name = name

    @figures.setter
    def figures(self, figures):
        self.current_figure = None

    @current_figure.setter
    def current_figure(self, figure):
        self._current_figure = figure

    @resource.setter
    def resource(self, resource):
        self._resource = resource

    """                                                         """
    """                      getter de class                    """
    """                                                         """

    @property
    def nb_electrodes(self):
        return self._nb_electrodes

    """                                                         """
    """                      setter de class                    """
    """                                                         """

    @nb_electrodes.setter
    def nb_electrodes(self, nb):
        self._nb_electrodes = nb
