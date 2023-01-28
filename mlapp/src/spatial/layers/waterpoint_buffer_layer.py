# -*- coding: utf-8 -*-
from ...utils import PLUGIN_NAME
from ..features.waterpoint_buffer import WaterpointBuffer
from .derived_waterpoint_buffer_layer import DerivedWaterpointBufferLayer
from .persisted_derived_feature_layer import PersistedDerivedFeatureLayer


class WaterpointBufferLayer(PersistedDerivedFeatureLayer):

    NAME = "Waterpoint Buffers"
    STYLE = "waterpoint_buffer"

    def __init__(self,
                 workspaceFile,
                 derivedWaterpointBufferLayer: DerivedWaterpointBufferLayer):
        f"""Create a new {PLUGIN_NAME} waterpoint buffer layer."""

        super().__init__(WaterpointBuffer,
                         workspaceFile,
                         layerName=WaterpointBufferLayer.NAME,
                         styleName=WaterpointBufferLayer.STYLE,
                         derivedLayer=derivedWaterpointBufferLayer)

