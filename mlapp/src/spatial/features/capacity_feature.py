# -*- coding: utf-8 -*-
from .area_feature import AreaFeature
from .schemas import CapacityFeatureSchema


@CapacityFeatureSchema.addSchema()
class CapacityFeature(AreaFeature):

    def __init__(self, featureLayer, existingFeature=None):
        """Create a new CapacityFeature."""
        super().__init__(featureLayer=featureLayer, existingFeature=existingFeature)
