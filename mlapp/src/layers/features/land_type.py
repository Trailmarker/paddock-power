# -*- coding: utf-8 -*-
from ..fields import LandTypeSchema
from .persisted_feature import PersistedFeature


@LandTypeSchema.addSchema()
class LandType(PersistedFeature):

    def __init__(self, featureLayer, existingFeature=None):
        """Create a new LandType."""
        super().__init__(featureLayer, existingFeature)

    @classmethod
    def focusOnSelect(cls):
        """Return True if the app should focus on this type of Feature when selected."""
        return False
