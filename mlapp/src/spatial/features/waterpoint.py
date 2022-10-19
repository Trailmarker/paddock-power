# -*- coding: utf-8 -*-
from .point_feature import PointFeature
from .schemas import WaterpointSchema


@WaterpointSchema.addSchema()
class Waterpoint(PointFeature):

    def __init__(self, featureLayer, elevationLayer=None, existingFeature=None):
        """Create a new LineFeature."""
        super().__init__(featureLayer=featureLayer, elevationLayer=elevationLayer, existingFeature=existingFeature)
