# -*- coding: utf-8 -*-
from ..fields import BasePaddockSchema
from .edits import Edits
from .feature_action import FeatureAction
from .persisted_feature import PersistedFeature
from .status_feature_mixin import StatusFeatureMixin


@BasePaddockSchema.addSchema()
class BasePaddock(PersistedFeature, StatusFeatureMixin):

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

    # Note FeatureAction decorators are not accompanied by @Edits.persistFeatures(): the Base
    # Paddock is not persisted directly, but rather through the Paddock that relies on it and 
    # that reflects its STATUS
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

    @FeatureAction.build.handler()
    def buildFeature(self):
        return Edits.upsert(self)

    @FeatureAction.undoBuild.handler()
    def undoBuildFeature(self):
        return Edits.upsert(self)

    @FeatureAction.supersede.handler()
    def supersedeFeature(self, fence):
        self.BUILD_FENCE = fence.BUILD_ORDER
        return Edits.upsert(self)

    @FeatureAction.undoSupersede.handler()
    def undoSupersedeFeature(self):
        self.BUILD_FENCE = None
        return Edits.upsert(self)
    
    @FeatureAction.archive.handler()
    def archiveFeature(self):
        return Edits.upsert(self)

    @FeatureAction.undoArchive.handler()
    def undoArchiveFeature(self):
        return Edits.upsert(self)