import copy

from Console_Objets.Data_Unit import Units
from Resources_file import Resources
import matplotlib.pyplot as pplot
import matplotlib.colors as mcolors


class Data_array:
    def __init__(self, data_unit, name, source, legende, color=None, **kwargs):
        # data : Data_unit
        self._data_unit = data_unit

        self._name = name
        """La source est le fichier de provenance de la data"""
        self._source = source

        if (legende is None or legende == "") and name != "LIGNE0":
            self._legend = name
        else:
            self._legend = legende

        self._color = color

        if data_unit.unit is None:
            self._unit = None
        else:
            self._unit = data_unit.unit

        # cette variable référence la position des donnée de self.data par rapport à l'intégralité
        # des données ne sera présente que sur data_array appartenant à X_axe
        self._global_index = []

        # détermine si ce data_array doit-être tracé ou non, par défault oui
        # cela ne sera modifié que pour un data_array d'un axe y1 ou y2, pas x
        self._visible = True

        # on garde un dict des argument apssé en plus, si il y a des infos
        # que l'on souhaite garder
        self.kwargs = kwargs

    def get_color_map(self):
        if self._color is None:
            return None
        else:
            color = Resources.COLOR_MAP[self._color]
            try:
                colors = pplot.get_cmap(color).colors
            except AttributeError:
                return pplot.cm.get_cmap(color)
            else:
                return mcolors.LinearSegmentedColormap.from_list(self._color, colors, N=256)

    def get_data(self):
        return self._data_unit.data

    def change_unit(self, unit):
        """
        si unit est de type str, on la converti en BasicUnit

        :param unit: str / BasicUnit
        :return:
        """
        # si unit est un str, on récupére l'unité correspondante
        # avec la class Units
        if isinstance(unit, str):
            units = Units()
            unit = units[unit]

        # on met à jours l'unité de self
        self.unit = unit

        # on convert les données
        self.data_unit.convert_to(unit)

    def copy(self):
        new_data_unit = self.data_unit.copy()

        new_data_array = Data_array(new_data_unit, self.name, self.source, self.legend)

        if new_data_unit.unit is None:
            new_data_array.unit = None
        else:
            new_data_array.unit = new_data_unit.unit

        new_data_array.color = self.color
        new_data_array.global_index = copy.copy(self.global_index)
        new_data_array.visible = self.visible

        return new_data_array

    """                                                  """
    """                      getter                      """
    """                                                  """

    @property
    def data_unit(self):
        return self._data_unit

    @property
    def name(self):
        if self.data_unit.unit is None:
            return self._name
        else:
            return self._name

    @property
    def source(self):
        return self._source

    @property
    def legend(self):
        return self._legend

    @property
    def color(self):
        if self._color is None:
            return None
        else:
            if isinstance(self._color, list):
                return self._color
            elif "#" in self._color:
                return self._color
            elif isinstance(self._color, tuple):
                return self._color
            else:
                color = Resources.COLOR_MAP[self._color]
                try:
                    temp = pplot.get_cmap(color).colors[0]
                except AttributeError:
                    return pplot.cm.get_cmap(color)(0.1)
                else:
                    return temp

    @property
    def unit(self):
        return self._unit

    @property
    def visible(self):
        return self._visible

    @property
    def global_index(self):
        return self._global_index

    @property
    def data(self):
        return self.data_unit.data

    """                                                  """
    """                      setter                      """
    """                                                  """

    @data_unit.setter
    def data_unit(self, data):
        self._data_unit = data

    @name.setter
    def name(self, name):
        self._name = name

    @source.setter
    def source(self, source):
        self._source = source

    @legend.setter
    def legend(self, legende):
        self._legend = legende

    @color.setter
    def color(self, color):
        if color is None or "#" in color or type(color) == tuple:
            self._color = color
        elif color not in Resources.COLOR_MAP:
            print(" @color.setter : couleur invalide")
            raise ValueError
        else:
            self._color = color

    @visible.setter
    def visible(self, bool):
        self._visible = bool

    @global_index.setter
    def global_index(self, global_index):
        self._global_index = global_index

    @unit.setter
    def unit(self, value):
        self._unit = value

    @data.setter
    def data(self, data):
        self.data_unit.data = data
