# -*- coding: utf-8 -*-
from .capacity_feature import CapacityFeature
from .schemas import PaddockSchema, addSchema

@addSchema(PaddockSchema)
class Paddock(CapacityFeature):

    def __init__(self, featureLayer, existingFeature=None):
        """Create a new Paddock."""
        super().__init__(featureLayer=featureLayer, existingFeature=existingFeature)

    def planPaddock(self, fence):
        self.plan.emit()

        try:
            self.buildFence = fence
            self.recalculate()
            self.upsert()
        except BaseException:
            self.undoPlan.emit()
            raise
    
    def supersedePaddock(self, fence):
        self.supersede.emit()
        self.buildFence = fence.buildOrder
        self.upsert()

    def undoSupersedePaddock(self):
        self.undoSupersede.emit()
        self.buildFence = None
        self.upsert()
