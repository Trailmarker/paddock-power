# -*- coding: utf-8 -*-
from qgis.core import QgsFeatureRequest, QgsProject

from ...models.glitch import Glitch
from ..layers.waterpoint_buffer_layer import WaterpointBufferLayer
from ..layers.waterpoint_popup_layer import WaterpointPopupLayer
from .edits import Edits
from .feature_action import FeatureAction
from .point_feature import PointFeature
from ..schemas.schemas import WaterpointSchema, WATERPOINT
from ..schemas.waterpoint_buffer_type import WaterpointBufferType


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

    def addPopupLayer(self):
        """Add a water buffer layer to the project."""
        item = QgsProject.instance().layerTreeRoot().findLayer(self.featureLayer)
        if not item:
            # If the Paddocks layer isn't in the map, don't initialise or add the condition layer.
            return
        self.popupLayer = WaterpointPopupLayer(
            f"{self.waterpointType.value} {self.id} Watered Area",
            self,
            self.waterpointBufferLayer)
        group = item.parent()

        # Insert the buffers layer immediately below this waterpoint, so it and any neighbouring waterpoints
        # remain visible.
        group.insertLayer(group.children().index(item) + 1, self.popupLayer)

    def removePopupLayer(self):
        try:
            if self.popupLayer:
                layer = QgsProject.instance().layerTreeRoot().findLayer(self.popupLayer)
                if layer:
                    layer.parent().removeChildNode(layer)
                self.popupLayer = None
        except BaseException:
            pass

    def onSelectFeature(self):
        if super().onSelectFeature():
            # Returning True from onSelectFeature() means that the feature was newly selected.
            self.addPopupLayer()
            return True
        return False

    def onDeselectFeature(self):
        if super().onDeselectFeature():
            # Returning False from onDeselectFeature() means that the feature was newly deselected.
            self.removePopupLayer()
            return True
        return False

    @Glitch.glitchy()
    def getBuffer(self, distance):
        """Get the waterpoint buffer geometries for this Waterpoint."""

        bufferPoint = self.geometry

        # Sensible limits
        if not bufferPoint or not distance or distance <= 0.0 or distance > 20000.0:
            return None

        # Get 3 km and 5 km buffers
        return bufferPoint.buffer(distance, 10)

    @Glitch.glitchy()
    def getWaterpointBuffers(self):
        waterpointRequest = QgsFeatureRequest().setFilterExpression(f'"{WATERPOINT}" = {self.id}')
        return list(self.waterpointBufferLayer.getFeatures(request=waterpointRequest))

    @Edits.persistFeatures
    @FeatureAction.draft.handler()
    def draftFeature(self, point):
        """Draft a Waterpoint."""
        self.geometry = point

        return Edits.upsert(self)
        """Draft a Waterpoint."""
        self.geometry = point

        return Edits.upsert(self)

    @Edits.persistFeatures
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

    @Edits.persistFeatures
    @FeatureAction.undoPlan.handler()
    def undoPlanFeature(self):
        """Undo the plan of Waterpoint Buffers implied by a Waterpoint."""
        edits = Edits()

        waterpointBuffers = self.getWaterpointBuffers()

        for waterpointBuffer in waterpointBuffers:
            edits = edits.editBefore(waterpointBuffer.undoPlanFeature())

        return Edits.upsert(self).editAfter(edits)
