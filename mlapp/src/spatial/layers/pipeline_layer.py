# -*- coding: utf-8 -*-
from ..features.pipeline import Pipeline
from .elevation_layer import ElevationLayer
from .feature_layer import FeatureLayer, FeatureLayerSourceType


class PipelineLayer(FeatureLayer):

    STYLE = "pipeline"

    def __init__(self, elevationLayer: ElevationLayer, sourceType=FeatureLayerSourceType.Memory, layerName=None, gpkgFile=None):
        """Create or open a Pipeline layer."""

        super().__init__(Pipeline,
                         sourceType,
                         layerName,
                         gpkgFile,
                         styleName=PipelineLayer.STYLE)

        self.wrapFeature = lambda feature: Pipeline(self, elevationLayer, feature)
