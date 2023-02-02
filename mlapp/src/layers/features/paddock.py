# -*- coding: utf-8 -*-
from ..fields import PaddockSchema
from .edits import Edits
from .feature_action import FeatureAction
from .persisted_feature import PersistedFeature
from .status_feature_mixin import StatusFeatureMixin


@PaddockSchema.addSchema()
class Paddock(PersistedFeature, StatusFeatureMixin):

    def __init__(self,
                 featureLayer,
                 existingFeature=None):
        """Create a new Paddock."""
        PersistedFeature.__init__(self, featureLayer, existingFeature)
        StatusFeatureMixin.__init__(self)

        self.crossedPaddockId = None

    @property
    def TITLE(self):
        return f"{self.NAME} ({self.AREA:.2f} km²)"

    @property
    def landTypeConditionTable(self):
        """Return the LandTypeConditionTable for this Paddock."""
        return self.featureLayer.workspace.landTypeConditionTable

    def upsert(self):
        """Upsert the Paddock and also upsert a Condition record if the Paddock has been split."""
        super().upsert()

        if self.crossedPaddockId:
            self.landTypeConditionTable.upsertSplitPaddockRecord(self.FID, self.crossedPaddockId)

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
