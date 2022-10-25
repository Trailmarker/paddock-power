# -*- coding: utf-8 -*-
from .feature import Feature
from .schemas import LandSystemSchema


@LandSystemSchema.addSchema()
class LandSystem(Feature):

    def __init__(self, featureLayer, existingFeature=None):
        """Create a new LandSystem."""
        super().__init__(featureLayer=featureLayer, existingFeature=existingFeature)
