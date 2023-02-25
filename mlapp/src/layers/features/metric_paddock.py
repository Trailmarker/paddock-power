# -*- coding: utf-8 -*-
from ..fields import FID, STATUS, TIMEFRAME, PADDOCK, MetricPaddockSchema
from .base_paddock import BasePaddock


@MetricPaddockSchema.addSchema()
class MetricPaddock(BasePaddock):
    """'Augmented' Base Paddock with all Paddock metrics, and a Timeframe."""

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
    # Note that this means they do not have the @FeatureAction decorators - STATUS is managed by the Base Paddock
    def getBasePaddock(self):
        """Get the Base Paddock that this Metric Paddock is associated with."""
        return self.basePaddockLayer.getFeature(self.PADDOCK)

    def draftFeature(self, geometry, name):
        """Draft a Paddock."""
        return self.getBasePaddock().draftFeature(geometry, name)

    def trashFeature(self):
        return self.getBasePaddock().trashFeature()

    def planFeature(self, fence, crossedPaddock=None):
        return self.getBasePaddock().planFeature(fence, crossedPaddock)

    def undoPlanFeature(self):
        return self.getBasePaddock().undoPlanFeature()

    def buildFeature(self):
        return self.getBasePaddock().buildFeature()

    def undoBuildFeature(self):
        return self.getBasePaddock().undoBuildFeature()

    def supersedeFeature(self, fence):
        return self.getBasePaddock().supersedeFeature(fence)

    def undoSupersedeFeature(self):
        return self.getBasePaddock().undoSupersedeFeature()

    def archiveFeature(self):
        return self.getBasePaddock().archiveFeature()

    def undoArchiveFeature(self):
        return self.getBasePaddock().undoArchiveFeature()
