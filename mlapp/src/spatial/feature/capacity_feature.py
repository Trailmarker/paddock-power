# -*- coding: utf-8 -*-
from qgis.PyQt.QtCore import QVariant

from qgis.core import QgsField

from .area_feature import AreaFeature

class CapacityFeature(AreaFeature):
    CAPACITY = "AE/km²"

    SCHEMA = AreaFeature.SCHEMA + [
            QgsField(name="AE/km²", type=QVariant.Double, typeName="Real",
                        len=0, prec=0, comment="", subType=QVariant.Invalid)
    ]

    def featureCapacity(self):
        return self[CapacityFeature.CAPACITY]

    def setFeatureCapacity(self, capacity):
        self.setAttribute(CapacityFeature.CAPACITY, capacity)
