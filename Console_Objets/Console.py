class Console:
    def __init__(self):
        self.datas = []
        self.current_data = None

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
