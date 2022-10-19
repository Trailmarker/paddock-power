# -*- coding: utf-8 -*-
from ..calculator import Calculator
from ..layers.elevation_layer import ElevationLayer
from .feature import Feature
from .schemas import PointFeatureSchema


@PointFeatureSchema.addSchema()
class PointFeature(Feature):

    def __init__(self, featureLayer, elevationLayer=None, existingFeature=None):
        """Create a new LineFeature."""
        super().__init__(featureLayer=featureLayer, existingFeature=existingFeature)

        assert elevationLayer is None or isinstance(elevationLayer, ElevationLayer), "elevationLayer must be provided"

        self.elevationLayer = elevationLayer
        self.recalculate()

    def recalculate(self):
        """Recalculate the longitude, latitude and elevation of the PointFeature."""
        elevation = round(Calculator.calculateElevationAtPoint(self.geometry, self.elevationLayer), 2)
        # TODO Latitude and Longitude
        self.featureElevation = elevation
