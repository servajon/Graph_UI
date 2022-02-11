from Resources import Resources
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
    def unite(self):
        return self._unite

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
        if color not in Resources.COLOR_MAP:
            resource = Resources.Resource_class()
            resource.print_color(color + " : couleur invalide", "fail")
            raise ValueError
        else:
            self._color = color


