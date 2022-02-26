from Console_Objets.Data_Unit import Data_unit, Units
from Console_Objets.Data_array import Data_array
from Console_Objets.Figure import Figure
from Data_type.Traitement_cycle import Traitements_cycle_outils
from Resources_file import Resources
from Resources_file.Emit import Emit


def cycle_cccv(figure, loop_data, mode_data, i_data, ecell_data, cycle):
    """
    Prend en argument une figure, loop data et mode_data, loop_data et mode_data sont des dictionnaires
    mode_data sert a suprimer les plateaux et loop data pour créer les cycles
    return la figure créée

    si cycle == None => cycle all, on créer un vecteur avec les cycle pour garder la même structure de code
    is_cycle_none garde trace de si à l'origine cycle est None, utilisé pour le nom de la figure

    :param figure: figure de base sur laquelle on traite les cycles

    :param loop_data: dictionaire ayant pour clé le nom d'un fichier de donnée ouvert et pour value
                      une list contenant les index des loop du fichier ec_lab correspondant

    :param mode_data: dictionaire ayant pour clé le nom d'un fichier de donnée ouvert et pour value
                      une list contenant la colone mode du fichier ec_lab correspondant

    :param i_data: dictionaire ayant pour clé le nom d'un fichier de donnée ouvert et pour value
                      une list contenant la colone courant du fichier ec_lab correspondant

    :param ecell_data: dictionaire ayant pour clé le nom d'un fichier de donnée ouvert et pour value
                      une list contenant la colone potentiel du fichier ec_lab correspondant

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
        res = last_cycle_valide(loop_data[i], ecell_data[i], i_data[i])
        if res != 1:
            del_cycle[i] = [len(loop_data[i]) - 1, res]

    # Création de la nouvelle figure, elle est dirty
    new_figure = Figure("", 1)

    if figure.y2_axe is None:
        new_figure.type = "cycle_y1"
    else:
        new_figure.type = "cycle_y1_y2"

    name = "cycle"

    for i in range(len(cycle)):
        # On garde le nom de chaque cycle passé pour le nom de la figure
        # Utilisé uniquement si cycle is not None, all sinon
        name += "_" + str(cycle[i] + 1)

        # On récupére les données de data_y1 de current_figure
        # On associe à chaque data_y1 un nouveaux data_x de même taille
        # Obligatoire car les différents cycle n'ont pas le même nombre de point
        for j in range(len(figure.y1_axe.data)):
            # dans le cas ou il y a 2 fichier, sur un cycle all la lists des cycle
            # comprends tous les cycles de l'un des 2 fichiers. Si l'un posséde plus de cycle
            # que l'autre, on ne peux pas tracer ce cycle là
            if cycle[i] >= len(loop_data[figure.y1_axe.data[j].source]):
                continue

            # On récucpére premier et le dernier point correspondant au cycle en cours
            val_min = loop_data[figure.y1_axe.data[j].source][cycle[i]][0]
            val_max = loop_data[figure.y1_axe.data[j].source][cycle[i]][1]

            if val_max - val_min < 20:
                emit.emit("msg_console", type="msg_console", str="Cycle " + str(cycle[i] + 1) + " discard",
                          foreground_color="yellow")
                continue

            """last val représente la dernière valeur du dernier cycle, none si le cycle les valide ou discard"""

            point_centre = None

            # si le cycle correspond à un cycle du dictionaire del_cycle et qu'il vaut -1, on le discard
            if figure.y1_axe.data[j].source in del_cycle and del_cycle[figure.y1_axe.data[j].source][0] == cycle[i]:
                if del_cycle[figure.y1_axe.data[j].source][1] == -1:
                    emit.emit("msg_console", type="msg_console", str="Discard cycle " + str(cycle[i] + 1) + " y1",
                              foreground_color="yellow")
                    continue
                else:
                    emit.emit("msg_console", type="msg_console", str="Second half of cycle " + str(cycle[i] + 1) +
                                                                     " y1 discard", foreground_color="yellow")

                    # on cherche le centre du cycle
                    index_centre = find_center(val_min, val_max, i_data[figure.y1_axe.data[j].source])

                    # si il est introuvable, le cycle sera discard
                    if index_centre == -1:
                        emit.emit("msg_console", type="msg_console", str="Cycle Centre " + str(cycle[i]) +
                                                                         " untraceable", foreground_color="yellow")
                        continue

                    # on corrige l'index du centre, dans le cas ou la manip n'a pas était bien
                    # réalisé...
                    index_centre = correct_cccv_center(ecell_data[figure.y1_axe.data[j].source][val_min:val_max],
                                                       index_centre)
                    # [nouvelle index du cnetre, nombres de points suprimés avant le centre]
                    point_centre = [index_centre, 0]

            # si point centre n'est pas None, il faut regarder combien de point on suprime avant le centre
            if point_centre is None:
                # On suprime les plateaux, mode 2
                res = Traitements_cycle_outils.mode_del(figure.x_axe.data[j].data[val_min:val_max],
                                           figure.y1_axe.data[j].data[val_min:val_max],
                                           val_min, val_max, mode_data[figure.y1_axe.data[j].source], 2)

                # on suprime le mode 3, ocv
                res = Traitements_cycle_outils.mode_del(res[0], res[1], val_min, val_max,
                                                        mode_data[figure.y1_axe.data[j].source], 3)
            else:

                # On suprime les plateaux, mode 2
                res = Traitements_cycle_outils.mode_del(figure.x_axe.data[j].data[val_min:val_max],
                                           figure.y1_axe.data[j].data[val_min:val_max],
                                           val_min,
                                           val_max, mode_data[figure.y1_axe.data[j].source], 2, point_centre[0])

                # Si l'on a suprimer des valeurs avant le centre on les sauvegarde
                if len(res) == 3:
                    point_centre[1] = res[2]

                # on suprime le mode 3, ocv
                res = Traitements_cycle_outils.mode_del(res[0], res[1], val_min, val_max,
                                                        mode_data[figure.y1_axe.data[j].source], 3, point_centre[0])

                # Si l'on a suprimer des valeurs avant le centre on les sauvegarde
                if len(res) == 3:
                    point_centre[1] += res[2]

            # on fait repartir le vecteur à 0
            Traitements_cycle_outils.start_0(res[0])

            if point_centre is None:
                data_unit_x = Data_unit(res[0], unit_x)
                data_unit_y1 = Data_unit(res[1], unit_y)

                new_figure.add_data_x_Data(Data_array(data_unit_x, figure.y1_axe.data[j].name,
                                                      figure.y1_axe.data[j].source,
                                                      "cycle_" + str(cycle[i] + 1)))

                new_figure.add_data_y1_Data(Data_array(data_unit_y1, figure.y1_axe.data[j].name,
                                                       figure.y1_axe.data[j].source,
                                                       "cycle_" + str(cycle[i] + 1)))
            else:
                last_val = point_centre[0] - point_centre[1]
                data_unit_x = Data_unit(res[0][0:last_val], unit_x)
                data_unit_y1 = Data_unit(res[1][0:last_val], unit_y)

                new_figure.add_data_x_Data(Data_array(data_unit_x, figure.y1_axe.data[j].name,
                                                      figure.y1_axe.data[j].source,
                                                      "cycle_" + str(cycle[i] + 1)))

                new_figure.add_data_y1_Data(Data_array(data_unit_y1, figure.y1_axe.data[j].name,
                                                       figure.y1_axe.data[j].source,
                                                       "cycle_" + str(cycle[i] + 1)))
    if figure.y2_axe is not None:
        unit_y = figure.y2_axe.get_unit()

        for i in range(len(cycle)):

            # On récupére les données de data_y2 de current_figure
            # On associe à chaque data_y2 un nouveaux data_x de même taille
            # Obligatoire car les différents cycle n'ont pas le même nombre de point
            for j in range(len(figure.y2_axe.data)):

                # dans le cas ou il y a 2 fichier, sur un cycle all la lists des cycle
                # comprends tous les cycles de l'un des 2 fichiers. Si l'un posséde plus de cycle
                # que l'autre, on ne peux pas tracer ce cycle là
                if cycle[i] >= len(loop_data[figure.y2_axe.data[j].source]):
                    continue

                # On récucpére premier et le dernier point correspondant au cycle en cours
                val_min = loop_data[figure.y2_axe.data[j].source][cycle[i]][0]
                val_max = loop_data[figure.y2_axe.data[j].source][cycle[i]][1]

                if val_max - val_min < 20:
                    emit.emit("msg_console", type="msg_console", str="Cycle " + str(cycle[i] + 1) + " discard",
                              foreground_color="yellow")
                    continue

                """last val représente la dernière valeur du dernier cycle, none si le cycle les valide ou discard"""

                point_centre = None

                # si le cycle correspond à un cycle du dictionaire del_cycle et qu'il vaut -1, on le discard
                if figure.y2_axe.data[j].source in del_cycle and del_cycle[figure.y2_axe.data[j].source][0] == cycle[i]:
                    if del_cycle[figure.y2_axe.data[j].source][1] == -1:
                        emit.emit("msg_console", type="msg_console", str="Discard cycle " + str(cycle[i] + 1) + " y2",
                                  foreground_color="yellow")
                        continue
                    else:
                        emit.emit("msg_console", type="msg_console", str="Second half of cycle " + str(cycle[i] + 1) +
                                                                         " y2 discard", foreground_color="yellow")

                        # on cherche le centre du cycle
                        index_centre = find_center(val_min, val_max, i_data[figure.y2_axe.data[j].source])

                        # si il est introuvable, le cycle sera discard
                        if index_centre == -1:
                            emit.emit("msg_console", type="msg_console", str="Cycle Centre " + str(cycle[i]) +
                                                                             " untraceable", foreground_color="yellow")
                            continue

                        # on corrige l'index du centre, dans le cas ou la manip n'a pas était bien
                        # réalisé...
                        index_centre = correct_cccv_center(ecell_data[figure.y2_axe.data[j].source][val_min:val_max],
                                                           index_centre)
                        # [nouvelle index du cnetre, nombres de points suprimés avant le centre]
                        point_centre = [index_centre, 0]

                # si point centre n'est pas None, il faut regarder combien de point on suprime avant le centre
                if point_centre is None:
                    # On suprime les plateaux, mode 2
                    res = Traitements_cycle_outils.mode_del(figure.x_axe.data[j].data[val_min:val_max],
                                                            figure.y2_axe.data[j].data[val_min:val_max],
                                                            val_min, val_max, mode_data[figure.y2_axe.data[j].source],
                                                            2)

                    # on suprime le mode 3, ocv
                    res = Traitements_cycle_outils.mode_del(res[0], res[1], val_min, val_max,
                                                            mode_data[figure.y2_axe.data[j].source], 3)
                else:

                    # On suprime les plateaux, mode 2
                    res = Traitements_cycle_outils.mode_del(figure.x_axe.data[j].data[val_min:val_max],
                                                            figure.y2_axe.data[j].data[val_min:val_max],
                                                            val_min,
                                                            val_max, mode_data[figure.y2_axe.data[j].source], 2,
                                                            point_centre[0])

                    # Si l'on a suprimer des valeurs avant le centre on les sauvegarde
                    if len(res) == 3:
                        point_centre[1] = res[2]

                    # on suprime le mode 3, ocv
                    res = Traitements_cycle_outils.mode_del(res[0], res[1], val_min, val_max,
                                                            mode_data[figure.y2_axe.data[j].source], 3, point_centre[0])

                    # Si l'on a suprimer des valeurs avant le centre on les sauvegarde
                    if len(res) == 3:
                        point_centre[1] += res[2]

                # on fait repartir le vecteur à 0
                Traitements_cycle_outils.start_0(res[0])

                if point_centre is None:
                    data_unit_x = Data_unit(res[0], unit_x)
                    data_unit_y2 = Data_unit(res[1], unit_y)

                    new_figure.add_data_x_Data(Data_array(data_unit_x, figure.y2_axe.data[j].name,
                                                          figure.y2_axe.data[j].source,
                                                          "cycle_" + str(cycle[i] + 1)))

                    new_figure.add_data_y2_Data(Data_array(data_unit_y2, figure.y2_axe.data[j].name,
                                                           figure.y2_axe.data[j].source,
                                                           "cycle_" + str(cycle[i] + 1)))
                else:
                    last_val = point_centre[0] - point_centre[1]
                    data_unit_x = Data_unit(res[0][0:last_val], unit_x)
                    data_unit_y2 = Data_unit(res[1][0:last_val], unit_y)

                    new_figure.add_data_x_Data(Data_array(data_unit_x, figure.y2_axe.data[j].name,
                                                          figure.y2_axe.data[j].source,
                                                          "cycle_" + str(cycle[i] + 1)))

                    new_figure.add_data_y2_Data(Data_array(data_unit_y2, figure.y2_axe.data[j].name,
                                                           figure.y2_axe.data[j].source,
                                                           "cycle_" + str(cycle[i] + 1)))
    new_figure.created_from = figure
    new_figure.name = name

    if new_figure.x_axe is None:
        print("Aucun cycle n'a pu être tracé")
        return

    # On return la figure créée
    return new_figure


def cycle_norm_cccv(figure, loop_data, mode_data, i_data, ecell_data, cycle):
    """
    Prend en argument une figure, loop data et mode_data, loop_data et mode_data sont des dictionnaires
    mode_data sert a suprimer les plateaux et loop data pour créer les cycles
    return la figure créée

    si cycle == None => cycle all, on créer un vecteur avec les cycle pour garder la même structure de code
    is_cycle_none garde trace de si à l'origine cycle est None, utilisé pour le nom de la figure

    Après le traitement les cycles seront normalisés à 1

    :param figure: figure de base sur laquelle on traite les cycles

    :param loop_data: dictionaire ayant pour clé le nom d'un fichier de donnée ouvert et pour value
                      une list contenant les index des loop du fichier ec_lab correspondant

    :param mode_data: dictionaire ayant pour clé le nom d'un fichier de donnée ouvert et pour value
                      une list contenant la colone mode du fichier ec_lab correspondant

    :param i_data: dictionaire ayant pour clé le nom d'un fichier de donnée ouvert et pour value
                      une list contenant la colone courant du fichier ec_lab correspondant

    :param ecell_data: dictionaire ayant pour clé le nom d'un fichier de donnée ouvert et pour value
                      une list contenant la colone potentiel du fichier ec_lab correspondant

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
        res = last_cycle_valide(loop_data[i], ecell_data[i], i_data[i])
        if res != 1:
            del_cycle[i] = [len(loop_data[i]) - 1, res]

    """   Création de la nouvelle figure, elle est dirty """
    new_figure = Figure("", 1)

    if figure.y2_axe is None:
        new_figure.type = "cycle_y1"
    else:
        new_figure.type = "cycle_y1_y2"

    name = "cycle"

    for i in range(len(cycle)):
        # On garde le nom de chaque cycle passé pour le nom de la figure
        # Utilisé uniquement si cycle is not None, all sinon
        name += "_" + str(cycle[i] + 1)

        # On récupére les données de data_y1 de current_figure
        # On associe à chaque data_y1 un nouveaux data_x de même taille
        # Obligatoire car les différents cycle n'ont pas le même nombre de point
        for j in range(len(figure.y1_axe.data)):
            # dans le cas ou il y a 2 fichier, sur un cycle all la lists des cycle
            # comprends tous les cycles de l'un des 2 fichiers. Si l'un posséde plus de cycle
            # que l'autre, on ne peux pas tracer ce cycle là
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

            # On suprime les plateaux, mode 2
            res = Traitements_cycle_outils.mode_del(figure.x_axe.data[j].data[val_min:val_max],
                                                    figure.y1_axe.data[j].data[val_min:val_max],
                                                    val_min, val_max, mode_data[figure.y1_axe.data[j].source], 2)

            # on suprime le mode 3, ocv
            res = Traitements_cycle_outils.mode_del(res[0], res[1], val_min, val_max,
                                                    mode_data[figure.y1_axe.data[j].source], 3)

            try:
                normalise(res[0])
            except ValueError:
                emit.emit("msg_console", type="msg_console", str="Discard cycle " + str(cycle[i] + 1) + " y1",
                          foreground_color="yellow")
                continue

            data_unit_x = Data_unit(res[0], unit_x)
            data_unit_y1 = Data_unit(res[1], unit_y)

            new_figure.add_data_x_Data(Data_array(data_unit_x, "Normalisation", figure.x_axe.data[j].source,
                                                  "cycle_" + str(cycle[i] + 1)))
            new_figure.add_data_y1_Data(Data_array(data_unit_y1, figure.y1_axe.data[j].name, figure.y1_axe.data[j].source,
                                                   "cycle_" + str(cycle[i] + 1)))

    if figure.y2_axe is not None:
        unit_y = figure.y2_axe.get_unit()

        for i in range(len(cycle)):
            # On récupére les données de data_y2 de current_figure
            # On associe à chaque data_y2 un nouveaux data_x de même taille
            # Obligatoire car les différents cycle n'ont pas le même nombre de point
            for j in range(len(figure.y2_axe.data)):
                # dans le cas ou il y a 2 fichier, sur un cycle all la lists des cycle
                # comprends tous les cycles de l'un des 2 fichiers. Si l'un posséde plus de cycle
                # que l'autre, on ne peux pas tracer ce cycle là
                if cycle[i] >= len(loop_data[figure.y2_axe.data[j].source]):
                    continue

                # On récucpére premier et le dernier point correspondant au cycle en cours
                val_min = loop_data[figure.y2_axe.data[j].source][cycle[i]][0]
                val_max = loop_data[figure.y2_axe.data[j].source][cycle[i]][1]

                if val_max - val_min < 20:
                    emit.emit("msg_console", type="msg_console", str="Cycle " + str(cycle[i] + 1) + " discard",
                              foreground_color="yellow")
                    continue

                # si le cycle correspond à un cycle du dictionaire del_cycle et qu'il vaut -1, on le discard
                if figure.y2_axe.data[j].source in del_cycle and del_cycle[figure.y2_axe.data[j].source][0] == cycle[i]:
                    if del_cycle[figure.y2_axe.data[j].source][1] != 1:
                        emit.emit("msg_console", type="msg_console", str="Discard cycle " + str(cycle[i] + 1) + " y2",
                                  foreground_color="yellow")
                        continue

                # On suprime les plateaux, mode 2
                res = Traitements_cycle_outils.mode_del(figure.x_axe.data[j].data[val_min:val_max],
                                                        figure.y2_axe.data[j].data[val_min:val_max],
                                                        val_min, val_max, mode_data[figure.y2_axe.data[j].source], 2)

                # on suprime le mode 3, ocv
                res = Traitements_cycle_outils.mode_del(res[0], res[1], val_min, val_max,
                                                        mode_data[figure.y2_axe.data[j].source], 3)

                try:
                    normalise(res[0])
                except ValueError:
                    emit.emit("msg_console", type="msg_console", str="Discard cycle " + str(cycle[i] + 1) + " y1",
                              foreground_color="yellow")
                    continue

                data_unit_x = Data_unit(res[0], unit_x)
                data_unit_y2 = Data_unit(res[1], unit_y)

                new_figure.add_data_x_Data(Data_array(data_unit_x, figure.x_axe.data[j].name, figure.x_axe.data[j].source,
                                                      "cycle_" + str(cycle[i] + 1)))

                new_figure.add_data_y2_Data(Data_array(data_unit_y2, figure.y2_axe.data[j].name, figure.y2_axe.data[j].source,
                                                       "cycle_" + str(cycle[i] + 1)))

    new_figure.created_from = figure
    new_figure.name = name

    if new_figure.x_axe is None:
        print("Aucun cycle n'a pu être tracé")
        return

    # On return la figure créée
    return new_figure


def cycle_miror_cccv(figure, loop_data, mode_data, i_data, ecell_data, cycle):
    """
    Prend en argument une figure, loop data et mode_data, loop_data et mode_data sont des dictionnaires
    mode_data sert a suprimer les plateaux et loop data pour créer les cycles
    return la figure créée

    si cycle == None => cycle all, on créer un vecteur avec les cycle pour garder la même structure de code
    is_cycle_none garde trace de si à l'origine cycle est None, utilisé pour le nom de la figure

    :param figure: figure de base sur laquelle on traite les cycles

    :param loop_data: dictionaire ayant pour clé le nom d'un fichier de donnée ouvert et pour value
                      une list contenant les index des loop du fichier ec_lab correspondant

    :param mode_data: dictionaire ayant pour clé le nom d'un fichier de donnée ouvert et pour value
                      une list contenant la colone mode du fichier ec_lab correspondant

    :param i_data: dictionaire ayant pour clé le nom d'un fichier de donnée ouvert et pour value
                      une list contenant la colone courant du fichier ec_lab correspondant

    :param ecell_data: dictionaire ayant pour clé le nom d'un fichier de donnée ouvert et pour value
                      une list contenant la colone potentiel du fichier ec_lab correspondant

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
        res = last_cycle_valide(loop_data[i], ecell_data[i], i_data[i])
        if res != 1:
            del_cycle[i] = [len(loop_data[i]) - 1, res]

    # Création de la nouvelle figure, elle est dirty
    new_figure = Figure("", 1)

    if figure.y2_axe is None:
        new_figure.type = "cycle_y1"
    else:
        new_figure.type = "cycle_y1_y2"

    name = "cycle"

    for i in range(len(cycle)):
        # On garde le nom de chaque cycle passé pour le nom de la figure
        # Utilisé uniquement si cycle is not None, all sinon
        name += "_" + str(cycle[i] + 1)


        # On récupére les données de data_y1 de current_figure
        # On associe à chaque data_y1 un nouveaux data_x de même taille
        # Obligatoire car les différents cycle n'ont pas le même nombre de point
        for j in range(len(figure.y1_axe.data)):

            # dans le cas ou il y a 2 fichier, sur un cycle all la lists des cycle
            # comprends tous les cycles de l'un des 2 fichiers. Si l'un posséde plus de cycle
            # que l'autre, on ne peux pas tracer ce cycle là
            if cycle[i] >= len(loop_data[figure.y1_axe.data[j].source]):
                continue

            # On récucpére premier et le dernier point correspondant au cycle en cours
            val_min = loop_data[figure.y1_axe.data[j].source][cycle[i]][0]
            val_max = loop_data[figure.y1_axe.data[j].source][cycle[i]][1]

            if val_max - val_min < 20:
                emit.emit("msg_console", type="msg_console", str="Cycle " + str(cycle[i] + 1) + " discard",
                          foreground_color="yellow")
                continue

            last_val = None

            # si le cycle correspond à un cycle du dictionaire del_cycle et qu'il vaut -1, on le discard
            if figure.y1_axe.data[j].source in del_cycle and del_cycle[figure.y1_axe.data[j].source][0] == cycle[i]:
                if del_cycle[figure.y1_axe.data[j].source][1] == -1:
                    emit.emit("msg_console", type="msg_console", str="Discard cycle " + str(cycle[i] + 1) + " y1",
                              foreground_color="yellow")
                    continue
                else:
                    # le cycle est traité que set la motiée
                    emit.emit("msg_console", type="msg_console", str="Discard cycle " + str(cycle[i] + 1) + " y1",
                              foreground_color="yellow")
                    last_val = 1

            index_centre = find_center(val_min, val_max, i_data[figure.y1_axe.data[j].source])

            if index_centre == -1:
                emit.emit("msg_console", type="msg_console", str="Cycle Centre " + str(cycle[i]) +
                                                                 " untraceable", foreground_color="yellow")
                continue

            index_centre = correct_cccv_center(ecell_data[figure.y1_axe.data[j].source][val_min:val_max], index_centre)

            point_centre = [index_centre, 0]

            # On suprime les plateaux, mode 2
            res = Traitements_cycle_outils.mode_del(figure.x_axe.data[j].data[val_min:val_max], figure.y1_axe.data[j].data[val_min:val_max],
                                       val_min,
                                       val_max, mode_data[figure.y1_axe.data[j].source], 2, point_centre[0])
            # Si l'on a suprimer des valeurs avant le centre on les sauvegarde
            if len(res) == 3:
                point_centre[1] = res[2]

            # On suprime les plateaux, mode 2
            res = Traitements_cycle_outils.mode_del(res[0], res[1], val_min, val_max, mode_data[figure.y1_axe.data[j].source], 3,
                                       point_centre[0])
            if len(res) == 3:
                point_centre[1] += res[2]

            # on fait repartir le vecteur à 0
            Traitements_cycle_outils.start_0(res[0])

            """On transforme l'axe x pour effectuer l'effec miroir, le centre ici est
                        déduit du nombre de points que l'on a suprimer avant le centre"""
            res_miror = miror(res[0], point_centre[0] - point_centre[1])

            if last_val is None:
                data_unit_x = Data_unit(res_miror, unit_x)
                data_unit_y1 = Data_unit(res[1], unit_y)

                new_figure.add_data_x_Data(Data_array(data_unit_x, figure.x_axe.data[j].name, figure.x_axe.data[j].source,
                                                      "cycle_" + str(cycle[i] + 1),
                                                      figure.x_axe.data[j].color))

                new_figure.add_data_y1_Data(Data_array(data_unit_y1, figure.y1_axe.data[j].name, figure.y1_axe.data[j].source,
                                                       "cycle_" + str(cycle[i] + 1)))
            else:
                last_val = point_centre[0] - point_centre[1]
                # on utilise directement point_centre[0] - point_centre[1], pas besoin de faire autre chose

                data_unit_x = Data_unit(res_miror[0:last_val], unit_x)
                data_unit_y1 = Data_unit(res[1][0:last_val], unit_y)

                new_figure.add_data_x_Data(
                    Data_array(data_unit_x, figure.x_axe.data[j].name, figure.x_axe.data[j].source,
                               "cycle_" + str(cycle[i] + 1)))

                new_figure.add_data_y1_Data(
                    Data_array(data_unit_y1, figure.y1_axe.data[j].name, figure.y1_axe.data[j].source,
                               "cycle_" + str(cycle[i] + 1)))

    if figure.y2_axe is not None:
        unit_y = figure.y2_axe.get_unit()

        for i in range(len(cycle)):
            """  On récupére les données de data_y2 de current_figure """
            for j in range(len(figure.y2_axe.data)):
                # dans le cas ou il y a 2 fichier, sur un cycle all la lists des cycle
                # comprends tous les cycles de l'un des 2 fichiers. Si l'un posséde plus de cycle
                # que l'autre, on ne peux pas tracer ce cycle là
                if cycle[i] >= len(loop_data[figure.y2_axe.data[j].source]):
                    continue

                # On récucpére premier et le dernier point correspondant au cycle en cours
                val_min = loop_data[figure.data_y2[j].source][cycle[i]][0]
                val_max = loop_data[figure.data_y2[j].source][cycle[i]][1]
                if val_max - val_min < 20:
                    emit.emit("msg_console", type="msg_console", str="Cycle " + str(cycle[i] + 1) + " discard",
                              foreground_color="yellow")
                    continue

                last_val = None

                # si le cycle correspond à un cycle du dictionaire del_cycle et qu'il vaut -1, on le discard
                if figure.data_y2[j].source in del_cycle and del_cycle[figure.data_y2[j].source][0] == cycle[i]:
                    if del_cycle[figure.data_y2[j].source][1] == -1:
                        emit.emit("msg_console", type="msg_console", str="Discard cycle " + str(cycle[i] + 1) + " y2",
                                  foreground_color="yellow")
                        continue

                    elif del_cycle[figure.data_y2[j].source][1] != 0:
                        """le cycle est traité que set la motiée"""
                        last_val = 1
                        emit.emit("msg_console", type="msg_console", str="Second half of cycle " + str(cycle[i] + 1) +
                                                                         " y2 discard", foreground_color="yellow")
                # on cherche le centre du cycle
                index_centre = find_center(val_min, val_max, i_data[figure.data_y2[j].source])

                if index_centre == -1:
                    emit.emit("msg_console", type="msg_console", str="Cycle Centre " + str(cycle[i]) +
                                                                     " untraceable", foreground_color="yellow")
                    continue

                # on corrige l'index du centre, dans le cas ou la manip n'a pas était bien
                # réalisé...
                index_centre = correct_cccv_center(ecell_data[figure.data_y2[j].source][val_min:val_max],
                                                               index_centre)

                # [nouvelle index du cnetre, nombres de points suprimés avant le centre]
                point_centre = [index_centre, 0]

                # On suprime les plateaux, mode 2
                res = Traitements_cycle_outils.mode_del(figure.data_x[j].data[val_min:val_max], figure.data_y2[j].data[val_min:val_max],
                                           val_min,val_max, mode_data[figure.data_y2[j].source], 2)

                # Si l'on a suprimer des valeurs avant le centre on les sauvegarde
                if len(res) == 3:
                    point_centre[1] = res[2]

                # on suprime le mode 3, ocv
                res = Traitements_cycle_outils.mode_del(res[0], res[1], val_min, val_max, mode_data[figure.data_y2[j].source], 3)
                if len(res) == 3:
                    point_centre[1] += res[2]

                # On normalise à 0 les data_x
                Traitements_cycle_outils.start_0(res[0])

                # On transforme l'axe x pour effectuer l'effec miroir, le centre ici est
                # déduit du nombre de points que l'on a suprimer avant le centre
                res_miror = miror(res[0], point_centre[0] - point_centre[1])

                if last_val is None:
                    data_unit_x = Data_unit(res_miror, unit_x)
                    data_unit_y2 = Data_unit(res[1], unit_y)

                    new_figure.add_data_x_Data(Data_array(data_unit_x, figure.data_x[j].name, figure.data_x[j].source,
                                                          "cycle_" + str(cycle[i] + 1),
                                                          figure.data_x[j].color))

                    new_figure.add_data_y2_Data(Data_array(data_unit_y2, figure.data_y2[j].name, figure.data_y2[j].source,
                                                           "cycle_" + str(cycle[i] + 1)))
                else:
                    # on utilise directemetn point_centre[0] - point_centre[1], pas besoin de faire autre chose
                    last_val = point_centre[0] - point_centre[1]

                    data_unit_x = Data_unit(res_miror[0:last_val], unit_x)
                    data_unit_y2 = Data_unit(res[1], unit_y)

                    new_figure.add_data_x_Data(Data_array(data_unit_x, figure.data_x[j].name, figure.data_x[j].source,
                                   "cycle_" + str(cycle[i] + 1)))

                    new_figure.add_data_y2_Data(Data_array(data_unit_y2, figure.data_y2[j].name,
                                                           figure.data_y2[j].source, "cycle_" + str(cycle[i] + 1)))

    new_figure.created_from = figure
    new_figure.name = name

    if new_figure.x_axe is None:
        print("Aucun cycle n'a pu être tracé")
        return

    return new_figure


def potentio(loop_data, time_data, i_data, mode_data, cycle):
    """
    Prends en paramètre les data des loop, du temps, i, mode et le format du temps des data courrantes
    Return une figure format time est soit h, min ou s, c'est une chaine de caractère


    :param loop_data: information sur les loops du fichier dont proviennent les datas
    :param time_data: vecteur du temps
    :param i_data: vecteur courrant
    :param mode_data: vacteur de mode
    :param cycle: list de tous les cycle
    :param color_arg: nom de la color map
    :return: la nouvelle figure créée
    """

    units = Units()
    unit_x = units["minutes"]

    unit_y = units[i_data.unit.fullname]

    # on créer une nouvelle figure
    new_figure = Figure("", 1)

    new_figure.type = "cycle_y1"

    conversion = 60

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
                    temp_x.append(time_data[j] * conversion)
                    temp_y1.append(i_data[j])
                    global_index.append(j)
                    j += 1

                # on normalise le vecteur à 0
                Traitements_cycle_outils.start_0(temp_x)

                # on créer l'objet qui contiendra les valeurs et l'unité
                data_unit_x = Data_unit(temp_x, unit_x)

                # on créer data array_x
                data_array_x = Data_array(data_unit_x, "time", None, "cycle " + str(cycle[i] + 1))

                # on lui ajoute global index
                data_array_x.global_index = global_index

                # on ajoute data_array à new_figure
                new_figure.add_data_x_Data(data_array_x)

                # on créer l'objet qui contiendra les valeurs et l'unité
                data_unit_y = Data_unit(temp_y1, unit_y)

                # on ajoute data_array à new_figure
                new_figure.add_data_y1_Data(Data_array(data_unit_y, "Current", None, "cycle " + str(cycle[i] + 1)))

            else:
                j += 1

    new_figure.name = "potentio" + name

    # on return la figure
    return new_figure


"""---------------------------------------------------------------------------------------------"""

"""                     Ensuite se trouve toutes les fonctions outils                           """

"""---------------------------------------------------------------------------------------------"""


def last_cycle_valide(loop_data, ecell_data, i_data):
    """on check la validité du dernier cycle en fonction du second"""
    last = len(loop_data) - 1

    """On garde pour référence la première et dernière valeurs de E/cell du second cycle"""
    val_min = loop_data[1][0]
    val_max = loop_data[1][1]

    centre_ref = find_center(val_min, val_max, i_data)
    centre_last = find_center(loop_data[last][0], loop_data[last][1], i_data)

    if centre_last == -1:
        return -1

    centre_last = loop_data[last][0] + centre_last + 1

    ref_min = ecell_data[val_min]

    if centre_ref != -1:
        ref_max = ecell_data[centre_ref]
    else:
        raise ValueError

    if centre_last == -1:
        return -1

    if (ref_max * 1.05 < ecell_data[loop_data[-1][1]] or ref_max * 0.95 > ecell_data[loop_data[-1][1]]) \
            and (ref_min * 1.05 < ecell_data[loop_data[-1][1]] or ref_min * 0.95 > ecell_data[loop_data[-1][1]]):
        return centre_last
    return 1


def find_center(min, max, array_I):
    """min et max sont les point de début et de fin de cycle et array_I est
    l'array  correspondant à data.get("<I>/mA"), il sert pour déterminer le
    centre de chaque cycle sans faire aucun calcule"""

    if min + 100 > len(array_I):
        return -1
    temp = array_I[min + 100]
    """On regarde si les premier élements de array_I sont positif ou pas"""
    if temp < 0:
        signe = "n"
    else:
        signe = "p"

    """On parcours le vecteur array_I et on cherche son changement de signe
    on return le numéro du point de ce changement, normalisé à 0"""
    for i in range(min + 100, max + 1):
        if (signe == "n" and array_I[i] > 0) or (signe == "p" and array_I[i] < 0):
            return i - min - 2

    """On return -1 si l'on n'a pas trouvé"""
    return -1


def correct_cccv_center(ecell_data, index_centre):
    if ecell_data[index_centre - 21] < ecell_data[index_centre - 20]:
        signe = "c"
    else:
        signe = "d"

    for i in range(index_centre - 20, index_centre + 20):
        if (signe == "c" and ecell_data[i] < ecell_data[i - 1]) or (signe == "d" and ecell_data[i] > ecell_data[i - 1]):
            return i
    return index_centre


def normalise(array):
    """Dans certain cas il est possible que l'on demande de normaliser un cycle vide
    Si le dernier cycle n'est pas complet et que l'on cherche a normaliser une décharge qui n'est pas
    présente"""
    if len(array) == 0:
        return

    if len(array) < 20:
        raise ValueError

    """on start 0 """
    Traitements_cycle_outils.start_0(array)

    """On normalise par la valeur la plus grande, si array est croissant, cette valeur est la dernière"""
    if Traitements_cycle_outils.is_array_croissant(array):
        max_val = array[-1]
    else:
        """Sinon on cherche la valeur max"""
        """Si le vecteur n'est pas roissant, pas besoin de le mettre à 0"""
        """max_val = array[0]
        for i in range(len(array)):
        if array[i] > max_val:
        max_val = array[i]"""
        return
    """On normalise le vecteur par max_val"""
    for i in range(len(array)):
        array[i] = array[i] / max_val


def miror(array_x, centre):
    new_array_x = []
    """start point correspond à la différence de longueur entre la partie gache et la partie droite
    de la courbe, on l'aditionne à chaque loop avec array[i] et on soustrait la valeur du center"""
    start_point = (array_x[centre] - array_x[0]) - (array_x[len(array_x) - 1] - array_x[centre])
    for i in range(centre, len(array_x)):
        new_array_x.append(start_point + array_x[i] - array_x[centre])

    """On reverse le vecteur créé et le return en l'ajoutant à la partie gauche du vecteur qui n'a pas
    été transformé"""
    new_array_x.reverse()

    return array_x[0:centre] + new_array_x