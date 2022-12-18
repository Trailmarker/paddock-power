# -*- coding: utf-8 -*-
from ...utils import PLUGIN_NAME, qgsDebug
from ..features.waterpoint_buffer import WaterpointBuffer
from .derived_waterpoint_buffer_layer import DerivedWaterpointBufferLayer
from .persisted_derived_feature_layer import PersistedDerivedFeatureLayer


class WaterpointBufferLayer(PersistedDerivedFeatureLayer):

    STYLE = "waterpoint_buffer"

    def __init__(self, project, gpkgFile, layerName, waterpointLayer, paddockLayer):
        f"""Create a new {PLUGIN_NAME} waterpoint buffer layer."""

        derivedWaterpointBufferLayer = DerivedWaterpointBufferLayer(
            project, f"Derived {layerName}", waterpointLayer, paddockLayer)

        super().__init__(project, gpkgFile, layerName, derivedWaterpointBufferLayer, styleName=WaterpointBufferLayer.STYLE)

    def getFeatureType(self):
        """Return the type of feature that this layer contains. Override in subclasses"""
        return WaterpointBuffer
