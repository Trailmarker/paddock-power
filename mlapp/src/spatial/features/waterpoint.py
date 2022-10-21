# -*- coding: utf-8 -*-
from ...models.glitch import Glitch
from .point_feature import PointFeature
from .schemas import WaterpointSchema

from qgis.core import QgsFeatureRequest, QgsGeometry, QgsLineString, QgsPoint

from ...models.glitch import Glitch
from ...utils import qgsDebug
from .edits import Edits
from .feature import FeatureAction
from .feature_status import FeatureStatus
from .line_feature import LineFeature
from .schemas import FenceSchema, BUILD_FENCE


@WaterpointSchema.addSchema()
class Waterpoint(PointFeature):

    def __init__(self, featureLayer, elevationLayer=None, existingFeature=None):
        """Create a new LineFeature."""
        super().__init__(featureLayer=featureLayer, elevationLayer=elevationLayer, existingFeature=existingFeature)

    @Glitch.glitchy()
    def getBuffers(self):
        """Get the waterpoint buffer geometries for this Waterpoint."""

        bufferPoint = self.geometry

        if not bufferPoint:
            return None, None

        # Get 3 km and 5 km buffers
        return bufferPoint.buffer(3000), bufferPoint.buffer(5000)

    @Edits.persistEdits
    @FeatureAction.draft.handler()
    def draftWaterpoint(self):
        """Draft a Waterpoint."""
        
        return Edits.upsert(self)

    @Edits.persistEdits
    @FeatureAction.plan.handler()
    def planWaterpoint(self):
        """Plan a Waterpoint."""

        edits = Edits()

        # Derive waterpoint buffers

        return Edits.upsert(self)
