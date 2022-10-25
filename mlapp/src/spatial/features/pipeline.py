# -*- coding: utf-8 -*-
from .edits import Edits
from .feature_action import FeatureAction
from .line_feature import LineFeature
from .schemas import PipelineSchema


@PipelineSchema.addSchema()
class Pipeline(LineFeature):

    def __init__(self, featureLayer, elevationLayer=None, existingFeature=None):
        """Create a new LineFeature."""
        super().__init__(featureLayer=featureLayer, elevationLayer=elevationLayer, existingFeature=existingFeature)

    @property
    def title(self):
        return f"Pipeline ({self.id})  ({self.featureLength} km)"

    @property
    def isInfrastructure(self):
        """Return True for Pipeline."""
        return True

    @Edits.persistEdits
    @FeatureAction.plan.handler()
    def planFeature(self, geometry):
        """Plan a Pipeline."""

        self.geometry = geometry

        return Edits.upsert(self)

    @Edits.persistEdits
    @FeatureAction.undoPlan.handler()
    def undoPlanFeature(self):
        """Undo planning a Pipeline."""
        return Edits.delete(self)