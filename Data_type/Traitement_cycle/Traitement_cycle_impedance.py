from Console_Objets.Data_Unit import Data_unit
from Console_Objets.Data_array import Data_array
from Console_Objets.Figure import Figure
from Data_type.Traitement_cycle import Traitements_cycle_outils
from Resources_file.Emit import Emit


def cycle_impedance(figure, cycle):
    """
    La figure passé en param a été crée avec une commande, il n'y a donc presque rien à faire,
    c'est juste de la selection de data_array a ajouter à la nouvelle figure

    :param figure: figure issus de la commande diffraction
    :param cycle: cycles sélectionnés
    :return: nouvelle figure
    """

    new_figure = Figure("", 1)

    # La figure a été crée avec la commande diffraction, pas trop de trucs à faire
    for i in cycle:
        data_array_x = figure.x_axe.data[i].copy()
        data_array_y = figure.y1_axe.data[i].copy()

        new_figure.add_data_x_Data(data_array_x)
        new_figure.add_data_y1_Data(data_array_y)

        if figure.z1_axe is not None:
            data_array_z = figure.z1_axe.data[i].copy()
            new_figure.add_data_z1_Data(data_array_z)

    if figure.y2_axe is not None:
        for i in cycle:
            data_array_x = figure.x_axe.data[i].copy()
            data_array_y = figure.y2_axe.data[len(figure.y1_axe.data) + i].copy()

            new_figure.add_data_x_Data(data_array_x)
            new_figure.add_data_y2_Data(data_array_y)

    new_figure.type = figure.type + "_cycle"
    new_figure.created_from = figure
    new_figure.aspect = figure.aspect

    return new_figure


# je laisse ce biout de code là, il servira dans le cas ou il sera demandé de faire du traitement de cycle sur une
# figure custom sur de l'impedance

def cycle_impedance2(figure, loop_data, freq_data, cycle):
    """
    Prend en argument une figure, loop data et mode_data, loop_data et mode_data sont des dictionnaires
    mode_data sert a suprimer les plateaux et loop data pour créer les cycles
    return la figure créée

    si cycle == None => cycle all, on créer un vecteur avec les cycle pour garder la même structure de code
    is_cycle_none garde trace de si à l'origine cycle est None, utilisé pour le nom de la figure

    :param figure: figure de base sur laquelle on traite les cycles

    :param loop_data: dictionaire ayant pour clé le nom d'un fichier de donnée ouvert et pour value
                      une list contenant les index des loop du fichier ec_lab correspondant

    :param freq_data: dictionaire ayant pour clé le nom d'un fichier de donnée ouvert et pour value
                      une list contenant la colone freq du fichier ec_lab correspondant

    :param cycle: list contenant la liste des cycles que l'on souhaite selectionner, si None => all

    :return: nouvelle figure issu du traitmement
    """

    emit = Emit()

    unit_x = figure.x_axe.get_unit()
    unit_y = figure.y1_axe.get_unit()

    # key : cycle number
    # value : [data_name, res]
    # res : -1 => cycle invalide on le discard
    # res : number != 1 => index du centre, le demi cycle est valide
    del_cycle = {}

    for i in loop_data:
        res = last_cycle_valide(loop_data[i], freq_data[i])
        if res != 1:
            del_cycle[i] = [len(loop_data[i]) - 1, res]

    # Création de la nouvelle figure, elle est dirty
    new_figure = Figure("", 1)

    new_figure.type = "impedance_cycle"

    for i in range(len(cycle)):

        # On récupére les données de data_y1 de current_figure
        # On associe à chaque data_y1 un nouveaux data_x de même taille
        # Obligatoire car les différents cycle n'ont pas le même nombre de point
        for j in range(len(figure.y1_axe.data)):
            if cycle[i] >= len(loop_data[figure.y1_axe.data[j].source]):
                continue

            # On récucpére premier et le dernier point correspondant au cycle en cours
            val_min = loop_data[figure.y1_axe.data[j].source][cycle[i]][0]
            val_max = loop_data[figure.y1_axe.data[j].source][cycle[i]][1]

            if val_max - val_min < 20:
                emit.emit("msg_console", type="msg_console", str="Cycle " + str(cycle[i] + 1) + " discard",
                          foreground_color="yellow")
                continue

            # On discard le dernier cycle si pas fini, le traitement n'a pas de sens sur la normalisation avec un
            # cycle incomplet, totalement ou partiellement
            if figure.y1_axe.data[j].source in del_cycle and del_cycle[figure.y1_axe.data[j].source][0] == cycle[i]:
                if del_cycle[figure.y1_axe.data[j].source][1] != 1:
                    emit.emit("msg_console", type="msg_console", str="Discard cycle " + str(cycle[i] + 1) + " y1",
                             foreground_color="yellow")
                    continue

            global_index = [val for val in range(val_min, val_max)]

            res = [figure.x_axe.data[j].data[val_min:val_max], figure.y1_axe.data[j].data[val_min:val_max]]

            Traitements_cycle_outils.start_0(res[0])

            data_unit_x = Data_unit(res[0], unit_x)
            data_unit_y1 = Data_unit(res[1], unit_y)

            data_array_x = Data_array(data_unit_x, figure.x_axe.data[j].name, figure.x_axe.data[j].source,
                                                  "cycle " + str(cycle[i] + 1))
            data_array_x.global_index = global_index

            data_array_y = Data_array(data_unit_y1, figure.y1_axe.data[j].name, figure.y1_axe.data[j].source,
                                      "cycle " + str(cycle[i] + 1))

            new_figure.add_data_x_Data(data_array_x)

            new_figure.add_data_y1_Data(data_array_y)

    if len(figure.data_y2) > 0:
        unit_y = figure.y2_axe.get_unit()

        for i in range(len(cycle)):
            # On récupére les données de data_y1 de current_figure
            # On associe à chaque data_y1 un nouveaux data_x de même taille
            # Obligatoire car les différents cycle n'ont pas le même nombre de point
            for j in range(len(figure.data_y2)):
                if cycle[i] >= len(loop_data[figure.data_y2[j].source]):
                    continue

                # On récucpére premier et le dernier point correspondant au cycle en cours
                val_min = loop_data[figure.data_y2[j].source][cycle[i]][0]
                val_max = loop_data[figure.data_y2[j].source][cycle[i]][1]

                if val_max - val_min < 20:
                    emit.emit("msg_console", type="msg_console", str="Cycle " + str(cycle[i] + 1) + " discard",
                              foreground_color="yellow")
                    continue

                # On discard le dernier cycle si pas fini, le traitement n'a pas de sens sur la normalisation avec un
                # cycle incomplet, totalement ou partiellement
                if figure.data_y2[j].source in del_cycle and del_cycle[figure.data_y2[j].source][0] == i:
                    if del_cycle[figure.data_y2[j].source][1] != 1:
                        emit.emit("msg_console", type="msg_console", str="Discard cycle " + str(cycle[i] + 1) + " y2",
                                  foreground_color="yellow")
                        continue

                global_index = [val for val in range(val_min, val_max)]

                res = [figure.x_axe.data[j].data[val_min:val_max], figure.data_y2[j].data[val_min:val_max]]

                Traitements_cycle_outils.start_0(res[0])


                data_unit_x = Data_unit(res[0], unit_x)
                data_unit_y2 = Data_unit(res[1], unit_y)

                data_array_x = Data_array(data_unit_x, figure.x_axe.data[j].name, figure.x_axe.data[j].source,
                                          "cycle " + str(cycle[i] + 1))
                data_array_x.global_index = global_index

                data_array_y2 = Data_array(data_unit_y2, figure.y2_axe.data[j].name, figure.y2_axe.data[j].source,
                                          "cycle " + str(cycle[i] + 1))

                new_figure.add_data_x_Data(data_array_x)

                new_figure.add_data_y2_Data(data_array_y2)

    if len(figure.data_z1) > 0:

        unit_z = figure.z1_axe.get_unit()

        for i in range(len(cycle)):
            # On récupére les données de data_y1 de current_figure
            # On associe à chaque data_y1 un nouveaux data_x de même taille
            # Obligatoire car les différents cycle n'ont pas le même nombre de point
            for j in range(len(figure.data_z1)):
                if cycle[i] >= len(loop_data[figure.data_z1[j].source]):
                    continue

                # On récucpére premier et le dernier point correspondant au cycle en cours
                val_min = loop_data[figure.data_y2[j].source][cycle[i]][0]
                val_max = loop_data[figure.data_y2[j].source][cycle[i]][1]

                if val_max - val_min < 20:
                    emit.emit("msg_console", type="msg_console", str="Cycle " + str(cycle[i] + 1) + " discard",
                              foreground_color="yellow")

                # On discard le dernier cycle si pas fini, le traitement n'a pas de sens sur la normalisation avec un
                # cycle incomplet, totalement ou partiellement
                if figure.data_y2[j].source in del_cycle and del_cycle[figure.data_y2[j].source][0] == i:
                    if del_cycle[figure.data_y2[j].source][1] != 1:
                        emit.emit("msg_console", type="msg_console", str="Discard cycle " + str(cycle[i] + 1) + " y1",
                                  foreground_color="yellow")
                        continue

                res = [figure.x_axe.data[j].data[val_min:val_max], figure.data_y2[j].data[val_min:val_max]]

                global_index = [val for val in range(val_min, val_max)]

                Traitements_cycle_outils.start_0(res[0])

                data_unit_x = Data_unit(res[0], unit_x)
                data_unit_z1 = Data_unit(res[1], unit_z)

                data_array_x = Data_array(data_unit_x, figure.x_axe.data[j].name, figure.x_axe.data[j].source,
                               "cycle_" + str(cycle[i]))

                new_figure.add_data_x_Data()

                new_figure.add_data_y2_Data(Data_array(res[1], figure.data_y2[j].name, figure.data_y2[j].source,
                                                       "cycle_" + str(cycle[i] + 1)))

    if len(new_figure.x_axe.data) == 0:
        resource.print_color("Aucun cycle n'a pu être tracé", "fail")
        raise ValueError
    """   Si cycle est None au départ, la figure prends le nom all, le nom des cycle sinon """
    if is_cycle_none is None:
        new_figure.name = "cycle_all"
    else:
        new_figure.name = name

    new_figure.type = figure.type

    """ On return la figure créée """
    return new_figure


def last_cycle_valide(loop_data, freq_data):
    first_cycle = freq_data[loop_data[0][1]]
    last_cycle = freq_data[loop_data[-1][1]]

    if first_cycle * 1.05 < first_cycle and first_cycle * 0.95 > last_cycle:
        return -1
    return 1
