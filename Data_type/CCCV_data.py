import copy
import scipy.signal

from Console_Objets.Data_array import Data_array
from Console_Objets.Figure import Figure
from Data_type.Abstract_data import Abstract_data
from Data_type.Traitement_cycle import Traitements_cycle_outils, Traitement_cycle_cccv


class CCCV_data(Abstract_data):
    def __init__(self):
        super().__init__()

        self.__name__ = "cccv"

    """----------------------------------------------------------------------------------"""
    """                                   Methode abstraite                              """
    """----------------------------------------------------------------------------------"""

    def get_operation_available(self):
        return ["capa", "potentio", "custom"]

    """----------------------------------------------------------------------------------"""

    def capa(self):
        """
        On créer les graphs de capa

        Pour le moment les axes contenant des unités mAh/g ont None comme unité, il
        faudra s'occuper des conversion par la suite

        :return: None
        """

        # on répére la masse de l'électode
        val = self.data["mass_electrode"]

        # on créer une nouvelle figure
        figure = Figure(self.nom_cell + " capa", 1)

        # avec le type capa
        figure.type = "capa"

        # on récupére le nombre de cycles
        nb_cycle = len(self.data["loop_data"])

        # déclaration des vecteurs pour les données
        new_data_x1 = []
        new_data_x2 = []
        new_data_x3 = []

        new_data_y10 = []
        new_data_y11 = []
        new_data_y2 = []

        # on parcours touts les cycles
        for i in range(nb_cycle):
            val_min = self.data["loop_data"][i][0]
            val_max = self.data["loop_data"][i][1]

            val_max_1 = 0
            val_max_2 = 0
            val_max_3 = 0

            for j in range(val_min, val_max + 1):
                if abs(self.data.get(self.resource.Q_charge)[j]) > val_max_1:
                    val_max_1 = abs(self.data.get(self.resource.Q_charge)[j])

                if abs(self.data.get(self.resource.Q_discharge)[j]) > val_max_2:
                    val_max_2 = abs(self.data.get(self.resource.Q_discharge)[j])

                if self.data.get(self.resource.Efficiency)[j] > val_max_3:
                    val_max_3 = self.data.get(self.resource.Efficiency)[j]

            new_data_x1.append(i)
            new_data_y10.append(val_max_1 / val * 1000)

            new_data_x2.append(i)
            new_data_y11.append(val_max_2 / val * 1000)

            new_data_x3.append(i)
            new_data_y2.append(val_max_3)

        figure.add_data_x(new_data_x1, "Cycle Number", None, None)
        figure.add_data_y1(new_data_y10, "Q_charge/mA.h", None, None)

        figure.add_data_x(new_data_x2, "Cycle Number", None, None)
        figure.add_data_y1(new_data_y11, "Q_discharge/mA.h", None, None)

        figure.add_data_x(new_data_x3, "Cycle Number", None, None)
        figure.add_data_y2(new_data_y2, "Coulombic Efficiency[%]", None, None)

        figure.name_axes_y1 = "Specific charge (mAh/g)"

        # tricheur :/
        # on change les valeurs de début et de fin de la figure
        figure.y1_axe.first_val = 0
        figure.y2_axe.first_val = 40


        val_max = max(new_data_y2)
        # on fait en sorte de cacher les valeurs abérentes
        if val_max < 110:
            figure.y2_axe.last_val = 110
        else:
            figure.y2_axe.last_val = 140

        # On modifie le nom de la figure pour être sûr qu'il soit unique
        figure.name = self.unique_name(figure.name)

        # on modifie les markers de la figure
        figure.format_line_y1 = 'x'
        figure.format_line_y2 = '>'
        figure.marker_size = 6

        if self.data.get("mode") is None:
            self.resource.print_color("ImpossibLe de tracer les graphs additionnels", "work")
            return [figure]

        figure_charge = Figure(self.nom_cell + " Capacity Delithiation", 1)
        figure_decharge = Figure(self.nom_cell + " Capacity Lithiation", 1)

        figure_charge.type = "bar"
        figure_decharge.type = "bar"

        figure_charge_pc = Figure(self.nom_cell + " Capacity Delithiation (%)", 1)
        figure_decharge_pc = Figure(self.nom_cell + " Capacity Lithiation (%)", 1)

        figure_charge_pc.type = "bar"
        figure_decharge_pc.type = "bar"

        fig_charge_x = []
        fig_decharge_x = []
        val_max_non_p_v_charge = []
        val_max_p_v_charge = []
        val_max_non_p_v_decharge = []
        val_max_p_v_decharge = []

        for i in range(nb_cycle):
            val_min = self.data["loop_data"][i][0]
            val_max = self.data["loop_data"][i][1]

            val_max_non_p_charge = 0
            val_max_p_charge = 0
            val_max_non_p_decharge = 0
            val_max_p_decharge = 0

            val_max_charge = 0
            val_max_decharge = 0

            start_plateaux_charge = None
            start_plateaux_decharge = None

            # sah quel plaisir, tout ça pour 1 point de merde........

            mode_1_pass_charge = False
            mode_2_pass_charge = False
            mode_1_done_charge = False
            mode_2_done_charge = False

            mode_1_pass_decharge = False
            mode_2_pass_decharge = False
            mode_1_done_decharge = False
            mode_2_done_decharge = False

            for j in range(val_min, val_max + 1):
                if self.data.get("mode")[j] == 1 and self.data.get(self.resource.Q_charge)[j] > val_max_charge:
                    if not mode_1_done_charge:
                        if mode_2_pass_charge:
                            mode_2_done_charge = True
                        mode_1_pass_charge = True
                        val_max_non_p_charge = self.data.get(self.resource.Q_charge)[j]
                        val_max_charge = val_max_non_p_charge

                if self.data.get("mode")[j] == 2 and self.data.get(self.resource.Q_charge)[j] > val_max_charge:
                    if start_plateaux_charge is None:
                        if not mode_2_done_charge:
                            if mode_1_pass_charge:
                                mode_1_done_charge = True
                            mode_2_pass_charge = True
                            start_plateaux_charge = self.data.get(self.resource.Q_charge)[j]
                            val_max_p_charge = self.data.get(self.resource.Q_charge)[j] - start_plateaux_charge
                            val_max_charge = val_max_p_charge
                    else:
                        if not mode_2_done_charge:
                            if mode_1_pass_charge:
                                mode_1_done_charge = True
                            mode_2_pass_charge = True
                            val_max_p_charge = self.data.get(self.resource.Q_charge)[j] - start_plateaux_charge
                            val_max_charge = val_max_p_charge

                if self.data.get("mode")[j] == 1 and self.data.get(self.resource.Q_discharge)[j] > val_max_decharge:
                    if not mode_1_done_decharge:
                        if mode_2_pass_decharge:
                            mode_2_done_decharge = True
                        mode_1_pass_decharge = True
                        val_max_non_p_decharge = self.data.get(self.resource.Q_discharge)[j]
                        val_max_decharge = val_max_non_p_decharge

                if self.data.get("mode")[j] == 2 and self.data.get(self.resource.Q_discharge)[j] > val_max_decharge:
                    if start_plateaux_decharge is None:
                        if not mode_2_done_decharge:
                            if mode_1_pass_decharge:
                                mode_1_done_decharge = True
                            mode_2_pass_decharge = True
                            start_plateaux_decharge = self.data.get(self.resource.Q_discharge)[j]
                            val_max_p_decharge = self.data.get(self.resource.Q_discharge)[j] - start_plateaux_decharge
                            val_max_decharge = val_max_p_decharge
                    else:
                        if not mode_2_done_decharge:
                            if mode_1_pass_decharge:
                                mode_1_done_decharge = True
                            mode_2_pass_decharge = True
                            val_max_p_decharge = self.data.get(self.resource.Q_discharge)[j] - start_plateaux_decharge
                            val_max_decharge = val_max_p_decharge

            fig_decharge_x.append(i)
            fig_charge_x.append(i)

            val_max_non_p_v_charge.append(val_max_non_p_charge / val * 1000)
            val_max_p_v_charge.append(val_max_p_charge / val * 1000)
            val_max_non_p_v_decharge.append(val_max_non_p_decharge / val * 1000)
            val_max_p_v_decharge.append(val_max_p_decharge / val * 1000)

        figure_charge.add_data_x(copy.copy(fig_charge_x), "Cycle Number", None, None)
        figure_charge.add_data_y1(copy.copy(val_max_non_p_v_charge), "Specific capacity (mAh/g)", None, "capa Galvano")
        figure_charge.add_data_y1(copy.copy(val_max_p_v_charge), "Specific capacity (mAh/g)", None, "capa potentio")

        figure_decharge.add_data_x(copy.copy(fig_decharge_x), "Cycle Number", None, None)
        figure_decharge.add_data_y1(copy.copy(val_max_non_p_v_decharge), "Specific capacity (mAh/g)", None,
                                    "capa Galvano")
        figure_decharge.add_data_y1(copy.copy(val_max_p_v_decharge), "Specific capacity (mAh/g)", None, "capa potentio")

        for i in range(len(val_max_non_p_v_charge)):
            if new_data_y10[i] == 0:
                val_max_non_p_v_charge[i] = 0
            else:
                val_max_non_p_v_charge[i] = val_max_non_p_v_charge[i] / new_data_y10[i] * 100
        for i in range(len(val_max_p_v_charge)):
            if new_data_y10[i] == 0:
                val_max_p_v_charge[i] = 0
            else:
                val_max_p_v_charge[i] = val_max_p_v_charge[i] / new_data_y10[i] * 100
        for i in range(len(val_max_non_p_v_decharge)):
            if new_data_y11[i] == 0:
                val_max_non_p_v_decharge[i] = 0
            else:
                val_max_non_p_v_decharge[i] = val_max_non_p_v_decharge[i] / new_data_y11[i] * 100
        for i in range(len(val_max_p_v_decharge)):
            if new_data_y11[i] == 0:
                val_max_p_v_decharge[i] = 0
            else:
                val_max_p_v_decharge[i] = val_max_p_v_decharge[i] / new_data_y11[i] * 100

        figure_charge_pc.add_data_x(fig_charge_x, "Cycle Number", None, None)
        figure_charge_pc.add_data_y1(val_max_non_p_v_charge, "Specific capacity (%)", None, "capa Galvano")
        figure_charge_pc.add_data_y1(val_max_p_v_charge, "Specific capacity (%)", None, "capa potentio")

        figure_decharge_pc.add_data_x(fig_decharge_x, "Cycle Number", None, None)
        figure_decharge_pc.add_data_y1(val_max_non_p_v_decharge, "Specific capacity (%)", None, "capa Galvano")
        figure_decharge_pc.add_data_y1(val_max_p_v_decharge, "Specific capacity (%)", None, "capa potentio")

        figure_charge_pc.name = self.unique_name(figure_charge_pc.name)
        figure_decharge_pc.name = self.unique_name(figure_decharge_pc.name)
        figure_charge.name = self.unique_name(figure_charge.name)
        figure_decharge.name = self.unique_name(figure_decharge.name)

        figure_charge_pc.y1_axe.first_val = 0
        figure_charge_pc.y1_axe.last_val = 110

        figure_decharge_pc.y1_axe.first_val = 0
        figure_decharge_pc.y1_axe.last_val = 110

        return [figure, figure_charge_pc, figure_decharge_pc, figure_charge, figure_decharge]

    """----------------------------------------------------------------------------------"""

    def potentio(self, cycle=None):
        if self.data.get("mode") is None:
            print("ImpossibLe de tracer le graphique potentio pour ce fichier")
            return None

        if cycle is not None and len(cycle) == 3 and cycle[1] == "to":
            name = str(cycle[0]) + "_to_" + str(cycle[2])
            cycle = Traitements_cycle_outils.create_cycle_to(cycle[0], cycle[2])
        else:
            name = None

        if self.return_create_cycle(cycle) is False:
            return None


        new_figure = Traitement_cycle_cccv.potentio(self.data.get("loop_data"),
                                                    self.data.get("time/h"), self.data.get(self.resource.I),
                                                    self.data.get(self.resource.mode), cycle)

        # On modifie le nom de la figure pour être sûr qu'il soit unique
        if name is None:
            new_figure.name = self.unique_name(self.nom_cell + "_" + new_figure.name)
        else:
            new_figure.name = self.unique_name(self.nom_cell + "_cycle_" + name)

        return new_figure

    """----------------------------------------------------------------------------------"""

    def derive(self, nb_point=None, window_length=None, polyorder=None):
        return self.derivation(nb_point, window_length, polyorder)

    """----------------------------------------------------------------------------------"""
    """                                   Methode de class                               """
    """----------------------------------------------------------------------------------"""

    def derivation(self, nb_point, window_length, polyorder):
        new_figure = Figure(self.current_figure.name + "_derive", 1)

        new_data_x = []
        new_data_x2 = []
        new_data_y1 = []
        new_data_y2 = []

        data_x = self.current_figure.x_axe.data
        data_y1 = self.current_figure.y1_axe.data

        if self.current_figure.y2_axe is not None:
            data_y2 = self.current_figure.y2_axe.data
        else:
            data_y2 = None

        for i in range(len(data_y1)):
            if nb_point is None:
                nb_point = len(data_y1[i].data)

            new_x, new_y = _derive_class(data_x[i].data, data_y1[i].data, nb_point, window_length, polyorder)
            new_data_x.append(new_x)
            new_data_y1.append(new_y)

        if data_y2 is not None:
            for i in range(len(data_y2)):
                if nb_point is None:
                    nb_point = len(data_y2[i].data)

                new_x, new_y = _derive_class(data_x[len(data_y1) + i].data, data_y2[i].data, nb_point,
                                             window_length, polyorder)
                new_data_x2.append(new_x)
                new_data_y2.append(new_y)

        if len(new_data_y2) == 0:
            new_figure.type = "derive_y1"
        else:
            new_figure.type = "derive_y1_y2"

        new_data_x += new_data_x2

        for i in range(len(new_data_y1)):
            new_figure.add_data_x_Data(Data_array(new_data_x[i], self.current_figure.x_axe.data[0].name + " derive",
                                                  self.current_figure.x_axe.data[0].source,
                                                  self.current_figure.x_axe.data[0].legend,
                                                  self.current_figure.x_axe.data[0].color))

            new_figure.add_data_y1_Data(Data_array(new_data_y1[i], self.current_figure.y1_axe.data[i].name + " derive",
                                                   self.current_figure.y1_axe.data[i].source,
                                                   self.current_figure.y1_axe.data[i].legend,
                                                   self.current_figure.y1_axe.data[i].color))

        for i in range(len(new_data_y2)):
            new_figure.add_data_x_Data(
                Data_array(new_data_x[len(new_data_y1) + i], self.current_figure.x_axe.data[0].name + " derive",
                           self.current_figure.data_x[0].source, self.current_figure.data_x[0].legend,
                           self.current_figure.data_x[0].color))

            new_figure.add_data_y2_Data(Data_array(new_data_y2[i], self.current_figure.y2_axe.data[i].name + " derive",
                                                   self.current_figure.y2_axe.data[i].source,
                                                   self.current_figure.y2_axe.data[i].legend,
                                                   self.current_figure.y2_axe.data[i].color))

        new_figure.format_line_y1 = 'x'
        new_figure.format_line_y2 = 'x'

        new_figure.created_from = self.current_figure

        new_figure.name = self.unique_name(new_figure.name)

        return new_figure

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

    """                                                  """
    """                      setter                      """
    """                                                  """

    @data.setter
    def data(self, data):
        self._data = data
        # self.create_unit_array()

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


""""----------------------------------------------------------------------------------"""


def _derive_class(x_object, y_object, nb_point, window_length=None, polyorder=None):
    delta_y_moyen = 0
    for i in range(1, len(y_object)):
        delta_y_moyen += abs(y_object[i - 1] - y_object[i])

    delta_y_moyen /= len(y_object) - 1

    pas = len(y_object) / nb_point * delta_y_moyen
    newx = []
    deriv = []
    index = 0
    while index < len(y_object):
        res_deriv = _derive_point(x_object, y_object, index, pas)
        if res_deriv is not None:
            if res_deriv[0] is not None:
                newx.append(res_deriv[1])
                deriv.append(res_deriv[0])
                index = res_deriv[2]
            else:
                index = res_deriv[2]
        else:
            break
    if window_length is not None and polyorder is not None:
        deriv = scipy.signal.savgol_filter(deriv, window_length, polyorder)

    return newx, deriv


def _derive_point(array_x, array_y, index, pas):
    start_index = index
    start = array_y[index]
    index += 1

    while index < len(array_y) and abs(array_y[index] - start) < pas:
        index += 1
    """pb aux borne quand index ne change pas ?, à voir"""
    if index >= len(array_y) or start_index == index:
        return None

    milieu_start_y = (array_y[start_index + 1] + array_y[start_index]) / 2
    milieu_end_y = (array_y[index - 1] + array_y[index]) / 2
    milieu_start_x = (array_x[start_index + 1] + array_x[start_index]) / 2
    milieu_end_x = (array_x[index - 1] + array_x[index]) / 2

    new_x = (milieu_end_x + milieu_start_x) / 2

    if milieu_end_x - milieu_start_x == 0:
        return [None, None, index]
    else:
        res1 = (milieu_end_y - milieu_start_y) / (milieu_end_x - milieu_start_x)

    if res1 > 50 or res1 < -50:
        return [None, None, index]
    """on return le résulatat de la dérivé et le nouvelle index, qui garde trace du
    nombre de points que l'on a du avancé pour effectuer le pas"""

    """Ligne dégueu pour faire le miror quand on dériv Q-Qo, & voir si ça ne fait pas de la merde par la suite"""
    if array_x[index] - array_x[start_index] < 0:
        return [-res1, new_x, index]
    else:
        return [res1, new_x, index]
