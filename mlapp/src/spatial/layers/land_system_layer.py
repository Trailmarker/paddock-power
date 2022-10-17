# -*- coding: utf-8 -*-
from ..features.land_system import LandSystem
from .feature_layer import FeatureLayer, FeatureLayerSourceType


class LandSystemLayer(FeatureLayer):

    STYLE = "land_system"

    def __init__(self, sourceType=FeatureLayerSourceType.Memory, layerName=None, gpkgFile=None):
        """Create or open a Pipeline layer."""

        super().__init__(LandSystem,
                         sourceType,
                         layerName,
                         gpkgFile,
                         styleName=self.STYLE)

        self.wrapFeature = lambda feature: LandSystem(self, feature)