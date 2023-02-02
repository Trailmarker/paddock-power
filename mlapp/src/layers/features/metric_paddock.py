# -*- coding: utf-8 -*-
from ..fields import MetricPaddockSchema
from .feature_action import FeatureAction
from .persisted_feature import PersistedFeature
from .status_feature_mixin import StatusFeatureMixin


@MetricPaddockSchema.addSchema()
class MetricPaddock(PersistedFeature, StatusFeatureMixin):

    def __init__(self, featureLayer, existingFeature=None):
        """Initialise a new Metric Paddock."""
        PersistedFeature.__init__(self, featureLayer, existingFeature)
        StatusFeatureMixin.__init__(self)

    @property
    def TITLE(self):
        # return f"#{self.FID} {self.NAME} ({self.AREA:.2f} km²)"
        return f"{self.NAME} ({self.AREA:.2f} km²)"

    @property
    def paddockLayer(self):
        return self.featureLayer.workspace.paddockLayer

    @property
    def paddockLandTypesLayer(self):
        return self.featureLayer.workspace.paddockLandTypesLayer

    # All workflow functions are deferred to the underlying Paddock for this MetricPaddock
    def getPaddock(self):
        """Get the Paddock that this Metric Paddock is associated with."""
        return self.paddockLayer.getFeature(self.PADDOCK)

    @FeatureAction.draft.handler()
    def draftFeature(self, geometry, name):
        """Draft a Paddock."""
        return self.getPaddock().draftFeature(geometry, name)

    @FeatureAction.plan.handler()
    def planFeature(self, fence, crossedPaddock=None):
        return self.getPaddock().planFeature(fence, crossedPaddock)

    @FeatureAction.undoPlan.handler()
    def undoPlanFeature(self):
        return self.getPaddock().undoPlanFeature()

    @FeatureAction.supersede.handler()
    def supersedeFeature(self, fence):
        return self.getPaddock().supersedeFeature(fence)

    @FeatureAction.undoSupersede.handler()
    def undoSupersedeFeature(self):
        return self.getPaddock().undoSupersedeFeature()
