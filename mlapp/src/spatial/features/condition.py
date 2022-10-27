# -*- coding: utf-8 -*-
from .feature import Feature
from ..schemas.schemas import ConditionSchema


@ConditionSchema.addSchema()
class Condition(Feature):

    def __init__(self, featureLayer, existingFeature):
        """Create a new Boundary."""
        super().__init__(featureLayer, existingFeature)
