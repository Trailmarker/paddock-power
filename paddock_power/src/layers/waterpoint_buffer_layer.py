# -*- coding: utf-8 -*-
from ..utils import PLUGIN_NAME
from .features import WaterpointBuffer
from .derived_waterpoint_buffer_layer import DerivedWaterpointBufferLayer
from .persisted_derived_feature_layer import PersistedDerivedFeatureLayer


class WaterpointBufferLayer(PersistedDerivedFeatureLayer):

    LAYER_NAME = "Waterpoint Buffers"
    STYLE = "waterpoint_buffer"

    @classmethod
    def getFeatureType(cls):
        return WaterpointBuffer

    def __init__(self,
                 workspaceFile,
                 *dependentLayers):
        f"""Create a new {PLUGIN_NAME} waterpoint buffer layer."""

        super().__init__(workspaceFile,
                         WaterpointBufferLayer.defaultName(),
                         WaterpointBufferLayer.defaultStyle(),
                         DerivedWaterpointBufferLayer,
                         dependentLayers)
