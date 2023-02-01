# -*- coding: utf-8 -*-
from ..fields import BoundarySchema
from .feature import Feature

@BoundarySchema.addSchema()
class Boundary(Feature):

    def __init__(self, featureLayer, existingFeature):
        """Create a new AreaFeature."""
        super().__init__(featureLayer, existingFeature)

    @classmethod
    def focusOnSelect(cls):
        """Return True if the app should focus on this type of Feature when selected."""
        return False
