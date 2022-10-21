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

    @FeatureAction.draft.handler()
    def draftPaddock(self, geometry, name):
        """Draft a Paddock."""
        self.name = name
        self.geometry = geometry
        return Edits.upsert(self)

    @FeatureAction.plan.handler()
    def planPaddock(self, fence):
        self.buildFence = fence.buildOrder
        return Edits.upsert(self)

    @FeatureAction.undoPlan.handler()
    def undoPlanPaddock(self):
        self.buildFence = None
        return Edits.delete(self)

    @FeatureAction.supersede.handler()
    def supersedePaddock(self, fence):
        self.buildFence = fence.buildOrder
        return Edits.upsert(self)

    @FeatureAction.undoSupersede.handler()
    def undoSupersedePaddock(self):
        self.buildFence = None
        return Edits.upsert(self)
