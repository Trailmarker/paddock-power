# -*- coding: utf-8 -*-
from ..calculator import Calculator
from .persisted_feature import PersistedFeature
from ..fields.schemas import LandTypeSchema


@LandTypeSchema.addSchema()
class LandType(PersistedFeature):

    def __init__(self, featureLayer, existingFeature=None):
        """Create a new LandType."""
        super().__init__(featureLayer=featureLayer, existingFeature=existingFeature)

    def recalculate(self):
        """Recalculate the area and perimeter of the AreaFeature."""
        area = round(Calculator.calculateArea(self.geometry) / 1000000, 2)
        perimeter = round(Calculator.calculatePerimeter(
            self.geometry) / 1000, 2)
        self.featureArea = area
        self.featurePerimeter = perimeter

    @classmethod
    def focusOnSelect(cls):
        """Return True if the app should focus on this type of Feature when selected."""
        return False
