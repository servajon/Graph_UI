from Console_Objets.Figure import Figure


def cycle_diffraction(figure, cycle):
    """
    La figure passé en param a été crée avec une commande, il n'y a donc presque rien à faire,
    c'est juste de la selection de data_array a ajouter à la nouvelle figure

    :param figure: figure issus de la commande diffraction
    :param cycle: cycles sélectionnés
    :return: nouvelle figure
    """
    new_figure = Figure("", 1)

    # La figure a été crée avec la commande diffraction, pas trop de trucs à faire
    name = "cycle"
    for i in cycle:
        name += "_" + str(i + 1)

        data_array_x = figure.x_axe.data[i].copy()
        data_array_y = figure.y1_axe.data[i].copy()

        new_figure.add_data_x_Data(data_array_x)
        new_figure.add_data_y1_Data(data_array_y)

    new_figure.type = "diffraction_cycle"
    new_figure.name = name
    return new_figure
