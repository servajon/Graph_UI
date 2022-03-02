import Resources_file.Resources
from Data_type.Ihch_1501 import Ihch_1501_cycle, Ihch_1501_sample_saxs, Ihch_1501_scan, Ihch_1501_frame, \
    Ihch_1501_sample_waxs
from Resources_file.Emit import Emit


def open_ihch_1501(_dir_path):
    emit = Emit()
    emit.emit("msg_console", type="msg_console", str="Lecture des fichiers en cours", foreground_color="yellow")
    cycles = []
    dir_path = Resources_file.Resources.get_file_from_dir(_dir_path)
    for cycle_path in dir_path:
        cycles.append(Ihch_1501_cycle(cycle_path.split("/")[-1]))
        cycle_path += "/"
        samples_path = Resources_file.Resources.get_file_from_dir(cycle_path)
        if "SAXS" in samples_path[0]:
            saxs_paths = samples_path[0] + "/"
            waxs_paths = samples_path[1] + "/"
        else:
            saxs_paths = samples_path[1] + "/"
            waxs_paths = samples_path[0] + "/"

        saxs_paths = Resources_file.Resources.get_file_from_dir(saxs_paths)
        waxs_paths = Resources_file.Resources.get_file_from_dir(waxs_paths)

        for saxs_path in saxs_paths[1:]:
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
                cycles[-1].saxs[-1].scans[-1].frames[-1].data = read_frame(file)

        for waxs_path in waxs_paths[1:]:
            cycles[-1].waxs.append(Ihch_1501_sample_waxs(waxs_path.split("/")[-1]))
            waxs_path += "/"

            file_paths = Resources_file.Resources.get_file_from_dir(waxs_path)

            current = file_paths[0][-13:-9]
            cycles[-1].waxs[-1].scans.append(Ihch_1501_scan(current))
            for file_path in file_paths:
                if file_path[-13:-9] != current:
                    current = file_path[-13:-9]
                    cycles[-1].waxs[-1].scans.append(Ihch_1501_scan(current))

                cycles[-1].waxs[-1].scans[-1].frames.append(Ihch_1501_frame(file_path[-8:-4]))
                file = open(file_path)
                cycles[-1].waxs[-1].scans[-1].frames[-1].data = read_frame(file)
    return cycles


def read_frame(file):
    data = {}

    data_data = file.readlines()
    index = 0

    if "# time :" not in data_data[1]:
        raise TypeError

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
