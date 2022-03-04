import PyQt5
from PyQt5.QtCore import QObject, pyqtSignal

from Resources_file import Lecteur_diffraction, Lecteur_ihch_1501
from Resources_file.Emit import Emit
from Resources_file.Lecteur_threads import Lecteur_thread


class Open_file_cccv(QObject):
    finished = pyqtSignal(int)

    def __init__(self, path):
        QObject.__init__(self)
        """
        __file_path : [type, path]
        path pouvant être un array
        """
        self.__file_path = path
        self.__data = None
        self.__finish = False

    def run(self):
        try:
            self.__data = Lecteur_thread.open(self.__file_path, "cccv")
        except ValueError:
            self.finished.emit(-1)
            self.__finish = True
        else:
            self.finished.emit(1)
            self.__finish = True

    @property
    def file_path(self):
        return self.__file_path

    @property
    def data(self):
        return self.__data

    @property
    def finish(self):
        return self.__finish

    @file_path.setter
    def file_path(self, file_path):
        self.__file_path = file_path

    @data.setter
    def data(self, data):
        self.__data = data

    @finish.setter
    def finish(self, finish):
        self.__finish = finish



class Open_file_diffraction(QObject):
    finished = pyqtSignal(int)

    def __init__(self, path):
        QObject.__init__(self)
        """
        __file_path : [type, path]
        path pouvant être un array
        """
        self.__file_path = path
        self.__data = None
        self.__finish = False

    def run(self):
        try:
            data_w, loop_w, data_c, loop_c = Lecteur_diffraction.open_diffraction(self.__file_path)
            if len(data_w) == 0:
                name = data_c[0]["name"]
            else:
                name = data_w[0]["name"]
            self.__data = Lecteur_diffraction.create_dics(data_w, loop_w, data_c, loop_c)
            self.__data["name"] = name
        except ValueError:
            self.finished.emit(-1)
            self.__finish = True
        else:
            self.finished.emit(1)
            self.__finish = True

    @property
    def file_path(self):
        return self.__file_path

    @property
    def data(self):
        return self.__data

    @property
    def finish(self):
        return self.__finish

    @file_path.setter
    def file_path(self, file_path):
        self.__file_path = file_path

    @data.setter
    def data(self, data):
        self.__data = data

    @finish.setter
    def finish(self, finish):
        self.__finish = finish


class Open_file_ihch_1501(QObject):
    finished = pyqtSignal(list)

    def __init__(self, path, ec_lab_paths=None):
        QObject.__init__(self)
        """
        __file_path : [type, path]
        path pouvant être un array
        """
        self.__file_path = path
        self.__data = None
        self.__finish = False
        self.__ec_lab_paths = ec_lab_paths

    def run(self):
        emit = Emit()
        if self.__ec_lab_paths is None:
            try:
                self.__data = Lecteur_ihch_1501.open_ihch_1501(self.__file_path)
            except ValueError:
                self.finished.emit([-1])
                self.__finish = True
            else:
                # si le temp n'est pas créé on return data avec pour valeur le nombre de cycle et donc de fichier
                # ec_lab a ouvrir
                if isinstance(self.__data, int):
                    # on récupére le nombre de cycle
                    nb_cycle = self.__data

                    emit.emit("msg_console", type="msg_console", str="time need to be created", foreground_color="red")
                    self.finished.emit([-2, nb_cycle])
                    self.__finish = True
                else:
                    self.finished.emit([1])
                    self.__finish = True
        else:
            try:
                Lecteur_ihch_1501.create_time(self.__ec_lab_paths, self.__file_path)
                self.__data = Lecteur_ihch_1501.open_ihch_1501(self.__file_path)
            except ValueError:
                self.finished.emit([-1])
                self.__finish = True
            else:
                # si même avec la création du temps on n'arrive pas à lire l'exp, c'est la merde,
                # on stop jsute
                if isinstance(self.__data, int):
                    emit.emit("msg_console", type="msg_console", str="Unable to process the data",
                              foreground_color="red")
                    self.__data = None
                    self.finished.emit([-3])
                    self.__finish = True
                else:
                    self.finished.emit([1])
                    self.__finish = True

    @property
    def file_path(self):
        return self.__file_path

    @property
    def data(self):
        return self.__data

    @property
    def finish(self):
        return self.__finish

    @file_path.setter
    def file_path(self, file_path):
        self.__file_path = file_path

    @data.setter
    def data(self, data):
        self.__data = data

    @finish.setter
    def finish(self, finish):
        self.__finish = finish