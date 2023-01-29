# -*- coding: utf-8 -*-
from ...utils import PLUGIN_NAME
from ..features.watered_area import WateredArea
from ..fields.schemas import WateredAreaSchema
from .derived_watered_area_layer import DerivedWateredAreaLayer
from .persisted_derived_feature_layer import PersistedDerivedFeatureLayer


class WateredAreaLayer(PersistedDerivedFeatureLayer):

    NAME = "Watered Areas"
    STYLE = "watered_area"

    def __init__(self,
                 workspaceFile,
                 derivedWateredAreaLayer: DerivedWateredAreaLayer):
        f"""Create a new {PLUGIN_NAME} watered area layer."""

        super().__init__(WateredArea,
                         workspaceFile,
                         layerName=WateredAreaLayer.NAME,
                         styleName=WateredAreaLayer.STYLE,
                         derivedLayer=derivedWateredAreaLayer)

    def getSchema(self):
        """Return the Schema for this layer."""
        return WateredAreaSchema

    def getWkbType(self):
        """Return the WKB type for this layer."""
        return WateredAreaSchema.wkbType
