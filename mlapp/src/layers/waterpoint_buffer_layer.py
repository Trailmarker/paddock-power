# -*- coding: utf-8 -*-
from ..utils import PLUGIN_NAME
from .features import WaterpointBuffer
from .persisted_derived_feature_layer import PersistedDerivedFeatureLayer


class WaterpointBufferLayer(PersistedDerivedFeatureLayer):

    NAME = "Waterpoint Buffers"
    STYLE = "waterpoint_buffer"

    @classmethod
    def getFeatureType(cls):
        return WaterpointBuffer

    def __init__(self,
                 workspaceFile,
                 derivedWaterpointBufferLayer):
        f"""Create a new {PLUGIN_NAME} waterpoint buffer layer."""

        super().__init__(workspaceFile,
                         layerName=WaterpointBufferLayer.NAME,
                         styleName=WaterpointBufferLayer.STYLE,
                         derivedLayer=derivedWaterpointBufferLayer)

