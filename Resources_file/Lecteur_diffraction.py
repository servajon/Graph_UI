import copy
import os

from Resources_file.Emit import Emit
from Resources_file import Resources


def open_diffraction(_path):
    emit = Emit()
    emit.emit("msg_console", type="msg_console", str="Lecture des fichiers en cours", foreground_color="yellow")
    paths = Resources.get_file_from_dir(_path)


    data_c = []
    loop_data_c = []
    data_w = []
    loop_data_w = []

    for path in paths:
        # return data si le fichier a été touvé, raise value error sinon
        if type(path) != str:
            emit.emit("msg_console", type="msg_console", str="Un chemin d'accès au fichier est demandé",
                      foreground_color="red")
            raise ValueError
        if not os.path.exists(path):
            if len(path) > 3 and path[len(path) - 3] != '.':
                path = path + ".dat"
                if not os.path.exists(path):
                    path = path[0:len(path) - 4] + ".txt"
                    if not os.path.exists(path):
                        emit.emit("msg_console", type="msg_console", str="Fichier introuvable",
                                  foreground_color="red")
                        raise ValueError
            else:
                emit.emit("msg_console", type="msg_console", str="Fichier introuvable",
                          foreground_color="red")
                raise ValueError
        else:
            if not os.path.isfile(path):
                emit.emit("msg_console", type="msg_console", str="La ressource n'est pas un fichier",
                          foreground_color="red")
                raise ValueError

        if path[len(path) - 4: len(path)] == ".dat" or path[len(path) - 4: len(path)] == ".txt":
            file = open(path)
            _new_data, _loop_data = extract_data_diffraction(file)
            if _loop_data[2] == "c":
                data_c.append(_new_data)
                loop_data_c.append(_loop_data)
            elif _loop_data[2] == "w":
                data_w.append(_new_data)
                loop_data_w.append(_loop_data)
            else:
                raise NotImplementedError
        else:
            emit.emit("msg_console", type="msg_console", str="Le type du fichier est invalide",
                      foreground_color="red")
            raise ValueError
    return data_w, loop_data_w, data_c, loop_data_c


"----------------------------------------------------------"


def create_dics(data_w, loop_w, data_c, loop_c):
    emit = Emit()

    emit.emit("msg_console", type="msg_console", str="Warning open : " + str(len(loop_w)),
              foreground_color="green")
    emit.emit("msg_console", type="msg_console", str="Cooling open : " + str(len(loop_c)),
              foreground_color="green")

    order_w = []
    order_c = []

    new_loop_data = []
    tt = []
    intensite = []
    error = []

    temp = copy.copy(loop_w)
    while len(temp) != 0:
        _min = temp[0]
        index = 0
        for i in range(len(temp)):
            if temp[i] < _min:
                _min = temp[i]
                index = i
        order_w.append(temp[index][3])
        temp.pop(index)
    while len(order_w) != 0:
        index = 0
        while loop_w[index][3] != order_w[0]:
            index += 1

        temp_data = data_w[index]
        tt.extend(temp_data["2t"])
        intensite.extend(temp_data["intensite"])
        error.extend(temp_data["error"])
        new_loop_data.append(loop_w[index])
        order_w.pop(0)

    temp = copy.copy(loop_c)
    while len(temp) != 0:
        _max = temp[0]
        index = 0
        for i in range(len(temp)):
            if temp[i] > _max:
                _max = temp[i]
                index = i
        order_c.append(temp[index][3])
        temp.pop(index)

    while len(order_c) != 0:
        index = 0
        while loop_c[index][3] != order_c[0]:
            index += 1
        temp_data = data_c[index]
        tt.extend(temp_data["2t"])
        intensite.extend(temp_data["intensite"])
        error.extend(temp_data["error"])
        new_loop_data.append(loop_c[index])
        order_c.pop(0)

    data = {}
    start = 0
    test = []
    for i in range(len(new_loop_data)):
        n_start = new_loop_data[i][0] + start
        n_end = new_loop_data[i][1] + start
        test.append([n_start, n_end, new_loop_data[i][2], new_loop_data[i][3]])
        start = n_end + 1

    data["loop_data"] = test
    data["2t"] = tt
    data["intensite"] = intensite
    data["error"] = error
    if len(data_c) == 0:
        data["row_data"] = data_w[0]["row_data"]
    else:
        data["row_data"] = data_c[0]["row_data"]
    return data


"----------------------------------------------------------"


def extract_data_diffraction(file):
    emit = Emit()

    data_data = file.readlines()
    index = 0
    data = {}
    row_data = ["2t", "intensite", "error"]
    line = data_data[index]
    if not ".dat" in line:
        emit.emit("msg_console", type="msg_console", str="Format de fichier invalide",
                  foreground_color="red")
        raise ValueError

    nb = line.find(".dat")
    for i in reversed(range(0, nb)):
        if line[i] == '_':
            nb = i
            break

    _type = line[nb - 2]

    found = 0
    for i in reversed(range(0, nb)):
        if line[i] == '/' and found == 0:
            nb1 = i
            found += 1
        elif line[i] == '/' and found == 1:
            nb2 = i
            break

    data["name"] = line[nb2+1:nb1]

    nb1 = data_data[2].find("blowerT ") + 8
    for i in range(nb1, len(data_data[2])):
        if data_data[2][i] == " ":
            nb2 = i
            break
    temp = float(data_data[2][nb1:nb2].replace(',', '.'))
    data["2t"] = []
    data["intensite"] = []
    data["error"] = []
    index = 4
    while index < len(data_data):
        res = data_data[index].split("  ")
        data["2t"].append(float(res[0].replace(',', '.')))
        data["intensite"].append(float(res[1].replace(',', '.')))
        data["error"].append(float(res[2].replace(',', '.')))
        index += 1
    data["row_data"] = row_data
    loop_data = [0, len(data_data) - 5, _type, temp]
    return data, loop_data

