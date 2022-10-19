# -*- coding: utf-8 -*-
from .area_feature import AreaFeature
from .schemas import BoundarySchema


@BoundarySchema.addSchema()
class Boundary(AreaFeature):

    def __init__(self, featureLayer, existingFeature=None):
        """Create a new Boundary."""
        super().__init__(featureLayer=featureLayer, existingFeature=existingFeature)
