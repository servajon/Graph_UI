import os
import textwrap
from os import listdir
import matplotlib
import matplotlib.colors as mcolors

class Resource_class:
    _instance = None

    def __new__(cls):
        if cls._instance is None:
            cls._instance = super(Resource_class, cls).__new__(cls)
            cls.Ecell_name = "Ecell/V"
            cls.Q_charge = "Q_charge/mA.h"
            cls.Q_discharge = "Q_discharge/mA.h"
            cls.Efficiency = "Efficiency/%"
            cls.mode = "mode"
            cls.I = "<I>/mA"
            cls.freq = "freq/Hz"
            cls.time = "time/s"

            cls.Ecell_name_format = u"Potential [V] vs Li\u207A/Li"
            cls.Q_charge_format = "Specific Charge [mAh/g]"
            cls.Q_discharge_format = "Q_discharge/mA.h"
            cls.Efficiency_format = "Efficiency/%"
            cls.I_format = "Current [mA]"
            cls.time_h_format = "Time [h]"
            cls.time_min_format = "Time [min]"
            cls.time_s_format = "Time [s]"

            # taille par défaut de l'écriture dans le widget console
            cls.default_size = 10
            cls.default_font = ("Times", cls.default_size)



        return cls._instance


"""----------------------------------------------------------------------------------"""


def justify(s, width=80):
    """Code repris de cerium50, https://openclassrooms.com/forum/sujet/justifier-un-texte-avec-python-44256"""
    """J'ai juste modifier un tout petit truc pour que la dernière ligne ne soit pas justifié, donc absolument rien"""
    """Ce code me sert pour afficher mes textes d'explication de commande, merci à cette personne pour le partage :)"""
    lines = textwrap.wrap(s, width)
    newlines = []
    for i in range(len(lines)):
        line = lines[i].split()
        spaces = width - sum(map(len, line))
        remaining = len(line)
        newlines.append([])

        if i == len(lines) - 1:
            for w in line:
                newlines[-1].append(w)
                newlines[-1].append(' ')
        else:
            for w in line[:-2]:
                newlines[-1].append(w)
                n = round(spaces / remaining)
                newlines[-1].append(' ' * n)
                spaces -= n
                remaining -= 1

            if len(line) >= 2:
                newlines[-1].append(' ' * (spaces // 2))
                newlines[-1].append(line[-2])
                spaces -= spaces // 2
                newlines[-1].append(' ' * spaces)
            newlines[-1].append(line[-1])

    return '\n'.join(map(''.join, newlines))


"""----------------------------------------------------------------------------------"""


def space_to_(input):
    """prends en paramètre un string et remplace les espace par '_'"""
    if input is None:
        raise ValueError

    temp = ""
    for i in range(len(input)):
        if input[i] == " ":
            temp += "_"
        else:
            temp += input[i]
    return temp


"""----------------------------------------------------------------------------------"""


def get_rep_Y_N(text):
    """Prends en paramètre un string, l'écrit dans un input et tourne en boucle tant que
    l'utilisateur n'a pas répondu oui / non, et return la réponse, 1 pour oui, 0 sinon"""
    while 1 < 2:
        rep = input(text)
        rep = rep.lower()
        if rep == "oui" or rep == "y" or rep == "yes":
            return 1
        elif rep == "non" or rep == "n" or rep == "no":
            return 0


"""----------------------------------------------------------------------------------"""


def get_param(commande):
    """"Prends en paramètre une commande et return un array constituer de chaque mot
    Un mot est séparer d'un espace
    On retire gitt / cccv / cv du vecteur"""
    arg = []
    temp = ''
    for i in range(len(commande)):
        if commande[i] == ' ':
            if temp != ' ' and temp != '':
                arg.append(temp)
                temp = ''

        else:
            temp += commande[i]

    if temp != '' and temp != ' ':
        arg.append(temp)
    if len(arg) == 0:
        arg.append('')
    return arg


"""----------------------------------------------------------------------------------"""


def get_float(str):
    number = None
    while number is None:
        number = input(str)
        number = number.replace(',', '.')
        try:
            number = float(number)
        except ValueError:
            print("Un nombre est demandé")
            number = None
    return number


"""----------------------------------------------------------------------------------"""


def get_int(str):
    number = None
    while number is None:
        number = input(str)
        try:
            number = float(number)
            if number != int(number):
                print("Un entier est demandé")
                number = None
        except ValueError:
            print("Un nombre est demandé")
            number = None
    return int(number)


"""----------------------------------------------------------------------------------"""


def get_rep(str, array):
    rep = None
    while rep is None:
        rep = input(str)
        if rep not in array:
            print("La réponse donnée ne correspond pas à celle attendu")
            rep = None
    return rep


"""----------------------------------------------------------------------------------"""


def coord_to_point(coords, data_x, data_y):
    """Il récupére self.coords et return l'index du vecteur en x correspondant au point le plus proche de
        self.coords, return -1 si erreur"""
    """les bornes sont donnée arbitraierement, à voir si ça pose problème plus tard"""

    born_inf = coords[0][0]

    """Il y a Ecell/V sur la figure courrante, on vérifira cela avant"""
    """La figure sera créer pour qu'il n'y est pas de probléme"""
    """On récupére les 2 numéros de points correspondants aux valeurs des bornes"""
    res = [None, None]

    """calcule pour la born inf"""
    i = 0
    if data_x.data[i] > born_inf:
        while i < len(data_x.data) and data_x.data[i] > born_inf:
            i += 1
        if i == len(data_y.data):
            return - 1
        else:
            res_i_1 = i
    else:
        while i < len(data_x.data) and data_x.data[i] < born_inf:
            i += 1
        if i == len(data_y.data):
            return - 1
        else:
            res_i_1 = i

    i = len(data_x.data) - 1
    if data_x.data[i] > born_inf:
        while i > -1 and data_x.data[i] > born_inf:
            i -= 1
        if i == len(data_y.data):
            return - 1
        else:
            res_i_2 = i
    else:
        while i > -1 and data_x.data[i] < born_inf:
            i -= 1
        if i == len(data_y.data):
            return - 1
        else:
            res_i_2 = i

    if abs(data_y.data[res_i_1] - coords[0][1]) < \
            abs(data_y.data[res_i_2] - coords[0][1]):
        res[0] = res_i_1
    else:
        res[0] = res_i_2

    """calcule pour la born supp"""
    if len(coords) != 1:
        born_supp = coords[1][0]
        i = 0
        if data_x.data[i] > born_supp:
            while i < len(data_x.data) and data_x.data[i] > born_supp:
                i += 1
            if i == len(data_y.data):
                return - 1
            else:
                res_i_1 = i
        else:
            while i < len(data_x.data) and data_x.data[i] < born_supp:
                i += 1
            if i == len(data_y.data):
                return - 1
            else:
                res_i_1 = i

        i = len(data_x.data) - 1
        if data_x.data[i] > born_supp:
            while i > -1 and data_x.data[i] > born_supp:
                i -= 1
            if i == len(data_y.data):
                return - 1
            else:
                res_i_2 = i
        else:
            while i > -1 and data_x.data[i] < born_supp:
                i -= 1
            if i == len(data_y.data):
                return - 1
            else:
                res_i_2 = i

        if abs(data_y.data[res_i_1] - coords[1][1]) < \
                abs(data_y.data[res_i_2] - coords[1][1]):
            res[1] = res_i_1
        else:
            res[1] = res_i_2

        if res[0] > res[1]:
            temp = res[0]
            res[0] = res[1]
            res[1] = temp
        return [res[0], res[1] + 1]
    else:
        return res[0]


"""----------------------------------------------------------------------------------"""


def index_array(figure, coords):
    x = coords[0]
    y = coords[1]

    index_x = []
    for i in range(len(figure.y1_axe.data)):
        if figure.x_axe.data[i].name != "LIGNE0":
            res = coord_to_point([[x, y]], figure.x_axe.data[i], figure.y1_axe.data[i])
            index_x.append(res)

    min = None
    index_x_return = ["x", 0]
    index_y_return = ["y1", 0]

    for i in range(len(index_x)):
        if figure.x_axe.data[i].name != "LIGNE0" and figure.x_axe.data[i].visible:
            if min is None or abs(y - figure.y1_axe.data[i].data[index_x[i]]) < min:
                min = abs(y - figure.y1_axe.data[i].data[index_x[i]])
                index_x_return = ["x", i]
                index_y_return = ["y1", i]

    return index_x_return, index_y_return


"""----------------------------------------------------------------------------------"""


def get_new_path(name, path, ext):
    add = ""
    nb = 1
    while os.path.exists(path + "/" + name + add + ext):
        add = "(" + str(nb) + ")"
        nb += 1
    return path + "/" + name + add + ext


"""----------------------------------------------------------------------------------"""


def fusion_figure(fig1, fig2):
    from Console_Objets.Figure import Figure
    figure = Figure(fig1.name + "_" + fig2.name, 1)
    figure.format_line_y1 = fig1.format_line_y1
    figure.format_line_y2 = fig1.format_line_y2

    figure.type = fig1.type
    figure.start_x = fig1.start_x
    figure.end_x = fig1.end_x
    figure.start_y1 = fig1.start_y1
    figure.end_y1 = fig1.end_y1
    figure.start_y2 = fig1.start_y2
    figure.end_y2 = fig1.end_y2

    for i in range(len(fig1.data_y1)):
        figure.add_data_y1(fig1.data_y1[i].data, fig1.data_y1[i].name, None, fig1.data_y1[i].legende_affiche,
                           fig1.data_y1[i].color)
        figure.add_data_x(fig1.data_x[i].data, fig1.data_x[i].name, None)

    for i in range(len(fig2.data_y1)):
        figure.add_data_y1(fig2.data_y1[i].data, fig2.data_y1[i].name, None, fig2.data_y1[i].legende_affiche,
                           fig2.data_y1[i].color)
        figure.add_data_x(fig2.data_x[i].data, fig2.data_x[i].name, None)

    for i in range(len(fig1.data_y2)):
        figure.add_data_y2(fig1.data_y2[i].data, fig1.data_y2[i].name, None, fig1.data_y2[i].legende_affiche,
                           fig1.data_y2[i].color)
        figure.add_data_x(fig1.data_x[len(fig1.data_y1) + i].data, fig1.data_x[len(fig1.data_y1) + i].name, None)
    for i in range(len(fig2.data_y2)):
        figure.add_data_y2(fig2.data_y2[i].data, fig2.data_y2[i].name, None, fig2.data_y2[i].legende_affiche,
                           fig2.data_y2[i].color)
        figure.add_data_x(fig2.data_x[len(fig2.data_y1) + i].data, fig2.data_x[len(fig2.data_y1) + i].name, None)

    return figure


"""----------------------------------------------------------------------------------"""


def get_file_from_dir(path, ext=None):
    """
    Prend en input un chemin d'accés a un dossier et return le pth de tout ce qui est présent dans le dossier

    :param path: chemin d'un dossier
    :param ext: exentetion des fichier cherché, sinon None tous
    :return: list des dossier/fichier
    """

    if not os.path.exists(path):
        print("Chemin d'accès invalide", "fail")
        raise ValueError
    else:
        if not os.path.isdir(path):
            print("Un chemin d'accès à un dossier est demandé", "fail")
            raise ValueError
        else:
            res = []
            for f in os.listdir(path):
                if ext is not None:
                    if f[len(f) - len(ext):] == ext:
                        res.append(path + "/" + f)
                else:
                    res.append(path + "/" + f)
            return res


"""----------------------------------------------------------------------------------"""


def get_color_map(name):
    color = COLOR_MAP[name]
    try:
        colors = matplotlib.pyplot.get_cmap(color).colors
    except AttributeError:
        return matplotlib.pyplot.cm.get_cmap(color)
    else:
        return mcolors.LinearSegmentedColormap.from_list(name, colors, N=256)


"""----------------------------------------------------------------------------------"""


def create_array_color(color_map, nb):
    color = []
    if color_map is None:
        for i in range(0, nb):
            color.append(None)
        return color
    else:
        if nb < 3:
            for i in range(0, nb):
                start = 0
                end = 1/2
                pas = 1/2/nb
                while start < end:
                    color.append(color_map(start))
                    start += pas
        else:
            for i in range(0, nb):
                color.append(color_map(i/nb))
    return color


"""----------------------------------------------------------------------------------"""


def unique_name(array, name):
    """Parcours le nom des datas enregistrées et regarde si le nom donné en paramettre est unique, si il ne
    l'est pas on renvoie le même nom avec (1), (2) etc, si le nom est unique on renvoie jsute le nom """
    if array is None or array == []:
        return name

    for i in array:
        if i == name:
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
            return unique_name(array, name)
    return name


"""----------------------------------------------------------------------------------"""

COLOR_MAP = {
    "red": "autumn",
    "yellow": "Wistia",
    "blue": "winter",
    "pink": "spring",
    "black": "gray",
    "white": "binary",
    "cold": "cool",
    "green": "summer",
    "copper": "copper",
    "purple": "plasma",
    "viridis": "viridis",
    "plasma": "plasma",
    "inferno": "inferno",
    "magma": "magma",
    "cividis": "cividis",
    "Greys": "Greys",
    "Purples": "Purples",
    "Blues": "Blues",
    "Greens": "Greens",
    "Oranges": "Oranges",
    "Reds": "Reds",
    "YlOrBr": "YlOrBr",
    "YlOrRd": "YlOrRd",
    "OrRd": "OrRd",
    "PuRd": "PuRd",
    "RdPu": "RdPu",
    "BuPu": "BuPu",
    "GnBu": "GnBu",
    "PuBu": "PuBu",
    "YlGnBu": "YlGnBu",
    "PuBuGn": "PuBuGn",
    "BuGn": "BuGn",
    "YlGn": "YlGn",
    "binary": "binary",
    "gist_yarg": "gist_yarg",
    "gist_gray": "gist_gray",
    "gray": "gray",
    "bone": "bone",
    "spring": "spring",
    "summer": "summer",
    "autumn": "autumn",
    "winter": "winter",
    "cool": "cool",
    "Wistia": "Wistia",
    "hot": "hot",
    "afmhot": "afmhot",
    "gist_heat": "gist_heat",
    "PiYG": "PiYG",
    "PRGn": "PRGn",
    "BrBG": "BrBG",
    "PuOr": "PuOr",
    "RdGy": "RdGy",
    "RdBu": "RdBu",
    "RdYlBu": "RdYlBu",
    "RdYlGn": "RdYlGn",
    "Spectral": "Spectral",
    "coolwarm": "coolwarm",
    "bwr": "bwr",
    "seismic": "seismic",
    "twilight": "twilight",
    "twilight_shifted": "twilight_shifted",
    "hsv": "hsv",
    "Pastel1": "Pastel1",
    "Pastel2": "Pastel2",
    "Paired": "Paired",
    "Accent": "Accent",
    "Dark2": "Dark2",
    "Set1": "Set1",
    "Set2": "Set2",
    "Set3": "Set3",
    "tab10": "tab10",
    "tab20": "tab20",
    "tab20b": "tab20b",
    "tab20c": "tab20c",
    "flag": "flag",
    "prism": "prism",
    "ocean": "ocean",
    "gist_earth": "gist_earth",
    "terrain": "terrain",
    "gist_stern": "gist_stern",
    "gnuplot": "gnuplot",
    "gnuplot2": "gnuplot2",
    "CMRmap": "CMRmap",
    "cubehelix": "cubehelix",
    "brg": "brg",
    "gist_rainbow": "gist_rainbow",
    "rainbow": "rainbow",
    "jet": "jet",
    "turbo": "turbo",
    "nipy_spectral": "nipy_spectral",
    "gist_ncar": "gist_ncar"
}

MARKERS_PLOT = {
        '__': 'default',
        '.': 'point',
        ',': 'pixel',
        'o': 'circle',
        'v': 'triangle_down',
        '^': 'triangle_up',
        '<': 'triangle_left',
        '>': 'triangle_right',
        '1': 'tri_down',
        '2': 'tri_up',
        '3': 'tri_left',
        '4': 'tri_right',
        '8': 'octagon',
        's': 'square',
        'p': 'pentagon',
        '*': 'star',
        'h': 'hexagon1',
        'H': 'hexagon2',
        '+': 'plus',
        'x': 'x',
        'D': 'diamond',
        'd': 'thin_diamond',
        '|': 'vline',
        '_': 'hline',
        'P': 'plus_filled',
        'X': 'x_filled'
}


