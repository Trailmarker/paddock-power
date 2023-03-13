# -*- coding: utf-8 -*-
from ..fields import BoundarySchema
from .persisted_feature import PersistedFeature


@BoundarySchema.addSchema()
class Boundary(PersistedFeature):

    @classmethod
    def focusOnSelect(cls):
        """Return True if the app should focus on this type of Feature when selected."""
        return False

    def __init__(self, featureLayer, existingFeature):
        """Create a new AreaFeature."""
        super().__init__(featureLayer, existingFeature)


