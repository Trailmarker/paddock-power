# -*- coding: utf-8 -*-
from .metric_paddock import MetricPaddock


class Paddock(MetricPaddock):

    def __init__(self, featureLayer, existingFeature=None):
        """Initialise a new Paddock."""
        super().__init__(featureLayer, existingFeature)

    @property
    def STATUS(self):
        """Get the status of the Base Paddock that this Paddock relies on."""
        return self.getBasePaddock().STATUS
