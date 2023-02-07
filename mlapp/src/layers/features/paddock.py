# -*- coding: utf-8 -*-
from .metric_paddock import MetricPaddock


class Paddock(MetricPaddock):

    def __init__(self, featureLayer, existingFeature=None):
        """Initialise a new Metric Paddock."""
        super().__init__(featureLayer, existingFeature)

    @property
    def STATUS(self):
        """Get the status of the Paddock that this Metric Paddock is associated with."""
        return self.getBasePaddock().STATUS

    @STATUS.setter
    def STATUS(self, s):
        """Get the status of the Paddock that this Metric Paddock is associated with."""
        self.getBasePaddock().STATUS = s
