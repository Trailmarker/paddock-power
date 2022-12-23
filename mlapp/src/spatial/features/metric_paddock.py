# -*- coding: utf-8 -*-
from ..schemas.schemas import MetricPaddockSchema
from .feature import Feature


@MetricPaddockSchema.addSchema()
class MetricPaddock(Feature):

    def __init__(self, featureLayer, existingFeature=None):
        """Initialise a new Metric Paddock."""
        super().__init__(featureLayer=featureLayer, existingFeature=existingFeature)

    @property
    def focusOnSelect(self):
        """Return True if the app should focus on this Feature when selected."""
        return False
