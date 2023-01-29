# -*- coding: utf-8 -*-
from ..fields.schemas import WaterpointSchema
from ..layers.mixins.popup_feature_mixin import PopupFeatureMixin
from ..layers.waterpoint_popup_layer import WaterpointPopupLayer
from .edits import Edits
from .feature_action import FeatureAction
from .status_feature import StatusFeature


@WaterpointSchema.addSchema()
class Waterpoint(StatusFeature, PopupFeatureMixin):

    NEAREST_GRAZING_RADIUS = 0
    FARTHEST_GRAZING_RADIUS = 20000

    def __init__(self, featureLayer, existingFeature=None):
        """Create a new Waterpoint."""
        StatusFeature.__init__(self, featureLayer, existingFeature)
        PopupFeatureMixin.__init__(self)

    @property
    def popupLayerTypes(self): 
        return [WaterpointPopupLayer]

    @property
    def waterpointBufferLayer(self):
        return self.workspaceLayer("WaterpointBufferLayer")

    @property
    def TITLE(self):
        if self.NAME and self.NAME != "NULL":
            return f"{self.NAME} ({self.WATERPOINT_TYPE})"
        return f"Waterpoint ({self.FID}) ({self.WATERPOINT_TYPE})"

    @Edits.persistFeatures
    @FeatureAction.draft.handler()
    def draftFeature(self, point):
        """Draft a Waterpoint."""
        self.GEOMETRY = point

        return Edits.upsert(self)
