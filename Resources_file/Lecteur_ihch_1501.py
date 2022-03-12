import os
from datetime import datetime
import h5py
import numpy
import numpy as np

import Resources_file.Resources
from Data_type.Ihch_1501 import Ihch_1501_cycle, Ihch_1501_sample_saxs, Ihch_1501_scan, Ihch_1501_frame, \
    Ihch_1501_sample_waxs
from Resources_file.Emit import Emit


def open_ihch_1501(_dir_path):
    emit = Emit()
    emit.emit("msg_console", type="msg_console", str="Playing files in progress", foreground_color="yellow")
    cycles = []
    dir_path = Resources_file.Resources.get_file_from_dir(_dir_path)
    try:
        for cycle_path in dir_path:
            cycles.append(Ihch_1501_cycle(cycle_path.split("/")[-1]))
            cycle_path += "/"
            samples_path = Resources_file.Resources.get_file_from_dir(cycle_path)


            if "saxs" in samples_path[0]:
                saxs_paths = samples_path[0] + "/"
                waxs_paths = samples_path[1] + "/"
            else:
                saxs_paths = samples_path[1] + "/"
                waxs_paths = samples_path[0] + "/"

            saxs_paths = Resources_file.Resources.get_file_from_dir(saxs_paths)
            waxs_paths = Resources_file.Resources.get_file_from_dir(waxs_paths)

            for saxs_path in saxs_paths:
                cycles[-1].saxs.append(Ihch_1501_sample_saxs(saxs_path.split("/")[-1]))
                saxs_path += "/"

                file_paths = Resources_file.Resources.get_file_from_dir(saxs_path)

                current = file_paths[0][-13:-9]

                cycles[-1].saxs[-1].scans.append(Ihch_1501_scan(current))
                for file_path in file_paths:
                    if file_path[-13:-9] != current:
                        current = file_path[-13:-9]
                        cycles[-1].saxs[-1].scans.append(Ihch_1501_scan(current))

                    cycles[-1].saxs[-1].scans[-1].frames.append(Ihch_1501_frame(file_path[-8:-4]))
                    file = open(file_path)
                    frame = read_frame(file)
                    if frame is not None:
                        cycles[-1].saxs[-1].scans[-1].frames[-1].data = frame

            for waxs_path in waxs_paths:
                cycles[-1].waxs.append(Ihch_1501_sample_waxs(waxs_path.split("/")[-1]))
                waxs_path += "/"

                file_paths = Resources_file.Resources.get_file_from_dir(waxs_path)

                current = file_paths[0][-13:-9]
                cycles[-1].waxs[-1].scans.append(Ihch_1501_scan(current))
                for file_path in file_paths:
                    file = open(file_path)
                    frame = read_frame(file)
                    if frame is not None:
                        if file_path[-13:-9] != current:
                            current = file_path[-13:-9]
                            cycles[-1].waxs[-1].scans.append(Ihch_1501_scan(current))

                        cycles[-1].waxs[-1].scans[-1].frames.append(Ihch_1501_frame(file_path[-8:-4]))
                        cycles[-1].waxs[-1].scans[-1].frames[-1].data = frame
                    """else:
                        print(file_path)
                        emit.emit("msg_console", type="msg_console", str=file_path + " invalid",
                                  foreground_color="red")"""

    except TypeError:
        return len(dir_path)
    else:
        return cycles


def read_frame(file):
    data = {}

    data_data = file.readlines()

    if not "valid" in data_data[0] and not "invalid" in data_data[0]:
        print(file.name)
        print(data_data)
        raise TypeError
    else:
        if "invalid" in data_data[0]:
            return

        data["time/s"] = float(data_data[1][19:-1])
        if data_data[2][21:-1] == "not started":
            data["Ecell/V"] = None
        else:
            data["Ecell/V"] = float(data_data[2][21:-1])

        if data_data[3][20:-1] == "not started":
            data["<I>/mA"] = None
        else:
            data["<I>/mA"] = float(data_data[3][20:-1])

    index = 3

    while data_data[index][0] == "#":
        index += 1

    temp_row_data = data_data[index - 1].split(" ")
    row_data = []
    for i in temp_row_data[1:-1]:
        if i != '':
            row_data.append(i)

    for _data in row_data:
        data[_data] = []

    while index < len(data_data):
        res_line = data_data[index].split(" ")
        res_line2 = []
        for i in res_line:
            if i != '':
                res_line2.append(i)
        # on dégage le \n
        res_line2[-1] = res_line2[-1][:-1]
        for i, _data in enumerate(row_data):
            data[_data].append(float(res_line2[i]))
        index += 1
    return data


def extract_data_cccv(path):
    file = open(path, "r")
    data_data = file.readlines()
    file.close()
    index = 0
    data = {}

    while index < len(data_data) and "Acquisition started on" not in data_data[index]:
        index += 1

    if index == len(data_data):
        # emit.emit("msg_console", type="msg_console", str="Invalide file", foreground_color="red")
        raise ValueError

    start_time_exp = data_data[index][25:-1]
    start_time_exp = datetime.strptime(start_time_exp, '%m/%d/%Y %H:%M:%S.%f')
    data["start_time_exp"] = start_time_exp

    while data_data[index][0:4] != "mode":
        index += 1

    data_row = []

    mot = ''

    for i in range(len(data_data[index])):
        if data_data[index][i] == '\t':
            if mot == "Ewe/V":
                data_row.append("Ecell/V")
                data["Ecell/V"] = []
                mot = ""
            else:
                data_row.append(mot)
                data[mot] = []
                mot = ""
        else:
            if data_data[index][i] == " ":
                mot += "_"
            else:
                mot += data_data[index][i]
    data = create_data(data_data[index + 1:], data, data_row)

    return data


def create_data(data_data, data, data_row):
    if len(data_row) == 0:
        raise ValueError("Le fichier ne correspond pas à l'expérience indiqué")

    data = work([data, data_data, data_row])
    data["row_data"] = data_row
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


def get_index(array, value):
    index = 0
    while value > array[index]:
        index += 1
    return index


def create_time(ec_lab_paths, root_folder):
    emit = Emit()


    start_global_time = None
    delta_t_electroch_dif = None
    try:
        ec_lab_files = []
        for ec_lab_path in ec_lab_paths:
            ec_lab_files.append(extract_data_cccv(ec_lab_path))
    except ValueError as err:
        emit.emit("msg_console", type="msg_console", str="Invalide file", foreground_color="red")
        raise err

    cycle_folders = get_file_from_dir(root_folder, "dir")

    if len(cycle_folders) == 0:
        emit.emit("msg_console", type="msg_console", str="No cycle found", foreground_color="red")
        raise ValueError
    else:
        emit.emit("msg_console", type="msg_console", str="rewriting in progress", foreground_color="yellow")

        fail = None

        for i, cycle_folder in enumerate(cycle_folders):

            ec_lab_file = ec_lab_files[i]
            start_time_ec_lab = ec_lab_file["start_time_exp"]

            dir_path = get_file_from_dir(cycle_folder, "dir")

            if len(dir_path) != 2 or ((dir_path[0][-5:-1] != "saxs" or dir_path[1][-5:-1] != "waxs") and
                                      (dir_path[1][-5:-1] != "saxs" or dir_path[0][-5:-1] != "waxs")):
                emit.emit("msg_console", type="msg_console", str="The directory does not have the right structure",
                          foreground_color="red")
                raise ValueError

            paths_h5 = get_file_from_dir(cycle_folder, "h5")
            if len(paths_h5) == 0:
                emit.emit("msg_console", type="msg_console", str="Fichier h5 introuvable " + cycle_folder,
                          foreground_color="red")
                raise ValueError
            else:
                names_h5 = []
                for path_h5 in paths_h5:
                    names_h5.append(path_h5[len(cycle_folder):])
            for name_h5 in names_h5:
                h5_file = h5py.File(cycle_folder + name_h5)

                # on parcours les key en ordered par int key
                for key, value in sorted(h5_file.items(), key=lambda item: float(item[0])):
                    if 'measurement' in value:
                        if 'p3' in value["measurement"]:
                            try:
                                srcur = np.array(value['instrument']['srcur']['data'])
                                index = 0
                                try:
                                    while index < len(srcur) and int(srcur[index]) > 180:
                                        index += 1

                                    if index != len(srcur):
                                        fail = srcur[index]
                                        print(key)
                                        print(fail)
                                    else:
                                        fail = None
                                except TypeError:
                                    if srcur < 180:
                                        fail = srcur
                                        print(key)
                                        print(fail)
                                    else:
                                        fail = None
                            except KeyError:
                                print(key)

                            try:
                                list_time = []

                                epoch = np.array(value['measurement/epoch'])

                                if start_global_time is None:
                                    start_global_time = epoch[0]
                                    temp = str(np.array(value["start_time"]))[2:-7]
                                    temp = datetime.strptime(temp, '%Y-%m-%dT%H:%M:%S.%f')

                                    delta_t_electroch_dif = (start_time_ec_lab - temp).total_seconds()

                                for time in epoch:
                                    list_time.append(time - start_global_time - delta_t_electroch_dif)

                                for i in range(len(epoch)):
                                    outfile = cycle_folder + "waxs/" + name_h5[:-3] + name_h5[:-3] + '_{:0>4d}'.format(
                                        int(key[:-2])) + '_{:0>4d}'.format(
                                        i) + '.dat'

                                    file = open(outfile, "r")
                                    lines = file.readlines()
                                    file.close()

                                    if fail is None:
                                        lines.insert(0, "# valid data\n")
                                    else:
                                        lines.insert(0, "# invalid data: beam " + str(fail) + "\n")

                                    lines.insert(1, "# time/s electroch: " + str(list_time[i]) + "\n")

                                    if list_time[i] >= 0:
                                        index = get_index(ec_lab_file["time/s"], list_time[i])
                                        lines.insert(2,
                                                     "# Ecell/V electroch: " + str(ec_lab_file["Ecell/V"][index]) + "\n")
                                        lines.insert(3,
                                                     "# <I>/mA electroch: " + str(ec_lab_file["<I>/mA"][index]) + "\n")
                                    else:
                                        lines.insert(2, "# Ecell/V electroch: not started\n")
                                        lines.insert(3, "# <I>/mA electroch: not started\n")

                                    file = open(outfile, "w")
                                    file.writelines(lines)
                                    file.close()

                            except Exception:
                                pass
                        else:

                            try:
                                srcur = np.array(value['instrument']['srcur']['data'])
                                index = 0
                                try:
                                    while index < len(srcur) and int(srcur[index]) > 180:
                                        index += 1

                                    if index != len(srcur):
                                        fail = srcur[index]
                                        print(key)
                                        print(fail)
                                    else:
                                        fail = None
                                except TypeError:
                                    if srcur < 180:
                                        fail = srcur
                                        print(key)
                                        print(fail)
                                    else:
                                        fail = None
                            except KeyError:
                                print(key)


                            try:
                                list_time = []

                                epoch = np.array(value['measurement/epoch'])

                                if start_global_time is None:
                                    start_global_time = epoch[0]
                                    temp = str(np.array(value["start_time"]))[2:-7]
                                    temp = datetime.strptime(temp, '%Y-%m-%dT%H:%M:%S.%f')

                                    delta_t_electroch_dif = start_time_ec_lab - temp

                                try:
                                    for time in epoch:
                                        list_time.append(time - start_global_time - delta_t_electroch_dif)
                                except TypeError:
                                    list_time.append(epoch - start_global_time - delta_t_electroch_dif)

                                if isinstance(epoch, numpy.ndarray):
                                    for i in range(len(epoch)):
                                        outfile = cycle_folder + "saxs" + name_h5[:-3] + name_h5[
                                                                                         :-3] + '_{:0>4d}'.format(
                                            int(key[:-2])) + '_{:0>4d}'.format(
                                            i) + '.dat'

                                        file = open(outfile, "r")
                                        lines = file.readlines()
                                        file.close()

                                        if fail is None:
                                            lines.insert(0, "# valid data\n")
                                        else:
                                            lines.insert(0, "# invalid data: beam " + str(fail) + "\n")

                                        lines.insert(1, "# time/s electroch: " + str(list_time[i]) + "\n")

                                        if list_time[i] >= 0:
                                            index = get_index(ec_lab_file["time/s"], list_time[i])
                                            lines.insert(2, "# Ecell/V electroch: " + str(
                                                ec_lab_file["Ecell/V"][index]) + "\n")
                                            lines.insert(3, "# <I>/mA electroch: " + str(
                                                ec_lab_file["<I>/mA"][index]) + "\n")
                                        else:
                                            lines.insert(2, "# Ecell/V electroch: not started\n")
                                            lines.insert(3, "# <I>/mA electroch: not started\n")

                                        file = open(outfile, "w")
                                        file.writelines(lines)
                                        file.close()

                                else:
                                    outfile = cycle_folder + "saxs" + name_h5[:-3] + name_h5[:-3] + '_{:0>4d}'.format(
                                        int(key[:-2])) + '_{:0>4d}'.format(0) + '.dat'

                                    file = open(outfile, "r")
                                    lines = file.readlines()
                                    file.close()

                                    lines.insert(0, "# time/s electroch: " + str(list_time[i]) + "\n")

                                    if list_time[i] >= 0:
                                        index = get_index(ec_lab_file["time/s"], list_time[i])
                                        lines.insert(1,
                                                     "# Ecell/V electroch: " + str(ec_lab_file["Ecell/V"][index]) + "\n")
                                        lines.insert(2,
                                                     "# <I>/mA electroch: " + str(ec_lab_file["<I>/mA"][index]) + "\n")
                                    else:
                                        lines.insert(1, "# Ecell/V electroch: not started\n")
                                        lines.insert(2, "# <I>/mA electroch: not started\n")

                                    file = open(outfile, "w")
                                    file.writelines(lines)
                                    file.close()

                            except Exception:
                                pass

        emit.emit("msg_console", type="msg_console", str="Done", foreground_color="green")


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
                    if ext == "dir":
                        if os.path.isdir(path + "/" + f + "/"):
                            res.append(path + "/" + f + "/")
                    else:
                        if f[len(f) - len(ext):] == ext:
                            res.append(path + "/" + f)
                else:
                    res.append(path + "/" + f)
            return res
