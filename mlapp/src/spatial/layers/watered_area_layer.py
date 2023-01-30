# -*- coding: utf-8 -*-
from ...utils import PLUGIN_NAME
from ..features.watered_area import WateredArea
from .derived_watered_area_layer import DerivedWateredAreaLayer
from .persisted_derived_feature_layer import PersistedDerivedFeatureLayer


class WateredAreaLayer(PersistedDerivedFeatureLayer):

    NAME = "Watered Areas"
    STYLE = "watered_area"

    @classmethod
    def getFeatureType(cls):
        return WateredArea

    def __init__(self,
                 workspaceFile,
                 derivedWateredAreaLayer: DerivedWateredAreaLayer):
        f"""Create a new {PLUGIN_NAME} watered area layer."""

        super().__init__(workspaceFile,
                         layerName=WateredAreaLayer.NAME,
                         styleName=WateredAreaLayer.STYLE,
                         derivedLayer=derivedWateredAreaLayer)
