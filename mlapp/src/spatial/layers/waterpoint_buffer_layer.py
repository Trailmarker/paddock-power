# -*- coding: utf-8 -*-
from ..features.waterpoint import Waterpoint
from .waterpoint_layer import WaterpointLayer
from .feature_layer import FeatureLayer, FeatureLayerSourceType


class WaterpointBufferLayer(FeatureLayer):

    # STYLE = "waterpoint_buffer"

    def __init__(self, waterpointLayer: WaterpointLayer,
                 sourceType=FeatureLayerSourceType.Memory, layerName=None, gpkgFile=None):
        """Create or open a Waterpoint layer."""

        super().__init__(featureType=Waterpoint,
                         sourceType=sourceType,
                         layerName=layerName,
                         gpkgFile=gpkgFile,
                         styleName=None)

        self.waterpointLyer = waterpointLayer

        self.wrapFeature = lambda feature: Waterpoint(self, waterpointLayer, feature)
