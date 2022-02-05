import os
import copy
import multiprocessing as mp
from Python_files.Resources.Affiche_objet import Array_Abstract_objet_affiche
from Python_files.Resources import Resource as R
import Python_files.Resources.Install as install

try:
    from galvani import BioLogic
except ModuleNotFoundError:
    install.install("galvani")
    from galvani import BioLogic


def extract_data_mpr(path, type_exp, format_time=None):
    resource = R.Resource_class()
    resource.print_color("Lecture du fichier en cours", "work")

    "----------------------------------------------------------"

    obj_data = Array_Abstract_objet_affiche()
    obj_data.event_thread1.set()
    obj_data.stop_main = True
    obj_data.event_thread2.wait()
    mpr_file = BioLogic.MPRfile(path)
    obj_data.stop_main = False
    obj_data.event_thread1.set()
    obj_data.event_thread1.clear()
    obj_data.event_thread2.clear()

    "----------------------------------------------------------"

    data = {}
    row_data = []

    for flag in mpr_file.flags_dict:
        row_data.append(flag)
        data[flag] = []
    name_data = str(mpr_file.dtype)
    i = 0
    while i < len(name_data):
        if name_data[i] == '(':
            i += 2
            index_start = i
            while name_data[i] != "'":
                i += 1
            mot = name_data[index_start:i]
            if mot == "time/s":
                if format_time == "s":
                    row_data.append("time/s")
                    data["time/s"] = []
                elif format_time == "min":
                    row_data.append("time/min")
                    data["time/min"] = []
                else:
                    row_data.append("time/h")
                    data["time/h"] = []
            elif mot == "Ewe/V" or mot == "<Ewe>/V":
                row_data.append("Ecell/V")
                data["Ecell/V"] = []
            elif mot == "I/mA":
                row_data.append("<I>/mA")
                data["<I>/mA"] = []
            elif name_data[index_start:i] != "flags":
                mot = name_data[index_start:i]
                row_data.append(mot)
                data[mot] = []
        i += 1

    data["name"] = "no_name_found"
    data["mass_electrode"] = -1
    flag = []
    for i in mpr_file.flags_dict.items():
        flag.append(i[0])

    try:
        data = create_data(mpr_file.data, flag, mpr_file, data, row_data)
    except ValueError:
        resource.print_color("Fichier contenant des valeurs invalides : UNKVAR", "fail")
        raise ValueError
    else:
        if "<I>/mA" not in data["row_data"]:
            create_i(data)

        print(data["loop_data"])
        if data["loop_data"] == -1:
            if type_exp == "cccv":
                create_loop_cccv(data)
            elif type_exp == "impedance":
                create_loop_impedance(data)
            else:
                raise NotImplementedError
            print(data["loop_data"])

        for i in range(len(data["row_data"])):
            if " " in data["row_data"][i]:
                newmot = ""
                for j in data["row_data"][i]:
                    if j == " ":
                        newmot += "_"
                    else:
                        newmot += j
                data["row_data"][i] = newmot

        temp = []
        for key in data.keys():
            temp.append(key)

        for i in range(len(data["row_data"])):
            new_index = data["row_data"][i]
            old_index = temp[i]
            if new_index != old_index:
                data[new_index] = data[temp[i]]
                del data[old_index]

        if "Q_charge/discharge/mA.h" in row_data:
            data["row_data"].remove("Q_charge/discharge/mA.h")
            row_data.append("Q_discharge/mA.h")
            row_data.append("Q_charge/mA.h")
            data["Q_discharge/mA.h"] = []
            data["Q_charge/mA.h"] = []
            for val in data["Q_charge/discharge/mA.h"]:
                if val < 0:
                    data["Q_discharge/mA.h"].append(-val)
                    data["Q_charge/mA.h"].append(0)
                else:
                    data["Q_discharge/mA.h"].append(0)
                    data["Q_charge/mA.h"].append(val)
            del data["Q_charge/discharge/mA.h"]

            if len(data["Q_discharge/mA.h"]) > 30 and data["Q_discharge/mA.h"][30] == 0:
                print("charge")
                """on commence par une charge"""
                data["Efficiency/%"] = []
                index = 30
                br = False
                for loop in data["loop_data"]:
                    while index < len(data["Q_discharge/mA.h"]) and data["Q_discharge/mA.h"][index] == 0:
                        index += 1
                    if index != len(data["Q_discharge/mA.h"]):
                        charge = data["Q_charge/mA.h"][index - 1]
                    else:
                        br = True

                    while index < len(data["Q_charge/mA.h"]) and data["Q_charge/mA.h"][index] == 0:
                        index += 1
                    if index != len(data["Q_charge/mA.h"]):
                        decharge = data["Q_discharge/mA.h"][index - 1]
                    else:
                        br = True
                    for j in range(loop[0], loop[1]):
                        data["Efficiency/%"].append(0)
                    data["Efficiency/%"].append(decharge / charge * 100)
                    if br:
                        break
            else:
                """PAS ENCORE FAIT, faire l'effichiancy % pour la décharge, pareil que pour la charge mais si 
                on commence par une décharge le premier cycle est mis à 0, basiquement on skip le premier et on fait
                 comme pour la charge sur le reste"""
                print("decharge")
                data["Efficiency/%"] = []
                index = 30
                br = False
                for i in range(data["loop_data"][0][0], data["loop_data"][0][1] + 1):
                    data["Efficiency/%"].append(0)
                print(len(data["Efficiency/%"].append(0)))

                for loop in data["loop_data"]:
                    while index < len(data["Q_discharge/mA.h"]) and data["Q_discharge/mA.h"][index] == 0:
                        index += 1
                    if index != len(data["Q_discharge/mA.h"]):
                        charge = data["Q_charge/mA.h"][index - 1]
                    else:
                        br = True

                    while index < len(data["Q_charge/mA.h"]) and data["Q_charge/mA.h"][index] == 0:
                        index += 1
                    if index != len(data["Q_charge/mA.h"]):
                        decharge = data["Q_discharge/mA.h"][index - 1]
                    else:
                        br = True
                    for j in range(loop[0], loop[1]):
                        data["Efficiency/%"].append(0)
                    data["Efficiency/%"].append(decharge / charge * 100)
                    if br:
                        break
        return data


def create_data(data_data, flag, mprfile, data, data_row):
    resource = R.Resource_class()
    if len(data_row) == 0:
        resource.print_color("Le fichier ne correspond pas à l'expérience indiqué", "fail")
        raise ValueError
    loop_data = mprfile.loop_index
    if loop_data is not None:
        loop_data_new = []
        i = 1
        index_start = loop_data[0]
        while i < len(loop_data):
            loop_data_new.append([index_start, loop_data[i] - 1])
            index_start = loop_data[i]
            i += 1
        loop_data = loop_data_new
    else:
        if "cycle number" not in data_row:
            loop_data = -1

    if len(data_data) < 50000:
        if loop_data is not None:
            data = work([data, flag, mprfile, data_data, data_row])
            data["loop_data"] = loop_data
            data["row_data"] = data_row
        else:
            data = work_loop([data, flag, mprfile, data_data, data_row])
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

                array_data.append([copy.deepcopy(data), flag, mprfile,
                                   copy.deepcopy(data_data[start:end]), data_row, start])
                start += pas + 1

            array_data.append([copy.deepcopy(data), flag, mprfile,
                               copy.deepcopy(data_data[start:]), data_row, start])
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
                array_data.append([copy.deepcopy(data), flag, mprfile,
                                   copy.deepcopy(data_data[start:end]), data_row])
                start += pas + 1

            array_data.append([copy.deepcopy(data), flag, mprfile,
                               copy.deepcopy(data_data[start:]), data_row])
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
    flag = args[1]
    mprfile = args[2]
    data_data = args[3]
    data_row = args[4]

    start = len(mprfile.flags_dict)
    for i in range(len(data_data)):
        index_row = start
        for j in range(len(flag)):
            res = mprfile.get_flag(flag[j])[i]
            if res != 0 and res != 1:
                data[flag[j]].append(res)
            elif not res:
                data[flag[j]].append(0)
            else:
                data[flag[j]].append(1)
        for j in range(1, len(data_data[i])):
            if data_row[index_row] == "time/h":
                data[data_row[index_row]].append(data_data[i][j] / 3600)
            elif data_row[index_row] == "time/min":
                data[data_row[index_row]].append(data_data[i][j] / 60)
            else:
                data[data_row[index_row]].append(data_data[i][j])
            index_row += 1
    return data


def work_loop(args):
    data = args[0]
    flag = args[1]
    mprfile = args[2]
    data_data = args[3]
    data_row = args[4]
    loop_data = []

    ligne_count = 0
    current_loop = None
    start_loop = None

    start = len(mprfile.flags_dict)
    for i in range(len(data_data)):
        index_row = start
        for j in range(len(flag)):
            res = mprfile.get_flag(flag[j])[i]
            if res != 0 and res != 1:
                data[flag[j]].append(res)
            elif res is False:
                data[flag[j]].append(0)
            else:
                data[flag[j]].append(1)
            index_row += 1
        for j in range(1, len(data_data[i])):
            if data_row[index_row] == "time/h":
                data[data_row[index_row]].append(data_data[i][j] / 3600)
            elif data_row[index_row] == "time/min":
                data[data_row[index_row]].append(data_data[i][j] / 60)
            elif data_row[index_row] == "cycle number" and data_data[i][j] != current_loop:
                if start_loop is None:
                    start_loop = current_loop

                current_loop = int(data_data[i][j])
                if len(loop_data) > 0:
                    loop_data[current_loop - start_loop - 1][1] = ligne_count - 1
                    loop_data[current_loop - start_loop - 1][2] = current_loop - 1

                loop_data.append([ligne_count, None, None])
            else:
                data[data_row[index_row]].append(data_data[i][j])
            index_row += 1
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
        if (time[i] - time[i - 1]) > pas * 2:
            loop_data.append([index_min, i - 1])
            index_min = i
        i += 1
    loop_data.append([index_min, len(time) - 1])
    return loop_data


def create_loop_cccv(data):
    index = 0
    loop_data = []
    start = None

    while data["<I>/mA"][index] == 0:
        index += 1

    if data["<I>/mA"][index] < 0:
        """négatif first"""
        while index < len(data["<I>/mA"]) and data["<I>/mA"][index] <= 0:
            index += 1
        loop_data.append([0, index - 1])
        start = index

    while index < len(data["<I>/mA"]):
        if start is None:
            start = 0
        else:
            start = index
        while index < len(data["<I>/mA"]) and data["<I>/mA"][index] >= 0:
            index += 1
        while index < len(data["<I>/mA"]) and data["<I>/mA"][index] < 0:
            index += 1
        loop_data.append([start, index - 1])

    data["loop_data"] = loop_data


def create_loop_impedance(data):
    index = 0
    while data["freq/Hz"][index] == 0:
        index += 1

    freq_start = data["freq/Hz"][index]
    index += 1
    start = 0
    loop_data = []
    while index < len(data["freq/Hz"]):
        while index < len(data["freq/Hz"]) and freq_start != data["freq/Hz"][index]:
            index += 1
        loop_data.append([start, index - 1])
        start = index
    data["loop_data"] = loop_data


def create_i(data):
    I = [0]
    array_data = []
    nb_pross = os.cpu_count()
    start = 0
    pas = int(len(data["(Q-Qo)/mA.h"]) / nb_pross)

    if "time/h" in data["row_data"]:
        for i in range(nb_pross - 1):
            start = start
            end = start + pas + 1
            if start != 0:
                array_data.append([data["(Q-Qo)/mA.h"][start - 1:end], data["time/h"][start - 1:end]])
            else:
                array_data.append([data["(Q-Qo)/mA.h"][start:end], data["time/h"][start:end]])
            start += pas + 1
        array_data.append([data["(Q-Qo)/mA.h"][start - 1:], data["time/h"][start - 1:]])
        with mp.Pool() as pool:
            res = pool.map(work_i_h, array_data)
    elif "time/min" in data["row_data"]:
        for i in range(nb_pross - 1):
            start = start
            end = start + pas + 1
            if start != 0:
                array_data.append([data["(Q-Qo)/mA.h"][start - 1:end], data["time/min"][start - 1:end]])
            else:
                array_data.append([data["(Q-Qo)/mA.h"][start:end], data["time/min"][start:end]])
            start += pas + 1
        array_data.append([data["(Q-Qo)/mA.h"][start - 1:], data["time/min"][start - 1:]])
        with mp.Pool() as pool:
            res = pool.map(work_i_min, array_data)
    else:
        for i in range(nb_pross - 1):
            start = start
            end = start + pas + 1
            if start != 0:
                array_data.append([data["(Q-Qo)/mA.h"][start - 1:end], data["time/s"][start - 1:end]])
            else:
                array_data.append([data["(Q-Qo)/mA.h"][start:end], data["time/s"][start:end]])
            start += pas + 1
        array_data.append([data["(Q-Qo)/mA.h"][start - 1:], data["time/s"][start - 1:]])
        with mp.Pool() as pool:
            res = pool.map(work_i_s, array_data)

    for r in res:
        I.extend(r)
    data["<I>/mA"] = I
    data["row_data"].append("<I>/mA")


def work_i_h(args):
    q = args[0]
    time = args[1]
    res = []
    index = 1
    count = 0
    while index < len(q):
        calc = (q[index] - q[index - 1]) / (time[index] - time[index - 1])
        count += abs(calc)
        res.append(calc)
        index += 1
    moy = count / len(q)
    for i in range(len(res)):
        if abs(res[i]) > 1.5 * moy:
            res[i] = 0
    return res


def work_i_min(args):
    q = args[0]
    time = args[1]
    res = []
    index = 1
    count = 0
    while index < len(q):
        calc = (q[index] - q[index - 1] * 60) / (time[index] - time[index - 1])
        count += calc
        res.append(calc)
        index += 1
    moy = count / len(q)
    for i in range(len(res)):
        if abs(res[i]) > 1.5 * moy:
            res[i] = 0
    return res


def work_i_s(args):
    q = args[0]
    time = args[1]
    res = []
    index = 1
    count = 0
    while index < len(q):
        calc = (q[index] - q[index - 1] * 3600) / (time[index] - time[index - 1])
        res.append(calc)
        count += calc
        index += 1
    moy = count / len(q)
    for i in range(len(res)):
        if abs(res[i]) > 1.5 * moy:
            res[i] = 0
    return res
