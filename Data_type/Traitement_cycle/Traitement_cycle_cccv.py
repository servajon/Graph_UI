from Console_Objets.Data_array import Data_array
from Console_Objets.Figure import Figure
from Data_type.Traitement_cycle import Traitements_cycle_outils


def potentio(loop_data, time_data, i_data, mode_data, cycle):
    """
    Prends en paramètre les data des loop, du temps, i, mode et le format du temps des data courrantes
    Return une figure format time est soit h, min ou s, c'est une chaine de caractère


    :param loop_data: information sur les loops du fichier dont proviennent les datas
    :param time_data: vecteur du temps
    :param i_data: vecteur courrant
    :param mode_data: vacteur de mode
    :param cycle: None : tous les cycle, un vecteur d'int ou int1 to int2
    :param color_arg: nom de la color map
    :return: la nouvelle figure créée
    """

    # si cycle est None c'est qu'il faut tracer tous les cycles, on créer le vecteur
    if cycle is None:
        cycle_start = None
        cycle = create_array_cycle_all_array(loop_data)
    else:
        # on réindex les cycle, dans les données ils commencent à 0 non pas à 1
        for i in range(len(cycle)):
            cycle[i] = cycle[i] - 1
        cycle_start = 1

    # on créer une nouvelle figure
    new_figure = Figure("", 1)

    new_figure.type = "cycle"

    # variable name qui évoluera en fonction des cycles tracés
    name = ""

    # on parcours le vecteur de cycle
    for i in range(len(cycle)):

        # update du nom
        name += "_" + str(cycle[i] + 1)

        # on récupére l'index de début et de fin du cycle avec loop_data
        val_min = loop_data[cycle[i]][0]
        val_max = loop_data[cycle[i]][1]

        j = val_min
        # on cherche quand mode vaut 2
        while j < val_max:
            if mode_data[j] == 2:
                temp_x = []
                temp_y1 = []

                # on créer le vectuer global index pour l'affichage des valeurs
                global_index = []

                # Quand on a trouvé la région ou le mod est 2, on créer 2 nouveaux vecteur et on ajoute les
                # données dans ces derniers
                while j < val_max and mode_data[j] == 2:
                    temp_x.append(time_data[j])
                    temp_y1.append(i_data[j])
                    global_index.append(j)
                    j += 1

                # on normalise le vecteur à 0
                Traitements_cycle_outils.start_0(temp_x)

                # on créer data array_x
                data_array_x = Data_array(temp_x, "time/min", None, "cycle " + str(cycle[i] + 1))

                # on lui ajoute global index
                data_array_x.global_index = global_index

                # on ajoute data_array à new_figure
                new_figure.add_data_x_Data(data_array_x)
                # on ajoute data_array à new_figure
                new_figure.add_data_y1_Data(Data_array(temp_y1, "<I>/mA", None, "cycle " + str(cycle[i] + 1)))

            else:
                j += 1

    # on rename la figure en fonction de si la commande était all
    if cycle_start is None:
        new_figure.name = "potentio_all"
    else:
        new_figure.name = "potentio" + name

    # on return la figure
    return new_figure


"""---------------------------------------------------------------------------------------------"""

"""                     Ensuite se trouve toutes les fonctions outils                           """

"""---------------------------------------------------------------------------------------------"""


def create_array_cycle_all_array(loop_data):
    """array en input et return un vecteur avec les loop dedans"""
    array_return = []
    for i in range(len(loop_data)):
        array_return.append(i)
    return array_return
