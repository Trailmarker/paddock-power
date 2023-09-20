# -*- coding: utf-8 -*-
from ..fields import PipelineSchema
from .edits import Edits
from .feature_action import FeatureAction
from .persisted_feature import PersistedFeature
from .status_feature_mixin import StatusFeatureMixin


@PipelineSchema.addSchema()
class Pipeline(PersistedFeature, StatusFeatureMixin):

    def __init__(self, featureLayer, existingFeature=None):
        """Create a new Pipeline."""
        PersistedFeature.__init__(self, featureLayer, existingFeature)
        StatusFeatureMixin.__init__(self)

    @property
    def TITLE(self):
        return f"{self.NAME} ({self.LENGTH} km)"

    @property
    def isInfrastructure(self):
        """Return True for Pipeline."""
        return True

    def profile(self):
        """Return this Pipeline's profile."""
        if not self._profile:
            self.recalculateElevationProfile()
        return self._profile

    @FeatureAction.draft.handleWithSave()
    def draftFeature(self, geometry):
        """Draft a Pipeline."""
        self.GEOMETRY = geometry
        return Edits.upsert(self)
