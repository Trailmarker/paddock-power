# -*- coding: utf-8 -*-
from .persisted_feature import PersistedFeature
from ..schemas.schemas import LandSystemSchema


@LandSystemSchema.addSchema()
class LandSystem(PersistedFeature):

    def __init__(self, featureLayer, existingFeature=None):
        """Create a new LandSystem."""
        super().__init__(featureLayer=featureLayer, existingFeature=existingFeature)

    @classmethod
    def focusOnSelect(cls):
        """Return True if the app should focus on this type of Feature when selected."""
        return False
