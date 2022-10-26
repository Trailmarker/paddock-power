# -*- coding: utf-8 -*-
from .feature import Feature
from ..schemas.schemas import BoundarySchema


@BoundarySchema.addSchema()
class Boundary(Feature):

    def __init__(self, featureLayer, existingFeature):
        """Create a new AreaFeature."""
        super().__init__(featureLayer, existingFeature)
