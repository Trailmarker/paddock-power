# -*- coding: utf-8 -*-
from qgis.PyQt.QtCore import Qt, QAbstractTableModel, QModelIndex
from qgis.PyQt.QtGui import QColor

from ..utils import qgsDebug


class PaddockTableModel(QAbstractTableModel):

    ATTRIBUTES = ["Paddock Name", "Paddock Area (km²)", "Perimeter (km)"]
    HEADERS = ["Name", "Area (km²)", "Perimeter (km)"]

    def __init__(self, milestone):
        QAbstractTableModel.__init__(self)
        self.milestone = milestone

    def rowCount(self, parent=QModelIndex()):
        count = len(self.milestone.paddockFeatures)
        # qgsDebug(f"rowCount: {count}", tag="PaddockTableModel.rowCount")
        return count

    def columnCount(self, parent=QModelIndex()):
        return 2

    def headerData(self, section, orientation, role):
        if role != Qt.DisplayRole:
            return None
        if orientation == Qt.Horizontal:
            return self.HEADERS[section]

    def data(self, index, role=Qt.DisplayRole):
        column = index.column()
        row = index.row()

        # qgsDebug("column: " + str(column) + " row: " + str(row), tag="PaddockTableModel.data")

        # qgsDebug(f"number of features: {len(self.milestone.paddockFeatures)}", tag="PaddockTableModel.data")

        if role == Qt.DisplayRole:
            if column in [0, 1]:
                return self.milestone.paddockFeatures[row][self.ATTRIBUTES[column]]
        elif role == Qt.BackgroundRole:
            return QColor(Qt.white)
        elif role == Qt.TextAlignmentRole:
            return Qt.AlignRight

        return None
