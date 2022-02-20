from Resources_file import Resources


def rename_axe(name):
    resource = Resources.Resource_class()
    if name == "Ecell/V":
        return resource.Ecell_name_format
    elif name == "<I>/mA":
        return resource.I_format
    elif name == "time/h":
        return resource.time_h_format
    elif name == "time/s":
        return resource.time_s_format
    elif name == "time/min":
        return resource.time_min_format
    elif name == "Q_charge/mA.h":
        return resource.Q_charge_format
    elif name == "(Q-Qo)/mA.h derive":
        return "dQ / dE"
    elif name == "Ecell/V derive":
        return resource.Ecell_name_format
    else:
        return name


class Axe:
    __TYPE = ["x", "y1", "y2", "z1"]

    def __init__(self, type):
        if type not in self.__TYPE:
            raise ValueError
        else:
            self.type = type
            self.scale = None
            self.__name = None

            # valeurs auquels l'axes commance et termine
            self.first_val = None
            self.last_val = None

            # vecteur d'objet data_array
            self.data = []

            self._color_map = None

    """----------------------------------------------------------------------------------"""

    def append(self, _data):
        """pour l'axe x et z1 les couleurs ne seront pas prisent en compte, je préfère les interdires"""
        if (self.type == "x" or self.type == "z1") and _data.color is not None:
            raise ValueError

        self.data.append(_data)

    """----------------------------------------------------------------------------------"""

    def clear(self):
        self.data.clear()

    """----------------------------------------------------------------------------------"""

    def set_color_lines(self, color_name):
        """pour l'axe x et z1 les couleurs ne seront pas prisent en compte, je préfère les interdires"""
        if self.type == "x" or self.type == "z1":
            raise ValueError

        if color_name not in Resources.COLOR_MAP:
            raise ValueError
        else:
            self.color_map = Resources.get_color_map(color_name)

    """----------------------------------------------------------------------------------"""

    def apply_color(self, reverse=False):
        """pour l'axe x et z1 les couleurs ne seront pas prisent en compte, je préfère les interdires"""
        if self.type == "x" or self.type == "z1":
            raise ValueError

        # On applique la color map au données de l'axe
        if self.color_map is not None:
            array_color = Resources.create_array_color(self.color_map, len(self.data))
            if reverse:
                for i in reversed(range(len(self.data))):
                    self.data[i].color = array_color[i]
            else:

                for i in range(len(self.data)):
                    self.data[i].color = array_color[i]

    """----------------------------------------------------------------------------------"""

    def change_unit(self, new_unit):
        """
        si new_unit est de type str, la fonction data_array la convertira en BasicUnit

        :param new_unit: str ou BasicUnit
        :return: None
        """

        # on parcours les data_array et on update l'unité
        for data_array in self.data:
            data_array.change_unit(new_unit)

    """----------------------------------------------------------------------------------"""

    def __len__(self):
        return len(self.data)

    """----------------------------------------------------------------------------------"""

    @property
    def name(self):
        if self.__name is None:
            if self.data[0].unit is not None:
                return rename_axe(self.data[0].name)
            else:
                return rename_axe(self.data[0].name)
        else:
            if self.data[0].unit is not None:
                return self.__name
            else:
                return self.__name

    @property
    def name_unit(self):
        if self.__name is None:
            if self.data[0].unit is not None:
                return rename_axe(self.data[0].name) + " [" + self.data[0].unit.name + "]"
            else:
                return rename_axe(self.data[0].name)
        else:
            if self.data[0].unit is not None:
                return self.__name + " [" + self.data[0].unit.name + "]"
            else:
                return self.__name

    @property
    def color_map(self):
        return self._color_map

    @color_map.setter
    def color_map(self, _color_map):
        if type(_color_map) == str:
            self._color_map = Resources.get_color_map(_color_map)
        else:
            self._color_map = _color_map

    @name.setter
    def name(self, _name):
        self.__name = _name