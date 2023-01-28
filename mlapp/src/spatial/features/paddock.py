# -*- coding: utf-8 -*-
from ..fields.schemas import PaddockSchema
from ..layers.condition_table import ConditionTable
from .edits import Edits
from .feature_action import FeatureAction
from .status_feature import StatusFeature


@PaddockSchema.addSchema()
class Paddock(StatusFeature):

    def __init__(self,
                 featureLayer,
                 existingFeature=None):
        """Create a new Paddock."""
        super().__init__(featureLayer, existingFeature)

        self._popupLayerId = None
        self.crossedPaddockId = None

    @property
    def TITLE(self):
        return f"{self.NAME} ({self.FEATURE_AREA:.2f} km²)"

    @property
    def conditionTable(self):
        """Return the ConditionTable for this Paddock."""
        return self.depend(ConditionTable)

    def upsert(self):
        """Upsert the Paddock and also upsert a Condition record if the Paddock has been split."""
        super().upsert()

        if self.crossedPaddockId:
            # qgsDebug(f"{self}.conditionTable.upsertSplit({self.id}, {self.crossedPaddockId})")
            self.conditionTable.upsertSplit(self.FID, self.crossedPaddockId)

        self.featureUpserted.emit()
        return self.FID

    @FeatureAction.draft.handler()
    def draftFeature(self, geometry, name):
        """Draft a Paddock."""
        self.NAME = name
        self.GEOMETRY = geometry
        return Edits.upsert(self)

    @FeatureAction.plan.handler()
    def planFeature(self, fence, crossedPaddock=None):
        self.BUILD_FENCE = fence.BUILD_ORDER
        self.crossedPaddockId = crossedPaddock.FID if crossedPaddock else None
        return Edits.upsert(self)

    @FeatureAction.undoPlan.handler()
    def undoPlanFeature(self):
        self.BUILD_FENCE = None
        return Edits.delete(self)

    @FeatureAction.supersede.handler()
    def supersedeFeature(self, fence):
        self.BUILD_FENCE = fence.BUILD_ORDER
        return Edits.upsert(self)

    @FeatureAction.undoSupersede.handler()
    def undoSupersedeFeature(self):
        self.BUILD_FENCE = None
        return Edits.upsert(self)
