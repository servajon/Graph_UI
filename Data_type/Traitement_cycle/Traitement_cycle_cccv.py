from Console_Objets.Data_array import Data_array
from Console_Objets.Figure import Figure
from Data_type.Traitement_cycle import Traitements_cycle_outils
import matplotlib.pyplot as pplot
from Resources import Resources


def potentio(loop_data, time_data, i_data, mode_data, format_time, cycle, color_arg=None):
    """Prends en paramètre les data des loop, du temps, i, mode et le format du temps des data courrantes
    Return une figure format time est soit h, min ou s, c'est une chaine de caractère"""
    resource = Resources.Resource_class()
    if cycle is None:
        cycle_start = None
        cycle = create_array_cycle_all_array(loop_data)
        print(cycle)
    else:
        for i in range(len(cycle)):
            cycle[i] = cycle[i] - 1
        cycle_start = 1

    new_figure = Figure("", 1)

    """Converssion vaux 1/60, 1, 60 en fonction du format du temps de l'axe time_data, 
    on veux un format en min à la fin"""
    if format_time == "h":
        conversion = 60
    elif format_time == "min":
        conversion = 1
    else:
        conversion = 1 / 60

    name = ""

    if color_arg is not None:
        if color_arg not in Resources.COLOR_MAP:
            resource.print_color(color_arg + " : couleur invalide", "fail")
            color_arg = None

    color_y1 = []

    if color_arg is not None:
        for i in range(len(cycle)):
            color_y1.append(Traitements_cycle_outils.create_array_color(pplot.cm.get_cmap(color_arg), len(cycle)))
    else:
        for i in range(len(cycle)):
            color_y1.append(Traitements_cycle_outils.create_array_color(None, len(cycle)))

    for i in range(len(cycle)):
        name += "_" + str(cycle[i] + 1)
        val_min = loop_data[i][0]
        val_max = loop_data[i][1]
        j = val_max

        try:
            color = color_y1[0][i]
        except (TypeError, IndexError):
            color = None

        """On parcours le vecteur dans l'autre sens, en général les mode 2, que l'on cherche sont en fin ou
        au milieu de fichier, boucle en moyenne moins longue"""

        while val_min < j:
            if mode_data[j] == 2:
                temp_x = []
                temp_y1 = []
                """Quand on a trouvé la région ou le mod est 2, on créer 2 nouveaux vecteur et on ajoute les
                données dans ces derniers"""
                while val_min < j and mode_data[j] == 2:
                    temp_x.append(time_data[j] * conversion)
                    temp_y1.append(i_data[j])
                    j -= 1

                temp_x.reverse()
                Traitements_cycle_outils.start_0(temp_x)

                temp_y1.reverse()

                new_figure.add_data_x_Data(Data_array(temp_x, "time/min", None, "cycle " + str(cycle[i] + 1)))
                new_figure.add_data_y1_Data(Data_array(temp_y1, "<I>/mA", None, "cycle " + str(cycle[i] + 1), color))

            else:
                j -= 1

    if cycle_start is None:
        new_figure.name = "potentio_all"
    else:
        new_figure.name = "potentio"

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
