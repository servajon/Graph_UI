from Console_Objets.Data_Unit import Units, Data_unit


class Console:
    _instance = None

    def __new__(cls):
        if cls._instance is None:
            cls._instance = super(Console, cls).__new__(cls)

            cls.datas = []
            cls.current_data = None


        return cls._instance

    """----------------------------------------------------------------------------------"""

    def add_data(self, data):
        """On ajoute le nouveau obj fichier à self.datas, on rends son nom unique et le place en fichier courant"""
        data.name = self.unique_name(data.name)
        self.current_data = data
        self.datas.append(data)

    """----------------------------------------------------------------------------------"""

    def unique_name(self, name):
        """Parcours le nom des datas enregistrées et regarde si le nom donné en paramettre est unique, si il ne
        l'est pas on renvoie le même nom avec (1), (2) etc, si le nom est unique on renvoie jsute le nom """
        if self.current_data is None:
            return name

        for i in self.datas:
            if i.name == name:
                """Si dans name il n'y a pas (*) à la fin, on apelle la fonction unique_name en ajoutant
                (1)"""
                if len(name) > 2 and name[len(name) - 3] != '(' and name[len(name) - 1] != ')':
                    name += "(1)"
                elif len(name) < 3:
                    name += "(1)"
                else:
                    num = int(name[len(name) - 2]) + 1
                    temp = "(" + str(num) + ")"
                    name = name[0:len(name) - 3] + temp
                self.unique_name(name)
        return name

    """----------------------------------------------------------------------------------"""

    def set_current_data_name(self, name):
        for data in self.datas:
            if data.name == name:
                self.current_data = data
                return
        raise ValueError

    """----------------------------------------------------------------------------------"""

    def get_info_data_all(self):
        for i in range(len(self.datas)):
            self.datas[i].get_info_data()
            print("\n----------------------------")

    """----------------------------------------------------------------------------------"""

    def create_data_unit(self, data_name, row_name):
        for data in self.datas:
            if data.name == data_name:
                units = Units()
                unit = units.get_unit(row_name)
                array = data.data[row_name]
                data_unit = Data_unit(array, unit)
                return data_unit
        raise ValueError

    """----------------------------------------------------------------------------------"""

    def create_dictioanaries_loop(self):
        """
        On créer le dictionnaire d'information utile pour la création de cycles
        pour le type de fichier en current_data

        :return: dictionnaire utilisable par les traitements de cycles
        """

        # on récupére la list des donnée que le traitement cycle du fichier de donnée va utiliser
        array = self.current_data.get_dics()

        data_get = {}
        for arg in array:
            data_get[arg] = {}
        data_get["vieillissement_info_data"] = {}

        # On regarde l'origine des différentes data de la figure qui va être traité
        # On récupére les information des loops et des modes sur les fichiers correspondant
        for i in self.current_data.current_figure.x_axe.data:
            if i.source not in data_get["loop_data"].keys():
                j = 0
                while j < len(self.datas) and i.source != self.datas[j].name:
                    j += 1
                if i.source != self.datas[j].name:
                    print("Fichier introuvable")
                    raise ValueError
                else:
                    for k in data_get.keys():
                        if type(self.datas[j]).__name__ == "Modulo_bat_vieillissement":
                            data_get[k][i.source] = self.datas[j].vieillissement.get(k)
                        else:
                            data_get[k][i.source] = self.datas[j].data.get(k)
                    if type(self.datas[j]).__name__ == "Modulo_bat_vieillissement":
                        data_get["vieillissement_info_data"][i.source] = self.datas[j].vieillissement_info_data
        print(data_get.keys())
        return data_get
