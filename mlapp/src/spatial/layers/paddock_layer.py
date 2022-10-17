# -*- coding: utf-8 -*-
from ..features.paddock import Paddock
from .feature_layer import FeatureLayerSourceType, FeatureLayer


class PaddockLayer(FeatureLayer):

    STYLE = "paddock"

    def __init__(self, sourceType=FeatureLayerSourceType.Memory, layerName=None, gpkgFile=None):
        """Create or open a Paddock layer."""

        super().__init__(Paddock,
                         sourceType,
                         layerName,
                         gpkgFile,
                         styleName=PaddockLayer.STYLE)
