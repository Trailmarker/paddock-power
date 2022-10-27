# -*- coding: utf-8 -*-
from qgis.core import QgsProject

from ..calculator import Calculator
from ..schemas.schemas import LineFeatureSchema
from .status_feature import StatusFeature


@LineFeatureSchema.addSchema()
class LineFeature(StatusFeature):

    def __init__(self, featureLayer, elevationLayer=None, existingFeature=None):
        """Create a new LineFeature."""
        super().__init__(featureLayer=featureLayer, existingFeature=existingFeature)

        self._elevationLayerId = elevationLayer.id() if elevationLayer else None
        self._profile = None
        # self.recalculate()

    @property
    def elevationLayer(self):
        return QgsProject.instance().mapLayer(self._elevationLayerId) if self._elevationLayerId else None

    def profile(self):
        return self._profile

    def recalculate(self):
        """Recalculate the length of this Pipeline."""
        self._profile = Calculator.calculateProfile(self.geometry, self.elevationLayer)
        length = round(self._profile.maximumDistance / 1000, 2)
        self.featureLength = length
