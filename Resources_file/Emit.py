from PyQt5.QtCore import pyqtSignal
from PyQt5.QtWidgets import QWidget


class Emit(QWidget):
    """
    On utlise cette class pour faire passer des signaux de n'importe quel class
    à la fenêtre principal, notament utile pour afficher les messages de la console
    sur la fenêtre en bas à gauche
    """
    # c'est un singleton
    _instance = None

    # vecteur des fonctions de callbacks
    _connect = {}

    # dictionnaire d'argument a passer comme signal
    message = pyqtSignal(dict)

    def __new__(cls):
        if cls._instance is None:
            cls._instance = super(Emit, cls).__new__(cls)
        return cls._instance

    def emit(self, name, **kwargs):
        self._connect[name](kwargs)

    def connect(self, name, func):
        self._connect[name] = func

    def disconnect(self, name):
        self._connect.pop(name)

    def disconnect_all(self):
        self._connect.clear()
