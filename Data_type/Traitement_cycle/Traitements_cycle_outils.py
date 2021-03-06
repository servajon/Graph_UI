import matplotlib
import numpy as np


"""---------------------------------------------------------------------------------------------"""

def is_array_croissant(array):
    """   Return 0 sinon l'array n'est pas strictement croissant, 1 si il l'est
    Utilisé pour la création des cycle, si l'array est stictement croissant il faut le mettre à 0
    Pour la superposition des cycles
    Le temps est strictement croissnant => remiser à 0 pour la superposition
    Ecell ne l'est pas => pas besoin de remise à zero """
    i = 10
    """   Les pas se font de 10 en 10, pas besoin de check chaque point, si il n'est pas
    Croissant il reviendra à sont point de départ : 0 => 10 => 0
    Contrairement au temps par exemple : 0 => 20 """
    while i < len(array) and array[i - 10] < array[i]:
        i += 10
    if i >= len(array):
        return 1
    else:
        return 0


"""---------------------------------------------------------------------------------------------"""


def mode_del(array_x, array_y, global_index, val_min, val_max, mode_data, mode, centre=None):
    if mode_data is None:
        return [array_x, array_y, global_index]

    """Si le mode que l'on cherche a suprimer est au milieux du cycle, on return dans rien faire"""
    if mode_data[val_min] != mode and mode_data[val_max] != mode:
        # si la dernière valeur n'est pas celle que l'on cherche mais pas 1 non plus
        # on check si on ne tombe pas dessus avant le 1
        if mode_data[val_max] != 1:
            index = val_max
            while index > val_min and mode_data[index] != 1 and mode_data[index] != mode:
                index -= 1
            if index == val_min or mode_data[index] == 1:
                return [array_x, array_y, global_index]
            else:
                # print("cas celia")
                return [array_x, array_y, global_index]

    nb_avant_centre = 0
    array_return_x = []
    array_return_y = []
    global_index_return = []

    print(len(array_x))
    print(len(global_index))

    for i in range(len(array_x)):
        if mode_data[val_min + i] != mode:
            array_return_x.append(array_x[i])
            array_return_y.append(array_y[i])
            if global_index is not None:
                global_index_return.append(global_index[i])
        elif centre is not None:
            if i < centre:
                nb_avant_centre += 1

    """On return deux nouveaux array résultat"""
    if centre is None:
        return [array_return_x, array_return_y, global_index_return]

    else:
        return [array_return_x, array_return_y, global_index_return, nb_avant_centre]


"""---------------------------------------------------------------------------------------------"""


def mode_del_3d(array_x, array_y, array_z, val_min, val_max, mode_data, mode):
    if mode_data is None:
        return [array_x, array_y, array_z]
    """Si le mode que l'on cherche a suprimer est au milier du cycle, on return dans rien faire"""
    if mode_data[val_min] != mode and mode_data[val_max] != mode:
        return [array_x, array_y, array_z]

    """on suprime le mode mode, utilisé pour retirer les plateaux, correspondant au mode 2
    Mode_data sert à déterminer le mode de chaque point"""

    array_return_x = []
    array_return_y = []
    array_return_z = []
    for i in range(len(array_x)):
        if mode_data[val_min + i] != mode:
            array_return_x.append(array_x[i])
            array_return_y.append(array_y[i])
            array_return_z.append(array_z[i])

    """On return deux nouveaux array résultat"""
    return [array_return_x, array_return_y, array_return_z]


"""---------------------------------------------------------------------------------------------"""


def start_0(array):
    """Prends un vecteur en argument et le fait commencer à 0
    Utilisé pour superposé des donnée => time qui est croissant entre les cycles"""

    """Si array est strictement croissant on prends simplement la première valeur et on soustrait
    à tous les élements"""

    """Dans certain cas il est possible que l'on demande de normaliser un cycle vide
    Si le dernier cycle n'est pas complet et que l'on cherche a normaliser une décharge qui n'est pas
    présente"""
    if len(array) == 0:
        return
    if is_array_croissant(array) == 1:
        val_min = array[0]
    else:
        return

    for i in range(len(array)):
        array[i] = (array[i] - val_min)


"""---------------------------------------------------------------------------------------------"""


def degrade_color(c1, c2, mix=0):
    c1 = np.array(c1)
    c2 = np.array(c2)
    return matplotlib.colors.to_hex((1 - mix) * c1 + mix * c2)


"""---------------------------------------------------------------------------------------------"""


def fusion_legende(figure):
    source_y1 = []
    source_y2 = []
    for i in range(len(figure.data_y1)):
        if figure.data_y1[i].source not in source_y1:
            source_y1.append(figure.data_y1[i].source)

    for i in range(len(figure.data_y2)):
        if figure.data_y2[i].source not in source_y2:
            source_y2.append(figure.data_y2[i].source)

    for i in range(len(figure.data_y1)):
        if figure.data_y1[i].source in source_y1:
            if figure.data_y1[i].extra_legende is not None:
                figure.data_y1[i].legende = "cell " + figure.data_y1[i].extra_legende
            else:
                index = 0
                for j in reversed(range(len(figure.data_y1[i].legende))):
                    if figure.data_y1[i].legende[j] == "/":
                        index = j
                        break
                if index == 0:
                    figure.data_y1[i].legende = "unknown cell"
                else:
                    figure.data_y1[i].legende = figure.data_y1[i].legende[index + 2:] + " cell"
            source_y1.remove(figure.data_y1[i].source)
            figure.data_y1[i].extra_legende = None
        else:
            figure.data_y1[i].legende = None

    for i in range(len(figure.data_y2)):
        if figure.data_y2[i].source in source_y2:
            if figure.data_y2[i].extra_legende is not None:
                figure.data_y2[i].legende = figure.data_y2[i].extra_legende
            else:
                index = 0
                for j in reversed(range(len(figure.data_y1[i].legende))):
                    if figure.data_y2[i].legende[j] == "/":
                        index = j
                        break
                    if index == 0:
                        figure.data_y2[i].legende = "unknown cell"
                    else:
                        figure.data_y2[i].legende = figure.data_y2[i].legende[index + 2:] + " cell"
            source_y2.remove(figure.data_y2[i].source)
            figure.data_y2[i].extra_legende = None
        else:
            figure.data_y2[i].legende = None


"""---------------------------------------------------------------------------------------------"""


def get_vecteur_color(figure):
    color_y1 = []
    color_y2 = []

    for data in figure.data_y1:
        if data.color is not None:
            new_color = matplotlib.colors.to_rgba(data.color)
            color_y1.append(new_color)
        else:
            color_y1.append(None)
    for data in figure.data_y2:
        if data.color is not None:
            new_color = matplotlib.colors.to_rgba(data.color)
            color_y2.append(new_color)
        else:
            color_y2.append(None)
    return color_y1, color_y2


"""---------------------------------------------------------------------------------------------"""
