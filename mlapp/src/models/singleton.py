# -*- coding: utf-8 -*-
from qgis.PyQt.QtCore import QObject

# See https://stackoverflow.com/questions/59459770/receiving-pyqtsignal-from-singleton


class Singleton(type(QObject), type):
    def __init__(cls, name, bases, dict):
        super().__init__(name, bases, dict)
        cls._instance = None

    def __call__(cls, *args, **kwargs):
        if cls._instance is None:
            cls._instance = super().__call__(*args, **kwargs)
        return cls._instance
