# -*- coding: utf-8 -*-
from ..fields import WaterpointSchema
from .edits import Edits
from .feature_action import FeatureAction
from .persisted_feature import PersistedFeature
from .status_feature_mixin import StatusFeatureMixin


@WaterpointSchema.addSchema()
class Waterpoint(PersistedFeature, StatusFeatureMixin):

    NEAREST_GRAZING_RADIUS = 0
    FARTHEST_GRAZING_RADIUS = 20000

    def __init__(self, featureLayer, existingFeature=None):
        """Create a new Waterpoint."""
        PersistedFeature.__init__(self, featureLayer, existingFeature)
        StatusFeatureMixin.__init__(self)

    @property
    def waterpointBufferLayer(self):
        return self.featureLayer.workspace.waterpointBufferLayer

    @property
    def TITLE(self):
        if self.NAME and self.NAME != "NULL":
            return f"{self.NAME} ({self.WATERPOINT_TYPE})"
        return f"Waterpoint ({self.FID}) ({self.WATERPOINT_TYPE})"

    @FeatureAction.draft.handleWithSave()
    def draftFeature(self, point):
        """Draft a Waterpoint."""
        self.GEOMETRY = point

        return Edits.upsert(self)

    def onSelectFeature(self):
        """Do the stuff we'd normally do, but also add the popup layer."""
        super().onSelectFeature()

        if self.WATERPOINT_TYPE.givesWater():
            for layerType in self.popupLayerTypes:
                self.addPopupLayer(layerType)

    def onDeselectFeature(self):
        """Do the stuff we'd normally do, but also remove the popup layer."""
        super().onDeselectFeature()

        self.removeAllPopupLayers()
