# -*- coding: utf-8 -*-
from ..fields.schemas import PipelineSchema
from .edits import Edits
from .feature_action import FeatureAction
from .status_feature import StatusFeature


@PipelineSchema.addSchema()
class Pipeline(StatusFeature):

    def __init__(self, featureLayer, existingFeature=None):
        """Create a new Pipeline."""
        super().__init__(featureLayer, existingFeature)

    @property
    def TITLE(self):
        return f"Pipeline ({self.FID})  ({self.LENGTH} km)"

    @property
    def isInfrastructure(self):
        """Return True for Pipeline."""
        return True

    @Edits.persistFeatures
    @FeatureAction.draft.handler()
    def draftFeature(self, geometry):
        """Draft a Pipeline."""
        self.GEOMETRY = geometry
        return Edits.upsert(self)

    @Edits.persistFeatures
    @FeatureAction.plan.handler()
    def planFeature(self, geometry):
        """Plan a Pipeline (skip the Draft step)."""
        self.GEOMETRY = geometry
        return Edits.upsert(self)

    @Edits.persistFeatures
    @FeatureAction.undoPlan.handler()
    def undoPlanFeature(self):
        """Undo planning a Pipeline."""
        return Edits.delete(self)
