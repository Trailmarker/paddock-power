# -*- coding: utf-8 -*-
from qgis.core import QgsWkbTypes

from ..calculator import Calculator
from ..layers.elevation_layer import ElevationLayer
from .feature import Feature
from .schemas import LineFeatureSchema, addSchema


@addSchema(LineFeatureSchema, QgsWkbTypes.LineString)
class LineFeature(Feature):

    def __init__(self, featureLayer, elevationLayer=None, existingFeature=None):
        """Create a new LineFeature."""
        super().__init__(featureLayer=featureLayer, existingFeature=existingFeature)

        assert featureLayer.__class__.__name__ == "FenceLayer", f"featureLayer must be a FenceLayer, not {featureLayer.__class__.__name__}"
        assert elevationLayer is None or isinstance(
            elevationLayer, ElevationLayer), "elevationLayer must be an ElevationLayer"

        self.elevationLayer = elevationLayer
        self._profile = None
        # self.recalculate()

    def profile(self):
        return self._profile

    def recalculate(self):
        """Recalculate the length of this Pipeline."""
        self._profile = Calculator.calculateProfile(
            self.geometry(), self.elevationLayer)
        length = round(self._profile.maximumDistance / 1000, 2)
        self.featureLength = length
