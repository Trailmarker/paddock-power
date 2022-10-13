# -*- coding: utf-8 -*-
from qgis.PyQt.QtCore import QVariant

from qgis.core import QgsField

from ..calculator import Calculator
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

    def featureArea(self):
        return self[AreaFeature.AREA]

    def featurePerimeter(self):
        return self[AreaFeature.PERIMETER]

    def recalculate(self, elevationLayer=None):
        """Recalculate the area and perimeter of the AreaFeature."""
        area = round(Calculator.calculateArea(self.geometry()) / 1000000, 2)
        perimeter = round(Calculator.calculatePerimeter(
            self.geometry()) / 1000, 2)
        self.setAttribute(AreaFeature.AREA, area)
        self.setAttribute(AreaFeature.PERIMETER, perimeter)
