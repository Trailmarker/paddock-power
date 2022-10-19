# -*- coding: utf-8 -*-
from .area_feature import AreaFeature
from .feature import addSchema
from .schemas import BoundarySchema


@addSchema(BoundarySchema)
class Boundary(AreaFeature):

    def __init__(self, featureLayer, existingFeature=None):
        """Create a new Boundary."""
        super().__init__(featureLayer=featureLayer, existingFeature=existingFeature)
