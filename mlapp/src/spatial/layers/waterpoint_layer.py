# -*- coding: utf-8 -*-
from ..features.waterpoint import Waterpoint
from .elevation_layer import ElevationLayer
from .feature_layer import FeatureLayer, FeatureLayerSourceType


class WaterpointLayer(FeatureLayer):

    STYLE = "waterpoint"

    def __init__(self, elevationLayer: ElevationLayer,
                 sourceType=FeatureLayerSourceType.Memory, layerName=None, gpkgFile=None):
        """Create or open a Waterpoint layer."""

        super().__init__(featureType=Waterpoint,
                         sourceType=sourceType,
                         layerName=layerName,
                         gpkgFile=gpkgFile,
                         styleName=WaterpointLayer.STYLE)

        self.wrapFeature = lambda feature: Waterpoint(self, elevationLayer, feature)
