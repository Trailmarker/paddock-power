# -*- coding: utf-8 -*-
from ..utils import PLUGIN_NAME
from .features import WateredArea
from .derived_watered_area_layer import DerivedWateredAreaLayer
from .persisted_derived_feature_layer import PersistedDerivedFeatureLayer


class WateredAreaLayer(PersistedDerivedFeatureLayer):

    LAYER_NAME = "Watered Areas"
    STYLE = "watered_area"

    @classmethod
    def getFeatureType(cls):
        return WateredArea

    def __init__(self,
                 workspaceFile,
                 *dependentLayers):
        f"""Create a new {PLUGIN_NAME} watered area layer."""

        super().__init__(workspaceFile,
                         WateredAreaLayer.defaultName(),
                         WateredAreaLayer.defaultStyle(),
                         DerivedWateredAreaLayer,
                         *dependentLayers)
