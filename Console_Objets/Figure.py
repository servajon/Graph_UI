import unicodedata

from Console_Objets.Axe import Axe
from Console_Objets.Data_Unit import Data_unit
from Console_Objets.Data_array import Data_array


class Figure:
    __TYPE = {
        "capa": ["shift x"],  # figure du traitement capa
        "potentio": ["derive", "shift x", "shift y"],  # figure du traitement potentio
        "bar": [],  # graph bar de la capa
        "custom_y1": ["derive", "cycle", "shift x", "shift y"],  # random figure avec uniquement quelque chose en y1
        "custom_y1_y2": ["derive", "cycle", "shift x"],  # random figure avec axe y1 ET y2
        "cycle_y1": ["derive", "shift x", "shift y"],   # figure issus d'un traitement de cycle avec quelque chose en y1
        "cycle_y1_y2": ["derive", "shift x"],   # figure issus d'un traitement de cycle avec quelque chose en y1 ET y2
        "derive_y1": ["shift x", "shift y", "derive"],  # figure issus d'une dérivée avec data en y1
        "derive_y1_y2": ["shift x", "derive"],  # figure issus d'une dérivée avec data en y1 ET y2
        "diffraction": ["cycle", "fit"],    # figure du traitement diffraction
        "diffraction_cycle": ["fit"],    # figure issus d'une selection de cycle d'une figure de diffraction
        "res_fitting_temperature": [],   # figure résultat d'un fit
        "res_fitting_temps": [],  # figure résultat d'un fit
        "contour": [],  # figure résultat d'un fit
        "saxs": [],
        "waxs": [],
    }

    def __init__(self, name, dirty=None, **kwarks):
        self.x_axe = None
        self.y1_axe = None
        self.y2_axe = None
        self.z1_axe = None

        self.__plot_name = ""
        self._type = None

        # pour la normalisation
        self.aspect = None

        # nom de la figure
        self._name = name

        # si la figure est dirty ou non
        self._dirty = dirty

        # nombre de légendes a afficher
        self._nb_legende = 5

        # format des 2dlines en y1
        self._format_ligne_y1 = None

        # format des 2dlines en y2
        self._format_ligne_y2 = None

        # taille des markers
        self._marker_size = 4

        # margin en %, 0 par défaut
        self._margin = 0

        # Si la figure a était créer depuis une autre figure, on garde l'adresse pour l'afficher
        self._created_from = None

        # information complémetaire de la figure contnue ici
        self.kwarks = kwarks

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
    def margin(self):
        return self._margin

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

    @margin.setter
    def margin(self, zoom):
        self._margin = zoom

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

    def add_data_x(self, data_x, name, source, legend=None):
        """
        On ajoute à l'axe x de la figure data_x. data_x est soit une list
        soit un objet Data_unit

        Dans le cas ou c'est une list, on créer l'objet Data_unit ici, son
        unité sera None

        Si c'est un ojbet data_unit on l'append juste
        Pas d'argument color pour l'axe x

        :param data_x: list / Data_unit
        :param name: Nom que l'on souhaite affichier comme nom par défaut de l'axe x
        :param source: fichier source dont les données proviennent
        :param legende: légende a afficher pour cette courbe
        :return: None
        """

        # créer l'axe x si il n'existe pas encore
        if self.x_axe is None:
            self.x_axe = Axe("x")
            self.x_axe.name = name

        # si data_x est une list, on créer un objet data_unit
        # son unité sera None, aucune conversion possible
        if not isinstance(data_x, Data_unit):
            data_x = Data_unit(data_x)

        # créer un objet Data_array et l'ajoute à l'axe
        data = Data_array(data_x, name, source, legend)

        """# on passe les unité de l'obj data_array comme étant celle de l'obj data_unit
        data.unit = data_x.unit"""

        # on ajoute l'ojet data_array
        self.x_axe.append(data)

    """----------------------------------------------------------------------------------"""

    def add_data_x_Data(self, data):
        """
        data est de type Data_array, on suppose ici que les unités sont
        correct

        :param data: Data_array
        :return: None
        """

        # créer l'axe x si il n'existe pas encore
        if self.x_axe is None:
            self.x_axe = Axe("x")
            self.x_axe.name = data.name

        # On ajoute l'objet data_array à l'axe x
        self.x_axe.append(data)

    """----------------------------------------------------------------------------------"""

    def set_data_x(self, data_x, name, source, legend=None):
        """
        On ajoute à l'axe x de la figure data_x. data_x est soit une list
        soit un objet Data_unit

        Dans le cas ou c'est une list, on créer l'objet Data_unit ici, son
        unité sera None

        l'objet Data_array sera ici le seul a être présent sur l'axe

        :param data_x: list / Data_unit
        :param name: Nom que l'on souhaite affichier comme nom par défaut de l'axe x
        :param source: fichier source dont les données proviennent
        :param legende: légende a afficher pour cette courbe
        :return: None
        """

        # pas d'argument color pour l'axe

        # créer l'axe x si il n'existe pas encore
        if self.x_axe is None:
            self.x_axe = Axe("x")
            self.x_axe.name = name

        # si data_x est une list, on créer un objet data_unit
        # son unité sera None, aucune conversion possible
        if not isinstance(data_x, Data_unit):
            data_x = Data_unit(data_x)

        # clear l'ancien data_x, créer et ajoute un nouvel objet Data_array
        self.x_axe.clear()

        # créer un objet Data_array et l'ajoute à l'axe
        data = Data_array(data_x, name, source, legend)

        """# on passe les unité de l'obj data_array comme étant celle de l'obj data_unit
        data.unit = data_x.unit"""

        self.x_axe.append(data)

    """----------------------------------------------------------------------------------"""

    def add_data_y1(self, data_y, name, source, legend=None, color=None):
        """
        On ajoute à l'axe y1 de la figure data_y. data_y est soit une list
        soit un objet Data_unit

        Dans le cas ou c'est une list, on créer l'objet Data_unit ici, son
        unité sera None

        Si c'est un ojbet data_unit on l'append juste

        :param data_y: list / Data_unit
        :param name: Nom que l'on souhaite affichier comme nom par défaut de l'axe x
        :param source: fichier source dont les données proviennent
        :param legende: légende a afficher pour cette courbe
        :return: None
        """

        # créer l'axe y1 si il n'existe pas encore
        if self.y1_axe is None:
            self.y1_axe = Axe("y1")
            self.y1_axe.name = name

        # si data_y est une list, on créer un objet data_unit
        # son unité sera None, aucune conversion possible
        if not isinstance(data_y, Data_unit):
            data_y = Data_unit(data_y)

        # créer un objet Data_array et l'ajoute à l'axe
        data = Data_array(data_y, name, source, legend, color)

        """# on passe les unité de l'obj data_array comme étant celle de l'obj data_unit
        data.unit = data_y.unit"""

        self.y1_axe.append(data)

    """----------------------------------------------------------------------------------"""

    def add_data_y1_Data(self, data):
        """
        data est de type Data_array, on suppose ici que les unités sont
        correct

        :param data: Data_array
        :return: None
        """

        # créer l'axe y1 si il n'existe pas encore
        if self.y1_axe is None:
            self.y1_axe = Axe("y1")
            self.y1_axe.name = data.name

        # ajoute un nouvel objet Data_array à data_y1
        self.y1_axe.append(data)

    """----------------------------------------------------------------------------------"""

    def add_data_y2(self, data_y, name, source, legende=None, color=None):
        """
        On ajoute à l'axe y2 de la figure data_y. data_y est soit une list
        soit un objet Data_unit

        Dans le cas ou c'est une list, on créer l'objet Data_unit ici, son
        unité sera None

        Si c'est un ojbet data_unit on l'append juste

        :param data_y: list / Data_unit
        :param name: Nom que l'on souhaite affichier comme nom par défaut de l'axe x
        :param source: fichier source dont les données proviennent
        :param legende: légende a afficher pour cette courbe
        :return: None
        """

        # créer l'axe y2 si il n'existe pas encore
        if self.y2_axe is None:
            self.y2_axe = Axe("y2")
            self.y2_axe.name = name

        # si data_y est une list, on créer un objet data_unit
        # son unité sera None, aucune conversion possible
        if not isinstance(data_y, Data_unit):
            data_y = Data_unit(data_y)

        # créer et ajoute un nouvel objet Data_array à data_y2
        data = Data_array(data_y, name, source, legende, color)

        """# on passe les unité de l'obj data_array comme étant celle de l'obj data_unit
        data.unit = data_y.unit"""

        self.y2_axe.append(data)

    """----------------------------------------------------------------------------------"""

    def add_data_y2_Data(self, data):
        """
        data est de type Data_array, on suppose ici que les unités sont
        correct

        :param data: Data_array
        :return: None
        """

        # créer l'axe y2 si il n'existe pas encore
        if self.y2_axe is None:
            self.y2_axe = Axe("y2")
            self.y2_axe.name = data.name

        # ajoute un nouvel objet Data_array à data_y2
        self.y2_axe.append(data)

    """----------------------------------------------------------------------------------"""

    def add_data_z1(self, data_z, name, source, legende=None):
        """
        On ajoute à l'axe z1 de la figure data_z. data_z est soit une list
        soit un objet Data_unit

        Dans le cas ou c'est une list, on créer l'objet Data_unit ici, son
        unité sera None

        Si c'est un ojbet data_unit on l'append juste

        :param data_z: list / Data_unit
        :param name: Nom que l'on souhaite affichier comme nom par défaut de l'axe x
        :param source: fichier source dont les données proviennent
        :param legende: légende a afficher pour cette courbe
        :return: None
        """

        # créer l'axe z1 si il n'existe pas encore
        if self.z1_axe is None:
            self.z1_axe = Axe("z1")
            self.z1_axe.name = name

        # si data_y est une list, on créer un objet data_unit
        # son unité sera None, aucune conversion possible
        if not isinstance(data_z, Data_unit):
            data_z = Data_unit(data_z)

        # créer et ajoute un nouvel objet Data_array à data_z1
        data = Data_array(data_z, name, source, legende)

        """# on passe les unité de l'obj data_array comme étant celle de l'obj data_unit
        data.unit = data_z.unit"""

        self.z1_axe.append(data)

    """----------------------------------------------------------------------------------"""

    def add_data_z1_Data(self, data):
        """
        data est de type Data_array, on suppose ici que les unités sont
        correct

        :param data: Data_array
        :return: None
        """

        # créer l'axe z1 si il n'existe pas encore
        if self.z1_axe is None:
            self.z1_axe = Axe("z1")
            self.z1_axe.name = data.name

        # ajoute un nouvel objet Data_array à data_z1
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
                        print(
                            "Données chargées en y1 : " + self.data_y1[i].name + " couleur : " + self.data_y1[i].color)
                    else:
                        print("Donnéss chargées en y1 : " + self.data_y1[i].name)

        if len(self.data_z1) == 0:
            print("Données chargées en z1 : aucune")
        else:
            for i in range(len(self.data_z1)):
                if self.data_z1[i].name is not None:
                    if type(self.data_z1[i].color) == type(str):
                        print(
                            "Données chargées en z1 : " + self.data_z1[i].name + " couleur : " + self.data_z1[i].color)
                    else:
                        print("Données chargées en z1 : " + self.data_z1[i].name)

        if len(self.data_y2) == 0:
            print("Données chargées en y2 : aucune")
        else:
            for i in range(len(self.data_y2)):
                if self.data_y2[i].name is not None:
                    if type(self.data_y2[i].color) == type(str):
                        print(
                            "Données chargées en y2 : " + self.data_y2[i].name + " couleur : " + self.data_y2[i].color)
                    else:
                        print("Données chargées en y2 : " + self.data_y2[i].name)

    """----------------------------------------------------------------------------------"""

    def is_data_set(self):
        if self.x_axe is None or self.y1_axe is None:
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
        if self.type == "3d" or self.type == "bar" or self.type == "contour" \
                or self.type == "res_saxs" or self.type == "res_waxs" or (self.y2_axe is not None and
                                                                          len(self.y2_axe) != 0):
            return 0
        else:
            return 1

    """----------------------------------------------------------------------------------"""

    def get_data_yaxe_i(self, index):
        """
        On return data_array y1 ou y2 en fonction de l'index donnée en paramètre
        C'est l'index d'un data_array y1

        :param index:
        :return: Data_array
        """
        if index >= len(self.y1_axe):
            return self.y2_axe.data[index - len(self.y1_axe.data)]
        else:
            return self.y1_axe.data[index]

    """----------------------------------------------------------------------------------"""

    def get_operation(self):
        """
        On return les oppération disponibles pour ce type de figure

        :return: list
        """
        return self.__TYPE[self.type]

    def copy(self):
        new_figure = Figure(self.name + "_copy", self.dirty)

        for att, value in self.__dict__.items():
            if not isinstance(value, Axe):
                new_figure.__setattr__(att, value)
            else:
                new_figure.__setattr__(att, value.copy())

        return new_figure

    """----------------------------------------------------------------------------------"""

    def export(self, path):
        len_max = 0
        """On récupére l'index du vecteur en x le plus grand"""
        for i in range(len(self.x_axe.data)):
            len_max = max(len_max, len(self.x_axe.data[i].data))

        file = open(path, "w")

        for i in range(len(self.y1_axe.data)):
            file.write(self.y1_axe.name_unit + "\t")
            file.write(self.x_axe.name_unit + "\t")

        if self.y2_axe is not None:
            for i in range(len(self.y2_axe.data)):
                file.write(self.y2_axe.name_unit + "\t")
                file.write(self.x_axe.name_unit + "\t")

        file.write("\n")

        for i in range(len_max):
            for j in range(len(self.y1_axe.data)):
                if i < len(self.y1_axe.data[j].data):
                    if self.y1_axe.data[j].legend is not None:
                        file.write(str(self.x_axe.data[j].data[i]) + "\t")
                        file.write(str(self.y1_axe.data[j].data[i]) + "\t")
                else:
                    file.write("\t")

            if self.y2_axe is not None:
                for j in range(len(self.y2_axe.data)):
                    if i < len(self.y2_axe.data[j].data):
                        if self.y2_axe.data[j].legend is not None:
                            file.write(str(self.x_axe.data[j].data[i]) + "\t")
                            file.write(str(self.y2_axe.data[j].data[i]) + "\t")
                    else:
                        file.write("\t")
            file.write("\n")
        file.close()
