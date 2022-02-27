from abc import ABC

from Console_Objets.Data_Unit import Units, Data_unit
from Console_Objets.Data_array import Data_array
from Console_Objets.Figure import Figure
from Data_type.Abstract_data import Abstract_data
from Data_type.Traitement_cycle import Traitement_cycle_diffraction


class Diffraction_data(Abstract_data):
    def __init__(self):
        super().__init__()

        self.__name__ = "diffraction"
        self.res_calc = []

    def get_operation_available(self):
        return ["Diffraction", "Contour"]

    def create_diffraction(self):
        """
        Création du graph de diffraction

        :return: nouvelle figure
        """

        """start = self.data["2t"][self.data["loop_data"][0][0]]
        end = self.data["2t"][self.data["loop_data"][0][1]]"""

        """t_start = None
        while t_start is None:
            t_start = Resource.get_float("Start x ? >> ")
            if t_start > end or t_start < start:
                self.resource.print_color("Valeur invalide, doit être comprise entre "
                                          + str(start) + " et " + str(end), "fail")
                t_start = None"""

        figure = Figure("diffraction")
        figure.type = "diffraction"
        figure.plot_name = "Diffraction"

        units = Units()
        unit_x = units["degrees"]
        unit_y = units["ua"]

        for i in range(len(self.data["loop_data"])):

            start = self.data["loop_data"][i][0]
            end = self.data["loop_data"][i][1]

            global_index = [val for val in range(start, end)]
            temp_x = self.data["2t"][start:end]
            temp_y = self.data["intensite"][start:end]

            # calcule d'une ligne de base clodo, à refaire
            """calc = (self.data["intensite"][end] - self.data["intensite"][start]) / 
                   (self.data["2t"][end] - self.data["2t"][start])
            _minus = self.data["intensite"][start]"""

            """for j in range(len(temp_x)):
                temp_y[j] -= temp_x[j] * calc + _minus"""

            data_unit_x = Data_unit(temp_x, unit_x)
            data_unit_y = Data_unit(temp_y, unit_y)

            d1 = Data_array(data_unit_x, "2 θ", self.name, "cycle " + str(self.data["loop_data"][i][3]))
            d2 = Data_array(data_unit_y, "Unité arbitraire", self.name, "temperature " + str(self.data["loop_data"][i][3]))

            d1.global_index = global_index
            d2.global_index = global_index

            figure.add_data_x_Data(d1)
            figure.add_data_y1_Data(d2)

        figure.name = self.unique_name(figure.name)

        return figure

    def capa(self):
        raise ValueError

    def potentio(self, cycle):
        raise ValueError

    def derive(self, *args, **kwargs):
        pass

    def shift_axe(self, *args, **kwargs):
        pass

    """----------------------------------------------------------------------------------"""

    def create_figure_cycle(self, *args, **kwargs):
        """
       La création de cycle passe par cette methode, en fonction du type de cycle
       on appelle la methode de création correspondante

       :param args:
       :param kwargs:
       :return:
        """

        cycle = kwargs["cycles"]

        # on créer le nom de la figure
        if cycle is not None and len(cycle) == 3 and cycle[1] == "to":
            name = str(cycle[0]) + "_to_" + str(cycle[2])
        elif cycle is None:
            name = "all"
        else:
            s = ""
            for i in cycle:
                s += str(i) + " "
            name = s[0:-1]

        cycle = self.return_create_cycle(cycle)

        if cycle is None:
            return

        figure = self.cycle(cycle)

        # On modifie le nom de la figure pour être sûr qu'il soit unique
        if isinstance(figure, list):
            for f in figure:
                f.name = self.unique_name(self.nom_cell + " cycle " + name + f.name)
        else:
            figure.name = self.unique_name(self.nom_cell + " cycle " + name + figure.name)

        return figure

    """----------------------------------------------------------------------------------"""

    def cycle(self, cycle):
        return Traitement_cycle_diffraction.cycle_diffraction(self.current_figure, cycle)

    """----------------------------------------------------------------------------------"""

    def get_dics(self):
        return ["loop_data"]

    """----------------------------------------------------------------------------------"""

    def get_cycle_available(self):
        return ["Cycle"]

    """----------------------------------------------------------------------------------"""

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


