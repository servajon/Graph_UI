from Resources_file import Resources
import matplotlib.pyplot as pplot
import matplotlib.colors as mcolors


class Data_array:
    """extra_legende gére une légende que l'on veux concerver même quand il y a une tranformation et que la
    légende ne porte plus le nom de la data mais du cycle"""

    def __init__(self, data, name, source, legende, color=None):
        self._data = data

        self._name = name
        """La source est le fichier de provenance de la data"""
        self._source = source

        if (legende is None or legende == "") and name != "LIGNE0":
            self._legend = name
        else:
            self._legend = legende

        self._color = color
        self._unite = None
        self.extra_info = None

        # cette variable référence la position des donnée de self.data par rapport à l'intégralité
        # des données ne sera présente que sur data_array appartenant à X_axe
        self._global_index = []

        # détermine si ce data_array doit-être tracé ou non, par défault oui
        # cela ne sera modifié que pour un data_array d'un axe y1 ou y2, pas x
        self._visible = True

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
        return self._unite

    @property
    def visible(self):
        return self._visible

    @property
    def global_index(self):
        return self._global_index

    """                                                  """
    """                      setter                      """
    """                                                  """

    @data.setter
    def data(self, data):
        self._data = data

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

