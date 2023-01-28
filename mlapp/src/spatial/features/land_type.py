# -*- coding: utf-8 -*-
from .persisted_feature import PersistedFeature
from ..fields.schemas import LandTypeSchema


@LandTypeSchema.addSchema()
class LandType(PersistedFeature):

    def __init__(self, featureLayer, existingFeature=None):
        """Create a new LandType."""
        super().__init__(featureLayer, existingFeature)

    @classmethod
    def focusOnSelect(cls):
        """Return True if the app should focus on this type of Feature when selected."""
        return False
