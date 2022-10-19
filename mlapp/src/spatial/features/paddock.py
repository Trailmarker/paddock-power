# -*- coding: utf-8 -*-
from .capacity_feature import CapacityFeature
from .edits import Edits
from .feature import FeatureAction
from .schemas import PaddockSchema


@PaddockSchema.addSchema()
class Paddock(CapacityFeature):

    def __init__(self, featureLayer, existingFeature=None):
        """Create a new Paddock."""
        super().__init__(featureLayer=featureLayer, existingFeature=existingFeature)

    @FeatureAction.handler(FeatureAction.plan)
    def planPaddock(self, fence):
        self.buildFence = fence
        return Edits.upsert(self)

    @FeatureAction.handler(FeatureAction.undoPlan)
    def undoPlanPaddock(self):
        self.buildFence = None
        return Edits.delete(self)

    @FeatureAction.handler(FeatureAction.supersede)
    def supersedePaddock(self, fence):
        self.buildFence = fence.buildOrder
        return Edits.upsert(self)

    @FeatureAction.handler(FeatureAction.undoSupersede)
    def undoSupersedePaddock(self):
        self.buildFence = None
        return Edits.upsert(self)
