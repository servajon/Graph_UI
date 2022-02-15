import copy
import multiprocessing as mp
import os

import Resources_file.Resources as R
from Console_Objets.Affiche_objet import Array_Abstract_objet_affiche

class Lecteur_thread:
    def open(path, file_type, format_time=None):
        """return data si le fichier a été touvé, raise value error sinon"""
        if type(path) != str:
            print("Un chemin d'accès au fichier est demandé")
            raise ValueError
        if not os.path.exists(path):
            if len(path) > 3 and path[len(path) - 3] != '.':
                path = path + ".mpt"
                if not os.path.exists(path):
                    path = path[0:len(path) - 4] + ".txt"
                    if not os.path.exists(path):
                        path = path[0:len(path) - 4] + ".mpr"
                        if not os.path.exists(path):
                            print("Fichier introuvable", "fail")
                            raise ValueError
            else:
                print("Fichier introuvable")
                raise ValueError
        else:
            if not os.path.isfile(path):
                print("La ressource n'est pas un fichier")
                raise ValueError

        if path[len(path) - 4: len(path)] == ".mpt" or path[len(path) - 4: len(path)] == ".txt":
            file = open(path)
            if file_type == "cccv" or file_type == "cv":
                return extract_data_cccv(file, format_time)
            elif file_type == "gitt":
                return extract_data_gitt(file, format_time)
            elif file_type == "impedance":
                return extract_data_impedance(file, format_time)
            elif file_type == "cp":
                return extract_data_cp(file, format_time)
            elif file_type == "modulo_v":
                return extract_data_modulo_v(file, format_time)
            else:
                raise ValueError
        elif path[len(path) - 4: len(path)] == ".mpr":
            print("Merci de convertir votre fichier EC-lab en fichier texte")
            raise ValueError
            if file_type == "cccv" or file_type == "cv" or file_type == "gitt" or file_type == "cp" or \
                    file_type == "modulo_v":
                return Lecteur_mpr.extract_data_mpr(path, "cccv", format_time)
            else:
                return Lecteur_mpr.extract_data_mpr(path, "impedance", format_time)
        else:
            print("Le type du fichier est invalide")
            raise ValueError


def extract_data_cccv(file, format_time=None):
    from UI_interface.Main_windows_UI import Emit
    emit = Emit()
    emit.emit(type="msg_console", str="Lecture du fichier en cours", foreground_color="yellow")


    data_data = file.readlines()

    index = 0
    data = {}
    loop_data = []

    # on récupére le nom original du fichier
    while index < len(data_data) and "Saved on :" not in data_data[index] and "Number of loops" not in data_data[index] \
            and "mode" not in data_data[index]:
        index += 1

    if index == len(data_data):
        raise ValueError
    elif data_data[index][0:5] == "Saved":
        index += 1
        ligne = data_data[index][8: len(data_data[index]) - 5]

        name = ""
        for i in range(len(ligne)):
            if ligne[i] == " ":
                name += "_"
            else:
                name += ligne[i]

        # on avance j'usqu'aux informations sur les loop
        while index < len(data_data) and "Number of loops" not in data_data[index] and "mode" not in data_data[index] \
                and "Mass of active material" not in data_data[index]:
            index += 1

        if index == len(data_data):
            raise ValueError
        elif data_data[index][0:4] == "Mass":
            val = data_data[index][data_data[index].find(":") + 2:data_data[index].rfind(" ")]
            val = float(val.replace(',', '.'))
            if val == 0.001:
                emit.emit(type="msg_console", str="La masse de l'électrode inscrite dans le fichier est incorrecte", foreground_color="yellow")
                mass_electrode = -1
            else:
                pass
                mass_electrode = float(val)
            while index < len(data_data) and "Number of loops" not in data_data[index] and "mode" not in data_data[index]:
                index += 1
            if index == len(data_data):
                emit.emit(type="msg_console", str="Fichier invalide", foreground_color="red")
                raise ValueError
        elif index == len(data_data):
            emit.emit(type="msg_console", str="Fichier invalide", foreground_color="red")
            raise ValueError
        else:
            emit.emit(type="msg_console", str="La masse de l'électrode inscrite dans le fichier est incorrecte",
                      foreground_color="yellow")
            mass_electrode = -1
    elif data_data[index] == "":
        emit.emit(type="msg_console", str="Fichier invalide", foreground_color="red")
        raise ValueError
    else:
        emit.emit(type="msg_console", str="L'entête du fichier est introuvable",
                  foreground_color="yellow")
        name = "no_name_found"
        mass_electrode = -1

    if data_data[index][0:4] != "mode":
        # on récupére les information sur les loop
        max_index = 0
        index += 1
        while get_mot_num(data_data[index], 0) == "Loop":
            temp_min = int(get_mot_num(data_data[index], 5))
            temp_max = int(get_mot_num(data_data[index], 7))

            loop_data.append([temp_min, temp_max])
            # on récupére l'info de la taille de l'index
            if temp_max > max_index:
                max_index = temp_max
            index += 1

        # on récupére le nom de colonnes dans le fichier
        index += 1
        miss_loop = False
    else:
        """On n'a pas trouvé le loops, il faut les construire"""
        miss_loop = True

    data_row = []

    mot = ''
    for i in range(len(data_data[index])):
        if data_data[index][i] == '\t':
            if mot == "time/s":
                if format_time == "s":
                    data_row.append("time/s")
                    data["time/s"] = []
                elif format_time == "min":
                    data_row.append("time/min")
                    data["time/min"] = []
                else:
                    data_row.append("time/h")
                    data["time/h"] = []
                    """Pour un fichier de CV on n'a pas Ecell/V mais Ewe/V, on le remplace par Ecell/V"""
            elif mot == "Ewe/V":
                data_row.append("Ecell/V")
                data["Ecell/V"] = []
            else:
                data_row.append(mot)
                data[mot] = []

            mot = ''
        else:
            if data_data[index][i] == " ":
                mot += "_"
            else:
                mot += data_data[index][i]

    data["name"] = name
    data["mass_electrode"] = mass_electrode
    if "cycle_number" not in data_row and miss_loop:
        data = create_data(data_data[index + 1:], data, data_row, -1)
        if format_time == "s":
            res = create_loop(data["time/s"])
        elif format_time == "min":
            res = create_loop(data["time/min"])
        else:
            res = create_loop(data["time/h"])
        if len(res) == 1:
            emit.emit(type="msg_console", str="Fichier invalide, impossible de créer les loops",
                      foreground_color="red")
            raise ValueError
        else:
            data["loop_data"] = res
            return data
    try:
        if not miss_loop:
            data = create_data(data_data[index+1:], data, data_row, loop_data)
        else:
            data = create_data(data_data[index+1:], data, data_row)

    except ValueError:
        emit.emit(type="msg_console", str="Fichier contenant des valeurs invalides : UNKVAR",
                  foreground_color="red")
        raise ValueError
    else:
        return data


def extract_data_gitt(file, format_time=None):
    print("Lecture du fichier en cours")


    data_data = file.readlines()

    index = 0
    data = {}
    loop_data = []

    # on récupére le nom original du fichier
    while "Saved on :" not in data_data[index] and "Number of loops" not in data_data[index] and \
            "mode" not in data_data[index] and data_data[index] != "":
        index += 1

    if data_data[index][0:5] == "Saved":
        index += 1
        ligne = data_data[index][8: len(data_data[index]) - 5]

        name = ""
        for i in range(len(ligne)):
            if ligne[i] == " ":
                name += "_"
            else:
                name += ligne[i]

        # on avance j'usqu'aux informations sur les loop
        while "Number of loops" not in data_data[index] and "mode" not in data_data[index] and \
                "Is" not in data_data[index] and data_data[index] != "":
            index += 1

        if data_data[index][0:2] == "Is":
            index_Is = 2
            while index_Is < len(data_data[index]) and data_data[index][index_Is] == " " or \
                    data_data[index][index_Is] == "\t":
                index_Is += 1
            val = data_data[index][index_Is:-1]
            val = float(val.replace(',', '.'))
            data["Is"] = val

            while "dQM" not in data_data[index]:
                index += 1

            index_dqm = 3
            while index < len(data_data[index]) and data_data[index][index_dqm] == " " or data_data[index][index_dqm] == "\t":
                index_dqm += 1
            val = data_data[index][index_dqm:-1]
            val = float(val.replace(',', '.'))
            data["dQM"] = val

            while "Number of loops" not in data_data[index] and "mode" not in data_data[index]:
                index += 1

        elif data_data[index] == "":
            print("Fichier invalide")
            raise ValueError
    elif data_data[index] == "":
        print("Fichier invalide")
        raise ValueError
    else:
        print("L'entête du fichier est introuvable")
        name = "no_name_found"

    if data_data[index][0:4] != "mode":
        # on récupére les information sur les loop
        max_index = 0
        index += 1
        while get_mot_num(data_data[index], 0) == "Loop":
            temp_min = int(get_mot_num(data_data[index], 5))
            temp_max = int(get_mot_num(data_data[index], 7))

            loop_data.append([temp_min, temp_max])
            # on récupére l'info de la taille de l'index
            if temp_max > max_index:
                max_index = temp_max
            index += 1

        # on récupére le nom de colonnes dans le fichier
        index += 1
        miss_loop = False
    else:
        """On n'a pas trouvé le loops, il faut les construirent"""
        miss_loop = True

    data_row = []

    mot = ''
    for i in range(len(data_data[index])):
        if data_data[index][i] == '\t':
            if mot == "time/s":
                if format_time == "s":
                    data_row.append("time/s")
                    data["time/s"] = []
                elif format_time == "min":
                    data_row.append("time/min")
                    data["time/min"] = []
                else:
                    data_row.append("time/h")
                    data["time/h"] = []
                    """Pour un fichier de CV on n'a pas Ecell/V mais Ewe/V, on le remplace par Ecell/V"""
            elif mot == "Ewe/V":
                data_row.append("Ecell/V")
                data["Ecell/V"] = []
            else:
                data_row.append(mot)
                data[mot] = []

            mot = ''
        else:
            if data_data[index][i] == " ":
                mot += "_"
            else:
                mot += data_data[index][i]

    data["name"] = name
    if "cycle_number" not in data_row and miss_loop:
        data = create_data(data_data[index + 1:], data, data_row, -1)
        if format_time == "s":
            res = create_loop(data["time/s"])
        elif format_time == "min":
            res = create_loop(data["time/min"])
        else:
            res = create_loop(data["time/h"])
        if len(res) == 1:
            print("Fichier invalide, impossible de créer les loops")
            raise ValueError
        else:
            data["loop_data"] = res
            return data
    try:
        if not miss_loop:
            data = create_data(data_data[index+1:], data, data_row, loop_data)
        else:
            data = create_data(data_data[index+1:], data, data_row)
    except ValueError:
        print("Fichier contenant des valeurs invalides : UNKVAR / mauvais export")
        raise ValueError
    else:
        return data


def extract_data_impedance(file, format_time=None):
    resource = R.Resource_class()
    print("Lecture du fichier en cours")


    data_data = file.readlines()

    index = 0
    data = {}
    loop_data = []

    # on récupére le nom original du fichier
    while index < len(data_data) and "Saved on :" not in data_data[index] and "Number of loops" not in data_data[index] and \
            "freq/Hz" not in data_data[index] and data_data[index] != "":
        index += 1

    if data_data[index][0:5] == "Saved":
        index += 1
        ligne = data_data[index][8: len(data_data[index]) - 5]

        name = ""
        for i in range(len(ligne)):
            if ligne[i] == " ":
                name += "_"
            else:
                name += ligne[i]

        # on avance j'usqu'aux informations sur les loop
        while index < len(data_data) and "Number of loops" not in data_data[index] \
                and "freq/Hz" not in data_data[index]:
            index += 1

        if index == len(data_data):
            print("Fichier invalide")
            raise ValueError
    elif index == len(data_data):
        resource.print_color("Fichier invalide", "fail")
        raise ValueError
    else:
        resource.print_color("L'entête du fichier est introuvable", "fail")
        name = "no_name_found"
        data["mass_electrode"] = -1

    if "freq/Hz" not in data_data[index]:
        # on récupére les information sur les loop
        max_index = 0
        index += 1
        while get_mot_num(data_data[index], 0) == "Loop":
            temp_min = int(get_mot_num(data_data[index], 5))
            temp_max = int(get_mot_num(data_data[index], 7))

            loop_data.append([temp_min, temp_max])
            # on récupére l'info de la taille de l'index
            if temp_max > max_index:
                max_index = temp_max
            index += 1

        #   on ajoute les données des loop à data
        data["index"] = [0, max_index]
        data["loop_data"] = loop_data

        # on récupére le nom de colonnes dans le fichier
        index += 1
        miss_loop = False
    else:
        """On n'a pas trouvé le loops, il faut les construire"""
        miss_loop = True

    data_row = []

    mot = ''
    for i in range(len(data_data[index])):
        if data_data[index][i] == '\t':
            if mot == "time/s":
                if format_time == "s":
                    data_row.append("time/s")
                    data["time/s"] = []
                elif format_time == "min":
                    data_row.append("time/min")
                    data["time/min"] = []
                else:
                    data_row.append("time/h")
                    data["time/h"] = []
                    """Pour un fichier de CV on n'a pas Ecell/V mais Ewe/V, on le remplace par Ecell/V"""
            elif mot == "<Ewe>/V":
                data_row.append("Ecell/V")
                data["Ecell/V"] = []
            else:
                data_row.append(mot)
                data[mot] = []

            mot = ''
        else:
            if data_data[index][i] == " ":
                mot += "_"
            else:
                mot += data_data[index][i]

    data["name"] = name
    if "cycle_number" not in data_row and miss_loop:
        data = create_data(data_data[index + 1:], data, data_row, -1)
        if format_time == "s":
            res = create_loop(data["time/s"])
        elif format_time == "min":
            res = create_loop(data["time/min"])
        else:
            res = create_loop(data["time/h"])
        if len(res) == 1:
            resource.print_color("Fichier invalide, impossible de créer les loops", "fail")
            raise ValueError
        else:
            data["loop_data"] = res
            return data
    try:
        if not miss_loop:
            data = create_data(data_data[index+1:], data, data_row, loop_data)
        else:
            data = create_data(data_data[index+1:], data, data_row)
    except ValueError:
        resource.print_color("Fichier contenant des valeurs invalides : UNKVAR", "fail")
        raise ValueError
    else:
        return data


def extract_data_cp(file, format_time=None):
    resource = R.Resource_class()
    resource.print_color("Lecture du fichier en cours", "work")

    data_data = file.readlines()

    index = 0
    data = {}
    loop_data = []

    # on récupére le nom original du fichier
    while "Saved on :" not in data_data[index] and "Number of loops" not in data_data[index] \
            and "mode" not in data_data[index] and data_data[index] != "":
        index += 1

    if data_data[index][0:5] == "Saved":
        index += 1
        ligne = data_data[index][8: len(data_data[index]) - 5]

        name = ""
        for i in range(len(ligne)):
            if ligne[i] == " ":
                name += "_"
            else:
                name += ligne[i]

        # on avance j'usqu'aux informations sur les loop
        while "Number of loops" not in data_data[index] and "mode" not in data_data[index] and\
                "Is" not in data_data[index] and data_data[index] != "":
            index += 1

        if data_data[index][0:2] == "Is":
            index_Is = 2
            while index_Is < len(data_data[index]) and data_data[index][index_Is] == " " or \
                    data_data[index][index_Is] == "\t":
                index_Is += 1
            val = data_data[index][index_Is:-1]
            val = float(val.replace(',', '.'))
            data["Is"] = val

            while "Number of loops" not in data_data[index] and "mode" not in data_data[index]:
                index += 1

        elif data_data[index] == "":
            resource.print_color("Fichier invalide", "fail")
            raise ValueError
    elif data_data[index] == "":
        resource.print_color("Fichier invalide", "fail")
        raise ValueError
    else:
        resource.print_color("L'entête du fichier est introuvable", "fail")
        name = "no_name_found"

    if data_data[index][0:4] != "mode":
        # on récupére les information sur les loop
        max_index = 0
        index += 1
        while get_mot_num(data_data[index], 0) == "Loop":
            temp_min = int(get_mot_num(data_data[index], 5))
            temp_max = int(get_mot_num(data_data[index], 7))

            loop_data.append([temp_min, temp_max])
            # on récupére l'info de la taille de l'index
            if temp_max > max_index:
                max_index = temp_max
            index += 1

        # on récupére le nom de colonnes dans le fichier
        index += 1
        miss_loop = False
    else:
        """On n'a pas trouvé le loops, il faut les construirent"""
        miss_loop = True

    data_row = []

    mot = ''
    for i in range(len(data_data[index])):
        if data_data[index][i] == '\t':
            if mot == "time/s":
                if format_time == "s":
                    data_row.append("time/s")
                    data["time/s"] = []
                elif format_time == "min":
                    data_row.append("time/min")
                    data["time/min"] = []
                else:
                    data_row.append("time/h")
                    data["time/h"] = []
                    """Pour un fichier de CV on n'a pas Ecell/V mais Ewe/V, on le remplace par Ecell/V"""
            elif mot == "<Ewe>/V" or mot == "Ewe/V":
                data_row.append("Ecell/V")
                data["Ecell/V"] = []
            elif mot == "I/mA":
                data_row.append("<I>/mA")
                data["<I>/mA"] = []
            else:
                data_row.append(mot)
                data[mot] = []

            mot = ''
        else:
            if data_data[index][i] == " ":
                mot += "_"
            else:
                mot += data_data[index][i]

    data["name"] = name
    if "cycle_number" not in data_row and miss_loop:
        data = create_data(data_data[index + 1:], data, data_row, -1)
        if format_time == "s":
            res = create_loop(data["time/s"])
        elif format_time == "min":
            res = create_loop(data["time/min"])
        else:
            res = create_loop(data["time/h"])
        if len(res) == 1:
            resource.print_color("Fichier invalide, impossible de créer les loops", "fail")
            raise ValueError
        else:
            data["loop_data"] = res
            return data
    try:
        if not miss_loop:
            data = create_data(data_data[index+1:], data, data_row, loop_data)
        else:
            data = create_data(data_data[index+1:], data, data_row)
    except ValueError:
        resource.print_color("Fichier contenant des valeurs invalides : UNKVAR", "fail")
        raise ValueError
    else:
        return data


def extract_data_modulo_v(file, format_time=None):
    resource = R.Resource_class()
    resource.print_color("Lecture du fichier en cours", "work")

    if resource.interactive:
        obj_data = Array_Abstract_objet_affiche()
        obj_data.event_thread1.set()
        obj_data.stop_main = True
        obj_data.event_thread2.wait()
        data_data = file.readlines()
        obj_data.stop_main = False
        obj_data.event_thread1.set()
        obj_data.event_thread1.clear()
        obj_data.event_thread2.clear()
    else:
        data_data = file.readlines()

    index = 0
    data = {}

    # on récupére le nom original du fichier
    while "Saved on :" not in data_data[index] and "mode" not in data_data[index] and data_data[index] != "":
        index += 1

    if data_data[index][0:5] == "Saved":
        index += 1
        ligne = data_data[index][8: len(data_data[index]) - 5]

        name = ""
        for i in range(len(ligne)):
            if ligne[i] == " ":
                name += "_"
            else:
                name += ligne[i]

        # on avance j'usqu'aux informations sur les loop
        while "mode" not in data_data[index] and data_data[index] != "":
            index += 1

        if data_data[index] == "":
            resource.print_color("Fichier invalide", "fail")
            raise ValueError

    elif data_data[index] == "":
        resource.print_color("Fichier invalide", "fail")
        raise ValueError
    else:
        resource.print_color("L'entête du fichier est introuvable", "fail")
        name = "no_name_found"

    data_row = []
    mot = ''
    for i in range(len(data_data[index])):
        if data_data[index][i] == '\t':
            if mot == "time/s":
                if format_time == "s":
                    data_row.append("time/s")
                    data["time/s"] = []
                elif format_time == "min":
                    data_row.append("time/min")
                    data["time/min"] = []
                else:
                    data_row.append("time/h")
                    data["time/h"] = []
                    """Pour un fichier de CV on n'a pas Ecell/V mais Ewe/V, on le remplace par Ecell/V"""
            elif mot == "Ewe/V":
                data_row.append("Ecell/V")
                data["Ecell/V"] = []
            elif mot == "I/mA":
                data_row.append("<I>/mA")
                data["<I>/mA"] = []
            else:
                data_row.append(mot)
                data[mot] = []

            mot = ''
        else:
            if data_data[index][i] == " ":
                mot += "_"
            else:
                mot += data_data[index][i]

    data["name"] = name
    if "cycle_number" not in data_row:
        data = create_data(data_data[index + 1:], data, data_row, -1)
        if format_time == "s":
            res = create_loop(data["time/s"])
        elif format_time == "min":
            res = create_loop(data["time/min"])
        else:
            res = create_loop(data["time/h"])
        if len(res) == 1:
            resource.print_color("Fichier invalide, impossible de créer les loops", "fail")
            raise ValueError
        else:
            data["loop_data"] = res
            return data
    try:
        data = create_data(data_data[index+1:], data, data_row)
    except ValueError:
        resource.print_color("Fichier contenant des valeurs invalides : UNKVAR", "fail")
        raise ValueError
    else:
        return data


# return un mot à une position donné dans un string, le premier étant 0
# return un string vide sinon le num est plus grand que le nombre de mot du string
# return un string vide si num est négatif
def get_mot_num(str, num):
    # remplace les tabulations par un espace
    if '\t' in str:
        i = 0
        while i < len(str):
            if str[i] == "\t":
                if 0 < i < len(str):
                    str = str[0:i] + " " + str[i + 1: len(str)]
                elif i == 0:
                    str = str[1: len(str)]
                elif i == len(str):
                    str = str[0:len(str) - 1]
            i += 1
    mot = ''
    j = 0
    for i in range(len(str)):
        if str[i] == ' ':
            j = j + 1
        elif j == num:
            mot += str[i]
        elif j > num:
            break
    # retire le caractére de fin de chaine si le mot est le dernier de la chaine
    if '\n' in mot:
        mot = mot[0: len(mot) - 1]
    return mot


def open_script(path):
    resource = R.Resource_class()
    if type(path) != str:
        resource.print_color("Un chemin d'accès au fichier est demandé", "fail")
        raise ValueError
    if not os.path.exists(path):
        if len(path) > 3 and path[len(path) - 3] != '.':
            path += ".txt"
        if not os.path.exists(path):
            resource.print_color("Fichier introuvable", "fail")
            raise ValueError
        else:
            resource.print_color("Fichier introuvable", "fail")
            raise ValueError
    else:
        if not os.path.isfile(path):
            resource.print_color("La ressource n'est pas un fichier", "fail")
            raise ValueError

    if path[len(path) - 4: len(path)] == ".txt":
        file = open(path)
        return Lecteur_thread.extract_script(file)
    else:
        resource.print_color("Format de fichier invalide, un .mpt ou .txt est demandé", "fail")


def extract_script(file):
    data = []
    ligne = file.readline()
    while ligne != "":
        temp = ligne[0:len(ligne)]
        if temp[len(temp) - 1] == "\n":
            temp = temp[0:len(temp) - 1]
        data.append(temp)
        ligne = file.readline()
    return data


def create_data(data_data, data, data_row, loop_data=None):
    if len(data_row) == 0:
        print("Le fichier ne correspond pas à l'expérience indiqué")
        raise ValueError

    if len(data_data) < 200000:
        if loop_data is not None:
            data = work([data, data_data, data_row])
            data["loop_data"] = loop_data
            data["row_data"] = data_row
        else:
            data = work_loop([data, data_data, data_row])
            data["row_data"] = data_row
        return data
    else:
        array_data = []
        if loop_data is not None:
            nb_pross = os.cpu_count()
            start = 0
            pas = int(len(data_data) / nb_pross)
            for i in range(nb_pross - 1):
                start = start
                end = start + pas + 1
                array_data.append([copy.
                                  deepcopy(data), copy.deepcopy(data_data[start:end]), data_row])
                start += pas + 1

            array_data.append([copy.deepcopy(data), copy.deepcopy(data_data[start:]), data_row])
            with mp.Pool() as pool:
                res = pool.map(work, array_data)
            data = res[0]
            data["loop_data"] = loop_data

        else:
            nb_pross = os.cpu_count()
            start = 0
            pas = int(len(data_data) / nb_pross)
            for i in range(nb_pross - 1):
                start = start
                end = start + pas + 1
                array_data.append([copy.
                                  deepcopy(data), copy.deepcopy(data_data[start:end]), data_row])
                start += pas + 1

            array_data.append([copy.deepcopy(data), copy.deepcopy(data_data[start:]), data_row])
            with mp.Pool() as pool:
                res = pool.map(work_loop, array_data)
            data = res[0]
            loop_data = []
            for r in res:
                for loop in r.get("loop_data"):
                    loop_data.append(loop)
            i = 1
            while i < len(loop_data):
                if loop_data[i - 1][1] > loop_data[i][1]:
                    loop_data[i][1] = loop_data[i - 1][1] + 1 + loop_data[i][1] - loop_data[i][0]
                    loop_data[i][0] = loop_data[i - 1][1] + 1
                i += 1
            i = 0
            temp = []
            while i < len(loop_data) - 1:
                if loop_data[i][2] == loop_data[i + 1][2]:
                    start = loop_data[i][0]
                    while i < len(loop_data) - 1 and loop_data[i + 1][2] == loop_data[i][2]:
                        i += 1
                    temp.append([start, loop_data[i][1]])
                else:
                    temp.append([loop_data[i][0], loop_data[i][1]])
                i += 1
            if len(loop_data) > 1 and loop_data[-2] != loop_data[-1]:
                temp.append(loop_data[-1])
            data["loop_data"] = temp

        data["row_data"] = data_row
        for i in range(1, len(res)):
            for key in data.get("row_data"):
                data.get(key).extend(res[i].get(key))
        return data


def work(args):
    data = args[0]
    data_data = args[1]
    data_row = args[2]

    for ligne in data_data:
        index = 0
        value = ""
        for i in range(len(ligne)):
            if ligne[i] == "\t":
                if data_row[index] == "time/h":
                    f = float(value.replace(',', '.'))
                    f = f / 3600
                    data.get(data_row[index]).append(f)
                elif data_row[index] == "time/min":
                    f = float(value.replace(',', '.'))
                    f = f / 60
                    data.get(data_row[index]).append(f)
                else:
                    # on remplace , par ., notation différente pour les chiffres
                    data.get(data_row[index]).append(float(value.replace(',', '.')))
                value = ""
                index += 1
            else:
                value += ligne[i]
        # on ajouter la dernière donnée de la ligne
        # sans ajouter la toute dernière ligne qui est vide..........
        if value != '':
            value = value[0:len(value) - 1]
            data.get(data_row[index]).append(float(value.replace(',', '.')))
    return data


def work_loop(args):
    data = args[0]
    data_data = args[1]
    data_row = args[2]
    loop_data = []

    ligne_count = 0
    current_loop = None
    start_loop = None

    for ligne in data_data:
        index = 0
        value = ""
        for i in range(len(ligne)):
            if ligne[i] == "\t":
                if data_row[index] == "time/h":
                    f = float(value.replace(',', '.'))
                    f = f / 3600
                    data.get(data_row[index]).append(f)
                elif data_row[index] == "time/min":
                    f = float(value.replace(',', '.'))
                    f = f / 60
                    data.get(data_row[index]).append(f)
                elif data_row[index] == "cycle_number" and int(
                        float(value.replace(',', '.'))) != current_loop:

                    if start_loop is None:
                        start_loop = current_loop

                    current_loop = int(float(value.replace(',', '.')))
                    if len(loop_data) > 0:
                        loop_data[current_loop - start_loop - 1][1] = ligne_count - 1
                        loop_data[current_loop - start_loop - 1][2] = current_loop - 1

                    loop_data.append([ligne_count, None, None])
                else:
                    # on remplace , par ., notation différente pour les chiffres
                    data.get(data_row[index]).append(float(value.replace(',', '.')))
                value = ""
                index += 1
            else:
                value += ligne[i]
        # on ajouter la dernière donnée de la ligne
        # sans ajouter la toute dernière ligne qui est vide..........
        if value != '':
            if data_row[index] == "cycle_number" and int(
                    float(value.replace(',', '.'))) != current_loop:
                if start_loop is None:
                    start_loop = current_loop

                current_loop = int(float(value.replace(',', '.')))
                if len(loop_data) > 0:
                    loop_data[current_loop - start_loop - 1][1] = ligne_count - 1
                    loop_data[current_loop - start_loop - 1][2] = current_loop - 1

                loop_data.append([ligne_count, None, None])
            else:
                value = value[0:len(value) - 1]
                data.get(data_row[index]).append(float(value.replace(',', '.')))
        ligne_count += 1

    loop_data[-1][1] = ligne_count - 1
    loop_data[-1][2] = current_loop
    data["loop_data"] = loop_data
    return data


def create_loop(time):
    loop_data = []
    if len(time) > 20:
        pas = float(time[19]) - float(time[18])
    elif float(time[0]) != 0:
        pas = float(time[1]) - float(time[0])
    else:
        raise ValueError
    i = 1
    index_min = 0
    while i < len(time):
        if (time[i] - time[i-1]) > pas * 2:
            loop_data.append([index_min, i - 1])
            index_min = i
        i += 1
    loop_data.append([index_min, len(time) - 1])
    return loop_data