from Resources import Resources


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

    def __init__(self, type, unite=None):
        if type not in self.__TYPE:
            raise ValueError
        else:
            self.type = type
            self.scale = None
            self.__name = None

            """valeurs auquels l'axes commance et termine"""
            self.first_val = None
            self.last_val = None

            """unite : [temps, s] / [temp, min] / [potential, V] etc"""
            self.unite = unite

            self.data = []

            self.color_map = None

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

    def apply_color(self):
        """pour l'axe x et z1 les couleurs ne seront pas prisent en compte, je préfère les interdires"""
        if self.type == "x" or self.type == "z1":
            raise ValueError

        """On applique la color map au données de l'axe"""
        if self.color_map is not None:
            for i in range(len(self.data)):
                self.data[i].color = self.color_map(i / len(self.data))

    """----------------------------------------------------------------------------------"""

    def __len__(self):
        return len(self.data)

    """----------------------------------------------------------------------------------"""

    @property
    def name(self):
        if self.__name is None:
            self.__name = rename_axe(self.data[0].name)

        return self.__name

    @name.setter
    def name(self, _name):
        self.__name = _name


