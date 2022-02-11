from Console_Objets.Axe import Axe
from Console_Objets.Data_array import Data_array


class Figure:
    def __init__(self, name, dirty=None):
        self.x_axe = None
        self.y1_axe = None
        self.y2_axe = None
        self.z1_axe = None

        self.__plot_name = ""
        self._type = {}

        """pour la normalisation"""
        self.aspect = None

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
    def plot_name(self):
        if self.__plot_name == "":
            return self._name
        else:
            return self.__plot_name

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
    def created_from(self):
        return self._created_from

    """                                                  """
    """                      setter                      """
    """                                                  """

    @plot_name.setter
    def plot_name(self, _plot_name):
        self.__plot_name = _plot_name

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
        """créer l'axe x si il n'existe pas encore"""
        if self.x_axe is None:
            self.x_axe = Axe("x")

        """créer un objet Data_array et l'ajoute à l'axe"""
        data = Data_array(data_x, name, source, legende)
        self.x_axe.append(data)

    """----------------------------------------------------------------------------------"""

    def add_data_x_Data(self, data):
        """créer l'axe x si il n'existe pas encore"""
        if self.x_axe is None:
            self.x_axe = Axe("x")

        """On ajoute l'objet data_array à l'axe x"""
        self.x_axe.append(data)

    """----------------------------------------------------------------------------------"""

    def set_data_x(self, data_x, name,  source, legende=None):
        """pas d'argument color pour l'axe"""

        """créer l'axe x si il n'existe pas encore"""
        if self.x_axe is None:
            self.x_axe = Axe("x")

        """clear l'ancien data_x, créer et ajoute un nouvel objet Data_array"""
        self.x_axe.clear()

        """créer un objet Data_array et l'ajoute à l'axe"""
        data = Data_array(data_x, name, source, legende)
        self.x_axe.append(data)

    """----------------------------------------------------------------------------------"""

    def add_data_y1(self, data_y, name,  source, legende=None, color=None):
        """créer l'axe y1 si il n'existe pas encore"""
        if self.y1_axe is None:
            self.y1_axe = Axe("y1")

        """créer un objet Data_array et l'ajoute à l'axe"""
        data = Data_array(data_y, name, source, legende, color)
        self.y1_axe.append(data)

    """----------------------------------------------------------------------------------"""

    def add_data_y1_Data(self, data):
        """créer l'axe y1 si il n'existe pas encore"""
        if self.y1_axe is None:
            self.y1_axe = Axe("y1")

        """ajoute un nouvel objet Data_array à data_y1"""
        self.y1_axe.append(data)

        if self.x_axe is not None and len(self.y1_axe) != len(self.x_axe):
            self.x_axe.append(self.x_axe[-1])

    """----------------------------------------------------------------------------------"""

    def add_data_y2(self, data_y, name,  source, legende=None, color=None):
        """créer l'axe y2 si il n'existe pas encore"""
        if self.y2_axe is None:
            self.y2_axe = Axe("y2")

        """créer et ajoute un nouvel objet Data_array à data_y2"""
        data = Data_array(data_y, name, source, legende, color)
        self.y2_axe.append(data)

    """----------------------------------------------------------------------------------"""

    def add_data_y2_Data(self, data):
        """créer l'axe y2 si il n'existe pas encore"""
        if self.y2_axe is None:
            self.y2_axe = Axe("y2")

        """ajoute un nouvel objet Data_array à data_y2"""
        self.y2_axe.append(data)

    """----------------------------------------------------------------------------------"""

    def add_data_z1(self, data_y, name,  source, legende=None):
        """créer l'axe z1 si il n'existe pas encore"""
        if self.z1_axe is None:
            self.z1_axe = Axe("z1")

        """créer et ajoute un nouvel objet Data_array à data_z1"""
        data = Data_array(data_y, name, source, legende)
        self.z1_axe.append(data)

    """----------------------------------------------------------------------------------"""

    def add_data_z1_Data(self, data):
        """créer l'axe z1 si il n'existe pas encore"""
        if self.z1_axe is None:
            self.z1_axe = Axe("z1")

        """ajoute un nouvel objet Data_array à data_z1"""
        self.z1_axe.append(data)

    """----------------------------------------------------------------------------------"""

    def get_info(self):
        print("a réécrire")
        return

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
        if len(self.x_axe) == 0 or len(self.y1_axe) == 0:
            return 0
        else:
            return 1

    """----------------------------------------------------------------------------------"""

    def is_data_set_3d(self):
        """return 1 si la figure est correct pour être affiché, 0 sinon"""
        if (len(self.x_axe) == 0 or len(self.y1_axe) == 0 or len(self.z1_axe) == 0) or len(self.y2_axe) != 0:
            return 0
        else:
            return 1

    """----------------------------------------------------------------------------------"""

    def is_data_set_contour(self):
        """return 1 si la figure est correct pour être affiché, 0 sinon"""
        if len(self.x_axe) == 0 or len(self.y1_axe) == 0 or len(self.z1_axe) == 0:
            return 0
        else:
            return 1

    """----------------------------------------------------------------------------------"""

    def is_data_set_bar(self):
        """return 1 si la figure est correct pour être affiché, 0 sinon"""
        if self.x_axe is None and self.y1_axe is None:
            return 0
        else:
            if len(self.x_axe) == 0 or len(self.y1_axe) == 0 or self.y2_axe is not None:
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

    def format_x_axe(self):
        """on ajoute les data_array manquant à l'axe x
        si ils sont manquant c'est que la figure a été faire par l'utilisateur"""
        if self.y2_axe is None:
            while len(self.x_axe) != len(self.y1_axe):
                self.x_axe.append(self.x_axe.data[0])
        else:
            while len(self.x_axe) != len(self.y1_axe) + len(self.y2_axe):
                self.x_axe.append(self.x_axe.data[-1])
