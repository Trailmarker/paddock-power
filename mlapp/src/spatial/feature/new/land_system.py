# -*- coding: utf-8 -*-
from qgis.PyQt.QtCore import QVariant

from qgis.core import QgsField

from .capacity_feature import CapacityFeature


class LandSystem(CapacityFeature):

    MAP_UNIT = "Map Unit"
    LANDSCAPE_CLASS = "Landscape Class"
    CLASS_DESCRIPTION = "Class Description"
    EROSION_RISK = "Erosion Risk"

    SCHEMA = CapacityFeature.SCHEMA + [
        QgsField(name="Map Unit", type=QVariant.String, typeName="String",
                 len=10, prec=0, comment="", subType=QVariant.Invalid),
        QgsField(name="Landscape Class", type=QVariant.String, typeName="String",
                 len=50, prec=0, comment="", subType=QVariant.Invalid),
        QgsField(name="Class Description", type=QVariant.String, typeName="String",
                 len=254, prec=0, comment="", subType=QVariant.Invalid),
        QgsField(name="Erosion Risk", type=QVariant.String, typeName="String",
                 len=100, prec=0, comment="", subType=QVariant.Invalid)
    ]
