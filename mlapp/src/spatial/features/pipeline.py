# -*- coding: utf-8 -*-
from .feature import addSchema
from .line_feature import LineFeature
from .schemas import PipelineSchema


@addSchema(PipelineSchema)
class Pipeline(LineFeature):

    def __init__(self, featureLayer, elevationLayer=None, existingFeature=None):
        """Create a new LineFeature."""
        super().__init__(featureLayer=featureLayer, elevationLayer=elevationLayer, existingFeature=existingFeature)
