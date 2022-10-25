# -*- coding: utf-8 -*-
from .area_feature import AreaFeature
from .edits import Edits
from .feature_action import FeatureAction
from .schemas import WaterpointBufferSchema


@WaterpointBufferSchema.addSchema()
class WaterpointBuffer(AreaFeature):

    def __init__(self, featureLayer, existingFeature=None):
        """Create a new Boundary."""
        super().__init__(featureLayer=featureLayer, existingFeature=existingFeature)

    @FeatureAction.plan.handler()
    def planFeature(self, waterpoint, geometry, waterpointBufferType, bufferDistance):
        self.waterpoint = waterpoint.id
        self.geometry = geometry
        self.waterpointBufferType = waterpointBufferType
        self.bufferDistance = bufferDistance
        return Edits.upsert(self)

    @FeatureAction.undoPlan.handler()
    def undoPlanFeature(self):
        self.waterpoint = None
        return Edits.delete(self)
