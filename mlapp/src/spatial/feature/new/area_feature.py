# -*- coding: utf-8 -*-
from qgis.PyQt.QtCore import QVariant

from qgis.core import QgsField

from ...calculator import Calculator
from .feature import Feature


class AreaFeature(Feature):
    AREA = "Area (km²)"
    PERIMETER = "Perimeter (km)"

    SCHEMA = Feature.SCHEMA + [
        QgsField(name=AREA, type=QVariant.Double,
                 typeName="Real", len=0, prec=0, comment="", subType=QVariant.Invalid),
        QgsField(name=PERIMETER, type=QVariant.Double,
                 typeName="Real", len=0, prec=0, comment="", subType=QVariant.Invalid)
    ]

    def __init__(self, feature=None):
        """Create a new AreaFeature."""
        super().__init__(feature)

    def featureArea(self):
        return self.feature[AreaFeature.AREA]

    def featurePerimeter(self):
        return self.feature[AreaFeature.PERIMETER]

    def recalculate(self):
        """Recalculate the area and perimeter of the AreaFeature."""
        area = round(Calculator.calculateArea(self.geometry()) / 1000000, 2)
        perimeter = round(Calculator.calculatePerimeter(
            self.geometry()) / 1000, 2)
        self.feature.setAttribute(AreaFeature.AREA, area)
        self.feature.setAttribute(AreaFeature.PERIMETER, perimeter)
