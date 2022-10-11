# -*- coding: utf-8 -*-
from qgis.PyQt.QtCore import Qt, QAbstractTableModel, QModelIndex
from qgis.PyQt.QtGui import QColor

from qgis.core import QgsFeature

from ...layer.paddock_layer import PaddockLayer
from ...models.paddock_power_error import PaddockPowerError

class PaddockTableModel(QAbstractTableModel):

    ATTRIBUTES = ["Paddock Name",
                  "Paddock Area (km²)", "Paddock Perimeter (km)"]
    HEADERS = ["Name", "Area (km²)", "Perimeter (km)"]

    def __init__(self, paddockLayer, specifiedPaddockFeatures = None):
        QAbstractTableModel.__init__(self)

        if paddockLayer is None:
            self.paddockLayer = None
            self.paddockFeatures = []
            self.specifiedPaddockFeaturesOnly = True
            return
        if not isinstance(paddockLayer, PaddockLayer):
            raise PaddockPowerError("PaddockTableModel.__init__: paddockLayer must be a PaddockLayer")

        if specifiedPaddockFeatures and (not isinstance(specifiedPaddockFeatures, list) or not all(isinstance(QgsFeature, f) for f in specifiedPaddockFeatures)):
            raise PaddockPowerError("PaddockTableModel.__init__: if provided, paddockFeatures must be a list of QGIS QgsFeature objects")

        self.paddockFeatures = specifiedPaddockFeatures
        self.paddockLayer = paddockLayer

        if specifiedPaddockFeatures:
            self.specifiedPaddockFeaturesOnly = True
        else:
            self.specifiedPaddockFeaturesOnly = False
            self.dataChanged.connect(self.refreshFeatures)
            self.refreshFeatures()


    def refreshFeatures(self):
        """Refresh array of features from the layer."""
        if self.paddockLayer is not None:
            self.paddockFeatures = [f for f in self.paddockLayer.getFeatures()]
        else:
            self.paddockFeatures = []
        self.layoutChanged.emit()

    def flags(self, index):
        if index.column() == 0:
            return Qt.ItemIsEnabled|Qt.ItemIsEditable
        else:
            return Qt.ItemIsEnabled

    def rowCount(self, parent=QModelIndex()):
        if self.paddockLayer is None:
            return 0
        return len(self.paddockFeatures)

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
                return self.paddockFeatures[row][self.ATTRIBUTES[column]]
        elif role == Qt.BackgroundRole:
            return QColor(Qt.white)
        elif role == Qt.TextAlignmentRole:
            return Qt.AlignRight

        return None

    def setData(self, index, value, role):
        """Set the data in a cell (currently 'Paddock Name' only is supported)."""
        if role == Qt.EditRole:
            if index.column() == 0: # Assumes 'Paddock Name' is the first column
                self.paddockLayer.updatePaddockName(self.paddockFeatures[index.row()], value)
                self.dataChanged.emit(index, index)
                return True
        return False