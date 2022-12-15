# -*- coding: utf-8 -*-
from ..schemas.schemas import WaterpointBufferSchema
from .persisted_feature import PersistedFeature


@WaterpointBufferSchema.addSchema()
class WaterpointBuffer(PersistedFeature):

    def __init__(self, featureLayer, existingFeature=None):
        """Create a new Waterpoint Buffer."""
        super().__init__(featureLayer=featureLayer, existingFeature=existingFeature)
