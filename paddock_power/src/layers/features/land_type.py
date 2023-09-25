# -*- coding: utf-8 -*-
from ..fields import LandTypeSchema
from .persisted_feature import PersistedFeature


@LandTypeSchema.addSchema()
class LandType(PersistedFeature):

    MINIMUM_OPTIMAL_CAPACITY_PER_AREA = 0
    MAXIMUM_OPTIMAL_CAPACITY_PER_AREA = 100

    def __init__(self, featureLayer, existingFeature=None):
        """Create a new LandType."""
        super().__init__(featureLayer, existingFeature)

    @property
    def NAME(self):
        """Override the default implementation of the NAME property for Land Types."""
        return self.LAND_TYPE_NAME

    @property
    def TITLE(self):
        """Override the default implementation of the TITLE property for Land Types."""
        return self.LAND_TYPE_NAME

    @classmethod
    def focusOnSelect(cls):
        """Return True if the app should focus on this type of Feature when selected."""
        return False
