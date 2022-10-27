# -*- coding: utf-8 -*-
from qgis.core import QgsProject

from ..calculator import Calculator
from ..layers.elevation_layer import ElevationLayer
from ..schemas.schemas import PointFeatureSchema
from .status_feature import StatusFeature


@PointFeatureSchema.addSchema()
class PointFeature(StatusFeature):

    def __init__(self, featureLayer, elevationLayer=None, existingFeature=None):
        """Create a new PointFeature."""
        super().__init__(featureLayer=featureLayer, existingFeature=existingFeature)

        assert elevationLayer is None or isinstance(elevationLayer, ElevationLayer), "elevationLayer must be provided"

        self._elevationLayerId = elevationLayer.id() if elevationLayer else None

    @property
    def elevationLayer(self):
        return QgsProject.instance().mapLayer(self._elevationLayerId) if self._elevationLayerId else None

    def recalculate(self):
        """Recalculate the longitude, latitude and elevation of the PointFeature."""
        elevation = round(Calculator.calculateElevationAtPoint(self.geometry, self.elevationLayer), 2)
        # TODO Latitude and Longitude
        self.featureElevation = elevation
