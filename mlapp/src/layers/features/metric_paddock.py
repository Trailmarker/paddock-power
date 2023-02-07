# -*- coding: utf-8 -*-
from ..fields import FID, STATUS, TIMEFRAME, PADDOCK, MetricPaddockSchema
from .feature_action import FeatureAction
from .base_paddock import BasePaddock


@MetricPaddockSchema.addSchema()
class MetricPaddock(BasePaddock):

    def __init__(self, featureLayer, existingFeature=None):
        """Initialise a new Metric Paddock."""
        super().__init__(featureLayer, existingFeature)

    def __repr__(self):
        """Return a string representation of the Feature."""
        attrs = [f"{f}={self.attribute(f)}" for f in [FID, STATUS, TIMEFRAME, PADDOCK] if self.hasField(f)]
        return f"{type(self).__name__}({', '.join(attrs)})"

    @property
    def TITLE(self):
        # return f"#{self.FID} {self.NAME} ({self.AREA:.2f} km²)"
        return f"{self.NAME} ({self.AREA:.2f} km²)"

    @property
    def basePaddockLayer(self):
        return self.featureLayer.workspace.basePaddockLayer

    @property
    def paddockLandTypesLayer(self):
        return self.featureLayer.workspace.paddockLandTypesLayer

    # All workflow functions are deferred to the underlying Base Paddock for this MetricPaddock
    def getBasePaddock(self):
        """Get the Base Paddock that this Metric Paddock is associated with."""
        return self.basePaddockLayer.getFeature(self.PADDOCK)

    @FeatureAction.draft.handler()
    def draftFeature(self, geometry, name):
        """Draft a Paddock."""
        return self.getBasePaddock().draftFeature(geometry, name)

    @FeatureAction.trash.handler()
    def trashFeature(self):
        return self.getBasePaddock().trashFeature()

    @FeatureAction.plan.handler()
    def planFeature(self, fence, crossedPaddock=None):
        return self.getBasePaddock().planFeature(fence, crossedPaddock)

    @FeatureAction.undoPlan.handler()
    def undoPlanFeature(self):
        return self.getBasePaddock().undoPlanFeature()

    @FeatureAction.build.handler()
    def buildFeature(self):
        return self.getBasePaddock().buildFeature()

    @FeatureAction.undoBuild.handler()
    def undoBuildFeature(self):
        return self.getBasePaddock().undoBuildFeature()

    @FeatureAction.supersede.handler()
    def supersedeFeature(self, fence):
        return self.getBasePaddock().supersedeFeature(fence)

    @FeatureAction.undoSupersede.handler()
    def undoSupersedeFeature(self):
        return self.getBasePaddock().undoSupersedeFeature()

    @FeatureAction.archive.handler()
    def archiveFeature(self):
        return self.getBasePaddock().archiveFeature()

    @FeatureAction.undoArchive.handler()
    def undoArchiveFeature(self):
        return self.getBasePaddock().undoArchiveFeature()
