# -*- coding: utf-8 -*-
from .feature import Feature
from ..schemas.schemas import WateredAreaSchema


@WateredAreaSchema.addSchema()
class WateredArea(Feature):

    def __init__(self, featureLayer, existingFeature):
        """Create a new Boundary."""
        super().__init__(featureLayer, existingFeature)
