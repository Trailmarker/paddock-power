# -*- coding: utf-8 -*-
from .area_feature import AreaFeature
from .feature import addSchema
from .schemas import CapacityFeatureSchema


@addSchema(CapacityFeatureSchema)
class CapacityFeature(AreaFeature):

    def __init__(self, featureLayer, existingFeature=None):
        """Create a new CapacityFeature."""
        super().__init__(featureLayer=featureLayer, existingFeature=existingFeature)
