

class Data_array:
    """extra_legende gére une légende que l'on veux concerver même quand il y a une tranformation et que la
    légende ne porte plus le nom de la data mais du cycle"""

    def __init__(self, data, name, source, legende, color=None, extra_legende=None):
        self._data = data
        self._name = name
        """La source est le fichier de provenance de la data"""
        self._source = source

        if (legende is None or legende == "") and name != "LIGNE0":
            self._legende = name
        else:
            self._legende = legende

        self._color = color
        self._extra_legende = extra_legende
        self._unite = None
        self.extra_info = None

    def get_color_map(self):
        if self._color is None:
            return None
        else:
            color = Resource.COLOR_MAP[self._color]
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
    def legende(self):
        return self._legende

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
                color = Resource.COLOR_MAP[self._color]
                try:
                    temp = pplot.get_cmap(color).colors[0]
                except AttributeError:
                    return pplot.cm.get_cmap(color)(0.1)
                else:
                    return temp

    @property
    def extra_legende(self):
        return self._extra_legende

    @property
    def extra_legende_affichage(self):
        if self._extra_legende is None:
            return ""
        else:
            return " / " + self._extra_legende

    @property
    def legende_affiche(self):
        if self._legende is None:
            return None
        elif self._extra_legende is None:
            return self._legende
        else:
            return self._legende + " / " + self._extra_legende

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

    @legende.setter
    def legende(self, legende):
        self._legende = legende

    @color.setter
    def color(self, color):
        if color not in Resource.COLOR_MAP:
            resource = Resource.Resource_class()
            resource.print_color(color + " : couleur invalide", "fail")
            raise ValueError
        else:
            self._color = color

    @extra_legende.setter
    def extra_legende(self, legende):
        self._extra_legende = legende

    @unite.setter
    def unite(self, unite):
        self._unite = unite

