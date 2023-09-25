# -*- coding: utf-8 -*-
from ..fields import PropertySchema
from .persisted_feature import PersistedFeature


@PropertySchema.addSchema()
class Property(PersistedFeature):

    @classmethod
    def focusOnSelect(cls):
        """Return True if the app should focus on this type of Feature when selected."""
        return False

    def __init__(self, featureLayer, existingFeature):
        """Create a new AreaFeature."""
        super().__init__(featureLayer, existingFeature)
