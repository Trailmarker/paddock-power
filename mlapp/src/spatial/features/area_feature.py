# -*- coding: utf-8 -*-
from ..calculator import Calculator
from .feature import Feature
from .schemas import AreaFeatureSchema


@AreaFeatureSchema.addSchema()
class AreaFeature(Feature):

    def __init__(self, featureLayer, existingFeature=None):
        """Create a new AreaFeature."""
        super().__init__(featureLayer, existingFeature)

    def recalculate(self):
        """Recalculate the area and perimeter of the AreaFeature."""
        area = round(Calculator.calculateArea(self.geometry) / 1000000, 2)
        perimeter = round(Calculator.calculatePerimeter(
            self.geometry) / 1000, 2)
        self.featureArea = area
        self.featurePerimeter = perimeter
