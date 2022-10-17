# -*- coding: utf-8 -*-
from .area_feature import AreaFeature
from .schemas import WaterpointBufferSchema, addSchema


@addSchema(WaterpointBufferSchema)
class WaterpointBuffer(AreaFeature):

    def __init__(self, featureLayer, existingFeature=None):
        """Create a new Boundary."""
        super().__init__(featureLayer=featureLayer, existingFeature=existingFeature)

    def recalculate(self, bufferDistance, landSystemLayer=None):
        """Recalculate stats for this Waterpoint Buffer"""
        # TODO
        pass
