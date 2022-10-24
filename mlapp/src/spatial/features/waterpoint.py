# -*- coding: utf-8 -*-
from qgis.core import QgsProject

from ...models.glitch import Glitch
from ..layers.waterpoint_buffer_layer import WaterpointBufferLayer
from .edits import Edits
from .feature import FeatureAction
from .point_feature import PointFeature
from .schemas import WaterpointSchema
from .waterpoint_type import WaterpointBufferType


@WaterpointSchema.addSchema()
class Waterpoint(PointFeature):

    def __init__(self, featureLayer, waterpointBufferLayer: WaterpointBufferLayer,
                 elevationLayer=None, existingFeature=None):
        """Create a new LineFeature."""
        super().__init__(featureLayer=featureLayer, elevationLayer=elevationLayer, existingFeature=existingFeature)
        self._waterpointBufferLayerId = waterpointBufferLayer.id()

    @property
    def waterpointBufferLayer(self):
        return QgsProject.instance().mapLayer(self._waterpointBufferLayerId)

    @Glitch.glitchy()
    def getBuffer(self, distance):
        """Get the waterpoint buffer geometries for this Waterpoint."""

        bufferPoint = self.geometry

        # Sensible limits
        if not bufferPoint or not distance or distance <= 0.0 or distance > 20000.0:
            return None

        # Get 3 km and 5 km buffers
        return bufferPoint.buffer(distance)

    @Edits.persistEdits
    @FeatureAction.draft.handler()
    def draftWaterpoint(self, point):
        """Draft a Waterpoint."""
        self.geometry = point

        return Edits.upsert(self)

    @Edits.persistEdits
    @FeatureAction.plan.handler()
    def planWaterpoint(self):
        """Plan a Waterpoint."""

        nearBuffer = self.getBuffer(self.nearBuffer)

        nearWaterpointBuffer = self.waterpointBufferLayer.makeFeature()
        nearWaterpointBuffer.geometry = nearBuffer
        nearWaterpointBuffer.waterpoint = self.id
        nearWaterpointBuffer.waterpointBufferType = WaterpointBufferType.Inner
        nearWaterpointBuffer.bufferDistance = self.nearBuffer
        nearWaterpointBuffer.planFeature()

        farBuffer = self.getBuffer(self.farBuffer)
        farWaterpointBuffer = self.waterpointBufferLayer.makeFeature()
        farWaterpointBuffer.geometry = farBuffer
        farWaterpointBuffer.waterpoint = self.id
        farWaterpointBuffer.waterpointBufferType = WaterpointBufferType.Outer
        farWaterpointBuffer.bufferDistance = self.farBuffer
        farWaterpointBuffer.planFeature()

        return Edits.upsert(self, nearWaterpointBuffer, farWaterpointBuffer)
