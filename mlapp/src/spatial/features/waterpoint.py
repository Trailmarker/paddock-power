# -*- coding: utf-8 -*-
from qgis.core import QgsFeatureRequest, QgsProject

from ...models.glitch import Glitch
from ..layers.waterpoint_buffer_layer import WaterpointBufferLayer
from .edits import Edits
from .feature_action import FeatureAction
from .feature_status import FeatureStatus
from .point_feature import PointFeature
from .schemas import WaterpointSchema, WATERPOINT
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

    @property
    def title(self):
        return f"Waterpoint ({self.id}) ({self.waterpointType})"

    @Glitch.glitchy()
    def getBuffer(self, distance):
        """Get the waterpoint buffer geometries for this Waterpoint."""

        bufferPoint = self.geometry

        # Sensible limits
        if not bufferPoint or not distance or distance <= 0.0 or distance > 20000.0:
            return None

        # Get 3 km and 5 km buffers
        return bufferPoint.buffer(distance, 10.0)

    @Glitch.glitchy()
    def getPlannedWaterpointBuffers(self):
        waterpointRequest = QgsFeatureRequest().setFilterExpression(f'"{WATERPOINT}" = {self.id}')

        waterpointBuffers = list(self.waterpointBufferLayer.getFeatures(request=waterpointRequest))

        return [f for f in waterpointBuffers if f.status.match(FeatureStatus.Planned)]

    @Edits.persistEdits
    @FeatureAction.draft.handler()
    def draftFeature(self, point):
        """Draft a Waterpoint."""
        self.geometry = point

        return Edits.upsert(self)
        """Draft a Waterpoint."""
        self.geometry = point

        return Edits.upsert(self)

    @Edits.persistEdits
    @FeatureAction.plan.handler()
    def planFeature(self):
        """Plan a Waterpoint."""
        edits = Edits()

        nearGeometry = self.getBuffer(self.nearBuffer)
        if nearGeometry:
            near = self.waterpointBufferLayer.makeFeature()
            edits.editBefore(near.planFeature(self, nearGeometry, WaterpointBufferType.Near, self.nearBuffer))

        farGeometry = self.getBuffer(self.farBuffer)
        if farGeometry:
            far = self.waterpointBufferLayer.makeFeature()
            edits.editBefore(far.planFeature(self, farGeometry, WaterpointBufferType.Far, self.farBuffer))

        return edits.editAfter(Edits.upsert(self))

    @Edits.persistEdits
    @FeatureAction.undoPlan.handler()
    def undoPlanFeature(self):
        """Undo the plan of Waterpoint Buffers implied by a Waterpoint."""
        edits = Edits()

        plannedWaterpointBuffers = self.getPlannedWaterpointBuffers()

        for waterpointBuffer in plannedWaterpointBuffers:
            edits = edits.editBefore(waterpointBuffer.undoPlanFeature())

        return Edits.upsert(self).editAfter(edits)
