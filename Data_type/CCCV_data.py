import copy

from Console_Objets.Figure import Figure
from Data_type.Abstract_data import Abstract_data
from Resources_file import Resources
from Data_type.Traitement_cycle import Traitements_cycle_outils, Traitement_cycle_cccv




class CCCV_data(Abstract_data):
    def __init__(self):
        super().__init__()

        self.__name__ = "cccv"

    """----------------------------------------------------------------------------------"""

    def get_operation_available(self):
        return ["capa", "potentio", "custom"]

    """----------------------------------------------------------------------------------"""

    def capa(self):
        if self.data["mass_electrode"] == -1:
            print("La masse de l'électrode lue dans le fichier est invalide")
            val = Resources.get_float("Merci de donner une valeur correct (mg) : >> ")
        else:
            print("La masse de l'électrode lue est : " + str(self.data["mass_electrode"]) + " mg")
            if Resources.get_rep_Y_N("Garder cette masse ? (y/n) >> ") == 0:
                val = Resources.get_float("Merci de donner une valeur (mg) : >> ")
            else:
                val = self.data["mass_electrode"]

        figure = Figure(self.nom_cell + " capa", 1)
        figure.type = "capa"

        nb_cycle = len(self.data["loop_data"])

        new_data_x1 = []
        new_data_x2 = []
        new_data_x3 = []

        new_data_y10 = []
        new_data_y11 = []
        new_data_y2 = []

        for i in range(nb_cycle):
            min = self.data["loop_data"][i][0]
            max = self.data["loop_data"][i][1]

            val_max_1 = 0
            val_max_2 = 0
            val_max_3 = 0

            for j in range(min, max + 1):
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

        """tricheur :/ """
        figure.y1_axe.first_val = 0
        figure.y2_axe.first_val = 40

        max = 0
        for i in new_data_y2:
            if i > max:
                max = i
        if max < 110:
            figure.y2_axe.last_val = 110
        else:
            figure.y2_axe.last_val = 140

        """On modifie le nom de la figure pour être sûr qu'il soit unique"""
        figure.name = self.unique_name(figure.name)
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
            min = self.data["loop_data"][i][0]
            max = self.data["loop_data"][i][1]

            val_max_non_p_charge = 0
            val_max_p_charge = 0
            val_max_non_p_decharge = 0
            val_max_p_decharge = 0

            val_max_charge = 0
            val_max_decharge = 0

            start_plateaux_charge = None
            start_plateaux_decharge = None

            """sah quel plaisir, tout ça pour 1 point de merde........"""

            mode_1_pass_charge = False
            mode_2_pass_charge = False
            mode_1_done_charge = False
            mode_2_done_charge = False

            mode_1_pass_decharge = False
            mode_2_pass_decharge = False
            mode_1_done_decharge = False
            mode_2_done_decharge = False

            for j in range(min, max + 1):
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
        figure_decharge.add_data_y1(copy.copy(val_max_non_p_v_decharge), "Specific capacity (mAh/g)", None, "capa Galvano")
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

        temp = "time/" + self.get_format_time()

        new_figure = Traitement_cycle_cccv.potentio(self.data.get("loop_data"),
                                                    self.data.get(temp), self.data.get(self.resource.I),
                                                    self.data.get(self.resource.mode), self.get_format_time(), cycle)

        """On modifie le nom de la figure pour être sûr qu'il soit unique"""

        if name is None:
            new_figure.name = self.unique_name(self.nom_cell + "_" + new_figure.name)
        else:
            new_figure.name = self.unique_name(self.nom_cell + "_cycle_" + name)

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