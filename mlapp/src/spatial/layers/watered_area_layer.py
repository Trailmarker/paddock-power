# -*- coding: utf-8 -*-
from ...utils import PLUGIN_NAME
from ..features.watered_area import WateredArea
from .derived_watered_area_layer import DerivedWateredAreaLayer
from .persisted_derived_feature_layer import PersistedDerivedFeatureLayer


class WateredAreaLayer(PersistedDerivedFeatureLayer):

    STYLE = "watered_area"

    def __init__(self, project, gpkgFile, layerName, paddockLayer, waterpointBufferLayer):
        f"""Create a new {PLUGIN_NAME} watered area layer."""

        derivedWateredAreaLayer = DerivedWateredAreaLayer(
            project, f"Derived {layerName}", paddockLayer, waterpointBufferLayer)

        super().__init__(project, gpkgFile, layerName, derivedWateredAreaLayer, styleName=WateredAreaLayer.STYLE)

    def getFeatureType(self):
        """Return the type of feature that this layer contains. Override in subclasses"""
        return WateredArea
