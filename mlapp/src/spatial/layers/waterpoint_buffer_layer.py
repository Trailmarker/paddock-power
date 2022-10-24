# -*- coding: utf-8 -*-
from ..features.waterpoint_buffer import WaterpointBuffer
from .feature_layer import FeatureLayer


class WaterpointBufferLayer(FeatureLayer):

    # STYLE = "waterpoint_buffer"
    @classmethod
    def getFeatureType(cls):
        return WaterpointBuffer

    def __init__(self, gpkgFile, layerName):
        """Create or open a Waterpoint layer."""

        super().__init__(gpkgFile, layerName, styleName=None)
