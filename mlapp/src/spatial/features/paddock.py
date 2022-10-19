# -*- coding: utf-8 -*-
from .capacity_feature import CapacityFeature
from .feature import FeatureAction, actionHandler, addSchema, deletes, upserts
from .schemas import PaddockSchema


@addSchema(PaddockSchema)
class Paddock(CapacityFeature):

    def __init__(self, featureLayer, existingFeature=None):
        """Create a new Paddock."""
        super().__init__(featureLayer=featureLayer, existingFeature=existingFeature)

    @actionHandler(FeatureAction.plan)
    def planPaddock(self, fence):
        self.buildFence = fence
        return upserts(self)

    @actionHandler(FeatureAction.undoPlan)
    def undoPlanPaddock(self):
        self.buildFence = None
        return deletes(self)

    @actionHandler(FeatureAction.supersede)
    def supersedePaddock(self, fence):
        self.buildFence = fence.buildOrder
        return upserts(self)

    @actionHandler(FeatureAction.undoSupersede)
    def undoSupersedePaddock(self):
        self.buildFence = None
        return upserts(self)
