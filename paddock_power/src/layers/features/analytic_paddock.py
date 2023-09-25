# -*- coding: utf-8 -*-
from ..fields import AnalyticPaddockSchema
from .base_paddock import BasePaddock


@AnalyticPaddockSchema.addSchema()
class AnalyticPaddock(BasePaddock):
    """'Augmented' Base Paddock with a reference to its 'parent' Paddock."""

    def __init__(self, featureLayer, existingFeature=None):
        """Initialise a new Analytic Paddock."""
        super().__init__(featureLayer, existingFeature)
