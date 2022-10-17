# -*- coding: utf-8 -*-
from ..features.boundary import Boundary
from .feature_layer import FeatureLayer, FeatureLayerSourceType


class BoundaryLayer(FeatureLayer):

    STYLE = "boundary"

    def __init__(self, sourceType=FeatureLayerSourceType.Memory, layerName=None, gpkgFile=None):
        """Create or open a Boundary layer."""

        super().__init__(featureType=Boundary,
                         sourceType=sourceType,
                         layerName=layerName,
                         gpkgFile=gpkgFile,
                         styleName=BoundaryLayer.STYLE)

        self.wrapFeature = lambda feature: Boundary(self, feature)
