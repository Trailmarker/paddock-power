# -*- coding: utf-8 -*-
from mlapp.src.spatial.layers.waterpoint_buffer_layer import WaterpointBufferLayer
from ..features.waterpoint import Waterpoint
from .elevation_layer import ElevationLayer
from .feature_layer import FeatureLayer


class WaterpointLayer(FeatureLayer):

    STYLE = "waterpoint"

    @classmethod
    def getFeatureType(cls):
        return Waterpoint

    def __init__(self, gpkgFile, layerName,
                 waterpointBufferLayer: WaterpointBufferLayer,
                 elevationLayer: ElevationLayer):
        """Create or open a Waterpoint layer."""

        super().__init__(gpkgFile, layerName, styleName=WaterpointLayer.STYLE)

        self.waterpointBufferLayer = waterpointBufferLayer
        self.elevationLayer = elevationLayer

    def wrapFeature(self, feature):
        return self.getFeatureType()(self, self.waterpointBufferLayer, self.elevationLayer, feature)
