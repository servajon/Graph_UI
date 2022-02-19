from abc import ABC, abstractmethod

from PyQt5 import QtWidgets
from PyQt5.QtWidgets import QTreeWidgetItem


class Tree_widget(QtWidgets.QTreeWidget):
    """
    on override QTreeWidget pour y ajouter des methode servant à
    l'ajout de figures et fichiers. Cette class représente l'arbre
    "pysique", c'est l'objet qui gére l'affichage, len events etc

    En plus de cette arbre, un arbre "logique" est créée, il comportera
    la même structure que l'arbre phyqiue dont il dépends. Il servira a
    faciliter les calcules pour l'insersion de nouvelles figures.
    """

    def __init__(self, parent=None):
        super().__init__(parent)
        self.items = []

    """---------------------------------------------------------------------------------"""

    def add_data(self, type, name):
        """
        On ajoute la nouvelle data au tree

        :param type: type exp (cccv, cv, ...)
        :param name: nom du fichier de donnée
        :return: None
        """
        self.items.append(self.Conteneur_data(name))

        # on récupére le nom et le type d'expérience pour créer un nouvel item
        item = QTreeWidgetItem([name, type])

        # c'est toujours un top level item, une experience ne dépends de rien
        self.addTopLevelItem(item)

        # on place l'item comme le focus
        self.setCurrentItem(item)

    """---------------------------------------------------------------------------------"""

    def add_figure(self, figure, current_data_name):
        """
        on ajoute la figure au tree en fonction de _created_from de la figure

        :param figure: objet Figure
        :param current_data_name: nom de la data auquel appartient la figure, le premier parent
        :return: None
        """
        for i, item in enumerate(self.items):
            if item.name == current_data_name:

                # la figure ne dépends pas d'une autre, on l'ajoute juste
                if figure.created_from is None:
                    # la figure n'a pas était créée à partir d'une autre

                    # on crééer un nouvel objet Conteneur
                    new_item = self.Conteneur_figure(figure.name)

                    # on l'ajoute à l'objet Conteneur_data correspondant à current_data_name
                    item.append(new_item)

                    # on crééer un nouvel objet QTreeWidgetItem
                    item = QTreeWidgetItem([figure.name, "figure"])

                    # on ajoute l'item à la place correspondante
                    self.topLevelItem(i).addChild(item)

                    # on place le focus sur le dernier ajout
                    self.setCurrentItem(item)
                else:
                    # on créer un array qui liste les "origines" de la figure en parcourant récursivement
                    # created_from de la figure est de ses parents
                    array_created_from = []
                    self.get_array_created_from(figure, array_created_from)

                    # on créer un nouvel item
                    item = QTreeWidgetItem([figure.name, "figure"])

                    # on créer obj qui correspond à l'objet qui va parcourir l'arbre logique
                    obj = self.items[i]

                    # _item lui parcous l'arbre "physique"
                    _item = self.topLevelItem(i)
                    for i, name in enumerate(array_created_from):
                        # ou parcours l'arbre en utilisant les noms obtenus par get_array_created_from
                        obj, index = obj.get_child(name)
                        _item = _item.child(index)

                    # on est au bonne endroit de l'arbre logique et physique pour ajouter litem
                    # arbre logique
                    new_item = self.Conteneur_figure(figure.name)
                    obj.append(new_item)

                    # arbre pysique
                    _item.addChild(item)
                break

    """---------------------------------------------------------------------------------"""

    def get_array_created_from(self, figure, array_res):
        """
        créer un array contenant le nom des figure ayant servis à la création de la figure passé
        en paramétre. On parcours récursivement les parent de la figure.

        :param figure: figure sur laquel la recherche de parent est effectué
        :param array_res: array dans lequel on stock les noms
        :return: array contenant les toutes les figure .created_from de figure
                 si figure à été créée à aprtir de f2, f2 à partir de f3 et f3 à partir de f4 :
                 :return [f4.name, f3.name, f2.name]
        """

        if figure.created_from is not None:
            self.get_array_created_from(figure.created_from, array_res)
            array_res.append(figure.created_from.name)

    """---------------------------------------------------------------------------------"""

    def info(self):
        """
        affiche de maniére textuel les informations de l'arbre logique

        :return: None
        """
        for conteneur in self.items:
            conteneur.get_name(0)

    """---------------------------------------------------------------------------------"""

    class Conteneur(ABC):
        """
        class abstraite de qui vont hériter Conteneur_data et Conteneur_figure
        elle fournis les methode pour aider le parcours de l'arbre logique
        """

        def __init__(self, name):
            self.name = name

        @abstractmethod
        def get_child(self, name):
            """
            return l'index et la figure correspondant au nom donnée en
            paramètre, raise ValueError si elle n'est pas présente dans
            le conteneur

            :param name: non du chiel que l'on souhaite avoir
            :return: Figure, index

            :exception ValueError
            """
            pass

        @abstractmethod
        def get_name(self, nb_tab):
            """
            Methode utilisé pour l'affichage text de l'arbre logique, nb_tab
            est incrémenté à chaque fois que l'on passe à l'affichage d'un child

            :param nb_tab: nombre tabulation pour l'affichage
            :return: None
            """
            pass

        @abstractmethod
        def append(self, item):
            """
            en fonction de la class fille l'array du conteneur ne porte pas ne même nom,
            on utilise cette methode pour append un item au conteneur

            :param item: Conteneur_data, Conteneur_figure
            :return: None
            """
            pass

    class Conteneur_data(Conteneur):
        def __init__(self, name):
            super().__init__(name)

            # objet de la class Conteneur_figure
            self.figures_child = []

        def get_child(self, name):
            for i, figure in enumerate(self.figures_child):
                if figure.name == name:
                    return figure, i
            raise ValueError

        def get_name(self, nb_tab):
            str = ""
            for i in range(nb_tab):
                str += "\t"
            str += self.name
            print(str)
            for item in self.figures_child:
                item.get_name(nb_tab + 1)

        def append(self, item):
            self.figures_child.append(item)

    class Conteneur_figure(Conteneur):
        def __init__(self, name):
            super().__init__(name)

            # objet de la class Conteneur_figure
            self.figures_child = []

        def get_child(self, name):
            for i, figure in enumerate(self.figures_child):
                if figure.name == name:
                    return figure, i
            raise ValueError

        def get_name(self, nb_tab):
            str = ""
            for i in range(nb_tab):
                str += "\t"
            str += self.name
            print(str)
            for item in self.figures_child:
                item.get_name(nb_tab + 1)

        def append(self, item):
            self.figures_child.append(item)