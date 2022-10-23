# -*- coding: utf-8 -*-
from abc import ABCMeta

from qgis.PyQt.QtCore import QObject


class QtMeta(ABCMeta, type(QObject)):
    """Metaclass for Qt classes so they can co-inherit abstract base classes."""
    pass
