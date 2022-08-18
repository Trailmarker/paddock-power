# -*- coding: utf-8 -*-
from qgis.PyQt.QtCore import Qt, QAbstractTableModel, QModelIndex
from qgis.PyQt.QtGui import QColor

from ..layer.paddock_layer import PaddockLayer
from ..utils import qgsDebug


class PaddockTableModel(QAbstractTableModel):

    ATTRIBUTES = ["Paddock Name", "Paddock Area (km²)", "Paddock Perimeter (km)"]
    HEADERS = ["Name", "Area (km²)", "Perimeter (km)"]

    def __init__(self, paddockLayer):
        QAbstractTableModel.__init__(self)

        if paddockLayer is not None and not isinstance(paddockLayer, PaddockLayer):
            raise TypeError("paddockLayer must be a PaddockLayer")

        self.paddockLayer = paddockLayer
        self.features = [f for f in self.paddockLayer.getFeatures()]

    def rowCount(self, parent=QModelIndex()):
        if self.paddockLayer is None:
            return 0
        return len(self.features)

    def columnCount(self, parent=QModelIndex()):
        return 3

    def headerData(self, section, orientation, role):
        if role != Qt.DisplayRole:
            return None
        if orientation == Qt.Horizontal:
            return self.HEADERS[section]

    def data(self, index, role=Qt.DisplayRole):
        column = index.column()
        row = index.row()

        if self.paddockLayer is None:
            return None

        if role == Qt.DisplayRole:
            if column in [0, 1, 2]:
                return self.features[row][self.ATTRIBUTES[column]]
        elif role == Qt.BackgroundRole:
            return QColor(Qt.white)
        elif role == Qt.TextAlignmentRole:
            return Qt.AlignRight

        return None
