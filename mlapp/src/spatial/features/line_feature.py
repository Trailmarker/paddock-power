# -*- coding: utf-8 -*-
from qgis.core import QgsProject

from ..calculator import Calculator
from ..layers.elevation_layer import ElevationLayer
from .feature import Feature
from .schemas import LineFeatureSchema


@LineFeatureSchema.addSchema()
class LineFeature(Feature):

    def __init__(self, featureLayer, elevationLayer=None, existingFeature=None):
        """Create a new LineFeature."""
        super().__init__(featureLayer=featureLayer, existingFeature=existingFeature)

        self._elevationLayerId = elevationLayer.id()
        self._profile = None
        # self.recalculate()

    @property
    def elevationLayer(self):
        return QgsProject.instance().mapLayer(self._elevationLayerId)

    def profile(self):
        return self._profile

    def recalculate(self):
        """Recalculate the length of this Pipeline."""
        self._profile = Calculator.calculateProfile(self.geometry, self.elevationLayer)
        length = round(self._profile.maximumDistance / 1000, 2)
        self.featureLength = length
