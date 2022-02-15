import PyQt5
from PyQt5.QtCore import QObject, QThread, pyqtSignal
from PyQt5.uic.properties import QtCore

from Resources_file import Lecteur_threads
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
