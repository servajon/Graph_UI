import math

from scipy.stats import linregress
import matplotlib.colors as mcolors

from Console_Objets.Data_array import Data_array
from Console_Objets.Figure import Figure
from Data_type.Abstract_data import Abstract_data


class Gitt_data(Abstract_data):
    def __init__(self):
        super().__init__()
        self._potentiel = None
        self._pulse = None
        self._relaxation = None

        self.interupt = False

        self._borne1 = []
        self._borne2 = []

        self.export_gitt_array = []

    """----------------------------------------------------------------------------------"""

    def get_operation_available(self):
        return ["Create gitt"]

    """----------------------------------------------------------------------------------"""

    def capa(self):
        raise ValueError

    """----------------------------------------------------------------------------------"""

    def potentio(self, cycle):
        raise ValueError

    """----------------------------------------------------------------------------------"""

    def derive(self, *args, **kwargs):
        raise ValueError

    """----------------------------------------------------------------------------------"""

    def shift_axe(self, *args, **kwargs):
        raise ValueError

    """----------------------------------------------------------------------------------"""

    def create_figure_cycle(self, *args, **kwargs):
        raise ValueError

    """----------------------------------------------------------------------------------"""

    def get_dics(self):
        raise ValueError

    """----------------------------------------------------------------------------------"""

    def create_diffraction(self):
        raise ValueError

    """----------------------------------------------------------------------------------"""

    def get_cycle_available(self):
        raise ValueError

    """----------------------------------------------------------------------------------"""

    def diffraction_contour_temperature(self):
        raise ValueError

    """----------------------------------------------------------------------------------"""

    def create_GITT(self, surface, vm, constante_d_n, bornes1, bornes2):
        # On reset tout avant de recréer les graphs de gitt"""
        self.current_figure = None
        self.create_gitt_methode(surface, vm, constante_d_n, bornes1, bornes2)

    """----------------------------------------------------------------------------------"""

    def create_gitt_methode(self, surface, vm, constante_d_n, bornes1, bornes2):
        loop_potentiel = self.potentiel.get("loop_data")
        loop_pulse = self.pulse.get("loop_data")
        loop_relax = self.relaxation.get("loop_data")

        self.export_gitt_array = []

        if not (len(loop_potentiel) == len(loop_pulse) and len(loop_potentiel) == len(loop_relax)):
            temp = []
            for i in range(len(loop_potentiel)):
                if loop_potentiel[i][0] != loop_potentiel[i][1]:
                    temp.append(loop_potentiel[i])

            loop_potentiel = temp
            temp = []
            for i in range(len(loop_pulse)):
                if loop_pulse[i][0] != loop_pulse[i][1]:
                    temp.append(loop_pulse[i])

            loop_pulse = temp
            temp = []
            for i in range(len(loop_relax)):
                if loop_relax[i][0] != loop_relax[i][1]:
                    temp.append(loop_relax[i])
            loop_relax = temp

            if not (len(loop_potentiel) == len(loop_pulse) and len(loop_potentiel) == len(loop_relax)):
                print("Nombre de loop différent entre les fichiers")
                raise ValueError

        constante_a = (4 / math.pi) * ((vm * abs(self._pulse.get("Is")) * 10 ** -6) / (surface * 96486)) ** 2

        plot_1 = Figure("GITT_général", 1)
        plot_1.plot_name = "GITT général"

        plot_2 = Figure("Potentiel_eq", 1)
        plot_2.plot_name = "Potentiel thermodynamique d'équilibre"

        plot_3 = Figure("Coef_diff", 1)
        plot_3.plot_name = "Coef de diffusion en fonction de l'état de charge"

        plot_controle = Figure("controle_regression", 1)

        plot_3.type = "coef_dif"

        plot_2.format_line_y1 = "x"
        plot_3.format_line_y1 = "x"

        array_plot_2_x_blue = []
        array_plot_2_x_green = []

        array_plot_2_y_blue = []
        array_plot_2_y_green = []

        blue = mcolors.CSS4_COLORS["blue"]
        red = mcolors.CSS4_COLORS["red"]
        green = mcolors.CSS4_COLORS["green"]
        black = mcolors.CSS4_COLORS["black"]

        for i in range(len(loop_potentiel)):
            plot_1.add_data_x_Data(
                Data_array(self._potentiel.get("time/s")[loop_potentiel[i][0]:loop_potentiel[i][1]], "time/h", "GITT",
                           "Potentiel initial", blue))
            plot_1.add_data_y1_Data(
                Data_array(self._potentiel.get("Ecell/V")[loop_potentiel[i][0]: loop_potentiel[i][1]], "Ecell/V",
                           "GITT", "Potentiel initial", blue))

            array_plot_2_x_blue.append(self._pulse.get("Is") * i / 1000)
            array_plot_2_y_blue.append(self._potentiel.get("Ecell/V")[loop_potentiel[i][1]])
        for i in range(len(loop_pulse)):
            plot_1.add_data_x_Data(
                Data_array(self._pulse.get("time/s")[loop_pulse[i][0]: loop_pulse[i][1]], "time/h", "GITT",
                           "Pulse de courant", red))
            plot_1.add_data_y1_Data(
                Data_array(self._pulse.get("Ecell/V")[loop_pulse[i][0]: loop_pulse[i][1]], "Ecell/V", "GITT",
                           "Pulse de courant", red))

        array_plot_2_x_green.append(0)
        array_plot_2_y_green.append(self._potentiel.get("Ecell/V")[loop_potentiel[0][1]])

        for i in range(len(loop_relax)):
            plot_1.add_data_x_Data(
                Data_array(self._relaxation.get("time/s")[loop_relax[i][0]: loop_relax[i][1]], "time/h", "GITT",
                           "Relaxation", green))
            plot_1.add_data_y1_Data(
                Data_array(self._relaxation.get("Ecell/V")[loop_relax[i][0]: loop_relax[i][1]], "Ecell/V", "GITT",
                           "Relaxation", green))

            array_plot_2_x_green.append(self._pulse.get("Is") * (i + 1) / 1000)
            array_plot_2_y_green.append(self._relaxation.get("Ecell/V")[loop_relax[i][1]])

        """a voir si ça fonctionne avec les légendes par la suite, une solution de merde..."""
        plot_1.nb_legende = 3
        plot_controle.nb_legende = 2

        plot_2.add_data_x_Data(Data_array(array_plot_2_x_green, "Capacité mAh", "GITT", "Eeq Relaxation", green))
        plot_2.add_data_y1_Data(
            Data_array(array_plot_2_y_green, "Potentiel de relaxation", "GITT", "Eeq Relaxation", green))

        array_x_plot3 = []
        array_y_plot3 = []

        self.export_gitt_array.append(["surface:" + str(surface) + "\tVM:" + str(vm) + "\tdelta n:" + str(constante_d_n)])
        self.export_gitt_array.append(["Cycle", "borne1", "borne2", "slope", "coef_difusion", "E-", "E+", "deltaE"])

        for i in range(len(loop_pulse)):
            array_export = [str(self.nom_cell) + "_loop_" + str(i + 1), str(math.sqrt(bornes1[i])),
                            str(math.sqrt(bornes2[i]))]

            num = (array_plot_2_y_green[i] - array_plot_2_y_green[i + 1]) / constante_d_n
            start_x = self._pulse.get("time/s")[loop_pulse[i][0]]
            j = loop_pulse[i][0]
            while j < loop_pulse[i][1] and self._pulse.get("time/s")[j] < start_x + bornes1[i]:
                j += 1

            if j == loop_pulse[i][1]:
                self.resource.print_color("Borne 1 invalide", "fail")
                raise ValueError

            index_min = j

            while j < loop_pulse[i][1] and self._pulse.get("time/s")[j] < start_x + bornes2[i]:
                j += 1

            if j == loop_pulse[i][1]:
                self.resource.print_color("Borne 2 invalide", "fail")
                raise ValueError

            index_max = j

            sqrt_temp = self._pulse.get("time/s")[loop_pulse[i][0]:loop_pulse[i][1]]
            sqrt_temp_start = sqrt_temp[0]
            for j in range(len(sqrt_temp)):
                sqrt_temp[j] = math.sqrt(sqrt_temp[j] - sqrt_temp_start)

            result = linregress(sqrt_temp[index_min - loop_pulse[i][0]:index_max - loop_pulse[i][0]],
                                self._pulse.get("Ecell/V")[index_min:index_max])

            calc = constante_a * ((num / result.slope) ** 2)
            array_export.append(str(result.slope))
            array_export.append(str(calc))

            array_export.append(str(array_plot_2_y_green[i]))
            array_export.append(str(array_plot_2_y_green[i + 1]))
            array_export.append(str(array_plot_2_y_green[i] - array_plot_2_y_green[i + 1]))

            array_x_plot3.append(i * self._pulse.get("Is") / 1000)
            array_y_plot3.append(calc)

            plot_controle.add_data_x_Data(Data_array(sqrt_temp, "", "", "Pulse de courant", blue))
            plot_controle.add_data_y1_Data(
                Data_array(self._pulse.get("Ecell/V")[loop_pulse[i][0]:loop_pulse[i][1]], "", "", "Pulse de courant",
                           blue))

            array_slop_x = sqrt_temp[index_min - loop_pulse[i][0]:index_max - loop_pulse[i][0]]
            array_slop_y = []
            plot_controle.add_data_x_Data(Data_array(array_slop_x, "sqrt(t)", "GITT", "Regression linéaire", black))
            for j in range(len(array_slop_x)):
                array_slop_y.append(array_slop_x[j] * result.slope + result.intercept)

            plot_controle.add_data_y1_Data((Data_array(array_slop_y, "E", "GITT", "Regression linéaire", black)))

            self.export_gitt_array.append(array_export)

        plot_3.add_data_x_Data(Data_array(array_x_plot3, "Capacité mAh", "GITT", "Coef diffusion", blue))
        plot_3.add_data_y1_Data(Data_array(array_y_plot3, "Dlit [cm\u00b2/s]", "GITT", "Coef diffusion", blue))

        """On passe l'axe des x pour le graph gitt général en heure"""
        for i in range(len(plot_1.data_x)):
            for j in range(len(plot_1.data_x[i].data)):
                plot_1.data_x[i].data[j] /= 3600

        """Pas besoin d'utiliser unique_name, les figures de GITT_data sont uniques"""

        plot_1.name = self.unique_name(plot_1.name)
        plot_2.name = self.unique_name(plot_2.name)
        plot_3.name = self.unique_name(plot_3.name)
        plot_controle.name = self.unique_name(plot_controle.name)

        return [plot_1, plot_2, plot_3, plot_controle]

    """----------------------------------------------------------------------------------"""

    @property
    def data(self):
        raise ValueError

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
        raise ValueError

    @name.setter
    def name(self, name):
        self._name = name

    @nom_cell.setter
    def nom_cell(self, name):
        self._nom_cell = name

    @figures.setter
    def figures(self, figures):
        print("Impossible d'utiliser le setter de figures de la class abstract data")
        raise ValueError

    @current_figure.setter
    def current_figure(self, figure):
        self._current_figure = figure

    @resource.setter
    def resource(self, resource):
        self._resource = resource

    @property
    def potentiel(self):
        return self._potentiel

    @property
    def pulse(self):
        return self._pulse

    @property
    def relaxation(self):
        return self._relaxation

    @potentiel.setter
    def potentiel(self, potentiel):
        self._potentiel = potentiel

    @pulse.setter
    def pulse(self, pulse):
        self._pulse = pulse

    @relaxation.setter
    def relaxation(self, relaxation):
        self._relaxation = relaxation