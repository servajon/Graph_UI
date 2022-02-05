from Console_Objets import Data_array


class Figure:
    def __init__(self, name, dirty=None):
        self._name_axes_x = ""
        self._name_axes_y1 = ""
        self._name_axes_y2 = ""
        self._name_axes_z1 = ""
        self._plot_name = ""

        self._type = None
        self._extra_type = None

        self._start_x = None
        self._end_x = None

        self._start_y1 = None
        self._end_y1 = None

        self._start_y2 = None
        self._end_y2 = None

        """[x, 5.2]
            [y1, 1000]"""
        self.norm = []

        """les array data_ stock des objet data, possedant un array de data, un nom et une source
        La source étant le nom du fichier de provenance de la data"""
        self._data_x = []
        self._data_y1 = []
        self._data_y2 = []
        self._data_z1 = []
        self._data_z2 = []

        self._name = name
        self._dirty = dirty

        self._nb_legende = 5
        self._format_ligne_y1 = None
        self._format_ligne_y2 = None
        self._marker_size = 4

        """Le zoom est en %, zoom = 10 correspond à un zoom de 10%, -10 à un dézoom de 10%
        On dézoom de 5% par défaut"""
        self._zoom = -5

        """SI la figure a était créer depuis une autre figure, on garde l'adresse pour l'afficher"""
        self._created_from = None

    """                                                  """
    """                      getter                      """
    """                                                  """

    @property
    def name_axes_x(self):
        if self._name_axes_x == "":
            if len(self._data_x) > 0:
                return self._data_x[0].name
            else:
                raise ValueError
        else:
            return self._name_axes_x

    @property
    def name_axes_y1(self):
        if self._name_axes_y1 == "":
            if len(self._data_y1) > 0:
                return self._data_y1[0].name
            else:
                raise ValueError
        else:
            return self._name_axes_y1

    @property
    def name_axes_y2(self):
        if self._name_axes_y2 == "":
            if len(self._data_y2) > 0:
                return self._data_y2[0].name
            else:
                raise ValueError
        else:
            return self._name_axes_y2

    @property
    def name_axes_z1(self):
        if self._name_axes_z1 == "":
            if len(self._data_z1) > 0:
                return self._data_z1[0].name
            else:
                raise ValueError
        else:
            return self._name_axes_z1

    @property
    def plot_name(self):
        if self._plot_name == "":
            return self._name
        else:
            return self._plot_name

    @property
    def start_x(self):
        return self._start_x

    @property
    def end_x(self):
        return self._end_x

    @property
    def start_y1(self):
        return self._start_y1

    @property
    def end_y1(self):
        return self._end_y1

    @property
    def start_y2(self):
        return self._start_y2

    @property
    def end_y2(self):
        return self._end_y2

    @property
    def data_x(self):
        return self._data_x

    @property
    def data_y1(self):
        return self._data_y1

    @property
    def data_y2(self):
        return self._data_y2

    @property
    def name(self):
        return self._name

    @property
    def dirty(self):
        return self._dirty

    @property
    def nb_legende(self):
        return self._nb_legende

    @property
    def format_line_y1(self):
        return self._format_ligne_y1

    @property
    def format_line_y2(self):
        return self._format_ligne_y2

    @property
    def marker_size(self):
        return self._marker_size

    @property
    def zoom(self):
        return self._zoom

    @property
    def type(self):
        return self._type

    @property
    def data_z1(self):
        return self._data_z1

    @property
    def data_z2(self):
        return self._data_z2

    @property
    def extra_type(self):
        return self._extra_type

    @property
    def created_from(self):
        return self._created_from

    """                                                  """
    """                      setter                      """
    """                                                  """

    @name_axes_x.setter
    def name_axes_x(self, name):
        self._name_axes_x = name

    @name_axes_y1.setter
    def name_axes_y1(self, name):
        self._name_axes_y1 = name

    @name_axes_y2.setter
    def name_axes_y2(self, name):
        self._name_axes_y2 = name

    @plot_name.setter
    def plot_name(self, name):
        self._plot_name = name

    @start_x.setter
    def start_x(self, num):
        if num is None:
            self._start_x = num
        else:
            self._start_x = float(num)

    @end_x.setter
    def end_x(self, num):
        if num is None:
            self._end_x = num
        else:
            self._end_x = float(num)

    @start_y1.setter
    def start_y1(self, num):
        if num is None:
            self._start_y1 = num
        else:
            self._start_y1 = float(num)

    @end_y1.setter
    def end_y1(self, num):
        if num is None:
            self._end_y1 = num
        else:
            self._end_y1 = float(num)

    @start_y2.setter
    def start_y2(self, num):
        if num is None:
            self._start_y2 = num
        else:
            self._start_y2 = float(num)

    @end_y2.setter
    def end_y2(self, num):
        if num is None:
            self._end_y2 = num
        else:
            self._end_y2 = float(num)

    @data_x.setter
    def data_x(self, data):
        self._data_x = data

    @data_y1.setter
    def data_y1(self, data):
        self._data_y1 = data

    @data_y2.setter
    def data_y2(self, data):
        self._data_y2 = data

    @name.setter
    def name(self, name):
        self._name = name

    @dirty.setter
    def dirty(self, dirty):
        self._dirty = dirty

    @nb_legende.setter
    def nb_legende(self, nb_legende):
        nb_legende = int(nb_legende)
        self._nb_legende = nb_legende

    @format_line_y1.setter
    def format_line_y1(self, format):
        self._format_ligne_y1 = format

    @format_line_y2.setter
    def format_line_y2(self, format):
        self._format_ligne_y2 = format

    @marker_size.setter
    def marker_size(self, num):
        num = int(num)
        self._marker_size = num

    @zoom.setter
    def zoom(self, zoom):
        self._zoom = zoom

    @type.setter
    def type(self, type):
        self._type = type

    @data_z1.setter
    def data_z1(self, data_z1):
        self._data_z1 = data_z1

    @data_z2.setter
    def data_z2(self, data_z2):
        self._data_z2 = data_z2

    @extra_type.setter
    def extra_type(self, extra_type):
        self._extra_type = extra_type

    @created_from.setter
    def created_from(self, created_form):
        self._created_from = created_form
    """                                                             """
    """                      methodes de class                      """
    """                                                             """

    """                                                                        """
    """                      methodes add vecteur de data                      """
    """                                                                        """

    def add_data_x(self, data_x, name,  source, legende=None):
        """créer un nouvelle Data_array et l'ajoute à data_x
        methode utilisable uniquement par le programme, elle ne sera pas déclancher pas un utilisateur"""
        data = Data_array(data_x, name, source, legende)
        self.data_x.append(data)

    """----------------------------------------------------------------------------------"""

    def add_data_x_Data(self, data):
        """ajoute un nouvelle Data_array à data_x
        methode utilisable uniquement par le programme, elle ne sera pas déclancher pas un utilisateur"""
        self.data_x.append(data)

    """----------------------------------------------------------------------------------"""

    def set_data_x(self, data_x, name,  source, legende=None):
        """clear l'ancien data_x, créer et ajoute un nouvel objet Data_array"""
        data = Data_array(data_x, name, source, legende)
        self.data_x = [data]

    """----------------------------------------------------------------------------------"""

    def add_data_y1(self, data_y, name,  source, legende=None, color=None, extra_legende=None):
        """créer et ajoute un nouvel objet Data_array à data_y1"""
        data = Data_array(data_y, name, source, legende, color, extra_legende)
        self.data_y1.append(data)

    """----------------------------------------------------------------------------------"""

    def add_data_y1_Data(self, data):
        """ajoute un nouvel objet Data_array à data_y1"""
        self.data_y1.append(data)

    """----------------------------------------------------------------------------------"""

    def add_data_y2(self, data_y, name,  source, legende=None, color=None, extra_legende=None):
        """créer et ajoute un nouvel objet Data_array à data_y2"""
        data = Data_array(data_y, name, source, legende, color, extra_legende)
        self.data_y2.append(data)

    """----------------------------------------------------------------------------------"""

    def add_data_y2_Data(self, data):
        """ajoute un nouvel objet Data_array à data_y2"""
        self.data_y2.append(data)

    """----------------------------------------------------------------------------------"""

    def add_data_z1(self, data_y, name,  source, legende=None, color=None, extra_legende=None):
        """créer et ajoute un nouvel objet Data_array à data_z1"""
        data = Data_array(data_y, name, source, legende, color, extra_legende)
        self.data_z1.append(data)

    """----------------------------------------------------------------------------------"""

    def add_data_z1_Data(self, data):
        """ajoute un nouvel objet Data_array à data_z1"""
        self.data_z1.append(data)

    """----------------------------------------------------------------------------------"""

    def add_data_z2(self, data_y, name,  source, legende=None, color=None, extra_legende=None):
        """créer et ajoute un nouvel objet Data_array à data_z2"""
        data = Data_array(data_y, name, source, legende, color, extra_legende)
        self.data_z2.append(data)

    """----------------------------------------------------------------------------------"""

    def add_data_z2_Data(self, data):
        """ajoute un nouvel objet Data_array à data_z2"""
        self.data_z2.append(data)

    """----------------------------------------------------------------------------------"""

    def get_info(self):
        """affiche les information de la figure, n'affiche rien si la figure est dirty"""
        if self.dirty is not None:
            print("Les données de cette figure ont été modifiées par le programme, elles n'ont pas de sens à être "
                  "affichées")

        if len(self.data_x) == 0:
            print("Données chargées en x : aucune")
        else:
            for i in range(len(self.data_x)):
                if self.data_x[i].name is not None:
                    if type(self.data_x[i].color) == type(str):
                        print("Données chargées en x : " + self.data_x[i].name + " couleur : " + self.data_x[i].color)
                    else:
                        print("Données chargées en x : " + self.data_x[i].name)
        if len(self.data_y1) == 0:
            print("Données chargées en y1 : aucune")
        else:
            for i in range(len(self.data_y1)):
                if self.data_y1[i].name is not None:
                    if type(self.data_y1[i].color) == type(str):
                        print("Données chargées en y1 : " + self.data_y1[i].name + " couleur : " + self.data_y1[i].color)
                    else:
                        print("Donnéss chargées en y1 : " + self.data_y1[i].name)

        if len(self.data_z1) == 0:
            print("Données chargées en z1 : aucune")
        else:
            for i in range(len(self.data_z1)):
                if self.data_z1[i].name is not None:
                    if type(self.data_z1[i].color) == type(str):
                        print("Données chargées en z1 : " + self.data_z1[i].name + " couleur : " + self.data_z1[i].color)
                    else:
                        print("Données chargées en z1 : " + self.data_z1[i].name)

        if len(self.data_y2) == 0:
            print("Données chargées en y2 : aucune")
        else:
            for i in range(len(self.data_y2)):
                if self.data_y2[i].name is not None:
                    if type(self.data_y2[i].color) == type(str):
                        print("Données chargées en y2 : " + self.data_y2[i].name + " couleur : " + self.data_y2[i].color)
                    else:
                        print("Données chargées en y2 : " + self.data_y2[i].name)

    """----------------------------------------------------------------------------------"""

    def is_data_set(self):
        """return 1 si la figure est correctself.resource.print_color("Figure invalide pour traiter les cycles", "fail") pour être affiché, 0 sinon"""
        if len(self.data_x) == 0 or len(self.data_y1) == 0:
            return 0
        else:
            return 1

    """----------------------------------------------------------------------------------"""

    def is_data_set_3d(self):
        """return 1 si la figure est correct pour être affiché, 0 sinon"""
        if (len(self.data_x) == 0 or len(self.data_y1) == 0 or len(self.data_z1) == 0) or len(self._data_y2) != 0:
            return 0
        else:
            return 1

    """----------------------------------------------------------------------------------"""

    def is_data_set_contour(self):
        """return 1 si la figure est correct pour être affiché, 0 sinon"""
        if len(self.data_x) == 0 or len(self.data_y1) == 0 or len(self.data_z1) == 0:
            return 0
        else:
            return 1

    """----------------------------------------------------------------------------------"""

    def is_data_set_bar(self):
        """return 1 si la figure est correct pour être affiché, 0 sinon"""
        if (len(self.data_x) == 0 or len(self.data_y1) == 0) or len(self._data_y2) != 0:
            return 0
        else:
            return 1

    """----------------------------------------------------------------------------------"""

    def is_interact(self):
        """return 1 si la figure est correct pour être interactive, 0 sinon"""
        if self.type == "3d" or self.type == "bar" or len(self._data_y2) != 0 or self.type == "contour"\
                or self.type == "res_saxs" or self.type == "res_waxs":
            return 0
        else:
            return 1

    """----------------------------------------------------------------------------------"""
