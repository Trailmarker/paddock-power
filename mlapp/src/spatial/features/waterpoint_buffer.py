# -*- coding: utf-8 -*-
from ..fields.schemas import WaterpointBufferSchema
from .persisted_feature import PersistedFeature


@WaterpointBufferSchema.addSchema()
class WaterpointBuffer(PersistedFeature):

    def __init__(self, featureLayer, existingFeature=None):
        """Create a new Waterpoint Buffer."""
        super().__init__(featureLayer, existingFeature)

    @classmethod
    def focusOnSelect(cls):
        """Return True if the app should focus on this type of Feature when selected."""
        return False
