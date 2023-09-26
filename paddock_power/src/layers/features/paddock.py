# -*- coding: utf-8 -*-
from ..fields import AnalysisType, FeatureStatus
from .metric_paddock import MetricPaddock


class Paddock(MetricPaddock):

    def __init__(self, featureLayer, existingFeature=None):
        """Initialise a new Paddock."""
        super().__init__(featureLayer, existingFeature)

    @property
    def STATUS(self):
        """Get the status of the Base Paddock that this Paddock relies on."""
        basePaddock = self.getBasePaddock()
        return basePaddock.STATUS if basePaddock else FeatureStatus.Undefined
    
    @property
    def isAnalytic(self):
        """Check if the Paddock is analytic."""
        return self.ANALYSIS_TYPE in [AnalysisType.Default]