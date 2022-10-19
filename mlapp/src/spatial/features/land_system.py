# -*- coding: utf-8 -*-
from .capacity_feature import CapacityFeature
from .schemas import LandSystemSchema


@LandSystemSchema.addSchema()
class LandSystem(CapacityFeature):

    def __init__(self, featureLayer, existingFeature=None):
        """Create a new LandSystem."""
        super().__init__(featureLayer=featureLayer, existingFeature=existingFeature)
